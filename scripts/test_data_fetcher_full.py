#!/usr/bin/env python3
"""
测试DataFetcher完整流程

测试自动化数据拉取功能：
1. 初始化DataFetcher
2. 测试单表拉取（stock_daily、trade_calendar、income）
3. 验证游标更新
4. 验证数据入库
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'code' / 'backend'))

from src.core.data_fetcher import DataFetcher
from src.core.database import Database
import yaml

print("=" * 80)
print("测试DataFetcher完整流程")
print("=" * 80)

# 加载配置
config_path = Path(__file__).parent.parent / 'code' / 'backend' / 'config' / 'config.yaml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

db_path = 'database/adata.db'

# 初始化DataFetcher
print("\n初始化DataFetcher...")
fetcher = DataFetcher(db_path, config)

print(f"✓ DataFetcher初始化成功")
print(f"✓ fetch_enabled: {fetcher.fetch_enabled}")
print(f"✓ trade_calendar loaded: {len(fetcher.trade_calendar)}个交易日")

# 测试1：单表拉取（trade_calendar - 无游标策略）
print("\n" + "=" * 80)
print("测试1：trade_calendar（无游标策略，全量拉取）")
print("=" * 80)

try:
    # 修改游标为pending，触发拉取
    import duckdb
    conn = duckdb.connect(db_path)
    conn.execute("UPDATE global_cursor SET cursor_value=NULL, status='pending' WHERE table_name='trade_calendar'")
    conn.close()

    print("\n触发拉取...")
    fetcher._fetch_table('trade_calendar')

    # 查看游标状态
    db = Database(db_path)
    result = db.execute("SELECT cursor_value, status, last_record_count FROM global_cursor WHERE table_name='trade_calendar'")
    cursor_value, status, count = result[0]

    print(f"\n游标状态:")
    print(f"  cursor_value: {cursor_value}")
    print(f"  status: {status}")
    print(f"  last_record_count: {count}")

    # 查看数据记录数
    result = db.execute("SELECT COUNT(*) FROM trade_calendar WHERE exchange='SSE' OR exchange='SZSE'")
    data_count = result[0][0]
    print(f"\n数据库验证:")
    print(f"  trade_calendar记录数: {data_count}")

    if status == 'success' and data_count > 0:
        print("✓ trade_calendar测试成功")
    else:
        print("⚠ trade_calendar测试异常")

except Exception as e:
    print(f"✗ 测试失败: {e}")

# 测试2：单表拉取（stock_daily - 按交易日策略）
print("\n" + "=" * 80)
print("测试2：stock_daily（按交易日策略，增量拉取）")
print("=" * 80)

try:
    # 设置游标为2026-04-09（拉取2026-04-10）
    import duckdb
    conn = duckdb.connect(db_path)
    conn.execute("UPDATE global_cursor SET cursor_value='20260409', status='pending' WHERE table_name='stock_daily'")
    conn.close()

    print("\n游标设置: 20260409")
    print("预期拉取: 20260410")

    print("\n触发拉取...")
    fetcher._fetch_table('stock_daily')

    # 查看游标状态
    db = Database(db_path)
    result = db.execute("SELECT cursor_value, status, last_record_count FROM global_cursor WHERE table_name='stock_daily'")
    cursor_value, status, count = result[0]

    print(f"\n游标状态:")
    print(f"  cursor_value: {cursor_value}")
    print(f"  status: {status}")
    print(f"  last_record_count: {count}")

    # 查看数据记录数（2026-04-10）
    result = db.execute("SELECT COUNT(*) FROM stock_daily WHERE trade_date='2026-04-10'")
    data_count = result[0][0]
    print(f"\n数据库验证:")
    print(f"  stock_daily (2026-04-10)记录数: {data_count}")

    if status == 'success' and data_count > 0:
        print("✓ stock_daily测试成功")
    else:
        print("⚠ stock_daily测试异常")

except Exception as e:
    print(f"✗ 测试失败: {e}")

# 测试3：单表拉取（income - 按自然日策略，VIP接口）
print("\n" + "=" * 80)
print("测试3：income（按自然日策略，VIP接口）")
print("=" * 80)

try:
    # 设置游标为2026-04-08（拉取2026-04-09）
    import duckdb
    conn = duckdb.connect(db_path)
    conn.execute("UPDATE global_cursor SET cursor_value='20260408', status='pending' WHERE table_name='income'")
    conn.close()

    print("\n游标设置: 20260408")
    print("预期拉取: 20260409")

    print("\n触发拉取...")
    fetcher._fetch_table('income')

    # 查看游标状态
    db = Database(db_path)
    result = db.execute("SELECT cursor_value, status, last_record_count FROM global_cursor WHERE table_name='income'")
    cursor_value, status, count = result[0]

    print(f"\n游标状态:")
    print(f"  cursor_value: {cursor_value}")
    print(f"  status: {status}")
    print(f"  last_record_count: {count}")

    # 查看数据记录数（2026-04-09）
    result = db.execute("SELECT COUNT(*) FROM income WHERE ann_date='2026-04-09'")
    data_count = result[0][0]
    print(f"\n数据库验证:")
    print(f"  income (2026-04-09)记录数: {data_count}")

    # 财务表允许无数据更新
    if status == 'success':
        print("✓ income测试成功（游标已更新，财务表允许无数据）")
    else:
        print("⚠ income测试异常")

except Exception as e:
    print(f"✗ 测试失败: {e}")

print("\n" + "=" * 80)
print("DataFetcher测试完成")
print("=" * 80)