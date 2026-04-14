"""
StockDailyBasicCollector - 每日估值指标拉取器

严格按照CSV文档：
- 接口名称：daily_basic
- 接口参数：trade_date={游标+1}
- 文档地址：https://tushare.pro/document/2?doc_id=32
- 游标策略：daily_trade（按交易日记录）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class StockDailyBasicCollector(BaseCollector):
    """每日估值指标拉取器（P1行情表，按交易日每日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化StockDailyBasicCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='stock_daily_basic',
            api_name='daily_basic',  # 严格按照CSV文档
            date_field='trade_date',
            vip_interface=False  # 标准接口
        )

    def collect_by_date(self, trade_date: str) -> List[Dict]:
        """
        拉取指定交易日的所有股票每日估值指标数据

        Args:
            trade_date: 交易日期（YYYYMMDD格式）

        Returns:
            每日估值指标数据列表

        示例：
            collect_by_date('20260409') → 拉取2026-04-09所有股票估值指标
        """
        self.logger.info(f"拉取每日估值指标: trade_date={trade_date}")

        # 严格按照CSV文档参数
        data = self.collect(trade_date=trade_date)

        return data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照p1_schema.sql定义）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（字段顺序：ts_code, trade_date, close, pe, pe_ttm, pb, ps, ps_ttm, dv_ratio, dv_ttm, total_mv, circ_mv, total_share, float_share, free_share, turnover_rate, turnover_rate_f, volume_ratio）
        """
        return (
            item.get('ts_code'),        # ts_code
            convert_date_format(item.get('trade_date')),  # trade_date
            item.get('close'),          # close（当日收盘价）
            item.get('pe'),             # pe
            item.get('pe_ttm'),         # pe_ttm
            item.get('pb'),             # pb
            item.get('ps'),             # ps
            item.get('ps_ttm'),         # ps_ttm
            item.get('dv_ratio'),       # dv_ratio
            item.get('dv_ttm'),         # dv_ttm（新增）
            item.get('total_mv'),       # total_mv
            item.get('circ_mv'),        # circ_mv
            item.get('total_share'),    # total_share（新增：总股本）
            item.get('float_share'),    # float_share（新增：流通股本）
            item.get('free_share'),     # free_share（新增：自由流通股本）
            item.get('turnover_rate'),  # turnover_rate
            item.get('turnover_rate_f'), # turnover_rate_f（新增）
            item.get('volume_ratio'),   # volume_ratio
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理）

        Returns:
            INSERT SQL语句
        """
        return """
            INSERT INTO stock_daily_basic (
                ts_code, trade_date, close, pe, pe_ttm, pb, ps, ps_ttm,
                dv_ratio, dv_ttm, total_mv, circ_mv,
                total_share, float_share, free_share,
                turnover_rate, turnover_rate_f, volume_ratio, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET
                close = excluded.close,
                pe = excluded.pe,
                pe_ttm = excluded.pe_ttm,
                pb = excluded.pb,
                ps = excluded.ps,
                ps_ttm = excluded.ps_ttm,
                dv_ratio = excluded.dv_ratio,
                dv_ttm = excluded.dv_ttm,
                total_mv = excluded.total_mv,
                circ_mv = excluded.circ_mv,
                total_share = excluded.total_share,
                float_share = excluded.float_share,
                free_share = excluded.free_share,
                turnover_rate = excluded.turnover_rate,
                turnover_rate_f = excluded.turnover_rate_f,
                volume_ratio = excluded.volume_ratio,
                updated_at = NOW()
        """

    def run_by_date(self, trade_date: str) -> int:
        """
        拉取并保存指定交易日数据

        Args:
            trade_date: 交易日期（YYYYMMDD）

        Returns:
            保存的记录数
        """
        data = self.collect_by_date(trade_date)
        return self.save(data)