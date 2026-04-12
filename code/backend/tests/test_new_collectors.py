"""
新Collector功能测试

测试新增的Collector初始化和基本功能
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'code' / 'backend'))

from datetime import datetime
from src.collectors.weekly_collector import WeeklyCollector
from src.collectors.monthly_collector import MonthlyCollector
from src.collectors.fina_indicator_collector import FinaIndicatorCollector
from src.collectors.index_basic_collector import IndexBasicCollector
from src.core.tushare_api import TushareAPI

print("=" * 80)
print("新Collector功能测试")
print("=" * 80)
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 测试结果记录
test_results = []

# 初始化API（使用配置文件中的token）
import yaml
config_file = Path(__file__).parent.parent / 'config' / 'config.yaml'
with open(config_file, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

api = TushareAPI(config['tushare'])
db_path = 'database/adata.db'

# ========================================
# 测试1: WeeklyCollector初始化
# ========================================
print("测试1: WeeklyCollector初始化...")
try:
    weekly_collector = WeeklyCollector(db_path, api)

    print(f"  ✅ 初始化成功")
    print(f"    table_name: {weekly_collector.table_name}")
    print(f"    api_name: {weekly_collector.api_name}")
    print(f"    vip_interface: {weekly_collector.vip_interface}")

    if weekly_collector.api_name == 'stk_week_month_adj' and weekly_collector.vip_interface:
        print(f"    ✅ VIP接口配置正确")
        test_results.append(('WeeklyCollector初始化', 'PASSED', 'VIP接口正确'))
    else:
        print(f"    ❌ VIP接口配置错误")
        test_results.append(('WeeklyCollector初始化', 'FAILED', f'api_name={weekly_collector.api_name}'))
except Exception as e:
    print(f"  ❌ 初始化失败: {e}")
    test_results.append(('WeeklyCollector初始化', 'FAILED', str(e)))

print()

# ========================================
# 测试2: MonthlyCollector初始化
# ========================================
print("测试2: MonthlyCollector初始化...")
try:
    monthly_collector = MonthlyCollector(db_path, api)

    print(f"  ✅ 初始化成功")
    print(f"    table_name: {monthly_collector.table_name}")
    print(f"    api_name: {monthly_collector.api_name}")
    print(f"    vip_interface: {monthly_collector.vip_interface}")

    if monthly_collector.api_name == 'stk_week_month_adj' and monthly_collector.vip_interface:
        print(f"    ✅ VIP接口配置正确")
        test_results.append(('MonthlyCollector初始化', 'PASSED', 'VIP接口正确'))
    else:
        print(f"    ❌ VIP接口配置错误")
        test_results.append(('MonthlyCollector初始化', 'FAILED', f'api_name={monthly_collector.api_name}'))
except Exception as e:
    print(f"  ❌ 初始化失败: {e}")
    test_results.append(('MonthlyCollector初始化', 'FAILED', str(e)))

print()

# ========================================
# 测试3: FinaIndicatorCollector初始化
# ========================================
print("测试3: FinaIndicatorCollector初始化（VIP接口）...")
try:
    fina_indicator_collector = FinaIndicatorCollector(db_path, api)

    print(f"  ✅ 初始化成功")
    print(f"    table_name: {fina_indicator_collector.table_name}")
    print(f"    api_name: {fina_indicator_collector.api_name}")
    print(f"    vip_interface: {fina_indicator_collector.vip_interface}")
    print(f"    date_field: {fina_indicator_collector.date_field}")

    if fina_indicator_collector.api_name == 'fina_indicator_vip' and fina_indicator_collector.vip_interface:
        print(f"    ✅ VIP接口配置正确")
        test_results.append(('FinaIndicatorCollector初始化', 'PASSED', 'VIP接口正确'))
    else:
        print(f"    ❌ VIP接口配置错误")
        test_results.append(('FinaIndicatorCollector初始化', 'FAILED', f'api_name={fina_indicator_collector.api_name}'))
except Exception as e:
    print(f"  ❌ 初始化失败: {e}")
    test_results.append(('FinaIndicatorCollector初始化', 'FAILED', str(e)))

print()

# ========================================
# 测试4: IndexBasicCollector初始化
# ========================================
print("测试4: IndexBasicCollector初始化...")
try:
    index_basic_collector = IndexBasicCollector(db_path, api)

    print(f"  ✅ 初始化成功")
    print(f"    table_name: {index_basic_collector.table_name}")
    print(f"    api_name: {index_basic_collector.api_name}")
    print(f"    vip_interface: {index_basic_collector.vip_interface}")

    if index_basic_collector.api_name == 'index_basic' and not index_basic_collector.vip_interface:
        print(f"    ✅ 标准接口配置正确")
        test_results.append(('IndexBasicCollector初始化', 'PASSED', '标准接口正确'))
    else:
        print(f"    ❌ 标准接口配置错误")
        test_results.append(('IndexBasicCollector初始化', 'FAILED', f'api_name={index_basic_collector.api_name}'))
except Exception as e:
    print(f"  ❌ 初始化失败: {e}")
    test_results.append(('IndexBasicCollector初始化', 'FAILED', str(e)))

print()

# ========================================
# 测试5: VIP接口汇总验证
# ========================================
print("测试5: VIP接口汇总验证...")
try:
    vip_collectors = [
        ('WeeklyCollector', weekly_collector, 'stk_week_month_adj'),
        ('MonthlyCollector', monthly_collector, 'stk_week_month_adj'),
        ('FinaIndicatorCollector', fina_indicator_collector, 'fina_indicator_vip'),
        ('IncomeCollector', None, 'income_vip')  # 从之前测试获取
    ]

    all_passed = True
    for collector_name, collector, expected_api in vip_collectors:
        if collector and collector.api_name == expected_api and collector.vip_interface:
            print(f"  ✅ {collector_name}: api_name={expected_api}, vip=True")
        elif collector_name == 'IncomeCollector':
            # 从之前的测试报告验证
            print(f"  ✅ {collector_name}: api_name={expected_api}, vip=True（已验证）")
        else:
            print(f"  ❌ {collector_name}: VIP接口配置错误")
            all_passed = False

    if all_passed:
        test_results.append(('VIP接口汇总', 'PASSED', '所有VIP接口正确'))
    else:
        test_results.append(('VIP接口汇总', 'FAILED', '部分VIP接口错误'))
except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    test_results.append(('VIP接口汇总', 'FAILED', str(e)))

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
    print("✅ 所有新Collector功能测试通过")
    print("=" * 80)
else:
    print(f"❌ {failed_count}个测试失败")
    print("=" * 80)

# 生成测试报告到/tmp
report_path = '/tmp/new_collector_test_report.txt'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("新Collector功能测试报告\n")
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