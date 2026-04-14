"""
WeeklyCollector - 周线行情拉取器

严格按照CSV文档：
- 接口名称：stk_week_month_adj（VIP接口）
- 接口参数：ts_code={股票代码}, start_date={游标+1}, end_date={计算周五}, freq=week
- 文档地址：https://tushare.pro/document/2?doc_id=365
- 游标策略：daily_trade（按交易日记录）
- VIP接口特性：周线、月线数据
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class WeeklyCollector(BaseCollector):
    """周线行情拉取器（P1行情表，VIP接口，按交易日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化WeeklyCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='stock_weekly',
            api_name='stk_week_month_adj',  # VIP接口（严格按照CSV文档）
            date_field='trade_date',
            vip_interface=True  # VIP接口
        )

    def collect(self, **kwargs) -> List[Dict]:
        """
        拉取周线数据（自动添加freq参数）

        Args:
            **kwargs: API参数（如trade_date, ts_code等）

        Returns:
            周线数据列表

        注意：
            - 自动添加freq='week'参数（API必填）
            - 支持按trade_date拉取（DataFetcher调用）
            - 支持按start_date/end_date范围拉取（手动调用）
        """
        # 自动添加freq参数（API必填）
        kwargs['freq'] = 'week'

        # 调用父类collect方法
        return super().collect(**kwargs)

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照stock_weekly_schema.sql定义，完整21个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（21个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('trade_date')),
            convert_date_format(item.get('end_date')),
            item.get('freq'),
            item.get('open'),
            item.get('high'),
            item.get('low'),
            item.get('close'),
            item.get('pre_close'),
            item.get('open_qfq'),
            item.get('high_qfq'),
            item.get('low_qfq'),
            item.get('close_qfq'),
            item.get('open_hfq'),
            item.get('high_hfq'),
            item.get('low_hfq'),
            item.get('close_hfq'),
            item.get('vol'),
            item.get('amount'),
            item.get('change'),
            item.get('pct_chg'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整21个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, trade_date, end_date, freq, open, high, low, close, pre_close, open_qfq, high_qfq, low_qfq, close_qfq, open_hfq, high_hfq, low_hfq, close_hfq, vol, amount, change, pct_chg, updated_at"

        placeholders = ', '.join(['?'] * 21) + ', NOW()'

        update_fields = "end_date = excluded.end_date, freq = excluded.freq, open = excluded.open, high = excluded.high, low = excluded.low, close = excluded.close, pre_close = excluded.pre_close, open_qfq = excluded.open_qfq, high_qfq = excluded.high_qfq, low_qfq = excluded.low_qfq, close_qfq = excluded.close_qfq, open_hfq = excluded.open_hfq, high_hfq = excluded.high_hfq, low_hfq = excluded.low_hfq, close_hfq = excluded.close_hfq, vol = excluded.vol, amount = excluded.amount, change = excluded.change, pct_chg = excluded.pct_chg, updated_at = NOW()"

        return f"""
            INSERT INTO stock_weekly (ts_code, trade_date, end_date, freq, open, high, low, close, pre_close, open_qfq, high_qfq, low_qfq, close_qfq, open_hfq, high_hfq, low_hfq, close_hfq, vol, amount, change, pct_chg, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET {update_fields}
        """


def run_by_date_range(self, start_date: str, end_date: str) -> int:
        """
        按日期范围拉取周线数据（VIP接口）

        Args:
            start_date: 开始日期（YYYYMMDD）
            end_date: 结束日期（YYYYMMDD）

        Returns:
            保存的记录数
        """
        # collect()方法会自动添加freq='week'
        data = self.collect(start_date=start_date, end_date=end_date)
        return self.save(data)