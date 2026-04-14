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
        提取字段值

        Args:
            item: 单条数据

        Returns:
            字段值元组
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('trade_date')),
            item.get('open'),
            item.get('high'),
            item.get('low'),
            item.get('close'),
            item.get('vol'),
            item.get('amount'),
            item.get('pct_chg')
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO ths_index_daily (
                ts_code, trade_date, open, high, low, close, vol, amount, pct_chg, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET
                open = excluded.open,
                high = excluded.high,
                low = excluded.low,
                close = excluded.close,
                vol = excluded.vol,
                amount = excluded.amount,
                pct_chg = excluded.pct_chg,
                updated_at = NOW()
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