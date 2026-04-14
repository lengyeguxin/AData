"""
ExpressCollector - 业绩预告拉取器（VIP接口）

严格按照CSV文档：
- 接口名称：forecast_vip（VIP接口）
- 接口参数：ann_date={游标+1}、report_type=1
- 文档地址：https://tushare.pro/document/2?doc_id=45
- 游标策略：daily_natural（按自然日记录）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class ExpressCollector(BaseCollector):
    """业绩预告拉取器（P2财务表，VIP接口）"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path, api=api, table_name='express',
            api_name='forecast_vip', date_field='ann_date', vip_interface=True
        )

    def collect_by_date(self, ann_date: str) -> List[Dict]:
        """
        按公告日期拉取数据

        Args:
            ann_date: 公告日期（YYYYMMDD格式）

        Returns:
            数据列表
        """
        self.logger.info(f"拉取业绩预告: ann_date={ann_date}")
        return self.collect(ann_date=ann_date)

    def _extract_values(self, item: Dict) -> tuple:
        """提取20个字段"""
        return (
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('end_date')),
            item.get('report_type'),
            item.get('comp_type'),
            item.get('end_type'),
            item.get('update_flag'),
            item.get('type'),
            item.get('summary'),
            item.get('n_income_min'),
            item.get('n_income_max'),
            item.get('n_income_min_last'),
            item.get('n_income_max_last'),
            item.get('p_change_min'),
            item.get('p_change_max'),
            item.get('p_change_min_last'),
            item.get('p_change_max_last'),
            item.get('n_income_last'),
            item.get('p_change_last'),
            item.get('change_reason'),
        )

    def _build_insert_query(self) -> str:
        """INSERT语句（20字段，ON CONFLICT使用三字段主键）"""
        fields = """ts_code, ann_date, end_date, report_type, comp_type, end_type, update_flag,
            type, summary, n_income_min, n_income_max, n_income_min_last, n_income_max_last,
            p_change_min, p_change_max, p_change_min_last, p_change_max_last,
            n_income_last, p_change_last, change_reason, updated_at"""
        placeholders = ', '.join(['?'] * 20) + ', NOW()'
        updates = """report_type = excluded.report_type, comp_type = excluded.comp_type,
            end_type = excluded.end_type, update_flag = excluded.update_flag,
            type = excluded.type, summary = excluded.summary,
            n_income_min = excluded.n_income_min, n_income_max = excluded.n_income_max,
            n_income_min_last = excluded.n_income_min_last, n_income_max_last = excluded.n_income_max_last,
            p_change_min = excluded.p_change_min, p_change_max = excluded.p_change_max,
            p_change_min_last = excluded.p_change_min_last, p_change_max_last = excluded.p_change_max_last,
            n_income_last = excluded.n_income_last, p_change_last = excluded.p_change_last,
            change_reason = excluded.change_reason, updated_at = NOW()"""

        return f"""
            INSERT INTO express ({fields}) VALUES ({placeholders})
            ON CONFLICT (ts_code, ann_date, end_date) DO UPDATE SET {updates}
        """