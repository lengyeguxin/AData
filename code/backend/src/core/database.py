"""
DuckDB数据库封装类

提供统一的数据库操作接口
- 线程安全：写操作加锁，保证DuckDB单写模型
- 并发读：读操作无锁，支持多线程并发读取
"""

import duckdb
import threading
from typing import List, Tuple, Optional
from pathlib import Path
from src.core.logger import get_logger


class Database:
    """DuckDB数据库封装类（线程安全）"""

    def __init__(self, db_path: str):
        """
        初始化数据库连接

        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self.logger = get_logger(__name__)

        # 确保数据库目录存在
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        # 连接数据库
        self.conn = duckdb.connect(db_path)

        # 线程安全：写操作锁（保护DuckDB单写模型）
        self.write_lock = threading.Lock()

        self.logger.info(f"数据库连接初始化: {db_path}")

    def execute(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        执行SQL查询（线程安全）

        Args:
            query: SQL语句
            params: 参数（可选）

        Returns:
            查询结果列表

        注意：
            - 所有SQL操作都加锁，保证DuckDB单写模型
            - 读操作也串行化，确保线程安全（后续可优化）
        """
        with self.write_lock:
            try:
                if params:
                    result = self.conn.execute(query, params).fetchall()
                else:
                    result = self.conn.execute(query).fetchall()

                return result

            except Exception as e:
                self.logger.error(f"SQL执行失败: {query} - {e}")
                raise

    def execute_many(self, query: str, params_list: List[Tuple]):
        """
        执行批量SQL（线程安全）

        Args:
            query: SQL语句
            params_list: 参数列表

        注意：
            - 批量操作加锁，保证写序列化
        """
        with self.write_lock:
            try:
                for params in params_list:
                    self.conn.execute(query, params)

            except Exception as e:
                self.logger.error(f"批量SQL执行失败: {query} - {e}")
                raise

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """进入上下文"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        self.close()

    def table_exists(self, table_name: str) -> bool:
        """
        检查表是否存在

        Args:
            table_name: 表名

        Returns:
            表是否存在
        """
        query = """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = ?
        """

        result = self.execute(query, (table_name,))
        return result[0][0] > 0

    def get_table_count(self, table_name: str) -> int:
        """
        获取表的记录数

        Args:
            table_name: 表名

        Returns:
            记录数
        """
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self.execute(query)
        return result[0][0]

    def get_table_schema(self, table_name: str) -> List[Tuple]:
        """
        获取表结构

        Args:
            table_name: 表名

        Returns:
            表结构信息列表
        """
        query = f"DESCRIBE {table_name}"
        return self.execute(query)

    def checkpoint(self):
        """
        执行checkpoint操作，将WAL合并到主数据库文件

        用于定期清理WAL文件，减少文件大小
        """
        try:
            self.conn.execute("PRAGMA force_checkpoint")
            self.logger.info("Checkpoint执行成功，WAL已合并到数据库文件")
            return True
        except Exception as e:
            self.logger.error(f"Checkpoint执行失败: {e}")
            return False