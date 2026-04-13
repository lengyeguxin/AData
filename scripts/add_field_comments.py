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
    # P1行情表 - 通用字段
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

    # 复权字段
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

    # 异常标记
    'is_suspended': '是否停牌',
    'is_abnormal': '是否异常',

    # stock_daily_basic - 估值指标
    'pe': '市盈率（总市值/净利润）',
    'pe_ttm': '市盈率TTM（总市值/最近12个月净利润）',
    'pb': '市净率（总市值/净资产）',
    'ps': '市销率（总市值/营业收入）',
    'ps_ttm': '市销率TTM',
    'dv_ratio': '股息率（%）',
    'dv_ttm': '股息率TTM（%）',

    # 市值指标
    'total_mv': '总市值（万元）',
    'circ_mv': '流通市值（万元）',

    # 股本指标
    'total_share': '总股本（万股）',
    'float_share': '流通股本（万股）',
    'free_share': '自由流通股本（万股）',

    # 交易指标
    'turnover_rate': '换手率（%）',
    'turnover_rate_f': '换手率（自由流通股）',
    'volume_ratio': '量比',

    # 周线月线字段
    'end_date': '计算截至日期',
    'freq': '频率（week/month）',

    # P0基础表 - trade_calendar
    'exchange': '交易所代码（SSE=上交所,SZSE=深交所）',
    'cal_date': '交易日期',
    'is_open': '是否交易（0=休市,1=交易）',
    'pretrade_date': '上一交易日',

    # stock_basic
    'name': '股票名称',
    'industry': '所属行业',
    'market': '市场类型（主板/中小板/创业板/科创板）',
    'list_date': '上市日期',
    'delist_date': '退市日期',
    'is_hs': '是否沪深港通标的（N=否,H=沪股通,S=深股通）',

    # index_basic
    'fullname': '指数全称',
    'publisher': '发布方',
    'index_type': '指数类型',
    'category': '指数类别',
    'base_date': '基期',
    'base_point': '基点',
    'weight_rule': '加权方法',
    'description': '描述',

    # etf_basic
    'fund_type': '基金类型',
    'fund_manager': '基金经理',
    'issue_date': '发行日期',
    'issue_amount': '发行份额（万份）',
    'm_fee': '管理费（%）',
    'c_fee': '托管费（%）',
    'benchmark': '跟踪标的',
    'status': '状态',
    'invest_type': '投资类型',
    'type': 'ETF类型',
    'trustee': '托管人',
    'perf_benchmark': '业绩比较基准',
    'index_code': '跟踪指数代码',
    'index_name': '跟踪指数名称',
    'tracking_type': '跟踪类型',
    'tracking_ratio': '跟踪比例',

    # ths_index_basic
    'type': '指数类型（N=概念,S=特色）',

    # 系统字段
    'updated_at': '更新时间',
    'created_at': '创建时间',
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
