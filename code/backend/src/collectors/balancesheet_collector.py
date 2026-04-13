"""
BalancesheetCollector - 资产负债表拉取器（VIP接口）

严格按照CSV文档：
- 接口名称：balancesheet_vip（VIP接口）
- 接口参数：ann_date={游标+1}、report_type=1
- 文档地址：https://tushare.pro/document/2?doc_id=36
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

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化BalancesheetCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
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
        提取字段值（严格按照p2_schema.sql定义，完整49个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（49个字段，严格按照schema定义顺序）
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

            # 流动资产（17个）
            item.get('total_cur_assets'),
            item.get('money_cap'),
            item.get('trad_asset'),
            item.get('notes_receiv'),
            item.get('accounts_receiv'),
            item.get('adv_payment'),
            item.get('other_receiv'),
            item.get('inventories'),
            item.get('amor_exp'),
            item.get('long_ampay_dep_rec_asim'),
            item.get('total_nca'),
            item.get('fix_assets'),
            item.get('cip'),
            item.get('const_materials'),
            item.get('intang_assets'),
            item.get('goodwill'),
            item.get('long_deferred_exp'),

            # 非流动资产（2个）
            item.get('defer_tax_assets'),
            item.get('total_assets'),

            # 流动负债（11个）
            item.get('total_cur_liab'),
            item.get('st_borr'),
            item.get('notes_payable'),
            item.get('accounts_pay'),
            item.get('adv_receipts'),
            item.get('payroll_pay'),
            item.get('taxes_payable'),
            item.get('interest_payable'),
            item.get('div_payable'),
            item.get('other_payable'),
            item.get('total_ncl'),

            # 非流动负债（5个）
            item.get('long_borr'),
            item.get('bonds_payable'),
            item.get('long_deferred_rev'),
            item.get('defer_tax_liab'),
            item.get('total_liab'),

            # 所有者权益（5个）
            item.get('cap_rese'),
            item.get('undistr_porfit'),
            item.get('minority_int_ratio'),
            item.get('total_hldr_eqy_exc_min_int'),
            item.get('total_hldr_eqy_inc_min_int'),

            # 合计（1个）
            item.get('total_liab_hldr_eqy'),
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整49个字段）

        Returns:
            INSERT SQL语句

        注意：
            - DuckDB不允许在ON CONFLICT中更新ann_date字段（有约束限制）
            - 主键：PRIMARY KEY (ts_code, end_date, report_type)
        """
        # 构建字段列表（49个字段 + updated_at）
        fields = """ts_code, ann_date, f_ann_date, end_date, report_type, comp_type, end_type, update_flag,
            total_cur_assets, money_cap, trad_asset, notes_receiv, accounts_receiv, adv_payment, other_receiv,
            inventories, amor_exp, long_ampay_dep_rec_asim, total_nca, fix_assets, cip, const_materials,
            intang_assets, goodwill, long_deferred_exp, defer_tax_assets, total_assets,
            total_cur_liab, st_borr, notes_payable, accounts_pay, adv_receipts, payroll_pay, taxes_payable,
            interest_payable, div_payable, other_payable, total_ncl,
            long_borr, bonds_payable, long_deferred_rev, defer_tax_liab, total_liab,
            cap_rese, undistr_porfit, minority_int_ratio, total_hldr_eqy_exc_min_int, total_hldr_eqy_inc_min_int,
            total_liab_hldr_eqy, updated_at"""

        # 构建VALUES占位符（49个 ? + NOW()）
        placeholders = ', '.join(['?'] * 49) + ', NOW()'

        # 构建DO UPDATE SET语句（排除主键字段ts_code、end_date、report_type，排除ann_date）
        update_fields = """f_ann_date = excluded.f_ann_date,
            comp_type = excluded.comp_type,
            end_type = excluded.end_type,
            update_flag = excluded.update_flag,
            total_cur_assets = excluded.total_cur_assets, money_cap = excluded.money_cap,
            trad_asset = excluded.trad_asset, notes_receiv = excluded.notes_receiv,
            accounts_receiv = excluded.accounts_receiv, adv_payment = excluded.adv_payment,
            other_receiv = excluded.other_receiv, inventories = excluded.inventories,
            amor_exp = excluded.amor_exp, long_ampay_dep_rec_asim = excluded.long_ampay_dep_rec_asim,
            total_nca = excluded.total_nca, fix_assets = excluded.fix_assets, cip = excluded.cip,
            const_materials = excluded.const_materials, intang_assets = excluded.intang_assets,
            goodwill = excluded.goodwill, long_deferred_exp = excluded.long_deferred_exp,
            defer_tax_assets = excluded.defer_tax_assets, total_assets = excluded.total_assets,
            total_cur_liab = excluded.total_cur_liab, st_borr = excluded.st_borr,
            notes_payable = excluded.notes_payable, accounts_pay = excluded.accounts_pay,
            adv_receipts = excluded.adv_receipts, payroll_pay = excluded.payroll_pay,
            taxes_payable = excluded.taxes_payable, interest_payable = excluded.interest_payable,
            div_payable = excluded.div_payable, other_payable = excluded.other_payable,
            total_ncl = excluded.total_ncl,
            long_borr = excluded.long_borr, bonds_payable = excluded.bonds_payable,
            long_deferred_rev = excluded.long_deferred_rev, defer_tax_liab = excluded.defer_tax_liab,
            total_liab = excluded.total_liab,
            cap_rese = excluded.cap_rese, undistr_porfit = excluded.undistr_porfit,
            minority_int_ratio = excluded.minority_int_ratio,
            total_hldr_eqy_exc_min_int = excluded.total_hldr_eqy_exc_min_int,
            total_hldr_eqy_inc_min_int = excluded.total_hldr_eqy_inc_min_int,
            total_liab_hldr_eqy = excluded.total_liab_hldr_eqy,
            updated_at = NOW()"""

        return f"""
            INSERT INTO balancesheet ({fields})
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