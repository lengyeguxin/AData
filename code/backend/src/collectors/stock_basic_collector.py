"""
StockBasicCollector - 股票列表拉取器

严格按照CSV文档：
- 接口名称：stock_basic
- 接口参数：无参数
- 文档地址：https://tushare.pro/document/2?doc_id=25
- 游标策略：none（无游标，全量拉取）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List, Tuple
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI


class StockBasicCollector(BaseCollector):
    """股票列表拉取器（P0前置表）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化StockBasicCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='stock_basic',
            api_name='stock_basic',  # 严格按照CSV文档
            date_field=None,  # 无日期字段
            vip_interface=False  # 标准接口
        )

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照p0_schema.sql定义）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组
        """
        from core.transformers import convert_date_format

        return (
            item.get('ts_code'),        # ts_code
            item.get('name'),           # name
            item.get('industry'),       # industry
            item.get('market'),         # market
            convert_date_format(item.get('list_date')),  # list_date
            convert_date_format(item.get('delist_date')), # delist_date
            item.get('is_hs'),          # is_hs
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句

        注意：DuckDB不允许在ON CONFLICT DO UPDATE SET中更新market字段
        """
        return """
            INSERT INTO stock_basic (
                ts_code, name, industry, market, list_date, delist_date, is_hs, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code)
            DO UPDATE SET
                name = excluded.name,
                industry = excluded.industry,
                list_date = excluded.list_date,
                delist_date = excluded.delist_date,
                is_hs = excluded.is_hs,
                updated_at = NOW()
        """