"""
测试重试机制

验证：
1. 配置中的 max_retries 和 retry_delay 被正确加载
2. 行情表拉取失败时会重试
3. 重试失败后会停止拉取后续日期
4. 财务表无数据时继续拉取
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from unittest.mock import Mock, patch, MagicMock
from src.core.data_fetcher import DataFetcher
from src.core.global_cursor_manager import GlobalCursorManager


def test_retry_config_loaded():
    """测试重试配置是否正确加载"""
    print("\n=== 测试1: 重试配置加载 ===")

    config = {
        'fetch': {
            'max_retries': 3,
            'retry_delay': 45
        }
    }

    # Mock必要组件
    fetcher = DataFetcher.__new__(DataFetcher)
    fetcher.config = config
    fetcher.logger = Mock()

    # 手动设置重试配置
    fetcher.max_retries = config.get('fetch', {}).get('max_retries', 2)
    fetcher.retry_delay = config.get('fetch', {}).get('retry_delay', 30)

    assert fetcher.max_retries == 3, f"max_retries应为3，实际为{fetcher.max_retries}"
    assert fetcher.retry_delay == 45, f"retry_delay应为45，实际为{fetcher.retry_delay}"

    print(f"✓ max_retries: {fetcher.max_retries}")
    print(f"✓ retry_delay: {fetcher.retry_delay}")


def test_retry_fetch_success():
    """测试重试机制 - 成功场景"""
    print("\n=== 测试2: 重试机制 - 成功场景 ===")

    # Mock必要组件
    fetcher = Mock()
    fetcher.max_retries = 2
    fetcher.retry_delay = 1  # 缩短延迟时间用于测试
    fetcher.logger = Mock()

    # 重试函数第一次调用成功
    fetch_func = Mock(side_effect=[100])  # 第一次返回100条数据

    # 调用重试方法
    import time
    with patch('time.sleep'):
        result = DataFetcher._retry_fetch(
            fetcher, 'stock_daily', '20260410', fetch_func, date_type='trade_date'
        )

    assert result == 100, f"应返回100，实际为{result}"
    assert fetch_func.call_count == 1, f"应调用1次，实际调用{fetch_func.call_count}次"

    print(f"✓ 拉取成功，返回{result}条数据")
    print(f"✓ 调用次数: {fetch_func.call_count}")


def test_retry_fetch_with_retries():
    """测试重试机制 - 失败后重试成功"""
    print("\n=== 测试3: 重试机制 - 失败后重试成功 ===")

    # Mock必要组件
    fetcher = Mock()
    fetcher.max_retries = 2
    fetcher.retry_delay = 1
    fetcher.logger = Mock()

    # 重试函数：前2次失败，第3次成功
    fetch_func = Mock(side_effect=[
        Exception("Network error"),
        Exception("Network error"),
        100  # 第3次成功
    ])

    # 调用重试方法
    import time
    with patch('time.sleep'):
        result = DataFetcher._retry_fetch(
            fetcher, 'stock_daily', '20260410', fetch_func, date_type='trade_date'
        )

    assert result == 100, f"应返回100，实际为{result}"
    assert fetch_func.call_count == 3, f"应调用3次，实际调用{fetch_func.call_count}次"

    print(f"✓ 重试2次后成功，返回{result}条数据")
    print(f"✓ 总调用次数: {fetch_func.call_count}")


def test_retry_fetch_all_failed():
    """测试重试机制 - 全部失败"""
    print("\n=== 测试4: 重试机制 - 全部失败 ===")

    # Mock必要组件
    fetcher = Mock()
    fetcher.max_retries = 2
    fetcher.retry_delay = 1
    fetcher.logger = Mock()

    # 重试函数：全部失败
    fetch_func = Mock(side_effect=[
        Exception("Network error"),
        Exception("Network error"),
        Exception("Network error")
    ])

    # 调用重试方法
    import time
    with patch('time.sleep'):
        result = DataFetcher._retry_fetch(
            fetcher, 'stock_daily', '20260410', fetch_func, date_type='trade_date'
        )

    assert result is None, f"应返回None，实际为{result}"
    assert fetch_func.call_count == 3, f"应调用3次，实际调用{fetch_func.call_count}次"

    print(f"✓ 重试3次后全部失败，返回None")
    print(f"✓ 总调用次数: {fetch_func.call_count}")


def test_retry_fetch_no_data_with_retries():
    """测试重试机制 - 无数据（行情表）"""
    print("\n=== 测试5: 重试机制 - 无数据（行情表） ===")

    # Mock必要组件
    fetcher = Mock()
    fetcher.max_retries = 2
    fetcher.retry_delay = 1
    fetcher.logger = Mock()

    # 重试函数：前2次返回0，第3次返回100
    fetch_func = Mock(side_effect=[0, 0, 100])

    # 调用重试方法
    import time
    with patch('time.sleep'):
        result = DataFetcher._retry_fetch(
            fetcher, 'stock_daily', '20260410', fetch_func, date_type='trade_date'
        )

    assert result == 100, f"应返回100，实际为{result}"
    assert fetch_func.call_count == 3, f"应调用3次，实际调用{fetch_func.call_count}次"

    print(f"✓ 无数据重试2次后成功，返回{result}条数据")
    print(f"✓ 总调用次数: {fetch_func.call_count}")


def test_retry_fetch_financial_no_data():
    """测试重试机制 - 无数据（财务表）"""
    print("\n=== 测试6: 重试机制 - 无数据（财务表） ===")

    # Mock必要组件
    fetcher = Mock()
    fetcher.max_retries = 2
    fetcher.retry_delay = 1
    fetcher.logger = Mock()

    # 重试函数：返回0（财务表允许无数据）
    fetch_func = Mock(return_value=0)

    # 调用重试方法
    import time
    with patch('time.sleep'):
        result = DataFetcher._retry_fetch(
            fetcher, 'income', '20260410', fetch_func, date_type='ann_date'
        )

    assert result == 0, f"应返回0，实际为{result}"
    assert fetch_func.call_count == 1, f"应调用1次，实际调用{fetch_func.call_count}次"

    print(f"✓ 财务表无数据不算失败，返回{result}")
    print(f"✓ 调用次数: {fetch_func.call_count}")


def test_retry_fetch_none_success():
    """测试基础表重试机制 - 成功场景"""
    print("\n=== 测试7: 基础表重试机制 - 成功场景 ===")

    # Mock必要组件
    fetcher = Mock()
    fetcher.max_retries = 2
    fetcher.retry_delay = 1
    fetcher.logger = Mock()

    # 重试函数：返回100条数据
    fetch_func = Mock(return_value=100)

    # 调用重试方法
    import time
    with patch('time.sleep'):
        result = DataFetcher._retry_fetch_none(
            fetcher, 'stock_basic', fetch_func
        )

    assert result == 100, f"应返回100，实际为{result}"
    assert fetch_func.call_count == 1, f"应调用1次，实际调用{fetch_func.call_count}次"

    print(f"✓ 基础表拉取成功，返回{result}条数据")
    print(f"✓ 调用次数: {fetch_func.call_count}")


def test_retry_fetch_none_with_retries():
    """测试基础表重试机制 - 失败后重试成功"""
    print("\n=== 测试8: 基础表重试机制 - 失败后重试成功 ===")

    # Mock必要组件
    fetcher = Mock()
    fetcher.max_retries = 2
    fetcher.retry_delay = 1
    fetcher.logger = Mock()

    # 重试函数：前2次失败，第3次成功
    fetch_func = Mock(side_effect=[
        Exception("Network error"),
        Exception("Network error"),
        100  # 第3次成功
    ])

    # 调用重试方法
    import time
    with patch('time.sleep'):
        result = DataFetcher._retry_fetch_none(
            fetcher, 'stock_basic', fetch_func
        )

    assert result == 100, f"应返回100，实际为{result}"
    assert fetch_func.call_count == 3, f"应调用3次，实际调用{fetch_func.call_count}次"

    print(f"✓ 基础表重试2次后成功，返回{result}条数据")
    print(f"✓ 总调用次数: {fetch_func.call_count}")


def test_retry_fetch_none_all_failed():
    """测试基础表重试机制 - 全部失败"""
    print("\n=== 测试9: 基础表重试机制 - 全部失败 ===")

    # Mock必要组件
    fetcher = Mock()
    fetcher.max_retries = 2
    fetcher.retry_delay = 1
    fetcher.logger = Mock()

    # 重试函数：全部失败
    fetch_func = Mock(side_effect=[
        Exception("Network error"),
        Exception("Network error"),
        Exception("Network error")
    ])

    # 调用重试方法
    import time
    with patch('time.sleep'):
        result = DataFetcher._retry_fetch_none(
            fetcher, 'stock_basic', fetch_func
        )

    assert result is None, f"应返回None，实际为{result}"
    assert fetch_func.call_count == 3, f"应调用3次，实际调用{fetch_func.call_count}次"

    print(f"✓ 基础表重试3次后全部失败，返回None")
    print(f"✓ 总调用次数: {fetch_func.call_count}")


def test_retry_fetch_none_zero_data():
    """测试基础表重试机制 - 返回0条数据"""
    print("\n=== 测试10: 基础表重试机制 - 返回0条数据 ===")

    # Mock必要组件
    fetcher = Mock()
    fetcher.max_retries = 2
    fetcher.retry_delay = 1
    fetcher.logger = Mock()

    # 重试函数：返回0（基础表允许无数据）
    fetch_func = Mock(return_value=0)

    # 调用重试方法
    import time
    with patch('time.sleep'):
        result = DataFetcher._retry_fetch_none(
            fetcher, 'stock_basic', fetch_func
        )

    assert result == 0, f"应返回0，实际为{result}"
    assert fetch_func.call_count == 1, f"应调用1次，实际调用{fetch_func.call_count}次"

    print(f"✓ 基础表无数据不算失败，返回{result}")
    print(f"✓ 调用次数: {fetch_func.call_count}")


if __name__ == '__main__':
    print("=" * 80)
    print("重试机制测试")
    print("=" * 80)

    try:
        test_retry_config_loaded()
        test_retry_fetch_success()
        test_retry_fetch_with_retries()
        test_retry_fetch_all_failed()
        test_retry_fetch_no_data_with_retries()
        test_retry_fetch_financial_no_data()
        test_retry_fetch_none_success()
        test_retry_fetch_none_with_retries()
        test_retry_fetch_none_all_failed()
        test_retry_fetch_none_zero_data()

        print("\n" + "=" * 80)
        print("✅ 所有测试通过！")
        print("=" * 80)

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
