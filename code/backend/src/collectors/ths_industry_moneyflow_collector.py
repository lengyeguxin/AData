"""
同花顺行业资金流向Collector

表：ths_industry_moneyflow
API：moneyflow_ind_ths
- 文档地址：https://tushare.pro/document/2?doc_id=343
游标策略：daily_trade（按交易日）
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class THSIndustryMoneyflowCollector(BaseCollector):
    """同花顺行业资金流向Collector"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='ths_industry_moneyflow',
            api_name='moneyflow_ind_ths',
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
        self.logger.info(f"拉取同花顺行业资金流向: trade_date={trade_date}")
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
            item.get('industry'),
            item.get('lead_stock'),
            item.get('close'),
            item.get('pct_change'),
            item.get('company_num'),
            item.get('pct_change_stock'),
            item.get('close_price'),
            item.get('net_buy_amount'),
            item.get('net_sell_amount'),
            item.get('net_amount')
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO ths_industry_moneyflow (
                ts_code, trade_date, industry, lead_stock, close,
                pct_change, company_num, pct_change_stock, close_price,
                net_buy_amount, net_sell_amount, net_amount, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET
                industry = excluded.industry,
                lead_stock = excluded.lead_stock,
                close = excluded.close,
                pct_change = excluded.pct_change,
                company_num = excluded.company_num,
                pct_change_stock = excluded.pct_change_stock,
                close_price = excluded.close_price,
                net_buy_amount = excluded.net_buy_amount,
                net_sell_amount = excluded.net_sell_amount,
                net_amount = excluded.net_amount,
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