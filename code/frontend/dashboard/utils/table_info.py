"""
表信息映射配置（按设计文档最新分类标准）

维护所有数据表的中文名称、分类、描述、更新频率等元信息
"""

from typing import Dict

# 表信息配置字典（按设计文档最新分类）
TABLE_INFO: Dict[str, Dict] = {
    # ============ P0基础（6张表） ============
    'trade_calendar': {
        'chinese_name': '交易日历',
        'category': 'P0基础',
        'description': '各交易所交易日历，包括开市日期、节假日等',
        'date_field': 'cal_date',
        'update_frequency': '按年更新'
    },
    'stock_basic': {
        'chinese_name': '股票列表',
        'category': 'P0基础',
        'description': '上市公司基础信息，包括代码、名称、行业、上市日期等',
        'date_field': 'list_date',
        'update_frequency': '按月更新'
    },
    'index_basic': {
        'chinese_name': '指数列表',
        'category': 'P0基础',
        'description': '指数基础信息，包括名称、类型、基准日期等',
        'date_field': 'list_date',
        'update_frequency': '一次性更新'
    },
    'ths_index_basic': {
        'chinese_name': '同花顺指数列表',
        'category': 'P0基础',
        'description': '同花顺指数基础信息，包括概念指数、行业指数等',
        'date_field': 'list_date',
        'update_frequency': '按月更新'
    },
    'etf_basic': {
        'chinese_name': 'ETF列表',
        'category': 'P0基础',
        'description': 'ETF基础信息列表',
        'date_field': 'list_date',
        'update_frequency': '按月更新'
    },
    'etf_index': {
        'chinese_name': 'ETF指数',
        'category': 'P0基础',
        'description': 'ETF指数基础信息',
        'date_field': 'updated_at',
        'update_frequency': '按月更新'
    },

    # ============ P1行情（7张表） ============
    'stock_daily': {
        'chinese_name': '股票日线行情',
        'category': 'P1行情',
        'description': '股票日线行情数据，包括开高低收、成交量、复权因子等',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },
    'stock_daily_basic': {
        'chinese_name': '股票每日指标',
        'category': 'P1行情',
        'description': '每日估值指标，包括PE/PB/PS、市值、换手率等',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },
    'stock_weekly': {
        'chinese_name': '股票周线行情',
        'category': 'P1行情',
        'description': '股票周线行情数据',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },
    'stock_monthly': {
        'chinese_name': '股票月线行情',
        'category': 'P1行情',
        'description': '股票月线行情数据',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },
    'index_daily': {
        'chinese_name': '指数日线行情',
        'category': 'P1行情',
        'description': '指数日线行情数据',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },
    'etf_daily': {
        'chinese_name': 'ETF日线行情',
        'category': 'P1行情',
        'description': 'ETF日线行情数据',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },
    'etf_adj_factor': {
        'chinese_name': 'ETF复权因子',
        'category': 'P1行情',
        'description': 'ETF复权因子数据',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },

    # ============ P2财务（7张表） ============
    'fina_indicator': {
        'chinese_name': '财务指标',
        'category': 'P2财务',
        'description': '上市公司财务指标数据，包括ROE、利润率、增长率等',
        'date_field': 'ann_date',
        'update_frequency': '按天更新（自然日）'
    },
    'income': {
        'chinese_name': '利润表',
        'category': 'P2财务',
        'description': '上市公司利润表，包括营收、利润、EPS等',
        'date_field': 'ann_date',
        'update_frequency': '按天更新（自然日）'
    },
    'balancesheet': {
        'chinese_name': '资产负债表',
        'category': 'P2财务',
        'description': '上市公司资产负债表，包括资产、负债、股东权益等',
        'date_field': 'ann_date',
        'update_frequency': '按天更新（自然日）'
    },
    'cashflow': {
        'chinese_name': '现金流量表',
        'category': 'P2财务',
        'description': '上市公司现金流量表，包括经营、投资、筹资现金流等',
        'date_field': 'ann_date',
        'update_frequency': '按天更新（自然日）'
    },
    'express': {
        'chinese_name': '业绩预告',
        'category': 'P2财务',
        'description': '上市公司业绩预告，包括预告类型、利润范围等',
        'date_field': 'ann_date',
        'update_frequency': '按天更新（自然日）'
    },
    'express_brief': {
        'chinese_name': '业绩快报',
        'category': 'P2财务',
        'description': '上市公司业绩快报，包括主要财务指标',
        'date_field': 'ann_date',
        'update_frequency': '按天更新（自然日）'
    },
    'dividend': {
        'chinese_name': '分红送股',
        'category': 'P2财务',
        'description': '上市公司分红送股数据',
        'date_field': 'ann_date',
        'update_frequency': '按天更新（自然日）'
    },

    # ============ P3资金流向(THS)（3张表） ============
    'ths_moneyflow': {
        'chinese_name': '同花顺个股资金流',
        'category': 'P3资金流向(THS)',
        'description': '同花顺个股资金流向数据',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },
    'ths_concept_moneyflow': {
        'chinese_name': '同花顺概念资金流',
        'category': 'P3资金流向(THS)',
        'description': '同花顺概念板块资金流向',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },
    'ths_industry_moneyflow': {
        'chinese_name': '同花顺行业资金流',
        'category': 'P3资金流向(THS)',
        'description': '同花顺行业资金流向',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },

    # ============ P3概念板块（2张表） ============
    'ths_concept_member': {
        'chinese_name': '同花顺概念成分',
        'category': 'P3概念板块',
        'description': '同花顺概念板块成分股',
        'date_field': 'in_date',
        'update_frequency': '按月更新'
    },
    'ths_index_daily': {
        'chinese_name': '同花顺指数日线',
        'category': 'P3概念板块',
        'description': '同花顺指数日线行情数据',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },

    # ============ P4游资（2张表） ============
    'hots_user': {
        'chinese_name': '游资账户',
        'category': 'P4游资',
        'description': '游资账户信息列表',
        'date_field': 'reg_date',
        'update_frequency': '按月更新'
    },
    'hots_trader_detail': {
        'chinese_name': '游资交易明细',
        'category': 'P4游资',
        'description': '游资交易明细数据',
        'date_field': 'trade_date',
        'update_frequency': '按天更新（交易日）'
    },

    # ============ 系统表 ============
    'global_cursor': {
        'chinese_name': '全局游标表',
        'category': '系统表',
        'description': '全局游标管理系统，记录每张表的数据拉取进度',
        'date_field': 'updated_at',
        'update_frequency': '实时更新'
    }
}


