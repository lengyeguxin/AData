"""
FinaIndicatorCollector - 财务指标拉取器

严格按照CSV文档：
- 接口名称：fina_indicator_vip（VIP接口）
- 接口参数：ann_date={游标+1}
- 文档地址：https://tushare.pro/document/2?doc_id=79
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


class FinaIndicatorCollector(BaseCollector):
    """财务指标拉取器（P2财务表，VIP接口，按自然日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化FinaIndicatorCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='fina_indicator',
            api_name='fina_indicator_vip',  # VIP接口（严格按照CSV文档）
            date_field='ann_date',  # 公告日期（按自然日）
            vip_interface=True  # VIP接口
        )

    def collect_by_ann_date(self, ann_date: str) -> List[Dict]:
        """
        拉取指定公告日期的财务指标数据（VIP接口）

        Args:
            ann_date: 公告日期（YYYYMMDD格式）

        Returns:
            财务指标数据列表

        示例：
            collect_by_ann_date('20260409') → 拉取2026-04-09公告的财务指标

        注意：
            - 使用VIP接口fina_indicator_vip（更丰富字段）
            - ann_date可能无数据（正常情况，财务数据公告不规律）
        """
        self.logger.info(f"拉取财务指标（VIP接口）: ann_date={ann_date}")

        # 严格按照CSV文档参数
        data = self.collect(ann_date=ann_date)

        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照fina_indicator_schema.sql定义，完整167个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（167个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('end_date')),
            item.get('eps'),
            item.get('dt_eps'),
            item.get('total_revenue_ps'),
            item.get('revenue_ps'),
            item.get('capital_rese_ps'),
            item.get('surplus_rese_ps'),
            item.get('undist_profit_ps'),
            item.get('extra_item'),
            item.get('profit_dedt'),
            item.get('gross_margin'),
            item.get('current_ratio'),
            item.get('quick_ratio'),
            item.get('cash_ratio'),
            item.get('invturn_days'),
            item.get('arturn_days'),
            item.get('inv_turn'),
            item.get('ar_turn'),
            item.get('ca_turn'),
            item.get('fa_turn'),
            item.get('assets_turn'),
            item.get('op_income'),
            item.get('valuechange_income'),
            item.get('interst_income'),
            item.get('daa'),
            item.get('ebit'),
            item.get('ebitda'),
            item.get('fcff'),
            item.get('fcfe'),
            item.get('current_exint'),
            item.get('noncurrent_exint'),
            item.get('interestdebt'),
            item.get('netdebt'),
            item.get('tangible_asset'),
            item.get('working_capital'),
            item.get('networking_capital'),
            item.get('invest_capital'),
            item.get('retained_earnings'),
            item.get('diluted2_eps'),
            item.get('bps'),
            item.get('ocfps'),
            item.get('retainedps'),
            item.get('cfps'),
            item.get('ebit_ps'),
            item.get('fcff_ps'),
            item.get('fcfe_ps'),
            item.get('netprofit_margin'),
            item.get('grossprofit_margin'),
            item.get('cogs_of_sales'),
            item.get('expense_of_sales'),
            item.get('profit_to_gr'),
            item.get('saleexp_to_gr'),
            item.get('adminexp_of_gr'),
            item.get('finaexp_of_gr'),
            item.get('impai_ttm'),
            item.get('gc_of_gr'),
            item.get('op_of_gr'),
            item.get('ebit_of_gr'),
            item.get('roe'),
            item.get('roe_waa'),
            item.get('roe_dt'),
            item.get('roa'),
            item.get('npta'),
            item.get('roic'),
            item.get('roe_yearly'),
            item.get('roa2_yearly'),
            item.get('roe_avg'),
            item.get('opincome_of_ebt'),
            item.get('investincome_of_ebt'),
            item.get('n_op_profit_of_ebt'),
            item.get('tax_to_ebt'),
            item.get('dtprofit_to_profit'),
            item.get('salescash_to_or'),
            item.get('ocf_to_or'),
            item.get('ocf_to_opincome'),
            item.get('capitalized_to_da'),
            item.get('debt_to_assets'),
            item.get('assets_to_eqt'),
            item.get('dp_assets_to_eqt'),
            item.get('ca_to_assets'),
            item.get('nca_to_assets'),
            item.get('tbassets_to_totalassets'),
            item.get('int_to_talcap'),
            item.get('eqt_to_talcapital'),
            item.get('currentdebt_to_debt'),
            item.get('longdeb_to_debt'),
            item.get('ocf_to_shortdebt'),
            item.get('debt_to_eqt'),
            item.get('eqt_to_debt'),
            item.get('eqt_to_interestdebt'),
            item.get('tangibleasset_to_debt'),
            item.get('tangasset_to_intdebt'),
            item.get('tangibleasset_to_netdebt'),
            item.get('ocf_to_debt'),
            item.get('ocf_to_interestdebt'),
            item.get('ocf_to_netdebt'),
            item.get('ebit_to_interest'),
            item.get('longdebt_to_workingcapital'),
            item.get('ebitda_to_debt'),
            item.get('turn_days'),
            item.get('roa_yearly'),
            item.get('roa_dp'),
            item.get('fixed_assets'),
            item.get('profit_prefin_exp'),
            item.get('non_op_profit'),
            item.get('op_to_ebt'),
            item.get('nop_to_ebt'),
            item.get('ocf_to_profit'),
            item.get('cash_to_liqdebt'),
            item.get('cash_to_liqdebt_withinterest'),
            item.get('op_to_liqdebt'),
            item.get('op_to_debt'),
            item.get('roic_yearly'),
            item.get('total_fa_trun'),
            item.get('profit_to_op'),
            item.get('q_opincome'),
            item.get('q_investincome'),
            item.get('q_dtprofit'),
            item.get('q_eps'),
            item.get('q_netprofit_margin'),
            item.get('q_gsprofit_margin'),
            item.get('q_exp_to_sales'),
            item.get('q_profit_to_gr'),
            item.get('q_saleexp_to_gr'),
            item.get('q_adminexp_to_gr'),
            item.get('q_finaexp_to_gr'),
            item.get('q_impair_to_gr_ttm'),
            item.get('q_gc_to_gr'),
            item.get('q_op_to_gr'),
            item.get('q_roe'),
            item.get('q_dt_roe'),
            item.get('q_npta'),
            item.get('q_opincome_to_ebt'),
            item.get('q_investincome_to_ebt'),
            item.get('q_dtprofit_to_profit'),
            item.get('q_salescash_to_or'),
            item.get('q_ocf_to_sales'),
            item.get('q_ocf_to_or'),
            item.get('basic_eps_yoy'),
            item.get('dt_eps_yoy'),
            item.get('cfps_yoy'),
            item.get('op_yoy'),
            item.get('ebt_yoy'),
            item.get('netprofit_yoy'),
            item.get('dt_netprofit_yoy'),
            item.get('ocf_yoy'),
            item.get('roe_yoy'),
            item.get('bps_yoy'),
            item.get('assets_yoy'),
            item.get('eqt_yoy'),
            item.get('tr_yoy'),
            item.get('or_yoy'),
            item.get('q_gr_yoy'),
            item.get('q_gr_qoq'),
            item.get('q_sales_yoy'),
            item.get('q_sales_qoq'),
            item.get('q_op_yoy'),
            item.get('q_op_qoq'),
            item.get('q_profit_yoy'),
            item.get('q_profit_qoq'),
            item.get('q_netprofit_yoy'),
            item.get('q_netprofit_qoq'),
            item.get('equity_yoy'),
            item.get('rd_exp'),
            item.get('update_flag'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整167个字段）

        Returns:
            INSERT SQL语句

        注意：
            - DuckDB不允许在ON CONFLICT中更新ann_date字段（有约束限制）
            - 主键：PRIMARY KEY (ts_code, end_date)
        """
        fields = "ts_code, ann_date, end_date, eps, dt_eps, total_revenue_ps, revenue_ps, capital_rese_ps, surplus_rese_ps, undist_profit_ps, extra_item, profit_dedt, gross_margin, current_ratio, quick_ratio, cash_ratio, invturn_days, arturn_days, inv_turn, ar_turn, ca_turn, fa_turn, assets_turn, op_income, valuechange_income, interst_income, daa, ebit, ebitda, fcff, fcfe, current_exint, noncurrent_exint, interestdebt, netdebt, tangible_asset, working_capital, networking_capital, invest_capital, retained_earnings, diluted2_eps, bps, ocfps, retainedps, cfps, ebit_ps, fcff_ps, fcfe_ps, netprofit_margin, grossprofit_margin, cogs_of_sales, expense_of_sales, profit_to_gr, saleexp_to_gr, adminexp_of_gr, finaexp_of_gr, impai_ttm, gc_of_gr, op_of_gr, ebit_of_gr, roe, roe_waa, roe_dt, roa, npta, roic, roe_yearly, roa2_yearly, roe_avg, opincome_of_ebt, investincome_of_ebt, n_op_profit_of_ebt, tax_to_ebt, dtprofit_to_profit, salescash_to_or, ocf_to_or, ocf_to_opincome, capitalized_to_da, debt_to_assets, assets_to_eqt, dp_assets_to_eqt, ca_to_assets, nca_to_assets, tbassets_to_totalassets, int_to_talcap, eqt_to_talcapital, currentdebt_to_debt, longdeb_to_debt, ocf_to_shortdebt, debt_to_eqt, eqt_to_debt, eqt_to_interestdebt, tangibleasset_to_debt, tangasset_to_intdebt, tangibleasset_to_netdebt, ocf_to_debt, ocf_to_interestdebt, ocf_to_netdebt, ebit_to_interest, longdebt_to_workingcapital, ebitda_to_debt, turn_days, roa_yearly, roa_dp, fixed_assets, profit_prefin_exp, non_op_profit, op_to_ebt, nop_to_ebt, ocf_to_profit, cash_to_liqdebt, cash_to_liqdebt_withinterest, op_to_liqdebt, op_to_debt, roic_yearly, total_fa_trun, profit_to_op, q_opincome, q_investincome, q_dtprofit, q_eps, q_netprofit_margin, q_gsprofit_margin, q_exp_to_sales, q_profit_to_gr, q_saleexp_to_gr, q_adminexp_to_gr, q_finaexp_to_gr, q_impair_to_gr_ttm, q_gc_to_gr, q_op_to_gr, q_roe, q_dt_roe, q_npta, q_opincome_to_ebt, q_investincome_to_ebt, q_dtprofit_to_profit, q_salescash_to_or, q_ocf_to_sales, q_ocf_to_or, basic_eps_yoy, dt_eps_yoy, cfps_yoy, op_yoy, ebt_yoy, netprofit_yoy, dt_netprofit_yoy, ocf_yoy, roe_yoy, bps_yoy, assets_yoy, eqt_yoy, tr_yoy, or_yoy, q_gr_yoy, q_gr_qoq, q_sales_yoy, q_sales_qoq, q_op_yoy, q_op_qoq, q_profit_yoy, q_profit_qoq, q_netprofit_yoy, q_netprofit_qoq, equity_yoy, rd_exp, update_flag, updated_at"

        placeholders = ', '.join(['?'] * 167) + ', NOW()'

        update_fields = "eps = excluded.eps, dt_eps = excluded.dt_eps, total_revenue_ps = excluded.total_revenue_ps, revenue_ps = excluded.revenue_ps, capital_rese_ps = excluded.capital_rese_ps, surplus_rese_ps = excluded.surplus_rese_ps, undist_profit_ps = excluded.undist_profit_ps, extra_item = excluded.extra_item, profit_dedt = excluded.profit_dedt, gross_margin = excluded.gross_margin, current_ratio = excluded.current_ratio, quick_ratio = excluded.quick_ratio, cash_ratio = excluded.cash_ratio, invturn_days = excluded.invturn_days, arturn_days = excluded.arturn_days, inv_turn = excluded.inv_turn, ar_turn = excluded.ar_turn, ca_turn = excluded.ca_turn, fa_turn = excluded.fa_turn, assets_turn = excluded.assets_turn, op_income = excluded.op_income, valuechange_income = excluded.valuechange_income, interst_income = excluded.interst_income, daa = excluded.daa, ebit = excluded.ebit, ebitda = excluded.ebitda, fcff = excluded.fcff, fcfe = excluded.fcfe, current_exint = excluded.current_exint, noncurrent_exint = excluded.noncurrent_exint, interestdebt = excluded.interestdebt, netdebt = excluded.netdebt, tangible_asset = excluded.tangible_asset, working_capital = excluded.working_capital, networking_capital = excluded.networking_capital, invest_capital = excluded.invest_capital, retained_earnings = excluded.retained_earnings, diluted2_eps = excluded.diluted2_eps, bps = excluded.bps, ocfps = excluded.ocfps, retainedps = excluded.retainedps, cfps = excluded.cfps, ebit_ps = excluded.ebit_ps, fcff_ps = excluded.fcff_ps, fcfe_ps = excluded.fcfe_ps, netprofit_margin = excluded.netprofit_margin, grossprofit_margin = excluded.grossprofit_margin, cogs_of_sales = excluded.cogs_of_sales, expense_of_sales = excluded.expense_of_sales, profit_to_gr = excluded.profit_to_gr, saleexp_to_gr = excluded.saleexp_to_gr, adminexp_of_gr = excluded.adminexp_of_gr, finaexp_of_gr = excluded.finaexp_of_gr, impai_ttm = excluded.impai_ttm, gc_of_gr = excluded.gc_of_gr, op_of_gr = excluded.op_of_gr, ebit_of_gr = excluded.ebit_of_gr, roe = excluded.roe, roe_waa = excluded.roe_waa, roe_dt = excluded.roe_dt, roa = excluded.roa, npta = excluded.npta, roic = excluded.roic, roe_yearly = excluded.roe_yearly, roa2_yearly = excluded.roa2_yearly, roe_avg = excluded.roe_avg, opincome_of_ebt = excluded.opincome_of_ebt, investincome_of_ebt = excluded.investincome_of_ebt, n_op_profit_of_ebt = excluded.n_op_profit_of_ebt, tax_to_ebt = excluded.tax_to_ebt, dtprofit_to_profit = excluded.dtprofit_to_profit, salescash_to_or = excluded.salescash_to_or, ocf_to_or = excluded.ocf_to_or, ocf_to_opincome = excluded.ocf_to_opincome, capitalized_to_da = excluded.capitalized_to_da, debt_to_assets = excluded.debt_to_assets, assets_to_eqt = excluded.assets_to_eqt, dp_assets_to_eqt = excluded.dp_assets_to_eqt, ca_to_assets = excluded.ca_to_assets, nca_to_assets = excluded.nca_to_assets, tbassets_to_totalassets = excluded.tbassets_to_totalassets, int_to_talcap = excluded.int_to_talcap, eqt_to_talcapital = excluded.eqt_to_talcapital, currentdebt_to_debt = excluded.currentdebt_to_debt, longdeb_to_debt = excluded.longdeb_to_debt, ocf_to_shortdebt = excluded.ocf_to_shortdebt, debt_to_eqt = excluded.debt_to_eqt, eqt_to_debt = excluded.eqt_to_debt, eqt_to_interestdebt = excluded.eqt_to_interestdebt, tangibleasset_to_debt = excluded.tangibleasset_to_debt, tangasset_to_intdebt = excluded.tangasset_to_intdebt, tangibleasset_to_netdebt = excluded.tangibleasset_to_netdebt, ocf_to_debt = excluded.ocf_to_debt, ocf_to_interestdebt = excluded.ocf_to_interestdebt, ocf_to_netdebt = excluded.ocf_to_netdebt, ebit_to_interest = excluded.ebit_to_interest, longdebt_to_workingcapital = excluded.longdebt_to_workingcapital, ebitda_to_debt = excluded.ebitda_to_debt, turn_days = excluded.turn_days, roa_yearly = excluded.roa_yearly, roa_dp = excluded.roa_dp, fixed_assets = excluded.fixed_assets, profit_prefin_exp = excluded.profit_prefin_exp, non_op_profit = excluded.non_op_profit, op_to_ebt = excluded.op_to_ebt, nop_to_ebt = excluded.nop_to_ebt, ocf_to_profit = excluded.ocf_to_profit, cash_to_liqdebt = excluded.cash_to_liqdebt, cash_to_liqdebt_withinterest = excluded.cash_to_liqdebt_withinterest, op_to_liqdebt = excluded.op_to_liqdebt, op_to_debt = excluded.op_to_debt, roic_yearly = excluded.roic_yearly, total_fa_trun = excluded.total_fa_trun, profit_to_op = excluded.profit_to_op, q_opincome = excluded.q_opincome, q_investincome = excluded.q_investincome, q_dtprofit = excluded.q_dtprofit, q_eps = excluded.q_eps, q_netprofit_margin = excluded.q_netprofit_margin, q_gsprofit_margin = excluded.q_gsprofit_margin, q_exp_to_sales = excluded.q_exp_to_sales, q_profit_to_gr = excluded.q_profit_to_gr, q_saleexp_to_gr = excluded.q_saleexp_to_gr, q_adminexp_to_gr = excluded.q_adminexp_to_gr, q_finaexp_to_gr = excluded.q_finaexp_to_gr, q_impair_to_gr_ttm = excluded.q_impair_to_gr_ttm, q_gc_to_gr = excluded.q_gc_to_gr, q_op_to_gr = excluded.q_op_to_gr, q_roe = excluded.q_roe, q_dt_roe = excluded.q_dt_roe, q_npta = excluded.q_npta, q_opincome_to_ebt = excluded.q_opincome_to_ebt, q_investincome_to_ebt = excluded.q_investincome_to_ebt, q_dtprofit_to_profit = excluded.q_dtprofit_to_profit, q_salescash_to_or = excluded.q_salescash_to_or, q_ocf_to_sales = excluded.q_ocf_to_sales, q_ocf_to_or = excluded.q_ocf_to_or, basic_eps_yoy = excluded.basic_eps_yoy, dt_eps_yoy = excluded.dt_eps_yoy, cfps_yoy = excluded.cfps_yoy, op_yoy = excluded.op_yoy, ebt_yoy = excluded.ebt_yoy, netprofit_yoy = excluded.netprofit_yoy, dt_netprofit_yoy = excluded.dt_netprofit_yoy, ocf_yoy = excluded.ocf_yoy, roe_yoy = excluded.roe_yoy, bps_yoy = excluded.bps_yoy, assets_yoy = excluded.assets_yoy, eqt_yoy = excluded.eqt_yoy, tr_yoy = excluded.tr_yoy, or_yoy = excluded.or_yoy, q_gr_yoy = excluded.q_gr_yoy, q_gr_qoq = excluded.q_gr_qoq, q_sales_yoy = excluded.q_sales_yoy, q_sales_qoq = excluded.q_sales_qoq, q_op_yoy = excluded.q_op_yoy, q_op_qoq = excluded.q_op_qoq, q_profit_yoy = excluded.q_profit_yoy, q_profit_qoq = excluded.q_profit_qoq, q_netprofit_yoy = excluded.q_netprofit_yoy, q_netprofit_qoq = excluded.q_netprofit_qoq, equity_yoy = excluded.equity_yoy, rd_exp = excluded.rd_exp, update_flag = excluded.update_flag, updated_at = NOW()"

        return f"""
            INSERT INTO fina_indicator (ts_code, ann_date, end_date, eps, dt_eps, total_revenue_ps, revenue_ps, capital_rese_ps, surplus_rese_ps, undist_profit_ps, extra_item, profit_dedt, gross_margin, current_ratio, quick_ratio, cash_ratio, invturn_days, arturn_days, inv_turn, ar_turn, ca_turn, fa_turn, assets_turn, op_income, valuechange_income, interst_income, daa, ebit, ebitda, fcff, fcfe, current_exint, noncurrent_exint, interestdebt, netdebt, tangible_asset, working_capital, networking_capital, invest_capital, retained_earnings, diluted2_eps, bps, ocfps, retainedps, cfps, ebit_ps, fcff_ps, fcfe_ps, netprofit_margin, grossprofit_margin, cogs_of_sales, expense_of_sales, profit_to_gr, saleexp_to_gr, adminexp_of_gr, finaexp_of_gr, impai_ttm, gc_of_gr, op_of_gr, ebit_of_gr, roe, roe_waa, roe_dt, roa, npta, roic, roe_yearly, roa2_yearly, roe_avg, opincome_of_ebt, investincome_of_ebt, n_op_profit_of_ebt, tax_to_ebt, dtprofit_to_profit, salescash_to_or, ocf_to_or, ocf_to_opincome, capitalized_to_da, debt_to_assets, assets_to_eqt, dp_assets_to_eqt, ca_to_assets, nca_to_assets, tbassets_to_totalassets, int_to_talcap, eqt_to_talcapital, currentdebt_to_debt, longdeb_to_debt, ocf_to_shortdebt, debt_to_eqt, eqt_to_debt, eqt_to_interestdebt, tangibleasset_to_debt, tangasset_to_intdebt, tangibleasset_to_netdebt, ocf_to_debt, ocf_to_interestdebt, ocf_to_netdebt, ebit_to_interest, longdebt_to_workingcapital, ebitda_to_debt, turn_days, roa_yearly, roa_dp, fixed_assets, profit_prefin_exp, non_op_profit, op_to_ebt, nop_to_ebt, ocf_to_profit, cash_to_liqdebt, cash_to_liqdebt_withinterest, op_to_liqdebt, op_to_debt, roic_yearly, total_fa_trun, profit_to_op, q_opincome, q_investincome, q_dtprofit, q_eps, q_netprofit_margin, q_gsprofit_margin, q_exp_to_sales, q_profit_to_gr, q_saleexp_to_gr, q_adminexp_to_gr, q_finaexp_to_gr, q_impair_to_gr_ttm, q_gc_to_gr, q_op_to_gr, q_roe, q_dt_roe, q_npta, q_opincome_to_ebt, q_investincome_to_ebt, q_dtprofit_to_profit, q_salescash_to_or, q_ocf_to_sales, q_ocf_to_or, basic_eps_yoy, dt_eps_yoy, cfps_yoy, op_yoy, ebt_yoy, netprofit_yoy, dt_netprofit_yoy, ocf_yoy, roe_yoy, bps_yoy, assets_yoy, eqt_yoy, tr_yoy, or_yoy, q_gr_yoy, q_gr_qoq, q_sales_yoy, q_sales_qoq, q_op_yoy, q_op_qoq, q_profit_yoy, q_profit_qoq, q_netprofit_yoy, q_netprofit_qoq, equity_yoy, rd_exp, update_flag, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, end_date)
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