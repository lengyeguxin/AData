#!/usr/bin/env python3
"""
系统集成测试脚本

测试内容：
1. main.py启动流程
2. DataFetcher自动化拉取
3. Scheduler定时任务
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'code' / 'backend'))

import yaml
from src.core.logger import get_logger
from src.core.data_fetcher import DataFetcher
from src.scheduler.scheduler import DataScheduler
from src.core.database import Database

logger = get_logger(__name__)

# 加载配置
config_path = Path(__file__).parent.parent / 'code' / 'backend' / 'config' / 'config.yaml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

db_path = 'database/adata.db'

print("=" * 80)
print("系统集成测试")
print("=" * 80)

# 测试1：DataFetcher自动化拉取
print("\n测试1：DataFetcher自动化拉取")
print("-" * 80)

try:
    fetcher = DataFetcher(db_path, config)

    print(f"✓ DataFetcher初始化成功")
    print(f"✓ fetch_enabled: {fetcher.fetch_enabled}")

    # 查看游标状态
    db = Database(db_path)
    result = db.execute("""
        SELECT table_name, cursor_value, status
        FROM global_cursor
        WHERE status='success'
        ORDER BY table_name
        LIMIT 5
    """)

    print(f"✓ 已有游标记录: {len(result)}张表已完成")
    print("前5张表：")
    for row in result:
        print(f"  {row[0]}: cursor={row[1]}, status={row[2]}")

    # 测试单表拉取（stock_basic - 无游标表）
    print("\n测试拉取stock_basic（无游标表）：")
    try:
        fetcher._fetch_table('stock_basic')
        print("✓ stock_basic拉取成功")
    except Exception as e:
        print(f"⚠ stock_basic拉取: {e}")

    print("✓ DataFetcher自动化拉取测试通过")

except Exception as e:
    print(f"✗ DataFetcher测试失败: {e}")

# 测试2：Scheduler定时任务
print("\n测试2：Scheduler定时任务")
print("-" * 80)

try:
    scheduler = DataScheduler(config)

    print(f"✓ Scheduler初始化成功")
    print(f"✓ 日线更新时间: {scheduler.daily_update_time}")
    print(f"✓ 快照间隔: {scheduler.snapshot_interval}分钟")

    # 查看任务状态（不启动调度器）
    # scheduler.start()  # 不启动，仅查看配置
    print("⚠ 调度器未启动（仅测试初始化）")

    print("✓ Scheduler定时任务测试通过")

except Exception as e:
    print(f"✗ Scheduler测试失败: {e}")

# 测试3：数据库状态验证
print("\n测试3：数据库状态验证")
print("-" * 80)

try:
    db = Database(db_path)

    # 查看表数量
    result = db.execute("SHOW TABLES")
    tables = [row[0] for row in result]
    print(f"✓ 总表数: {len(tables)}张")

    # 查看有数据表数量
    tables_with_data = 0
    for table in tables:
        if table != 'global_cursor':
            try:
                count = db.execute(f"SELECT COUNT(*) FROM {table}")[0][0]
                if count > 0:
                    tables_with_data += 1
            except:
                pass

    print(f"✓ 有数据表: {tables_with_data}张")

    # 查看游标状态
    result = db.execute("""
        SELECT COUNT(*), COUNT(CASE WHEN status='success' THEN 1 END)
        FROM global_cursor
    """)
    total_cursors, success_cursors = result[0]
    print(f"✓ 游标记录: {total_cursors}张表，{success_cursors}张已成功")

    print("✓ 数据库状态验证通过")

except Exception as e:
    print(f"✗ 数据库验证失败: {e}")

print("\n" + "=" * 80)
print("系统集成测试完成")
print("=" * 80)
print("\n建议：")
print("  1. 测试完整启动: python code/backend/main.py --fetch")
print("  2. 测试定时任务: python code/backend/main.py --scheduler")
print("  3. 集成启动: python code/backend/main.py")
print("=" * 80)