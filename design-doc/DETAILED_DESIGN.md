# AData项目详细技术设计文档

## 文档概述

本文档详细描述A股数据项目的数据拉取系统设计，包括游标策略、接口规范、时间判断逻辑和数据处理流程。

---

## 一、数据表概览

### 1.1 表统计信息

**总计：27张数据表**

按优先级分类：
- **P0基础**：6张表（trade_calendar、stock_basic、index_basic、ths_index_basic、etf_basic、etf_index）
- **P1行情**：7张表（stock_daily、stock_daily_basic、stock_weekly、stock_monthly、index_daily、etf_daily、etf_adj_factor）
- **P2财务**：7张表（fina_indicator、income、balancesheet、cashflow、express、express_brief、dividend）
- **P3资金流向(THS)**：3张表（ths_moneyflow、ths_concept_moneyflow、ths_industry_moneyflow）
- **P3概念板块**：2张表（ths_concept_member、ths_index_daily）
- **P4游资**：2张表（hots_user、hots_trader_detail）

### 1.2 前置表依赖

**固定前置表（按顺序拉取）：**

1. trade_calendar（交易日历）
2. stock_basic（股票列表）
3. index_basic（指数列表）
4. ths_index_basic（同花顺指数列表）
5. etf_basic（ETF基本信息）
6. etf_index（ETF基准指数）

---

## 二、游标策略分类

### 2.1 无游标（全量拉取）

**适用表：**
- stock_basic
- trade_calendar（按年全量）
- index_basic
- etf_basic
- etf_index
- hots_user
- ths_index_basic

**特点：**
- 每次拉取全部数据
- 按月或按年定期更新
- 游标值：NULL或'completed'
- 不记录具体进度，每次全量刷新

### 2.2 按天记录（交易日）

**适用表：**
- stock_daily
- stock_daily_basic
- stock_weekly
- stock_monthly
- index_daily
- etf_daily
- etf_adj_factor
- hots_trader_detail
- ths_moneyflow
- ths_concept_moneyflow
- ths_industry_moneyflow
- ths_index_daily

**游标字段：**
- trade_date或start_date
- 游标示例：'20260409'

**更新频率：**
- 交易日每日拉取

**时间判断（18点判断）：**
- 当前时间 ≥ 18:00（可配置）：使用今天日期作为结束日期
- 当前时间 < 18:00：使用昨日日期作为结束日期

**游标更新规则：**
- **必须有数据**才更新游标
- 无数据则报错，在监控页展示异常

### 2.3 按天记录（自然日）

**适用表：**
- fina_indicator
- income
- balancesheet
- cashflow
- express
- express_brief
- dividend

**游标字段：**
- ann_date（公告日期）
- 游标示例：'20260409'

**更新频率：**
- 自然日每日拉取

**特点：**
- 不受交易日历限制
- 可能某日无数据（正常情况）

**游标更新规则：**
- 请求完毕且逻辑正常走完，即可更新游标
- **允许无数据**情况下更新游标

### 2.4 按年记录

**适用表：**
- trade_calendar

**游标字段：**
- start_date（年份）
- 游标示例：'2025'

**更新频率：**
- 每年拉取一次

### 2.5 特殊游标

**适用表：**
- ths_concept_member

**游标字段：**
- ts_code（指数代码）
- 游标示例：'885472.TI'

**拉取方式：**
- 遍历ths_index_basic的所有指数代码
- 游标记录当前遍历到的指数代码

---

## 三、接口参数规范

### 3.1 无游标表参数

| 表名 | 接口名 | 关键参数 |
|------|--------|---------|
| stock_basic | stock_basic | 无参数 |
| trade_calendar | trade_cal | exchange=SSE/SZSE, start_date={游标年+1}0101, end_date={当前年}1231 |
| index_basic | index_basic | market=SSE/SZSE（分两次拉取） |
| etf_basic | etf_basic | 无参数 |
| etf_index | etf_index | 无参数 |
| hots_user | hots_user | 无参数 |
| ths_index_basic | ths_index | exchange=A, type=N/S |

### 3.2 按天记录（交易日）表参数

