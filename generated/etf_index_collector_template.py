"""
etf_indexCollector - etf_index表拉取器模板

字段数量: 8个（严格按照Schema定义）
API接口: etf_index
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class EtfindexCollector(BaseCollector):
    """etf_index表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='etf_index',
            api_name='etf_index',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照etf_index_schema.sql定义，完整8个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（8个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            item.get('indx_name'),
            item.get('indx_csname'),
            item.get('pub_party_name'),
            convert_date_format(item.get('pub_date')),
            convert_date_format(item.get('base_date')),
            item.get('bp'),
            item.get('adj_circle'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整8个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, indx_name, indx_csname, pub_party_name, pub_date, base_date, bp, adj_circle, updated_at"

        placeholders = ', '.join(['?'] * 8) + ', NOW()'

        update_fields = "indx_name = excluded.indx_name, indx_csname = excluded.indx_csname, pub_party_name = excluded.pub_party_name, pub_date = excluded.pub_date, base_date = excluded.base_date, bp = excluded.bp, adj_circle = excluded.adj_circle, updated_at = NOW()"

        return f"""
            INSERT INTO etf_index (ts_code, indx_name, indx_csname, pub_party_name, pub_date, base_date, bp, adj_circle, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code)
            DO UPDATE SET {update_fields}
        """