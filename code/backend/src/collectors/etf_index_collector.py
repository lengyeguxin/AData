"""
ETFIndexCollector - ETF基准指数拉取器

严格按照CSV文档：
- 接口名称：etf_index
- 接口参数：无参数
- 文档地址：https://tushare.pro/document/2?doc_id=386
- 游标策略：none（无游标，全量拉取）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class ETFIndexCollector(BaseCollector):
    """ETF基准指数拉取器（P0前置表，全量拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化ETFIndexCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='etf_index',
            api_name='etf_index',  # 实际接口名（修正）
            date_field=None,  # 无日期字段
            vip_interface=False  # 标准接口
        )

    def collect_all(self) -> List[Dict]:
        """
        拉取所有ETF基准指数信息

        Returns:
            ETF基准指数列表

        注意：
            - 全量拉取（无参数限制）
        """
        self.logger.info(f"拉取ETF基准指数信息")

        data = self.collect()

        self.logger.info(f"拉取完成: 共{len(data)}条ETF基准指数数据")
        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照表结构定义）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组
        """
        return (
            item.get('ts_code'),        # ts_code（主键）
            item.get('index_code'),     # index_code
            item.get('index_name'),     # index_name
            item.get('tracking_type'),  # tracking_type
            item.get('tracking_ratio'), # tracking_ratio
            item.get('invest_type'),    # invest_type
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        注意：
            - index_code字段有索引(idx_etf_index_index_code)，ON CONFLICT时不更新
            - ts_code是PRIMARY KEY，ON CONFLICT时也不更新

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO etf_index (
                ts_code, index_code, index_name, tracking_type, tracking_ratio, invest_type, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code)
            DO UPDATE SET
                index_name = excluded.index_name,
                tracking_type = excluded.tracking_type,
                tracking_ratio = excluded.tracking_ratio,
                invest_type = excluded.invest_type,
                updated_at = NOW()
        """

    def run(self) -> int:
        """
        拉取并保存所有ETF基准指数信息

        Returns:
            保存的记录数
        """
        data = self.collect_all()
        return self.save(data)