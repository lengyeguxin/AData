"""
trade_calendarCollector - trade_calendar表拉取器模板

字段数量: 4个（严格按照Schema定义）
API接口: trade_cal
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class TradecalendarCollector(BaseCollector):
    """trade_calendar表拉取器"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='trade_calendar',
            api_name='trade_cal',
        )


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照trade_calendar_schema.sql定义，完整4个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（4个字段，严格按照schema定义顺序）
        """
        return (
            item.get('exchange'),
            convert_date_format(item.get('cal_date')),
            item.get('is_open'),
            convert_date_format(item.get('pretrade_date')),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整4个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "exchange, cal_date, is_open, pretrade_date, updated_at"

        placeholders = ', '.join(['?'] * 4) + ', NOW()'

        update_fields = "is_open = excluded.is_open, pretrade_date = excluded.pretrade_date, updated_at = NOW()"

        return f"""
            INSERT INTO trade_calendar (exchange, cal_date, is_open, pretrade_date, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (exchange, cal_date)
            DO UPDATE SET {update_fields}
        """