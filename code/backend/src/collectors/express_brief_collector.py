"""
ExpressBriefCollector - 业绩快报拉取器

严格按照CSV文档：
- 接口名称：express_vip（VIP接口）
- 接口参数：ann_date={游标+1}
- 文档地址：https://tushare.pro/document/2?doc_id=39
- 游标策略：daily_natural（按自然日记录）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class ExpressBriefCollector(BaseCollector):
    """业绩快报拉取器（P2财务表，VIP接口，按自然日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='express_brief',
            api_name='express_vip',  # VIP接口（严格按照CSV文档）
            date_field='ann_date',
            vip_interface=True
        )

    def collect_by_ann_date(self, ann_date: str) -> List[Dict]:
        self.logger.info(f"拉取业绩快报（VIP接口）: ann_date={ann_date}")
        data = self.collect(ann_date=ann_date)
        return data

    def _extract_values(self, item: Dict) -> tuple:
        return (
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('end_date')),
            item.get('revenue'),
            item.get('operate_profit'),
            item.get('total_profit'),
            item.get('n_income'),
            item.get('total_assets'),
            item.get('total_equity'),
        )

    def _build_insert_query(self) -> str:
        return """
            INSERT INTO express_brief (
                ts_code, ann_date, end_date, revenue, operate_profit,
                total_profit, n_income, total_assets, total_equity, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code, end_date)
            DO UPDATE SET
                ann_date = excluded.ann_date,
                revenue = excluded.revenue,
                operate_profit = excluded.operate_profit,
                total_profit = excluded.total_profit,
                n_income = excluded.n_income,
                total_assets = excluded.total_assets,
                total_equity = excluded.total_equity,
                updated_at = NOW()
        """

    def run_by_ann_date(self, ann_date: str) -> int:
        data = self.collect_by_ann_date(ann_date)
        return self.save(data)
