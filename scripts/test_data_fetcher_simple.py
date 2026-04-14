#!/usr/bin/env python3
"""
测试DataFetcher完整流程（简化版）

直接测试完整自动化拉取流程，不手动修改游标
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'code' / 'backend'))

from src.core.data_fetcher import DataFetcher
from src.core.database import Database
import yaml

print("=" * 80)
print("测试DataFetcher完整流程（简化版）")
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

# 查看当前游标状态
print("\n当前游标状态（前5张表）:")
print("-" * 80)

db = Database(db_path)
result = db.execute("""
    SELECT table_name, cursor_strategy, cursor_value, status, last_fetch_time
    FROM global_cursor
    ORDER BY table_name
    LIMIT 5
""")

for row in result:
    print(f"{row[0]:<20} | {row[1]:<20} | {row[2] or 'NULL':<15} | {row[3]:<10} | {row[4] or 'NULL'}")

print("=" * 80)

# 测试完整拉取流程（P0前置表）
print("\n测试：启动数据拉取（fetcher.start()）")
print("=" * 80)

# 设置fetch.enabled=true
fetcher.fetch_enabled = True

# 启动拉取（只拉取P0前置表测试）
print("\n拉取P0前置表（trade_calendar、stock_basic、index_basic）...")

try:
    # 单独测试几个表
    for table_name in ['trade_calendar', 'stock_basic', 'index_basic']:
        print(f"\n拉取: {table_name}")
        print("-" * 80)

        try:
            fetcher._fetch_table(table_name)

            # 查看游标状态
            result = db.execute(f"""
                SELECT cursor_value, status, last_record_count
                FROM global_cursor
                WHERE table_name='{table_name}'
            """)
            cursor_value, status, count = result[0]

            print(f"游标状态: cursor={cursor_value or 'NULL'}, status={status}, records={count}")

            # 查看数据记录数
            if table_name == 'trade_calendar':
                data_count = db.execute("SELECT COUNT(*) FROM trade_calendar")[0][0]
            elif table_name == 'stock_basic':
                data_count = db.execute("SELECT COUNT(*) FROM stock_basic")[0][0]
            elif table_name == 'index_basic':
                data_count = db.execute("SELECT COUNT(*) FROM index_basic")[0][0]

            print(f"数据记录数: {data_count}")

            if status == 'success' or (table_name in ['stock_basic', 'index_basic'] and cursor_value == 'completed'):
                print(f"✓ {table_name}测试成功")
            else:
                print(f"⚠ {table_name}状态: {status}")

        except Exception as e:
            print(f"✗ {table_name}拉取失败: {e}")

    print("\n" + "=" * 80)
    print("DataFetcher测试完成")
    print("=" * 80)

except Exception as e:
    print(f"✗ DataFetcher启动失败: {e}")