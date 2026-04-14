"""
DividendCollector - 分红送股拉取器

严格按照CSV文档：
- 接口名称：dividend（标准接口）
- 接口参数：ann_date={游标+1}
- 文档地址：https://tushare.pro/document/2?doc_id=103
- 游标策略：daily_natural（按自然日记录）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class DividendCollector(BaseCollector):
    """分红送股拉取器（P2财务表，标准接口）"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path, api=api, table_name='dividend',
            api_name='dividend', date_field='ann_date', vip_interface=False
        )

    def collect_by_date(self, ann_date: str) -> List[Dict]:
        """
        按公告日期拉取数据

        Args:
            ann_date: 公告日期（YYYYMMDD格式）

        Returns:
            数据列表
        """
        self.logger.info(f"拉取分红送股: ann_date={ann_date}")
        return self.collect(ann_date=ann_date)

    def save(self, data: List[Dict]) -> int:
        """
        保存数据（过滤record_date为None的记录）

        Args:
            data: 数据列表

        Returns:
            保存的记录数

        注意：
            - record_date是主键之一，不能为NULL
            - 过滤掉record_date为None的记录
        """
        # 过滤record_date为None的数据
        filtered_data = [
            item for item in data
            if item.get('record_date') is not None
        ]

        if len(filtered_data) < len(data):
            self.logger.warning(
                f"过滤了{len(data) - len(filtered_data)}条record_date为NULL的记录"
            )

        # 调用父类save方法
        return super().save(filtered_data)

    def _extract_values(self, item: Dict) -> tuple:
        """提取11个字段"""
        return (
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('record_date')),
            convert_date_format(item.get('ex_date')),
            convert_date_format(item.get('pay_date')),
            item.get('div_proc'),
            item.get('stk_div'),
            item.get('stk_bo_rate'),
            item.get('stk_co_rate'),
            item.get('cash_div'),
            item.get('cash_div_tax'),
        )

    def _build_insert_query(self) -> str:
        """INSERT语句（11字段，ON CONFLICT使用三字段主键）"""
        fields = """ts_code, ann_date, record_date, ex_date, pay_date, div_proc,
            stk_div, stk_bo_rate, stk_co_rate, cash_div, cash_div_tax, updated_at"""
        placeholders = ', '.join(['?'] * 11) + ', NOW()'
        updates = """ex_date = excluded.ex_date, pay_date = excluded.pay_date,
            div_proc = excluded.div_proc, stk_div = excluded.stk_div,
            stk_bo_rate = excluded.stk_bo_rate, stk_co_rate = excluded.stk_co_rate,
            cash_div = excluded.cash_div, cash_div_tax = excluded.cash_div_tax,
            updated_at = NOW()"""

        return f"""
            INSERT INTO dividend ({fields}) VALUES ({placeholders})
            ON CONFLICT (ts_code, ann_date, record_date) DO UPDATE SET {updates}
        """