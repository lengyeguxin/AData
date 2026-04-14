"""
dividendCollector - dividend表拉取器模板

字段数量: 16个（严格按照Schema定义）
API接口: dividend
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class DividendCollector(BaseCollector):
    """dividend表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='dividend',
            api_name='dividend',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照dividend_schema.sql定义，完整16个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（16个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('end_date')),
            convert_date_format(item.get('ann_date')),
            item.get('div_proc'),
            item.get('stk_div'),
            item.get('stk_bo_rate'),
            item.get('stk_co_rate'),
            item.get('cash_div'),
            item.get('cash_div_tax'),
            convert_date_format(item.get('record_date')),
            convert_date_format(item.get('ex_date')),
            convert_date_format(item.get('pay_date')),
            item.get('div_listdate'),
            convert_date_format(item.get('imp_ann_date')),
            convert_date_format(item.get('base_date')),
            item.get('base_share'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整16个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, end_date, ann_date, div_proc, stk_div, stk_bo_rate, stk_co_rate, cash_div, cash_div_tax, record_date, ex_date, pay_date, div_listdate, imp_ann_date, base_date, base_share, updated_at"

        placeholders = ', '.join(['?'] * 16) + ', NOW()'

        update_fields = "end_date = excluded.end_date, div_proc = excluded.div_proc, stk_div = excluded.stk_div, stk_bo_rate = excluded.stk_bo_rate, stk_co_rate = excluded.stk_co_rate, cash_div = excluded.cash_div, cash_div_tax = excluded.cash_div_tax, ex_date = excluded.ex_date, pay_date = excluded.pay_date, div_listdate = excluded.div_listdate, imp_ann_date = excluded.imp_ann_date, base_date = excluded.base_date, base_share = excluded.base_share, updated_at = NOW()"

        return f"""
            INSERT INTO dividend (ts_code, end_date, ann_date, div_proc, stk_div, stk_bo_rate, stk_co_rate, cash_div, cash_div_tax, record_date, ex_date, pay_date, div_listdate, imp_ann_date, base_date, base_share, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, ann_date, record_date)
            DO UPDATE SET {update_fields}
        """