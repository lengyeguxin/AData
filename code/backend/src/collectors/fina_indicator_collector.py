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
        提取字段值（严格按照p2_schema.sql定义）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组
        """
        return (
            item.get('ts_code'),        # ts_code
            convert_date_format(item.get('ann_date')),  # ann_date
            convert_date_format(item.get('end_date')),  # end_date
            # 核心财务指标（简化，实际字段很多，需根据p2_schema.sql完整定义）
            item.get('roe'),            # roe
            item.get('roa'),            # roa
            item.get('netprofit_margin'), # netprofit_margin
            item.get('grossprofit_margin'), # grossprofit_margin
            item.get('debt_to_assets'), # debt_to_assets
            item.get('current_ratio'),  # current_ratio
            item.get('quick_ratio'),    # quick_ratio
            item.get('ocfps'),          # ocfps
            item.get('bps'),            # bps
            item.get('eps'),            # eps
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO fina_indicator (
                ts_code, ann_date, end_date,
                roe, roa, netprofit_margin, grossprofit_margin,
                debt_to_assets, current_ratio, quick_ratio,
                ocfps, bps, eps,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code, end_date)
            DO UPDATE SET
                ann_date = excluded.ann_date,
                roe = excluded.roe,
                roa = excluded.roa,
                netprofit_margin = excluded.netprofit_margin,
                grossprofit_margin = excluded.grossprofit_margin,
                debt_to_assets = excluded.debt_to_assets,
                current_ratio = excluded.current_ratio,
                quick_ratio = excluded.quick_ratio,
                ocfps = excluded.ocfps,
                bps = excluded.bps,
                eps = excluded.eps,
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