def get_rolling_table_info(table_name: str) -> Dict:
    """
    获取滚动表信息

    Args:
        table_name: 滚动表名（如 cyq_performance_202601）

    Returns:
        表信息字典
    """
    if table_name.startswith('cyq_performance_'):
        month_suffix = table_name.replace('cyq_performance_', '')
        year = month_suffix[:4]
        month = month_suffix[4:]
        return {
            'chinese_name': f'筹码分布_{year}年{month}月',
            'category': 'P5滚动',
            'description': f'{year}年{month}月筹码分布数据',
            'date_field': 'trade_date',
            'update_frequency': '月更新'
        }
    elif table_name.startswith('margin_detail_'):
        month_suffix = table_name.replace('margin_detail_', '')
        year = month_suffix[:4]
        month = month_suffix[4:]
        return {
            'chinese_name': f'融资融券_{year}年{month}月',
            'category': 'P5滚动',
            'description': f'{year}年{month}月融资融券数据',
            'date_field': 'trade_date',
            'update_frequency': '月更新'
        }

    # 未知滚动表
    return {
        'chinese_name': table_name,
        'category': '未知',
        'description': '',
        'date_field': 'updated_at',
        'update_frequency': '未知'
    }


def get_table_info(table_name: str) -> Dict:
    """
    获取表的完整信息（支持固定表和滚动表）

    Args:
        table_name: 表名

    Returns:
        表信息字典
    """
    # 先尝试从固定表配置中查找
    if table_name in TABLE_INFO:
        return TABLE_INFO[table_name]

    # 如果是滚动表，使用滚动表解析逻辑
    if table_name.startswith('cyq_performance_') or table_name.startswith('margin_detail_'):
        return get_rolling_table_info(table_name)

    # 未知表，返回默认值
    return {
        'chinese_name': table_name,
        'category': '未知',
        'description': '',
        'date_field': 'updated_at',
        'update_frequency': '未知'
    }