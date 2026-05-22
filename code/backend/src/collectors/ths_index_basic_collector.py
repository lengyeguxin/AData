"""
THSIndexBasicCollector - 同花顺指数列表拉取器

严格按照CSV文档：
- 接口名称：ths_index
- 接口参数：exchange=A, type=N/S（分两次拉取）
- 文档地址：https://tushare.pro/document/2%sdoc_id=259
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

    def __init__(self, db_config: dict, api: TushareAPI):
        """
        初始化THSIndexBasicCollector

        Args:
            db_config: 数据库配置字典
            api: TushareAPI实例
        """
        super().__init__(
            db_config=db_config,
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
        提取字段值（严格按照ths_index_basic_schema.sql定义，完整6个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（6个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            item.get('name'),
            item.get('count'),
            item.get('exchange'),
            convert_date_format(item.get('list_date')),
            item.get('type'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整6个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, name, count, exchange, list_date, type, updated_at"

        placeholders = ', '.join(['%s'] * 6) + ', NOW()'

        update_fields = "name = excluded.name, count = excluded.count, exchange = excluded.exchange, list_date = excluded.list_date, type = excluded.type, updated_at = NOW()"

        return f"""
            INSERT INTO ths_index_basic (ts_code, name, count, exchange, list_date, type, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code)
            DO UPDATE SET {update_fields}
        """


def run(self) -> int:
        """
        拉取并保存所有同花顺指数列表

        Returns:
            保存的记录数
        """
        data = self.collect_all()
        return self.save(data)