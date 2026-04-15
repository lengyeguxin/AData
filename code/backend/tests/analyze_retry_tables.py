#!/usr/bin/env python3
"""
分析哪些表受重试机制影响
"""

import yaml

with open('/home/my/claude-project/AData/code/backend/config/table_config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

with open('/home/my/claude-project/AData/code/backend/config/config.yaml', 'r', encoding='utf-8') as f:
    app_config = yaml.safe_load(f)

print("=" * 80)
print("重试机制影响分析")
print("=" * 80)

max_retries = app_config.get('fetch', {}).get('max_retries', 2)
retry_delay = app_config.get('fetch', {}).get('retry_delay', 30)

daily_trade_tables = []
daily_natural_tables = []
other_tables = []

for table_name, table_config in config['tables'].items():
    cursor_strategy = table_config.get('cursor_strategy', 'none')

    if cursor_strategy == 'daily_trade':
        daily_trade_tables.append(table_name)
    elif cursor_strategy == 'daily_natural':
        daily_natural_tables.append(table_name)
    else:
        other_tables.append({
            'table': table_name,
            'strategy': cursor_strategy
        })

print(f"\n配置: max_retries={max_retries}, retry_delay={retry_delay}秒\n")

print("【🔥 受重试机制影响的表】")
print(f"\n1️⃣ 按交易日策略（DAILY_TRADE）- 行情表:")
print(f"   失败/无数据时重试{max_retries}次，失败后停止拉取")
for i, table in enumerate(daily_trade_tables, 1):
    print(f"   {i}. {table}")

print(f"\n2️⃣ 按自然日策略（DAILY_NATURAL）- 财务表:")
print(f"   失败时重试{max_retries}次，无数据继续")
for i, table in enumerate(daily_natural_tables, 1):
    print(f"   {i}. {table}")

print("\n3️⃣ 全量/按年/特殊策略 - 基础表:")
print(f"   失败时重试{max_retries}次，失败后抛出异常")
for i, item in enumerate(other_tables, 1):
    print(f"   {i}. {item['table']:30s} (策略: {item['strategy']})")

print("\n" + "=" * 80)
total_affected = len(daily_trade_tables) + len(daily_natural_tables) + len(other_tables)
print(f"总结: {len(daily_trade_tables)}个行情表 + {len(daily_natural_tables)}个财务表 + {len(other_tables)}个基础表 = {total_affected}个表全部受重试机制影响")
print("=" * 80)
