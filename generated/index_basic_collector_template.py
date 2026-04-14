"""
index_basicCollector - index_basic表拉取器模板

字段数量: 12个（严格按照Schema定义）
API接口: index_basic
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class IndexbasicCollector(BaseCollector):
    """index_basic表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='index_basic',
            api_name='index_basic',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照index_basic_schema.sql定义，完整12个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（12个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            item.get('name'),
            item.get('fullname'),
            item.get('market'),
            item.get('publisher'),
            item.get('index_type'),
            item.get('category'),
            convert_date_format(item.get('base_date')),
            item.get('base_point'),
            convert_date_format(item.get('list_date')),
            item.get('weight_rule'),
            convert_date_format(item.get('exp_date')),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整12个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, name, fullname, market, publisher, index_type, category, base_date, base_point, list_date, weight_rule, exp_date, updated_at"

        placeholders = ', '.join(['?'] * 12) + ', NOW()'

        update_fields = "name = excluded.name, fullname = excluded.fullname, market = excluded.market, publisher = excluded.publisher, index_type = excluded.index_type, category = excluded.category, base_date = excluded.base_date, base_point = excluded.base_point, list_date = excluded.list_date, weight_rule = excluded.weight_rule, exp_date = excluded.exp_date, updated_at = NOW()"

        return f"""
            INSERT INTO index_basic (ts_code, name, fullname, market, publisher, index_type, category, base_date, base_point, list_date, weight_rule, exp_date, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code)
            DO UPDATE SET {update_fields}
        """