"""
格式化工具函数

提供各种数据格式化和处理功能
"""

from typing import Dict


def extract_column_comments(create_statement: str) -> Dict[str, str]:
    """
    从CREATE TABLE语句中提取字段注释

    Args:
        create_statement: CREATE TABLE SQL语句

    Returns:
        字段注释字典 {column_name: comment}

    Example:
        CREATE TABLE stock_daily (
            ts_code VARCHAR(10),
            trade_date DATE,

            -- 未复权数据
            open REAL,  -- 开盘价
            high REAL,  -- 最高价
        )

        返回: {'open': '开盘价', 'high': '最高价'}
    """
    comments = {}
    lines = create_statement.split('\n')
    current_column = None

    for i, line in enumerate(lines):
        line = line.strip()

        # 检测字段行（包含类型定义的行）
        if any(type_keyword in line for type_keyword in ['VARCHAR', 'REAL', 'INTEGER', 'BOOLEAN', 'TEXT', 'DATE', 'TIMESTAMP']):
            # 提取字段名
            parts = line.split()
            if parts:
                column_name = parts[0].replace(',', '').strip()
                if column_name and not column_name.startswith('--'):
                    current_column = column_name

                    # 检查行尾是否有注释
                    if '--' in line:
                        comment_part = line.split('--')[-1].strip()
                        if comment_part:
                            comments[column_name] = comment_part

        # 检测单独的注释行（注释在下一行）
        elif line.startswith('--') and current_column:
            # 检查是否是字段注释（不是类别注释）
            comment = line.replace('--', '').strip()
            # 过滤掉类别注释（如"-- 未复权数据"）
            if comment and not comment.endswith('数据') and not comment.endswith('指标'):
                if current_column not in comments:  # 避免覆盖行尾注释
                    comments[current_column] = comment

    return comments


def format_number(num: int) -> str:
    """
    格式化数字（添加千位分隔符）

    Args:
        num: 数字

    Returns:
        格式化后的字符串
    """
    if num >= 100000000:  # 1亿
        return f"{num / 100000000:.2f}亿"
    elif num >= 10000:  # 1万
        return f"{num / 10000:.2f}万"
    else:
        return f"{num:,}"


def format_size(size_mb: float) -> str:
    """
    格式化存储大小

    Args:
        size_mb: MB大小

    Returns:
        格式化后的字符串
    """
    if size_mb >= 1024:  # 1GB
        return f"{size_mb / 1024:.2f} GB"
    else:
        return f"{size_mb:.2f} MB"