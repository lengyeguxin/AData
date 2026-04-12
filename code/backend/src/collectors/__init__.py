"""
Collector模块初始化

提供所有Collector类的导入入口
"""

from src.collectors.base_collector import BaseCollector
from src.collectors.stock_basic_collector import StockBasicCollector
from src.collectors.trade_calendar_collector import TradeCalendarCollector
from src.collectors.daily_collector import DailyCollector
from src.collectors.income_collector import IncomeCollector


__all__ = [
    'BaseCollector',
    'StockBasicCollector',
    'TradeCalendarCollector',
    'DailyCollector',
    'IncomeCollector'
]