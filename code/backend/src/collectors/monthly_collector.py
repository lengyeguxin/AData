"""
MonthlyCollector - 月线行情拉取器

严格按照CSV文档：
- 接口名称：stk_week_month_adj（VIP接口）
- 接口参数：ts_code={股票代码}, start_date={游标+1}, end_date={计算周五}, freq=month
- 文档地址：https://tushare.pro/document/2?doc_id=158
- 游标策略：daily_trade（按交易日记录）
- VIP接口特性：周线、月线数据
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class MonthlyCollector(BaseCollector):
    """月线行情拉取器（P1行情表，VIP接口，按交易日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化MonthlyCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='stock_monthly',
            api_name='stk_week_month_adj',  # VIP接口（严格按照CSV文档）
            date_field='trade_date',
            vip_interface=True  # VIP接口
        )

    def collect_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """
        按日期范围拉取月线数据（VIP接口）

        Args:
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）

        Returns:
            月线数据列表

        注意：
            - 使用VIP接口stk_week_month_adj
            - freq='month'（月线）
            - 按日期范围拉取（不是单个交易日）
        """
        self.logger.info(f"拉取月线数据（VIP接口）: start_date={start_date}, end_date={end_date}")

        # 严格按照CSV文档参数
        data = self.collect(
            start_date=start_date,
            end_date=end_date,
            freq='month'  # 月线（CSV文档明确要求）
        )

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
            INSERT INTO stock_monthly (
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

    def run_by_date_range(self, start_date: str, end_date: str) -> int:
        """
        拉取并保存指定日期范围数据（VIP接口）

        Args:
            start_date: 开始日期（YYYYMMDD）
            end_date: 结束日期（YYYYMMDD）

        Returns:
            保存的记录数
        """
        data = self.collect_by_date_range(start_date, end_date)
        return self.save(data)