| 表名 | 接口名 | 关键参数 |
|------|--------|---------|
| stock_daily | daily | trade_date={游标+1}, adj=null |
| stock_daily_basic | daily_basic | trade_date={游标+1}, adj=null |
| stock_weekly | stk_week_month_adj | start_date={游标+1}, end_date={计算周五}, freq=week |
| stock_monthly | stk_week_month_adj | start_date={游标+1}, end_date={计算周五}, freq=month |
| index_daily | index_daily | trade_date={游标+1} |
| etf_daily | fund_daily | trade_date={游标+1} |
| etf_adj_factor | fund_adj | trade_date={游标+1} |
| hots_trader_detail | hots_trader_detail | trade_date={游标+1} |
| ths_moneyflow | moneyflow_ths | trade_date={游标+1} |
| ths_concept_moneyflow | moneyflow_cnt_ths | trade_date={游标+1} |
| ths_industry_moneyflow | moneyflow_ind_ths | trade_date={游标+1} |
| ths_index_daily | ths_daily | trade_date={游标+1} |

### 3.3 按天记录（自然日）表参数

| 表名 | 接口名 | 关键参数 | 说明 |
|------|--------|---------|------|
| fina_indicator | fina_indicator_vip | ann_date={游标+1} | VIP接口 |
| income | income_vip | ann_date={游标+1}, report_type=1 | VIP接口 |
| balancesheet | balancesheet_vip | ann_date={游标+1}, report_type=1 | VIP接口 |
| cashflow | cashflow_vip | ann_date={游标+1}, report_type=1 | VIP接口 |
| express | forecast_vip | ann_date={游标+1} | VIP接口 |
| express_brief | express_vip | ann_date={游标+1} | VIP接口 |
| dividend | dividend | ann_date={游标+1} | 标准接口 |

### 3.4 特殊游标表参数

| 表名 | 接口名 | 关键参数 |
|------|--------|---------|
| ths_concept_member | ths_member | 遍历ths_index_basic: ts_code={指数代码} |

---

## 四、时间判断逻辑

### 4.1 18点判断算法

```python
def get_end_date_with_time_check() -> str:
    """
    获取结束日期（带18点时间判断）
    
    Returns:
        YYYYMMDD格式的结束日期
    """
    now = datetime.now()
    hour = now.hour
    
    # 从配置获取截止时间（默认18:00）
    fetch_after_hour = 18
    
    if hour >= fetch_after_hour:
        # 当前时间≥截止时间，使用今天日期
        return now.strftime('%Y%m%d')
    else:
        # 当前时间<截止时间，使用昨日日期
        yesterday = now - timedelta(days=1)
        return yesterday.strftime('%Y%m%d')
```

### 4.2 日期遍历流程

**按天记录（交易日）表：**

```python
def fetch_daily_table(table_name):
    # 1. 获取游标值
    cursor_value = get_cursor(table_name)  # 如'20260408'
    
    # 2. 计算起始日期（游标+1）
    start_date = increment_date(cursor_value)  # '20260409'
    
    # 3. 计算结束日期（带18点判断）
    end_date = get_end_date_with_time_check()  # 今天或昨日
    
    # 4. 加载交易日历（启动时已加载）
    trade_dates = filter_trade_dates(start_date, end_date)
    
    # 5. 遍历交易日
    for trade_date in trade_dates:
        fetch_and_save(table_name, trade_date)
    
    # 6. 更新游标（必须有数据）
    if has_data:
        update_cursor(table_name, end_date)
    else:
        raise_error_and_show_in_dashboard()
```

**按天记录（自然日）表：**

```python
def fetch_natural_daily_table(table_name):
    # 1. 获取游标值
    cursor_value = get_cursor(table_name)  # 如'20260408'
    
    # 2. 计算起始日期（游标+1）
    start_date = increment_date(cursor_value)  # '20260409'
    
    # 3. 计算结束日期（今天）
    end_date = datetime.now().strftime('%Y%m%d')
    
    # 4. 遍历自然日
    for date in range(start_date, end_date):
        fetch_and_save(table_name, date)
    
    # 5. 更新游标（允许无数据）
    update_cursor(table_name, end_date)
```

---

## 五、游标更新时机

### 5.1 规则对比

| 游标策略 | 游标更新条件 | 无数据处理 |
|----------|------------|----------|
| 无游标 | 不需要更新游标 | 无影响 |
| 按天记录（交易日） | 必须有数据 | 报错，监控页展示 |
| 按天记录（自然日） | 允许无数据 | 正常更新游标 |
| 按年记录 | 必须有数据 | 报错 |
| 特殊游标 | 必须有数据 | 报错 |

