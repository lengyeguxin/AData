"""
ths_concept_memberCollector - ths_concept_member表拉取器模板

字段数量: 7个（严格按照Schema定义）
API接口: ths_member
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class ThsconceptmemberCollector(BaseCollector):
    """ths_concept_member表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='ths_concept_member',
            api_name='ths_member',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照ths_concept_member_schema.sql定义，完整7个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（7个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            item.get('con_code'),
            item.get('con_name'),
            item.get('weight'),
            convert_date_format(item.get('in_date')),
            convert_date_format(item.get('out_date')),
            item.get('is_new'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整7个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, con_code, con_name, weight, in_date, out_date, is_new, updated_at"

        placeholders = ', '.join(['?'] * 7) + ', NOW()'

        update_fields = "con_name = excluded.con_name, weight = excluded.weight, in_date = excluded.in_date, out_date = excluded.out_date, is_new = excluded.is_new, updated_at = NOW()"

        return f"""
            INSERT INTO ths_concept_member (ts_code, con_code, con_name, weight, in_date, out_date, is_new, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, con_code)
            DO UPDATE SET {update_fields}
        """