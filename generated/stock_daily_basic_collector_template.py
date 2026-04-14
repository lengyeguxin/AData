"""
stock_daily_basicCollector - stock_daily_basic表拉取器模板

字段数量: 18个（严格按照Schema定义）
API接口: daily_basic
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class StockdailybasicCollector(BaseCollector):
    """stock_daily_basic表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='stock_daily_basic',
            api_name='daily_basic',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照stock_daily_basic_schema.sql定义，完整18个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（18个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('trade_date')),
            item.get('close'),
            item.get('turnover_rate'),
            item.get('turnover_rate_f'),
            item.get('volume_ratio'),
            item.get('pe'),
            item.get('pe_ttm'),
            item.get('pb'),
            item.get('ps'),
            item.get('ps_ttm'),
            item.get('dv_ratio'),
            item.get('dv_ttm'),
            item.get('total_share'),
            item.get('float_share'),
            item.get('free_share'),
            item.get('total_mv'),
            item.get('circ_mv'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整18个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, trade_date, close, turnover_rate, turnover_rate_f, volume_ratio, pe, pe_ttm, pb, ps, ps_ttm, dv_ratio, dv_ttm, total_share, float_share, free_share, total_mv, circ_mv, updated_at"

        placeholders = ', '.join(['?'] * 18) + ', NOW()'

        update_fields = "close = excluded.close, turnover_rate = excluded.turnover_rate, turnover_rate_f = excluded.turnover_rate_f, volume_ratio = excluded.volume_ratio, pe = excluded.pe, pe_ttm = excluded.pe_ttm, pb = excluded.pb, ps = excluded.ps, ps_ttm = excluded.ps_ttm, dv_ratio = excluded.dv_ratio, dv_ttm = excluded.dv_ttm, total_share = excluded.total_share, float_share = excluded.float_share, free_share = excluded.free_share, total_mv = excluded.total_mv, circ_mv = excluded.circ_mv, updated_at = NOW()"

        return f"""
            INSERT INTO stock_daily_basic (ts_code, trade_date, close, turnover_rate, turnover_rate_f, volume_ratio, pe, pe_ttm, pb, ps, ps_ttm, dv_ratio, dv_ttm, total_share, float_share, free_share, total_mv, circ_mv, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET {update_fields}
        """