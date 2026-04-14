#!/usr/bin/env python3
"""
DuckDB数据查看工具

用途：快速查看adata.db中的数据，无需安装额外工具

功能：
1. 表列表查看
2. 单表数据查询（支持WHERE条件）
3. 数据导出CSV
4. 自定义SQL查询

使用示例：
    # 查看所有表
    python3 scripts/view_duckdb_data.py --list-tables

    # 查看stock_daily最新10条
    python3 scripts/view_duckdb_data.py --table stock_daily --limit 10

    # 查看特定股票数据
    python3 scripts/view_duckdb_data.py --table stock_daily --where "ts_code='000001.SZ'" --limit 20

    # 自定义SQL查询
    python3 scripts/view_duckdb_data.py --sql "SELECT ts_code, COUNT(*) FROM stock_daily GROUP BY ts_code ORDER BY COUNT(*) DESC LIMIT 10"

    # 导出数据到CSV
    python3 scripts/view_duckdb_data.py --table stock_daily --export stock_daily.csv
"""

import argparse
import duckdb
import sys
import csv
from pathlib import Path
from typing import List, Tuple

# 数据库路径
DB_PATH = '/home/my/claude-project/AData/database/adata.db'

def print_table(rows: List[Tuple], headers: List[str] = None):
    """格式化打印表格数据"""
    if not rows:
        print("无数据")
        return

    # 如果没有提供headers，使用第一条记录的字段名（如果有的话）
    if headers is None:
        headers = [f"列{i}" for i in range(len(rows[0]))]

    # 计算列宽
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val) if val is not None else 'NULL'))

    # 打印表头
    header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print("-" * len(header_line))

    # 打印数据行
    for row in rows:
        row_line = " | ".join(str(val if val is not None else 'NULL').ljust(col_widths[i]) for i, val in enumerate(row))
        print(row_line)

def list_tables(conn: duckdb.DuckDBPyConnection):
    """列出所有表及其基本信息"""
    print("=" * 80)
    print("所有表列表")
    print("=" * 80)

    query = """
        SELECT
            table_name,
            estimated_size as record_count
        FROM duckdb_tables()
        ORDER BY estimated_size DESC
    """

    result = conn.execute(query).fetchall()
    headers = ['表名', '估计记录数']

    print_table(result, headers)

    print(f"\n总表数: {len(result)}")

def view_table(conn: duckdb.DuckDBPyConnection, table_name: str, limit: int = 20, where: str = None, order_by: str = None):
    """查看单表数据"""
    print("=" * 80)
    print(f"表: {table_name}")
    print("=" * 80)

    # 构建查询
    query = f"SELECT * FROM {table_name}"

    if where:
        query += f" WHERE {where}"

    if order_by:
        query += f" ORDER BY {order_by}"
    else:
        # 尝试自动排序（如果有日期字段）
        try:
            schema = conn.execute(f"DESCRIBE {table_name}").fetchall()
            date_fields = ['trade_date', 'ann_date', 'cal_date', 'end_date', 'list_date']
            for field in date_fields:
                if any(col[0] == field for col in schema):
                    query += f" ORDER BY {field} DESC"
                    break
        except:
            pass

    query += f" LIMIT {limit}"

    try:
        result = conn.execute(query).fetchall()

        # 获取列名
        schema = conn.execute(f"DESCRIBE {table_name}").fetchall()
        headers = [col[0] for col in schema]

        print_table(result, headers)

        print(f"\n显示记录数: {len(result)}")

        # 显示总记录数
        count_query = f"SELECT COUNT(*) FROM {table_name}"
        if where:
            count_query += f" WHERE {where}"
        total_count = conn.execute(count_query).fetchone()[0]
        print(f"总记录数: {total_count}")

    except Exception as e:
        print(f"查询失败: {e}")

