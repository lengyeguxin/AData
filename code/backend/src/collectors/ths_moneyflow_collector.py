"""
同花顺资金流向Collector

表：ths_moneyflow
API：moneyflow_ths
- 文档地址：https://tushare.pro/document/2?doc_id=348
游标策略：daily_trade（按交易日）
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class THSMoneyflowCollector(BaseCollector):
    """同花顺资金流向Collector"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='ths_moneyflow',
            api_name='moneyflow_ths',
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
        self.logger.info(f"拉取同花顺资金流向: trade_date={trade_date}")
        return self.collect(trade_date=trade_date)

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照ths_moneyflow_schema.sql定义，完整13个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（13个字段，严格按照schema定义顺序）
        """
        return (
            convert_date_format(item.get('trade_date')),
            item.get('ts_code'),
            item.get('name'),
            item.get('pct_change'),
            item.get('latest'),
            item.get('net_amount'),
            item.get('net_d5_amount'),
            item.get('buy_lg_amount'),
            item.get('buy_lg_amount_rate'),
            item.get('buy_md_amount'),
            item.get('buy_md_amount_rate'),
            item.get('buy_sm_amount'),
            item.get('buy_sm_amount_rate'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整13个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "trade_date, ts_code, name, pct_change, latest, net_amount, net_d5_amount, buy_lg_amount, buy_lg_amount_rate, buy_md_amount, buy_md_amount_rate, buy_sm_amount, buy_sm_amount_rate, updated_at"

        placeholders = ', '.join(['?'] * 13) + ', NOW()'

        update_fields = "name = excluded.name, pct_change = excluded.pct_change, latest = excluded.latest, net_amount = excluded.net_amount, net_d5_amount = excluded.net_d5_amount, buy_lg_amount = excluded.buy_lg_amount, buy_lg_amount_rate = excluded.buy_lg_amount_rate, buy_md_amount = excluded.buy_md_amount, buy_md_amount_rate = excluded.buy_md_amount_rate, buy_sm_amount = excluded.buy_sm_amount, buy_sm_amount_rate = excluded.buy_sm_amount_rate, updated_at = NOW()"

        return f"""
            INSERT INTO ths_moneyflow (trade_date, ts_code, name, pct_change, latest, net_amount, net_d5_amount, buy_lg_amount, buy_lg_amount_rate, buy_md_amount, buy_md_amount_rate, buy_sm_amount, buy_sm_amount_rate, updated_at)
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