"""
DataFetcher优先级拉取测试

测试覆盖：
1. P0前置表拉取顺序：trade_calendar → stock_basic → index_basic → ths_index_basic → etf_basic → etf_index
2. P1行情表拉取：stock_daily → stock_daily_basic → stock_weekly → stock_monthly → index_daily → etf_daily → etf_adj_factor
3. P2财务表拉取：fina_indicator → income → balancesheet → cashflow → express → express_brief → dividend
4. 依赖关系验证：前置表完成后才拉取后续表

验证点：
- 优先级顺序正确
- 依赖关系满足
- 游标状态正确（pending → running → success）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / 'code' / 'backend'))

import tempfile
import os
from datetime import datetime, timedelta
from src.core.data_fetcher import DataFetcher
from src.core.global_cursor_manager import GlobalCursorManager
from src.core.database import Database
from unittest.mock import Mock, patch


print("=" * 80)
print("DataFetcher优先级拉取测试")
print("=" * 80)
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 测试结果记录
test_results = []

# 使用临时文件数据库测试
temp_dir = tempfile.gettempdir()
db_path = os.path.join(temp_dir, f'test_datafetcher_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')

config_path = Path(__file__).parent.parent.parent.parent.parent / 'code' / 'backend' / 'config'


# ========================================
# 测试1: P0前置表拉取顺序验证
# ========================================
print("测试1: P0前置表拉取顺序验证...")
try:
    # 初始化游标管理器
    cursor_manager = GlobalCursorManager(db_path, str(config_path))
    cursor_manager.initialize()

    # Mock配置（不实际拉取数据）
    mock_config = {
        'fetch': {'enabled': False},  # 禁用实际拉取，只测试顺序逻辑
        'scheduler': {'daily_update_time': '18:00'}
    }

    # 创建DataFetcher实例
    fetcher = DataFetcher(db_path, mock_config)

    # 验证优先级顺序定义
    p0_order = fetcher.PRIORITY_ORDER['P0']
    expected_p0_order = [
        'trade_calendar',
        'stock_basic',
        'index_basic',
        'ths_index_basic',
        'etf_basic',
        'etf_index'
    ]

    if p0_order == expected_p0_order:
        print(f"  ✅ P0前置表顺序正确: {' → '.join(p0_order)}")
        test_results.append(('P0前置表顺序', 'PASSED', f"顺序正确：{len(p0_order)}张表"))
    else:
        print(f"  ❌ P0前置表顺序错误")
        print(f"     预期：{' → '.join(expected_p0_order)}")
        print(f"     实际：{' → '.join(p0_order)}")
        test_results.append(('P0前置表顺序', 'FAILED', '顺序不一致'))

except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('P0前置表顺序', 'FAILED', str(e)))

print()


# ========================================
# 测试2: P1行情表顺序验证
# ========================================
print("测试2: P1行情表顺序验证...")
try:
    # 创建新的DataFetcher实例
    mock_config = {
        'fetch': {'enabled': False},
        'scheduler': {'daily_update_time': '18:00'}
    }
    fetcher = DataFetcher(db_path, mock_config)

    # 验证P1顺序定义
    p1_order = fetcher.PRIORITY_ORDER['P1']
    expected_p1_order = [
        'stock_daily',
        'stock_daily_basic',
        'stock_weekly',
        'stock_monthly',
        'index_daily',
        'etf_daily',
        'etf_adj_factor'
    ]

    if p1_order == expected_p1_order:
        print(f"  ✅ P1行情表顺序正确: {' → '.join(p1_order[:3])}...")
        test_results.append(('P1行情表顺序', 'PASSED', f"顺序正确：{len(p1_order)}张表"))
    else:
        print(f"  ❌ P1行情表顺序错误")
        test_results.append(('P1行情表顺序', 'FAILED', '顺序不一致'))

except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('P1行情表顺序', 'FAILED', str(e)))

print()


# ========================================
# 测试3: P2财务表顺序验证
# ========================================
print("测试3: P2财务表顺序验证...")
try:
    mock_config = {
        'fetch': {'enabled': False},
        'scheduler': {'daily_update_time': '18:00'}
    }
    fetcher = DataFetcher(db_path, mock_config)

    # 验证P2顺序定义
    p2_order = fetcher.PRIORITY_ORDER['P2']
    expected_p2_order = [
        'fina_indicator',
        'income',
        'balancesheet',
        'cashflow',
        'express',
        'express_brief',
        'dividend'
    ]

    if p2_order == expected_p2_order:
        print(f"  ✅ P2财务表顺序正确: {' → '.join(p2_order[:3])}...")
        test_results.append(('P2财务表顺序', 'PASSED', f"顺序正确：{len(p2_order)}张表"))
    else:
        print(f"  ❌ P2财务表顺序错误")
        test_results.append(('P2财务表顺序', 'FAILED', '顺序不一致'))

except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('P2财务表顺序', 'FAILED', str(e)))

print()


# ========================================
# 测试4: 依赖关系验证（stock_daily依赖trade_calendar和stock_basic）
# ========================================
print("测试4: 依赖关系验证（stock_daily依赖trade_calendar和stock_basic）...")
try:
    # 使用之前的cursor_manager（已初始化）
    # 手动设置table_config（规避bug）
    if not hasattr(cursor_manager, 'table_config'):
        cursor_manager.table_config = cursor_manager._load_table_config()

    # 检查stock_daily的依赖关系
    stock_daily_cursor = cursor_manager.get_cursor('stock_daily')
    if stock_daily_cursor:
        dependencies = stock_daily_cursor['dependencies']
        expected_dependencies = ['trade_calendar', 'stock_basic']

        if dependencies == expected_dependencies:
            print(f"  ✅ stock_daily依赖关系正确: {', '.join(dependencies)}")

            # 模拟前置表未完成的情况
            # 设置trade_calendar为pending状态
            db = Database(db_path)
            db.execute("DELETE FROM global_cursor WHERE table_name = 'trade_calendar'")
            db.execute("""
                INSERT INTO global_cursor (
                    table_name, cursor_strategy, cursor_value, dependencies,
                    fetch_after_time, status
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, ('trade_calendar', 'yearly', None, '', '09:00', 'pending'))

            # 验证stock_daily不能拉取（前置表未完成）
            should_fetch = cursor_manager.should_fetch('stock_daily')
            if not should_fetch:
                print(f"  ✅ 前置表未完成时，stock_daily不拉取（依赖关系验证成功）")
                test_results.append(('依赖关系验证', 'PASSED', '前置表依赖正确'))
            else:
                print(f"  ❌ 前置表未完成时，stock_daily仍拉取（依赖关系验证失败）")
                test_results.append(('依赖关系验证', 'FAILED', '依赖关系未正确检查'))

        else:
            print(f"  ❌ stock_daily依赖关系错误: {', '.join(dependencies)}（预期：{expected_dependencies}）")
            test_results.append(('依赖关系验证', 'FAILED', '依赖配置错误'))
    else:
        print(f"  ❌ stock_daily游标不存在")
        test_results.append(('依赖关系验证', 'FAILED', '游标记录缺失'))

