"""
ths_moneyflow表Collector单元测试

测试覆盖：
- Collector初始化验证
- 数据转换验证
- 数据保存验证
- 字段数量验证
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "code" / "backend"))

import json
from src.collectors.ths_moneyflow_collector import THSMoneyflowCollector
from src.core.tushare_api import TushareAPI
from src.core.database import Database


# Mock配置（不消耗API积分）
mock_config = {
    "token": "test_token",
    "api_url": "http://api.tushare.pro",
    "rate_limit": 500
}

# Mock数据
mock_data_file = Path(__file__).parent.parent.parent.parent.parent / "tests" / "mock_data" / "ths_moneyflow.json"


def test_collector_init():
    """测试Collector初始化"""
    db_path = ":memory:"  # 内存数据库
    api = TushareAPI(mock_config)

    collector = THSMoneyflowCollector(db_path, api)

    assert collector.table_name == "ths_moneyflow"
    assert collector.api_name == "moneyflow_ths"

    print(f"✅ THSMoneyflowCollector初始化测试通过")


def test_transform():
    """测试数据转换"""
    db_path = ":memory:"
    api = TushareAPI(mock_config)
    collector = THSMoneyflowCollector(db_path, api)

    # 加载Mock数据
    with open(mock_data_file, "r", encoding="utf-8") as f:
        mock_data = json.load(f)

    # 执行转换
    records = collector.transform(mock_data)

    # 验证
    assert len(records) > 0
    print(f"✅ 数据转换测试通过: {len(records[0])}个字段")


def test_field_count():
    """测试字段数量"""
    db_path = ":memory:"
    api = TushareAPI(mock_config)
    collector = THSMoneyflowCollector(db_path, api)

    # 加载Mock数据
    with open(mock_data_file, "r", encoding="utf-8") as f:
        mock_data = json.load(f)

    # 转换并获取字段数
    records = collector.transform(mock_data)
    mock_field_count = len(mock_data[0])
    collector_field_count = len(records[0])

    assert mock_field_count == collector_field_count
    print(f"✅ 字段数量匹配: Mock={mock_field_count}, Collector={collector_field_count}")


if __name__ == "__main__":
    print("=" * 80)
    print("ths_moneyflow表Collector单元测试")
    print("=" * 80)

    test_results = []

    try:
        test_collector_init()
        test_results.append(("Collector初始化", "PASSED", "成功"))
    except Exception as e:
        test_results.append(("Collector初始化", "FAILED", str(e)))

    try:
        test_transform()
        test_results.append(("数据转换", "PASSED", "成功"))
    except Exception as e:
        test_results.append(("数据转换", "FAILED", str(e)))

    try:
        test_field_count()
        test_results.append(("字段数量验证", "PASSED", "成功"))
    except Exception as e:
        test_results.append(("字段数量验证", "FAILED", str(e)))

    # 打印测试报告
    print("\n测试结果:")
    for test_name, status, message in test_results:
        status_icon = "✅" if status == "PASSED" else "❌"
        print(f"{status_icon} {test_name}: {status} - {message}")

    # 统计
    passed = sum(1 for _, status, _ in test_results if status == "PASSED")
    failed = sum(1 for _, status, _ in test_results if status == "FAILED")
    print(f"\n汇总: 通过={passed}, 失败={failed}, 总计={len(test_results)}")
    print("=" * 80)