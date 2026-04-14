"""
ths_concept_moneyflowCollector - ths_concept_moneyflow表拉取器模板

字段数量: 12个（严格按照Schema定义）
API接口: moneyflow_cnt_ths
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class ThsconceptmoneyflowCollector(BaseCollector):
    """ths_concept_moneyflow表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='ths_concept_moneyflow',
            api_name='moneyflow_cnt_ths',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照ths_concept_moneyflow_schema.sql定义，完整12个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（12个字段，严格按照schema定义顺序）
        """
        return (
            convert_date_format(item.get('trade_date')),
            item.get('ts_code'),
            item.get('name'),
            item.get('lead_stock'),
            item.get('close_price'),
            item.get('pct_change'),
            item.get('industry_index'),
            item.get('company_num'),
            item.get('pct_change_stock'),
            item.get('net_buy_amount'),
            item.get('net_sell_amount'),
            item.get('net_amount'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整12个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "trade_date, ts_code, name, lead_stock, close_price, pct_change, industry_index, company_num, pct_change_stock, net_buy_amount, net_sell_amount, net_amount, updated_at"

        placeholders = ', '.join(['?'] * 12) + ', NOW()'

        update_fields = "name = excluded.name, lead_stock = excluded.lead_stock, close_price = excluded.close_price, pct_change = excluded.pct_change, industry_index = excluded.industry_index, company_num = excluded.company_num, pct_change_stock = excluded.pct_change_stock, net_buy_amount = excluded.net_buy_amount, net_sell_amount = excluded.net_sell_amount, net_amount = excluded.net_amount, updated_at = NOW()"

        return f"""
            INSERT INTO ths_concept_moneyflow (trade_date, ts_code, name, lead_stock, close_price, pct_change, industry_index, company_num, pct_change_stock, net_buy_amount, net_sell_amount, net_amount, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET {update_fields}
        """