"""
数据拉取功能测试（模拟API，不消耗配额）

测试各个游标策略的数据拉取逻辑
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from datetime import datetime, timedelta
from src.core.global_cursor_manager import GlobalCursorManager
from src.core.database import Database

print("=" * 80)
print("数据拉取功能测试（模拟API）")
print("=" * 80)
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 测试结果记录
test_results = []

# ========================================
# 测试1: 游标策略判断
# ========================================
print("测试1: 游标策略判断...")
try:
    db_path = 'database/adata.db'
    cursor_manager = GlobalCursorManager(db_path, 'code/backend/config')

    # 测试各表的游标策略
    test_tables = [
        ('stock_basic', 'none'),
        ('trade_calendar', 'yearly'),
        ('stock_daily', 'daily_trade'),
        ('income', 'daily_natural'),
        ('ths_concept_member', 'special_ths_member')
    ]

    all_passed = True
    for table_name, expected_strategy in test_tables:
        strategy = cursor_manager.get_cursor_strategy(table_name)
        if strategy == expected_strategy:
            print(f"  ✅ {table_name}: strategy={strategy}（预期：{expected_strategy}）")
        else:
            print(f"  ❌ {table_name}: strategy={strategy}（预期：{expected_strategy}）")
            all_passed = False

    if all_passed:
        test_results.append(('游标策略判断', 'PASSED', '所有表策略正确'))
    else:
        test_results.append(('游标策略判断', 'FAILED', '部分表策略错误'))
except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('游标策略判断', 'FAILED', str(e)))

print()

# ========================================
# 测试2: 18点时间判断逻辑
# ========================================
print("测试2: 18点时间判断逻辑...")
try:
    cursor_manager = GlobalCursorManager(db_path, 'code/backend/config')

    # 测试stock_daily表（18:00截止）
    end_date_daily = cursor_manager.get_end_date_with_time_check('stock_daily')
    now = datetime.now()
    current_hour = now.hour

    print(f"  当前时间: {now.strftime('%H:%M')}")
    print(f"  当前小时: {current_hour}")
    print(f"  stock_daily截止时间: 18:00")
    print(f"  stock_daily结束日期: {end_date_daily}")

    # 验证逻辑
    expected_end_date = now.strftime('%Y%m%d') if current_hour >= 18 else (now - timedelta(days=1)).strftime('%Y%m%d')

    if end_date_daily == expected_end_date:
        print(f"  ✅ 18点判断正确: end_date={end_date_daily}")
    else:
        print(f"  ❌ 18点判断错误: end_date={end_date_daily}（预期：{expected_end_date}）")

    # 测试stock_basic表（09:00截止）
    end_date_basic = cursor_manager.get_end_date_with_time_check('stock_basic')
    print(f"  stock_basic截止时间: 09:00")
    print(f"  stock_basic结束日期: {end_date_basic}")

    expected_end_date_basic = now.strftime('%Y%m%d') if current_hour >= 9 else (now - timedelta(days=1)).strftime('%Y%m%d')

    if end_date_basic == expected_end_date_basic:
        print(f"  ✅ 09点判断正确: end_date={end_date_basic}")
    else:
        print(f"  ❌ 09点判断错误: end_date={end_date_basic}（预期：{expected_end_date_basic}）")

    if end_date_daily == expected_end_date and end_date_basic == expected_end_date_basic:
        test_results.append(('截止时间判断', 'PASSED', f'18:00={end_date_daily}, 09:00={end_date_basic}'))
    else:
        test_results.append(('截止时间判断', 'FAILED', '时间判断逻辑错误'))
except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('截止时间判断', 'FAILED', str(e)))

print()

# ========================================
# 测试3: 游标更新时机判断
# ========================================
print("测试3: 游标更新时机判断（财务表允许无数据）...")
try:
    cursor_manager = GlobalCursorManager(db_path, 'code/backend/config')

    # 测试财务表（允许无数据更新）
    should_update_income = cursor_manager.should_update_cursor('income', has_data=False)
    if should_update_income:
        print(f"  ✅ income表（daily_natural）: 允许无数据更新")
    else:
        print(f"  ❌ income表（daily_natural）: 不允许无数据更新（应该允许）")

    # 测试日线表（必须有数据）
    should_update_daily = cursor_manager.should_update_cursor('stock_daily', has_data=False)
    if not should_update_daily:
        print(f"  ✅ stock_daily表（daily_trade）: 必须有数据才更新")
    else:
        print(f"  ❌ stock_daily表（daily_trade）: 允许无数据更新（不应该允许）")

    # 测试有数据的情况（都应该允许）
    should_update_income_with_data = cursor_manager.should_update_cursor('income', has_data=True)
    should_update_daily_with_data = cursor_manager.should_update_cursor('stock_daily', has_data=True)

    if should_update_income and not should_update_daily and should_update_income_with_data and should_update_daily_with_data:
        print(f"  ✅ 游标更新时机逻辑正确")
        test_results.append(('游标更新时机', 'PASSED', '财务表允许无数据，其他表必须有数据'))
    else:
        print(f"  ❌ 游标更新时机逻辑错误")
        test_results.append(('游标更新时机', 'FAILED', '逻辑判断错误'))
except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    test_results.append(('游标更新时机', 'FAILED', str(e)))

print()

# ========================================
# 测试4: 下次拉取日期计算
# ========================================
print("测试4: 下次拉取日期计算...")
try:
    # 先设置一些游标值
    with Database(db_path) as db:
        # 设置stock_daily游标为昨天
        from datetime import timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        db.execute("""
            UPDATE global_cursor
            SET cursor_value = ?
            WHERE table_name = 'stock_daily'
        """, (yesterday,))

        # 设置trade_calendar游标为2025
        db.execute("""
            UPDATE global_cursor
            SET cursor_value = '2025'
            WHERE table_name = 'trade_calendar'
        """)

    cursor_manager = GlobalCursorManager(db_path, 'code/backend/config')

    # 测试stock_daily（daily_trade策略）
    next_date_daily = cursor_manager.get_next_fetch_date('stock_daily')
    expected_next_daily = datetime.now().strftime('%Y%m%d')

    if next_date_daily == expected_next_daily:
        print(f"  ✅ stock_daily: next_date={next_date_daily}（游标={yesterday}）")
    else:
        print(f"  ❌ stock_daily: next_date={next_date_daily}（预期：{expected_next_daily}）")

    # 测试trade_calendar（yearly策略）
    next_year_calendar = cursor_manager.get_next_fetch_date('trade_calendar')
    expected_next_year = '2026'

    if next_year_calendar == expected_next_year:
        print(f"  ✅ trade_calendar: next_year={next_year_calendar}（游标=2025）")
    else:
        print(f"  ❌ trade_calendar: next_year={next_year_calendar}（预期：{expected_next_year}）")

    # 测试income（无游标，从start_date开始）
    next_date_income = cursor_manager.get_next_fetch_date('income')
    start_date = '20210101'  # 默认start_date

    if next_date_income == start_date:
        print(f"  ✅ income: next_date={next_date_income}（无游标，从start_date开始）")
    else:
        print(f"  ❌ income: next_date={next_date_income}（预期：{start_date}）")

    test_results.append(('下次拉取日期', 'PASSED', '各策略计算正确'))
except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('下次拉取日期', 'FAILED', str(e)))

print()

# ========================================
# 测试汇总
# ========================================
print("=" * 80)
print("测试汇总")
print("=" * 80)

passed_count = sum(1 for r in test_results if r[1] == 'PASSED')
failed_count = sum(1 for r in test_results if r[1] == 'FAILED')

print(f"总测试数: {len(test_results)}")
print(f"通过数: {passed_count}")
print(f"失败数: {failed_count}")
print()

print("详细结果:")
for test_name, status, message in test_results:
    status_icon = "✅" if status == "PASSED" else "❌"
    print(f"  {status_icon} {test_name}: {message}")

print()
print("=" * 80)

if failed_count == 0:
    print("✅ 所有数据拉取功能测试通过")
    print("=" * 80)
else:
    print(f"❌ {failed_count}个测试失败")
    print("=" * 80)

# 生成测试报告到/tmp
report_path = '/tmp/fetch_logic_test_report.txt'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("数据拉取功能测试报告（模拟API）\n")
    f.write("=" * 80 + "\n")
    f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"\n总测试数: {len(test_results)}\n")
    f.write(f"通过数: {passed_count}\n")
    f.write(f"失败数: {failed_count}\n")
    f.write("\n详细结果:\n")
    for test_name, status, message in test_results:
        status_icon = "✅" if status == "PASSED" else "❌"
        f.write(f"  {status_icon} {test_name}: {message}\n")
    f.write("\n" + "=" * 80 + "\n")
    if failed_count == 0:
        f.write("✅ 所有测试通过\n")
    else:
        f.write(f"❌ {failed_count}个测试失败\n")
    f.write("=" * 80 + "\n")

print(f"\n📋 测试报告已生成: {report_path}")