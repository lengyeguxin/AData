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
        提取字段值（严格按照cashflow_schema.sql定义，完整97个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（97个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('f_ann_date')),
            convert_date_format(item.get('end_date')),
            item.get('comp_type'),
            item.get('report_type'),
            item.get('end_type'),
            item.get('net_profit'),
            item.get('finan_exp'),
            item.get('c_fr_sale_sg'),
            item.get('recp_tax_rends'),
            item.get('n_depos_incr_fi'),
            item.get('n_incr_loans_cb'),
            item.get('n_inc_borr_oth_fi'),
            item.get('prem_fr_orig_contr'),
            item.get('n_incr_insured_dep'),
            item.get('n_reinsur_prem'),
            item.get('n_incr_disp_tfa'),
            item.get('ifc_cash_incr'),
            item.get('n_incr_disp_faas'),
            item.get('n_incr_loans_oth_bank'),
            item.get('n_cap_incr_repur'),
            item.get('c_fr_oth_operate_a'),
            item.get('c_inf_fr_operate_a'),
            item.get('c_paid_goods_s'),
            item.get('c_paid_to_for_empl'),
            item.get('c_paid_for_taxes'),
            item.get('n_incr_clt_loan_adv'),
            item.get('n_incr_dep_cbob'),
            item.get('c_pay_claims_orig_inco'),
            item.get('pay_handling_chrg'),
            item.get('pay_comm_insur_plcy'),
            item.get('oth_cash_pay_oper_act'),
            item.get('st_cash_out_act'),
            item.get('n_cashflow_act'),
            item.get('oth_recp_ral_inv_act'),
            item.get('c_disp_withdrwl_invest'),
            item.get('c_recp_return_invest'),
            item.get('n_recp_disp_fiolta'),
            item.get('n_recp_disp_sobu'),
            item.get('stot_inflows_inv_act'),
            item.get('c_pay_acq_const_fiolta'),
            item.get('c_paid_invest'),
            item.get('n_disp_subs_oth_biz'),
            item.get('oth_pay_ral_inv_act'),
            item.get('n_incr_pledge_loan'),
            item.get('stot_out_inv_act'),
            item.get('n_cashflow_inv_act'),
            item.get('c_recp_borrow'),
            item.get('proc_issue_bonds'),
            item.get('oth_cash_recp_ral_fnc_act'),
            item.get('stot_cash_in_fnc_act'),
            item.get('free_cashflow'),
            item.get('c_prepay_amt_borr'),
            item.get('c_pay_dist_dpcp_int_exp'),
            item.get('incl_dvd_profit_paid_sc_ms'),
            item.get('oth_cashpay_ral_fnc_act'),
            item.get('stot_cashout_fnc_act'),
            item.get('n_cash_flows_fnc_act'),
            item.get('eff_fx_flu_cash'),
            item.get('n_incr_cash_cash_equ'),
            item.get('c_cash_equ_beg_period'),
            item.get('c_cash_equ_end_period'),
            item.get('c_recp_cap_contrib'),
            item.get('incl_cash_rec_saims'),
            item.get('uncon_invest_loss'),
            item.get('prov_depr_assets'),
            item.get('depr_fa_coga_dpba'),
            item.get('amort_intang_assets'),
            item.get('lt_amort_deferred_exp'),
            item.get('decr_deferred_exp'),
            item.get('incr_acc_exp'),
            item.get('loss_disp_fiolta'),
            item.get('loss_scr_fa'),
            item.get('loss_fv_chg'),
            item.get('invest_loss'),
            item.get('decr_def_inc_tax_assets'),
            item.get('incr_def_inc_tax_liab'),
            item.get('decr_inventories'),
            item.get('decr_oper_payable'),
            item.get('incr_oper_payable'),
            item.get('others'),
            item.get('im_net_cashflow_oper_act'),
            item.get('conv_debt_into_cap'),
            item.get('conv_copbonds_due_within_1y'),
            item.get('fa_fnc_leases'),
            item.get('im_n_incr_cash_equ'),
            item.get('net_dism_capital_add'),
            item.get('net_cash_rece_sec'),
            item.get('credit_impa_loss'),
            item.get('use_right_asset_dep'),
            item.get('oth_loss_asset'),
            item.get('end_bal_cash'),
            item.get('beg_bal_cash'),
            item.get('end_bal_cash_equ'),
            item.get('beg_bal_cash_equ'),
            item.get('update_flag'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整97个字段）

        Returns:
            INSERT SQL语句

        注意：
            - DuckDB不允许在ON CONFLICT中更新ann_date字段（有约束限制）
            - 主键：PRIMARY KEY (ts_code, end_date, report_type)
        """
        fields = "ts_code, ann_date, f_ann_date, end_date, comp_type, report_type, end_type, net_profit, finan_exp, c_fr_sale_sg, recp_tax_rends, n_depos_incr_fi, n_incr_loans_cb, n_inc_borr_oth_fi, prem_fr_orig_contr, n_incr_insured_dep, n_reinsur_prem, n_incr_disp_tfa, ifc_cash_incr, n_incr_disp_faas, n_incr_loans_oth_bank, n_cap_incr_repur, c_fr_oth_operate_a, c_inf_fr_operate_a, c_paid_goods_s, c_paid_to_for_empl, c_paid_for_taxes, n_incr_clt_loan_adv, n_incr_dep_cbob, c_pay_claims_orig_inco, pay_handling_chrg, pay_comm_insur_plcy, oth_cash_pay_oper_act, st_cash_out_act, n_cashflow_act, oth_recp_ral_inv_act, c_disp_withdrwl_invest, c_recp_return_invest, n_recp_disp_fiolta, n_recp_disp_sobu, stot_inflows_inv_act, c_pay_acq_const_fiolta, c_paid_invest, n_disp_subs_oth_biz, oth_pay_ral_inv_act, n_incr_pledge_loan, stot_out_inv_act, n_cashflow_inv_act, c_recp_borrow, proc_issue_bonds, oth_cash_recp_ral_fnc_act, stot_cash_in_fnc_act, free_cashflow, c_prepay_amt_borr, c_pay_dist_dpcp_int_exp, incl_dvd_profit_paid_sc_ms, oth_cashpay_ral_fnc_act, stot_cashout_fnc_act, n_cash_flows_fnc_act, eff_fx_flu_cash, n_incr_cash_cash_equ, c_cash_equ_beg_period, c_cash_equ_end_period, c_recp_cap_contrib, incl_cash_rec_saims, uncon_invest_loss, prov_depr_assets, depr_fa_coga_dpba, amort_intang_assets, lt_amort_deferred_exp, decr_deferred_exp, incr_acc_exp, loss_disp_fiolta, loss_scr_fa, loss_fv_chg, invest_loss, decr_def_inc_tax_assets, incr_def_inc_tax_liab, decr_inventories, decr_oper_payable, incr_oper_payable, others, im_net_cashflow_oper_act, conv_debt_into_cap, conv_copbonds_due_within_1y, fa_fnc_leases, im_n_incr_cash_equ, net_dism_capital_add, net_cash_rece_sec, credit_impa_loss, use_right_asset_dep, oth_loss_asset, end_bal_cash, beg_bal_cash, end_bal_cash_equ, beg_bal_cash_equ, update_flag, updated_at"

        placeholders = ', '.join(['?'] * 97) + ', NOW()'

        update_fields = "f_ann_date = excluded.f_ann_date, comp_type = excluded.comp_type, end_type = excluded.end_type, net_profit = excluded.net_profit, finan_exp = excluded.finan_exp, c_fr_sale_sg = excluded.c_fr_sale_sg, recp_tax_rends = excluded.recp_tax_rends, n_depos_incr_fi = excluded.n_depos_incr_fi, n_incr_loans_cb = excluded.n_incr_loans_cb, n_inc_borr_oth_fi = excluded.n_inc_borr_oth_fi, prem_fr_orig_contr = excluded.prem_fr_orig_contr, n_incr_insured_dep = excluded.n_incr_insured_dep, n_reinsur_prem = excluded.n_reinsur_prem, n_incr_disp_tfa = excluded.n_incr_disp_tfa, ifc_cash_incr = excluded.ifc_cash_incr, n_incr_disp_faas = excluded.n_incr_disp_faas, n_incr_loans_oth_bank = excluded.n_incr_loans_oth_bank, n_cap_incr_repur = excluded.n_cap_incr_repur, c_fr_oth_operate_a = excluded.c_fr_oth_operate_a, c_inf_fr_operate_a = excluded.c_inf_fr_operate_a, c_paid_goods_s = excluded.c_paid_goods_s, c_paid_to_for_empl = excluded.c_paid_to_for_empl, c_paid_for_taxes = excluded.c_paid_for_taxes, n_incr_clt_loan_adv = excluded.n_incr_clt_loan_adv, n_incr_dep_cbob = excluded.n_incr_dep_cbob, c_pay_claims_orig_inco = excluded.c_pay_claims_orig_inco, pay_handling_chrg = excluded.pay_handling_chrg, pay_comm_insur_plcy = excluded.pay_comm_insur_plcy, oth_cash_pay_oper_act = excluded.oth_cash_pay_oper_act, st_cash_out_act = excluded.st_cash_out_act, n_cashflow_act = excluded.n_cashflow_act, oth_recp_ral_inv_act = excluded.oth_recp_ral_inv_act, c_disp_withdrwl_invest = excluded.c_disp_withdrwl_invest, c_recp_return_invest = excluded.c_recp_return_invest, n_recp_disp_fiolta = excluded.n_recp_disp_fiolta, n_recp_disp_sobu = excluded.n_recp_disp_sobu, stot_inflows_inv_act = excluded.stot_inflows_inv_act, c_pay_acq_const_fiolta = excluded.c_pay_acq_const_fiolta, c_paid_invest = excluded.c_paid_invest, n_disp_subs_oth_biz = excluded.n_disp_subs_oth_biz, oth_pay_ral_inv_act = excluded.oth_pay_ral_inv_act, n_incr_pledge_loan = excluded.n_incr_pledge_loan, stot_out_inv_act = excluded.stot_out_inv_act, n_cashflow_inv_act = excluded.n_cashflow_inv_act, c_recp_borrow = excluded.c_recp_borrow, proc_issue_bonds = excluded.proc_issue_bonds, oth_cash_recp_ral_fnc_act = excluded.oth_cash_recp_ral_fnc_act, stot_cash_in_fnc_act = excluded.stot_cash_in_fnc_act, free_cashflow = excluded.free_cashflow, c_prepay_amt_borr = excluded.c_prepay_amt_borr, c_pay_dist_dpcp_int_exp = excluded.c_pay_dist_dpcp_int_exp, incl_dvd_profit_paid_sc_ms = excluded.incl_dvd_profit_paid_sc_ms, oth_cashpay_ral_fnc_act = excluded.oth_cashpay_ral_fnc_act, stot_cashout_fnc_act = excluded.stot_cashout_fnc_act, n_cash_flows_fnc_act = excluded.n_cash_flows_fnc_act, eff_fx_flu_cash = excluded.eff_fx_flu_cash, n_incr_cash_cash_equ = excluded.n_incr_cash_cash_equ, c_cash_equ_beg_period = excluded.c_cash_equ_beg_period, c_cash_equ_end_period = excluded.c_cash_equ_end_period, c_recp_cap_contrib = excluded.c_recp_cap_contrib, incl_cash_rec_saims = excluded.incl_cash_rec_saims, uncon_invest_loss = excluded.uncon_invest_loss, prov_depr_assets = excluded.prov_depr_assets, depr_fa_coga_dpba = excluded.depr_fa_coga_dpba, amort_intang_assets = excluded.amort_intang_assets, lt_amort_deferred_exp = excluded.lt_amort_deferred_exp, decr_deferred_exp = excluded.decr_deferred_exp, incr_acc_exp = excluded.incr_acc_exp, loss_disp_fiolta = excluded.loss_disp_fiolta, loss_scr_fa = excluded.loss_scr_fa, loss_fv_chg = excluded.loss_fv_chg, invest_loss = excluded.invest_loss, decr_def_inc_tax_assets = excluded.decr_def_inc_tax_assets, incr_def_inc_tax_liab = excluded.incr_def_inc_tax_liab, decr_inventories = excluded.decr_inventories, decr_oper_payable = excluded.decr_oper_payable, incr_oper_payable = excluded.incr_oper_payable, others = excluded.others, im_net_cashflow_oper_act = excluded.im_net_cashflow_oper_act, conv_debt_into_cap = excluded.conv_debt_into_cap, conv_copbonds_due_within_1y = excluded.conv_copbonds_due_within_1y, fa_fnc_leases = excluded.fa_fnc_leases, im_n_incr_cash_equ = excluded.im_n_incr_cash_equ, net_dism_capital_add = excluded.net_dism_capital_add, net_cash_rece_sec = excluded.net_cash_rece_sec, credit_impa_loss = excluded.credit_impa_loss, use_right_asset_dep = excluded.use_right_asset_dep, oth_loss_asset = excluded.oth_loss_asset, end_bal_cash = excluded.end_bal_cash, beg_bal_cash = excluded.beg_bal_cash, end_bal_cash_equ = excluded.end_bal_cash_equ, beg_bal_cash_equ = excluded.beg_bal_cash_equ, update_flag = excluded.update_flag, updated_at = NOW()"

        return f"""
            INSERT INTO cashflow (ts_code, ann_date, f_ann_date, end_date, comp_type, report_type, end_type, net_profit, finan_exp, c_fr_sale_sg, recp_tax_rends, n_depos_incr_fi, n_incr_loans_cb, n_inc_borr_oth_fi, prem_fr_orig_contr, n_incr_insured_dep, n_reinsur_prem, n_incr_disp_tfa, ifc_cash_incr, n_incr_disp_faas, n_incr_loans_oth_bank, n_cap_incr_repur, c_fr_oth_operate_a, c_inf_fr_operate_a, c_paid_goods_s, c_paid_to_for_empl, c_paid_for_taxes, n_incr_clt_loan_adv, n_incr_dep_cbob, c_pay_claims_orig_inco, pay_handling_chrg, pay_comm_insur_plcy, oth_cash_pay_oper_act, st_cash_out_act, n_cashflow_act, oth_recp_ral_inv_act, c_disp_withdrwl_invest, c_recp_return_invest, n_recp_disp_fiolta, n_recp_disp_sobu, stot_inflows_inv_act, c_pay_acq_const_fiolta, c_paid_invest, n_disp_subs_oth_biz, oth_pay_ral_inv_act, n_incr_pledge_loan, stot_out_inv_act, n_cashflow_inv_act, c_recp_borrow, proc_issue_bonds, oth_cash_recp_ral_fnc_act, stot_cash_in_fnc_act, free_cashflow, c_prepay_amt_borr, c_pay_dist_dpcp_int_exp, incl_dvd_profit_paid_sc_ms, oth_cashpay_ral_fnc_act, stot_cashout_fnc_act, n_cash_flows_fnc_act, eff_fx_flu_cash, n_incr_cash_cash_equ, c_cash_equ_beg_period, c_cash_equ_end_period, c_recp_cap_contrib, incl_cash_rec_saims, uncon_invest_loss, prov_depr_assets, depr_fa_coga_dpba, amort_intang_assets, lt_amort_deferred_exp, decr_deferred_exp, incr_acc_exp, loss_disp_fiolta, loss_scr_fa, loss_fv_chg, invest_loss, decr_def_inc_tax_assets, incr_def_inc_tax_liab, decr_inventories, decr_oper_payable, incr_oper_payable, others, im_net_cashflow_oper_act, conv_debt_into_cap, conv_copbonds_due_within_1y, fa_fnc_leases, im_n_incr_cash_equ, net_dism_capital_add, net_cash_rece_sec, credit_impa_loss, use_right_asset_dep, oth_loss_asset, end_bal_cash, beg_bal_cash, end_bal_cash_equ, beg_bal_cash_equ, update_flag, updated_at)
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