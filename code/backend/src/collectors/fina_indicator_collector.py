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
        提取字段值（严格按照p2_schema.sql定义，完整99个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（99个字段，严格按照schema定义顺序）
        """
        # 基础字段（3个）
        values = [
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('end_date')),
        ]

        # 每股指标（15个）
        values.extend([
            item.get('eps'),                    # 每股收益
            item.get('dt_eps'),                 # 每股收益(扣非)
            item.get('total_revenue_ps'),       # 每股营业总收入
            item.get('revenue_ps'),             # 每股营业收入
            item.get('capital_rese_ps'),        # 每股资本公积
            item.get('surplus_rese_ps'),        # 每股盈余公积
            item.get('undist_profit_ps'),       # 每股未分配利润
            item.get('diluted2_eps'),           # 每股收益(稀释2)
            item.get('bps'),                    # 每股净资产
            item.get('ocfps'),                  # 每股经营现金流
            item.get('retainedps'),             # 每股留存收益
            item.get('cfps'),                   # 每股现金流
            item.get('ebit_ps'),                # 每股EBIT
            item.get('fcff_ps'),                # 每股企业自由现金流
            item.get('fcfe_ps'),                # 每股股东自由现金流
        ])

        # 盈利能力指标（12个）
        values.extend([
            item.get('roe'),                    # 净资产收益率
            item.get('roe_waa'),                # 加权平均净资产收益率
            item.get('roe_dt'),                 # 净资产收益率(扣非)
            item.get('roa'),                    # 总资产报酬率
            item.get('npta'),                   # 总资产净利润
            item.get('roic'),                   # 投入资本回报率
            item.get('roe_yearly'),             # 净资产收益率(年化)
            item.get('roa2_yearly'),            # 总资产报酬率2(年化)
            item.get('roe_avg'),                # 平均净资产收益率
            item.get('roa_yearly'),             # 总资产净利润(年化)
            item.get('roa_dp'),                 # 总资产净利润(双季)
            item.get('roic_yearly'),            # 投入资本回报率(年化)
        ])

        # 营运能力指标（9个）
        values.extend([
            item.get('invturn_days'),           # 存货周转天数
            item.get('arturn_days'),            # 应收账款周转天数
            item.get('inv_turn'),               # 存货周转率
            item.get('ar_turn'),                # 应收账款周转率
            item.get('ca_turn'),                # 流动资产周转率
            item.get('fa_turn'),                # 固定资产周转率
            item.get('assets_turn'),            # 总资产周转率
            item.get('turn_days'),              # 营业周期
            item.get('total_fa_trun'),          # 固定资产周转率(TTM)
        ])

        # 偿债能力指标（8个）
        values.extend([
            item.get('current_ratio'),          # 流动比率
            item.get('quick_ratio'),            # 速动比率
            item.get('cash_ratio'),             # 现金比率
            item.get('debt_to_assets'),         # 资产负债率
            item.get('assets_to_eqt'),          # 权益乘数
            item.get('dp_assets_to_eqt'),       # 权益乘数(双季)
            item.get('debt_to_eqt'),            # 产权比率
            item.get('eqt_to_debt'),            # 产权比率倒数
        ])

        # 现金流指标（6个）
        values.extend([
            item.get('fcff'),                   # 企业自由现金流
            item.get('fcfe'),                   # 股东自由现金流
            item.get('ocf_to_debt'),            # 现金债务覆盖率
            item.get('ocf_to_interestdebt'),    # 现金利息债务覆盖率
            item.get('ocf_to_netdebt'),         # 现金净债务覆盖率
            item.get('ocf_to_shortdebt'),       # 现金短期债务覆盖率
        ])

        # 其他重要指标（12个）
        values.extend([
            item.get('gross_margin'),           # 毛利率
            item.get('ebit'),                   # 息税前利润
            item.get('ebitda'),                 # 息税折旧摊销前利润
            item.get('profit_dedt'),            # 扣除非经常损益后的净利润
            item.get('working_capital'),        # 营运资本
            item.get('networking_capital'),     # 净营运资本
            item.get('invest_capital'),         # 投入资本
            item.get('retained_earnings'),      # 留存收益
            item.get('tangible_asset'),         # 有形资产
            item.get('interestdebt'),           # 利息债务
            item.get('netdebt'),                # 净债务
            item.get('fixed_assets'),           # 固定资产
        ])

        # 同比增长指标（15个）
        values.extend([
            item.get('basic_eps_yoy'),          # 基本每股收益同比增长
            item.get('dt_eps_yoy'),             # 扣非每股收益同比增长
            item.get('cfps_yoy'),               # 每股现金流同比增长
            item.get('op_yoy'),                 # 营业利润同比增长
            item.get('ebt_yoy'),                # 利润总额同比增长
            item.get('netprofit_yoy'),          # 净利润同比增长
            item.get('dt_netprofit_yoy'),       # 扣非净利润同比增长
            item.get('ocf_yoy'),                # 经营现金流同比增长
            item.get('roe_yoy'),                # 净资产收益率同比增长
            item.get('bps_yoy'),                # 每股净资产同比增长
            item.get('assets_yoy'),             # 总资产同比增长
            item.get('eqt_yoy'),                # 净资产同比增长
            item.get('tr_yoy'),                 # 营业总收入同比增长
            item.get('or_yoy'),                 # 营业收入同比增长
            item.get('equity_yoy'),             # 股东权益同比增长
        ])

        # 单季度指标（16个）
        values.extend([
            item.get('q_opincome'),             # 单季度营业利润
            item.get('q_investincome'),         # 单季度投资收益
            item.get('q_dtprofit'),             # 单季度扣非净利润
            item.get('q_eps'),                  # 单季度每股收益
            item.get('q_netprofit_margin'),     # 单季度净利润率
            item.get('q_gsprofit_margin'),      # 单季度毛利率
            item.get('q_roe'),                  # 单季度ROE
            item.get('q_dt_roe'),               # 单季度扣非ROE
            item.get('q_opprofit_margin'),      # 单季度营业利润率
            item.get('q_ebit_margin'),          # 单季度EBIT利润率
            item.get('q_ebitda_margin'),        # 单季度EBITDA利润率
            item.get('q_opincome_yoy'),         # 单季度营业利润同比增长
            item.get('q_investincome_yoy'),     # 单季度投资收益同比增长
            item.get('q_dtprofit_yoy'),         # 单季度扣非净利润同比增长
            item.get('q_eps_yoy'),              # 单季度每股收益同比增长
            item.get('q_netprofit_yoy'),        # 单季度净利润同比增长
        ])

        # 其他字段（2个）
        values.extend([
            item.get('rd_exp'),                 # 研发费用
            item.get('update_flag'),            # 更新标识
        ])

        return tuple(values)

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整99个字段）

        Returns:
            INSERT SQL语句
        """
        # 构建字段列表（98个字段 + updated_at）
        fields = """ts_code, ann_date, end_date,
            eps, dt_eps, total_revenue_ps, revenue_ps, capital_rese_ps, surplus_rese_ps, undist_profit_ps,
            diluted2_eps, bps, ocfps, retainedps, cfps, ebit_ps, fcff_ps, fcfe_ps,
            roe, roe_waa, roe_dt, roa, npta, roic, roe_yearly, roa2_yearly, roe_avg, roa_yearly, roa_dp, roic_yearly,
            invturn_days, arturn_days, inv_turn, ar_turn, ca_turn, fa_turn, assets_turn, turn_days, total_fa_trun,
            current_ratio, quick_ratio, cash_ratio, debt_to_assets, assets_to_eqt, dp_assets_to_eqt, debt_to_eqt, eqt_to_debt,
            fcff, fcfe, ocf_to_debt, ocf_to_interestdebt, ocf_to_netdebt, ocf_to_shortdebt,
            gross_margin, ebit, ebitda, profit_dedt, working_capital, networking_capital, invest_capital,
            retained_earnings, tangible_asset, interestdebt, netdebt, fixed_assets,
            basic_eps_yoy, dt_eps_yoy, cfps_yoy, op_yoy, ebt_yoy, netprofit_yoy, dt_netprofit_yoy, ocf_yoy,
            roe_yoy, bps_yoy, assets_yoy, eqt_yoy, tr_yoy, or_yoy, equity_yoy,
            q_opincome, q_investincome, q_dtprofit, q_eps, q_netprofit_margin, q_gsprofit_margin,
            q_roe, q_dt_roe, q_opprofit_margin, q_ebit_margin, q_ebitda_margin,
            q_opincome_yoy, q_investincome_yoy, q_dtprofit_yoy, q_eps_yoy, q_netprofit_yoy,
            rd_exp, update_flag, updated_at"""

        # 构建VALUES占位符（98个 ? + NOW()）
        placeholders = ', '.join(['?'] * 98) + ', NOW()'

        # 构建DO UPDATE SET语句（排除主键字段ts_code、end_date，移除ann_date）
        # 注意：DuckDB不允许在ON CONFLICT中更新ann_date字段（有约束限制）
        update_fields = """eps = excluded.eps, dt_eps = excluded.dt_eps, total_revenue_ps = excluded.total_revenue_ps,
            revenue_ps = excluded.revenue_ps, capital_rese_ps = excluded.capital_rese_ps,
            surplus_rese_ps = excluded.surplus_rese_ps, undist_profit_ps = excluded.undist_profit_ps,
            diluted2_eps = excluded.diluted2_eps, bps = excluded.bps, ocfps = excluded.ocfps,
            retainedps = excluded.retainedps, cfps = excluded.cfps, ebit_ps = excluded.ebit_ps,
            fcff_ps = excluded.fcff_ps, fcfe_ps = excluded.fcfe_ps,
            roe = excluded.roe, roe_waa = excluded.roe_waa, roe_dt = excluded.roe_dt, roa = excluded.roa,
            npta = excluded.npta, roic = excluded.roic, roe_yearly = excluded.roe_yearly,
            roa2_yearly = excluded.roa2_yearly, roe_avg = excluded.roe_avg, roa_yearly = excluded.roa_yearly,
            roa_dp = excluded.roa_dp, roic_yearly = excluded.roic_yearly,
            invturn_days = excluded.invturn_days, arturn_days = excluded.arturn_days,
            inv_turn = excluded.inv_turn, ar_turn = excluded.ar_turn, ca_turn = excluded.ca_turn,
            fa_turn = excluded.fa_turn, assets_turn = excluded.assets_turn, turn_days = excluded.turn_days,
            total_fa_trun = excluded.total_fa_trun,
            current_ratio = excluded.current_ratio, quick_ratio = excluded.quick_ratio,
            cash_ratio = excluded.cash_ratio, debt_to_assets = excluded.debt_to_assets,
            assets_to_eqt = excluded.assets_to_eqt, dp_assets_to_eqt = excluded.dp_assets_to_eqt,
            debt_to_eqt = excluded.debt_to_eqt, eqt_to_debt = excluded.eqt_to_debt,
            fcff = excluded.fcff, fcfe = excluded.fcfe, ocf_to_debt = excluded.ocf_to_debt,
            ocf_to_interestdebt = excluded.ocf_to_interestdebt, ocf_to_netdebt = excluded.ocf_to_netdebt,
            ocf_to_shortdebt = excluded.ocf_to_shortdebt,
            gross_margin = excluded.gross_margin, ebit = excluded.ebit, ebitda = excluded.ebitda,
            profit_dedt = excluded.profit_dedt, working_capital = excluded.working_capital,
            networking_capital = excluded.networking_capital, invest_capital = excluded.invest_capital,
            retained_earnings = excluded.retained_earnings, tangible_asset = excluded.tangible_asset,
            interestdebt = excluded.interestdebt, netdebt = excluded.netdebt, fixed_assets = excluded.fixed_assets,
            basic_eps_yoy = excluded.basic_eps_yoy, dt_eps_yoy = excluded.dt_eps_yoy,
            cfps_yoy = excluded.cfps_yoy, op_yoy = excluded.op_yoy, ebt_yoy = excluded.ebt_yoy,
            netprofit_yoy = excluded.netprofit_yoy, dt_netprofit_yoy = excluded.dt_netprofit_yoy,
            ocf_yoy = excluded.ocf_yoy, roe_yoy = excluded.roe_yoy, bps_yoy = excluded.bps_yoy,
            assets_yoy = excluded.assets_yoy, eqt_yoy = excluded.eqt_yoy, tr_yoy = excluded.tr_yoy,
            or_yoy = excluded.or_yoy, equity_yoy = excluded.equity_yoy,
            q_opincome = excluded.q_opincome, q_investincome = excluded.q_investincome,
            q_dtprofit = excluded.q_dtprofit, q_eps = excluded.q_eps, q_netprofit_margin = excluded.q_netprofit_margin,
            q_gsprofit_margin = excluded.q_gsprofit_margin, q_roe = excluded.q_roe, q_dt_roe = excluded.q_dt_roe,
            q_opprofit_margin = excluded.q_opprofit_margin, q_ebit_margin = excluded.q_ebit_margin,
            q_ebitda_margin = excluded.q_ebitda_margin,
            q_opincome_yoy = excluded.q_opincome_yoy, q_investincome_yoy = excluded.q_investincome_yoy,
            q_dtprofit_yoy = excluded.q_dtprofit_yoy, q_eps_yoy = excluded.q_eps_yoy,
            q_netprofit_yoy = excluded.q_netprofit_yoy,
            rd_exp = excluded.rd_exp, update_flag = excluded.update_flag, updated_at = NOW()"""

        return f"""
            INSERT INTO fina_indicator ({fields})
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