### 5.2 实现逻辑

```python
def should_update_cursor(table_name: str, has_data: bool) -> bool:
    """
    判断是否应该更新游标
    """
    strategy = get_cursor_strategy(table_name)
    
    # 财务表（按自然日），允许无数据更新
    if strategy == 'daily_natural':
        return True
    
    # 其他表，必须有数据才更新
    return has_data
```

---

## 六、全局游标表结构

### 6.1 数据库表设计

```sql
CREATE TABLE global_cursor (
    table_name VARCHAR(50) PRIMARY KEY,
    
    cursor_strategy VARCHAR(20) NOT NULL,  -- 游标策略
    cursor_value VARCHAR(20),              -- 游标值
    
    update_frequency VARCHAR(20),          -- 更新频率
    fetch_type VARCHAR(20),                -- 拉取方式
    
    dependencies TEXT,                     -- 前置表依赖
    fetch_after_time VARCHAR(10),          -- 截止时间（HH:MM）
    
    last_fetch_time TIMESTAMP,             -- 最后拉取时间
    last_record_count INTEGER DEFAULT 0,   -- 拉取记录数
    status VARCHAR(10) DEFAULT 'pending',  -- 状态
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 6.2 游标策略枚举

```python
CURSOR_STRATEGY_NONE = 'none'                  # 无游标
CURSOR_STRATEGY_DAILY_TRADE = 'daily_trade'    # 按天（交易日）
CURSOR_STRATEGY_DAILY_NATURAL = 'daily_natural' # 按天（自然日）
CURSOR_STRATEGY_YEARLY = 'yearly'              # 按年
CURSOR_STRATEGY_SPECIAL_THS_MEMBER = 'special_ths_member' # 特殊
```

---

## 七、配置文件示例

### 7.1 主配置（config.yaml）

```yaml
database:
  path: database/adata.db
  type: duckdb

tushare:
  token: bd829d8919ffcdc1d18c1b99739286e913d65232edac5b3d2fc6c362a2ca
  api_url: http://lianghua.nanyangqiankun.top
  rate_limit: 500  # 每分钟500次（1万积分）

fetch:
  enabled: true                    # 数据拉取开关
  start_date: "20210101"           # 最早开始时间
  check_interval: 60               # 检测间隔（分钟）

scheduler:
  daily_update_time: "18:00"       # 日数据更新时间（18点判断）
  
snapshot:
  enabled: true
  interval: 30                     # 快照间隔（分钟）
  locations:
    - database/adata_snapshot.db
    - /home/my/claude-project/AiStock/database/adata_snapshot.db
```

### 7.2 表配置（table_config.yaml）

```yaml
tables:
  # 示例：无游标表
  stock_basic:
    cursor_strategy: none
    update_frequency: monthly
    fetch_type: full
    dependencies: []
    api_name: stock_basic
    
  # 示例：按天记录（交易日）
  stock_daily:
    cursor_strategy: daily_trade
    update_frequency: daily
    fetch_type: incremental
    dependencies: [trade_calendar, stock_basic]
    fetch_after_time: "18:00"
    api_name: daily
    
  # 示例：按天记录（自然日）
  income:
    cursor_strategy: daily_natural
    update_frequency: daily
    fetch_type: incremental
    dependencies: [stock_basic]
    fetch_after_time: "20:00"
    api_name: income_vip
    cursor_field: ann_date
    
  # 示例：特殊游标
  ths_concept_member:
    cursor_strategy: special_ths_member
    update_frequency: monthly
    fetch_type: full
    dependencies: [ths_index_basic]
    api_name: ths_member
    cursor_field: ts_code
```

---

## 八、数据处理流程图

### 8.1 启动流程

```
启动应用
    ↓
加载配置
    ↓
初始化数据库（详见下方）
    ↓
加载交易日历（一次性加载）
    ↓
检查fetch.enabled开关
    ↓
【开启】
    ↓
按固定顺序拉取前置表
    ↓
遍历其他表，检查游标
    ↓
根据游标策略执行拉取
    ↓
更新游标
    ↓
