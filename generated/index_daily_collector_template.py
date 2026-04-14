"""
index_dailyCollector - index_daily表拉取器模板

字段数量: 11个（严格按照Schema定义）
API接口: index_daily
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class IndexdailyCollector(BaseCollector):
    """index_daily表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='index_daily',
            api_name='index_daily',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照index_daily_schema.sql定义，完整11个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（11个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('trade_date')),
            item.get('close'),
            item.get('open'),
            item.get('high'),
            item.get('low'),
            item.get('pre_close'),
            item.get('change'),
            item.get('pct_chg'),
            item.get('vol'),
            item.get('amount'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整11个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, trade_date, close, open, high, low, pre_close, change, pct_chg, vol, amount, updated_at"

        placeholders = ', '.join(['?'] * 11) + ', NOW()'

        update_fields = "close = excluded.close, open = excluded.open, high = excluded.high, low = excluded.low, pre_close = excluded.pre_close, change = excluded.change, pct_chg = excluded.pct_chg, vol = excluded.vol, amount = excluded.amount, updated_at = NOW()"

        return f"""
            INSERT INTO index_daily (ts_code, trade_date, close, open, high, low, pre_close, change, pct_chg, vol, amount, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET {update_fields}
        """