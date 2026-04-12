"""
ETFDailyCollector - ETF日线行情拉取器

严格按照CSV文档：
- 接口名称：fund_daily
- 接口参数：trade_date={游标+1}
- 文档地址：https://tushare.pro/document/2?doc_id=117
- 游标策略：daily_trade（按交易日记录）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class ETFDailyCollector(BaseCollector):
    """ETF日线行情拉取器（P1行情表，按交易日每日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化ETFDailyCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='etf_daily',
            api_name='fund_daily',  # 严格按照CSV文档
            date_field='trade_date',
            vip_interface=False  # 标准接口
        )

    def collect_by_date(self, trade_date: str) -> List[Dict]:
        """
        拉取指定交易日的所有ETF日线数据

        Args:
            trade_date: 交易日期（YYYYMMDD格式）

        Returns:
            ETF日线数据列表

        示例：
            collect_by_date('20260409') → 拉取2026-04-09所有ETF日线数据
        """
        self.logger.info(f"拉取ETF日线数据: trade_date={trade_date}")

        # 严格按照CSV文档参数
        data = self.collect(trade_date=trade_date)

        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照p1_schema.sql定义）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组
        """
        return (
            item.get('ts_code'),        # ts_code
            convert_date_format(item.get('trade_date')),  # trade_date
            item.get('open'),           # open
            item.get('high'),           # high
            item.get('low'),            # low
            item.get('close'),          # close
            item.get('vol'),            # vol
            item.get('amount'),         # amount
            item.get('pct_chg'),        # pct_chg
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO etf_daily (
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
        拉取并保存指定交易日数据

        Args:
            trade_date: 交易日期（YYYYMMDD）

        Returns:
            保存的记录数
        """
        data = self.collect_by_date(trade_date)
        return self.save(data)