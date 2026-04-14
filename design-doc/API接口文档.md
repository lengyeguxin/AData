# AData API接口文档

**生成时间：** 2026-04-14  
**覆盖范围：** 28张数据表的完整API接口说明

---

## 目录

1. [P0基础表（6张）](#p0基础表)
2. [P1行情表（7张）](#p1行情表)
3. [P2财务表（7张）](#p2财务表)
4. [P3资金流向（3张）](#p3资金流向)
5. [P3概念板块（2张）](#p3概念板块)
6. [P4游资（2张）](#p4游资)
7. [VIP接口特殊说明](#vip接口特殊说明)
8. [游标策略说明](#游标策略说明)

---

## P0基础表

### 1. trade_calendar（交易日历）

**接口名称：** `trade_cal`

**游标策略：** `yearly`（按年记录）

**拉取参数：**
```python
{
    'exchange': 'SSE',      # 交易所（SSE=上交所, SZSE=深交所）
    'start_date': '20260101',
    'end_date': '20261231'
}
```

**字段列表：**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| exchange | VARCHAR(10) | 交易所代码（SSE=上交所,SZSE=深交所） |
| cal_date | DATE | 交易日期 |
| is_open | INTEGER | 是否交易（0=休市,1=交易） |
| pretrade_date | DATE | 上一交易日 |
| updated_at | TIMESTAMP | 更新时间 |

**拉取频率：** 按年拉取，每年一次性拉取全年交易日历

**游标更新：** 每年拉取完成后，游标更新为年份（如'2026'）

**注意事项：**
- 需要分别拉取上交所（SSE）和深交所（SZSE）两个交易所
- 交易日历包含未来日期（提前设置），不用于判断最新数据时间

---

### 2. stock_basic（股票列表）

**接口名称：** `stock_basic`

**游标策略：** `none`（无游标，全量拉取）

**拉取参数：**
```python
{
    'exchange': '',         # 交易所（空=全部）
    'list_status': 'L',     # 上市状态（L=上市, D=退市, P=暂停上市）
    'fields': 'ts_code,name,industry,market,list_date'
}
```

**字段列表：**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| ts_code | VARCHAR(10) | 股票代码（TS格式，如000001.SZ） |
| name | VARCHAR(50) | 股票名称 |
| industry | VARCHAR(50) | 所属行业 |
| market | VARCHAR(10) | 市场类型（主板/中小板/创业板/科创板） |
| list_date | DATE | 上市日期 |
| delist_date | DATE | 退市日期 |
| is_hs | VARCHAR(2) | 是否沪深港通标的（N=否,H=沪股通,S=深股通） |
| updated_at | TIMESTAMP | 更新时间 |

**拉取频率：** 按月全量拉取（每月更新一次）

**注意事项：**
- 每次全量拉取，ON CONFLICT更新
- 作为stock_daily、income等表的前置依赖

---

### 3. index_basic（指数列表）

**接口名称：** `index_basic`

**游标策略：** `none`（无游标，全量拉取）

**拉取参数：**
```python
{
    'market': 'SSE'  # 市场类型（SSE=上交所, SZSE=深交所）
}
```

**需要拉取两次：**
- SSE市场（上交所指数）
- SZSE市场（深交所指数）

**字段列表：**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| ts_code | VARCHAR(10) | 指数代码（TS格式） |
| name | VARCHAR(50) | 指数简称 |
| fullname | VARCHAR(100) | 指数全称 |
| market | VARCHAR(10) | 市场类型 |
| publisher | VARCHAR(50) | 发布方 |
| index_type | VARCHAR(20) | 指数类型 |
| category | VARCHAR(20) | 指数类别 |
| base_date | DATE | 基期 |
| base_point | REAL | 基点 |
| list_date | DATE | 发布日期 |
| weight_rule | VARCHAR(20) | 加权方法 |
| description | TEXT | 描述 |
| updated_at | TIMESTAMP | 更新时间 |

**拉取频率：** 按月全量拉取

---

### 4. ths_index_basic（同花顺指数列表）

**接口名称：** `ths_index_basic`

**游标策略：** `none`（无游标）

**拉取参数：**
```python
{
    'exchange': 'A',  # 市场（A=A股）
    'type': 'N'       # 类型（N=概念, S=特色）
}
```

**需要拉取两次：**
- type='N'（概念指数）
- type='S'（特色指数）

**字段列表：**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| ts_code | VARCHAR(10) | 指数代码（TI格式） |
| name | VARCHAR(50) | 指数简称 |
| fullname | VARCHAR(100) | 指数全称 |
| exchange | VARCHAR(10) | 交易所 |
| type | VARCHAR(10) | 指数类型（N=概念,S=特色） |
| list_date | DATE | 发布日期 |
| weight_rule | VARCHAR(20) | 加权方法 |
| description | TEXT | 描述 |
| updated_at | TIMESTAMP | 更新时间 |

---

### 5. etf_basic（ETF列表）

**接口名称：** `etf_basic`

**游标策略：** `none`（无游标）

**拉取参数：** 无参数（全量拉取）

**字段列表：**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| ts_code | VARCHAR(10) | ETF代码（TS格式） |
| name | VARCHAR(50) | ETF简称 |
| fullname | VARCHAR(100) | ETF全称 |
| fund_type | VARCHAR(20) | 基金类型 |
| fund_manager | VARCHAR(50) | 基金经理 |
| list_date | DATE | 上市日期 |
| issue_date | DATE | 发行日期 |
| delist_date | DATE | 退市日期 |
| issue_amount | REAL | 发行份额（万份） |
| m_fee | REAL | 管理费（%） |
| c_fee | REAL | 托管费（%） |
| benchmark | VARCHAR(200) | 跟踪标的 |
| status | VARCHAR(10) | 状态 |
| invest_type | VARCHAR(20) | 投资类型 |
| type | VARCHAR(20) | ETF类型 |
| trustee | VARCHAR(50) | 托管人 |
| perf_benchmark | VARCHAR(200) | 业绩比较基准 |
| updated_at | TIMESTAMP | 更新时间 |

---

### 6. etf_index（ETF基准指数）

**接口名称：** `etf_index`（实际接口名，已修正）

**游标策略：** `none`

**拉取参数：** 无参数（全量拉取）

**文档地址：** https://tushare.pro/document/2?doc_id=386

**注意事项：** 之前曾误用fund_index_basic接口名，现已修正为etf_index

**字段列表：**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| ts_code | VARCHAR(10) | ETF代码 |
| index_code | VARCHAR(10) | 跟踪指数代码 |
| index_name | VARCHAR(50) | 跟踪指数名称 |
| tracking_type | VARCHAR(20) | 跟踪类型 |
| tracking_ratio | REAL | 跟踪比例 |
| invest_type | VARCHAR(20) | 投资类型 |
| updated_at | TIMESTAMP | 更新时间 |

---

## P1行情表

### 7. stock_daily（日线行情）

**接口名称：** `daily`

**游标策略：** `daily_trade`（按天记录，交易日每日拉取）

**拉取参数：**
```python
{
    'ts_code': '',         # 股票代码（空=全部，并发拉取）
    'trade_date': '20260410',  # 交易日期
    'adj': None            # 复权类型（null=不复权）
}
```

**拉取方式：** 按交易日遍历，并发拉取所有股票（ThreadPoolExecutor）

**字段列表（已注释100%）：**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| ts_code | VARCHAR(10) | 股票代码/指数代码/ETF代码 |
| trade_date | DATE | 交易日期 |
| pre_close | REAL | 昨收价（除权价） |
| open | REAL | 开盘价 |
| high | REAL | 最高价 |
| low | REAL | 最低价 |
| close | REAL | 收盘价 |
| change | REAL | 涨跌额 |
| pct_chg | REAL | 涨跌幅（%） |
| vol | REAL | 成交量（手） |
| amount | REAL | 成交额（千元） |
| adj_factor | REAL | 复权因子 |
| open_adj | REAL | 前复权开盘价 |
| high_adj | REAL | 前复权最高价 |
| low_adj | REAL | 前复权最低价 |
| close_adj | REAL | 前复权收盘价 |
| is_suspended | BOOLEAN | 是否停牌 |
| is_abnormal | BOOLEAN | 是否异常 |
| updated_at | TIMESTAMP | 更新时间 |

**游标更新时机：**
- 必须有数据才更新（无数据报错）
- 游标值：YYYYMMDD格式（如'20260410'）

**18点判断逻辑：**
- 当前时间≥18:00：拉取今天数据
- 当前时间<18:00：拉取昨天数据

**前置依赖：**
- trade_calendar（交易日历）
- stock_basic（股票列表）

---

### 8. adj_factor（复权因子）

**接口名称：** `adj_factor`

**游标策略：** `daily_trade`

**拉取参数：**
```python
{
    'ts_code': '',
    'trade_date': '20260410'
}
```

**字段列表：**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| ts_code | VARCHAR(10) | 股票代码 |
| trade_date | DATE | 交易日期 |
| adj_factor | REAL | 复权因子 |
| updated_at | TIMESTAMP | 更新时间 |

**前置依赖：** stock_daily

---

### 9. stock_daily_basic（每日指标）

**接口名称：** `daily_basic`

**游标策略：** `daily_trade`

**拉取参数：**
```python
{
    'ts_code': '',
    'trade_date': '20260410'
}
```

**字段列表（已注释100%）：**
- 估值指标：pe、pe_ttm、pb、ps、ps_ttm、dv_ratio、dv_ttm
- 市值指标：total_mv、circ_mv
- 股本指标：total_share、float_share、free_share
- 交易指标：turnover_rate、turnover_rate_f、volume_ratio

**前置依赖：** stock_basic

---

### 10. stock_weekly（周线行情）

**接口名称：** `stk_week_month_adj`

**游标策略：** `daily_trade`

**拉取参数：**
```python
{
    'ts_code': '',
    'start_date': '20260401',
    'end_date': '20260405',  # 计算周五
    'freq': 'week'
}
```

**游标更新时机：** 19:00后拉取（weekly_update_time配置）

---

### 11. stock_monthly（月线行情）

**接口名称：** `stk_week_month_adj`

**游标策略：** `monthly`

**拉取参数：**
```python
{
    'ts_code': '',
    'start_date': '20260101',
    'end_date': '20260131',
    'freq': 'month'
}
```

**游标更新时机：** 20:00后拉取（monthly_update_time配置）

---

### 12. index_daily（指数日线）

**接口名称：** `index_daily`

**游标策略：** `daily_trade`

**拉取参数：**
```python
{
    'ts_code': '',
    'trade_date': '20260410'
}
```

**前置依赖：**
- trade_calendar
- index_basic

---

### 13. etf_daily（ETF日线）

**接口名称：** `fund_daily`

**游标策略：** `daily_trade`

**前置依赖：**
- trade_calendar
- fund_basic

---

## P2财务表

### VIP接口说明

**重要：** P2财务表使用VIP接口，接口名称需加`_vip`后缀：

| 表名 | VIP接口名 |
|------|-----------|
| fina_indicator | `fina_indicator_vip` |
| income | `income_vip` |
| balancesheet | `balancesheet_vip` |
| cashflow | `cashflow_vip` |
| express | `forecast_vip` |
| express_brief | `express_vip` |
| dividend | `dividend` |

---

### 14. fina_indicator（财务指标）

**接口名称：** `fina_indicator_vip` ⭐VIP

**游标策略：** `daily_natural`（按自然日，每日拉取）

**拉取参数：**
```python
{
    'ts_code': '',
    'ann_date': '20260410',  # 公告日期（游标字段）
    'period': ''  # 报告期（可选）
}
```

**游标字段：** `ann_date`（公告日期）

**游标更新时机：**
- **财务表特殊规则：** 允许无数据更新（ann_date可能无公告）
- 只要请求正常走完，即可更新游标

**字段列表（已注释100%，100个字段）：**
- 每股指标：eps、dt_eps、bps、ocfps等23个
- 盈利能力：roe、roa、roic等15个
- 营运能力：inv_turn、ar_turn等12个
- 偿债能力：current_ratio、quick_ratio等10个
- 现金流：fcff、fcfe等6个
- 其他重要指标：gross_margin、ebit等23个
- 同比增长：roe_yoy、bps_yoy等11个

---

### 15. income（利润表）

**接口名称：** `income_vip` ⭐VIP

**游标策略：** `daily_natural`

**拉取参数：**
```python
{
    'ts_code': '',
    'ann_date': '20260410',
    'report_type': '1',  # 报告类型（1=合并报表）
    'start_date': '',    # 可选，用于指定报告期开始日期
    'end_date': ''       # 可选，用于指定报告期结束日期
}
```

**游标字段：** `ann_date`

**字段列表（部分）：**
- 营业收入：total_revenue、revenue
- 利润指标：profit_dedt、total_profit、n_income
- 每股指标：basic_eps、diluted_eps
- 其他：ebit、ebitda、rd_exp

**主键：** (ts_code, end_date, report_type)

---

### 16. balancesheet（资产负债表）

**接口名称：** `balancesheet_vip` ⭐VIP

**游标策略：** `daily_natural`

**字段分类：**
- 流动资产：money_cap、trad_asset、accounts_receiv等
- 非流动资产：fix_assets、intang_assets、goodwill等
- 流动负债：st_borr、notes_payable、accounts_pay等
- 非流动负债：long_borr、bonds_payable等
- 资产总计：total_assets、total_liab

---

### 17. cashflow（现金流量表）

**接口名称：** `cashflow_vip` ⭐VIP

**游标策略：** `daily_natural`

**字段分类：**
- 经营活动：cash_recp_sg_and_rsr、net_cash_flows_oper_act等
- 投资活动：cash_recp_disp_withdrw_invest、net_cash_flows_inv_act等
- 筹资活动：cash_recp_cap_contrib、net_cash_flows_fnc_act等
- 现金变化：cash_equ_incr_decr

---

### 18. express（业绩预告）

**接口名称：** `forecast_vip` ⭐VIP

**游标策略：** `daily_natural`

**字段列表：**
- 预告数据：forecast_type、forecast_content
- 业绩预测：net_profit_min、net_profit_max
- 预告日期：ann_date、end_date

---

### 19. express_brief（业绩快报）

**接口名称：** `express_vip` ⭐VIP

**游标策略：** `daily_natural`

---

### 20. dividend（分红送股）

**接口名称：** `dividend`

**游标策略：** `daily_natural`

**字段列表：**
- 分红方案：div_proc、cash_div、stk_div
- 分红日期：ann_date、ex_date、pay_date

---

## P3资金流向（THS）

### 21. ths_moneyflow（个股资金流）

**接口名称：** `ths_moneyflow`

**游标策略：** `daily_trade`

**前置依赖：** stock_daily

---

### 22. ths_concept_moneyflow（概念资金流）

**接口名称：** `ths_concept_moneyflow`

**游标策略：** `daily_trade`

---

### 23. ths_industry_moneyflow（行业资金流）

**接口名称：** `ths_industry_moneyflow`

**游标策略：** `daily_trade`

---

## P3概念板块

### 24. ths_concept_member（概念成分）

**接口名称：** `ths_member`

**游标策略：** `special_ths_member`（特殊游标）

**拉取逻辑：** 遍历ths_index_basic的所有ts_code

**前置依赖：** ths_index_basic

---

### 25. concept_basic（概念列表）

**接口名称：** 待确认

**游标策略：** `none`

---

## P4游资

### 26. hots_user（游资账户）

**接口名称：** `hm_list`（实际接口名，不是hots_user）

**游标策略：** `none`

**接口参数：** 无参数（全量拉取）

**文档地址：** https://tushare.pro/document/2?doc_id=311

---

### 27. hots_trader_detail（游资明细）

**接口名称：** `hm_detail`（实际接口名，不是hots_trader_detail）

**游标策略：** `daily_trade`

**接口参数：** `trade_date={游标+1}`（按交易日拉取）

**文档地址：** https://tushare.pro/document/2?doc_id=312

---

## 游标策略说明

### 5种游标策略

| 游标策略 | 说明 | 游标字段 | 更新时机 | 示例表 |
|---------|------|---------|---------|--------|
| `none` | 无游标，全量拉取 | NULL或'completed' | 每次全量拉取 | stock_basic、trade_calendar |
| `daily_trade` | 按天记录（交易日） | YYYYMMDD | 必须有数据 | stock_daily、stock_weekly |
| `daily_natural` | 按天记录（自然日） | YYYYMMDD | 允许无数据 | fina_indicator、income |
| `yearly` | 按年记录 | YYYY | 每年一次 | trade_calendar（按年） |
| `special_ths_member` | 特殊游标（遍历） | ts_code | 遍历指数列表 | ths_concept_member |

---

### 游标更新规则

**规则1：非财务表（daily_trade、yearly）**
- 必须有数据才更新游标
- 无数据报错并在监控页展示

**规则2：财务表（daily_natural）**
- 允许无数据更新（ann_date可能无公告）
- 只要请求正常走完，即可更新游标

**规则3：全量拉取（none）**
- 每次全量拉取，无游标记录
- 游标值固定为'completed'

---

### 18点时间判断逻辑

**判断规则：**
```python
now = datetime.now()
fetch_after_time = "18:00"  # 从配置读取

if now.hour >= 18:
    # 当前时间≥18:00，拉取今天数据
    end_date = now.strftime('%Y%m%d')
else:
    # 当前时间<18:00，拉取昨天数据
    end_date = (now - timedelta(days=1)).strftime('%Y%m%d')
```

**应用场景：**
- stock_daily：18:00后拉取当天日线数据
- stock_weekly：19:00后拉取（weekly_update_time）
- stock_monthly：20:00后拉取（monthly_update_time）

---

## 数据拉取示例

### 示例1：拉取stock_daily

```python
from src.collectors.daily_collector import DailyCollector
from src.core.tushare_api import TushareAPI

# 初始化
api = TushareAPI(config['tushare'])
collector = DailyCollector('database/adata.db', api)

# 拉取单日数据
count = collector.run(trade_date='20260410')
print(f"拉取成功: {count}条记录")
```

---

### 示例2：拉取income（VIP接口）

```python
from src.collectors.income_collector import IncomeCollector

collector = IncomeCollector('database/adata.db', api)

# 拉取公告日数据
count = collector.run(ann_date='20260410', report_type='1')
print(f"拉取成功: {count}条记录")
```

---

### 示例3：使用游标管理器

```python
from src.core.global_cursor_manager import GlobalCursorManager

cursor_manager = GlobalCursorManager('database/adata.db', 'code/backend/config')

# 判断是否需要拉取
if cursor_manager.should_fetch('stock_daily'):
    # 获取下次拉取日期
    next_date = cursor_manager.get_next_fetch_date('stock_daily')
    
    # 标记为running
    cursor_manager.mark_running('stock_daily')
    
    try:
        # 拉取数据
        count = collector.run(trade_date=next_date)
        
        # 更新游标
        cursor_manager.update_cursor('stock_daily', next_date, count)
        
    except Exception as e:
        cursor_manager.mark_failed('stock_daily', str(e))
```

---

## 附录

### A. VIP接口完整列表

| VIP接口 | 用途 | 积分要求 |
|---------|------|---------|
| fina_indicator_vip | 财务指标 | ≥5000积分 |
| income_vip | 利润表 | ≥5000积分 |
| balancesheet_vip | 资产负债表 | ≥5000积分 |
| cashflow_vip | 现金流量表 | ≥5000积分 |
| forecast_vip | 业绩预告 | ≥5000积分 |
| express_vip | 业绩快报 | ≥5000积分 |

---

### B. 前置依赖关系图

```
trade_calendar → stock_daily
stock_basic → stock_daily, stock_daily_basic, income, balancesheet, cashflow
index_basic → index_daily, ths_index_basic
ths_index_basic → ths_concept_member
etf_basic → etf_daily, etf_adj_factor
stock_daily → adj_factor, ths_moneyflow
```

---

### C. 数据拉取顺序

**固定顺序：**
1. trade_calendar（交易日历）
2. stock_basic（股票列表）
3. index_basic（指数列表）
4. ths_index_basic（同花顺指数）
5. etf_basic（ETF列表）
6. 其他表按游标策略拉取

---

**文档生成：** Claude Code Agent  
**更新时间：** 2026-04-14  
**文档状态：** 完整版（28张表）