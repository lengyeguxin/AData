"""
Dashboard数据库连接模块

独立的数据库访问层，不依赖后端代码
只提供只读操作，强制使用快照数据库，绝不连接主数据库adata.db
"""

import duckdb
from pathlib import Path
from typing import List, Tuple, Optional, Dict
import logging

logger = logging.getLogger('dashboard')


class DashboardDatabase:
    """Dashboard专用数据库连接（只读，强制使用快照数据库）"""

    def __init__(self, db_path: Optional[str] = None):
        """
        初始化数据库连接

        Args:
            db_path: 数据库路径（仅用于定位快照数据库，实际连接快照）

        注意：Dashboard永远只连接快照数据库adata_snapshot.db，不连接主数据库adata.db
        """
        if db_path is None:
            # 默认使用项目根目录的database/adata_snapshot.db
            project_root = Path(__file__).parent.parent.parent.parent
            snapshot_path = project_root / 'database' / 'adata_snapshot.db'
        else:
            # 智能路径转换：如果是主数据库路径，转为快照路径；已经是快照路径，直接使用
            if '_snapshot.db' in db_path:
                # 已经是快照路径，直接使用
                snapshot_path = Path(db_path)
                logger.debug(f"使用现有快照路径: {db_path}")
            else:
                # 主数据库路径，转换为快照路径
                snapshot_path = Path(db_path.replace('.db', '_snapshot.db'))
                logger.debug(f"转换主数据库路径为快照路径: {db_path} → {snapshot_path}")

        # 检查快照数据库是否存在
        if not snapshot_path.exists():
            logger.error(f"快照数据库不存在: {snapshot_path}")
            raise FileNotFoundError(f"快照数据库不存在: {snapshot_path}")

        self.db_path = str(snapshot_path)
        logger.info(f"Dashboard连接快照数据库: {self.db_path}")

        # 建立连接（只读模式）
        try:
            self.conn = duckdb.connect(self.db_path, read_only=True)
            logger.info(f"数据库连接成功（只读模式）")
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
            # 区分错误类型：列不存在是预期情况（尝试不同日期字段），使用DEBUG级别
            error_msg = str(e)
            if 'not found in FROM clause' in error_msg or 'Candidate bindings:' in error_msg:
                logger.debug(f"SQL查询失败（预期情况）: {query[:100]}... - {e}")
            else:
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