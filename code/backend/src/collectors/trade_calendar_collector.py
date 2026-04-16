"""
TradeCalendarCollector - 交易日历拉取器

严格按照CSV文档：
- 接口名称：trade_cal
- 接口参数：exchange=SSE/SZSE, start_date={游标年+1}0101, end_date={当前年}1231
- 文档地址：https://tushare.pro/document/2?doc_id=26
- 游标策略：yearly（按年记录）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List, Tuple
from datetime import datetime
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class TradeCalendarCollector(BaseCollector):
    """交易日历拉取器（P0前置表，按年更新）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化TradeCalendarCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='trade_calendar',
            api_name='trade_cal',  # 严格按照CSV文档
            date_field='cal_date',  # 日历日期字段
            vip_interface=False  # 标准接口
        )

    def collect_year(self, year: int) -> List[Dict]:
        """
        拉取指定年份的交易日历（默认SSE即可）

        Args:
            year: 年份（如2025）

        Returns:
            交易日历数据列表

        示例：
            collect_year(2025) → 拉取2025年交易日历（默认SSE）
        """
        # YYYYMMDD 格式
        start_date = f"{year}0101"  # 年初：20210101
        end_date = f"{year}1231"    # 年末：20211231

        self.logger.info(
            f"拉取 {year}年 交易日历: "
            f"start_date={start_date}, end_date={end_date}"
        )

        # 只调用一次API（默认SSE即可，不需要分别调用SSE和SZSE）
        data = self.collect(
            exchange='SSE',
            start_date=start_date
        )

        self.logger.info(f"拉取完成: {year}年 共{len(data)}条交易日历")
        return data


    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照p0_schema.sql定义）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组
        """
        return (
            item.get('exchange'),       # exchange
            convert_date_format(item.get('cal_date')),  # cal_date
            item.get('is_open'),        # is_open
            convert_date_format(item.get('pretrade_date')),  # pretrade_date
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO trade_calendar (
                exchange, cal_date, is_open, pretrade_date, updated_at
            ) VALUES (?, ?, ?, ?, NOW())
            ON CONFLICT (exchange, cal_date)
            DO UPDATE SET
                is_open = excluded.is_open,
                pretrade_date = excluded.pretrade_date,
                updated_at = NOW()
        """

    def run_year(self, year: int) -> int:
        """
        拉取并保存指定年份交易日历

        Args:
            year: 年份

        Returns:
            保存的记录数
        """
        try:
            data = self.collect_year(year)
            return self.save(data)
        except Exception as e:
            self.logger.error(f"run_year({year}) 失败: {e}")
            raise