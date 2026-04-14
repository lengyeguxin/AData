"""
HotsTraderDetailCollector - 游资交易明细拉取器

严格按照CSV文档：
- 接口名称：hm_detail
- 接口参数：trade_date={游标+1}
- 文档地址：https://tushare.pro/document/2?doc_id=312
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
            api_name='hm_detail',  # 实际接口名（修正）
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
        """
        self.logger.info(f"拉取游资交易明细: trade_date={trade_date}")

        # 严格按照CSV文档参数
        data = self.collect(trade_date=trade_date)

        return data

    def save(self, data: List[Dict]) -> int:
        """
        保存数据（过滤account为None的记录）

        Args:
            data: 数据列表

        Returns:
            保存的记录数

        注意：
            - account是主键且NOT NULL，不能为NULL
            - 过滤掉account为None的记录
        """
        # 过滤account为None的数据
        filtered_data = [
            item for item in data
            if item.get('account') is not None
        ]

        if len(filtered_data) < len(data):
            self.logger.warning(
                f"过滤了{len(data) - len(filtered_data)}条account为NULL的记录"
            )

        # 调用父类save方法
        return super().save(filtered_data)

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照hots_trader_detail_schema.sql定义，完整9个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（9个字段，严格按照schema定义顺序）
        """
        return (
            convert_date_format(item.get('trade_date')),
            item.get('ts_code'),
            item.get('ts_name'),
            item.get('buy_amount'),
            item.get('sell_amount'),
            item.get('net_amount'),
            item.get('hm_name'),
            item.get('hm_orgs'),
            item.get('tag'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整9个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "trade_date, ts_code, ts_name, buy_amount, sell_amount, net_amount, hm_name, hm_orgs, tag, updated_at"

        placeholders = ', '.join(['?'] * 9) + ', NOW()'

        update_fields = "ts_name = excluded.ts_name, buy_amount = excluded.buy_amount, sell_amount = excluded.sell_amount, net_amount = excluded.net_amount, hm_name = excluded.hm_name, hm_orgs = excluded.hm_orgs, tag = excluded.tag, updated_at = NOW()"

        return f"""
            INSERT INTO hots_trader_detail (trade_date, ts_code, ts_name, buy_amount, sell_amount, net_amount, hm_name, hm_orgs, tag, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (account, ts_code, trade_date)
            DO UPDATE SET {update_fields}
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