"""
统一数据拉取控制器

负责协调所有数据表的拉取流程：
- 启动流程：按固定顺序拉取前置表
- 判断进度：读取游标，断点续传
- 数据存在性检查：避免重复爬取
- 18点时间判断：确保数据完整性
- 按优先级顺序拉取：P0 → P1 → P2 → P3 → P4
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from src.core.global_cursor_manager import GlobalCursorManager
from src.core.logger import get_logger


class DataFetcher:
    """统一数据拉取控制器"""

    # 前置表固定顺序（必须先拉取）
    PRIORITY_ORDER = {
        'P0': [
            'trade_calendar',
            'stock_basic',
            'index_basic',
            'ths_index_basic',
            'etf_basic',
            'etf_index'
        ],
        'P1': [
            'stock_daily',
            'stock_daily_basic',
            'stock_weekly',
            'stock_monthly',
            'index_daily',
            'etf_daily',
            'etf_adj_factor'
        ],
        'P2': [
            'fina_indicator',
            'income',
            'balancesheet',
            'cashflow',
            'express',
            'express_brief',
            'dividend'
        ],
        'P3': [
            'ths_moneyflow',
            'ths_concept_moneyflow',
            'ths_industry_moneyflow',
            'ths_concept_member',
            'ths_index_daily'
        ],
        'P4': [
            'hots_user',
            'hots_trader_detail'
        ]
    }

    def __init__(self, db_path: str, config: Dict):
        """
        初始化数据拉取控制器

        Args:
            db_path: 数据库路径
            config: 配置字典
        """
        self.db_path = db_path
        self.config = config
        self.logger = get_logger(__name__)

        # 初始化游标管理器
        self.cursor_manager = GlobalCursorManager(db_path, 'code/backend/config')

        # 数据拉取开关
        self.fetch_enabled = config.get('fetch', {}).get('enabled', True)

        # 加载交易日历（启动时一次性加载到内存）
        self.trade_calendar = self._load_trade_calendar()

    def start(self):
        """
        启动数据拉取（入口方法）

        流程：
        1. 检查fetch.enabled开关
        2. 加载交易日历到内存
        3. 按优先级顺序拉取（P0 → P1 → P2 → P3 → P4）
        4. 每张表判断游标进度，断点续传
        5. 更新游标（根据策略决定更新时机）
        """
        if not self.fetch_enabled:
            self.logger.info("数据拉取已禁用（fetch.enabled=false）")
            return

        self.logger.info("=" * 80)
        self.logger.info("数据拉取控制器启动")
        self.logger.info("=" * 80)
        self.logger.info(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"数据库路径: {self.db_path}")
        self.logger.info(f"交易日历已加载: {len(self.trade_calendar)}个交易日")
        self.logger.info("")

        # 按优先级顺序拉取所有表
        self._fetch_all_tables()

    def _load_trade_calendar(self) -> List[str]:
        """
        加载交易日历到内存（启动时一次性加载）

        Returns:
            交易日列表（YYYY-MM-DD格式）
        """
        query = """
            SELECT cal_date
            FROM trade_calendar
            WHERE is_open = 1
            ORDER BY cal_date
        """

        try:
            # 使用Database类统一管理连接
            from src.core.database import Database
            db = Database(self.db_path)
            results = db.execute(query)

            # 转换为YYYYMMDD格式（去掉横线）
            trade_dates = [str(row[0]).replace('-', '') for row in results]

            self.logger.info(f"交易日历加载成功: {len(trade_dates)}个交易日")
            return trade_dates

        except Exception as e:
            self.logger.warning(f"交易日历加载失败（表可能未初始化）: {e}")
            return []

    def _fetch_all_tables(self):
        """
        拉取所有表（按优先级顺序）

        顺序：P0前置表 → P1行情表 → P2财务表 → P3其他表 → P4游资表
        """
        # P0前置表（必须先拉取）
        self.logger.info("拉取P0前置表（固定顺序）...")
        for table_name in self.PRIORITY_ORDER['P0']:
            if not self.fetch_enabled:
                self.logger.info("数据拉取已停止")
                return

            self._fetch_table(table_name)

        self.logger.info("")

        # P1行情表
        self.logger.info("拉取P1行情表...")
        for table_name in self.PRIORITY_ORDER['P1']:
            if not self.fetch_enabled:
                self.logger.info("数据拉取已停止")
                return

            self._fetch_table(table_name)

        self.logger.info("")

        # P2财务表
        self.logger.info("拉取P2财务表...")
        for table_name in self.PRIORITY_ORDER['P2']:
            if not self.fetch_enabled:
                self.logger.info("数据拉取已停止")
                return

            self._fetch_table(table_name)

        self.logger.info("")

        # P3其他表
        self.logger.info("拉取P3其他表...")
        for table_name in self.PRIORITY_ORDER['P3']:
            if not self.fetch_enabled:
                self.logger.info("数据拉取已停止")
                return

            self._fetch_table(table_name)

        self.logger.info("")

        # P4游资表
        self.logger.info("拉取P4游资表...")
        for table_name in self.PRIORITY_ORDER['P4']:
            if not self.fetch_enabled:
                self.logger.info("数据拉取已停止")
                return

            self._fetch_table(table_name)

    def _fetch_table(self, table_name: str):
        """
        拉取单张表（核心逻辑）

        Args:
            table_name: 表名
        """
        self.logger.info(f"开始拉取: {table_name}")

        # 1. 判断是否需要拉取（游标+前置表+时间）
        if not self.cursor_manager.should_fetch(table_name):
            cursor = self.cursor_manager.get_cursor(table_name)
            self.logger.info(
                f"{table_name}: 游标已是最新或前置表未完成"
                f"(cursor={cursor['cursor_value']}, status={cursor['status']})"
            )
            return

        # 2. 标记为running
        self.cursor_manager.mark_running(table_name)

        try:
            # 3. 获取游标策略
            cursor_strategy = self.cursor_manager.get_cursor_strategy(table_name)

            # 4. 根据策略拉取
            if cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_NONE:
                # 无游标：全量拉取
                record_count = self._fetch_none_strategy(table_name)

            elif cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_DAILY_TRADE:
                # 按交易日：增量拉取
                record_count = self._fetch_daily_trade_strategy(table_name)

            elif cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_DAILY_NATURAL:
                # 按自然日：增量拉取（财务表）
                record_count = self._fetch_daily_natural_strategy(table_name)

            elif cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_YEARLY:
                # 按年：增量拉取
                record_count = self._fetch_yearly_strategy(table_name)

            elif cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_SPECIAL_THS_MEMBER:
                # 特殊游标：遍历指数列表
                record_count = self._fetch_special_ths_member_strategy(table_name)

            else:
                self.logger.error(f"{table_name}: 未知的游标策略 {cursor_strategy}")
                self.cursor_manager.mark_failed(table_name, "未知的游标策略")
                return

            # 5. 判断是否更新游标
            has_data = record_count > 0
            should_update = self.cursor_manager.should_update_cursor(table_name, has_data)

            if should_update:
                # 计算新的游标值
                new_cursor_value = self._calculate_new_cursor_value(
                    table_name, cursor_strategy
                )
                self.cursor_manager.update_cursor(table_name, new_cursor_value, record_count)
                self.logger.info(
                    f"{table_name}: 拉取成功，游标更新为 {new_cursor_value}"
                    f"({record_count}条记录)"
                )
            else:
                # 不更新游标（无数据且不允许无数据更新）
                self.logger.warning(
                    f"{table_name}: 拉取完成但无数据，游标不更新"
                )
                # 标记为失败（需要在Dashboard展示）
                self.cursor_manager.mark_failed(table_name, "无数据（行情表必须有数据）")

        except Exception as e:
            self.logger.error(f"{table_name}: 拉取失败: {e}")
            self.cursor_manager.mark_failed(table_name, str(e))
            raise

    def _fetch_none_strategy(self, table_name: str) -> int:
        """
        无游标策略（全量拉取）

        Args:
            table_name: 表名

        Returns:
            拉取的记录数
        """
        self.logger.info(f"{table_name}: 无游标策略，全量拉取")

        # 获取对应的Collector
        collector = self._get_collector(table_name)

        if not collector:
            self.logger.error(f"{table_name}: 未找到对应的Collector")
            return 0

        # 调用Collector拉取数据
        try:
            # 不同表的拉取参数不同
            if table_name == 'stock_basic':
                count = collector.run()
            elif table_name == 'trade_calendar':
                # 拉取当年数据
                current_year = datetime.now().year
                count = collector.run_year(current_year)
            elif table_name == 'index_basic':
                count = collector.run()
            elif table_name == 'etf_basic':
                count = collector.run()
            elif table_name == 'ths_index_basic':
                count = collector.run()
            else:
                # 默认全量拉取
                count = collector.run()

            self.logger.info(f"{table_name}: 全量拉取成功 ({count}条记录)")
            return count

        except Exception as e:
            self.logger.error(f"{table_name}: 全量拉取失败: {e}")
            raise

    def _fetch_daily_trade_strategy(self, table_name: str) -> int:
        """
        按交易日策略（增量拉取）

        Args:
            table_name: 表名

        Returns:
            拉取的记录数
        """
        self.logger.info(f"{table_name}: 按交易日策略，增量拉取")

        # 1. 获取下次拉取日期（游标+1）
        start_date = self.cursor_manager.get_next_fetch_date(table_name)

        # 2. 获取结束日期（18点判断）
        end_date = self.cursor_manager.get_end_date_with_time_check(table_name)

        self.logger.info(f"{table_name}: 从 {start_date} 到 {end_date}")

        # 3. 过滤交易日
        trade_dates = self._filter_trade_dates(start_date, end_date)

        self.logger.info(f"{table_name}: 共 {len(trade_dates)} 个交易日")

        if not trade_dates:
            self.logger.info(f"{table_name}: 无新交易日需要拉取")
            return 0

        # 4. 获取Collector
        collector = self._get_collector(table_name)

        if not collector:
            self.logger.error(f"{table_name}: 未找到对应的Collector")
            return 0

        # 5. 遍历交易日拉取
        total_count = 0
        for trade_date in trade_dates:
            # 检查数据是否已存在（避免重复爬取）
            if self._data_exists(table_name, trade_date):
                self.logger.info(f"{table_name}: {trade_date} 数据已存在，跳过")
                continue

            try:
                # 调用Collector拉取该日期数据
                count = collector.run(trade_date=trade_date)

                total_count += count

                if count > 0:
                    self.logger.info(f"{table_name}: {trade_date} 拉取成功 ({count}条)")

            except Exception as e:
                self.logger.error(f"{table_name}: {trade_date} 拉取失败: {e}")
                # 继续拉取下一个日期
                continue

        return total_count

    def _fetch_daily_natural_strategy(self, table_name: str) -> int:
        """
        按自然日策略（财务表，增量拉取）

        Args:
            table_name: 表名

        Returns:
            拉取的记录数
        """
        self.logger.info(f"{table_name}: 按自然日策略，增量拉取（财务表）")

        # 1. 获取下次拉取日期（游标+1）
        start_date = self.cursor_manager.get_next_fetch_date(table_name)

        # 2. 获取结束日期（今天）
        end_date = datetime.now().strftime('%Y%m%d')

        self.logger.info(f"{table_name}: 从 {start_date} 到 {end_date}（自然日）")

        # 3. 获取Collector
        collector = self._get_collector(table_name)

        if not collector:
            self.logger.error(f"{table_name}: 未找到对应的Collector")
            return 0

        # 4. 遍历自然日拉取
        total_count = 0
        current_date = datetime.strptime(start_date, '%Y%m%d')
        end_datetime = datetime.strptime(end_date, '%Y%m%d')

        while current_date <= end_datetime:
            date_str = current_date.strftime('%Y%m%d')

            # 检查数据是否已存在
            if self._data_exists(table_name, date_str):
                self.logger.info(f"{table_name}: {date_str} 数据已存在，跳过")
                current_date += timedelta(days=1)
                continue

            try:
                # 调用Collector拉取该日期数据
                # 财务表需要report_type参数
                if table_name in ['income', 'balancesheet', 'cashflow']:
                    count = collector.run(ann_date=date_str, report_type='1')
                else:
                    count = collector.run(ann_date=date_str)

                total_count += count

                if count > 0:
                    self.logger.info(f"{table_name}: {date_str} 拉取成功 ({count}条)")
                else:
                    # 财务表允许无数据（ann_date可能无数据）
                    self.logger.info(f"{table_name}: {date_str} 无数据（正常）")

            except Exception as e:
                self.logger.error(f"{table_name}: {date_str} 拉取失败: {e}")
                current_date += timedelta(days=1)
                continue

            current_date += timedelta(days=1)

        return total_count

    def _fetch_yearly_strategy(self, table_name: str) -> int:
        """
        按年策略（增量拉取）

        Args:
            table_name: 表名

        Returns:
            拉取的记录数
        """
        self.logger.info(f"{table_name}: 按年策略，增量拉取")

        # 1. 获取下次拉取年份（游标+1）
        next_year = self.cursor_manager.get_next_fetch_date(table_name)

        # 2. 获取当前年份
        current_year = datetime.now().year

        self.logger.info(f"{table_name}: 从 {next_year} 年开始")

        # 3. 获取Collector
        collector = self._get_collector(table_name)

        if not collector:
            self.logger.error(f"{table_name}: 未找到对应的Collector")
            return 0

        try:
            # 调用Collector拉取该年数据
            if table_name == 'trade_calendar':
                count = collector.run_year(int(next_year))
            else:
                count = collector.run(year=int(next_year))

            self.logger.info(f"{table_name}: {next_year}年 拉取成功 ({count}条)")
            return count

        except Exception as e:
            self.logger.error(f"{table_name}: {next_year}年 拉取失败: {e}")
            raise

    def _fetch_special_ths_member_strategy(self, table_name: str) -> int:
        """
        特殊游标策略（ths_concept_member）

        Args:
            table_name: 表名

        Returns:
            拉取的记录数
        """
        self.logger.info(f"{table_name}: 特殊游标策略，遍历指数列表")

        # 获取Collector
        collector = self._get_collector(table_name)

        if not collector:
            self.logger.error(f"{table_name}: 未找到对应的Collector")
            return 0

        try:
            # ths_concept_member需要遍历ths_index_basic的所有指数代码
            # 调用ths_member接口拉取成分股
            count = collector.run()

            self.logger.info(f"{table_name}: 拉取成功 ({count}条)")
            return count

        except Exception as e:
            self.logger.error(f"{table_name}: 拉取失败: {e}")
            raise

    def _get_collector(self, table_name: str):
        """
        根据表名获取对应的Collector实例

        Args:
            table_name: 表名

        Returns:
            Collector实例
        """
        # Collector映射表
        COLLECTOR_MAP = {
            'stock_daily': 'DailyCollector',
            'stock_daily_basic': 'StockDailyBasicCollector',
            'stock_basic': 'StockBasicCollector',
            'stock_weekly': 'WeeklyCollector',
            'stock_monthly': 'MonthlyCollector',
            'trade_calendar': 'TradeCalendarCollector',
            'index_basic': 'IndexBasicCollector',
            'index_daily': 'IndexDailyCollector',
            'etf_basic': 'ETFBasicCollector',
            'etf_daily': 'ETFDailyCollector',
            'etf_adj_factor': 'ETFAdjFactorCollector',
            'etf_index': 'ETFIndexCollector',
            'fina_indicator': 'FinaIndicatorCollector',
            'income': 'IncomeCollector',
            'balancesheet': 'BalancesheetCollector',
            'cashflow': 'CashflowCollector',
            'dividend': 'DividendCollector',
            'express': 'ExpressCollector',
            'express_brief': 'ExpressBriefCollector',
            'ths_index_basic': 'THSIndexBasicCollector',
            'ths_concept_member': 'THSConceptMemberCollector',
            'ths_moneyflow': 'THSMoneyflowCollector',
            'ths_concept_moneyflow': 'THSConceptMoneyflowCollector',
            'ths_industry_moneyflow': 'THSIndustryMoneyflowCollector',
            'ths_index_daily': 'THSIndexDailyCollector',
            'hots_user': 'HotsUserCollector',
            'hots_trader_detail': 'HotsTraderDetailCollector',
        }

        collector_class_name = COLLECTOR_MAP.get(table_name)

        if not collector_class_name:
            self.logger.warning(f"{table_name}: 未在映射表中找到Collector")
            return None

        # 动态导入Collector
        try:
            # 导入Collector模块
            import importlib

            # 根据类名确定模块名（驼峰转下划线，处理缩写）
            # 例如: TradeCalendarCollector → trade_calendar_collector
            # 例如: THSIndexBasicCollector → ths_index_basic_collector
            # 例如: ETFBasicCollector → etf_basic_collector
            import re
            # 先移除'Collector'后缀
            name_without_collector = collector_class_name.replace('Collector', '')
            # 特殊处理：先替换全大写缩写（THS→ths, ETF→etf）
            # 然后驼峰转下划线（Index→index_basic）
            # Step 1: 全大写缩写转小写
            name_with_abbrevs = re.sub('([A-Z]+)([A-Z][a-z])', r'\1_\2', name_without_collector)
            # Step 2: 驼峰转下划线（剩余的驼峰部分）
            name_snake = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name_with_abbrevs).lower()
            module_name = name_snake + '_collector'

            # 导入模块
            module = importlib.import_module(f'src.collectors.{module_name}')

            # 获取类
            collector_class = getattr(module, collector_class_name)

            # 创建实例（需要db_path和api）
            # 从config获取tushare配置，创建API实例
            from src.core.tushare_api import TushareAPI
            api = TushareAPI(self.config['tushare'])

            # 创建Collector实例
            collector = collector_class(self.db_path, api)

            return collector

        except Exception as e:
            self.logger.error(f"{table_name}: 导入Collector失败: {e}")
            return None

    def _filter_trade_dates(self, start_date: str, end_date: str) -> List[str]:
        """
        过滤交易日（从加载的交易日历中）

        Args:
            start_date: 开始日期（YYYYMMDD）
            end_date: 结束日期（YYYYMMDD）

        Returns:
            交易日列表
        """
        trade_dates = []

        for date in self.trade_calendar:
            if start_date <= date <= end_date:
                trade_dates.append(date)

        return trade_dates

    def _data_exists(self, table_name: str, date: str) -> bool:
        """
        检查数据是否已存在（避免重复爬取）

        Args:
            table_name: 表名
            date: 日期（YYYYMMDD）

        Returns:
            数据是否已存在
        """
        # 转换日期格式（YYYYMMDD → YYYY-MM-DD）
        date_formatted = f"{date[:4]}-{date[4:6]}-{date[6:8]}"

        # 根据表名判断字段名
        date_field = self._get_date_field(table_name)

        if not date_field:
            return False

        query = f"""
            SELECT COUNT(*)
            FROM {table_name}
            WHERE {date_field} = ?
            LIMIT 1
        """

        try:
            from src.core.database import Database
            db = Database(self.db_path)
            result = db.execute(query, (date_formatted,))

            return result[0][0] > 0

        except Exception as e:
            self.logger.warning(f"{table_name}: 数据存在性检查失败: {e}")
            return False

    def _get_date_field(self, table_name: str) -> Optional[str]:
        """
        获取表的日期字段名

        Args:
            table_name: 表名

        Returns:
            日期字段名（trade_date、ann_date、cal_date等）
        """
        # 根据游标策略判断日期字段
        cursor_strategy = self.cursor_manager.get_cursor_strategy(table_name)

        if cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_DAILY_TRADE:
            return 'trade_date'

        elif cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_DAILY_NATURAL:
            return 'ann_date'

        elif cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_YEARLY:
            return 'cal_date'

        return None

    def _calculate_new_cursor_value(self, table_name: str, cursor_strategy: str) -> str:
        """
        计算新的游标值

        Args:
            table_name: 表名
            cursor_strategy: 游标策略

        Returns:
            新的游标值
        """
        if cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_DAILY_TRADE:
            # 使用结束日期（18点判断后的日期）
            return self.cursor_manager.get_end_date_with_time_check(table_name)

        elif cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_DAILY_NATURAL:
            # 使用今天日期
            return datetime.now().strftime('%Y%m%d')

        elif cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_YEARLY:
            # 使用当前年份
            return str(datetime.now().year)

        elif cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_NONE:
            # 无游标，标记为completed
            return 'completed'

        return ''

    def stop(self):
        """停止数据拉取"""
        self.fetch_enabled = False
        self.logger.info("数据拉取已停止")

    def resume(self):
        """恢复数据拉取"""
        self.fetch_enabled = True
        self.logger.info("数据拉取已恢复")

    def get_status(self) -> Dict:
        """
        获取数据拉取状态（用于Dashboard展示）

        Returns:
            状态字典
        """
        cursors = self.cursor_manager.get_all_cursors()

        status_by_strategy = {}
        for cursor in cursors:
            strategy = cursor['cursor_strategy']
            if strategy not in status_by_strategy:
                status_by_strategy[strategy] = []

            status_by_strategy[strategy].append(cursor)

        return {
            'fetch_enabled': self.fetch_enabled,
            'trade_calendar_loaded': len(self.trade_calendar),
            'cursors': cursors,
            'status_by_strategy': status_by_strategy
        }