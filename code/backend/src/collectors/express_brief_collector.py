"""
ExpressBriefCollector - 业绩快报拉取器（VIP接口）

严格按照CSV文档：
- 接口名称：express_vip（VIP接口）
- 接口参数：ann_date={游标+1}、report_type=1
- 文档地址：https://tushare.pro/document/2?doc_id=46
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
    """业绩快报拉取器（P2财务表，VIP接口）"""

    def __init__(self, db_path: str, api: TushareAPI):
        super().__init__(
            db_path=db_path, api=api, table_name='express_brief',
            api_name='express_vip', date_field='ann_date', vip_interface=True
        )

    def collect_by_date(self, ann_date: str) -> List[Dict]:
        """
        按公告日期拉取数据

        Args:
            ann_date: 公告日期（YYYYMMDD格式）

        Returns:
            数据列表
        """
        self.logger.info(f"拉取业绩快报: ann_date={ann_date}")
        return self.collect(ann_date=ann_date)

    def _extract_values(self, item: Dict) -> tuple:
        """提取30个字段"""
        return (
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('end_date')),
            item.get('report_type'),
            item.get('comp_type'),
            item.get('end_type'),
            item.get('update_flag'),
            item.get('total_revenue'),
            item.get('revenue'),
            item.get('operate_profit'),
            item.get('total_profit'),
            item.get('n_income'),
            item.get('n_income_attr_p'),
            item.get('basic_eps'),
            item.get('diluted_eps'),
            item.get('n_income_cut'),
            item.get('yoy_sales'),
            item.get('yoy_dedu_np'),
            item.get('yoy_eps'),
            item.get('yoy_op'),
            item.get('yoy_tp'),
            item.get('yoy_np'),
            item.get('yoy_np_cut'),
            item.get('qoq_sales'),
            item.get('qoq_dedu_np'),
            item.get('qoq_eps'),
            item.get('qoq_op'),
            item.get('qoq_tp'),
            item.get('qoq_np'),
            item.get('qoq_np_cut'),
        )

    def _build_insert_query(self) -> str:
        """INSERT语句（30字段，ON CONFLICT使用三字段主键）"""
        fields = """ts_code, ann_date, end_date, report_type, comp_type, end_type, update_flag,
            total_revenue, revenue, operate_profit, total_profit, n_income, n_income_attr_p,
            basic_eps, diluted_eps, n_income_cut,
            yoy_sales, yoy_dedu_np, yoy_eps, yoy_op, yoy_tp, yoy_np, yoy_np_cut,
            qoq_sales, qoq_dedu_np, qoq_eps, qoq_op, qoq_tp, qoq_np, qoq_np_cut, updated_at"""
        placeholders = ', '.join(['?'] * 30) + ', NOW()'
        updates = """report_type = excluded.report_type, comp_type = excluded.comp_type,
            end_type = excluded.end_type, update_flag = excluded.update_flag,
            total_revenue = excluded.total_revenue, revenue = excluded.revenue,
            operate_profit = excluded.operate_profit, total_profit = excluded.total_profit,
            n_income = excluded.n_income, n_income_attr_p = excluded.n_income_attr_p,
            basic_eps = excluded.basic_eps, diluted_eps = excluded.diluted_eps,
            n_income_cut = excluded.n_income_cut,
            yoy_sales = excluded.yoy_sales, yoy_dedu_np = excluded.yoy_dedu_np,
            yoy_eps = excluded.yoy_eps, yoy_op = excluded.yoy_op, yoy_tp = excluded.yoy_tp,
            yoy_np = excluded.yoy_np, yoy_np_cut = excluded.yoy_np_cut,
            qoq_sales = excluded.qoq_sales, qoq_dedu_np = excluded.qoq_dedu_np,
            qoq_eps = excluded.qoq_eps, qoq_op = excluded.qoq_op, qoq_tp = excluded.qoq_tp,
            qoq_np = excluded.qoq_np, qoq_np_cut = excluded.qoq_np_cut, updated_at = NOW()"""

        return f"""
            INSERT INTO express_brief ({fields}) VALUES ({placeholders})
            ON CONFLICT (ts_code, ann_date, end_date) DO UPDATE SET {updates}
        """