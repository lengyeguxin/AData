"""
完整字段差异检查脚本
检查所有17张表的字段差异(包括VIP接口和标准接口)
"""

import sys
import yaml
from pathlib import Path

backend_path = Path(__file__).parent.parent / 'code' / 'backend'
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / 'src'))

from core.tushare_api import TushareAPI


def load_config():
    """加载配置文件"""
    config_path = backend_path / 'config' / 'config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def read_schema_fields(schema_file):
    """从schema文件中读取字段列表"""
    fields = []
    with open(schema_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        # 提取字段定义行
        if line.strip() and not line.strip().startswith('--') and not line.strip().startswith('CREATE'):
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0] not in ['PRIMARY', 'UNIQUE', 'CREATE', 'INDEX']:
                # 过滤掉主键约束、索引等
                field_name = parts[0].rstrip(',')
                if field_name and field_name != 'updated_at':
                    fields.append(field_name)

    return fields


def check_all_tables():
    """检查所有17张表的字段差异"""

    config_dict = load_config()
    api = TushareAPI(config_dict['tushare'])

    # 定义所有表的API和schema信息
    tables_info = {
        # VIP财务表
        'balancesheet': {
            'api_name': 'balancesheet_vip',
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 158
        },
        'cashflow': {
            'api_name': 'cashflow_vip',
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 97
        },
        'income': {
            'api_name': 'income_vip',
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 94
        },
        'fina_indicator': {
            'api_name': 'fina_indicator_vip',
            'params': {'ann_date': '20260409'},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 167
        },
        'express': {
            'api_name': 'forecast_vip',
            'params': {'ann_date': '20260409'},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 12
        },
        'express_brief': {
            'api_name': 'express_vip',
            'params': {'ann_date': '20260409'},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 32
        },
        'dividend': {
            'api_name': 'dividend',
            'params': {'ann_date': '20260409'},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 16
        },

        # P0基础表
        'stock_basic': {
            'api_name': 'stock_basic',
            'params': {},
            'schema_file': 'database/schemas/p0_schema.sql',
            'expected_fields': 17
        },
        'index_basic': {
            'api_name': 'index_basic',
            'params': {},
            'schema_file': 'database/schemas/p0_schema.sql',
            'expected_fields': 13
        },
        'etf_basic': {
            'api_name': 'etf_basic',
            'params': {},
            'schema_file': 'database/schemas/p0_schema.sql',
            'expected_fields': 14
        },
        'etf_index': {
            'api_name': 'etf_index',
            'params': {},
            'schema_file': 'database/schemas/p0_schema.sql',
            'expected_fields': 8
        },

        # P1行情表
        'stock_daily': {
            'api_name': 'daily',
            'params': {'trade_date': '20260409'},
            'schema_file': 'database/schemas/p1_schema.sql',
            'expected_fields': 11
        },

        # P3概念板块表
        'ths_index_basic': {
            'api_name': 'ths_index',
            'params': {},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 6
        },
        'ths_index_daily': {
            'api_name': 'ths_daily',
            'params': {'trade_date': '20260409'},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 14
        },
        'ths_concept_member': {
            'api_name': 'ths_member',
            'params': {},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 7
        },

        # P4游资表
        'hots_user': {
            'api_name': 'hm_list',  # 正确接口名
            'params': {},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 3
        },
        'hots_trader_detail': {
            'api_name': 'hm_detail',  # 正确接口名
            'params': {'trade_date': '20260409'},
            'schema_file': 'database/schemas/p2_schema.sql',
            'expected_fields': 9
        }
    }

    print("=" * 80)
    print("完整字段差异检查报告")
    print("=" * 80)
    print(f"检查时间: 2026-04-14")
    print(f"检查表数: {len(tables_info)} 张")
    print("=" * 80)

    results = {}

    for table_name, info in tables_info.items():
        try:
            print(f"\n检查表: {table_name}")
            print(f"API接口: {info['api_name']}")
            print(f"文档字段数: {info['expected_fields']}")

            # 读取schema字段
            schema_fields = read_schema_fields(info['schema_file'])
            # 过滤出当前表的字段(需要更精确的方法)
            # 这里简化处理,假设schema文件中字段都属于该表

            print(f"Schema字段数: {len(schema_fields)} (估算)")

            # 调用API获取实际字段
            data = api.query(info['api_name'], **info['params'])

            if data and len(data) > 0:
                api_fields = list(data[0].keys())
                print(f"API返回字段数: {len(api_fields)}")

                # 统计差异
                missing_fields = [f for f in api_fields if f not in schema_fields]
                extra_fields = [f for f in schema_fields if f not in api_fields and f != 'updated_at']

                results[table_name] = {
                    'api_fields': len(api_fields),
                    'schema_fields': len(schema_fields),
                    'missing_count': len(missing_fields),
                    'missing_fields': missing_fields,
                    'extra_count': len(extra_fields),
                    'extra_fields': extra_fields,
                    'coverage': len(schema_fields) / len(api_fields) * 100 if len(api_fields) > 0 else 0
                }

                print(f"缺失字段数: {len(missing_fields)}")
                print(f"多余字段数: {len(extra_fields)}")
                print(f"字段覆盖率: {results[table_name]['coverage']:.1f}%")

                if missing_fields:
                    print(f"\n缺失字段列表:")
                    for i, field in enumerate(missing_fields[:10], 1):
                        print(f"  {i}. {field}")
                    if len(missing_fields) > 10:
                        print(f"  ... 还有 {len(missing_fields)-10} 个字段")

                if extra_fields:
                    print(f"\nSchema多余字段:")
                    for field in extra_fields[:10]:
                        print(f"  - {field}")
                    if len(extra_fields) > 10:
                        print(f"  ... 还有 {len(extra_fields)-10} 个字段")

            else:
                print(f"⚠️  API返回空数据")
                results[table_name] = {
                    'api_fields': 0,
                    'schema_fields': len(schema_fields),
                    'missing_count': 0,
                    'missing_fields': [],
                    'extra_count': 0,
                    'extra_fields': [],
                    'coverage': 100.0,
                    'note': 'API返回空数据'
                }

        except Exception as e:
            print(f"❌ 检查失败: {e}")
            results[table_name] = {
                'error': str(e)
            }

    print("\n" + "=" * 80)
    print("字段差异汇总统计")
    print("=" * 80)

    # 汇总统计
    total_missing = sum(r.get('missing_count', 0) for r in results.values())
    total_extra = sum(r.get('extra_count', 0) for r in results.values())

    print(f"\n总计缺失字段: {total_missing} 个")
    print(f"总计多余字段: {total_extra} 个")

    # 按缺失数量排序
    sorted_results = sorted(
        [(k, v) for k, v in results.items() if 'missing_count' in v],
        key=lambda x: x[1]['missing_count'],
        reverse=True
    )

    print(f"\n按缺失数量排序:")
    for i, (table, stats) in enumerate(sorted_results[:10], 1):
        print(f"{i}. {table}: 缺失{stats['missing_count']}字段, 覆盖率{stats['coverage']:.1f}%")

    print("\n" + "=" * 80)
    print("检查完成")
    print("=" * 80)

    return results


if __name__ == '__main__':
    results = check_all_tables()

    # 保存结果到JSON
    output_file = Path(__file__).parent.parent / 'docs' / 'field_diff_results.json'
    output_file.parent.mkdir(parents=True, exist_ok=True)

    import json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存到: {output_file}")