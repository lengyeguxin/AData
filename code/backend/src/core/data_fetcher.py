"""
统一数据拉取控制器

负责协调所有数据表的拉取流程：
- 启动流程：按固定顺序拉取前置表
- 判断进度：读取游标，断点续传
- 数据存在性检查：避免重复爬取
- 18点时间判断：确保数据完整性
- 按优先级顺序拉取：P0 → P1 → P2 → P3 → P4
- 运行状态管理：全局running标志，支持调度器检查
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

    # 全局运行状态标志（类变量，供调度器检查）
    running = False

    # 前置表固定顺序（必须先拉取）
    PRIORITY_ORDER = {
        'P0': [
            'trade_calendar',
            'stock_basic',
            'index_basic',
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
        'P3': [],
        'P4': [
            'hots_user',
            'hots_trader_detail'
        ]
    }

    def __init__(self, db_config: dict, config: Dict):
        """
        初始化数据拉取控制器

        Args:
            db_config: 数据库配置字典
            config: 配置字典
        """
        self.db_config = db_config
        self.config = config
        self.logger = get_logger(__name__)

        # 初始化游标管理器
        self.cursor_manager = GlobalCursorManager(db_config, 'code/backend/config')

        # 数据拉取开关
        self.fetch_enabled = config.get('fetch', {}).get('enabled', True)

        # 重试配置
        self.max_retries = config.get('fetch', {}).get('max_retries', 2)
        self.retry_delay = config.get('fetch', {}).get('retry_delay', 30)
        self.logger.info(f"重试配置: max_retries={self.max_retries}, retry_delay={self.retry_delay}秒")

        # 无数据记录文件路径（database目录下）
        import yaml
        with open('config/table_config.yaml', 'r', encoding='utf-8') as f:
            table_config = yaml.safe_load(f)
        self.financial_tables = [
            table for table, cfg in table_config['tables'].items()
            if cfg.get('cursor_strategy') == 'daily_natural'
        ]

        # 加载交易日历（启动时一次性加载到内存）
        self.trade_calendar = self._load_trade_calendar()

    def start(self):
        """
        启动数据拉取（入口方法）

        流程：
        1. 设置running标志为True（表示正在拉取）
        2. 检查fetch.enabled开关
        3. 加载交易日历到内存
        4. 按优先级顺序拉取（P0 → P1 → P2 → P3 → P4）
        5. 每张表判断游标进度，断点续传
        6. 更新游标（根据策略决定更新时机）
        7. 设置running标志为False（表示拉取完成）
        """
        # 设置运行状态（正在拉取）
        DataFetcher.running = True
        self.logger.info("✓ 数据拉取任务启动（running=True）")

        try:
            if not self.fetch_enabled:
                self.logger.info("数据拉取已禁用（fetch.enabled=false）")
                DataFetcher.running = False
                return

            self.logger.info("=" * 80)
            self.logger.info("数据拉取控制器启动")
            self.logger.info("=" * 80)
            self.logger.info(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.logger.info(f"数据库: {self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}")
            self.logger.info(f"交易日历已加载: {len(self.trade_calendar)}个交易日")
            self.logger.info("")

            # 按优先级顺序拉取所有表
            self._fetch_all_tables()

        except Exception as e:
            self.logger.error(f"数据拉取异常: {e}")
            # 异常情况下也要设置running=False，避免调度器一直跳过
            DataFetcher.running = False
            self.logger.info("✗ 数据拉取异常终止（running=False）")
            raise

        finally:
            # 确保无论如何都设置running=False（拉取完成）
            DataFetcher.running = False
            self.logger.info("✓ 数据拉取任务完成（running=False）")

    def _load_trade_calendar(self) -> List[str]:
        """
        加载交易日历到内存（启动时一次性加载）

        Returns:
            交易日列表（YYYY-MM-DD格式）
        """
        query = """
            SELECT cal_date
            FROM trade_calendar
            WHERE is_open = '1'
            ORDER BY cal_date
        """

        try:
            # 使用Database类统一管理连接
            from src.core.database import Database
            db = Database(self.db_config)
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

        # P0完成后，重新加载交易日历（trade_calendar表在运行时才拉取数据）
        self.logger.info("P0前置表完成，重新加载交易日历...")
        self.trade_calendar = self._load_trade_calendar()

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
            fetch_time = cursor.get('fetch_after_time', 'N/A')
            self.logger.info(
                f"{table_name}: 未到拉取时间或游标已最新"
                f"(cursor={cursor['cursor_value']}, status={cursor['status']}, fetch_after={fetch_time})"
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

            else:
                self.logger.error(f"{table_name}: 未知的游标策略 {cursor_strategy}")
                self.cursor_manager.mark_failed(table_name, "未知的游标策略")
                return

            # 5. 更新游标状态（按批次拉取的策略已内部更新游标值）
            # DAILY_TRADE和DAILY_NATURAL策略：每批次已更新游标，只需标记success
            # 其他策略：需要一次性更新游标
            if cursor_strategy in [GlobalCursorManager.CURSOR_STRATEGY_DAILY_TRADE,
                                   GlobalCursorManager.CURSOR_STRATEGY_DAILY_NATURAL]:
                # 按批次拉取的策略已内部更新游标，只需标记为success
                # 获取当前游标值（已由策略方法更新）
                cursor = self.cursor_manager.get_cursor(table_name)
                self.logger.info(
                    f"{table_name}: 拉取完成，游标已更新为 {cursor['cursor_value']}"
                    f"(共{record_count}条记录)"
                )
                # mark_success会自动设置status=success（游标值已在策略中更新）
                self.cursor_manager.update_cursor(
                    table_name, cursor['cursor_value'], record_count
                )
            else:
                # NONE/YEARLY/SPECIAL策略：需要一次性更新游标
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
        无游标策略（全量拉取，带重试）

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

        # 使用重试机制拉取
        def fetch_none():
            # 不同表的拉取参数不同
            if table_name == 'stock_basic':
                return collector.run()
            elif table_name == 'trade_calendar':
                # 拉取当年数据
                current_year = datetime.now().year
                return collector.run_year(current_year)
            elif table_name == 'index_basic':
                return collector.run()
            elif table_name == 'etf_basic':
                return collector.run()
            elif table_name == 'hots_user':
                return collector.run()
            else:
                # 默认全量拉取
                return collector.run()

        count = self._retry_fetch_none(table_name, fetch_none)

        if count is not None:
            self.logger.info(f"{table_name}: 全量拉取成功 ({count}条记录)")
            return count
        else:
            # 重试失败
            self.logger.error(f"{table_name}: 全量拉取失败，重试{self.max_retries}次后仍然失败")
            raise Exception(f"{table_name}: 全量拉取失败，重试{self.max_retries}次后仍然失败")

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

        # 5. 遍历交易日拉取，每拉取成功一个立即更新游标
        total_count = 0

        # 特殊处理：周线和月线的去重拉取
        if table_name == 'stock_weekly':
            last_date = None  # 记录上次拉取的周五日期

            for trade_date in trade_dates:
                # 计算本周五日期
                friday_date = self._get_friday_date(trade_date)

                # 如果周五日期小于等于last_date，表示本周数据已拉取，跳过
                if last_date and friday_date <= last_date:
                    self.logger.info(
                        f"{table_name}: {trade_date} (周五{friday_date}) 已处理，跳过"
                    )
                    continue

                # 使用重试机制拉取
                def fetch_weekly():
                    return collector.run(trade_date=friday_date)

                count = self._retry_fetch(
                    table_name, trade_date,
                    fetch_weekly,
                    date_type='trade_date'
                )

                if count is not None:
                    # 拉取成功
                    total_count += count
                    # 更新游标到当前交易日，记录last_date
                    self.cursor_manager.update_cursor(table_name, trade_date, count)
                    self.logger.info(f"{table_name}: 游标更新为 {trade_date}")
                    last_date = friday_date
                else:
                    # 重试后仍然失败，停止拉取后续日期
                    self.logger.error(f"{table_name}: {trade_date} 拉取失败，停止拉取后续日期")
                    break

        elif table_name == 'stock_monthly':
            last_date = None  # 记录上次拉取的月末日期

            for trade_date in trade_dates:
                # 计算本月末日期
                month_end_date = self._get_month_end_date(trade_date)

                # 如果月末日期小于等于last_date，表示本月数据已拉取，跳过
                if last_date and month_end_date <= last_date:
                    self.logger.info(
                        f"{table_name}: {trade_date} (月末{month_end_date}) 已处理，跳过"
                    )
                    continue

                # 使用重试机制拉取
                def fetch_monthly():
                    return collector.run(trade_date=month_end_date)

                count = self._retry_fetch(
                    table_name, trade_date,
                    fetch_monthly,
                    date_type='trade_date'
                )

                if count is not None:
                    # 拉取成功
                    total_count += count
                    # 更新游标到当前交易日，记录last_date
                    self.cursor_manager.update_cursor(table_name, trade_date, count)
                    self.logger.info(f"{table_name}: 游标更新为 {trade_date}")
                    last_date = month_end_date
                else:
                    # 重试后仍然失败，停止拉取后续日期
                    self.logger.error(f"{table_name}: {trade_date} 拉取失败，停止拉取后续日期")
                    break

        else:
            # 普通表：正常遍历每个交易日
            for trade_date in trade_dates:
                # 使用重试机制拉取
                def fetch_daily():
                    # index_daily特殊处理：使用run_by_date方法
                    if table_name == 'index_daily':
                        return collector.run_by_date(trade_date=trade_date)
                    else:
                        return collector.run(trade_date=trade_date)

                count = self._retry_fetch(
                    table_name, trade_date,
                    fetch_daily,
                    date_type='trade_date'
                )

                if count is not None:
                    # 拉取成功
                    total_count += count
                    if count > 0:
                        self.logger.info(f"{table_name}: {trade_date} 拉取成功 ({count}条)")
                    elif count == 0:
                        # 无数据但不算失败（同花顺和游资早期可能没有数据）
                        # _retry_fetch已记录到no_data_dates.json并返回0，这里只需更新游标
                        self.cursor_manager.update_cursor(table_name, trade_date, 0)
                        self.logger.info(f"{table_name}: 游标更新为 {trade_date}（无数据，已记录）")
                        continue
                    # 每拉取成功一个批次，立即更新游标到该日期
                    self.cursor_manager.update_cursor(table_name, trade_date, count)
                    self.logger.info(f"{table_name}: 游标更新为 {trade_date}")
                else:
                    # 重试后仍然失败，停止拉取后续日期
                    self.logger.error(f"{table_name}: {trade_date} 拉取失败，停止拉取后续日期")
                    break

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

        # 4. 遍历自然日拉取，每拉取成功一个立即更新游标
        total_count = 0
        current_date = datetime.strptime(start_date, '%Y%m%d')
        end_datetime = datetime.strptime(end_date, '%Y%m%d')

        while current_date <= end_datetime:
            date_str = current_date.strftime('%Y%m%d')

            # 使用重试机制拉取（财务表允许无数据）
            def fetch_financial():
                if table_name in ['income', 'balancesheet', 'cashflow']:
                    return collector.run(ann_date=date_str, report_type='1')
                else:
                    return collector.run(ann_date=date_str)

            count = self._retry_fetch(
                table_name, date_str,
                fetch_financial,
                date_type='ann_date'
            )

            if count is not None:
                # 拉取成功（包括无数据）
                total_count += count
                # 每拉取成功一个批次，立即更新游标到该日期（财务表允许无数据更新）
                self.cursor_manager.update_cursor(table_name, date_str, count)
                self.logger.info(f"{table_name}: 游标更新为 {date_str}")
            else:
                # 重试后仍然失败（异常），不更新游标，下次从失败日期重新开始
                self.logger.error(f"{table_name}: {date_str} 拉取失败，停止拉取后续日期")
                break

            current_date += timedelta(days=1)

        return total_count

    def _fetch_yearly_strategy(self, table_name: str) -> int:
        """
        按年策略（增量拉取，带重试）

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

        # 使用重试机制拉取
        def fetch_yearly():
            if table_name == 'trade_calendar':
                return collector.run_year(int(next_year))
            else:
                return collector.run(year=int(next_year))

        count = self._retry_fetch_none(table_name, fetch_yearly)

        if count is not None:
            # 对于 yearly 策略，游标应该更新为拉取的年份，而不是当前年份
            new_cursor = next_year  # 使用拉取的年份，而不是当前年份
            self.cursor_manager.update_cursor(table_name, new_cursor, count)
            self.logger.info(f"{table_name}: {next_year}年 拉取成功 ({count}条)，游标更新为 {new_cursor}")
            return count
        else:
            #. 重试失败
            self.logger.error(f"{table_name}: {next_year}年 拉取失败，重试{self.max_retries}次后仍然失败")
            raise Exception(f"{table_name}: {next_year}年 拉取失败，重试{self.max_retries}次后仍然失败")

    def _get_collector(self, table_name: str):
        """
        根据表名获取对应的Collector实例

        Args:
            table_name: 表名

        Returns:
            Collector实例
        """
        # 直接映射：表名 → (模块名, 类名)
        COLLECTOR_MAP = {
            'stock_daily': ('daily_collector', 'DailyCollector'),
            'stock_daily_basic': ('stock_daily_basic_collector', 'StockDailyBasicCollector'),
            'stock_weekly': ('weekly_collector', 'WeeklyCollector'),
            'stock_monthly': ('monthly_collector', 'MonthlyCollector'),
            'stock_basic': ('stock_basic_collector', 'StockBasicCollector'),
            'trade_calendar': ('trade_calendar_collector', 'TradeCalendarCollector'),
            'index_basic': ('index_basic_collector', 'IndexBasicCollector'),
            'index_daily': ('index_daily_collector', 'IndexDailyCollector'),
            'etf_basic': ('etf_basic_collector', 'ETFBasicCollector'),
            'etf_daily': ('etf_daily_collector', 'ETFDailyCollector'),
            'etf_adj_factor': ('etf_adj_factor_collector', 'ETFAdjFactorCollector'),
            'etf_index': ('etf_index_collector', 'ETFIndexCollector'),
            'fina_indicator': ('fina_indicator_collector', 'FinaIndicatorCollector'),
            'income': ('income_collector', 'IncomeCollector'),
            'balancesheet': ('balancesheet_collector', 'BalancesheetCollector'),
            'cashflow': ('cashflow_collector', 'CashflowCollector'),
            'dividend': ('dividend_collector', 'DividendCollector'),
            'express': ('express_collector', 'ExpressCollector'),
            'express_brief': ('express_brief_collector', 'ExpressBriefCollector'),
            'hots_user': ('hots_user_collector', 'HotsUserCollector'),
            'hots_trader_detail': ('hots_trader_detail_collector', 'HotsTraderDetailCollector'),
        }

        collector_info = COLLECTOR_MAP.get(table_name)

        if not collector_info:
            self.logger.warning(f"{table_name}: 未在映射表中找到Collector")
            return None

        module_name, class_name = collector_info

        # 动态导入Collector
        try:
            import importlib

            # 导入模块
            module = importlib.import_module(f'src.collectors.{module_name}')

            # 获取类
            collector_class = getattr(module, class_name)

            # 创建实例（需要db_config和api）
            # 从config获取tushare配置，创建API实例
            from src.core.tushare_api import TushareAPI
            api = TushareAPI(self.config['tushare'])

            # 创建Collector实例
            collector = collector_class(self.db_config, api)

            return collector

        except Exception as e:
            self.logger.error(f"{table_name}: 导入Collector失败 (模块: {module_name}, 类: {class_name}): {e}")
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

    def _get_friday_date(self, date_str: str) -> str:
        """
        计算某天所在周的周五日期

        Args:
            date_str: 日期字符串（YYYYMMDD）

        Returns:
            周五日期（YYYYMMDD）
        """
        dt = datetime.strptime(date_str, '%Y%m%d')
        days_to_friday = 4 - dt.weekday()  # weekday(): 周一=0, 周五=4
        friday_dt = dt + timedelta(days=days_to_friday)
        return friday_dt.strftime('%Y%m%d')

    def _get_month_end_date(self, date_str: str) -> str:
        """
        计算某天所在月的月末日期

        Args:
            date_str: 日期字符串（YYYYMMDD）

        Returns:
            月末日期（YYYYMMDD）
        """
        dt = datetime.strptime(date_str, '%Y%m%d')
        if dt.month == 12:
            next_month_first = datetime(dt.year + 1, 1, 1)

        else:
            next_month_first = datetime(dt.year, dt.month + 1, 1)
        month_end_dt = next_month_first - timedelta(days=1)
        return month_end_dt.strftime('%Y%m%d')

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
            db = Database(self.db_config)
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
        计算新的游标值（仅用于NONE/YEARLY/SPECIAL策略）

        注意：DAILY_TRADE和DAILY_NATURAL策略已在策略方法内部按批次更新游标，
        不使用此方法。

        Args:
            table_name: 表名
            cursor_strategy: 游标策略

        Returns:
            新的游标值
        """
        if cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_YEARLY:
            # 使用当前年份
            return str(datetime.now().year)

        elif cursor_strategy == GlobalCursorManager.CURSOR_STRATEGY_NONE:
            # 无游标，标记为completed
            return 'completed'

        # DAILY_TRADE和DAILY_NATURAL不应使用此方法
        # 如果被调用，返回空字符串（不会发生）
        return ''

    def _record_no_data_date(self, table_name: str, date_str: str):
        """
        记录财务表无数据的日期到文件

        Args:
            table_name: 表名
            date_str: 日期（YYYYMMDD）
        """
        import json

        # 统一日期格式为YYYY-MM-DD
        date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

        # 无数据记录文件路径（database目录下）
        no_data_file = Path('database/no_data_dates.json')

        # 加载现有记录
        try:
            if no_data_file.exists():
                with open(no_data_file, 'r', encoding='utf-8') as f:
                    records = json.load(f)
            else:
                records = {}
        except Exception as e:
            self.logger.warning(f"加载无数据记录失败: {e}")
            records = {}

        # 初始化表记录
        if table_name not in records:
            records[table_name] = []

        # 添加日期（去重）
        if date_formatted not in records[table_name]:
            records[table_name].append(date_formatted)

            # 按日期排序
            records[table_name].sort()

            # 保存
            try:
                with open(no_data_file, 'w', encoding='utf-8') as f:
                    json.dump(records, f, ensure_ascii=False, indent=2)
            except Exception as e:
                self.logger.error(f"保存无数据记录失败: {e}")
                return

            # 记录INFO日志（而不是WARNING，因为这是正常情况）
            self.logger.info(
                f"{table_name}: {date_str} 无数据（重试{self.max_retries+1}次后），"
                f"已记录到 no_data_dates.json，继续拉取后续日期"
            )

    def _retry_fetch_none(self, table_name: str, fetch_func) -> Optional[int]:
        """
        带重试机制的基础表拉取（无游标、按年、特殊策略）

        Args:
            table_name: 表名
            fetch_func: 拉取函数（返回记录数）

        Returns:
            拉取的记录数（成功），None（失败）
        """
        import time

        for attempt in range(self.max_retries + 1):
            try:
                count = fetch_func()

                # 检查返回值
                if count is None:
                    # 返回 None 表示失败
                    if attempt < self.max_retries:
                        self.logger.warning(
                            f"{table_name}: 拉取返回None，重试 {attempt + 1}/{self.max_retries + 1}"
                        )
                        time.sleep(self.retry_delay)
                    else:
                        # 重试后仍然失败
                        self.logger.error(
                            f"{table_name}: 重试{self.max_retries + 1}次后仍然失败"
                        )
                        return None
                elif count > 0:
                    self.logger.info(
                        f"{table_name}: 拉取成功 ({count}条记录)"
                    )
                    return count
                else:
                    # 无数据的情况
                    if attempt < self.max_retries:
                        self.logger.warning(
                            f"{table_name}: 返回空数据，重试 {attempt+1}/{self.max_retries+1}"
                        )
                        time.sleep(self.retry_delay)
                    else:
                        # 重试后仍然无数据
                        self.logger.error(
                            f"{table_name}: 重试{self.max_retries+1}次后仍然无数据"
                        )
                        return None

            except Exception as e:
                if attempt < self.max_retries:
                    self.logger.warning(
                        f"{table_name}: 拉取失败: {e},尝试 {attempt+1}/{self.max_retries+1}"
                    )
                    time.sleep(self.retry_delay)
                else:
                    # 重试后仍然失败
                    self.logger.error(
                        f"{table_name}: 重试{self.max_retries+1}次后仍然失败: {e}"
                    )
                    return None

        return None

    def _retry_fetch(self, table_name: str, date_str: str, fetch_func, date_type: str = 'trade_date') -> Optional[int]:
        """
        带重试机制的数据拉取（按交易日/自然日策略）

        Args:
            table_name: 表名
            date_str: 日期字符串
            fetch_func: 拉取函数（返回记录数）
            date_type: 日期类型（trade_date 或 ann_date）

        Returns:
            拉取的记录数（成功），None（失败）
        """
        import time

        for attempt in range(self.max_retries + 1):
            try:
                count = fetch_func()

                # 检查是否有数据
                if count > 0:
                    self.logger.info(f"{table_name}: {date_str} 拉取成功 ({count}条)")
                    return count
                else:
                    # 无数据的情况
                    if date_type == 'trade_date':
                        # 行情表无数据：检查是否是允许无数据的特殊表
                        special_tables = ['hots_trader_detail']

                        if table_name in special_tables:
                            # 特殊表允许无数据（早期可能无数据），记录并返回0
                            self._record_no_data_date(table_name, date_str)
                            return 0

                        # 其他行情表无数据是异常
                        if attempt < self.max_retries:
                            self.logger.warning(
                                f"{table_name}: {date_str} 返回空数据，重试 {attempt+1}/{self.max_retries+1}"
                            )
                            time.sleep(self.retry_delay)
                            continue
                        else:
                            # 重试后仍然无数据
                            self.logger.error(
                                f"{table_name}: {date_str} 重试{self.max_retries+1}次后仍然无数据"
                            )
                            return None
                    else:
                        # 财务表无数据，记录到文件并返回0
                        self._record_no_data_date(table_name, date_str)
                        return 0

            except Exception as e:
                if attempt < self.max_retries:
                    self.logger.warning(
                        f"{table_name}: {date_str} 拉取失败: {e}, 重试 {attempt + 1}/{self.max_retries + 1}"
                    )
                    time.sleep(self.retry_delay)
                else:
                    # 重试后仍然失败
                    self.logger.error(
                        f"{table_name}: {date_str} 重试{self.max_retries + 1}次后仍然失败: {e}"
                    )
                    return None

        return None

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