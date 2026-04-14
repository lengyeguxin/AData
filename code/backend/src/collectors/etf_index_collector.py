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
        提取字段值（严格按照etf_index_schema.sql定义，完整8个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（8个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            item.get('indx_name'),
            item.get('indx_csname'),
            item.get('pub_party_name'),
            convert_date_format(item.get('pub_date')),
            convert_date_format(item.get('base_date')),
            item.get('bp'),
            item.get('adj_circle'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整8个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, indx_name, indx_csname, pub_party_name, pub_date, base_date, bp, adj_circle, updated_at"

        placeholders = ', '.join(['?'] * 8) + ', NOW()'

        update_fields = "indx_name = excluded.indx_name, indx_csname = excluded.indx_csname, pub_party_name = excluded.pub_party_name, pub_date = excluded.pub_date, base_date = excluded.base_date, bp = excluded.bp, adj_circle = excluded.adj_circle, updated_at = NOW()"

        return f"""
            INSERT INTO etf_index (ts_code, indx_name, indx_csname, pub_party_name, pub_date, base_date, bp, adj_circle, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code)
            DO UPDATE SET {update_fields}
        """


def run(self) -> int:
        """
        拉取并保存所有ETF基准指数信息

        Returns:
            保存的记录数
        """
        data = self.collect_all()
        return self.save(data)