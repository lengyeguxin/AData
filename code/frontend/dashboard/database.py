"""
Dashboard数据库连接模块

独立的数据库访问层，不依赖后端代码
只提供只读操作，使用快照数据库避免冲突
"""

import duckdb
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import logging

logger = logging.getLogger('dashboard')


class DashboardDatabase:
    """Dashboard专用数据库连接（只读）"""

    def __init__(self, db_path: Optional[str] = None, use_snapshot: bool = True):
        """
        初始化数据库连接

        Args:
            db_path: 数据库路径（默认使用项目根目录）
            use_snapshot: 是否使用快照数据库（默认True，避免与后端冲突）
        """
        if db_path is None:
            # 默认使用项目根目录的database/adata.db
            project_root = Path(__file__).parent.parent.parent.parent
            db_path = str(project_root / 'database' / 'adata.db')

        # 如果启用快照模式，优先使用快照副本
        if use_snapshot:
            snapshot_path = db_path.replace('.db', '_snapshot.db')
            snapshot_file = Path(snapshot_path)
            if snapshot_file.exists():
                self.db_path = snapshot_path
                logger.info(f"使用快照数据库: {snapshot_path}")
            else:
                self.db_path = db_path
                logger.warning(f"快照数据库不存在，使用主数据库: {db_path}")
        else:
            self.db_path = db_path

        # 建立连接（只读模式）
        try:
            self.conn = duckdb.connect(self.db_path, read_only=True)
            logger.info(f"数据库连接成功: {self.db_path}")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise

    def execute(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        执行SQL查询（只读）

        Args:
            query: SQL查询语句
            params: 参数（可选）

        Returns:
            查询结果列表
        """
        try:
            if params:
                result = self.conn.execute(query, params).fetchall()
            else:
                result = self.conn.execute(query).fetchall()
            return result
        except Exception as e:
            logger.error(f"SQL执行失败: {query[:100]}... - {e}")
            raise

    def get_table_list(self) -> List[str]:
        """
        获取所有表名列表

        Returns:
            表名列表
        """
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'main'
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
            WHERE table_name = ?
            ORDER BY ordinal_position
        """
        return self.execute(query, (table_name,))

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logger.info("数据库连接已关闭")

    def __enter__(self):
        """支持上下文管理"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持上下文管理"""
        self.close()