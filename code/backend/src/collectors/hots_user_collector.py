"""
HotsUserCollector - 游资账户拉取器

严格按照CSV文档：
- 接口名称：hots_user
- 接口参数：无参数
- 文档地址：https://tushare.pro/document/2?doc_id=272
- 游标策略：none（无游标，全量拉取）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class HotsUserCollector(BaseCollector):
    """游资账户拉取器（P4游资表，全量拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化HotsUserCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='hots_user',
            api_name='hots_user',  # 严格按照CSV文档
            date_field=None,  # 无日期字段
            vip_interface=False  # 标准接口
        )

    def collect_all(self) -> List[Dict]:
        """
        拉取所有游资账户列表（无参数）

        Returns:
            游资账户列表

        注意：
            - 无参数（全量拉取）
            - 按月更新策略
        """
        self.logger.info("拉取游资账户列表: 无参数")

        data = self.collect()

        self.logger.info(f"拉取完成: 共{len(data)}条游资账户数据")
        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照p2_schema.sql定义，完整6个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（6个字段）
        """
        return (
            item.get('account'),        # account（主键）
            item.get('trader_name'),    # trader_name
            item.get('broker_name'),    # broker_name
            item.get('license'),        # license
            convert_date_format(item.get('reg_date')),  # reg_date
            item.get('status'),         # status
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整6个字段）

        Returns:
            INSERT SQL语句

        注意：
            - 主键：account（VARCHAR(50) PRIMARY KEY）
        """
        return """
            INSERT INTO hots_user (
                account, trader_name, broker_name, license, reg_date, status, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (account)
            DO UPDATE SET
                trader_name = excluded.trader_name,
                broker_name = excluded.broker_name,
                license = excluded.license,
                reg_date = excluded.reg_date,
                status = excluded.status,
                updated_at = NOW()
        """

    def run(self) -> int:
        """
        拉取并保存所有游资账户列表

        Returns:
            保存的记录数
        """
        data = self.collect_all()
        return self.save(data)