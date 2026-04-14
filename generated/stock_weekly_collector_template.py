"""
stock_weeklyCollector - stock_weekly表拉取器模板

字段数量: 21个（严格按照Schema定义）
API接口: stk_week_month_adj
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class StockweeklyCollector(BaseCollector):
    """stock_weekly表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='stock_weekly',
            api_name='stk_week_month_adj',
        )


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