"""
HotsTraderDetailCollector - 游资交易明细拉取器

严格按照CSV文档：
- 接口名称：hots_trader_detail（龙虎榜交易明细）
- 接口参数：trade_date={游标+1}
- 文档地址：https://tushare.pro/document/2?doc_id=164
- 游标策略：daily_trade（按交易日记录）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class HotsTraderDetailCollector(BaseCollector):
    """游资交易明细拉取器（P4游资表，按交易日每日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化HotsTraderDetailCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='hots_trader_detail',
            api_name='hots_trader_detail',  # 严格按照CSV文档
            date_field='trade_date',
            vip_interface=False  # 标准接口
        )

    def collect_by_date(self, trade_date: str) -> List[Dict]:
        """
        拉取指定交易日的游资交易明细数据

        Args:
            trade_date: 交易日期（YYYYMMDD格式）

        Returns:
            游资交易明细数据列表

        示例：
            collect_by_date('20260409') → 拉取2026-04-09游资交易明细
        """
        self.logger.info(f"拉取游资交易明细: trade_date={trade_date}")

        # 严格按照CSV文档参数
        data = self.collect(trade_date=trade_date)

        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照p2_schema.sql定义）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（字段顺序：account, ts_code, trade_date, buy_amount, sell_amount, net_amount, buy_vol, sell_vol, net_vol, reason）
        """
        return (
            item.get('account'),        # account（游资账户）
            item.get('ts_code'),        # ts_code（股票代码）
            convert_date_format(item.get('trade_date')),  # trade_date
            item.get('buy_amount'),     # buy_amount（买入金额）
            item.get('sell_amount'),    # sell_amount（卖出金额）
            item.get('net_amount'),     # net_amount（净金额）
            item.get('buy_vol'),        # buy_vol（买入量）
            item.get('sell_vol'),       # sell_vol（卖出量）
            item.get('net_vol'),        # net_vol（净量）
            item.get('reason'),         # reason（买卖原因）
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO hots_trader_detail (
                account, ts_code, trade_date, buy_amount, sell_amount, net_amount,
                buy_vol, sell_vol, net_vol, reason, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (account, ts_code, trade_date)
            DO UPDATE SET
                buy_amount = excluded.buy_amount,
                sell_amount = excluded.sell_amount,
                net_amount = excluded.net_amount,
                buy_vol = excluded.buy_vol,
                sell_vol = excluded.sell_vol,
                net_vol = excluded.net_vol,
                reason = excluded.reason,
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