"""
获取Tushare API完整字段列表
通过实际API调用获取VIP接口返回的所有字段名称
"""

import sys
import json
import yaml
from pathlib import Path

# 添加正确的导入路径
backend_path = Path(__file__).parent.parent / 'code' / 'backend'
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / 'src'))

from core.tushare_api import TushareAPI


def load_config():
    """加载配置文件"""
    config_path = backend_path / 'config' / 'config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_api_fields(api_name: str, sample_params: dict) -> list:
    """
    获取API返回的所有字段名称

    Args:
        api_name: API名称
        sample_params: 示例查询参数

    Returns:
        字段名称列表
    """
    config_dict = load_config()
    api = TushareAPI(config_dict['tushare'])

    print(f"\n调用API: {api_name}")
    print(f"参数: {sample_params}")

    # 调用API获取数据
    data = api.query(api_name, **sample_params)

    if not data:
        print(f"⚠️  API返回空数据")
        return []

    # 从第一条数据中获取所有字段名
    first_record = data[0]
    fields = list(first_record.keys())

    print(f"✓ 获取到 {len(fields)} 个字段")
    print(f"字段列表: {fields}")

    return fields


def compare_fields(api_name: str, api_fields: list, schema_fields: list):
    """
    对比API字段和Schema字段

    Args:
        api_name: API名称
        api_fields: API返回的字段列表
        schema_fields: Schema定义的字段列表
    """
    print(f"\n{'='*60}")
    print(f"字段对比: {api_name}")
    print(f"{'='*60}")
    print(f"API字段数: {len(api_fields)}")
    print(f"Schema字段数: {len(schema_fields)}")

    # 找出缺失字段
    missing_fields = [f for f in api_fields if f not in schema_fields]
    print(f"缺失字段数: {len(missing_fields)}")

    if missing_fields:
        print(f"\n缺失字段列表:")
        for i, field in enumerate(missing_fields, 1):
            print(f"  {i}. {field}")

    # 找出多余字段(Schema中有但API中没有的字段)
    extra_fields = [f for f in schema_fields if f not in api_fields and f != 'updated_at']
    if extra_fields:
        print(f"\nSchema中的多余字段:")
        for field in extra_fields:
            print(f"  - {field}")


def main():
    """主函数"""

    # VIP接口列表(财务表)
    vip_interfaces = {
        'fina_indicator_vip': {
            'params': {'ann_date': '20260409'},
            'schema_fields': [
            ]
        },
        'income_vip': {
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'schema_fields': [
                'ts_code', 'ann_date', 'f_ann_date', 'end_date', 'report_type',
                'comp_type', 'end_type', 'update_flag', 'total_revenue', 'revenue',
                'operate_profit', 'total_cogs', 'interest_income', 'profit_dedt',
                'sell_exp', 'admin_exp', 'fin_exp', 'asset_impair_loss',
                'non_oper_income', 'non_oper_exp', 'total_profit', 'income_tax',
                'n_income', 'n_income_attr_p', 'minority_gain', 'basic_eps',
                'diluted_eps', 'oth_compr_income', 't_compr_income',
                'compr_inc_attr_p', 'compr_inc_attr_m_s', 'ebit', 'ebitda',
                'rd_exp', 'fin_exp_int_exp', 'fin_exp_int_income',
                'transfer_surplus_reserve', 'transfer_risk_reserve'
            ]
        },
        'balancesheet_vip': {
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'schema_fields': [
                'ts_code', 'ann_date', 'f_ann_date', 'end_date', 'report_type',
                'comp_type', 'end_type', 'update_flag', 'total_cur_assets',
                'money_cap', 'trad_asset', 'notes_receiv', 'accounts_receiv',
                'adv_payment', 'other_receiv', 'inventories', 'amor_exp',
                'long_ampay_dep_rec_asim', 'total_nca', 'fix_assets', 'cip',
                'const_materials', 'intang_assets', 'goodwill', 'long_deferred_exp',
                'defer_tax_assets', 'total_assets', 'total_cur_liab', 'st_borr',
                'notes_payable', 'accounts_pay', 'adv_receipts', 'payroll_pay',
                'taxes_payable', 'interest_payable', 'div_payable', 'other_payable',
                'total_ncl', 'long_borr', 'bonds_payable', 'long_deferred_rev',
                'defer_tax_liab', 'total_liab', 'cap_rese', 'undistr_porfit',
                'minority_int_ratio', 'total_hldr_eqy_exc_min_int',
                'total_hldr_eqy_inc_min_int', 'total_liab_hldr_eqy'
            ]
        },
        'cashflow_vip': {
            'params': {'ann_date': '20260409', 'report_type': '1'},
            'schema_fields': [
                'ts_code', 'ann_date', 'f_ann_date', 'end_date', 'report_type',
                'comp_type', 'end_type', 'update_flag', 'n_cashflow_act',
                'cash_recp_sg_and_rs', 'recp_tax_rends', 'cash_pay_for_tax',
                'cash_pay_acq_const_fi', 'cash_pay_for_depos', 'cash_recp_loan_rel_fi',
                'free_cashflow', 'n_cash_flows_inv_act', 'c_fr_sale_sg', 'c_fr_for_sale',
                'c_fr_disp_withdrw_invest', 'c_recp_return_invest', 'c_recp_loan_rel_fi',
                'c_fr_oth_inv_act', 'n_cashflow_inv_act', 'c_pay_for_acq_fi',
                'c_pay_for_invest', 'c_pay_oth_inv_act', 'n_cash_flows_fnc_act',
                'c_fr_cap_contr', 'c_fr_borrow', 'c_fr_oth_fnc_act', 'n_cashflow_fnc_act',
                'c_pay_for_dist_dpcp_int_exp', 'c_pay_for_loan_rel_fi', 'c_pay_oth_fnc_act',
                'n_incr_cash_cash_equ', 'effect_forex_cash'
            ]
        }
    }

    print("=" * 60)
    print("开始获取VIP接口完整字段列表")
    print("=" * 60)

    # 遍历VIP接口获取字段
    for api_name, config in vip_interfaces.items():
        try:
            api_fields = get_api_fields(api_name, config['params'])
            compare_fields(api_name, api_fields, config['schema_fields'])
        except Exception as e:
            print(f"❌ 获取{api_name}字段失败: {e}")

    print("\n" + "=" * 60)
    print("字段列表获取完成")
    print("=" * 60)


if __name__ == '__main__':
    main()