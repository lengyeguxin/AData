"""
生成完整Schema文件脚本
根据API返回的完整字段列表生成schema定义，保持API字段顺序
"""

import json
import re
from pathlib import Path

backend_path = Path(__file__).parent.parent / 'code' / 'backend'
import sys
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / 'src'))

import yaml
from core.tushare_api import TushareAPI


def load_config():
    """加载配置"""
    config_path = backend_path / 'config' / 'config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def infer_field_type(field_name):
    """推断字段SQL类型"""
    # 日期字段
    if field_name.endswith('_date') or field_name == 'date':
        return 'DATE'

    # 数值字段(财务数据大多是数值)
    numeric_patterns = [
        'amount', 'vol', 'ratio', 'rate', 'margin', 'yield', 'cost', 'exp',
        'income', 'profit', 'assets', 'liab', 'equity', 'capital', 'share',
        'eps', 'bps', 'roe', 'roa', 'pe', 'pb', 'mv', 'price', 'fee', 'div',
        'tax', 'pay', 'recp', 'cash', 'flow', 'depos', 'loan', 'bond', 'invest',
        'turn', 'days', 'num', 'count', 'chg', 'change'
    ]

    for pattern in numeric_patterns:
        if pattern in field_name.lower():
            return 'REAL'

    # 字符串字段
    string_patterns = {
        'name': 'VARCHAR(100)',
        'code': 'VARCHAR(10)',
        'type': 'VARCHAR(20)',
        'status': 'VARCHAR(10)',
        'reason': 'VARCHAR(500)',
        'desc': 'TEXT',
        'summary': 'VARCHAR(500)',
        'exchange': 'VARCHAR(10)',
        'industry': 'VARCHAR(50)',
        'market': 'VARCHAR(20)',
        'flag': 'VARCHAR(10)',
        'license': 'VARCHAR(20)',
        'orgs': 'VARCHAR(200)',
    }

    for pattern, sql_type in string_patterns.items():
        if pattern in field_name.lower():
            return sql_type

    # 默认数值型
    return 'REAL'


def get_field_comment(field_name):
    """获取字段中文注释"""
    # 基础字段注释
    base_comments = {
        'ts_code': 'TS代码',
        'trade_date': '交易日期',
        'ann_date': '公告日期',
        'end_date': '报告期',
        'report_type': '报告类型',
        'comp_type': '公司类型',
        'update_flag': '更新标识',
        'name': '名称',
        'total_share': '总股本',
        'surplus_rese': '盈余公积',
        'special_rese': '专项储备',
        'oth_receiv': '其他应收款',
        'prepayment': '预付款项',
        'lt_rec': '长期应收款',
        'intan_assets': '无形资产',
        'fixed_assets_disp': '固定资产清理',
        'produc_bio_assets': '生产性生物资产',
        'oil_and_gas_assets': '油气资产',
        'r_and_d': '研发支出',
        'lt_amor_exp': '长期待摊费用',
        'use_right_assets': '使用权资产',
        'lease_liab': '租赁负债',
        'contract_assets': '合同资产',
        'contract_liab': '合同负债',
        'net_profit': '净利润',
        'finan_exp': '财务费用',
        'int_income': '利息收入',
        'invest_income': '投资收益',
        'credit_impa_loss': '信用减值损失',
        'continued_net_profit': '持续经营净利润',
        'end_net_profit': '终止经营净利润',
        'netprofit_margin': '净利润率',
        'grossprofit_margin': '毛利润率',
    }

    if field_name in base_comments:
        return base_comments[field_name]

    # 推断注释
    if 'amount' in field_name:
        return '金额'
    if 'income' in field_name:
        return '收入'
    if 'exp' in field_name and 'income' not in field_name:
        return '费用'
    if 'assets' in field_name:
        return '资产'
    if 'liab' in field_name:
        return '负债'
    if 'pay' in field_name or 'payable' in field_name:
        return '应付'
    if 'receiv' in field_name or 'recp' in field_name:
        return '应收'

    return ''  # 无注释


