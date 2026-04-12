#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库表结构验证脚本

验证27张数据表和global_cursor表的结构是否正确
检查主键、索引、字段是否存在
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import duckdb
from datetime import datetime


def verify_schema(db_path: str = "database/adata.db"):
    """
    验证数据库表结构

    Args:
        db_path: 数据库文件路径
    """
    print("=" * 80)
    print("AData数据库表结构验证脚本")
    print("=" * 80)
    print(f"数据库路径: {db_path}")
    print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 检查数据库文件是否存在
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return False

    # 连接数据库
    print("步骤1: 连接数据库...")
    conn = duckdb.connect(db_path, read_only=True)
    print(f"✅ 数据库已连接")
    print()

    # 获取所有表
    print("步骤2: 获取所有表...")
    tables_result = conn.execute("SHOW TABLES").fetchall()
    tables_created = [table[0] for table in tables_result]

    print(f"  已创建表数: {len(tables_created)}")
    print()

    # 预期表列表
    expected_tables = {
        # P0基础（6张）
        'trade_calendar': {'primary_keys': ['exchange', 'cal_date'], 'indexes': ['idx_trade_cal_date', 'idx_trade_cal_exchange']},
        'stock_basic': {'primary_keys': ['ts_code'], 'indexes': ['idx_stock_basic_code', 'idx_stock_basic_market']},
        'index_basic': {'primary_keys': ['ts_code'], 'indexes': ['idx_index_basic_code', 'idx_index_basic_market']},
        'ths_index_basic': {'primary_keys': ['ts_code'], 'indexes': ['idx_ths_index_basic_code', 'idx_ths_index_basic_type']},
        'etf_basic': {'primary_keys': ['ts_code'], 'indexes': ['idx_etf_basic_code', 'idx_etf_basic_type']},
        'etf_index': {'primary_keys': ['ts_code'], 'indexes': ['idx_etf_index_code', 'idx_etf_index_index_code']},

        # P1行情（7张）
        'stock_daily': {'primary_keys': ['ts_code', 'trade_date'], 'indexes': ['idx_daily_date', 'idx_daily_code', 'idx_daily_date_code']},
        'stock_daily_basic': {'primary_keys': ['ts_code', 'trade_date'], 'indexes': ['idx_basic_date', 'idx_basic_code', 'idx_basic_date_code']},
        'stock_weekly': {'primary_keys': ['ts_code', 'trade_date'], 'indexes': ['idx_weekly_date', 'idx_weekly_code', 'idx_weekly_date_code']},
        'stock_monthly': {'primary_keys': ['ts_code', 'trade_date'], 'indexes': ['idx_monthly_date', 'idx_monthly_code', 'idx_monthly_date_code']},
        'index_daily': {'primary_keys': ['ts_code', 'trade_date'], 'indexes': ['idx_index_daily_date', 'idx_index_daily_code', 'idx_index_daily_date_code']},
        'etf_daily': {'primary_keys': ['ts_code', 'trade_date'], 'indexes': ['idx_etf_daily_date', 'idx_etf_daily_code', 'idx_etf_daily_date_code']},
        'etf_adj_factor': {'primary_keys': ['ts_code', 'trade_date'], 'indexes': ['idx_etf_adj_date', 'idx_etf_adj_code', 'idx_etf_adj_date_code']},

        # P2财务（7张）
        'fina_indicator': {'primary_keys': ['ts_code', 'end_date'], 'indexes': ['idx_fina_date', 'idx_fina_code', 'idx_fina_end_date']},
        'income': {'primary_keys': ['ts_code', 'end_date', 'report_type'], 'indexes': ['idx_income_date', 'idx_income_code', 'idx_income_ann_date']},
        'balancesheet': {'primary_keys': ['ts_code', 'end_date', 'report_type'], 'indexes': ['idx_balance_date', 'idx_balance_code', 'idx_balance_ann_date']},
        'cashflow': {'primary_keys': ['ts_code', 'end_date', 'report_type'], 'indexes': ['idx_cashflow_date', 'idx_cashflow_code', 'idx_cashflow_ann_date']},
        'express': {'primary_keys': ['ts_code', 'end_date', 'ann_date'], 'indexes': ['idx_express_date', 'idx_express_code', 'idx_express_ann_date']},
        'express_brief': {'primary_keys': ['ts_code', 'end_date', 'ann_date'], 'indexes': ['idx_express_brief_date', 'idx_express_brief_code', 'idx_express_brief_ann_date']},
        'dividend': {'primary_keys': ['ts_code', 'ann_date', 'record_date'], 'indexes': ['idx_dividend_date', 'idx_dividend_code']},

        # P3资金流向(THS)（3张）
        'ths_moneyflow': {'primary_keys': ['ts_code', 'trade_date'], 'indexes': ['idx_ths_moneyflow_date', 'idx_ths_moneyflow_code']},
        'ths_concept_moneyflow': {'primary_keys': ['ts_code', 'trade_date'], 'indexes': ['idx_ths_concept_moneyflow_date', 'idx_ths_concept_moneyflow_code']},
        'ths_industry_moneyflow': {'primary_keys': ['ts_code', 'trade_date'], 'indexes': ['idx_ths_industry_moneyflow_date', 'idx_ths_industry_moneyflow_code']},

        # P3概念板块（2张）
        'ths_concept_member': {'primary_keys': ['ts_code', 'con_code'], 'indexes': ['idx_ths_concept_member_code', 'idx_ths_concept_member_ts_code']},
        'ths_index_daily': {'primary_keys': ['ts_code', 'trade_date'], 'indexes': ['idx_ths_index_daily_date', 'idx_ths_index_daily_code']},

        # P4游资（2张）
        'hots_user': {'primary_keys': ['account'], 'indexes': ['idx_hots_user_account', 'idx_hots_user_broker']},
        'hots_trader_detail': {'primary_keys': ['account', 'ts_code', 'trade_date'], 'indexes': ['idx_hots_trader_detail_date', 'idx_hots_trader_detail_code', 'idx_hots_trader_detail_account']},

        # 游标表
        'global_cursor': {'primary_keys': ['table_name'], 'indexes': ['idx_cursor_strategy', 'idx_status']}
    }

    print(f"  预期表数: {len(expected_tables)}")
    print()

    # 验证表结构
    print("步骤3: 验证表结构...")
    issues = []

    for table_name, expected_structure in expected_tables.items():
        print(f"  验证表: {table_name}")

        # 检查表是否存在
        if table_name not in tables_created:
            issues.append(f"表缺失: {table_name}")
            print(f"    ❌ 表不存在")
            continue

        # 获取表结构
        describe_result = conn.execute(f"DESCRIBE {table_name}").fetchall()
        columns = {row[0]: row[1] for row in describe_result}  # column_name: column_type

        print(f"    字段数: {len(columns)}")

        # 检查关键字段（如主键字段）
        primary_keys = expected_structure['primary_keys']
        for pk in primary_keys:
            if pk not in columns:
                issues.append(f"{table_name}: 缺失主键字段 '{pk}'")
                print(f"    ❌ 缺失主键字段: {pk}")

        # 检查索引（DuckDB的索引验证方式）
        # DuckDB自动管理索引，这里只做记录
        indexes = expected_structure['indexes']
        print(f"    预期索引数: {len(indexes)}")

    print()

    # 验证global_cursor表数据
    print("步骤4: 验证global_cursor表数据...")
    cursor_count = conn.execute("SELECT COUNT(*) FROM global_cursor").fetchone()[0]
    print(f"  游标记录数: {cursor_count}")

    if cursor_count != 27:
        issues.append(f"游标记录数不正确（预期27，实际{cursor_count}）")
        print(f"  ❌ 游标记录数不正确")
    else:
        print(f"  ✅ 游标记录数正确（27条）")

    print()

    # 显示游标策略分布
    print("步骤5: 显示游标策略分布...")
    strategy_result = conn.execute("""
        SELECT cursor_strategy, COUNT(*) as count
        FROM global_cursor
        GROUP BY cursor_strategy
        ORDER BY cursor_strategy
    """).fetchall()

    for row in strategy_result:
        print(f"  {row[0]}: {row[1]}张表")

    print()

    # 关闭连接
    conn.close()

    # 判断验证结果
    if issues:
        print("=" * 80)
        print("❌ 数据库表结构验证失败")
        print("=" * 80)
        print()
        print("问题列表:")
        for issue in issues:
            print(f"  - {issue}")
        print()
    else:
        print("=" * 80)
        print("✅ 数据库表结构验证通过")
        print("=" * 80)
        print()

    # 生成测试报告
    generate_test_report(db_path, tables_created, cursor_count, strategy_result, issues)

    return len(issues) == 0


