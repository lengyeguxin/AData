"""
BalancesheetCollector - 资产负债表拉取器（VIP接口）

严格按照CSV文档：
- 接口名称：balancesheet_vip（VIP接口）
- 接口参数：ann_date={游标+1}、report_type=1
- 文档地址：https://tushare.pro/document/2%sdoc_id=36
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


class BalancesheetCollector(BaseCollector):
    """资产负债表拉取器（P2财务表，VIP接口，按自然日拉取）"""

    def __init__(self, db_config: dict, api: TushareAPI):
        """
        初始化BalancesheetCollector

        Args:
            db_config: 数据库配置字典
            api: TushareAPI实例
        """
        super().__init__(
            db_config=db_config,
            api=api,
            table_name='balancesheet',
            api_name='balancesheet_vip',  # VIP接口（严格按照CSV文档）
            date_field='ann_date',  # 公告日期（按自然日）
            vip_interface=True  # VIP接口
        )

    def collect_by_ann_date(self, ann_date: str) -> List[Dict]:
        """
        拉取指定公告日期的资产负债表数据（VIP接口）

        Args:
            ann_date: 公告日期（YYYYMMDD格式）

        Returns:
            资产负债表数据列表

        示例：
            collect_by_ann_date('20260409') → 拉取2026-04-09公告的资产负债表

        注意：
            - 使用VIP接口balancesheet_vip（更丰富字段）
            - ann_date可能无数据（正常情况，财务数据公告不规律）
        """
        self.logger.info(f"拉取资产负债表（VIP接口）: ann_date={ann_date}")

        # 严格按照CSV文档参数
        data = self.collect(ann_date=ann_date, report_type='1')  # 合并报表

        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照balancesheet_schema.sql定义，完整158个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（158个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('f_ann_date')),
            convert_date_format(item.get('end_date')),
            item.get('report_type'),
            item.get('comp_type'),
            item.get('end_type'),
            item.get('total_share'),
            item.get('cap_rese'),
            item.get('undistr_porfit'),
            item.get('surplus_rese'),
            item.get('special_rese'),
            item.get('money_cap'),
            item.get('trad_asset'),
            item.get('notes_receiv'),
            item.get('accounts_receiv'),
            item.get('oth_receiv'),
            item.get('prepayment'),
            item.get('div_receiv'),
            item.get('int_receiv'),
            item.get('inventories'),
            item.get('amor_exp'),
            item.get('nca_within_1y'),
            item.get('sett_rsrv'),
            item.get('loanto_oth_bank_fi'),
            item.get('premium_receiv'),
            item.get('reinsur_receiv'),
            item.get('reinsur_res_receiv'),
            item.get('pur_resale_fa'),
            item.get('oth_cur_assets'),
            item.get('total_cur_assets'),
            item.get('fa_avail_for_sale'),
            item.get('htm_invest'),
            item.get('lt_eqt_invest'),
            item.get('invest_real_estate'),
            item.get('time_deposits'),
            item.get('oth_assets'),
            item.get('lt_rec'),
            item.get('fix_assets'),
            item.get('cip'),
            item.get('const_materials'),
            item.get('fixed_assets_disp'),
            item.get('produc_bio_assets'),
            item.get('oil_and_gas_assets'),
            item.get('intan_assets'),
            item.get('r_and_d'),
            item.get('goodwill'),
            item.get('lt_amor_exp'),
            item.get('defer_tax_assets'),
            item.get('decr_in_disbur'),
            item.get('oth_nca'),
            item.get('total_nca'),
            item.get('cash_reser_cb'),
            item.get('depos_in_oth_bfi'),
            item.get('prec_metals'),
            item.get('deriv_assets'),
            item.get('rr_reins_une_prem'),
            item.get('rr_reins_outstd_cla'),
            item.get('rr_reins_lins_liab'),
            item.get('rr_reins_lthins_liab'),
            item.get('refund_depos'),
            item.get('ph_pledge_loans'),
            item.get('refund_cap_depos'),
            item.get('indep_acct_assets'),
            item.get('client_depos'),
            item.get('client_prov'),
            item.get('transac_seat_fee'),
            item.get('invest_as_receiv'),
            item.get('total_assets'),
            item.get('lt_borr'),
            item.get('st_borr'),
            item.get('cb_borr'),
            item.get('depos_ib_deposits'),
            item.get('loan_oth_bank'),
            item.get('trading_fl'),
            item.get('notes_payable'),
            item.get('acct_payable'),
            item.get('adv_receipts'),
            item.get('sold_for_repur_fa'),
            item.get('comm_payable'),
            item.get('payroll_payable'),
            item.get('taxes_payable'),
            item.get('int_payable'),
            item.get('div_payable'),
            item.get('oth_payable'),
            item.get('acc_exp'),
            item.get('deferred_inc'),
            item.get('st_bonds_payable'),
            item.get('payable_to_reinsurer'),
            item.get('rsrv_insur_cont'),
            item.get('acting_trading_sec'),
            item.get('acting_uw_sec'),
            item.get('non_cur_liab_due_1y'),
            item.get('oth_cur_liab'),
            item.get('total_cur_liab'),
            item.get('bond_payable'),
            item.get('lt_payable'),
            item.get('specific_payables'),
            item.get('estimated_liab'),
            item.get('defer_tax_liab'),
            item.get('defer_inc_non_cur_liab'),
            item.get('oth_ncl'),
            item.get('total_ncl'),
            item.get('depos_oth_bfi'),
            item.get('deriv_liab'),
            item.get('depos'),
            item.get('agency_bus_liab'),
            item.get('oth_liab'),
            item.get('prem_receiv_adva'),
            item.get('depos_received'),
            item.get('ph_invest'),
            item.get('reser_une_prem'),
            item.get('reser_outstd_claims'),
            item.get('reser_lins_liab'),
            item.get('reser_lthins_liab'),
            item.get('indept_acc_liab'),
            item.get('pledge_borr'),
            item.get('indem_payable'),
            item.get('policy_div_payable'),
            item.get('total_liab'),
            item.get('treasury_share'),
            item.get('ordin_risk_reser'),
            item.get('forex_differ'),
            item.get('invest_loss_unconf'),
            item.get('minority_int'),
            item.get('total_hldr_eqy_exc_min_int'),
            item.get('total_hldr_eqy_inc_min_int'),
            item.get('total_liab_hldr_eqy'),
            item.get('lt_payroll_payable'),
            item.get('oth_comp_income'),
            item.get('oth_eqt_tools'),
            item.get('oth_eqt_tools_p_shr'),
            item.get('lending_funds'),
            item.get('acc_receivable'),
            item.get('st_fin_payable'),
            item.get('payables'),
            item.get('hfs_assets'),
            item.get('hfs_sales'),
            item.get('cost_fin_assets'),
            item.get('fair_value_fin_assets'),
            item.get('cip_total'),
            item.get('oth_pay_total'),
            item.get('long_pay_total'),
            item.get('debt_invest'),
            item.get('oth_debt_invest'),
            item.get('oth_eq_invest'),
            item.get('oth_illiq_fin_assets'),
            item.get('oth_eq_ppbond'),
            item.get('receiv_financing'),
            item.get('use_right_assets'),
            item.get('lease_liab'),
            item.get('contract_assets'),
            item.get('contract_liab'),
            item.get('accounts_receiv_bill'),
            item.get('accounts_pay'),
            item.get('oth_rcv_total'),
            item.get('fix_assets_total'),
            item.get('update_flag'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整158个字段）

        Returns:
            INSERT SQL语句

        注意：
            - DuckDB不允许在ON CONFLICT中更新ann_date字段（有约束限制）
            - 主键：PRIMARY KEY (ts_code, end_date, report_type)
        """
        fields = "ts_code, ann_date, f_ann_date, end_date, report_type, comp_type, end_type, total_share, cap_rese, undistr_porfit, surplus_rese, special_rese, money_cap, trad_asset, notes_receiv, accounts_receiv, oth_receiv, prepayment, div_receiv, int_receiv, inventories, amor_exp, nca_within_1y, sett_rsrv, loanto_oth_bank_fi, premium_receiv, reinsur_receiv, reinsur_res_receiv, pur_resale_fa, oth_cur_assets, total_cur_assets, fa_avail_for_sale, htm_invest, lt_eqt_invest, invest_real_estate, time_deposits, oth_assets, lt_rec, fix_assets, cip, const_materials, fixed_assets_disp, produc_bio_assets, oil_and_gas_assets, intan_assets, r_and_d, goodwill, lt_amor_exp, defer_tax_assets, decr_in_disbur, oth_nca, total_nca, cash_reser_cb, depos_in_oth_bfi, prec_metals, deriv_assets, rr_reins_une_prem, rr_reins_outstd_cla, rr_reins_lins_liab, rr_reins_lthins_liab, refund_depos, ph_pledge_loans, refund_cap_depos, indep_acct_assets, client_depos, client_prov, transac_seat_fee, invest_as_receiv, total_assets, lt_borr, st_borr, cb_borr, depos_ib_deposits, loan_oth_bank, trading_fl, notes_payable, acct_payable, adv_receipts, sold_for_repur_fa, comm_payable, payroll_payable, taxes_payable, int_payable, div_payable, oth_payable, acc_exp, deferred_inc, st_bonds_payable, payable_to_reinsurer, rsrv_insur_cont, acting_trading_sec, acting_uw_sec, non_cur_liab_due_1y, oth_cur_liab, total_cur_liab, bond_payable, lt_payable, specific_payables, estimated_liab, defer_tax_liab, defer_inc_non_cur_liab, oth_ncl, total_ncl, depos_oth_bfi, deriv_liab, depos, agency_bus_liab, oth_liab, prem_receiv_adva, depos_received, ph_invest, reser_une_prem, reser_outstd_claims, reser_lins_liab, reser_lthins_liab, indept_acc_liab, pledge_borr, indem_payable, policy_div_payable, total_liab, treasury_share, ordin_risk_reser, forex_differ, invest_loss_unconf, minority_int, total_hldr_eqy_exc_min_int, total_hldr_eqy_inc_min_int, total_liab_hldr_eqy, lt_payroll_payable, oth_comp_income, oth_eqt_tools, oth_eqt_tools_p_shr, lending_funds, acc_receivable, st_fin_payable, payables, hfs_assets, hfs_sales, cost_fin_assets, fair_value_fin_assets, cip_total, oth_pay_total, long_pay_total, debt_invest, oth_debt_invest, oth_eq_invest, oth_illiq_fin_assets, oth_eq_ppbond, receiv_financing, use_right_assets, lease_liab, contract_assets, contract_liab, accounts_receiv_bill, accounts_pay, oth_rcv_total, fix_assets_total, update_flag, updated_at"

        placeholders = ', '.join(['%s'] * 158) + ', NOW()'

        update_fields = "f_ann_date = excluded.f_ann_date, comp_type = excluded.comp_type, end_type = excluded.end_type, total_share = excluded.total_share, cap_rese = excluded.cap_rese, undistr_porfit = excluded.undistr_porfit, surplus_rese = excluded.surplus_rese, special_rese = excluded.special_rese, money_cap = excluded.money_cap, trad_asset = excluded.trad_asset, notes_receiv = excluded.notes_receiv, accounts_receiv = excluded.accounts_receiv, oth_receiv = excluded.oth_receiv, prepayment = excluded.prepayment, div_receiv = excluded.div_receiv, int_receiv = excluded.int_receiv, inventories = excluded.inventories, amor_exp = excluded.amor_exp, nca_within_1y = excluded.nca_within_1y, sett_rsrv = excluded.sett_rsrv, loanto_oth_bank_fi = excluded.loanto_oth_bank_fi, premium_receiv = excluded.premium_receiv, reinsur_receiv = excluded.reinsur_receiv, reinsur_res_receiv = excluded.reinsur_res_receiv, pur_resale_fa = excluded.pur_resale_fa, oth_cur_assets = excluded.oth_cur_assets, total_cur_assets = excluded.total_cur_assets, fa_avail_for_sale = excluded.fa_avail_for_sale, htm_invest = excluded.htm_invest, lt_eqt_invest = excluded.lt_eqt_invest, invest_real_estate = excluded.invest_real_estate, time_deposits = excluded.time_deposits, oth_assets = excluded.oth_assets, lt_rec = excluded.lt_rec, fix_assets = excluded.fix_assets, cip = excluded.cip, const_materials = excluded.const_materials, fixed_assets_disp = excluded.fixed_assets_disp, produc_bio_assets = excluded.produc_bio_assets, oil_and_gas_assets = excluded.oil_and_gas_assets, intan_assets = excluded.intan_assets, r_and_d = excluded.r_and_d, goodwill = excluded.goodwill, lt_amor_exp = excluded.lt_amor_exp, defer_tax_assets = excluded.defer_tax_assets, decr_in_disbur = excluded.decr_in_disbur, oth_nca = excluded.oth_nca, total_nca = excluded.total_nca, cash_reser_cb = excluded.cash_reser_cb, depos_in_oth_bfi = excluded.depos_in_oth_bfi, prec_metals = excluded.prec_metals, deriv_assets = excluded.deriv_assets, rr_reins_une_prem = excluded.rr_reins_une_prem, rr_reins_outstd_cla = excluded.rr_reins_outstd_cla, rr_reins_lins_liab = excluded.rr_reins_lins_liab, rr_reins_lthins_liab = excluded.rr_reins_lthins_liab, refund_depos = excluded.refund_depos, ph_pledge_loans = excluded.ph_pledge_loans, refund_cap_depos = excluded.refund_cap_depos, indep_acct_assets = excluded.indep_acct_assets, client_depos = excluded.client_depos, client_prov = excluded.client_prov, transac_seat_fee = excluded.transac_seat_fee, invest_as_receiv = excluded.invest_as_receiv, total_assets = excluded.total_assets, lt_borr = excluded.lt_borr, st_borr = excluded.st_borr, cb_borr = excluded.cb_borr, depos_ib_deposits = excluded.depos_ib_deposits, loan_oth_bank = excluded.loan_oth_bank, trading_fl = excluded.trading_fl, notes_payable = excluded.notes_payable, acct_payable = excluded.acct_payable, adv_receipts = excluded.adv_receipts, sold_for_repur_fa = excluded.sold_for_repur_fa, comm_payable = excluded.comm_payable, payroll_payable = excluded.payroll_payable, taxes_payable = excluded.taxes_payable, int_payable = excluded.int_payable, div_payable = excluded.div_payable, oth_payable = excluded.oth_payable, acc_exp = excluded.acc_exp, deferred_inc = excluded.deferred_inc, st_bonds_payable = excluded.st_bonds_payable, payable_to_reinsurer = excluded.payable_to_reinsurer, rsrv_insur_cont = excluded.rsrv_insur_cont, acting_trading_sec = excluded.acting_trading_sec, acting_uw_sec = excluded.acting_uw_sec, non_cur_liab_due_1y = excluded.non_cur_liab_due_1y, oth_cur_liab = excluded.oth_cur_liab, total_cur_liab = excluded.total_cur_liab, bond_payable = excluded.bond_payable, lt_payable = excluded.lt_payable, specific_payables = excluded.specific_payables, estimated_liab = excluded.estimated_liab, defer_tax_liab = excluded.defer_tax_liab, defer_inc_non_cur_liab = excluded.defer_inc_non_cur_liab, oth_ncl = excluded.oth_ncl, total_ncl = excluded.total_ncl, depos_oth_bfi = excluded.depos_oth_bfi, deriv_liab = excluded.deriv_liab, depos = excluded.depos, agency_bus_liab = excluded.agency_bus_liab, oth_liab = excluded.oth_liab, prem_receiv_adva = excluded.prem_receiv_adva, depos_received = excluded.depos_received, ph_invest = excluded.ph_invest, reser_une_prem = excluded.reser_une_prem, reser_outstd_claims = excluded.reser_outstd_claims, reser_lins_liab = excluded.reser_lins_liab, reser_lthins_liab = excluded.reser_lthins_liab, indept_acc_liab = excluded.indept_acc_liab, pledge_borr = excluded.pledge_borr, indem_payable = excluded.indem_payable, policy_div_payable = excluded.policy_div_payable, total_liab = excluded.total_liab, treasury_share = excluded.treasury_share, ordin_risk_reser = excluded.ordin_risk_reser, forex_differ = excluded.forex_differ, invest_loss_unconf = excluded.invest_loss_unconf, minority_int = excluded.minority_int, total_hldr_eqy_exc_min_int = excluded.total_hldr_eqy_exc_min_int, total_hldr_eqy_inc_min_int = excluded.total_hldr_eqy_inc_min_int, total_liab_hldr_eqy = excluded.total_liab_hldr_eqy, lt_payroll_payable = excluded.lt_payroll_payable, oth_comp_income = excluded.oth_comp_income, oth_eqt_tools = excluded.oth_eqt_tools, oth_eqt_tools_p_shr = excluded.oth_eqt_tools_p_shr, lending_funds = excluded.lending_funds, acc_receivable = excluded.acc_receivable, st_fin_payable = excluded.st_fin_payable, payables = excluded.payables, hfs_assets = excluded.hfs_assets, hfs_sales = excluded.hfs_sales, cost_fin_assets = excluded.cost_fin_assets, fair_value_fin_assets = excluded.fair_value_fin_assets, cip_total = excluded.cip_total, oth_pay_total = excluded.oth_pay_total, long_pay_total = excluded.long_pay_total, debt_invest = excluded.debt_invest, oth_debt_invest = excluded.oth_debt_invest, oth_eq_invest = excluded.oth_eq_invest, oth_illiq_fin_assets = excluded.oth_illiq_fin_assets, oth_eq_ppbond = excluded.oth_eq_ppbond, receiv_financing = excluded.receiv_financing, use_right_assets = excluded.use_right_assets, lease_liab = excluded.lease_liab, contract_assets = excluded.contract_assets, contract_liab = excluded.contract_liab, accounts_receiv_bill = excluded.accounts_receiv_bill, accounts_pay = excluded.accounts_pay, oth_rcv_total = excluded.oth_rcv_total, fix_assets_total = excluded.fix_assets_total, update_flag = excluded.update_flag, updated_at = NOW()"

        return f"""
            INSERT INTO balancesheet (ts_code, ann_date, f_ann_date, end_date, report_type, comp_type, end_type, total_share, cap_rese, undistr_porfit, surplus_rese, special_rese, money_cap, trad_asset, notes_receiv, accounts_receiv, oth_receiv, prepayment, div_receiv, int_receiv, inventories, amor_exp, nca_within_1y, sett_rsrv, loanto_oth_bank_fi, premium_receiv, reinsur_receiv, reinsur_res_receiv, pur_resale_fa, oth_cur_assets, total_cur_assets, fa_avail_for_sale, htm_invest, lt_eqt_invest, invest_real_estate, time_deposits, oth_assets, lt_rec, fix_assets, cip, const_materials, fixed_assets_disp, produc_bio_assets, oil_and_gas_assets, intan_assets, r_and_d, goodwill, lt_amor_exp, defer_tax_assets, decr_in_disbur, oth_nca, total_nca, cash_reser_cb, depos_in_oth_bfi, prec_metals, deriv_assets, rr_reins_une_prem, rr_reins_outstd_cla, rr_reins_lins_liab, rr_reins_lthins_liab, refund_depos, ph_pledge_loans, refund_cap_depos, indep_acct_assets, client_depos, client_prov, transac_seat_fee, invest_as_receiv, total_assets, lt_borr, st_borr, cb_borr, depos_ib_deposits, loan_oth_bank, trading_fl, notes_payable, acct_payable, adv_receipts, sold_for_repur_fa, comm_payable, payroll_payable, taxes_payable, int_payable, div_payable, oth_payable, acc_exp, deferred_inc, st_bonds_payable, payable_to_reinsurer, rsrv_insur_cont, acting_trading_sec, acting_uw_sec, non_cur_liab_due_1y, oth_cur_liab, total_cur_liab, bond_payable, lt_payable, specific_payables, estimated_liab, defer_tax_liab, defer_inc_non_cur_liab, oth_ncl, total_ncl, depos_oth_bfi, deriv_liab, depos, agency_bus_liab, oth_liab, prem_receiv_adva, depos_received, ph_invest, reser_une_prem, reser_outstd_claims, reser_lins_liab, reser_lthins_liab, indept_acc_liab, pledge_borr, indem_payable, policy_div_payable, total_liab, treasury_share, ordin_risk_reser, forex_differ, invest_loss_unconf, minority_int, total_hldr_eqy_exc_min_int, total_hldr_eqy_inc_min_int, total_liab_hldr_eqy, lt_payroll_payable, oth_comp_income, oth_eqt_tools, oth_eqt_tools_p_shr, lending_funds, acc_receivable, st_fin_payable, payables, hfs_assets, hfs_sales, cost_fin_assets, fair_value_fin_assets, cip_total, oth_pay_total, long_pay_total, debt_invest, oth_debt_invest, oth_eq_invest, oth_illiq_fin_assets, oth_eq_ppbond, receiv_financing, use_right_assets, lease_liab, contract_assets, contract_liab, accounts_receiv_bill, accounts_pay, oth_rcv_total, fix_assets_total, update_flag, updated_at)
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