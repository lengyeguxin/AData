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

    def run(self) -> int:
        """
        拉取并保存所有游资账户列表

        Returns:
            保存的记录数
        """
        data = self.collect_all()
        return self.save(data)