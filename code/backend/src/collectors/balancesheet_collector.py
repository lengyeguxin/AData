"""
BalancesheetCollector - 资产负债表拉取器

严格按照CSV文档：
- 接口名称：balancesheet_vip（VIP接口）
- 接口参数：ann_date={游标+1}, report_type=1
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
            - report_type=1（合并报表）
            - ann_date可能无数据（正常情况，财务数据公告不规律）
        """
        self.logger.info(f"拉取资产负债表（VIP接口）: ann_date={ann_date}")

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
            字段值元组（简化版本，实际字段很多）
        """
        return (
            item.get('ts_code'),        # ts_code
            convert_date_format(item.get('ann_date')),  # ann_date
            convert_date_format(item.get('f_ann_date')),  # f_ann_date
            convert_date_format(item.get('end_date')),  # end_date
            item.get('report_type'),    # report_type
            item.get('comp_type'),      # comp_type
            # 资产项
            item.get('total_assets'),   # total_assets
            item.get('total_liab'),     # total_liab
            item.get('total_equity'),   # total_equity
            item.get('total_share'),    # total_share
            # 流动资产
            item.get('money_cap'),      # money_cap
            item.get('trad_asset'),     # trad_asset
            item.get('notes_receiv'),   # notes_receiv
            item.get('accounts_receiv'), # accounts_receiv
            # 流动负债
            item.get('total_cur_liab'), # total_cur_liab
            item.get('long_liab'),      # long_liab
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO balancesheet (
                ts_code, ann_date, f_ann_date, end_date, report_type, comp_type,
                total_assets, total_liab, total_equity, total_share,
                money_cap, trad_asset, notes_receiv, accounts_receiv,
                total_cur_liab, long_liab,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code, end_date, report_type)
            DO UPDATE SET
                ann_date = excluded.ann_date,
                f_ann_date = excluded.f_ann_date,
                comp_type = excluded.comp_type,
                total_assets = excluded.total_assets,
                total_liab = excluded.total_liab,
                total_equity = excluded.total_equity,
                total_share = excluded.total_share,
                money_cap = excluded.money_cap,
                trad_asset = excluded.trad_asset,
                notes_receiv = excluded.notes_receiv,
                accounts_receiv = excluded.accounts_receiv,
                total_cur_liab = excluded.total_cur_liab,
                long_liab = excluded.long_liab,
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