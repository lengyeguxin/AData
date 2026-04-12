"""
ExpressCollector - 业绩预告拉取器

严格按照CSV文档：
- 接口名称：forecast_vip（VIP接口）
- 接口参数：ann_date={游标+1}
- 文档地址：https://tushare.pro/document/2?doc_id=38
- 游标策略：daily_natural（按自然日记录）
- VIP接口特性：更丰富字段
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class ExpressCollector(BaseCollector):
    """业绩预告拉取器（P2财务表，VIP接口，按自然日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='express',
            api_name='forecast_vip',  # VIP接口（严格按照CSV文档）
            date_field='ann_date',
            vip_interface=True
        )

    def collect_by_ann_date(self, ann_date: str) -> List[Dict]:
        self.logger.info(f"拉取业绩预告（VIP接口）: ann_date={ann_date}")
        data = self.collect(ann_date=ann_date)
        return data

    def _extract_values(self, item: Dict) -> tuple:
        return (
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('end_date')),
            item.get('type'),
            item.get('p_change_min'),
            item.get('p_change_max'),
            item.get('net_profit_min'),
            item.get('net_profit_max'),
        )

    def _build_insert_query(self) -> str:
        return """
            INSERT INTO express (
                ts_code, ann_date, end_date, type,
                p_change_min, p_change_max, net_profit_min, net_profit_max, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code, end_date)
            DO UPDATE SET
                ann_date = excluded.ann_date,
                type = excluded.type,
                p_change_min = excluded.p_change_min,
                p_change_max = excluded.p_change_max,
                net_profit_min = excluded.net_profit_min,
                net_profit_max = excluded.net_profit_max,
                updated_at = NOW()
        """

    def run_by_ann_date(self, ann_date: str) -> int:
        data = self.collect_by_ann_date(ann_date)
        return self.save(data)