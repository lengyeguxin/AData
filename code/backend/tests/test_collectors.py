#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collector功能测试脚本

测试Collector类的核心功能：
1. Collector初始化
2. 数据转换（transform）
3. 数据保存（save，使用模拟数据）
4. 游标更新逻辑
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / 'code' / 'backend'))

from datetime import datetime
from typing import Dict
import duckdb

from src.collectors import StockBasicCollector, TradeCalendarCollector, DailyCollector, IncomeCollector
from src.core.tushare_api import TushareAPI
from src.core.global_cursor_manager import GlobalCursorManager
from src.core.logger import get_logger


def test_collectors():
    """
    测试Collector类（使用模拟数据，避免消耗API积分）
    """
    print("=" * 80)
    print("Collector功能测试")
    print("=" * 80)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    logger = get_logger(__name__)
    db_path = 'database/adata.db'

    # 初始化TushareAPI（使用配置，但不实际调用）
    config = {
        'token': 'test_token',
        'api_url': 'http://api.tushare.pro',
        'rate_limit': 500
    }
    api = TushareAPI(config)

    # 初始化GlobalCursorManager
    cursor_manager = GlobalCursorManager(db_path, 'code/backend/config')

    test_results = []

    # ========================================
    # 测试1: StockBasicCollector初始化
    # ========================================
    print("测试1: StockBasicCollector初始化...")
    try:
        collector = StockBasicCollector(db_path, api)
        print(f"  ✅ 初始化成功")
        print(f"    table_name: {collector.table_name}")
        print(f"    api_name: {collector.api_name}")
        print(f"    vip_interface: {collector.vip_interface}")

        test_results.append(('StockBasicCollector初始化', 'PASSED', '初始化成功'))

    except Exception as e:
        print(f"  ❌ 初始化失败: {e}")
        test_results.append(('StockBasicCollector初始化', 'FAILED', str(e)))

    print()

    # ========================================
    # 测试2: TradeCalendarCollector初始化
    # ========================================
    print("测试2: TradeCalendarCollector初始化...")
    try:
        collector = TradeCalendarCollector(db_path, api)
        print(f"  ✅ 初始化成功")
        print(f"    table_name: {collector.table_name}")
        print(f"    api_name: {collector.api_name}")

        test_results.append(('TradeCalendarCollector初始化', 'PASSED', '初始化成功'))

    except Exception as e:
        print(f"  ❌ 初始化失败: {e}")
        test_results.append(('TradeCalendarCollector初始化', 'FAILED', str(e)))

    print()

    # ========================================
    # 测试3: DailyCollector初始化
    # ========================================
    print("测试3: DailyCollector初始化...")
    try:
        collector = DailyCollector(db_path, api)
        print(f"  ✅ 初始化成功")
        print(f"    table_name: {collector.table_name}")
        print(f"    api_name: {collector.api_name}")
        print(f"    date_field: {collector.date_field}")

        test_results.append(('DailyCollector初始化', 'PASSED', '初始化成功'))

    except Exception as e:
        print(f"  ❌ 初始化失败: {e}")
        test_results.append(('DailyCollector初始化', 'FAILED', str(e)))

    print()

    # ========================================
    # 测试4: IncomeCollector初始化（VIP接口）
    # ========================================
    print("测试4: IncomeCollector初始化（VIP接口）...")
    try:
        collector = IncomeCollector(db_path, api)
        print(f"  ✅ 初始化成功")
        print(f"    table_name: {collector.table_name}")
        print(f"    api_name: {collector.api_name}")
        print(f"    vip_interface: {collector.vip_interface}（VIP接口）")

        test_results.append(('IncomeCollector初始化', 'PASSED', 'VIP接口初始化成功'))

    except Exception as e:
        print(f"  ❌ 初始化失败: {e}")
        test_results.append(('IncomeCollector初始化', 'FAILED', str(e)))

    print()

    # ========================================
    # 测试5: 数据转换（transform）
    # ========================================
    print("测试5: 数据转换（transform）...")

    # 使用模拟数据
    mock_data_stock_basic = [
        {'ts_code': '000001.SZ', 'name': '平安银行', 'industry': '银行', 'market': 'SZSE', 'list_date': '19910403'}
    ]

    try:
        collector = StockBasicCollector(db_path, api)
        records = collector.transform(mock_data_stock_basic)

        print(f"  ✅ 转换成功")
        print(f"    输入数据: 1条")
        print(f"    输出记录: {len(records)}条")
        print(f"    字段值示例: ts_code={records[0][0]}, name={records[0][1]}")

        # 验证日期转换
        if records[0][4] == '1991-04-03':  # list_date转换
            print(f"    ✅ 日期转换正确: 19910403 → 1991-04-03")
            test_results.append(('数据转换', 'PASSED', '日期格式转换正确'))
        else:
            print(f"    ❌ 日期转换错误: {records[0][4]}")
            test_results.append(('数据转换', 'FAILED', f'日期转换错误={records[0][4]}'))

    except Exception as e:
        print(f"  ❌ 转换失败: {e}")
        test_results.append(('数据转换', 'FAILED', str(e)))

    print()

    # ========================================
    # 测试6: 数据保存（save，使用模拟数据）
    # ========================================
    print("测试6: 数据保存（save，使用模拟数据）...")

    # 使用模拟数据（避免调用真实API）
    mock_data_trade_calendar = [
        {'exchange': 'SSE', 'cal_date': '20260411', 'is_open': '1', 'pretrade_date': '20260410'}
    ]

    try:
        collector = TradeCalendarCollector(db_path, api)
        count = collector.save(mock_data_trade_calendar)

        print(f"  ✅ 保存成功")
        print(f"    保存记录数: {count}")

        # 验证数据库写入
        conn = duckdb.connect(db_path, read_only=True)
        result = conn.execute("SELECT COUNT(*) FROM trade_calendar WHERE cal_date = '2026-04-11'").fetchone()
        conn.close()

        if result[0] > 0:
            print(f"    ✅ 数据库验证成功: {result[0]}条记录")
            test_results.append(('数据保存', 'PASSED', '数据库写入成功'))
        else:
            print(f"    ❌ 数据库验证失败: 未找到记录")
            test_results.append(('数据保存', 'FAILED', '数据库未写入'))

    except Exception as e:
        print(f"  ❌ 保存失败: {e}")
        test_results.append(('数据保存', 'FAILED', str(e)))

    print()

    # ========================================
    # 测试7: 游标更新逻辑
    # ========================================
    print("测试7: 游标更新逻辑...")
    try:
        # 更新trade_calendar游标（yearly策略）
        cursor_manager.update_cursor('trade_calendar', '2026', 1)

        cursor = cursor_manager.get_cursor('trade_calendar')
        print(f"  ✅ 游标更新成功")
        print(f"    cursor_value: {cursor['cursor_value']}")
        print(f"    status: {cursor['status']}")
        print(f"    last_record_count: {cursor['last_record_count']}")

        if cursor['cursor_value'] == '2026' and cursor['status'] == 'success':
            print(f"    ✅ 游标值正确")
            test_results.append(('游标更新', 'PASSED', '游标值正确'))
        else:
            print(f"    ❌ 游标值错误")
            test_results.append(('游标更新', 'FAILED', f'游标值={cursor["cursor_value"]}'))

    except Exception as e:
        print(f"  ❌ 游标更新失败: {e}")
        test_results.append(('游标更新', 'FAILED', str(e)))

    print()

    # ========================================
    # 测试8: VIP接口验证
    # ========================================
    print("测试8: VIP接口验证...")
    try:
        income_collector = IncomeCollector(db_path, api)

        # 检查VIP接口名称
        if income_collector.api_name == 'income_vip':
            print(f"  ✅ VIP接口名称正确: income_vip")
            test_results.append(('VIP接口验证', 'PASSED', 'income_vip正确'))
        else:
            print(f"  ❌ VIP接口名称错误: {income_collector.api_name}")
            test_results.append(('VIP接口验证', 'FAILED', f'接口名称={income_collector.api_name}'))

        # 检查VIP接口标记
        if income_collector.vip_interface:
            print(f"  ✅ VIP接口标记正确: vip_interface=True")
        else:
            print(f"  ❌ VIP接口标记错误")

    except Exception as e:
        print(f"  ❌ VIP接口验证失败: {e}")
        test_results.append(('VIP接口验证', 'FAILED', str(e)))

    print()

    # ========================================
    # 测试9: check_data_exists
    # ========================================
    print("测试9: check_data_exists（数据存在性检查）...")
    try:
        collector = TradeCalendarCollector(db_path, api)

        # 检查刚才插入的数据
        exists = collector.check_data_exists(cal_date='20260411')

        if exists:
            print(f"  ✅ 数据存在性检查正确: cal_date=20260411存在")
            test_results.append(('check_data_exists', 'PASSED', '数据存在性检查正确'))
        else:
            print(f"  ❌ 数据存在性检查错误: cal_date=20260411不存在")
            test_results.append(('check_data_exists', 'FAILED', '数据不存在'))

    except Exception as e:
        print(f"  ❌ 数据存在性检查失败: {e}")
        test_results.append(('check_data_exists', 'FAILED', str(e)))

    print()

    # ========================================
    # 生成测试报告
    # ========================================
    generate_test_report(test_results)


