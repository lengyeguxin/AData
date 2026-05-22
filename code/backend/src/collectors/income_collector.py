"""
IncomeCollector - 利润表拉取器（VIP接口）

严格按照CSV文档：
- 接口名称：income_vip（VIP接口）
- 接口参数：ann_date={游标+1}、report_type=1
- 文档地址：https://tushare.pro/document/2%sdoc_id=33
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


class IncomeCollector(BaseCollector):
    """利润表拉取器（P2财务表，VIP接口，按自然日拉取）"""

    def __init__(self, db_config: dict, api: TushareAPI):
        """
        初始化IncomeCollector

        Args:
            db_config: 数据库配置字典
            api: TushareAPI实例
        """
        super().__init__(
            db_config=db_config,
            api=api,
            table_name='income',
            api_name='income_vip',  # VIP接口（严格按照CSV文档）
            date_field='ann_date',  # 公告日期（按自然日）
            vip_interface=True  # VIP接口
        )

    def collect_by_ann_date(self, ann_date: str) -> List[Dict]:
        """
        拉取指定公告日期的利润表数据（VIP接口）

        Args:
            ann_date: 公告日期（YYYYMMDD格式）

        Returns:
            利润表数据列表

        示例：
            collect_by_ann_date('20260409') → 拉取2026-04-09公告的利润表

        注意：
            - 使用VIP接口income_vip（更丰富字段）
            - ann_date可能无数据（正常情况，财务数据公告不规律）
        """
        self.logger.info(f"拉取利润表（VIP接口）: ann_date={ann_date}")

        # 严格按照CSV文档参数
        data = self.collect(ann_date=ann_date, report_type='1')  # 合并报表

        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照income_schema.sql定义，完整94个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（94个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('f_ann_date')),
            convert_date_format(item.get('end_date')),
            item.get('report_type'),
            item.get('comp_type'),
            item.get('end_type'),
            item.get('basic_eps'),
            item.get('diluted_eps'),
            item.get('total_revenue'),
            item.get('revenue'),
            item.get('int_income'),
            item.get('prem_earned'),
            item.get('comm_income'),
            item.get('n_commis_income'),
            item.get('n_oth_income'),
            item.get('n_oth_b_income'),
            item.get('prem_income'),
            item.get('out_prem'),
            item.get('une_prem_reser'),
            item.get('reins_income'),
            item.get('n_sec_tb_income'),
            item.get('n_sec_uw_income'),
            item.get('n_asset_mg_income'),
            item.get('oth_b_income'),
            item.get('fv_value_chg_gain'),
            item.get('invest_income'),
            item.get('ass_invest_income'),
            item.get('forex_gain'),
            item.get('total_cogs'),
            item.get('oper_cost'),
            item.get('int_exp'),
            item.get('comm_exp'),
            item.get('biz_tax_surchg'),
            item.get('sell_exp'),
            item.get('admin_exp'),
            item.get('fin_exp'),
            item.get('assets_impair_loss'),
            item.get('prem_refund'),
            item.get('compens_payout'),
            item.get('reser_insur_liab'),
            item.get('div_payt'),
            item.get('reins_exp'),
            item.get('oper_exp'),
            item.get('compens_payout_refu'),
            item.get('insur_reser_refu'),
            item.get('reins_cost_refund'),
            item.get('other_bus_cost'),
            item.get('operate_profit'),
            item.get('non_oper_income'),
            item.get('non_oper_exp'),
            item.get('nca_disploss'),
            item.get('total_profit'),
            item.get('income_tax'),
            item.get('n_income'),
            item.get('n_income_attr_p'),
            item.get('minority_gain'),
            item.get('oth_compr_income'),
            item.get('t_compr_income'),
            item.get('compr_inc_attr_p'),
            item.get('compr_inc_attr_m_s'),
            item.get('ebit'),
            item.get('ebitda'),
            item.get('insurance_exp'),
            item.get('undist_profit'),
            item.get('distable_profit'),
            item.get('rd_exp'),
            item.get('fin_exp_int_exp'),
            item.get('fin_exp_int_inc'),
            item.get('transfer_surplus_rese'),
            item.get('transfer_housing_imprest'),
            item.get('transfer_oth'),
            item.get('adj_lossgain'),
            item.get('withdra_legal_surplus'),
            item.get('withdra_legal_pubfund'),
            item.get('withdra_biz_devfund'),
            item.get('withdra_rese_fund'),
            item.get('withdra_oth_ersu'),
            item.get('workers_welfare'),
            item.get('distr_profit_shrhder'),
            item.get('prfshare_payable_dvd'),
            item.get('comshare_payable_dvd'),
            item.get('capit_comstock_div'),
            item.get('net_after_nr_lp_correct'),
            item.get('credit_impa_loss'),
            item.get('net_expo_hedging_benefits'),
            item.get('oth_impair_loss_assets'),
            item.get('total_opcost'),
            item.get('amodcost_fin_assets'),
            item.get('oth_income'),
            item.get('asset_disp_income'),
            item.get('continued_net_profit'),
            item.get('end_net_profit'),
            item.get('update_flag'),
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整94个字段）

        Returns:
            INSERT SQL语句

        注意：
            - DuckDB不允许在ON CONFLICT中更新ann_date字段（有约束限制）
            - 主键：PRIMARY KEY (ts_code, end_date, report_type)
        """
        fields = "ts_code, ann_date, f_ann_date, end_date, report_type, comp_type, end_type, basic_eps, diluted_eps, total_revenue, revenue, int_income, prem_earned, comm_income, n_commis_income, n_oth_income, n_oth_b_income, prem_income, out_prem, une_prem_reser, reins_income, n_sec_tb_income, n_sec_uw_income, n_asset_mg_income, oth_b_income, fv_value_chg_gain, invest_income, ass_invest_income, forex_gain, total_cogs, oper_cost, int_exp, comm_exp, biz_tax_surchg, sell_exp, admin_exp, fin_exp, assets_impair_loss, prem_refund, compens_payout, reser_insur_liab, div_payt, reins_exp, oper_exp, compens_payout_refu, insur_reser_refu, reins_cost_refund, other_bus_cost, operate_profit, non_oper_income, non_oper_exp, nca_disploss, total_profit, income_tax, n_income, n_income_attr_p, minority_gain, oth_compr_income, t_compr_income, compr_inc_attr_p, compr_inc_attr_m_s, ebit, ebitda, insurance_exp, undist_profit, distable_profit, rd_exp, fin_exp_int_exp, fin_exp_int_inc, transfer_surplus_rese, transfer_housing_imprest, transfer_oth, adj_lossgain, withdra_legal_surplus, withdra_legal_pubfund, withdra_biz_devfund, withdra_rese_fund, withdra_oth_ersu, workers_welfare, distr_profit_shrhder, prfshare_payable_dvd, comshare_payable_dvd, capit_comstock_div, net_after_nr_lp_correct, credit_impa_loss, net_expo_hedging_benefits, oth_impair_loss_assets, total_opcost, amodcost_fin_assets, oth_income, asset_disp_income, continued_net_profit, end_net_profit, update_flag, updated_at"

        placeholders = ', '.join(['%s'] * 94) + ', NOW()'

        update_fields = "f_ann_date = excluded.f_ann_date, comp_type = excluded.comp_type, end_type = excluded.end_type, basic_eps = excluded.basic_eps, diluted_eps = excluded.diluted_eps, total_revenue = excluded.total_revenue, revenue = excluded.revenue, int_income = excluded.int_income, prem_earned = excluded.prem_earned, comm_income = excluded.comm_income, n_commis_income = excluded.n_commis_income, n_oth_income = excluded.n_oth_income, n_oth_b_income = excluded.n_oth_b_income, prem_income = excluded.prem_income, out_prem = excluded.out_prem, une_prem_reser = excluded.une_prem_reser, reins_income = excluded.reins_income, n_sec_tb_income = excluded.n_sec_tb_income, n_sec_uw_income = excluded.n_sec_uw_income, n_asset_mg_income = excluded.n_asset_mg_income, oth_b_income = excluded.oth_b_income, fv_value_chg_gain = excluded.fv_value_chg_gain, invest_income = excluded.invest_income, ass_invest_income = excluded.ass_invest_income, forex_gain = excluded.forex_gain, total_cogs = excluded.total_cogs, oper_cost = excluded.oper_cost, int_exp = excluded.int_exp, comm_exp = excluded.comm_exp, biz_tax_surchg = excluded.biz_tax_surchg, sell_exp = excluded.sell_exp, admin_exp = excluded.admin_exp, fin_exp = excluded.fin_exp, assets_impair_loss = excluded.assets_impair_loss, prem_refund = excluded.prem_refund, compens_payout = excluded.compens_payout, reser_insur_liab = excluded.reser_insur_liab, div_payt = excluded.div_payt, reins_exp = excluded.reins_exp, oper_exp = excluded.oper_exp, compens_payout_refu = excluded.compens_payout_refu, insur_reser_refu = excluded.insur_reser_refu, reins_cost_refund = excluded.reins_cost_refund, other_bus_cost = excluded.other_bus_cost, operate_profit = excluded.operate_profit, non_oper_income = excluded.non_oper_income, non_oper_exp = excluded.non_oper_exp, nca_disploss = excluded.nca_disploss, total_profit = excluded.total_profit, income_tax = excluded.income_tax, n_income = excluded.n_income, n_income_attr_p = excluded.n_income_attr_p, minority_gain = excluded.minority_gain, oth_compr_income = excluded.oth_compr_income, t_compr_income = excluded.t_compr_income, compr_inc_attr_p = excluded.compr_inc_attr_p, compr_inc_attr_m_s = excluded.compr_inc_attr_m_s, ebit = excluded.ebit, ebitda = excluded.ebitda, insurance_exp = excluded.insurance_exp, undist_profit = excluded.undist_profit, distable_profit = excluded.distable_profit, rd_exp = excluded.rd_exp, fin_exp_int_exp = excluded.fin_exp_int_exp, fin_exp_int_inc = excluded.fin_exp_int_inc, transfer_surplus_rese = excluded.transfer_surplus_rese, transfer_housing_imprest = excluded.transfer_housing_imprest, transfer_oth = excluded.transfer_oth, adj_lossgain = excluded.adj_lossgain, withdra_legal_surplus = excluded.withdra_legal_surplus, withdra_legal_pubfund = excluded.withdra_legal_pubfund, withdra_biz_devfund = excluded.withdra_biz_devfund, withdra_rese_fund = excluded.withdra_rese_fund, withdra_oth_ersu = excluded.withdra_oth_ersu, workers_welfare = excluded.workers_welfare, distr_profit_shrhder = excluded.distr_profit_shrhder, prfshare_payable_dvd = excluded.prfshare_payable_dvd, comshare_payable_dvd = excluded.comshare_payable_dvd, capit_comstock_div = excluded.capit_comstock_div, net_after_nr_lp_correct = excluded.net_after_nr_lp_correct, credit_impa_loss = excluded.credit_impa_loss, net_expo_hedging_benefits = excluded.net_expo_hedging_benefits, oth_impair_loss_assets = excluded.oth_impair_loss_assets, total_opcost = excluded.total_opcost, amodcost_fin_assets = excluded.amodcost_fin_assets, oth_income = excluded.oth_income, asset_disp_income = excluded.asset_disp_income, continued_net_profit = excluded.continued_net_profit, end_net_profit = excluded.end_net_profit, update_flag = excluded.update_flag, updated_at = NOW()"

        return f"""
            INSERT INTO income (ts_code, ann_date, f_ann_date, end_date, report_type, comp_type, end_type, basic_eps, diluted_eps, total_revenue, revenue, int_income, prem_earned, comm_income, n_commis_income, n_oth_income, n_oth_b_income, prem_income, out_prem, une_prem_reser, reins_income, n_sec_tb_income, n_sec_uw_income, n_asset_mg_income, oth_b_income, fv_value_chg_gain, invest_income, ass_invest_income, forex_gain, total_cogs, oper_cost, int_exp, comm_exp, biz_tax_surchg, sell_exp, admin_exp, fin_exp, assets_impair_loss, prem_refund, compens_payout, reser_insur_liab, div_payt, reins_exp, oper_exp, compens_payout_refu, insur_reser_refu, reins_cost_refund, other_bus_cost, operate_profit, non_oper_income, non_oper_exp, nca_disploss, total_profit, income_tax, n_income, n_income_attr_p, minority_gain, oth_compr_income, t_compr_income, compr_inc_attr_p, compr_inc_attr_m_s, ebit, ebitda, insurance_exp, undist_profit, distable_profit, rd_exp, fin_exp_int_exp, fin_exp_int_inc, transfer_surplus_rese, transfer_housing_imprest, transfer_oth, adj_lossgain, withdra_legal_surplus, withdra_legal_pubfund, withdra_biz_devfund, withdra_rese_fund, withdra_oth_ersu, workers_welfare, distr_profit_shrhder, prfshare_payable_dvd, comshare_payable_dvd, capit_comstock_div, net_after_nr_lp_correct, credit_impa_loss, net_expo_hedging_benefits, oth_impair_loss_assets, total_opcost, amodcost_fin_assets, oth_income, asset_disp_income, continued_net_profit, end_net_profit, update_flag, updated_at)
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