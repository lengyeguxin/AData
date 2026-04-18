"""
THSConceptMemberCollector - 同花顺概念板块成分拉取器

严格按照CSV文档：
- 接口名称：ths_member
- 接口参数：ts_code={同花顺指数代码}（遍历ths_index_basic）
- 文档地址：https://tushare.pro/document/2?doc_id=261
- 游标策略：special_ths_member（特殊游标，遍历指数列表）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format
import duckdb


class THSConceptMemberCollector(BaseCollector):
    """同花顺概念板块成分拉取器（P3概念板块表，特殊游标）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化THSConceptMemberCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='ths_concept_member',
            api_name='ths_member',  # 严格按照CSV文档
            date_field=None,  # 无日期字段
            vip_interface=False  # 标准接口
        )

    def collect_all(self) -> List[Dict]:
        """
        遍历ths_index_basic拉取所有概念板块成分股（特殊游标策略）

        Returns:
            所有概念板块成分股数据

        注意：
            - 从ths_index_basic表获取所有概念指数代码（type='N'）
            - 遍历每个概念指数代码，拉取其成分股
            - 特殊游标策略：记录已拉取的指数代码
        """
        self.logger.info("开始遍历ths_index_basic拉取概念板块成分股")

        # 从数据库获取所有概念指数代码（type='N'）
        from src.core.database import Database
        db = Database(self.db_path)
        index_codes = db.execute(
            "SELECT ts_code FROM ths_index_basic WHERE type='N' ORDER BY ts_code"
        )
        db.close()

        self.logger.info(f"找到{len(index_codes)}个概念指数代码")

        all_data = []
        failed_indices = []  # 记录失败的指数及原因

        for i, (ts_code,) in enumerate(index_codes):
            self.logger.info(f"[{i+1}/{len(index_codes)}] 拉取概念板块成分: ts_code={ts_code}")

            try:
                data = self.collect(ts_code=ts_code)
                all_data.extend(data)
                self.logger.info(f"  拉取{len(data)}条成分股数据")
            except Exception as e:
                error_msg = str(e)
                self.logger.error(f"  拉取失败: {error_msg}")
                failed_indices.append((ts_code, error_msg))
                # 继续拉取下一个概念指数

        # 遍历完成，记录失败信息
        if failed_indices:
            self.logger.warning(f"遍历完成但有失败: 成功{len(index_codes)-len(failed_indices)}/{len(index_codes)}个指数")
            for ts_code, error in failed_indices[:10]:  # 只显示前10个失败
                self.logger.warning(f"  失败指数: {ts_code} - {error}")
            if len(failed_indices) > 10:
                self.logger.warning(f"  ... 还有{len(failed_indices)-10}个失败")
        else:
            self.logger.info(f"遍历完成: 全部成功，共拉取{len(all_data)}条概念板块成分数据")

        return all_data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照ths_concept_member_schema.sql定义，完整7个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（7个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            item.get('con_code'),
            item.get('con_name'),
            item.get('weight'),
            convert_date_format(item.get('in_date')),
            convert_date_format(item.get('out_date')),
            item.get('is_new'),
        )


    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整7个字段）

        Returns:
            INSERT SQL语句

        """
        fields = "ts_code, con_code, con_name, weight, in_date, out_date, is_new, updated_at"

        placeholders = ', '.join(['?'] * 7) + ', NOW()'

        update_fields = "con_name = excluded.con_name, weight = excluded.weight, in_date = excluded.in_date, out_date = excluded.out_date, is_new = excluded.is_new, updated_at = NOW()"

        return f"""
            INSERT INTO ths_concept_member (ts_code, con_code, con_name, weight, in_date, out_date, is_new, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, con_code)
            DO UPDATE SET {update_fields}
        """

    def run(self) -> int:
        """
        遍历并保存所有概念板块成分股

        Returns:
            保存的记录数
        """
        data = self.collect_all()
        return self.save(data)