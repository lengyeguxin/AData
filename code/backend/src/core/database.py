"""
PostgreSQL数据库封装类

提供统一的数据库操作接口
- 单例模式：全局共享一个连接池
- 线程安全：使用连接池保证并发安全
- 连接池：支持多线程并发读写
"""

import psycopg2
import psycopg2.pool
import threading
from typing import List, Tuple, Optional
from pathlib import Path
from src.core.logger import get_logger


class Database:
    """PostgreSQL数据库封装类（单例模式，线程安全）"""

    # 单例实例和锁
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, db_config: dict):
        """
        单例模式：同一个db_config返回同一个实例

        Args:
            db_config: 数据库连接配置字典
                {
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'adatadb',
                    'user': 'adata',
                    'password': 'adata258963'
                }
        """
        # 使用数据库连接字符串作为key
        conn_key = f"{db_config['host']}:{db_config['port']}/{db_config['database']}"

        with cls._lock:
            if conn_key not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[conn_key] = instance
            return cls._instances[conn_key]

    def __init__(self, db_config: dict):
        """
        初始化数据库连接池（单例，只初始化一次）

        Args:
            db_config: 数据库连接配置字典
        """
        # 避免重复初始化
        conn_key = f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
        if hasattr(self, '_initialized') and self._initialized:
            return

        self.db_config = db_config
        self.conn_key = conn_key
        self.logger = get_logger(__name__)

        # 创建连接池（ThreadedConnectionPool支持多线程并发）
        try:
            self.pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=10,
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['database'],
                user=db_config['user'],
                password=db_config['password']
            )

            self._initialized = True
            self._closed = False
            self.logger.info(f"PostgreSQL连接池初始化成功: {conn_key}")

        except Exception as e:
            self.logger.error(f"PostgreSQL连接池初始化失败: {e}")
            raise

    def execute(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        执行SQL查询（线程安全，使用连接池）

        Args:
            query: SQL语句
            params: 参数（可选）

        Returns:
            查询结果列表

        注意：
            - 从连接池获取连接，执行后归还
            - PostgreSQL使用%s占位符（DuckDB也支持）
        """
        conn = None
        try:
            # 从连接池获取连接
            conn = self.pool.getconn()

            with conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                result = cursor.fetchall()
                return result

        except Exception as e:
            self.logger.error(f"SQL执行失败: {query} - {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            # 归还连接到连接池
            if conn:
                self.pool.putconn(conn)

    def execute_many(self, query: str, params_list: List[Tuple]):
        """
        执行批量SQL（线程安全，使用连接池）

        Args:
            query: SQL语句
            params_list: 参数列表

        注意：
            - 批量操作使用单个连接事务
            - 失败时自动回滚
        """
        conn = None
        try:
            conn = self.pool.getconn()

            with conn.cursor() as cursor:
                for params in params_list:
                    cursor.execute(query, params)

                # 提交事务
                conn.commit()

        except Exception as e:
            self.logger.error(f"批量SQL执行失败: {query} - {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                self.pool.putconn(conn)

    def close(self):
        """
        关闭连接池并清除单例实例

        注意：关闭后会清除单例，下次使用会重新创建连接池
        """
        if self._closed:
            return

        try:
            # 关闭所有连接池中的连接
            self.pool.closeall()
            self.logger.info(f"PostgreSQL连接池已关闭: {self.conn_key}")

        except Exception as e:
            self.logger.warning(f"关闭连接池失败: {e}")

        self._closed = True

        # 清除单例实例
        if self.conn_key in Database._instances:
            del Database._instances[self.conn_key]

    def __enter__(self):
        """进入上下文"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        self.close()

    def table_exists(self, table_name: str) -> bool:
        """
        检查表是否存在（PostgreSQL语法）

        Args:
            table_name: 表名

        Returns:
            表是否存在
        """
        query = """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = ?
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
        获取表结构（PostgreSQL语法）

        Args:
            table_name: 表名

        Returns:
            表结构信息列表（列名、类型等）
        """
        query = """
            SELECT column_name, data_type, character_maximum_length,
                   is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = ?
            ORDER BY ordinal_position
        """
        return self.execute(query, (table_name,))