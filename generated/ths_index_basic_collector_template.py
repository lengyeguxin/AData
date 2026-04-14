"""
ths_index_basicCollector - ths_index_basic表拉取器模板

字段数量: 6个（严格按照Schema定义）
API接口: ths_index
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class ThsindexbasicCollector(BaseCollector):
    """ths_index_basic表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='ths_index_basic',
            api_name='ths_index',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照ths_index_basic_schema.sql定义，完整6个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（6个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            item.get('name'),
            item.get('count'),
            item.get('exchange'),
            convert_date_format(item.get('list_date')),
            item.get('type'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整6个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, name, count, exchange, list_date, type, updated_at"

        placeholders = ', '.join(['?'] * 6) + ', NOW()'

        update_fields = "name = excluded.name, count = excluded.count, exchange = excluded.exchange, list_date = excluded.list_date, type = excluded.type, updated_at = NOW()"

        return f"""
            INSERT INTO ths_index_basic (ts_code, name, count, exchange, list_date, type, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code)
            DO UPDATE SET {update_fields}
        """