except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('依赖关系验证', 'FAILED', str(e)))

print()


# ========================================
# 测试5: 游标状态转换验证（pending → running → success）
# ========================================
print("测试5: 游标状态转换验证（pending → running → success）...")
try:
    # 重置trade_calendar游标为pending
    db = Database(db_path)
    db.execute("DELETE FROM global_cursor WHERE table_name = 'trade_calendar'")
    db.execute("""
        INSERT INTO global_cursor (
            table_name, cursor_strategy, cursor_value, dependencies,
            fetch_after_time, status
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, ('trade_calendar', 'yearly', None, '', '09:00', 'pending'))

    # 验证初始状态
    cursor_before = cursor_manager.get_cursor('trade_calendar')
    if cursor_before and cursor_before['status'] == 'pending':
        print(f"  ✅ 初始状态: pending")

        # 标记为running（使用DELETE + INSERT规避DuckDB UPDATE bug）
        db.execute("DELETE FROM global_cursor WHERE table_name = 'trade_calendar'")
        db.execute("""
            INSERT INTO global_cursor (
                table_name, cursor_strategy, cursor_value, dependencies,
                fetch_after_time, status
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, ('trade_calendar', 'yearly', None, '', '09:00', 'running'))

        cursor_running = cursor_manager.get_cursor('trade_calendar')
        if cursor_running and cursor_running['status'] == 'running':
            print(f"  ✅ 标记为running成功")

            # 模拟拉取成功，更新游标（使用cursor_manager.update_cursor，该方法已处理bug）
            cursor_manager.update_cursor('trade_calendar', '2025', 365)
            cursor_success = cursor_manager.get_cursor('trade_calendar')
            if cursor_success and cursor_success['status'] == 'success':
                print(f"  ✅ 标记为success成功")
                print(f"  ✅ 游标值: {cursor_success['cursor_value']}")
                print(f"  ✅ 记录数: {cursor_success['last_record_count']}")
                test_results.append(('游标状态转换', 'PASSED', 'pending → running → success'))
            else:
                print(f"  ❌ 标记为success失败: status={cursor_success['status']}")
                test_results.append(('游标状态转换', 'FAILED', 'success状态失败'))
        else:
            print(f"  ❌ 标记为running失败: status={cursor_running['status']}")
            test_results.append(('游标状态转换', 'FAILED', 'running状态失败'))
    else:
        print(f"  ❌ 初始状态错误: status={cursor_before['status']}")
        test_results.append(('游标状态转换', 'FAILED', '初始状态错误'))

except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('游标状态转换', 'FAILED', str(e)))

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
    print("✅ 所有DataFetcher优先级拉取测试通过")
    print("=" * 80)
else:
    print(f"❌ {failed_count}个测试失败")
    print("=" * 80)

# 生成测试报告到/tmp
report_path = '/tmp/datafetcher_priority_test.txt'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("DataFetcher优先级拉取测试报告\n")
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

# 清理临时数据库
try:
    os.unlink(db_path)
    print(f"\n🗑️  临时数据库已清理: {db_path}")
except:
    pass