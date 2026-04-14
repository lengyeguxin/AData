"""
etf_adj_factorCollector - etf_adj_factor表拉取器模板

字段数量: 3个（严格按照Schema定义）
API接口: fund_adj
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class EtfadjfactorCollector(BaseCollector):
    """etf_adj_factor表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='etf_adj_factor',
            api_name='fund_adj',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照etf_adj_factor_schema.sql定义，完整3个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（3个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('trade_date')),
            item.get('adj_factor'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整3个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, trade_date, adj_factor, updated_at"

        placeholders = ', '.join(['?'] * 3) + ', NOW()'

        update_fields = "adj_factor = excluded.adj_factor, updated_at = NOW()"

        return f"""
            INSERT INTO etf_adj_factor (ts_code, trade_date, adj_factor, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET {update_fields}
        """