启动定时任务（快照）
```

**初始化数据库详细步骤：**

1. **连接数据库文件**
   - 打开DuckDB数据库文件（adata.db）
   - 如果文件不存在，创建新数据库

2. **创建表结构**
   - 执行SQL脚本，创建27张数据表
   - 如果表已存在，跳过创建
   - 按照schema文件顺序执行：p0_schema.sql、p1_schema.sql、p2_schema.sql

3. **创建全局游标表**
   - 创建global_cursor表（记录每张表的游标状态）
   - 如果表已存在，跳过创建
   - 初始化游标记录（每张表一条记录，状态为'pending'）

4. **创建索引**
   - 为各表创建必要的索引（如trade_date、ts_code等）
   - 为global_cursor表创建索引（cursor_type、status）

5. **验证表结构完整性**
   - 检查关键字段是否存在（主键、游标字段）
   - 检查索引是否正常工作
   - 记录验证结果到日志

6. **完成初始化**
   - 保存数据库连接实例
   - 准备后续数据拉取

### 8.2 表拉取流程

```
读取游标值
    ↓
判断游标策略
    ↓
【无游标】
    → 全量拉取
    → 不更新游标
    
【按天记录（交易日）】
    → 计算起始日期（游标+1）
    → 计算结束日期（18点判断）
    → 过滤交易日
    → 遍历拉取
    → 判断是否有数据
        【有数据】→ 更新游标
        【无数据】→ 报错展示
        
【按天记录（自然日）】
    → 计算起始日期（游标+1）
    → 计算结束日期（今天）
    → 遍历自然日
    → 拉取数据（可能无数据）
    → 更新游标（允许无数据）
    
【特殊游标】
    → 遍历指数列表
    → 拉取成分
    → 更新游标（指数代码）
```

---

## 九、异常监控设计

### 9.1 异常类型

| 异常类型 | 说明 | 处理方式 |
|---------|------|---------|
| 无数据异常 | 按天记录（交易日）表无数据 | 记录到monitor表，Dashboard展示 |
| API限流 | 500次/分钟限制 | 自动重试，延迟5秒 |
| 网络异常 | 连接失败 | 重试3次 |
| 数据异常 | 数据格式错误 | 记录日志，跳过该日期 |

### 9.2 Dashboard展示

**监控页面内容：**
- 每张表的拉取状态（pending/running/success/failed）
- 游标值和最后拉取时间
- 无数据异常列表（表名、日期、错误信息）
- API调用统计（次数、成功率）

---

## 十、VIP接口说明

### 10.1 VIP接口列表

| 标准接口 | VIP接口 | 说明 |
|---------|--------|------|
| fina_indicator | fina_indicator_vip | 财务指标VIP版 |
| income | income_vip | 利润表VIP版 |
| balancesheet | balancesheet_vip | 资产负债表VIP版 |
| cashflow | cashflow_vip | 现金流量表VIP版 |
| express | forecast_vip | 业绩预告VIP版 |
| express_brief | express_vip | 业绩快报VIP版 |

### 10.2 VIP接口优势

- 更丰富的字段
- 更快的更新速度
- 更高的数据质量
- 支持更多查询参数

---

## 十一、关键设计决策

### 11.1 游标策略选择

**为什么财务表使用自然日游标？**

- 财务数据公告日期不遵循交易日历
- 可能某日无公告（正常情况）
- 允许无数据更新游标，避免死循环

**为什么其他表必须有数据才更新游标？**

- 日线数据等按交易日更新，必然有数据
- 无数据表示异常（API故障、网络问题）
- 报错并在Dashboard展示，便于用户介入

### 11.2 18点判断设计

**为什么需要18点判断？**

- Tushare数据更新时间通常在18:00后
- 避免18:00前拉取到不完整数据
- 确保数据完整性

**如何配置？**

- 在config.yaml设置daily_update_time
- 默认'18:00'，可根据实际情况调整

---

## 十二、总结

本详细设计文档描述了A股数据项目的核心数据拉取系统，包括：

1. **游标策略分类**：5种策略满足不同数据特性
2. **接口参数规范**：27张表的完整接口参数说明
3. **时间判断逻辑**：18点判断确保数据完整性
4. **游标更新时机**：区分交易日表和财务表的更新规则
5. **异常监控**：Dashboard实时展示异常状态

**核心优势：**

- 统一的游标管理（GlobalCursorManager）
- 避免重复爬取（数据存在性检查）
- 断点续传能力（游标记录进度）
- 异常监控机制（Dashboard展示）
- 配置化控制（YAML配置文件）

---

**文档版本：** 1.0
**最后更新：** 2026-04-11
**作者：** Claude Code Assistant