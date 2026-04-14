"""
etf_basicCollector - etf_basic表拉取器模板

字段数量: 14个（严格按照Schema定义）
API接口: etf_basic
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class EtfbasicCollector(BaseCollector):
    """etf_basic表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='etf_basic',
            api_name='etf_basic',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照etf_basic_schema.sql定义，完整14个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（14个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            item.get('csname'),
            item.get('extname'),
            item.get('cname'),
            item.get('index_code'),
            item.get('index_name'),
            convert_date_format(item.get('setup_date')),
            convert_date_format(item.get('list_date')),
            item.get('list_status'),
            item.get('exchange'),
            item.get('mgr_name'),
            item.get('custod_name'),
            item.get('mgt_fee'),
            item.get('etf_type'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整14个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, csname, extname, cname, index_code, index_name, setup_date, list_date, list_status, exchange, mgr_name, custod_name, mgt_fee, etf_type, updated_at"

        placeholders = ', '.join(['?'] * 14) + ', NOW()'

        update_fields = "csname = excluded.csname, extname = excluded.extname, cname = excluded.cname, index_code = excluded.index_code, index_name = excluded.index_name, setup_date = excluded.setup_date, list_date = excluded.list_date, list_status = excluded.list_status, exchange = excluded.exchange, mgr_name = excluded.mgr_name, custod_name = excluded.custod_name, mgt_fee = excluded.mgt_fee, etf_type = excluded.etf_type, updated_at = NOW()"

        return f"""
            INSERT INTO etf_basic (ts_code, csname, extname, cname, index_code, index_name, setup_date, list_date, list_status, exchange, mgr_name, custod_name, mgt_fee, etf_type, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code)
            DO UPDATE SET {update_fields}
        """