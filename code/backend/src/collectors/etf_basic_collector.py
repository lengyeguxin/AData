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
        提取字段值（严格按照etf_basic_schema.sql定义，完整14个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（14个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            item.get('csname'),
            item.get('extname'),
            item.get('cname'),
            item.get('index_code'),
            item.get('index_name'),
            convert_date_format(item.get('setup_date')),
            convert_date_format(item.get('list_date')),
            item.get('list_status'),
            item.get('exchange'),
            item.get('mgr_name'),
            item.get('custod_name'),
            item.get('mgt_fee'),
            item.get('etf_type'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整14个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, csname, extname, cname, index_code, index_name, setup_date, list_date, list_status, exchange, mgr_name, custod_name, mgt_fee, etf_type, updated_at"

        placeholders = ', '.join(['?'] * 14) + ', NOW()'

        update_fields = "csname = excluded.csname, extname = excluded.extname, cname = excluded.cname, index_code = excluded.index_code, index_name = excluded.index_name, setup_date = excluded.setup_date, list_date = excluded.list_date, list_status = excluded.list_status, exchange = excluded.exchange, mgr_name = excluded.mgr_name, custod_name = excluded.custod_name, mgt_fee = excluded.mgt_fee, etf_type = excluded.etf_type, updated_at = NOW()"

        return f"""
            INSERT INTO etf_basic (ts_code, csname, extname, cname, index_code, index_name, setup_date, list_date, list_status, exchange, mgr_name, custod_name, mgt_fee, etf_type, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code)
            DO UPDATE SET {update_fields}
        """


def run(self) -> int:
        """
        拉取并保存所有ETF基本信息

        Returns:
            保存的记录数
        """
        data = self.collect_all()
        return self.save(data)