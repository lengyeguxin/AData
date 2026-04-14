"""
hots_userCollector - hots_user表拉取器模板

字段数量: 2个（严格按照Schema定义）
API接口: hots_user
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class HotsuserCollector(BaseCollector):
    """hots_user表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='hots_user',
            api_name='hots_user',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照hots_user_schema.sql定义，完整2个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（2个字段，严格按照schema定义顺序）
        """
        return (
            item.get('name'),
            item.get('orgs'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整2个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "name, orgs, updated_at"

        placeholders = ', '.join(['?'] * 2) + ', NOW()'

        update_fields = "name = excluded.name, orgs = excluded.orgs, updated_at = NOW()"

        return f"""
            INSERT INTO hots_user (name, orgs, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (account)
            DO UPDATE SET {update_fields}
        """