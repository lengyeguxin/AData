"""
IncomeCollector - 利润表拉取器

严格按照CSV文档：
- 接口名称：income_vip（VIP接口）
- 接口参数：ann_date={游标+1}, report_type=1
- 文档地址：https://tushare.pro/document/2?doc_id=33
- 游标策略：daily_natural（按自然日记录）
- VIP接口特性：更丰富字段、更快更新速度
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List, Tuple
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class IncomeCollector(BaseCollector):
    """利润表拉取器（P2财务表，VIP接口，按自然日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化IncomeCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
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
            - report_type=1（合并报表）
            - ann_date可能无数据（正常情况，财务数据公告不规律）
        """
        self.logger.info(f"拉取利润表（VIP接口）: ann_date={ann_date}")

        # 严格按照CSV文档参数
        data = self.collect(
            ann_date=ann_date,
            report_type='1'  # 合并报表（CSV文档明确要求）
        )

        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照p2_schema.sql定义）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（37个字段）
        """
        return (
            item.get('ts_code'),        # ts_code
            convert_date_format(item.get('ann_date')),  # ann_date
            convert_date_format(item.get('f_ann_date')),  # f_ann_date
            convert_date_format(item.get('end_date')),  # end_date
            item.get('report_type'),    # report_type
            item.get('comp_type'),      # comp_type
            # 营业收入与成本
            item.get('total_revenue'),  # total_revenue
            item.get('revenue'),        # revenue
            item.get('operate_profit'), # operate_profit
            item.get('total_cogs'),     # total_cogs
            item.get('interest_income'), # interest_income
            # 利润指标
            item.get('profit_dedt'),    # profit_dedt
            item.get('sell_exp'),       # sell_exp
            item.get('admin_exp'),      # admin_exp
            item.get('fin_exp'),        # fin_exp
            item.get('asset_impair_loss'), # asset_impair_loss
            item.get('non_oper_income'), # non_oper_income
            item.get('non_oper_exp'),   # non_oper_exp
            item.get('total_profit'),   # total_profit
            item.get('income_tax'),     # income_tax
            item.get('n_income'),       # n_income
            item.get('n_income_attr_p'), # n_income_attr_p
            item.get('minority_gain'),  # minority_gain
            # 每股指标
            item.get('basic_eps'),      # basic_eps
            item.get('diluted_eps'),    # diluted_eps
            # 其他综合收益
            item.get('oth_compr_income'), # oth_compr_income
            item.get('t_compr_income'), # t_compr_income
            item.get('compr_inc_attr_p'), # compr_inc_attr_p
            item.get('compr_inc_attr_m_s'), # compr_inc_attr_m_s
            # 现金流相关
            item.get('ebit'),           # ebit
            item.get('ebitda'),         # ebitda
            item.get('rd_exp'),         # rd_exp
            item.get('fin_exp_int_exp'), # fin_exp_int_exp
            item.get('fin_exp_int_income'), # fin_exp_int_income
            item.get('transfer_surplus_reserve'), # transfer_surplus_reserve
            item.get('transfer_risk_reserve'), # transfer_risk_reserve
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO income (
                ts_code, ann_date, f_ann_date, end_date, report_type, comp_type,
                total_revenue, revenue, operate_profit, total_cogs, interest_income,
                profit_dedt, sell_exp, admin_exp, fin_exp, asset_impair_loss,
                non_oper_income, non_oper_exp, total_profit, income_tax,
                n_income, n_income_attr_p, minority_gain,
                basic_eps, diluted_eps,
                oth_compr_income, t_compr_income, compr_inc_attr_p, compr_inc_attr_m_s,
                ebit, ebitda, rd_exp, fin_exp_int_exp, fin_exp_int_income,
                transfer_surplus_reserve, transfer_risk_reserve,
                updated_at
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW()
            )
            ON CONFLICT (ts_code, end_date, report_type)
            DO UPDATE SET
                ann_date = excluded.ann_date,
                f_ann_date = excluded.f_ann_date,
                comp_type = excluded.comp_type,
                total_revenue = excluded.total_revenue,
                revenue = excluded.revenue,
                operate_profit = excluded.operate_profit,
                total_cogs = excluded.total_cogs,
                interest_income = excluded.interest_income,
                profit_dedt = excluded.profit_dedt,
                sell_exp = excluded.sell_exp,
                admin_exp = excluded.admin_exp,
                fin_exp = excluded.fin_exp,
                asset_impair_loss = excluded.asset_impair_loss,
                non_oper_income = excluded.non_oper_income,
                non_oper_exp = excluded.non_oper_exp,
                total_profit = excluded.total_profit,
                income_tax = excluded.income_tax,
                n_income = excluded.n_income,
                n_income_attr_p = excluded.n_income_attr_p,
                minority_gain = excluded.minority_gain,
                basic_eps = excluded.basic_eps,
                diluted_eps = excluded.diluted_eps,
                oth_compr_income = excluded.oth_compr_income,
                t_compr_income = excluded.t_compr_income,
                compr_inc_attr_p = excluded.compr_inc_attr_p,
                compr_inc_attr_m_s = excluded.compr_inc_attr_m_s,
                ebit = excluded.ebit,
                ebitda = excluded.ebitda,
                rd_exp = excluded.rd_exp,
                fin_exp_int_exp = excluded.fin_exp_int_exp,
                fin_exp_int_income = excluded.fin_exp_int_income,
                transfer_surplus_reserve = excluded.transfer_surplus_reserve,
                transfer_risk_reserve = excluded.transfer_risk_reserve,
                updated_at = NOW()
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