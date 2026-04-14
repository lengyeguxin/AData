"""
生成所有27张表的完整Schema文件
根据Tushare API返回的完整字段列表生成schema定义
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
        'turn', 'days', 'num', 'count', 'chg', 'change', 'adj', 'factor'
    ]

    for pattern in numeric_patterns:
        if pattern in field_name.lower():
            return 'REAL'

    # 整数字段
    int_patterns = ['count', 'num', 'total', 'qty', 'open', 'amount']
    for pattern in int_patterns:
        if pattern in field_name.lower():
            return 'INTEGER'

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
        'publisher': 'VARCHAR(50)',
        'category': 'VARCHAR(20)',
        'manager': 'VARCHAR(50)',
        'benchmark': 'VARCHAR(200)',
        'trustee': 'VARCHAR(50)',
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
        'f_ann_date': '实际公告日期',
        'report_type': '报告类型',
        'comp_type': '公司类型',
        'end_type': '报告期类型',
        'update_flag': '更新标识',
        'name': '名称',
        'fullname': '全称',
        'market': '市场类型',
        'exchange': '交易所',
        'industry': '行业',
        'list_date': '上市日期',
        'delist_date': '退市日期',
        'issue_date': '发行日期',
        'base_date': '基期',
        'base_point': '基点',
        'is_open': '是否交易',
        'pretrade_date': '上一交易日',
        'is_hs': '是否沪深港通标的',
        'publisher': '发布方',
        'index_type': '指数类型',
        'category': '类别',
        'weight_rule': '加权方法',
        'description': '描述',
        'fund_type': '基金类型',
        'fund_manager': '基金经理',
        'issue_amount': '发行份额',
        'm_fee': '管理费',
        'c_fee': '托管费',
        'benchmark': '跟踪标的',
        'status': '状态',
        'invest_type': '投资类型',
        'trustee': '托管人',
        'perf_benchmark': '业绩比较基准',
        'total_share': '总股本',
        'surplus_rese': '盈余公积',
        'special_rese': '专项储备',
        'treasury_share': '库存股',
        'minority_int': '少数股东权益',
        'oth_receiv': '其他应收款',
        'prepayment': '预付款项',
        'div_receiv': '应收股利',
        'int_receiv': '应收利息',
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
        'prem_earned': '已赚保费',
        'comm_income': '手续费及佣金收入',
        'invest_income': '投资收益',
        'fv_value_chg_gain': '公允价值变动收益',
        'forex_gain': '汇兑收益',
        'oper_cost': '营业成本',
        'int_exp': '利息支出',
        'credit_impa_loss': '信用减值损失',
        'continued_net_profit': '持续经营净利润',
        'end_net_profit': '终止经营净利润',
        'extra_item': '非经常性损益项目',
        'netprofit_margin': '净利润率',
        'grossprofit_margin': '毛利润率',
        'ca_to_assets': '流动资产/总资产',
        'nca_to_assets': '非流动资产/总资产',
        'desc': '描述',
        'orgs': '组织',
        'ts_name': '股票名称',
        'hm_name': '游资名称',
        'hm_orgs': '游资组织',
        'adj_factor': '复权因子',
        'open': '开盘价',
        'high': '最高价',
        'low': '最低价',
        'close': '收盘价',
        'pre_close': '昨收价',
        'vol': '成交量',
        'amount': '成交额',
        'turnover_rate': '换手率',
        'volume_ratio': '量比',
        'pe': '市盈率',
        'pe_ttm': '市盈率TTM',
        'pb': '市净率',
        'ps': '市销率',
        'ps_ttm': '市销率TTM',
        'dv_ratio': '股息率',
        'dv_ttm': '股息率TTM',
        'total_mv': '总市值',
        'circ_mv': '流通市值',
        'free_share': '流通股本',
        'total_share': '总股本',
        'limit': '涨跌幅限制',
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
    if 'vol' in field_name:
        return '成交量'
    if 'ratio' in field_name or 'rate' in field_name:
        return '比率'

    return ''  # 无注释


def generate_table_definition(api, table_config):
    """生成单张表的完整定义"""
    api_name = table_config['api_name']
    params = table_config['params']
    primary_key = table_config.get('primary_key', [])
    indexes = table_config.get('indexes', [])
    table_desc = table_config.get('desc', '')

    print(f"  获取API字段: {api_name}")

    # 调用API获取完整字段列表
    try:
        data = api.query(api_name, **params)
        if not data or len(data) == 0:
            print(f"  ⚠️ API返回空数据，无法获取字段列表")
            return None

        api_fields = list(data[0].keys())
        print(f"  ✓ API字段数: {len(api_fields)}")
    except Exception as e:
        print(f"  ❌ API调用失败: {e}")
        return None

    # 生成表定义SQL
    sql_lines = []
    sql_lines.append(f"-- {table_config['table_name']} ({table_desc})")
    sql_lines.append(f"-- API接口: {api_name}")
    sql_lines.append(f"-- API字段数: {len(api_fields)}")
    sql_lines.append(f"")

    # 表名中文注释
    sql_lines.append(f"COMMENT ON TABLE {table_config['table_name']} IS '{table_desc}';")
    sql_lines.append(f"")

    sql_lines.append(f"CREATE TABLE IF NOT EXISTS {table_config['table_name']} (")

    # 按API返回顺序生成字段定义
    field_definitions = []
    for i, field in enumerate(api_fields):
        sql_type = infer_field_type(field)
        comment = get_field_comment(field)

        # 判断是否主键字段
        is_pk = field in primary_key
        pk_suffix = ' PRIMARY KEY' if is_pk and len(primary_key) == 1 else ''

        # 生成字段定义
        if comment:
            field_def = f"    {field} {sql_type}{pk_suffix},  -- {comment}"
        else:
            field_def = f"    {field} {sql_type}{pk_suffix},  -- {field}"

        field_definitions.append(field_def)

    # 添加所有字段定义
    sql_lines.extend(field_definitions)

    # 添加updated_at字段
    sql_lines.append("    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间")

    # 复合主键定义
    if len(primary_key) > 1:
        pk_fields = ', '.join(primary_key)
        sql_lines.append(f");")
        sql_lines.append(f"")
        sql_lines.append(f"-- 复合主键")
        sql_lines.append(f"ALTER TABLE {table_config['table_name']} ADD PRIMARY KEY ({pk_fields});")
    else:
        sql_lines.append(f");")

    sql_lines.append(f"")

    # 字段注释
    for field in api_fields:
        comment = get_field_comment(field)
        if comment:
            sql_lines.append(f"COMMENT ON COLUMN {table_config['table_name']}.{field} IS '{comment}';")

    sql_lines.append(f"")

    # 创建索引
    if indexes:
        sql_lines.append(f"-- 索引")
        for index_name, index_fields in indexes:
            sql_lines.append(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_config['table_name']}({', '.join(index_fields)});")
        sql_lines.append(f"")

    return '\n'.join(sql_lines)


def main():
    """主函数"""
    print("=" * 60)
    print("生成所有27张表的完整Schema文件")
    print("=" * 60)

    config = load_config()
    api = TushareAPI(config['tushare'])

    # 定义所有27张表的配置（按用户提供的映射）
    tables_config = {
        # 财务报表类
        'balancesheet': {
            'api_name': 'balancesheet_vip',
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'primary_key': ['ts_code', 'end_date', 'report_type'],
            'indexes': [
                ('idx_balancesheet_date', ['end_date']),
                ('idx_balancesheet_code', ['ts_code']),
                ('idx_balancesheet_ann_date', ['ann_date'])
            ],
            'desc': '资产负债表'
        },
        'cashflow': {
            'api_name': 'cashflow_vip',
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'primary_key': ['ts_code', 'end_date', 'report_type'],
            'indexes': [
                ('idx_cashflow_date', ['end_date']),
                ('idx_cashflow_code', ['ts_code']),
                ('idx_cashflow_ann_date', ['ann_date'])
            ],
            'desc': '现金流量表'
        },
        'dividend': {
            'api_name': 'dividend',
            'params': {'ts_code': '600000.SH', 'ann_date': '20260409'},
            'primary_key': ['ts_code', 'end_date', 'ann_date'],
            'indexes': [
                ('idx_dividend_code', ['ts_code']),
                ('idx_dividend_end_date', ['end_date']),
                ('idx_dividend_ann_date', ['ann_date'])
            ],
            'desc': '分红送股数据'
        },
        'express': {
            'api_name': 'express',
            'params': {'ann_date': '20260409'},
            'primary_key': ['ts_code', 'ann_date'],
            'indexes': [
                ('idx_express_code', ['ts_code']),
                ('idx_express_ann_date', ['ann_date'])
            ],
            'desc': '业绩快报'
        },
        'express_brief': {
            'api_name': 'express_brief',
            'params': {'ann_date': '20260409'},
            'primary_key': ['ts_code', 'ann_date'],
            'indexes': [
                ('idx_express_brief_code', ['ts_code']),
                ('idx_express_brief_ann_date', ['ann_date'])
            ],
            'desc': '业绩快报摘要'
        },
        'fina_indicator': {
            'api_name': 'fina_indicator_vip',
            'params': {'ann_date': '20260409'},
            'primary_key': ['ts_code', 'end_date'],
            'indexes': [
                ('idx_fina_indicator_date', ['end_date']),
                ('idx_fina_indicator_code', ['ts_code']),
                ('idx_fina_indicator_ann_date', ['ann_date'])
            ],
            'desc': '财务指标'
        },
        'income': {
            'api_name': 'income_vip',
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'primary_key': ['ts_code', 'end_date', 'report_type'],
            'indexes': [
                ('idx_income_date', ['end_date']),
                ('idx_income_code', ['ts_code']),
                ('idx_income_ann_date', ['ann_date'])
            ],
            'desc': '利润表'
        },

        # ETF数据
        'etf_adj_factor': {
            'api_name': 'adj_factor',
            'params': {'ts_code': '510050.SH', 'trade_date': '20260409'},
            'primary_key': ['ts_code', 'trade_date'],
            'indexes': [
                ('idx_etf_adj_factor_code', ['ts_code']),
                ('idx_etf_adj_factor_date', ['trade_date'])
            ],
            'desc': 'ETF复权因子'
        },
        'etf_basic': {
            'api_name': 'etf_basic',
            'params': {},
            'primary_key': ['ts_code'],
            'indexes': [('idx_etf_basic_code', ['ts_code'])],
            'desc': 'ETF基本信息'
        },
        'etf_daily': {
            'api_name': 'fund_daily',
            'params': {'ts_code': '510050.SH', 'trade_date': '20260409'},
            'primary_key': ['ts_code', 'trade_date'],
            'indexes': [
                ('idx_etf_daily_code', ['ts_code']),
                ('idx_etf_daily_date', ['trade_date'])
            ],
            'desc': 'ETF日线行情'
        },
        'etf_index': {
            'api_name': 'etf_index',
            'params': {},
            'primary_key': ['ts_code'],
            'indexes': [('idx_etf_index_code', ['ts_code'])],
            'desc': 'ETF基准指数'
        },

        # 热门交易数据
        'hots_trader_detail': {
            'api_name': 'hots_trader_detail',
            'params': {'trade_date': '20260409'},
            'primary_key': ['trade_date', 'ts_code'],
            'indexes': [
                ('idx_hots_trader_detail_date', ['trade_date']),
                ('idx_hots_trader_detail_code', ['ts_code'])
            ],
            'desc': '热门交易明细'
        },
        'hots_user': {
            'api_name': 'hots_user',
            'params': {'trade_date': '20260409'},
            'primary_key': ['trade_date', 'ts_code'],
            'indexes': [
                ('idx_hots_user_date', ['trade_date']),
                ('idx_hots_user_code', ['ts_code'])
            ],
            'desc': '热门用户'
        },

        # 指数数据
        'index_basic': {
            'api_name': 'index_basic',
            'params': {},
            'primary_key': ['ts_code'],
            'indexes': [('idx_index_basic_code', ['ts_code'])],
            'desc': '指数基本信息'
        },
        'index_daily': {
            'api_name': 'index_daily',
            'params': {'ts_code': '000001.SH', 'trade_date': '20260409'},
            'primary_key': ['ts_code', 'trade_date'],
            'indexes': [
                ('idx_index_daily_code', ['ts_code']),
                ('idx_index_daily_date', ['trade_date'])
            ],
            'desc': '指数日线行情'
        },

        # 股票数据
        'stock_basic': {
            'api_name': 'stock_basic',
            'params': {},
            'primary_key': ['ts_code'],
            'indexes': [('idx_stock_basic_code', ['ts_code'])],
            'desc': '股票列表'
        },
        'stock_daily': {
            'api_name': 'daily',
            'params': {'ts_code': '600000.SH', 'trade_date': '20260409'},
            'primary_key': ['ts_code', 'trade_date'],
            'indexes': [
                ('idx_stock_daily_code', ['ts_code']),
                ('idx_stock_daily_date', ['trade_date'])
            ],
            'desc': '股票日线行情'
        },
        'stock_daily_basic': {
            'api_name': 'daily_basic',
            'params': {'ts_code': '600000.SH', 'trade_date': '20260409'},
            'primary_key': ['ts_code', 'trade_date'],
            'indexes': [
                ('idx_stock_daily_basic_code', ['ts_code']),
                ('idx_stock_daily_basic_date', ['trade_date'])
            ],
            'desc': '股票每日指标'
        },
        'stock_weekly': {
            'api_name': 'weekly',
            'params': {'ts_code': '600000.SH', 'trade_date': '20260409'},
            'primary_key': ['ts_code', 'trade_date'],
            'indexes': [
                ('idx_stock_weekly_code', ['ts_code']),
                ('idx_stock_weekly_date', ['trade_date'])
            ],
            'desc': '股票周线行情'
        },
        'stock_monthly': {
            'api_name': 'monthly',
            'params': {'ts_code': '600000.SH', 'trade_date': '20260409'},
            'primary_key': ['ts_code', 'trade_date'],
            'indexes': [
                ('idx_stock_monthly_code', ['ts_code']),
                ('idx_stock_monthly_date', ['trade_date'])
            ],
            'desc': '股票月线行情'
        },

        # 同花顺数据
        'ths_concept_member': {
            'api_name': 'ths_member',
            'params': {'ts_code': 'TI001001'},
            'primary_key': ['ts_code', 'con_code'],
            'indexes': [
                ('idx_ths_concept_member_code', ['ts_code']),
                ('idx_ths_concept_member_con_code', ['con_code'])
            ],
            'desc': '同花顺概念成分'
        },
        'ths_concept_moneyflow': {
            'api_name': 'ths_moneyflow',
            'params': {'ts_code': 'TI001001', 'trade_date': '20260409'},
            'primary_key': ['ts_code', 'trade_date'],
            'indexes': [
                ('idx_ths_concept_moneyflow_code', ['ts_code']),
                ('idx_ths_concept_moneyflow_date', ['trade_date'])
            ],
            'desc': '同花顺概念资金流向'
        },
        'ths_index_basic': {
            'api_name': 'ths_index',
            'params': {},
            'primary_key': ['ts_code'],
            'indexes': [('idx_ths_index_basic_code', ['ts_code'])],
            'desc': '同花顺指数基本信息'
        },
        'ths_index_daily': {
            'api_name': 'ths_daily',
            'params': {'ts_code': 'TI001001', 'trade_date': '20260409'},
            'primary_key': ['ts_code', 'trade_date'],
            'indexes': [
                ('idx_ths_index_daily_code', ['ts_code']),
                ('idx_ths_index_daily_date', ['trade_date'])
            ],
            'desc': '同花顺指数日线行情'
        },
        'ths_industry_moneyflow': {
            'api_name': 'ths_industry_moneyflow',
            'params': {'trade_date': '20260409'},
            'primary_key': ['ts_code', 'trade_date'],
            'indexes': [
                ('idx_ths_industry_moneyflow_code', ['ts_code']),
                ('idx_ths_industry_moneyflow_date', ['trade_date'])
            ],
            'desc': '同花顺行业资金流向'
        },
        'ths_moneyflow': {
            'api_name': 'ths_moneyflow',
            'params': {'trade_date': '20260409'},
            'primary_key': ['ts_code', 'trade_date'],
            'indexes': [
                ('idx_ths_moneyflow_code', ['ts_code']),
                ('idx_ths_moneyflow_date', ['trade_date'])
            ],
            'desc': '同花顺资金流向'
        },

        # 交易日历
        'trade_calendar': {
            'api_name': 'trade_cal',
            'params': {'exchange': 'SSE', 'start_date': '20260401', 'end_date': '20260430'},
            'primary_key': ['exchange', 'cal_date'],
            'indexes': [
                ('idx_trade_calendar_date', ['cal_date']),
                ('idx_trade_calendar_exchange', ['exchange'])
            ],
            'desc': '交易日历'
        }
    }

    # 输出目录
    output_dir = Path('database/schemas_new')
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成每张表的定义
    success_count = 0
    failed_count = 0

    for table_name, config in tables_config.items():
        print(f"\n生成表定义: {table_name}")
        config['table_name'] = table_name

        sql = generate_table_definition(api, config)
        if sql:
            output_file = output_dir / f'{table_name}_schema.sql'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(sql)

            print(f"  ✓ 已保存: {output_file}")
            success_count += 1
        else:
            failed_count += 1

    print("\n" + "=" * 60)
    print(f"✓ Schema文件生成完成")
    print(f"  成功: {success_count} 张表")
    print(f"  失败: {failed_count} 张表")
    print(f"  输出目录: {output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()