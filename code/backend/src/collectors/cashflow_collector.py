"""
CashflowCollector - 现金流量表拉取器（VIP接口）

严格按照CSV文档：
- 接口名称：cashflow_vip（VIP接口）
- 接口参数：ann_date={游标+1}、report_type=1
- 文档地址：https://tushare.pro/document/2?doc_id=44
- 游标策略：daily_natural（按自然日记录）
- VIP接口特性：更丰富字段、更快更新速度
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class CashflowCollector(BaseCollector):
    """现金流量表拉取器（P2财务表，VIP接口，按自然日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化CashflowCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='cashflow',
            api_name='cashflow_vip',  # VIP接口（严格按照CSV文档）
            date_field='ann_date',  # 公告日期（按自然日）
            vip_interface=True  # VIP接口
        )

    def collect_by_ann_date(self, ann_date: str) -> List[Dict]:
        """
        拉取指定公告日期的现金流量表数据（VIP接口）

        Args:
            ann_date: 公告日期（YYYYMMDD格式）

        Returns:
            现金流量表数据列表

        示例：
            collect_by_ann_date('20260409') → 拉取2026-04-09公告的现金流量表

        注意：
            - 使用VIP接口cashflow_vip（更丰富字段）
            - ann_date可能无数据（正常情况，财务数据公告不规律）
        """
        self.logger.info(f"拉取现金流量表（VIP接口）: ann_date={ann_date}")

        # 严格按照CSV文档参数
        data = self.collect(ann_date=ann_date, report_type='1')  # 合并报表

        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照p2_schema.sql定义，完整37个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（37个字段，严格按照schema定义顺序）
        """
        return (
            # 基础字段（8个）
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('f_ann_date')),
            convert_date_format(item.get('end_date')),
            item.get('report_type'),
            item.get('comp_type'),
            item.get('end_type'),       # 新增字段
            item.get('update_flag'),    # 新增字段

            # 经营活动现金流（8个）
            item.get('n_cashflow_act'),
            item.get('cash_recp_sg_and_rs'),
            item.get('recp_tax_rends'),
            item.get('cash_pay_for_tax'),
            item.get('cash_pay_acq_const_fi'),
            item.get('cash_pay_for_depos'),
            item.get('cash_recp_loan_rel_fi'),
            item.get('free_cashflow'),

            # 投资活动现金流（11个）
            item.get('n_cash_flows_inv_act'),
            item.get('c_fr_sale_sg'),
            item.get('c_fr_for_sale'),
            item.get('c_fr_disp_withdrw_invest'),
            item.get('c_recp_return_invest'),
            item.get('c_recp_loan_rel_fi'),
            item.get('c_fr_oth_inv_act'),
            item.get('n_cashflow_inv_act'),
            item.get('c_pay_for_acq_fi'),
            item.get('c_pay_for_invest'),
            item.get('c_pay_oth_inv_act'),

            # 筹资活动现金流（9个）
            item.get('n_cash_flows_fnc_act'),
            item.get('c_fr_cap_contr'),
            item.get('c_fr_borrow'),
            item.get('c_fr_oth_fnc_act'),
            item.get('n_cashflow_fnc_act'),
            item.get('c_pay_for_dist_dpcp_int_exp'),
            item.get('c_pay_for_loan_rel_fi'),
            item.get('c_pay_oth_fnc_act'),
            item.get('n_incr_cash_cash_equ'),

            # 其他（1个）
            item.get('effect_forex_cash'),
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整37个字段）

        Returns:
            INSERT SQL语句

        注意：
            - DuckDB不允许在ON CONFLICT中更新ann_date字段（有约束限制）
            - 主键：PRIMARY KEY (ts_code, end_date, report_type)
        """
        # 构建字段列表（37个字段 + updated_at）
        fields = """ts_code, ann_date, f_ann_date, end_date, report_type, comp_type, end_type, update_flag,
            n_cashflow_act, cash_recp_sg_and_rs, recp_tax_rends, cash_pay_for_tax,
            cash_pay_acq_const_fi, cash_pay_for_depos, cash_recp_loan_rel_fi, free_cashflow,
            n_cash_flows_inv_act, c_fr_sale_sg, c_fr_for_sale, c_fr_disp_withdrw_invest,
            c_recp_return_invest, c_recp_loan_rel_fi, c_fr_oth_inv_act, n_cashflow_inv_act,
            c_pay_for_acq_fi, c_pay_for_invest, c_pay_oth_inv_act,
            n_cash_flows_fnc_act, c_fr_cap_contr, c_fr_borrow, c_fr_oth_fnc_act,
            n_cashflow_fnc_act, c_pay_for_dist_dpcp_int_exp, c_pay_for_loan_rel_fi, c_pay_oth_fnc_act,
            n_incr_cash_cash_equ, effect_forex_cash, updated_at"""

        # 构建VALUES占位符（37个 ? + NOW()）
        placeholders = ', '.join(['?'] * 37) + ', NOW()'

        # 构建DO UPDATE SET语句（排除主键字段ts_code、end_date、report_type，排除ann_date）
        update_fields = """f_ann_date = excluded.f_ann_date,
            comp_type = excluded.comp_type,
            end_type = excluded.end_type,
            update_flag = excluded.update_flag,
            n_cashflow_act = excluded.n_cashflow_act, cash_recp_sg_and_rs = excluded.cash_recp_sg_and_rs,
            recp_tax_rends = excluded.recp_tax_rends, cash_pay_for_tax = excluded.cash_pay_for_tax,
            cash_pay_acq_const_fi = excluded.cash_pay_acq_const_fi, cash_pay_for_depos = excluded.cash_pay_for_depos,
            cash_recp_loan_rel_fi = excluded.cash_recp_loan_rel_fi, free_cashflow = excluded.free_cashflow,
            n_cash_flows_inv_act = excluded.n_cash_flows_inv_act, c_fr_sale_sg = excluded.c_fr_sale_sg,
            c_fr_for_sale = excluded.c_fr_for_sale, c_fr_disp_withdrw_invest = excluded.c_fr_disp_withdrw_invest,
            c_recp_return_invest = excluded.c_recp_return_invest, c_recp_loan_rel_fi = excluded.c_recp_loan_rel_fi,
            c_fr_oth_inv_act = excluded.c_fr_oth_inv_act, n_cashflow_inv_act = excluded.n_cashflow_inv_act,
            c_pay_for_acq_fi = excluded.c_pay_for_acq_fi, c_pay_for_invest = excluded.c_pay_for_invest,
            c_pay_oth_inv_act = excluded.c_pay_oth_inv_act,
            n_cash_flows_fnc_act = excluded.n_cash_flows_fnc_act, c_fr_cap_contr = excluded.c_fr_cap_contr,
            c_fr_borrow = excluded.c_fr_borrow, c_fr_oth_fnc_act = excluded.c_fr_oth_fnc_act,
            n_cashflow_fnc_act = excluded.n_cashflow_fnc_act,
            c_pay_for_dist_dpcp_int_exp = excluded.c_pay_for_dist_dpcp_int_exp,
            c_pay_for_loan_rel_fi = excluded.c_pay_for_loan_rel_fi, c_pay_oth_fnc_act = excluded.c_pay_oth_fnc_act,
            n_incr_cash_cash_equ = excluded.n_incr_cash_cash_equ, effect_forex_cash = excluded.effect_forex_cash,
            updated_at = NOW()"""

        return f"""
            INSERT INTO cashflow ({fields})
            VALUES ({placeholders})
            ON CONFLICT (ts_code, end_date, report_type)
            DO UPDATE SET {update_fields}
        """

    def run_by_ann_date(self, ann_date: str) -> int:
        """
        拉取并保存指定公告日期数据（VIP接口）

        Args:
            ann_date: 公告日期（YYYYMMDD）

        Returns:
            保存的记录数

        注意：
            - 财务表允许无数据（ann_date可能无公告）
            - 请求完毕即可更新游标（即使无数据）
        """
        data = self.collect_by_ann_date(ann_date)
        return self.save(data)