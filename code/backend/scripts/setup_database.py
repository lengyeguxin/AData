#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本

执行SQL schema文件，创建27张数据表和global_cursor表
严格按照database/schemas目录下的SQL文件顺序执行
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import duckdb
from datetime import datetime


def setup_database(db_path: str = "database/adata.db"):
    """
    初始化数据库

    Args:
        db_path: 数据库文件路径
    """
    print("=" * 80)
    print("AData数据库初始化脚本")
    print("=" * 80)
    print(f"数据库路径: {db_path}")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 确保database目录存在
    os.makedirs("database", exist_ok=True)

    # 连接数据库（不存在则创建）
    print("步骤1: 连接数据库...")
    conn = duckdb.connect(db_path)
    print(f"✅ 数据库已连接: {db_path}")
    print()

    # SQL文件列表（按顺序执行）
    schema_files = [
        "database/schemas/global_cursor_schema.sql",
        "database/schemas/p0_schema.sql",
        "database/schemas/p1_schema.sql",
        "database/schemas/p2_schema.sql"
    ]

    # 执行SQL文件
    print("步骤2: 执行SQL schema文件...")
    for schema_file in schema_files:
        print(f"  执行: {schema_file}")

        if not os.path.exists(schema_file):
            print(f"  ❌ 文件不存在: {schema_file}")
            continue

        # 读取SQL文件
        with open(schema_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # 执行SQL（DuckDB支持多语句）
        try:
            conn.execute(sql_content)
            print(f"  ✅ 执行成功")
        except Exception as e:
            print(f"  ❌ 执行失败: {e}")
            conn.close()
            return False

    print()

    # 验证表创建
    print("步骤3: 验证表创建...")
    tables_result = conn.execute("SHOW TABLES").fetchall()
    tables_created = [table[0] for table in tables_result]

    print(f"  已创建表数: {len(tables_created)}")

    # 预期表列表（27张数据表 + 1张global_cursor表）
    expected_tables = [
        # P0基础（6张）
        'trade_calendar', 'stock_basic', 'index_basic', 'ths_index_basic',
        'etf_basic', 'etf_index',

        # P1行情（7张）
        'stock_daily', 'stock_daily_basic', 'stock_weekly', 'stock_monthly',
        'index_daily', 'etf_daily', 'etf_adj_factor',

        # P2财务（7张）
        'fina_indicator', 'income', 'balancesheet', 'cashflow',
        'express', 'express_brief', 'dividend',

        # P3资金流向(THS)（3张）
        'ths_moneyflow', 'ths_concept_moneyflow', 'ths_industry_moneyflow',

        # P3概念板块（2张）
        'ths_concept_member', 'ths_index_daily',

        # P4游资（2张）
        'hots_user', 'hots_trader_detail',

        # 游标表
        'global_cursor'
    ]

    print(f"  预期表数: {len(expected_tables)}")

    # 检查缺失表
    missing_tables = []
    for table in expected_tables:
        if table not in tables_created:
            missing_tables.append(table)

    if missing_tables:
        print(f"  ❌ 缺失表: {missing_tables}")
        conn.close()
        return False
    else:
        print(f"  ✅ 所有表已创建")

    print()

    # 验证global_cursor表初始化
    print("步骤4: 验证global_cursor表初始化...")
    cursor_count = conn.execute("SELECT COUNT(*) FROM global_cursor").fetchone()[0]
    print(f"  游标记录数: {cursor_count}")

    if cursor_count != 27:
        print(f"  ❌ 游标记录数不正确（预期27，实际{cursor_count}）")
        conn.close()
        return False
    else:
        print(f"  ✅ 游标记录已初始化（27条）")

    print()

    # 显示游标状态
    print("步骤5: 显示游标状态（部分）...")
    cursors_result = conn.execute("""
        SELECT table_name, cursor_strategy, status
        FROM global_cursor
        LIMIT 10
    """).fetchall()

    print("  前10条游标记录:")
    for row in cursors_result:
        print(f"    - {row[0]}: strategy={row[1]}, status={row[2]}")

    print()

    # 关闭连接
    conn.close()

    print("=" * 80)
    print("✅ 数据库初始化完成")
    print("=" * 80)
    print()

    # 生成测试报告
    generate_test_report(db_path, tables_created, cursor_count)

    return True


def generate_test_report(db_path: str, tables_created: list, cursor_count: int):
    """
    生成测试报告（保存到/tmp）

    Args:
        db_path: 数据库路径
        tables_created: 已创建的表列表
        cursor_count: 游标记录数
    """
    report_path = "/tmp/adata_setup_report.txt"

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("AData数据库初始化测试报告\n")
        f.write("=" * 80 + "\n")
        f.write(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"数据库路径: {db_path}\n")
        f.write("\n")

        f.write("测试结果:\n")
        f.write(f"✅ 已创建表数: {len(tables_created)}\n")
        f.write(f"✅ 游标记录数: {cursor_count}\n")
        f.write("\n")

        f.write("已创建表列表:\n")
        for table in tables_created:
            f.write(f"  - {table}\n")

        f.write("\n")
        f.write("=" * 80 + "\n")
        f.write("测试状态: PASSED\n")
        f.write("=" * 80 + "\n")

    print(f"📋 测试报告已生成: {report_path}")
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="初始化AData数据库")
    parser.add_argument("--db-path", default="database/adata.db", help="数据库文件路径")

    args = parser.parse_args()

    success = setup_database(args.db_path)

    if not success:
        print("❌ 数据库初始化失败")
        sys.exit(1)
    else:
        print("✅ 数据库初始化成功，请查看测试报告: /tmp/adata_setup_report.txt")
        sys.exit(0)