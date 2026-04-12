"""
IndexBasicCollector - 指数列表拉取器

严格按照CSV文档：
- 接口名称：index_basic
- 接口参数：market=SSE/SZSE（分两次拉取）
- 文档地址：https://tushare.pro/document/2?doc_id=173
- 游标策略：none（无游标，全量拉取）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class IndexBasicCollector(BaseCollector):
    """指数列表拉取器（P0前置表，全量拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化IndexBasicCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='index_basic',
            api_name='index_basic',  # 严格按照CSV文档
            date_field=None,  # 无日期字段
            vip_interface=False  # 标准接口
        )

    def collect_all(self) -> List[Dict]:
        """
        拉取所有指数列表（分市场拉取：SSE上交所 + SZSE深交所）

        Returns:
            指数列表数据

        注意：
            - 分两次拉取：market=SSE和market=SZSE
            - 全量拉取（无参数限制）
        """
        all_data = []

        # 分市场拉取（SSE上交所、SZSE深交所）
        for market in ['SSE', 'SZSE']:
            self.logger.info(f"拉取指数列表: market={market}")

            data = self.collect(market=market)
            all_data.extend(data)

        self.logger.info(f"拉取完成: 共{len(all_data)}条指数数据")
        return all_data

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
            item.get('fullname'),       # fullname
            item.get('market'),         # market
            item.get('publisher'),      # publisher
            item.get('index_type'),     # index_type
            item.get('category'),       # category
            convert_date_format(item.get('base_date')),  # base_date
            item.get('base_point'),     # base_point
            convert_date_format(item.get('list_date')),  # list_date
            item.get('weight_rule'),    # weight_rule
            item.get('description'),    # description
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO index_basic (
                ts_code, name, fullname, market, publisher, index_type, category,
                base_date, base_point, list_date, weight_rule, description, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code)
            DO UPDATE SET
                name = excluded.name,
                fullname = excluded.fullname,
                market = excluded.market,
                publisher = excluded.publisher,
                index_type = excluded.index_type,
                category = excluded.category,
                base_date = excluded.base_date,
                base_point = excluded.base_point,
                list_date = excluded.list_date,
                weight_rule = excluded.weight_rule,
                description = excluded.description,
                updated_at = NOW()
        """

    def run(self) -> int:
        """
        拉取并保存所有指数列表

        Returns:
            保存的记录数
        """
        data = self.collect_all()
        return self.save(data)