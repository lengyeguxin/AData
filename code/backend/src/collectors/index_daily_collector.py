"""
IndexDailyCollector - 指数日线行情拉取器

严格按照CSV文档：
- 接口名称：index_daily
- 接口参数：trade_date={游标+1}
- 文档地址：https://tushare.pro/document/2?doc_id=95
- 游标策略：daily_trade（按交易日记录）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'code' / 'backend'))

from typing import Dict, List, Optional
from src.collectors.base_collector import BaseCollector
from src.core.tushare_api import TushareAPI
from src.core.transformers import convert_date_format


class IndexDailyCollector(BaseCollector):
    """指数日线行情拉取器（P1行情表，按交易日每日拉取）"""

    def __init__(self, db_path: str, api: TushareAPI):
        """
        初始化IndexDailyCollector

        Args:
            db_path: 数据库路径
            api: TushareAPI实例
        """
        super().__init__(
            db_path=db_path,
            api=api,
            table_name='index_daily',
            api_name='index_daily',  # 严格按照CSV文档
            date_field='trade_date',
            vip_interface=False  # 标准接口
        )

    def collect_by_date(self, trade_date: str, index_codes: Optional[List[str]] = None) -> List[Dict]:
        """
        拉取指定交易日的所有指数日线数据

        Args:
            trade_date: 交易日期（YYYYMMDD格式）
            index_codes: 指数列表（可选，不指定则从配置读取）

        Returns:
            指数日线数据列表

        注意：
            - 如果指定index_codes，只拉取这些指数
            - 如果不指定，从table_config.yaml的index_codes配置读取
            - index_daily接口需要ts_code参数（必填），不能只传trade_date。
        """
        self.logger.info(f"拉取指数日线数据: trade_date={trade_date}")

        # 如果没有指定指数列表，从配置读取
        if not index_codes:
            from pathlib import Path
            import yaml

            config_file = Path(__file__).parent.parent.parent / 'code' / 'backend' / 'config' / 'table_config.yaml'
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)

                index_codes = config.get('tables', {}).get('index_daily', {}).get('index_codes', [])

                if not index_codes:
                    self.logger.warning("未配置index_codes，将拉取所有指数")

        # 如果配置为空或未配置，则从index_basic表获取所有指数代码
        if not index_codes:
            from src.core.database import Database
            db = Database(self.db_path)

            index_codes = db.execute("""
                SELECT ts_code FROM index_basic ORDER BY ts_code
            """)

            db.close()
            self.logger.info(f"从index_basic表获取{len(index_codes)}个指数代码")

        all_data = []

        # 遍历所有指数代码
        for i, (ts_code,) in enumerate(index_codes):
            self.logger.info(f"拉取指数数据: {i+1}/{len(index_codes)} - {ts_code}")

            try:
                # 严格按照CSV文档参数：ts_code + trade_date
                data = self.collect(ts_code=ts_code, trade_date=trade_date)

                if data:
                    all_data.extend(data)
                    self.logger.debug(f"指数{ts_code}返回{len(data)}条数据")
                else:
                    self.logger.warning(f"指数{ts_code}返回空数据")

            except Exception as e:
                self.logger.error(f"拉取指数{ts_code}失败: {e}")
                # 继续拉取其他指数
                continue

        self.logger.info(f"拉取完成: 共{len(all_data)}条指数数据")
        return all_data

    def _extract_values(self, item: Dict) -> tuple:
        """
        提取字段值（严格按照index_daily_schema.sql定义，完整11个字段）

        Args:
            item: API返回的单条数据

        Returns:
            字段值元组（11个字段，严格按照schema定义顺序）
        """
        return (
            item.get('ts_code'),
            convert_date_format(item.get('trade_date')),
            item.get('close'),
            item.get('open'),
            item.get('high'),
            item.get('low'),
            item.get('pre_close'),
            item.get('change'),
            item.get('pct_chg'),
            item.get('vol'),
            item.get('amount'),
        )

    def _build_insert_query(self) -> str:
        """
        构建INSERT语句（ON CONFLICT处理，完整11个字段）

        Returns:
            INSERT SQL语句
        """
        fields = "ts_code, trade_date, close, open, high, low, pre_close, change, pct_chg, vol, amount, updated_at"

        placeholders = ', '.join(['?'] * 11) + ', NOW()'

        update_fields = "close = excluded.close, open = excluded.open, high = excluded.high, low = excluded.low, pre_close = excluded.pre_close, change = excluded.change, pct_chg = excluded.pct_chg, vol = excluded.vol, amount = excluded.amount, updated_at = NOW()"

        return f"""
            INSERT INTO index_daily (ts_code, trade_date, close, open, high, low, pre_close, change, pct_chg, vol, amount, updated_at)
            VALUES ({placeholders})
            ON CONFLICT (ts_code, trade_date)
            DO UPDATE SET {update_fields}
        """

    def run_by_date(self, trade_date: str) -> int:
        """
        拉取并保存指定交易日数据

        Args:
            trade_date: 交易日期（YYYYMMDD格式）

        Returns:
            保存的记录数
        """
        # 按指数逐个拉取、保存、更新游标
        total_count = 0
        success_indices = []  # 记录成功的指数

        for i, (ts_code,) in enumerate(index_codes):
            self.logger.info(f"拉取指数数据: {i+1}/{len(index_codes)} - {ts_code}, trade_date={trade_date}")

            try:
                # 拉取该指数数据
                data = self.collect(ts_code=ts_code, trade_date=trade_date)

                if data:
                    # 立即保存（避免竞态条件，单个指数单独插入）
                    count = 0
                    for item in data:
                        try:
                            record = self._extract_values(item)
                            query = self._build_insert_query()
                            db = Database(self.db_path)
                            db.execute(query, record)
                            db.close()
                            count += 1
                        except Exception as e:
                            self.logger.error(f"指数{ts_code}: {trade_date} 保存单条失败: {e}")

                    total_count += count
                    success_indices.append(ts_code)
                    self.logger.info(f"指数{ts_code}: {trade_date} 保存成功 ({count}条)")
                else:
                    self.logger.warning(f"指数{ts_code}: {trade_date} 无数据")

            except Exception as e:
                self.logger.error(f"拉取指数{ts_code}: {trade_date} 失败: {e}")
                # 继续拉取其他指数
                continue

        # 检查：所有指数都成功
        if len(success_indices) != len(index_codes):
            self.logger.error(f"拉取完成: trade_date={trade_date}, 失败{len(success_indices)}/{len(index_codes)}个指数，原因：部分指数失败")
            raise Exception(f"部分指数拉取失败: {len(success_indices)}/{len(index_codes)}个指数")

        self.logger.info(f"拉取完成: trade_date={trade_date}, 成功{total_count}/{len(index_codes) * 100}条记录")
        return total_count
