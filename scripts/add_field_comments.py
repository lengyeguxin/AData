"""
字段注释批量添加脚本

功能：
1. 扫描所有schema.sql文件，识别缺少注释的字段
2. 从Tushare官方文档获取字段含义（映射表）
3. 批量添加中文注释
4. 生成字段注释报告

使用方法：
    python scripts/add_field_comments.py --schema database/schemas/p1_schema.sql --output database/schemas/p1_schema_commented.sql
    python scripts/add_field_comments.py --schema database/schemas/p1_schema.sql --report
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

# 字段中文映射表（参考Tushare官方文档）
FIELD_COMMENT_MAP = {
    'ts_code': '股票代码/指数代码/ETF代码',
    'trade_date': '交易日期',
    'pre_close': '昨收价（除权价）',
    'open': '开盘价',
    'high': '最高价',
    'low': '最低价',
    'close': '收盘价',
    'change': '涨跌额',
    'pct_chg': '涨跌幅（%）',
    'vol': '成交量（手）',
    'amount': '成交额（千元）',
    'adj_factor': '复权因子',
    'open_adj': '前复权开盘价',
    'high_adj': '前复权最高价',
    'low_adj': '前复权最低价',
    'close_adj': '前复权收盘价',
    'open_qfq': '前复权开盘价',
    'high_qfq': '前复权最高价',
    'low_qfq': '前复权最低价',
    'close_qfq': '前复权收盘价',
    'open_hfq': '后复权开盘价',
    'high_hfq': '后复权最高价',
    'low_hfq': '后复权最低价',
    'close_hfq': '后复权收盘价',
    'is_suspended': '是否停牌',
    'is_abnormal': '是否异常',
    'pe': '市盈率（总市值/净利润）',
    'pe_ttm': '市盈率TTM（总市值/最近12个月净利润）',
    'pb': '市净率（总市值/净资产）',
    'ps': '市销率（总市值/营业收入）',
    'ps_ttm': '市销率TTM',
    'dv_ratio': '股息率（%）',
    'dv_ttm': '股息率TTM（%）',
    'total_mv': '总市值（万元）',
    'circ_mv': '流通市值（万元）',
    'total_share': '总股本（万股）',
    'float_share': '流通股本（万股）',
    'free_share': '自由流通股本（万股）',
    'turnover_rate': '换手率（%）',
    'turnover_rate_f': '换手率（自由流通股）',
    'volume_ratio': '量比',
    'end_date': '计算截至日期',
    'freq': '频率（week/month）',
    'exchange': '交易所代码（SSE=上交所SZSE=深交所）',
    'cal_date': '交易日期',
    'is_open': '是否交易（0=休市1=交易）',
    'pretrade_date': '上一交易日',
    'name': '股票名称',
    'industry': '所属行业',
    'market': '市场类型（主板/中小板/创业板/科创板）',
    'list_date': '上市日期',
    'delist_date': '退市日期',
    'is_hs': '是否沪深港通标的（N=否H=沪股通S=深股通）',
    'fullname': '指数全称',
    'publisher': '发布方',
    'index_type': '指数类型',
    'category': '指数类别',
    'base_date': '基期',
    'base_point': '基点',
    'weight_rule': '加权方法',
    'description': '描述',
    'fund_type': '基金类型',
    'fund_manager': '基金经理',
    'issue_date': '发行日期',
    'issue_amount': '发行份额（万份）',
    'm_fee': '管理费（%）',
    'c_fee': '托管费（%）',
    'benchmark': '跟踪标的',
    'status': '状态',
    'invest_type': '投资类型',
    'type': '指数类型（N=概念S=特色）',
    'trustee': '托管人',
    'perf_benchmark': '业绩比较基准',
    'index_code': '跟踪指数代码',
    'index_name': '跟踪指数名称',
    'tracking_type': '跟踪类型',
    'tracking_ratio': '跟踪比例',
    'updated_at': '更新时间',
    'created_at': '创建时间',
    'total_revenue': '营业总收入',
    'revenue': '营业收入',
    'operate_profit': '营业利润',
    'total_cogs': '营业总成本',
    'interest_income': '利息收入',
    'profit_dedt': '扣除非经常损益后的净利润',
    'sell_exp': '销售费用',
    'admin_exp': '管理费用',
    'fin_exp': '财务费用',
    'asset_impair_loss': '资产减值损失',
    'non_oper_income': '营业外收入',
    'non_oper_exp': '营业外支出',
    'total_profit': '利润总额',
    'income_tax': '所得税',
    'n_income': '净利润',
    'n_income_attr_p': '归属母公司所有者的净利润',
    'minority_gain': '少数股东损益',
    'basic_eps': '基本每股收益',
    'diluted_eps': '稀释每股收益',
    'oth_compr_income': '其他综合收益',
    't_compr_income': '综合收益总额',
    'compr_inc_attr_p': '归属母公司所有者的综合收益',
    'compr_inc_attr_m_s': '归属少数股东的综合收益',
    'ebit': '息税前利润',
    'ebitda': '息税折旧摊销前利润',
    'rd_exp': '研发费用',
    'fin_exp_int_exp': '财务费用-利息支出',
    'fin_exp_int_income': '财务费用-利息收入',
    'transfer_surplus_reserve': '盈余公积转入',
    'transfer_risk_reserve': '风险准备转入',
    'f_ann_date': '实际公告日期',
    'report_type': '报告类型',
    'comp_type': '公司类型',
    'end_type': '报告期类型',
    'update_flag': '更新标识',
    'total_cur_assets': '流动资产合计',
    'money_cap': '货币资金',
    'trad_asset': '交易性金融资产',
    'notes_receiv': '应收票据',
    'accounts_receiv': '应收账款',
    'adv_payment': '预付款项',
    'other_receiv': '其他应收款',
    'inventories': '存货',
    'amor_exp': '长期待摊费用',
    'long_ampay_dep_rec_asim': '长期应收款项',
    'total_nca': '非流动资产合计',
    'fix_assets': '固定资产',
    'cip': '在建工程',
    'const_materials': '工程物资',
    'intang_assets': '无形资产',
    'goodwill': '商誉',
    'long_deferred_exp': '长期待摊费用',
    'defer_tax_assets': '递延所得税资产',
    'total_assets': '资产总计',
    'total_cur_liab': '流动负债合计',
    'st_borr': '短期借款',
    'notes_payable': '应付票据',
    'accounts_pay': '应付账款',
    'adv_receipts': '预收款项',
    'payroll_pay': '应付职工薪酬',
    'taxes_payable': '应交税费',
    'interest_payable': '应付利息',
    'div_payable': '应付股利',
    'other_payable': '其他应付款',
    'total_ncl': '非流动负债合计',
    'long_borr': '长期借款',
    'bonds_payable': '应付债券',
    'long_deferred_rev': '长期递延收益',
    'defer_tax_liab': '递延所得税负债',
    'total_liab': '负债合计',
    'total_hldr_eqy_exc_min_int': '所有者权益合计(不含少数股东权益)',
    'total_hldr_eqy_inc_min_int': '所有者权益合计(含少数股东权益)',
    'total_equity': '所有者权益合计',
    'capital_rese': '资本公积',
    'surplus_rese': '盈余公积',
    'special_rese': '专项储备',
    'undistr_porfit': '未分配利润',
    'money_cap_reserved': '货币资金(受限)',
    'trad_asset_reserved': '交易性金融资产(受限)',
    'notes_receiv_reserved': '应收票据(受限)',
    'accounts_receiv_reserved': '应收账款(受限)',
    'inventories_reserved': '存货(受限)',
    'fix_assets_reserved': '固定资产(受限)',
    'intang_assets_reserved': '无形资产(受限)',
    'cash_recp_sg_and_rsr': '销售商品、提供劳务收到的现金',
    'cash_pay_sg_and_rsr': '购买商品、接受劳务支付的现金',
    'cash_recp_sc_and_rsr': '收到税费返还',
    'cash_pay_sc_and_rsr': '支付税费',
    'cash_recp_disp_withdrw_invest': '收回投资收到的现金',
    'cash_pay_acq_const_faulta': '购建固定资产、无形资产和其他长期资产支付的现金',
    'cash_recp_cap_contrib': '吸收投资收到的现金',
    'cash_prepay_amt_borr': '偿还债务支付的现金',
    'cash_pay_dist_dpcp_int_exp': '分配股利、利润或偿付利息支付的现金',
    'net_cash_flows_oper_act': '经营活动产生的现金流量净额',
    'net_cash_flows_inv_act': '投资活动产生的现金流量净额',
    'net_cash_flows_fnc_act': '筹资活动产生的现金流量净额',
    'cash_equ_incr_decr': '现金及现金等价物净增加额',
    'cash_pay_oper_fee': '支付其他经营活动现金',
    'cash_recp_oper_fee': '收到其他经营活动现金',
    'cash_pay_invest_fee': '支付其他投资活动现金',
    'cash_recp_invest_fee': '收到其他投资活动现金',
    'cash_pay_finance_fee': '支付其他筹资活动现金',
    'cash_recp_finance_fee': '收到其他筹资活动现金',
    'dividend': '每股股利',
    'div_ratio': '股利支付率',
    'div_yield': '股利收益率',
    'record_date': '除权日',
    'ex_div_date': '除息日',
    'pay_date': '派息日',
    'div_type': '分红类型',
    'stk_div': '送股比例',
    'cash_div': '现金分红',
    'stk_bo_rate': '送股比例',
    'stk_co_rate': '转增比例',
    'cash_div_tax': '扣税后现金分红',
    'q_opincome': '单季度营业利润',
    'q_investincome': '单季度投资收益',
    'q_dtprofit': '单季度扣非净利润',
    'q_eps': '单季度每股收益',
    'q_netprofit_margin': '单季度净利润率',
    'q_gsprofit_margin': '单季度毛利率',
    'q_roe': '单季度ROE',
    'q_dt_roe': '单季度扣非ROE',
    'q_opprofit_margin': '单季度营业利润率',
    'q_ebit_margin': '单季度EBIT利润率',
    'q_ebitda_margin': '单季度EBITDA利润率',
    'q_opincome_yoy': '单季度营业利润同比增长',
    'q_investincome_yoy': '单季度投资收益同比增长',
    'q_dtprofit_yoy': '单季度扣非净利润同比增长',
    'q_eps_yoy': '单季度每股收益同比增长',
    'q_netprofit_yoy': '单季度净利润同比增长',
    'equity_yoy': '股东权益同比增长',
    'ann_date': '公告日期',
    'n_cashflow_act': '经营活动现金流量净额',
    'n_cashflow_fnc_act': '筹资活动现金流量净额',
    'c_fr_sale_sg': '销售商品提供劳务收到的现金',
    'cash_recp_sg_and_rs': '销售商品提供劳务收到的现金',
    'c_pay_for_tax': '支付的各项税费',
    'cash_pay_for_tax': '支付的各项税费',
    'c_pay_for_acq_fi': '购建固定资产、无形资产和其他长期资产支付的现金',
    'cash_pay_acq_const_fi': '购建固定资产、无形资产和其他长期资产支付的现金',
    'c_pay_for_invest': '投资支付的现金',
    'c_pay_for_loan_rel_fi': '偿还债务支付的现金',
    'c_pay_oth_inv_act': '支付其他与投资活动有关的现金',
    'c_pay_oth_fnc_act': '支付其他与筹资活动有关的现金',
    'c_recp_return_invest': '收回投资收到的现金',
    'c_recp_loan_rel_fi': '取得借款收到的现金',
    'c_fr_borrow': '取得借款收到的现金',
    'c_fr_cap_contr': '吸收投资收到的现金',
    'c_fr_for_sale': '处置固定资产、无形资产和其他长期资产收回的现金净额',
    'c_fr_disp_withdrw_invest': '处置子公司及其他营业单位收到的现金净额',
    'c_fr_oth_inv_act': '收到其他与投资活动有关的现金',
    'c_fr_oth_fnc_act': '收到其他与筹资活动有关的现金',
    'c_pay_for_dist_dpcp_int_exp': '分配股利、利润或偿付利息支付的现金',
    'c_pay_for_depos': '支付存款净增加额',
    'cash_recp_loan_rel_fi': '取得借款收到的现金',
    'cash_pay_for_depos': '支付存款净增加额',
    'n_cash_flows_inv_act': '投资活动现金流量净额',
    'n_cash_flows_fnc_act': '筹资活动现金流量净额',
    'effect_forex_cash': '汇率变动对现金的影响',
    'free_cashflow': '自由现金流',
    'cap_rese': '资本公积',
    'minority_int_ratio': '少数股东权益比例',
    'total_liab_hldr_eqy': '负债和股东权益总计',
    'account': '账户',
    'broker_name': '券商名称',
    'buy_amount': '买入金额',
    'buy_vol': '买入量',
    'buy_lg_amount': '大单买入金额',
    'buy_lg_amount_rate': '大单买入金额占比',
    'buy_md_amount': '中单买入金额',
    'buy_md_amount_rate': '中单买入金额占比',
    'buy_sm_amount': '小单买入金额',
    'buy_sm_amount_rate': '小单买入金额占比',
    'sell_amount': '卖出金额',
    'sell_vol': '卖出量',
    'sell_lg_amount': '大单卖出金额',
    'sell_lg_amount_rate': '大单卖出金额占比',
    'sell_md_amount': '中单卖出金额',
    'sell_md_amount_rate': '中单卖出金额占比',
    'sell_sm_amount': '小单卖出金额',
    'sell_sm_amount_rate': '小单卖出金额占比',
    'industry_index': '行业指数',
    'lead_stock': '龙头股票',
    'company_num': '公司数量',
    'in_date': '纳入日期',
    'is_new': '是否新纳入',
    'latest': '最新数据',
    'change_reason': '变动原因',
    'license': '许可证',
    'close_price': '收盘价',
    'ex_date': '除权除息日',
    'div_proc': '分红进度',
}

class FieldCommentAdder:
    """字段注释添加器"""

    def __init__(self, comment_map: Dict[str, str]):
        self.comment_map = comment_map

    def parse_schema_file(self, schema_path: Path) -> List[Tuple[str, str, bool]]:
        """解析schema文件，提取所有字段定义"""
        with open(schema_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        fields = []
        for line in lines:
            match = re.match(r'\s+(\w+)\s+\w+', line)
            if match:
                field_name = match.group(1)
                has_comment = '--' in line
                fields.append((line, field_name, has_comment))

        return fields

    def add_comment_to_line(self, line: str, field_name: str) -> str:
        """为字段添加注释"""
        if field_name not in self.comment_map:
            return line

        comment = self.comment_map[field_name]

        if '--' in line:
            return line

        line_stripped = line.rstrip()
        if line_stripped.endswith(','):
            line_without_comma = line_stripped[:-1]
            return f"{line_without_comma},  -- {comment}\n"
        else:
            return f"{line_stripped}  -- {comment}\n"

    def process_schema_file(self, schema_path: Path, output_path: Path):
        """处理schema文件，添加注释"""
        with open(schema_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        output_lines = []
        added_count = 0

        for line in lines:
            match = re.match(r'\s+(\w+)\s+\w+', line)
            if match:
                field_name = match.group(1)
                has_comment = '--' in line

                if not has_comment and field_name in self.comment_map:
                    line = self.add_comment_to_line(line, field_name)
                    added_count += 1

            output_lines.append(line)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(output_lines)

        print(f"✓ 已添加 {added_count} 个字段注释")
        print(f"✓ 输出文件: {output_path}")

    def generate_report(self, schema_path: Path) -> Dict:
        """生成字段注释报告"""
        fields = self.parse_schema_file(schema_path)

        total_fields = len(fields)
        commented_fields = sum(1 for _, _, has_comment in fields if has_comment)
        missing_fields = []
        unknown_fields = []

        for _, field_name, has_comment in fields:
            if not has_comment:
                if field_name in self.comment_map:
                    missing_fields.append(field_name)
                else:
                    unknown_fields.append(field_name)

        return {
            'total_fields': total_fields,
            'commented_fields': commented_fields,
            'missing_fields': missing_fields,
            'unknown_fields': unknown_fields
        }


def main():
    parser = argparse.ArgumentParser(description='字段注释批量添加脚本')
    parser.add_argument('--schema', required=True, help='输入schema文件路径')
    parser.add_argument('--output', help='输出schema文件路径')
    parser.add_argument('--report', action='store_true', help='生成字段注释报告')

    args = parser.parse_args()

    schema_path = Path(args.schema)
    adder = FieldCommentAdder(FIELD_COMMENT_MAP)

    if args.report:
        # 生成报告
        report = adder.generate_report(schema_path)
        print(f"\n{'='*60}")
        print(f"字段注释报告 - {schema_path.name}")
        print(f"{'='*60}")
        print(f"总字段数: {report['total_fields']}")
        print(f"已注释字段: {report['commented_fields']} ({report['commented_fields']/report['total_fields']*100:.1f}%)")
        print(f"待添加注释字段: {len(report['missing_fields'])}")
        print(f"未知字段（无映射）: {len(report['unknown_fields'])}")
        print(f"{'='*60}\n")

        if report['missing_fields']:
            print(f"待添加注释的字段:")
            for field in report['missing_fields'][:10]:  # 只显示前10个
                print(f"  - {field}: {FIELD_COMMENT_MAP.get(field, '无映射')}")
            if len(report['missing_fields']) > 10:
                print(f"  ... 还有 {len(report['missing_fields'])-10} 个字段")
            print()

        if report['unknown_fields']:
            print(f"未知字段（需要人工添加）:")
            for field in report['unknown_fields'][:10]:
                print(f"  - {field}")
            if len(report['unknown_fields']) > 10:
                print(f"  ... 还有 {len(report['unknown_fields'])-10} 个字段")

    elif args.output:
        # 处理schema文件
        output_path = Path(args.output)
        adder.process_schema_file(schema_path, output_path)

    else:
        print("错误：需要指定 --output 或 --report 参数")


if __name__ == '__main__':
    main()
