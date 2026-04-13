"""
真实API调用测试

使用Tushare真实API测试数据拉取、游标更新、断点续传功能
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from datetime import datetime
import yaml
from src.core.tushare_api import TushareAPI
from src.core.global_cursor_manager import GlobalCursorManager
from src.collectors.stock_basic_collector import StockBasicCollector
from src.collectors.trade_calendar_collector import TradeCalendarCollector
from src.collectors.index_basic_collector import IndexBasicCollector
from src.core.database import Database

print("=" * 80)
print("真实API调用测试")
print("=" * 80)
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 加载配置
project_root = Path(__file__).parent.parent.parent.parent
config_file = project_root / 'code' / 'backend' / 'config' / 'config.yaml'
with open(config_file, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

db_path = str(project_root / 'database' / 'adata.db')
api = TushareAPI(config['tushare'])
cursor_manager = GlobalCursorManager(db_path, str(project_root / 'code' / 'backend' / 'config'))

test_results = []

# ========================================
# 测试1: stock_basic全量拉取（none策略）
# ========================================
print("测试1: stock_basic全量拉取（真实API调用）...")
try:
    collector = StockBasicCollector(db_path, api)

    # 检查游标状态
    cursor_before = cursor_manager.get_cursor('stock_basic')
    print(f"  游标状态（拉取前）: cursor_value={cursor_before['cursor_value']}, status={cursor_before['status']}")

    # 拉取数据
    count = collector.run()

    print(f"  ✅ 拉取成功: {count}条记录")

    # 验证数据库
    with Database(db_path) as db:
        result = db.execute("SELECT COUNT(*) FROM stock_basic")
        db_count = result[0][0]
        print(f"  数据库验证: {db_count}条记录")

    if db_count > 0:
        print(f"  ✅ stock_basic数据拉取成功")
        test_results.append(('stock_basic拉取', 'PASSED', f'{count}条记录入库'))
    else:
        print(f"  ❌ stock_basic数据拉取失败（无数据）")
        test_results.append(('stock_basic拉取', 'FAILED', '无数据入库'))

except Exception as e:
    print(f"  ❌ 拉取失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('stock_basic拉取', 'FAILED', str(e)))

print()

# ========================================
# 测试2: trade_calendar按年拉取（yearly策略）
# ========================================
print("测试2: trade_calendar按年拉取（真实API调用）...")
try:
    collector = TradeCalendarCollector(db_path, api)

    # 检查游标状态
    cursor_before = cursor_manager.get_cursor('trade_calendar')
    print(f"  游标状态（拉取前）: cursor_value={cursor_before['cursor_value']}, status={cursor_before['status']}")

    # 拉取2026年数据
    count = collector.run_year(2026)

    print(f"  ✅ 拉取成功: {count}条记录")

    # 验证数据库
    with Database(db_path) as db:
        result = db.execute("SELECT COUNT(*) FROM trade_calendar WHERE cal_date >= '2026-01-01'")
        db_count = result[0][0]
        print(f"  数据库验证（2026年）: {db_count}条记录")

    # 更新游标
    cursor_manager.update_cursor('trade_calendar', '2026', count)

    # 验证游标更新
    cursor_after = cursor_manager.get_cursor('trade_calendar')
    print(f"  游标状态（拉取后）: cursor_value={cursor_after['cursor_value']}, status={cursor_after['status']}")

    if cursor_after['cursor_value'] == '2026' and cursor_after['status'] == 'success':
        print(f"  ✅ trade_calendar拉取+游标更新成功")
        test_results.append(('trade_calendar拉取', 'PASSED', f'{count}条记录，游标更新为2026'))
    else:
        print(f"  ❌ 游标更新失败")
        test_results.append(('trade_calendar拉取', 'FAILED', f'游标={cursor_after["cursor_value"]}'))

except Exception as e:
    print(f"  ❌ 拉取失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('trade_calendar拉取', 'FAILED', str(e)))

print()

# ========================================
# 测试3: index_basic全量拉取（none策略）
# ========================================
print("测试3: index_basic全量拉取（真实API调用）...")
try:
    collector = IndexBasicCollector(db_path, api)

    # 拉取数据
    count = collector.run()

    print(f"  ✅ 拉取成功: {count}条记录")

    # 验证数据库
    with Database(db_path) as db:
        result = db.execute("SELECT COUNT(*) FROM index_basic")
        db_count = result[0][0]
        print(f"  数据库验证: {db_count}条记录")

    if db_count > 0:
        print(f"  ✅ index_basic数据拉取成功")
        test_results.append(('index_basic拉取', 'PASSED', f'{count}条记录入库'))
    else:
        print(f"  ❌ index_basic数据拉取失败（无数据）")
        test_results.append(('index_basic拉取', 'FAILED', '无数据入库'))

except Exception as e:
    print(f"  ❌ 拉取失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('index_basic拉取', 'FAILED', str(e)))

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
    print("✅ 所有真实API测试通过")
    print("=" * 80)
else:
    print(f"❌ {failed_count}个测试失败")
    print("=" * 80)

# 生成测试报告到tmp目录
report_path = str(project_root / 'tmp' / 'api_test_report.txt')
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("真实API调用测试报告\n")
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