"""
Collector基类

所有数据拉取collector继承此基类，消除代码冗余。
子类只需实现：
1. _extract_values(): 提取字段值
2. _build_insert_query(): 构建INSERT语句
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.database import Database
from core.tushare_api import TushareAPI
from core.logger import get_logger
from core.transformers import convert_date_format


class BaseCollector:
    """
    Collector基类（消除代码冗余）

    所有collector继承此基类，只需实现：
    1. _extract_values(): 提取字段值
    2. _build_insert_query(): 构建INSERT语句
    """

    def __init__(
        self,
        db_path: str,
        api: TushareAPI,
        table_name: str,
        api_name: str,
        date_field: str = 'trade_date',
        vip_interface: bool = False
    ):
        """
        初始化Collector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
            table_name: 表名
            api_name: Tushare API名称（严格按CSV文档）
            date_field: 日期字段名（默认'trade_date'）
            vip_interface: 是否VIP接口（财务表使用VIP接口）
        """
        self.db_path = db_path
        self.api = api
        self.table_name = table_name
        self.api_name = api_name
        self.date_field = date_field
        self.vip_interface = vip_interface
        self.logger = get_logger(__name__)

    def collect(self, **kwargs) -> List[Dict]:
        """
        通用数据拉取逻辑

        Args:
            **kwargs: API参数（如ts_code, trade_date, start_date, end_date等）

        Returns:
            数据列表（字典格式）
        """
        self.logger.info(
            f"拉取 {self.table_name}: API={self.api_name}, 参数={kwargs}"
        )

        try:
            # 调用TushareAPI
            data = self.api.query(self.api_name, **kwargs)

            self.logger.info(f"拉取成功: {len(data)}条记录")
            return data

        except Exception as e:
            self.logger.error(f"拉取失败: {e}")
            raise

    def transform(self, data: List[Dict]) -> List[tuple]:
        """
        数据转换（通用转换：日期格式）

        Args:
            data: 原始数据列表

        Returns:
            转换后的元组列表
        """
        records = []

        for item in data:
            # 通用转换：日期格式转换（YYYYMMDD → YYYY-MM-DD）
            for date_key in ['trade_date', 'ann_date', 'end_date', 'cal_date',
                             'list_date', 'delist_date', 'f_ann_date', 'record_date',
                             'ex_date', 'pay_date', 'pretrade_date', 'base_date']:
                if date_key in item and item[date_key]:
                    item[date_key] = convert_date_format(item[date_key])

            # 提取字段值（子类实现）
            record = self._extract_values(item)
            records.append(record)

        return records

    def save(self, data: List[Dict]) -> int:
        """
        通用保存逻辑（批量入库，ON CONFLICT）

        Args:
            data: 数据列表

        Returns:
            保存的记录数
        """
        if not data:
            self.logger.warning(f"{self.table_name}: 无数据需要保存")
            return 0

        self.logger.info(f"{self.table_name}: 开始保存 {len(data)}条记录")

        # 构建INSERT语句（子类实现）
        query = self._build_insert_query()

        # 转换数据
        records = self.transform(data)

        # 使用上下文管理器自动关闭连接（避免连接泄漏，确保WAL能合并）
        with Database(self.db_path) as db:
            try:
                # 批量插入
                for record in records:
                    db.execute(query, record)

                self.logger.info(f"{self.table_name}: 保存成功 {len(records)}条记录")
                return len(records)

            except Exception as e:
                self.logger.error(f"{self.table_name}: 保存失败: {e}")
                raise

    def run(self, **kwargs) -> int:
        """
        主入口：拉取并保存

        Args:
            **kwargs: API参数

        Returns:
            保存的记录数
        """
        data = self.collect(**kwargs)
        return self.save(data)

    def check_data_exists(self, **kwargs) -> bool:
        """
        检查数据是否已存在（避免重复拉取）

        Args:
            **kwargs: 查询参数（如ts_code, trade_date）

        Returns:
            数据是否已存在
        """
        # 构建查询条件
        conditions = []
        params = []

        if 'ts_code' in kwargs:
            conditions.append("ts_code = ?")
            params.append(kwargs['ts_code'])

        if 'trade_date' in kwargs:
            # 转换日期格式
            date_formatted = convert_date_format(kwargs['trade_date'])
            conditions.append("trade_date = ?")
            params.append(date_formatted)

        if 'ann_date' in kwargs:
            date_formatted = convert_date_format(kwargs['ann_date'])
            conditions.append("ann_date = ?")
            params.append(date_formatted)

        if 'cal_date' in kwargs:
            date_formatted = convert_date_format(kwargs['cal_date'])
            conditions.append("cal_date = ?")
            params.append(date_formatted)

        if not conditions:
            return False

        query = f"""
            SELECT COUNT(*)
            FROM {self.table_name}
            WHERE {' AND '.join(conditions)}
            LIMIT 1
        """

        # 使用Database类统一管理连接
        with Database(self.db_path) as db:
            result = db.execute(query, tuple(params))

            return result[0][0] > 0

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（子类必须实现）

        Args:
            item: 单条数据

        Returns:
            字段值元组
        """
        raise NotImplementedError("子类必须实现 _extract_values()")

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（子类必须实现）

        Returns:
            INSERT SQL语句（包含ON CONFLICT）
        """
        raise NotImplementedError("子类必须实现 _build_insert_query()")

    def get_table_count(self) -> int:
        """
        获取表的记录数

        Returns:
            记录数
        """
        query = f"SELECT COUNT(*) FROM {self.table_name}"

        # 使用Database类统一管理连接
        with Database(self.db_path) as db:
            result = db.execute(query)

            return result[0][0]

    def get_last_date(self) -> Optional[str]:
        """
        获取表的最后日期（用于判断进度）

        Returns:
            最后日期（YYYY-MM-DD格式）
        """
        query = f"""
            SELECT MAX({self.date_field})
            FROM {self.table_name}
        """

        # 使用Database类统一管理连接
        with Database(self.db_path) as db:
            result = db.execute(query)

            if result and result[0] and result[0][0]:
                return str(result[0][0])

        return None