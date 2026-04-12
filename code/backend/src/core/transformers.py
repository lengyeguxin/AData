"""
数据转换工具

提供通用的数据转换功能，如日期格式转换
"""

from datetime import datetime
from typing import Optional


def convert_date_format(date_str: Optional[str]) -> Optional[str]:
    """
    转换日期格式（YYYYMMDD → YYYY-MM-DD）

    Args:
        date_str: 日期字符串（YYYYMMDD或YYYY-MM-DD格式）

    Returns:
        YYYY-MM-DD格式的日期字符串

    示例：
        convert_date_format('20260409') → '2026-04-09'
        convert_date_format('2026-04-09') → '2026-04-09'
        convert_date_format(None) → None
    """
    if not date_str:
        return None

    # 如果已经是YYYY-MM-DD格式，直接返回
    if '-' in date_str:
        return date_str

    # YYYYMMDD格式转YYYY-MM-DD
    try:
        if len(date_str) == 8:
            year = date_str[:4]
            month = date_str[4:6]
            day = date_str[6:8]
            return f"{year}-{month}-{day}"
        elif len(date_str) == 6:
            # YYYYMM格式转YYYY-MM
            year = date_str[:4]
            month = date_str[4:6]
            return f"{year}-{month}"
        elif len(date_str) == 4:
            # YYYY格式
            return date_str
    except Exception:
        pass

    # 无法转换，返回原值
    return date_str


def convert_date_to_yyyymmdd(date_obj: datetime) -> str:
    """
    将datetime对象转换为YYYYMMDD格式

    Args:
        date_obj: datetime对象

    Returns:
        YYYYMMDD格式的日期字符串

    示例：
        convert_date_to_yyyymmdd(datetime(2026, 4, 9)) → '20260409'
    """
    return date_obj.strftime('%Y%m%d')


def increment_date(date_str: str) -> str:
    """
    日期加1天

    Args:
        date_str: YYYYMMDD格式的日期

    Returns:
        YYYYMMDD格式的日期（加1天）

    示例：
        increment_date('20260409') → '20260410'
    """
    try:
        date_obj = datetime.strptime(date_str, '%Y%m%d')
        next_date = date_obj + timedelta(days=1)
        return next_date.strftime('%Y%m%d')
    except Exception:
        return date_str


from datetime import timedelta