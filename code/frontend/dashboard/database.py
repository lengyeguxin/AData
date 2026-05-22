"""
Dashboard数据库连接模块

独立的数据库访问层，不依赖后端代码
只提供只读操作，直接连接PostgreSQL主数据库（只读模式）
"""

import psycopg2
import psycopg2.pool
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import logging
import yaml

logger = logging.getLogger('dashboard')


class DashboardDatabase:
    """Dashboard专用数据库连接（只读，连接PostgreSQL主数据库）"""

    def __init__(self, db_config: Optional[Dict] = None):
        """
        初始化数据库连接

        Args:
            db_config: 数据库配置字典（可选）
                {
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'adatadb',
                    'user': 'adata',
                    'password': 'adata258963'
                }
                如果为None，从后端config.yaml读取

        注意：Dashboard直接连接PostgreSQL主数据库（只读模式）
        """
        if db_config is None:
            # 从后端配置文件读取PostgreSQL连接信息
            backend_config_path = Path(__file__).parent.parent.parent.parent / 'code' / 'backend' / 'config' / 'config.yaml'
            if backend_config_path.exists():
                with open(backend_config_path, 'r', encoding='utf-8') as f:
                    backend_config = yaml.safe_load(f)
                    db_config = backend_config.get('database', {})
                    logger.info(f"从后端配置读取PostgreSQL连接信息: {backend_config_path}")
            else:
                # 使用默认PostgreSQL配置
                db_config = {
                    'host': 'localhost',
                    'port': 5432,
                    'database': 'adatadb',
                    'user': 'adata',
                    'password': 'adata258963'
                }
                logger.info("使用默认PostgreSQL配置")

        self.db_config = db_config
        logger.info(f"Dashboard连接PostgreSQL: {db_config['host']}:{db_config['port']}/{db_config['database']}")

        # 建立连接池（只读模式）
        try:
            self.pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=5,
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['database'],
                user=db_config['user'],
                password=db_config['password']
            )
            logger.info("PostgreSQL连接池初始化成功（只读模式）")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise

    def execute(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        执行SQL查询（只读）

        Args:
            query: SQL查询语句
            params: 参数（可选，PostgreSQL使用%s占位符）

        Returns:
            查询结果列表
        """
        conn = None
        try:
            conn = self.pool.getconn()
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                result = cursor.fetchall()
                return result
        except Exception as e:
            error_msg = str(e)
            if 'not found in FROM clause' in error_msg or 'does not exist' in error_msg:
                logger.debug(f"SQL查询失败（预期情况）: {query[:100]}... - {e}")
            else:
                logger.error(f"SQL执行失败: {query[:100]}... - {e}")
            raise
        finally:
            if conn:
                self.pool.putconn(conn)

    def get_table_list(self) -> List[str]:
        """
        获取所有表名列表

        Returns:
            表名列表
        """
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """
        result = self.execute(query)
        return [row[0] for row in result]

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
        return result[0][0] if result else 0

    def get_table_schema(self, table_name: str) -> List[Tuple]:
        """
        获取表的schema信息

        Args:
            table_name: 表名

        Returns:
            列信息列表（column_name, data_type, is_nullable）
        """
        query = """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """
        return self.execute(query, (table_name,))

    def close(self):
        """关闭数据库连接池"""
        if self.pool:
            self.pool.closeall()
            logger.info("PostgreSQL连接池已关闭")

    def __enter__(self):
        """支持上下文管理"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理"""
        self.close()