"""
WeeklyCollector - 周线行情拉取器

严格按照CSV文档：
- 接口名称：stk_week_month_adj（VIP接口）
- 接口参数：ts_code={股票代码}, start_date={游标+1}, end_date={计算周五}, freq=week
- 文档地址：https://tushare.pro/document/2?doc_id=365
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


class WeeklyCollector(BaseCollector):
    """周线行情拉取器（P1行情表，VIP接口，按交易日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化WeeklyCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='stock_weekly',
            api_name='stk_week_month_adj',  # VIP接口（严格按照CSV文档）
            date_field='trade_date',
            vip_interface=True  # VIP接口
        )

    def collect_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """
        按日期范围拉取周线数据（VIP接口）

        Args:
            start_date: 开始日期（YYYYMMDD格式）
            end_date: 结束日期（YYYYMMDD格式）

        Returns:
            周线数据列表

        注意：
            - 使用VIP接口stk_week_month_adj
            - freq='week'（周线）
            - 按日期范围拉取（不是单个交易日）
        """
        self.logger.info(f"拉取周线数据（VIP接口）: start_date={start_date}, end_date={end_date}")

        # 严格按照CSV文档参数
        data = self.collect(
            start_date=start_date,
            end_date=end_date,
            freq='week'  # 周线（CSV文档明确要求）
        )

        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照p1_schema.sql定义）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（字段顺序：ts_code, trade_date, end_date, freq, pre_close, open, high, low, close, change, pct_chg, vol, amount, open_qfq, high_qfq, low_qfq, close_qfq, open_hfq, high_hfq, low_hfq, close_hfq）
        """
        return (
            item.get('ts_code'),        # ts_code
            convert_date_format(item.get('trade_date')),  # trade_date
            convert_date_format(item.get('end_date')),    # end_date（计算截至日期）
            item.get('freq'),           # freq（频率：week）
            item.get('pre_close'),      # pre_close（上一周期收盘价）
            item.get('open'),           # open
            item.get('high'),           # high
            item.get('low'),            # low
            item.get('close'),          # close
            item.get('change'),         # change（涨跌额）
            item.get('pct_chg'),        # pct_chg
            item.get('vol'),            # vol
            item.get('amount'),         # amount
            item.get('open_qfq'),       # open_qfq（前复权开盘价）
            item.get('high_qfq'),       # high_qfq（前复权最高价）
            item.get('low_qfq'),        # low_qfq（前复权最低价）
            item.get('close_qfq'),      # close_qfq（前复权收盘价）
            item.get('open_hfq'),       # open_hfq（后复权开盘价）
            item.get('high_hfq'),       # high_hfq（后复权最高价）
            item.get('low_hfq'),        # low_hfq（后复权最低价）
            item.get('close_hfq'),      # close_hfq（后复权收盘价）
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO stock_weekly (
                ts_code, trade_date, end_date, freq, pre_close, open, high, low, close,
                change, pct_chg, vol, amount,
                open_qfq, high_qfq, low_qfq, close_qfq,
                open_hfq, high_hfq, low_hfq, close_hfq,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET
                end_date = excluded.end_date,
                freq = excluded.freq,
                pre_close = excluded.pre_close,
                open = excluded.open,
                high = excluded.high,
                low = excluded.low,
                close = excluded.close,
                change = excluded.change,
                pct_chg = excluded.pct_chg,
                vol = excluded.vol,
                amount = excluded.amount,
                open_qfq = excluded.open_qfq,
                high_qfq = excluded.high_qfq,
                low_qfq = excluded.low_qfq,
                close_qfq = excluded.close_qfq,
                open_hfq = excluded.open_hfq,
                high_hfq = excluded.high_hfq,
                low_hfq = excluded.low_hfq,
                close_hfq = excluded.close_hfq,
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