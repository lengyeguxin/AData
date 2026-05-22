"""
HotsUserCollector - 游资账户拉取器

严格按照CSV文档：
- 接口名称：hm_list
- 接口参数：无参数
- 文档地址：https://tushare.pro/document/2%sdoc_id=311
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

    def __init__(self, db_config: dict, api: TushareAPI):
        """
        初始化HotsUserCollector

        Args:
            db_config: 数据库配置字典
            api: TushareAPI实例
        """
        super().__init__(
            db_config=db_config,
            api=api,
            table_name='hots_user',
            api_name='hm_list',  # 实际接口名（修正）
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

    def run(self) -> int:
        """
        拉取并保存所有游资账户列表

        Returns:
                       保存的记录数
        """
        data = self.collect_all()
        return self.save(data)

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照hots_user_schema.sql定义）

        Args:
            item: API返回结果

        Returns:
            字段值元组
        """
        return (
            item.get('name'),         # name (主键)
            item.get('desc'),        # description (原desc列)
            item.get('orgs'),        # orgs (关联机构)
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO hots_user (
                name, description, orgs, updated_at
            ) VALUES (%s, %s, %s, NOW())
            ON CONFLICT (name)
            DO UPDATE SET
                description = excluded.description,
                orgs = excluded.orgs,
                updated_at = NOW()
        """