def generate_table_definition(api, table_config):
    """生成单张表的完整定义"""
    api_name = table_config['api_name']
    params = table_config['params']
    primary_key = table_config.get('primary_key', [])
    indexes = table_config.get('indexes', [])

    print(f"  获取API字段: {api_name}")

    # 调用API获取完整字段列表
    data = api.query(api_name, **params)
    if not data or len(data) == 0:
        print(f"  ⚠️ API返回空数据，无法获取字段列表")
        return None

    api_fields = list(data[0].keys())
    print(f"  ✓ API字段数: {len(api_fields)}")

    # 生成表定义SQL
    sql_lines = []
    sql_lines.append(f"-- {table_config['table_name']} ({table_config.get('desc', '')})")
    sql_lines.append(f"-- API接口: {api_name}")
    sql_lines.append(f"-- API字段数: {len(api_fields)}")
    sql_lines.append(f"CREATE TABLE IF NOT EXISTS {table_config['table_name']} (")

    # 按API返回顺序生成字段定义
    for i, field in enumerate(api_fields):
        sql_type = infer_field_type(field)
        comment = get_field_comment(field)

        # 判断是否主键字段
        is_pk = field in primary_key
        pk_suffix = ' PRIMARY KEY' if is_pk and len(primary_key) == 1 else ''

        # 生成字段定义
        if comment:
            sql_lines.append(f"    {field} {sql_type}{pk_suffix},  -- {comment}")
        else:
            sql_lines.append(f"    {field} {sql_type}{pk_suffix},  -- {field}")

    # 添加updated_at字段
    sql_lines.append("    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间")

    # 复合主键定义
    if len(primary_key) > 1:
        pk_fields = ', '.join(primary_key)
        sql_lines.append(f"    PRIMARY KEY ({pk_fields}),")

    sql_lines.append(");")

    # 创建索引
    for index_name, index_fields in indexes:
        sql_lines.append(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_config['table_name']}({', '.join(index_fields)});")

    return '\n'.join(sql_lines)


def main():
    """主函数"""
    print("=" * 60)
    print("生成完整Schema文件")
    print("=" * 60)

    config = load_config()
    api = TushareAPI(config['tushare'])

    # 定义所有表的配置
    tables_config = {
        # P0基础表
        'stock_basic': {
            'api_name': 'stock_basic',
            'params': {},
            'primary_key': ['ts_code'],
            'indexes': [('idx_stock_basic_code', ['ts_code'])],
            'desc': '股票列表'
        },
        'index_basic': {
            'api_name': 'index_basic',
            'params': {},
            'primary_key': ['ts_code'],
            'indexes': [('idx_index_basic_code', ['ts_code'])],
            'desc': '指数列表'
        },
        'etf_basic': {
            'api_name': 'etf_basic',
            'params': {},
            'primary_key': ['ts_code'],
            'indexes': [('idx_etf_basic_code', ['ts_code'])],
            'desc': 'ETF基本信息'
        },
        'etf_index': {
            'api_name': 'etf_index',
            'params': {},
            'primary_key': ['ts_code'],
            'indexes': [('idx_etf_index_code', ['ts_code'])],
            'desc': 'ETF基准指数'
        },

        # P2财务表
        'balancesheet': {
            'api_name': 'balancesheet_vip',
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'primary_key': ['ts_code', 'end_date', 'report_type'],
            'indexes': [
                ('idx_balance_date', ['end_date']),
                ('idx_balance_code', ['ts_code'])
            ],
            'desc': '资产负债表'
        },
        'income': {
            'api_name': 'income_vip',
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'primary_key': ['ts_code', 'end_date', 'report_type'],
            'indexes': [
                ('idx_income_date', ['end_date']),
                ('idx_income_code', ['ts_code'])
            ],
            'desc': '利润表'
        },
        'cashflow': {
            'api_name': 'cashflow_vip',
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'primary_key': ['ts_code', 'end_date', 'report_type'],
            'indexes': [
                ('idx_cashflow_date', ['end_date']),
                ('idx_cashflow_code', ['ts_code'])
            ],
            'desc': '现金流量表'
        },
        'fina_indicator': {
            'api_name': 'fina_indicator_vip',
            'params': {'ann_date': '20260409'},
            'primary_key': ['ts_code', 'end_date'],
            'indexes': [
                ('idx_fina_date', ['ann_date']),
                ('idx_fina_code', ['ts_code'])
            ],
            'desc': '财务指标'
        },
    }

    # 输出目录
    output_dir = Path('database/schemas_new')
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成每张表的定义
    for table_name, config in tables_config.items():
        print(f"\n生成表定义: {table_name}")
        config['table_name'] = table_name

        sql = generate_table_definition(api, config)
        if sql:
            output_file = output_dir / f'{table_name}_schema.sql'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(sql)

            print(f"  ✓ 已保存: {output_file}")

    print("\n" + "=" * 60)
    print("✓ Schema文件生成完成")
    print("=" * 60)


if __name__ == '__main__':
    main()