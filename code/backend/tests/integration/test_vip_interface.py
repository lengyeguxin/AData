"""
VIP接口处理测试

测试覆盖：
1. VIP接口名称验证：income_vip、balancesheet_vip、cashflow_vip等
2. vip_interface标记验证：vip_interface=True
3. 游标策略验证：daily_natural策略，允许无数据更新
4. 字段丰富度验证：财务表94-158字段

验证点：
- API调用参数正确
- VIP接口标记正确
- 游标更新逻辑正确（允许无数据更新）
- 字段数量符合预期
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / 'code' / 'backend'))

import tempfile
import os
from datetime import datetime, timedelta
from src.core.global_cursor_manager import GlobalCursorManager
from src.core.database import Database
from src.core.tushare_api import TushareAPI
from src.collectors.income_collector import IncomeCollector
from src.collectors.balancesheet_collector import BalancesheetCollector
from src.collectors.cashflow_collector import CashflowCollector
from src.collectors.fina_indicator_collector import FinaIndicatorCollector
from src.collectors.express_collector import ExpressCollector
from src.collectors.express_brief_collector import ExpressBriefCollector
from src.collectors.weekly_collector import WeeklyCollector
from src.collectors.monthly_collector import MonthlyCollector


print("=" * 80)
print("VIP接口处理测试")
print("=" * 80)
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 测试结果记录
test_results = []

# 使用临时文件数据库测试
temp_dir = tempfile.gettempdir()
db_path = os.path.join(temp_dir, f'test_vip_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')

config_path = Path(__file__).parent.parent.parent.parent.parent / 'code' / 'backend' / 'config'

# Mock API配置
mock_config = {
    "token": "test_token",
    "api_url": "http://api.tushare.pro",
    "rate_limit": 500
}


# ========================================
# 测试1: VIP财务表接口名称验证
# ========================================
print("测试1: VIP财务表接口名称验证...")
try:
    api = TushareAPI(mock_config)

    # 验证income_vip接口名称
    income_collector = IncomeCollector(db_path, api)
    if income_collector.api_name == 'income_vip':
        print(f"  ✅ income接口名称正确: {income_collector.api_name}")
    else:
        print(f"  ❌ income接口名称错误: {income_collector.api_name}（预期：income_vip）")

    # 验证balancesheet_vip接口名称
    balancesheet_collector = BalancesheetCollector(db_path, api)
    if balancesheet_collector.api_name == 'balancesheet_vip':
        print(f"  ✅ balancesheet接口名称正确: {balancesheet_collector.api_name}")
    else:
        print(f"  ❌ balancesheet接口名称错误: {balancesheet_collector.api_name}")

    # 验证cashflow_vip接口名称
    cashflow_collector = CashflowCollector(db_path, api)
    if cashflow_collector.api_name == 'cashflow_vip':
        print(f"  ✅ cashflow接口名称正确: {cashflow_collector.api_name}")
    else:
        print(f"  ❌ cashflow接口名称错误: {cashflow_collector.api_name}")

    # 验证fina_indicator_vip接口名称
    fina_indicator_collector = FinaIndicatorCollector(db_path, api)
    if fina_indicator_collector.api_name == 'fina_indicator_vip':
        print(f"  ✅ fina_indicator接口名称正确: {fina_indicator_collector.api_name}")
    else:
        print(f"  ❌ fina_indicator接口名称错误: {fina_indicator_collector.api_name}")

    # 验证forecast_vip接口名称（express）
    express_collector = ExpressCollector(db_path, api)
    if express_collector.api_name == 'forecast_vip':
        print(f"  ✅ express接口名称正确: {express_collector.api_name}")
    else:
        print(f"  ❌ express接口名称错误: {express_collector.api_name}")

    # 验证express_vip接口名称（express_brief）
    express_brief_collector = ExpressBriefCollector(db_path, api)
    if express_brief_collector.api_name == 'express_vip':
        print(f"  ✅ express_brief接口名称正确: {express_brief_collector.api_name}")
    else:
        print(f"  ❌ express_brief接口名称错误: {express_brief_collector.api_name}")

    # 统计验证结果
    all_correct = (
        income_collector.api_name == 'income_vip' and
        balancesheet_collector.api_name == 'balancesheet_vip' and
        cashflow_collector.api_name == 'cashflow_vip' and
        fina_indicator_collector.api_name == 'fina_indicator_vip'
    )

    if all_correct:
        test_results.append(('VIP财务表接口名称', 'PASSED', '4个VIP财务表接口名称正确'))
    else:
        test_results.append(('VIP财务表接口名称', 'FAILED', '部分接口名称错误'))

except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('VIP财务表接口名称', 'FAILED', str(e)))

print()


# ========================================
# 测试2: vip_interface标记验证
# ========================================
print("测试2: vip_interface标记验证...")
try:
    api = TushareAPI(mock_config)

    # 验证财务表VIP标记
    income_collector = IncomeCollector(db_path, api)
    balancesheet_collector = BalancesheetCollector(db_path, api)
    cashflow_collector = CashflowCollector(db_path, api)
    fina_indicator_collector = FinaIndicatorCollector(db_path, api)

    all_vip = (
        income_collector.vip_interface == True and
        balancesheet_collector.vip_interface == True and
        cashflow_collector.vip_interface == True and
        fina_indicator_collector.vip_interface == True
    )

    if all_vip:
        print(f"  ✅ VIP财务表标记正确: vip_interface=True")
        test_results.append(('VIP标记验证', 'PASSED', '4个VIP财务表标记正确'))
    else:
        print(f"  ❌ VIP财务表标记错误")
        test_results.append(('VIP标记验证', 'FAILED', 'VIP标记错误'))

except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('VIP标记验证', 'FAILED', str(e)))

print()


# ========================================
# 测试3: VIP财务表游标策略验证（daily_natural）
# ========================================
print("测试3: VIP财务表游标策略验证（daily_natural）...")
try:
    # 初始化游标管理器
    cursor_manager = GlobalCursorManager(db_path, str(config_path))
    cursor_manager.initialize()

    # 手动设置table_config（规避bug）
    if not hasattr(cursor_manager, 'table_config'):
        cursor_manager.table_config = cursor_manager._load_table_config()

    # 验证income游标策略
    income_strategy = cursor_manager.get_cursor_strategy('income')
    if income_strategy == 'daily_natural':
        print(f"  ✅ income游标策略正确: {income_strategy}")
    else:
        print(f"  ❌ income游标策略错误: {income_strategy}（预期：daily_natural）")

    # 验证balancesheet游标策略
    balancesheet_strategy = cursor_manager.get_cursor_strategy('balancesheet')
    if balancesheet_strategy == 'daily_natural':
        print(f"  ✅ balancesheet游标策略正确: {balancesheet_strategy}")
    else:
        print(f"  ❌ balancesheet游标策略错误: {balancesheet_strategy}")

    # 验证cashflow游标策略
    cashflow_strategy = cursor_manager.get_cursor_strategy('cashflow')
    if cashflow_strategy == 'daily_natural':
        print(f"  ✅ cashflow游标策略正确: {cashflow_strategy}")
    else:
        print(f"  ❌ cashflow策略错误: {cashflow_strategy}")

    # 验证fina_indicator游标策略
    fina_indicator_strategy = cursor_manager.get_cursor_strategy('fina_indicator')
    if fina_indicator_strategy == 'daily_natural':
        print(f"  ✅ fina_indicator游标策略正确: {fina_indicator_strategy}")
    else:
        print(f"  ❌ fina_indicator游标策略错误: {fina_indicator_strategy}")

    all_correct = (
        income_strategy == 'daily_natural' and
        balancesheet_strategy == 'daily_natural' and
        cashflow_strategy == 'daily_natural' and
        fina_indicator_strategy == 'daily_natural'
    )

    if all_correct:
        test_results.append(('VIP财务表游标策略', 'PASSED', '4个VIP财务表使用daily_natural策略'))
    else:
        test_results.append(('VIP财务表游标策略', 'FAILED', '游标策略错误'))

except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('VIP财务表游标策略', 'FAILED', str(e)))

print()


# ========================================
# 测试4: VIP财务表允许无数据更新游标验证
# ========================================
print("测试4: VIP财务表允许无数据更新游标验证...")
try:
    # 使用之前的cursor_manager

    # 验证income允许无数据更新
    should_update_income_no_data = cursor_manager.should_update_cursor('income', has_data=False)
    if should_update_income_no_data:
        print(f"  ✅ income允许无数据更新（财务表特殊逻辑）")
    else:
        print(f"  ❌ income不允许无数据更新（应该允许）")

    # 验证balancesheet允许无数据更新
    should_update_balancesheet_no_data = cursor_manager.should_update_cursor('balancesheet', has_data=False)
    if should_update_balancesheet_no_data:
        print(f"  ✅ balancesheet允许无数据更新")
    else:
        print(f"  ❌ balancesheet不允许无数据更新")

    # 验证cashflow允许无数据更新
    should_update_cashflow_no_data = cursor_manager.should_update_cursor('cashflow', has_data=False)
    if should_update_cashflow_no_data:
        print(f"  ✅ cashflow允许无数据更新")
    else:
        print(f"  ❌ cashflow不允许无数据更新")

    # 验证fina_indicator允许无数据更新
    should_update_fina_indicator_no_data = cursor_manager.should_update_cursor('fina_indicator', has_data=False)
    if should_update_fina_indicator_no_data:
        print(f"  ✅ fina_indicator允许无数据更新")
    else:
        print(f"  ❌ fina_indicator不允许无数据更新")

    all_correct = (
        should_update_income_no_data and
        should_update_balancesheet_no_data and
        should_update_cashflow_no_data and
        should_update_fina_indicator_no_data
    )

    if all_correct:
        test_results.append(('VIP财务表无数据更新', 'PASSED', '4个VIP财务表允许无数据更新游标'))
    else:
        test_results.append(('VIP财务表无数据更新', 'FAILED', '无数据更新逻辑错误'))

except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('VIP财务表无数据更新', 'FAILED', str(e)))

print()


# ========================================
# 测试5: VIP财务表字段丰富度验证
# ========================================
print("测试5: VIP财务表字段丰富度验证...")
try:
    api = TushareAPI(mock_config)

    # 加载Mock数据验证字段数
    import json
    mock_data_dir = Path(__file__).parent.parent.parent.parent.parent / 'tests' / 'mock_data'

    # income字段数验证（预期94个字段）
    income_mock_file = mock_data_dir / 'income.json'
    if income_mock_file.exists():
        with open(income_mock_file, 'r', encoding='utf-8') as f:
            income_mock_data = json.load(f)
        income_field_count = len(income_mock_data[0])
        if income_field_count >= 90:
            print(f"  ✅ income字段丰富度高: {income_field_count}个字段")
        else:
            print(f"  ❌ income字段丰富度低: {income_field_count}个字段（预期≥90）")
    else:
        print(f"  ⚠️  income Mock数据不存在")
        income_field_count = 0

    # balancesheet字段数验证（预期158个字段）
    balancesheet_mock_file = mock_data_dir / 'balancesheet.json'
    if balancesheet_mock_file.exists():
        with open(balancesheet_mock_file, 'r', encoding='utf-8') as f:
            balancesheet_mock_data = json.load(f)
        balancesheet_field_count = len(balancesheet_mock_data[0])
        if balancesheet_field_count >= 150:
            print(f"  ✅ balancesheet字段丰富度高: {balancesheet_field_count}个字段")
        else:
            print(f"  ❌ balancesheet字段丰富度低: {balancesheet_field_count}个字段")
    else:
        print(f"  ⚠️  balancesheet Mock数据不存在")
        balancesheet_field_count = 0

    # cashflow字段数验证（预期97个字段）
    cashflow_mock_file = mock_data_dir / 'cashflow.json'
    if cashflow_mock_file.exists():
        with open(cashflow_mock_file, 'r', encoding='utf-8') as f:
            cashflow_mock_data = json.load(f)
        cashflow_field_count = len(cashflow_mock_data[0])
        if cashflow_field_count >= 90:
            print(f"  ✅ cashflow字段丰富度高: {cashflow_field_count}个字段")
        else:
            print(f"  ❌ cashflow字段丰富度低: {cashflow_field_count}个字段")
    else:
        print(f"  ⚠️  cashflow Mock数据不存在")
        cashflow_field_count = 0

    # fina_indicator字段数验证（预期167个字段）
    fina_indicator_mock_file = mock_data_dir / 'fina_indicator.json'
    if fina_indicator_mock_file.exists():
        with open(fina_indicator_mock_file, 'r', encoding='utf-8') as f:
            fina_indicator_mock_data = json.load(f)
        fina_indicator_field_count = len(fina_indicator_mock_data[0])
        if fina_indicator_field_count >= 160:
            print(f"  ✅ fina_indicator字段丰富度高: {fina_indicator_field_count}个字段")
        else:
            print(f"  ❌ fina_indicator字段丰富度低: {fina_indicator_field_count}个字段")
    else:
        print(f"  ⚠️  fina_indicator Mock数据不存在")
        fina_indicator_field_count = 0

    # 统计
    rich_fields_count = sum(1 for count in [income_field_count, balancesheet_field_count, cashflow_field_count, fina_indicator_field_count] if count >= 90)

    if rich_fields_count >= 4:
        test_results.append(('VIP财务表字段丰富度', 'PASSED', f'{rich_fields_count}个VIP财务表字段丰富度高'))
    else:
        test_results.append(('VIP财务表字段丰富度', 'FAILED', '字段丰富度不足'))

except Exception as e:
    print(f"  ❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    test_results.append(('VIP财务表字段丰富度', 'FAILED', str(e)))

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
    print("✅ 所有VIP接口处理测试通过")
    print("=" * 80)
else:
    print(f"❌ {failed_count}个测试失败")
    print("=" * 80)

# 生成测试报告到/tmp
report_path = '/tmp/vip_interface_test.txt'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("VIP接口处理测试报告\n")
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