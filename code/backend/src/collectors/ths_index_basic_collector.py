"""
THSIndexBasicCollector - 同花顺指数列表拉取器

严格按照CSV文档：
- 接口名称：ths_index
- 接口参数：exchange=A, type=N/S（分两次拉取）
- 文档地址：https://tushare.pro/document/2?doc_id=259
- 游标策略：none（无游标，全量拉取）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class THSIndexBasicCollector(BaseCollector):
    """同花顺指数列表拉取器（P0前置表，全量拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化THSIndexBasicCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='ths_index_basic',
            api_name='ths_index',  # 严格按照CSV文档
            date_field=None,  # 无日期字段
            vip_interface=False  # 标准接口
        )

    def collect_all(self) -> List[Dict]:
        """
        拉取所有同花顺指数列表（分类型拉取：N概念 + S行业）

        Returns:
            同花顺指数列表数据

        注意：
            - exchange='A'（A股市场）
            - 分两次拉取：type='N'（概念板块）和type='S'（行业板块）
        """
        all_data = []

        # 分类型拉取（N概念板块、S行业板块）
        for type_code in ['N', 'S']:
            self.logger.info(f"拉取同花顺指数列表: exchange=A, type={type_code}")

            data = self.collect(exchange='A', type=type_code)
            all_data.extend(data)

        self.logger.info(f"拉取完成: 共{len(all_data)}条同花顺指数数据")
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
            item.get('exchange'),       # exchange
            item.get('type'),           # type
            convert_date_format(item.get('list_date')),  # list_date
            item.get('weight_rule'),    # weight_rule
            item.get('description'),    # description（不是desc）
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        注意：
            - type字段有索引，ON CONFLICT时不更新（避免约束错误）
            - ts_code是PRIMARY KEY，ON CONFLICT时也不更新

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO ths_index_basic (
                ts_code, name, fullname, exchange, type, list_date, weight_rule, description, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code)
            DO UPDATE SET
                name = excluded.name,
                fullname = excluded.fullname,
                exchange = excluded.exchange,
                list_date = excluded.list_date,
                weight_rule = excluded.weight_rule,
                description = excluded.description,
                updated_at = NOW()
        """

    def run(self) -> int:
        """
        拉取并保存所有同花顺指数列表

        Returns:
            保存的记录数
        """
        data = self.collect_all()
        return self.save(data)