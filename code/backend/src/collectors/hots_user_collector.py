"""
HotsUserCollector - 游资账户拉取器

严格按照CSV文档：
- 接口名称：hm_list
- 接口参数：无参数
- 文档地址：https://tushare.pro/document/2?doc_id=311
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

    def save(self, data: List[Dict]) -> int:
        """
        保存数据（过滤account为None的记录）

        Args:
            data: 数据列表

        Returns:
            保存的记录数

        注意：
            - account是主键且NOT NULL，不能为NULL
            - 过滤掉account为None的记录
        """
        # 过滤account为None的数据
        filtered_data = [
            item for item in data
            if item.get('account') is not None
        ]

        if len(filtered_data) < len(data):
            self.logger.warning(
                f"过滤了{len(data) - len(filtered_data)}条account为NULL的记录"
            )

        # 调用父类save方法
        return super().save(filtered_data)

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照hots_user_schema.sql定义，完整2个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（2个字段，严格按照schema定义顺序）
        """
        return (
            item.get('name'),
            item.get('orgs'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整2个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "name, orgs, updated_at"

        placeholders = ', '.join(['?'] * 2) + ', NOW()'

        update_fields = "name = excluded.name, orgs = excluded.orgs, updated_at = NOW()"

        return f"""
            INSERT INTO hots_user (name, orgs, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (account)
            DO UPDATE SET {update_fields}
        """


def run(self) -> int:
        """
        拉取并保存所有游资账户列表

        Returns:
            保存的记录数
        """
        data = self.collect_all()
        return self.save(data)