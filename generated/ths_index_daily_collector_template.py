"""
ths_index_dailyCollector - ths_index_daily表拉取器模板

字段数量: 14个（严格按照Schema定义）
API接口: ths_daily
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class ThsindexdailyCollector(BaseCollector):
    """ths_index_daily表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='ths_index_daily',
            api_name='ths_daily',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照ths_index_daily_schema.sql定义，完整14个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（14个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('trade_date')),
            item.get('close'),
            item.get('open'),
            item.get('high'),
            item.get('low'),
            item.get('pre_close'),
            item.get('avg_price'),
            item.get('change'),
            item.get('pct_change'),
            item.get('vol'),
            item.get('turnover_rate'),
            item.get('total_mv'),
            item.get('float_mv'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整14个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, trade_date, close, open, high, low, pre_close, avg_price, change, pct_change, vol, turnover_rate, total_mv, float_mv, updated_at"

        placeholders = ', '.join(['?'] * 14) + ', NOW()'

        update_fields = "close = excluded.close, open = excluded.open, high = excluded.high, low = excluded.low, pre_close = excluded.pre_close, avg_price = excluded.avg_price, change = excluded.change, pct_change = excluded.pct_change, vol = excluded.vol, turnover_rate = excluded.turnover_rate, total_mv = excluded.total_mv, float_mv = excluded.float_mv, updated_at = NOW()"

        return f"""
            INSERT INTO ths_index_daily (ts_code, trade_date, close, open, high, low, pre_close, avg_price, change, pct_change, vol, turnover_rate, total_mv, float_mv, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET {update_fields}
        """