def generate_test_report(test_results: list):
    """
    生成测试报告（保存到/tmp）

    Args:
        test_results: 测试结果列表
    """
    report_path = "/tmp/collector_test_report.txt"

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("Collector功能测试报告\n")
        f.write("=" * 80 + "\n")
        f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n")

        f.write("测试结果汇总:\n")
        f.write("-" * 80 + "\n")

        passed_count = sum(1 for r in test_results if r[1] == 'PASSED')
        failed_count = sum(1 for r in test_results if r[1] == 'FAILED')

        f.write(f"通过: {passed_count}\n")
        f.write(f"失败: {failed_count}\n")
        f.write(f"总计: {len(test_results)}\n")
        f.write("\n")

        f.write("详细测试结果:\n")
        f.write("-" * 80 + "\n")

        for test_name, status, message in test_results:
            status_icon = '✅' if status == 'PASSED' else '❌'
            f.write(f"{status_icon} {test_name}: {status}\n")
            f.write(f"   {message}\n")
            f.write("\n")

        f.write("=" * 80 + "\n")

        if failed_count == 0:
            f.write("测试状态: PASSED\n")
        else:
            f.write("测试状态: FAILED\n")

        f.write("=" * 80 + "\n")

    print("=" * 80)
    print("✅ Collector功能测试完成")
    print("=" * 80)
    print()
    print(f"📋 测试报告已生成: {report_path}")
    print()


if __name__ == "__main__":
    test_collectors()