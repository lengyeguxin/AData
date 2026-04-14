"""
同花顺指数日线Collector

表：ths_index_daily
API：ths_daily
- 文档地址：https://tushare.pro/document/2?doc_id=260
游标策略：daily_trade（按交易日）
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class THSIndexDailyCollector(BaseCollector):
    """同花顺指数日线Collector"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='ths_index_daily',
            api_name='ths_daily',
            date_field='trade_date',
            vip_interface=False
        )

    def collect_by_date(self, trade_date: str) -> List[Dict]:
        """
        按交易日拉取数据

        Args:
            trade_date: 交易日期（YYYYMMDD格式）

        Returns:
            数据列表
        """
        self.logger.info(f"拉取同花顺指数日线: trade_date={trade_date}")
        return self.collect(trade_date=trade_date)

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照ths_index_daily_schema.sql定义，完整14个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（14个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('trade_date')),
            item.get('close'),
            item.get('open'),
            item.get('high'),
            item.get('low'),
            item.get('pre_close'),
            item.get('avg_price'),
            item.get('change'),
            item.get('pct_change'),
            item.get('vol'),
            item.get('turnover_rate'),
            item.get('total_mv'),
            item.get('float_mv'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整14个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, trade_date, close, open, high, low, pre_close, avg_price, change, pct_change, vol, turnover_rate, total_mv, float_mv, updated_at"

        placeholders = ', '.join(['?'] * 14) + ', NOW()'

        update_fields = "close = excluded.close, open = excluded.open, high = excluded.high, low = excluded.low, pre_close = excluded.pre_close, avg_price = excluded.avg_price, change = excluded.change, pct_change = excluded.pct_change, vol = excluded.vol, turnover_rate = excluded.turnover_rate, total_mv = excluded.total_mv, float_mv = excluded.float_mv, updated_at = NOW()"

        return f"""
            INSERT INTO ths_index_daily (ts_code, trade_date, close, open, high, low, pre_close, avg_price, change, pct_change, vol, turnover_rate, total_mv, float_mv, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET {update_fields}
        """


def run_by_date(self, trade_date: str) -> int:
        """
        按交易日拉取并保存

        Args:
            trade_date: 交易日期

        Returns:
            保存的记录数
        """
        data = self.collect_by_date(trade_date)
        return self.save(data)