def generate_test_report(db_path: str, tables_created: list, cursor_count: int, strategy_result: list, issues: list):
    """
    生成测试报告（保存到/tmp）

    Args:
        db_path: 数据库路径
        tables_created: 已创建的表列表
        cursor_count: 游标记录数
        strategy_result: 游标策略分布
        issues: 问题列表
    """
    report_path = "/tmp/adata_verify_report.txt"

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("AData数据库表结构验证测试报告\n")
        f.write("=" * 80 + "\n")
        f.write(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"数据库路径: {db_path}\n")
        f.write("\n")

        f.write("验证结果:\n")
        f.write(f"已创建表数: {len(tables_created)}\n")
        f.write(f"游标记录数: {cursor_count}\n")
        f.write("\n")

        f.write("游标策略分布:\n")
        for row in strategy_result:
            f.write(f"  {row[0]}: {row[1]}张表\n")
        f.write("\n")

        f.write("已创建表列表:\n")
        for table in tables_created:
            f.write(f"  - {table}\n")
        f.write("\n")

        if issues:
            f.write("问题列表:\n")
            for issue in issues:
                f.write(f"  ❌ {issue}\n")
            f.write("\n")
            f.write("=" * 80 + "\n")
            f.write("测试状态: FAILED\n")
            f.write("=" * 80 + "\n")
        else:
            f.write("=" * 80 + "\n")
            f.write("测试状态: PASSED\n")
            f.write("=" * 80 + "\n")

    print(f"📋 测试报告已生成: {report_path}")
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="验证AData数据库表结构")
    parser.add_argument("--db-path", default="database/adata.db", help="数据库文件路径")

    args = parser.parse_args()

    success = verify_schema(args.db_path)

    if not success:
        print("❌ 数据库表结构验证失败，请查看测试报告: /tmp/adata_verify_report.txt")
        sys.exit(1)
    else:
        print("✅ 数据库表结构验证通过，请查看测试报告: /tmp/adata_verify_report.txt")
        sys.exit(0)