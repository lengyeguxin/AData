#!/usr/bin/env python3
"""
批量测试剩余Collector数据拉取

测试14个待测Collector：
1. dividend
2. etf_adj_factor
3. etf_basic
4. etf_index
5. express
6. express_brief
7. hots_trader_detail
8. hots_user
9. ths_concept_member
10. ths_concept_moneyflow
11. ths_index_basic
12. ths_index_daily
13. ths_industry_moneyflow
14. ths_moneyflow
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'code' / 'backend'))

from src.core.database import Database
from src.core.tushare_api import TushareAPI
from src.core.logger import get_logger
import yaml

# 导入所有Collector
from src.collectors.dividend_collector import DividendCollector
from src.collectors.etf_adj_factor_collector import ETFAdjFactorCollector
from src.collectors.etf_basic_collector import ETFBasicCollector
from src.collectors.etf_index_collector import ETFIndexCollector
from src.collectors.express_collector import ExpressCollector
from src.collectors.express_brief_collector import ExpressBriefCollector
from src.collectors.hots_trader_detail_collector import HotsTraderDetailCollector
from src.collectors.hots_user_collector import HotsUserCollector
from src.collectors.ths_concept_member_collector import THSConceptMemberCollector
from src.collectors.ths_concept_moneyflow_collector import THSConceptMoneyflowCollector
from src.collectors.ths_index_basic_collector import THSIndexBasicCollector
from src.collectors.ths_index_daily_collector import THSIndexDailyCollector
from src.collectors.ths_industry_moneyflow_collector import THSIndustryMoneyflowCollector
from src.collectors.ths_moneyflow_collector import THSMoneyflowCollector

logger = get_logger(__name__)

# 加载配置
config_path = Path(__file__).parent.parent / 'code' / 'backend' / 'config' / 'config.yaml'
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

db_path = 'database/adata.db'
api = TushareAPI(config['tushare'])
db = Database(db_path)

# 测试用例列表
test_cases = [
    {
        'name': 'dividend',
        'collector': DividendCollector(db_path, api),
        'test_type': 'date',
        'test_date': '20260409',
        'api_name': 'dividend'
    },
    {
        'name': 'etf_adj_factor',
        'collector': ETFAdjFactorCollector(db_path, api),
        'test_type': 'date',
        'test_date': '20260409',
        'api_name': 'etf_adj_factor'
    },
    {
        'name': 'etf_basic',
        'collector': ETFBasicCollector(db_path, api),
        'test_type': 'all',
        'api_name': 'etf_basic'
    },
    {
        'name': 'etf_index',
        'collector': ETFIndexCollector(db_path, api),
        'test_type': 'all',
        'api_name': 'etf_index'
    },
    {
        'name': 'express',
        'collector': ExpressCollector(db_path, api),
        'test_type': 'date',
        'test_date': '20260409',
        'api_name': 'forecast_vip'
    },
    {
        'name': 'express_brief',
        'collector': ExpressBriefCollector(db_path, api),
        'test_type': 'date',
        'test_date': '20260409',
        'api_name': 'express_vip'
    },
    {
        'name': 'hots_trader_detail',
        'collector': HotsTraderDetailCollector(db_path, api),
        'test_type': 'date',
        'test_date': '20260409',
        'api_name': 'hots_trader_detail'
    },
    {
        'name': 'hots_user',
        'collector': HotsUserCollector(db_path, api),
        'test_type': 'all',
        'api_name': 'hots_user'
    },
    {
        'name': 'ths_concept_member',
        'collector': THSConceptMemberCollector(db_path, api),
        'test_type': 'concept',
        'test_ts_code': '885472.TI',
        'api_name': 'ths_member'
    },
    {
        'name': 'ths_concept_moneyflow',
        'collector': THSConceptMoneyflowCollector(db_path, api),
        'test_type': 'date',
        'test_date': '20260409',
        'api_name': 'moneyflow_cnt_ths'
    },
    {
        'name': 'ths_index_basic',
        'collector': THSIndexBasicCollector(db_path, api),
        'test_type': 'all',
        'api_name': 'ths_index'
    },
    {
        'name': 'ths_index_daily',
        'collector': THSIndexDailyCollector(db_path, api),
        'test_type': 'date',
        'test_date': '20260409',
        'api_name': 'ths_daily'
    },
    {
        'name': 'ths_industry_moneyflow',
        'collector': THSIndustryMoneyflowCollector(db_path, api),
        'test_type': 'date',
        'test_date': '20260409',
        'api_name': 'moneyflow_ind_ths'
    },
    {
        'name': 'ths_moneyflow',
        'collector': THSMoneyflowCollector(db_path, api),
        'test_type': 'date',
        'test_date': '20260409',
        'api_name': 'moneyflow_ths'
    },
]

print("=" * 80)
print("批量测试剩余Collector数据拉取")
print("=" * 80)

results = []

for test_case in test_cases:
    name = test_case['name']
    collector = test_case['collector']
    test_type = test_case['test_type']
    api_name = test_case['api_name']

    print(f"\n测试Collector: {name}")
    print("-" * 80)
    print(f"API名称: {api_name}")
    print(f"测试类型: {test_type}")

    try:
        # 根据测试类型调用不同方法
        if test_type == 'all':
            # 无参数拉取（全量）
            print("拉取数据（无参数）...")
            data = collector.collect_all()
        elif test_type == 'date':
            # 按日期拉取
            test_date = test_case['test_date']
            print(f"拉取数据: trade_date={test_date}")
            data = collector.collect_by_date(test_date)
        elif test_type == 'concept':
            # 特殊测试（ths_concept_member）
            test_ts_code = test_case['test_ts_code']
            print(f"拉取数据: ts_code={test_ts_code}")
            data = collector.collect(ts_code=test_ts_code)
        else:
            print("未知测试类型，跳过")
            results.append({'name': name, 'status': 'skipped', 'count': 0})
            continue

        # 保存数据
        print(f"拉取数据: {len(data)}条")
        count = collector.save(data)
        print(f"入库数据: {count}条")

        # 验证数据库
        verify_count = db.execute(f"SELECT COUNT(*) FROM {name}")[0][0]
        print(f"数据库验证: {verify_count}条")

        if count == verify_count or (count > 0 and verify_count > 0):
            print(f"✅ {name}测试成功")
            results.append({'name': name, 'status': 'success', 'count': count})
        else:
            print(f"⚠️ {name}数据入库异常")
            results.append({'name': name, 'status': 'warning', 'count': count})

    except Exception as e:
        print(f"❌ {name}测试失败: {e}")
        results.append({'name': name, 'status': 'failed', 'error': str(e)})

print("\n" + "=" * 80)
print("测试结果汇总")
print("=" * 80)

success_count = sum(1 for r in results if r['status'] == 'success')
warning_count = sum(1 for r in results if r['status'] == 'warning')
failed_count = sum(1 for r in results if r['status'] == 'failed')

print(f"成功: {success_count}/{len(results)}")
print(f"警告: {warning_count}/{len(results)}")
print(f"失败: {failed_count}/{len(results)}")

print("\n详细结果:")
for r in results:
    status_emoji = {
        'success': '✅',
        'warning': '⚠️',
        'failed': '❌',
        'skipped': '⏭️'
    }.get(r['status'], '❓')

    if r['status'] == 'failed':
        print(f"{status_emoji} {r['name']}: {r.get('error', '未知错误')}")
    else:
        print(f"{status_emoji} {r['name']}: {r.get('count', 0)}条")

print("=" * 80)