def execute_sql(conn: duckdb.DuckDBPyConnection, sql: str):
    """执行自定义SQL查询"""
    print("=" * 80)
    print("自定义SQL查询")
    print("=" * 80)
    print(f"SQL: {sql}")
    print("=" * 80)

    try:
        result = conn.execute(sql).fetchall()

        # 尝试获取列名
        try:
            # DuckDB执行查询后无法直接获取列名，需要解析SQL
            # 简化处理：使用默认列名
            headers = [f"列{i}" for i in range(len(result[0]) if result else 0)]
        except:
            headers = None

        print_table(result, headers)
        print(f"\n返回记录数: {len(result)}")

    except Exception as e:
        print(f"SQL执行失败: {e}")

def export_csv(conn: duckdb.DuckDBPyConnection, table_name: str, output_file: str, where: str = None, limit: int = None):
    """导出数据到CSV"""
    print("=" * 80)
    print(f"导出数据到CSV: {output_file}")
    print("=" * 80)

    query = f"SELECT * FROM {table_name}"

    if where:
        query += f" WHERE {where}"

    if order_by:
        query += f" ORDER BY {order_by}"

    if limit:
        query += f" LIMIT {limit}"

    try:
        result = conn.execute(query).fetchall()

        # 获取列名
        schema = conn.execute(f"DESCRIBE {table_name}").fetchall()
        headers = [col[0] for col in schema]

        # 写入CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(result)

        print(f"✓ 成功导出 {len(result)} 条记录到 {output_file}")
        print(f"文件路径: {Path(output_file).absolute()}")

    except Exception as e:
        print(f"导出失败: {e}")

def show_table_stats(conn: duckdb.DuckDBPyConnection, table_name: str):
    """显示表的统计信息"""
    print("=" * 80)
    print(f"表统计信息: {table_name}")
    print("=" * 80)

    try:
        # 表结构
        schema = conn.execute(f"DESCRIBE {table_name}").fetchall()
        print("\n表结构:")
        print_table(schema, ['列名', '类型', '可空', '主键'])

        # 记录数
        count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"\n总记录数: {count}")

        # 尝试显示最新/最旧数据时间
        date_fields = ['trade_date', 'ann_date', 'cal_date', 'end_date', 'list_date']
        for field in date_fields:
            if any(col[0] == field for col in schema):
                min_date = conn.execute(f"SELECT MIN({field}) FROM {table_name}").fetchone()[0]
                max_date = conn.execute(f"SELECT MAX({field}) FROM {table_name}").fetchone()[0]
                print(f"\n{field}范围: {min_date} ~ {max_date}")
                break

    except Exception as e:
        print(f"统计信息查询失败: {e}")

def main():
    parser = argparse.ArgumentParser(description='DuckDB数据查看工具')
    parser.add_argument('--db', default=DB_PATH, help='数据库路径')
    parser.add_argument('--list-tables', action='store_true', help='列出所有表')
    parser.add_argument('--table', help='指定表名')
    parser.add_argument('--limit', type=int, default=20, help='显示记录数限制')
    parser.add_argument('--where', help='WHERE条件（例如: ts_code=\'000001.SZ\'）')
    parser.add_argument('--order-by', help='排序字段')
    parser.add_argument('--sql', help='自定义SQL查询')
    parser.add_argument('--export', help='导出CSV文件路径')
    parser.add_argument('--stats', action='store_true', help='显示表统计信息')

    args = parser.parse_args()

    try:
        conn = duckdb.connect(args.db, read_only=True)

        if args.list_tables:
            list_tables(conn)

        elif args.table:
            if args.stats:
                show_table_stats(conn, args.table)
            elif args.export:
                export_csv(conn, args.table, args.export, args.where, args.limit)
            else:
                view_table(conn, args.table, args.limit, args.where, args.order_by)

        elif args.sql:
            execute_sql(conn, args.sql)

        else:
            # 默认：列出所有表
            list_tables(conn)

        conn.close()

    except Exception as e:
        print(f"数据库连接失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()