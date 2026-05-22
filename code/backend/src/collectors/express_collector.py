"""
ExpressCollector - 业绩预告拉取器（VIP接口）

严格按照CSV文档：
- 接口名称：forecast_vip（VIP接口）
- 接口参数：ann_date={游标+1}、report_type=1
- 文档地址：https://tushare.pro/document/2%sdoc_id=45
- 游标策略：daily_natural（按自然日记录）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class ExpressCollector(BaseCollector):
    """业绩预告拉取器（P2财务表，VIP接口）"""

    def __init__(self, db_config: dict, api: TushareAPI):
        super().__init__(
            db_config=db_config, api=api, table_name='express',
            api_name='forecast_vip', date_field='ann_date', vip_interface=True
        )

    def collect_by_date(self, ann_date: str) -> List[Dict]:
        """
        按公告日期拉取数据

        Args:
            ann_date: 公告日期（YYYYMMDD格式）

        Returns:
            数据列表
        """
        self.logger.info(f"拉取业绩预告: ann_date={ann_date}")
        return self.collect(ann_date=ann_date)

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照express_schema.sql定义，完整12个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（12个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('ann_date')),
            convert_date_format(item.get('end_date')),
            item.get('type'),
            item.get('p_change_min'),
            item.get('p_change_max'),
            item.get('net_profit_min'),
            item.get('net_profit_max'),
            item.get('last_parent_net'),
            convert_date_format(item.get('first_ann_date')),
            item.get('summary'),
            item.get('change_reason'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整12个字段）

        Returns:
            INSERT SQL语句

        注意：
            - DuckDB不允许在ON CONFLICT中更新ann_date字段（有约束限制）
            - 主键：PRIMARY KEY (ts_code, end_date, ann_date)
        """
        fields = "ts_code, ann_date, end_date, type, p_change_min, p_change_max, net_profit_min, net_profit_max, last_parent_net, first_ann_date, summary, change_reason, updated_at"

        placeholders = ', '.join(['%s'] * 12) + ', NOW()'

        update_fields = "type = excluded.type, p_change_min = excluded.p_change_min, p_change_max = excluded.p_change_max, net_profit_min = excluded.net_profit_min, net_profit_max = excluded.net_profit_max, last_parent_net = excluded.last_parent_net, first_ann_date = excluded.first_ann_date, summary = excluded.summary, change_reason = excluded.change_reason, updated_at = NOW()"

        return f"""
            INSERT INTO express (ts_code, ann_date, end_date, type, p_change_min, p_change_max, net_profit_min, net_profit_max, last_parent_net, first_ann_date, summary, change_reason, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, end_date, ann_date)
            DO UPDATE SET {update_fields}
        """


