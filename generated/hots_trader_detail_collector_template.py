"""
hots_trader_detailCollector - hots_trader_detail表拉取器模板

字段数量: 9个（严格按照Schema定义）
API接口: hots_trader_detail
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class HotstraderdetailCollector(BaseCollector):
    """hots_trader_detail表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='hots_trader_detail',
            api_name='hots_trader_detail',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照hots_trader_detail_schema.sql定义，完整9个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（9个字段，严格按照schema定义顺序）
        """
        return (
            convert_date_format(item.get('trade_date')),
            item.get('ts_code'),
            item.get('ts_name'),
            item.get('buy_amount'),
            item.get('sell_amount'),
            item.get('net_amount'),
            item.get('hm_name'),
            item.get('hm_orgs'),
            item.get('tag'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整9个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "trade_date, ts_code, ts_name, buy_amount, sell_amount, net_amount, hm_name, hm_orgs, tag, updated_at"

        placeholders = ', '.join(['?'] * 9) + ', NOW()'

        update_fields = "ts_name = excluded.ts_name, buy_amount = excluded.buy_amount, sell_amount = excluded.sell_amount, net_amount = excluded.net_amount, hm_name = excluded.hm_name, hm_orgs = excluded.hm_orgs, tag = excluded.tag, updated_at = NOW()"

        return f"""
            INSERT INTO hots_trader_detail (trade_date, ts_code, ts_name, buy_amount, sell_amount, net_amount, hm_name, hm_orgs, tag, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (account, ts_code, trade_date)
            DO UPDATE SET {update_fields}
        """