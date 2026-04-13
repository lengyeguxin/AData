"""
元数据查询模块

封装所有数据库元数据查询逻辑，提供统一的接口供监控页面使用
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional

# 添加项目路径到Python路径
project_root = Path(__file__).parent.parent.parent
backend_path = project_root / 'backend'
sys.path.insert(0, str(backend_path))

from src.core.database import Database
from dashboard.utils.table_info import get_table_info
from dashboard.utils.formatters import extract_column_comments


class DatabaseMetadata:
    """数据库元数据查询器"""

    def __init__(self, db_path: str = None, use_snapshot: bool = True):
        """
        初始化元数据查询器

        Args:
            db_path: 数据库文件路径，默认使用项目根目录下的data/adata.db
            use_snapshot: 是否使用快照副本进行读取（读写分离）
        """
        if db_path is None:
            # 使用绝对路径，避免工作目录问题
            project_root = Path(__file__).parent.parent.parent.parent  # 回到AData根目录
            db_path = str(project_root / 'database' / 'adata.db')

        # 如果启用快照模式，优先使用快照副本
        if use_snapshot:
            snapshot_path = db_path.replace('.db', '_snapshot.db')
            snapshot_file = Path(snapshot_path)
            if snapshot_file.exists():
                self.db_path = snapshot_path
                self.using_snapshot = True
            else:
                self.db_path = db_path
                self.using_snapshot = False
        else:
            self.db_path = db_path
            self.using_snapshot = False

        self.db = Database(self.db_path)

    def get_table_list(self) -> List[str]:
        """
        获取所有表名列表

        Returns:
            表名列表
        """
        try:
            # DuckDB查询所有用户表（排除系统表）
            query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'main'
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """
            result = self.db.execute(query)
            return [row[0] for row in result]
        except Exception:
            return []

    def get_table_row_count(self, table_name: str) -> int:
        """
        查询表记录数

        Args:
            table_name: 表名

        Returns:
            记录数
        """
        try:
            # 对于大表，使用元数据估算以提高性能
            large_tables = ['stock_daily', 'stock_daily_basic', 'adj_factor', 'stock_weekly']

            if table_name in large_tables:
                # 使用DuckDB的统计信息估算
                query = """
                    SELECT estimated_size
                    FROM duckdb_tables()
                    WHERE table_name = ?
                """
                result = self.db.execute(query, (table_name,))
                if result and result[0]:
                    return int(result[0][0])

            # 对于小表，使用精确计数
            query = f"SELECT COUNT(*) FROM {table_name}"
            result = self.db.execute(query)
            return result[0][0] if result else 0

        except Exception:
            return 0

    def get_table_latest_date(self, table_name: str) -> Optional[str]:
        """
        智能查询表最新数据时间

        查询策略：按优先级尝试多个日期字段
        优先级：trade_date > ann_date > end_date > cal_date > list_date > reg_date > in_date > out_date > updated_at

        Args:
            table_name: 表名

        Returns:
            最新日期字符串（YYYY-MM-DD格式），如果查询失败返回None
        """
        # 日期字段候选列表（按优先级排序）
        date_field_candidates = [
            'trade_date',    # 行情表（stock_daily、index_daily、etf_daily等）
            'ann_date',      # 财务表（income、balancesheet、cashflow等）
            'end_date',      # 财务报告期
            'cal_date',      # 交易日历
            'list_date',     # 股票列表、指数列表、ETF列表
            'reg_date',      # 游资账户注册日期
            'in_date',       # 概念板块纳入日期
            'out_date',      # 概念板块剔除日期
            'updated_at'     # 最后更新时间
        ]

        # 按优先级依次尝试查询
        for date_field in date_field_candidates:
            try:
                query = f"SELECT MAX({date_field}) FROM {table_name} WHERE {date_field} IS NOT NULL"
                result = self.db.execute(query)
                if result and result[0] and result[0][0]:
                    date_val = result[0][0]
                    # 转换为字符串（只取日期部分）
                    return str(date_val)[:10] if len(str(date_val)) >= 10 else str(date_val)
            except Exception:
                # 该字段不存在，继续尝试下一个字段
                continue

        return None

    def get_table_size_mb(self, table_name: str) -> float:
        """
        查询表大小（MB）

        Args:
            table_name: 表名

        Returns:
            表大小（MB）
        """
        try:
            # 使用pragate_table_info获取表的统计信息
            query = f"PRAGMA table_info('{table_name}')"
            result = self.db.execute(query)

            # DuckDB不直接提供表大小，使用行数估算
            # 每行平均约100字节（粗略估算）
            row_count = self.get_table_row_count(table_name)
            estimated_size_mb = (row_count * 100) / 1024.0 / 1024.0
            return estimated_size_mb
        except Exception:
            return 0.0

    def get_table_schema(self, table_name: str) -> List[Dict]:
        """
        获取表结构信息（包括字段注释）

        Args:
            table_name: 表名

        Returns:
            字段信息列表 [{column_name, data_type, is_nullable, comment}]
        """
        try:
            # 1. 查询基本字段信息
            query = """
                SELECT
                    column_name,
                    data_type,
                    is_nullable
                FROM information_schema.columns
                WHERE table_name = ?
                ORDER BY ordinal_position
            """
            columns = self.db.execute(query, (table_name,))

            # 2. 尝试从schema.py提取注释
            comments = self._get_table_comments_from_schema(table_name)

            # 3. 组合结果
            result = []
            for col in columns:
                result.append({
                    'column_name': col[0],
                    'data_type': col[1],
                    'is_nullable': 'YES' if col[2] == 'YES' else 'NO',
                    'comment': comments.get(col[0], '')
                })

            return result

        except Exception:
            return []

    def _get_table_comments_from_schema(self, table_name: str) -> Dict[str, str]:
        """
        从schema.py提取表字段注释

        Args:
            table_name: 表名

        Returns:
            字段注释字典 {column_name: comment}
        """
        try:
            # 导入schema定义
            from src.storage import schema as schema_module

            # 构建CREATE语句变量名
            create_var_name = f'CREATE_{table_name.upper()}'

            # 对于滚动表，使用模板
            if table_name.startswith('cyq_performance_'):
                create_var_name = 'CREATE_CYQ_PERFORMANCE_TEMPLATE'
            elif table_name.startswith('margin_detail_'):
                create_var_name = 'CREATE_MARGIN_DETAIL_TEMPLATE'

            # 获取CREATE语句
            create_statement = getattr(schema_module, create_var_name, None)

            if create_statement:
                return extract_column_comments(create_statement)

        except Exception:
            pass

        return {}

    def get_all_tables_info(self) -> List[Dict]:
        """
        获取所有表的详细信息

        Returns:
            表信息列表 [{
                'table_name': str,
                'chinese_name': str,
                'category': str,
                'description': str,
                'row_count': int,
                'latest_date': str,
                'date_field': str,
                'update_frequency': str,
                'size_mb': float
            }]
        """
        all_tables = self.get_table_list()
        result = []

        for table_name in all_tables:
            # 获取表配置信息
            info = get_table_info(table_name)

            # 查询记录数
            row_count = self.get_table_row_count(table_name)

            # 查询最新数据时间
            latest_date = self.get_table_latest_date(table_name)

            # 查询表大小
            size_mb = self.get_table_size_mb(table_name)

            result.append({
                'table_name': table_name,
                'chinese_name': info['chinese_name'],
                'category': info['category'],
                'description': info['description'],
                'row_count': row_count,
                'latest_date': latest_date,
                'date_field': info['date_field'],
                'update_frequency': info['update_frequency'],
                'size_mb': size_mb
            })

        return result

    def get_database_stats(self) -> Dict:
        """
        获取数据库整体统计信息

        Returns:
            统计信息字典 {
                'total_tables': int,
                'total_rows': int,
                'total_size_mb': float,
                'categories': Dict[str, int],
                'oldest_data': str,
                'newest_data': str
            }
        """
        tables_info = self.get_all_tables_info()

        # 统计总记录数
        total_rows = sum(t['row_count'] for t in tables_info)

        # 获取数据库文件实际大小
        import os
        try:
            db_path = self.db_path
            if os.path.exists(db_path):
                total_size_mb = os.path.getsize(db_path) / 1024.0 / 1024.0
            else:
                total_size_mb = 0.0
        except Exception:
            total_size_mb = 0.0

        # 统计各分类表数量
        categories = {}
        for table in tables_info:
            cat = table['category']
            categories[cat] = categories.get(cat, 0) + 1

        # 查找数据时间范围
        dates = [t['latest_date'] for t in tables_info if t['latest_date']]
        oldest_data = min(dates) if dates else None
        newest_data = max(dates) if dates else None

        return {
            'total_tables': len(tables_info),
            'total_rows': total_rows,
            'total_size_mb': total_size_mb,
            'categories': categories,
            'oldest_data': oldest_data,
            'newest_data': newest_data
        }

    def close(self):
        """关闭数据库连接"""
        self.db.close()

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.close()