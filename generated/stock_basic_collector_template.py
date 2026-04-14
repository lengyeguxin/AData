"""
stock_basicCollector - stock_basic表拉取器模板

字段数量: 17个（严格按照Schema定义）
API接口: stock_basic
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class StockbasicCollector(BaseCollector):
    """stock_basic表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='stock_basic',
            api_name='stock_basic',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照stock_basic_schema.sql定义，完整17个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（17个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            item.get('symbol'),
            item.get('name'),
            item.get('area'),
            item.get('industry'),
            item.get('fullname'),
            item.get('enname'),
            item.get('cnspell'),
            item.get('market'),
            item.get('exchange'),
            item.get('curr_type'),
            item.get('list_status'),
            convert_date_format(item.get('list_date')),
            convert_date_format(item.get('delist_date')),
            item.get('is_hs'),
            item.get('act_name'),
            item.get('act_ent_type'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整17个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, symbol, name, area, industry, fullname, enname, cnspell, market, exchange, curr_type, list_status, list_date, delist_date, is_hs, act_name, act_ent_type, updated_at"

        placeholders = ', '.join(['?'] * 17) + ', NOW()'

        update_fields = "symbol = excluded.symbol, name = excluded.name, area = excluded.area, industry = excluded.industry, fullname = excluded.fullname, enname = excluded.enname, cnspell = excluded.cnspell, market = excluded.market, exchange = excluded.exchange, curr_type = excluded.curr_type, list_status = excluded.list_status, list_date = excluded.list_date, delist_date = excluded.delist_date, is_hs = excluded.is_hs, act_name = excluded.act_name, act_ent_type = excluded.act_ent_type, updated_at = NOW()"

        return f"""
            INSERT INTO stock_basic (ts_code, symbol, name, area, industry, fullname, enname, cnspell, market, exchange, curr_type, list_status, list_date, delist_date, is_hs, act_name, act_ent_type, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code)
            DO UPDATE SET {update_fields}
        """