"""
自动生成完整Schema定义脚本
根据field_diff_results.json自动为缺失字段生成SQL定义
"""

import json
import re
from pathlib import Path

# 字段类型推断映射(根据字段名模式)
FIELD_TYPE_MAP = {
    # 数值型字段(金额、数量、比率等)
    'amount': 'REAL',
    'vol': 'REAL',
    'ratio': 'REAL',
    'rate': 'REAL',
    'margin': 'REAL',
    'yield': 'REAL',
    'cost': 'REAL',
    'exp': 'REAL',
    'income': 'REAL',
    'profit': 'REAL',
    'assets': 'REAL',
    'liab': 'REAL',
    'equity': 'REAL',
    'capital': 'REAL',
    'share': 'REAL',
    'eps': 'REAL',
    'bps': 'REAL',
    'roe': 'REAL',
    'roa': 'REAL',
    'pe': 'REAL',
    'pb': 'REAL',
    'mv': 'REAL',
    'price': 'REAL',
    'fee': 'REAL',
    'div': 'REAL',
    'tax': 'REAL',
    'pay': 'REAL',
    'recp': 'REAL',
    'cash': 'REAL',
    'flow': 'REAL',
    'depos': 'REAL',
    'loan': 'REAL',
    'bond': 'REAL',
    'invest': 'REAL',
    'turn': 'REAL',
    'days': 'REAL',

    # 日期型字段
    'date': 'DATE',
    '_dt': 'DATE',
    '_ym': 'VARCHAR(10)',

    # 字符串型字段
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

# 字段注释映射(参考Tushare文档)
FIELD_COMMENT_MAP = {
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
}


def infer_field_type(field_name):
    """推断字段类型"""
    # 特殊字段处理
    if field_name.endswith('_date') or field_name == 'date':
        return 'DATE'

    # 根据字段名模式匹配
    for pattern, sql_type in FIELD_TYPE_MAP.items():
        if pattern in field_name.lower():
            return sql_type

    # 默认数值型(Tushare财务数据大多是数值)
    return 'REAL'


def get_field_comment(field_name):
    """获取字段注释"""
    # 查找映射表
    if field_name in FIELD_COMMENT_MAP:
        return FIELD_COMMENT_MAP[field_name]

    # 根据字段名推断
    if 'amount' in field_name:
        return '金额'
    if 'vol' in field_name:
        return '数量'
    if 'ratio' in field_name or 'rate' in field_name:
        return '比率'
    if 'margin' in field_name:
        return '利润率'
    if 'income' in field_name:
        return '收入'
    if 'exp' in field_name:
        return '费用'
    if 'assets' in field_name:
        return '资产'
    if 'liab' in field_name:
        return '负债'
    if 'pay' in field_name or 'payable' in field_name:
        return '应付'
    if 'receiv' in field_name or 'recp' in field_name:
        return '应收'

    return field_name  # 无注释时返回字段名


def generate_table_alter_sql(table_name, missing_fields):
    """生成ALTER TABLE语句添加缺失字段"""
    sql_lines = []
    sql_lines.append(f"-- 为{table_name}表添加缺失字段")
    sql_lines.append(f"-- 缺失字段数: {len(missing_fields)}")

    for field in missing_fields:
        sql_type = infer_field_type(field)
        comment = get_field_comment(field)

        sql_lines.append(
            f"ALTER TABLE {table_name} ADD COLUMN {field} {sql_type};  -- {comment}"
        )

    return '\n'.join(sql_lines)


def generate_complete_table_schema(table_name, existing_fields, api_fields, missing_fields):
    """生成完整的表定义(包含所有API字段)"""
    sql_lines = []
    sql_lines.append(f"-- {table_name}完整字段定义")
    sql_lines.append(f"-- API字段数: {len(api_fields)}, 缺失字段数: {len(missing_fields)}")
    sql_lines.append(f"CREATE TABLE IF NOT EXISTS {table_name} (")

    # 按API返回顺序生成字段定义
    for i, field in enumerate(api_fields):
        sql_type = infer_field_type(field)
        comment = get_field_comment(field)

        # 判断是否主键或已有字段
        if field in existing_fields:
            sql_lines.append(f"    {field} {sql_type},  -- {comment} (已有)")
        else:
            sql_lines.append(f"    {field} {sql_type},  -- {comment} (新增)")

    # 添加updated_at字段
    sql_lines.append("    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间")
    sql_lines.append(");")

    return '\n'.join(sql_lines)


def main():
    """主函数"""
    # 读取字段差异结果
    with open('docs/field_diff_results.json', 'r') as f:
        diff_data = json.load(f)

    output_dir = Path('database/migrations')
    output_dir.mkdir(parents=True, exist_ok=True)

    # 为每张表生成迁移脚本
    for table_name, info in diff_data.items():
        if 'error' in info or info.get('missing_count', 0) == 0:
            continue

        missing_fields = info.get('missing_fields', [])
        if not missing_fields:
            continue

        print(f"\n生成迁移脚本: {table_name}")
        print(f"  缺失字段数: {len(missing_fields)}")

        # 生成ALTER TABLE语句
        alter_sql = generate_table_alter_sql(table_name, missing_fields)

        # 保存到文件
        output_file = output_dir / f'add_fields_{table_name}.sql'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"-- {table_name}表字段迁移脚本\n")
            f.write(f"-- 生成时间: 2026-04-14\n")
            f.write(f"-- 缺失字段数: {len(missing_fields)}\n\n")
            f.write(alter_sql)
            f.write("\n\n-- 执行前请先备份数据库\n")
            f.write("-- 执行命令: duckdb database/adata.db < database/migrations/add_fields_{table_name}.sql\n")

        print(f"  ✓ 已保存: {output_file}")

    # 生成汇总迁移脚本
    summary_file = output_dir / 'add_all_missing_fields.sql'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("-- 数据库字段迁移汇总脚本\n")
        f.write("-- 生成时间: 2026-04-14\n")
        f.write("-- 总计缺失字段: 356个\n\n")

        total_missing = sum(
            info.get('missing_count', 0)
            for info in diff_data.values()
            if 'error' not in info
        )
        f.write(f"-- 总计缺失字段数: {total_missing}\n\n")

        for table_name, info in sorted(
            diff_data.items(),
            key=lambda x: x[1].get('missing_count', 0),
            reverse=True
        ):
            if 'error' in info or info.get('missing_count', 0) == 0:
                continue

            missing_fields = info.get('missing_fields', [])
            alter_sql = generate_table_alter_sql(table_name, missing_fields)

            f.write(f"\n{'='*60}\n")
            f.write(f"-- {table_name}表\n")
            f.write(f"{'='*60}\n\n")
            f.write(alter_sql)
            f.write("\n")

        f.write("\n-- 执行前请先备份数据库:\n")
        f.write("-- cp database/adata.db database/adata.db.backup_YYYYMMDD\n")
        f.write("-- 执行命令: duckdb database/adata.db < database/migrations/add_all_missing_fields.sql\n")

    print(f"\n{'='*60}")
    print(f"✓ 汇总迁移脚本已生成: {summary_file}")
    print(f"✓ 总计处理 {len([k for k,v in diff_data.items() if 'error' not in v and v.get('missing_count',0)>0])} 张表")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()