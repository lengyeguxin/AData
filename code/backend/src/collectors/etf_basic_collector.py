"""
ETFBasicCollector - ETF基本信息拉取器

严格按照CSV文档：
- 接口名称：fund_basic
- 接口参数：market=E（ETF市场）
- 文档地址：https://tushare.pro/document/2?doc_id=114
- 游标策略：none（无游标，全量拉取）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class ETFBasicCollector(BaseCollector):
    """ETF基本信息拉取器（P0前置表，全量拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化ETFBasicCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='etf_basic',
            api_name='fund_basic',  # 严格按照CSV文档
            date_field=None,  # 无日期字段
            vip_interface=False  # 标准接口
        )

    def collect_all(self) -> List[Dict]:
        """
        拉取所有ETF基本信息（market=E）

        Returns:
            ETF基本信息列表

        注意：
            - market='E'（ETF市场）
            - 全量拉取（无参数限制）
        """
        self.logger.info(f"拉取ETF基本信息: market=E")

        data = self.collect(market='E')

        self.logger.info(f"拉取完成: 共{len(data)}条ETF数据")
        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照p0_schema.sql定义）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组
        """
        return (
            item.get('ts_code'),        # ts_code
            item.get('name'),           # name
            item.get('fund_type'),      # fund_type
            item.get('fund_setup_date'), # fund_setup_date
            item.get('list_date'),      # list_date
            item.get('issue_date'),     # issue_date
            item.get('issue_amount'),   # issue_amount
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO etf_basic (
                ts_code, name, fund_type, fund_setup_date, list_date,
                issue_date, issue_amount, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code)
            DO UPDATE SET
                name = excluded.name,
                fund_type = excluded.fund_type,
                fund_setup_date = excluded.fund_setup_date,
                list_date = excluded.list_date,
                issue_date = excluded.issue_date,
                issue_amount = excluded.issue_amount,
                updated_at = NOW()
        """

    def run(self) -> int:
        """
        拉取并保存所有ETF基本信息

        Returns:
            保存的记录数
        """
        data = self.collect_all()
        return self.save(data)