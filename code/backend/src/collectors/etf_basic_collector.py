"""
ETFBasicCollector - ETF基本信息拉取器

严格按照CSV文档：
- 接口名称：etf_basic（不是fund_basic）
- 接口参数：无参数
- 文档地址：https://tushare.pro/document/2?doc_id=385
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
            api_name='etf_basic',  # 严格按照CSV文档（修正：不是fund_basic）
            date_field=None,  # 无日期字段
            vip_interface=False  # 标准接口
        )

    def collect_all(self) -> List[Dict]:
        """
        拉取所有ETF基本信息（无参数）

        Returns:
            ETF基本信息列表

        注意：
            - 无参数（全量拉取）
            - 按月更新策略
        """
        self.logger.info("拉取ETF基本信息: 无参数")

        data = self.collect()

        self.logger.info(f"拉取完成: 共{len(data)}条ETF数据")
        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照p0_schema.sql定义，完整17个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（17个字段）
        """
        return (
            # 基础字段
            item.get('ts_code'),
            item.get('name'),
            item.get('fullname'),
            item.get('fund_type'),
            item.get('fund_manager'),

            # 日期字段
            convert_date_format(item.get('list_date')),
            convert_date_format(item.get('issue_date')),
            convert_date_format(item.get('delist_date')),

            # 数值字段
            item.get('issue_amount'),
            item.get('m_fee'),
            item.get('c_fee'),

            # 文本字段
            item.get('benchmark'),
            item.get('status'),
            item.get('invest_type'),
            item.get('type'),
            item.get('trustee'),
            item.get('perf_benchmark'),
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整17个字段）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO etf_basic (
                ts_code, name, fullname, fund_type, fund_manager,
                list_date, issue_date, delist_date, issue_amount,
                m_fee, c_fee, benchmark, status, invest_type, type, trustee, perf_benchmark,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code)
            DO UPDATE SET
                name = excluded.name,
                fullname = excluded.fullname,
                fund_type = excluded.fund_type,
                fund_manager = excluded.fund_manager,
                list_date = excluded.list_date,
                issue_date = excluded.issue_date,
                delist_date = excluded.delist_date,
                issue_amount = excluded.issue_amount,
                m_fee = excluded.m_fee,
                c_fee = excluded.c_fee,
                benchmark = excluded.benchmark,
                status = excluded.status,
                invest_type = excluded.invest_type,
                type = excluded.type,
                trustee = excluded.trustee,
                perf_benchmark = excluded.perf_benchmark,
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