"""
ExpressBriefCollector - 业绩快报拉取器（VIP接口）

严格按照CSV文档：
- 接口名称：express_vip（VIP接口）
- 接口参数：ann_date={游标+1}、report_type=1
- 文档地址：https://tushare.pro/document/2%sdoc_id=46
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

    def __init__(self, db_config: dict, api: TushareAPI):
        super().__init__(
            db_config=db_config, api=api, table_name='express_brief',
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
        """
        提取字段值（严格按照express_brief_schema.sql定义，完整32个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（32个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('end_date')),
            item.get('revenue'),
            item.get('operate_profit'),
            item.get('total_profit'),
            item.get('n_income'),
            item.get('total_assets'),
            item.get('total_hldr_eqy_exc_min_int'),
            item.get('diluted_eps'),
            item.get('diluted_roe'),
            item.get('yoy_net_profit'),
            item.get('bps'),
            item.get('yoy_sales'),
            item.get('yoy_op'),
            item.get('yoy_tp'),
            item.get('yoy_dedu_np'),
            item.get('yoy_eps'),
            item.get('yoy_roe'),
            item.get('growth_assets'),
            item.get('yoy_equity'),
            item.get('growth_bps'),
            item.get('or_last_year'),
            item.get('op_last_year'),
            item.get('tp_last_year'),
            item.get('np_last_year'),
            item.get('eps_last_year'),
            item.get('open_net_assets'),
            item.get('open_bps'),
            item.get('perf_summary'),
            item.get('is_audit'),
            item.get('remark'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整32个字段）

        Returns:
            INSERT SQL语句

        注意：
            - DuckDB不允许在ON CONFLICT中更新ann_date字段（有约束限制）
            - 主键：PRIMARY KEY (ts_code, end_date, ann_date)
        """
        fields = "ts_code, ann_date, end_date, revenue, operate_profit, total_profit, n_income, total_assets, total_hldr_eqy_exc_min_int, diluted_eps, diluted_roe, yoy_net_profit, bps, yoy_sales, yoy_op, yoy_tp, yoy_dedu_np, yoy_eps, yoy_roe, growth_assets, yoy_equity, growth_bps, or_last_year, op_last_year, tp_last_year, np_last_year, eps_last_year, open_net_assets, open_bps, perf_summary, is_audit, remark, updated_at"

        placeholders = ', '.join(['%s'] * 32) + ', NOW()'

        update_fields = "revenue = excluded.revenue, operate_profit = excluded.operate_profit, total_profit = excluded.total_profit, n_income = excluded.n_income, total_assets = excluded.total_assets, total_hldr_eqy_exc_min_int = excluded.total_hldr_eqy_exc_min_int, diluted_eps = excluded.diluted_eps, diluted_roe = excluded.diluted_roe, yoy_net_profit = excluded.yoy_net_profit, bps = excluded.bps, yoy_sales = excluded.yoy_sales, yoy_op = excluded.yoy_op, yoy_tp = excluded.yoy_tp, yoy_dedu_np = excluded.yoy_dedu_np, yoy_eps = excluded.yoy_eps, yoy_roe = excluded.yoy_roe, growth_assets = excluded.growth_assets, yoy_equity = excluded.yoy_equity, growth_bps = excluded.growth_bps, or_last_year = excluded.or_last_year, op_last_year = excluded.op_last_year, tp_last_year = excluded.tp_last_year, np_last_year = excluded.np_last_year, eps_last_year = excluded.eps_last_year, open_net_assets = excluded.open_net_assets, open_bps = excluded.open_bps, perf_summary = excluded.perf_summary, is_audit = excluded.is_audit, remark = excluded.remark, updated_at = NOW()"

        return f"""
            INSERT INTO express_brief (ts_code, ann_date, end_date, revenue, operate_profit, total_profit, n_income, total_assets, total_hldr_eqy_exc_min_int, diluted_eps, diluted_roe, yoy_net_profit, bps, yoy_sales, yoy_op, yoy_tp, yoy_dedu_np, yoy_eps, yoy_roe, growth_assets, yoy_equity, growth_bps, or_last_year, op_last_year, tp_last_year, np_last_year, eps_last_year, open_net_assets, open_bps, perf_summary, is_audit, remark, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, end_date, ann_date)
            DO UPDATE SET {update_fields}
        """


