-- Global Cursor表（全局游标管理）
-- 每张表一个游标，记录整体拉取进度

CREATE TABLE IF NOT EXISTS global_cursor (
    -- 主键
    table_name VARCHAR(50) PRIMARY KEY,  -- 表名

    -- 游标信息
    cursor_strategy VARCHAR(20) NOT NULL,  -- 游标策略：none/daily_trade/daily_natural/yearly/special_ths_member
    cursor_value VARCHAR(20),  -- 游标值：YYYYMMDD或YYYY或ts_code或completed

    -- 依赖和时间判断
    dependencies TEXT,  -- 前置表依赖，逗号分隔
    fetch_after_time VARCHAR(10),  -- 截至7时间判断，HH:MM格式（如18:00）

    -- 拉取状态
    last_fetch_time TIMESTAMP,  -- 最后成功拉取时间
    last_record_count INTEGER DEFAULT 0,  -- 最后拉取记录数
    status VARCHAR(10) DEFAULT 'pending',  -- 状态：pending/running/success/failed

    -- 时间戳
    created_at TIMESTAMP DEFAULT NOW(),  -- 创建时间
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_cursor_strategy ON global_cursor(cursor_strategy);
CREATE INDEX IF NOT EXISTS idx_status ON global_cursor(status);

-- 初始化数据（27张表）
INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'trade_calendar', 'yearly', '', '09:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'trade_calendar');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'stock_basic', 'none', '', '09:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'stock_basic');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'index_basic', 'none', '', '09:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'index_basic');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'ths_index_basic', 'none', '', '09:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'ths_index_basic');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'etf_basic', 'none', '', '09:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'etf_basic');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'etf_index', 'none', 'etf_basic', '09:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'etf_index');

-- P1行情（7张）
INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'stock_daily', 'daily_trade', 'trade_calendar,stock_basic', '18:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'stock_daily');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'stock_daily_basic', 'daily_trade', 'stock_basic', '18:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'stock_daily_basic');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'stock_weekly', 'daily_trade', 'trade_calendar,stock_basic', '19:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'stock_weekly');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'stock_monthly', 'daily_trade', 'trade_calendar,stock_basic', '20:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'stock_monthly');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'index_daily', 'daily_trade', 'trade_calendar,index_basic', '18:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'index_daily');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'etf_daily', 'daily_trade', 'trade_calendar,etf_basic', '18:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'etf_daily');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'etf_adj_factor', 'daily_trade', 'etf_daily', '18:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'etf_adj_factor');

-- P2财务（7张）
INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'fina_indicator', 'daily_natural', 'stock_basic', '20:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'fina_indicator');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'income', 'daily_natural', 'stock_basic', '20:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'income');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'balancesheet', 'daily_natural', 'stock_basic', '20:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'balancesheet');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'cashflow', 'daily_natural', 'stock_basic', '20:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'cashflow');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'express', 'daily_natural', 'stock_basic', '20:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'express');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'express_brief', 'daily_natural', 'stock_basic', '20:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'express_brief');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'dividend', 'daily_natural', 'stock_basic', '20:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'dividend');

-- P3资金流向(THS)（3张）
INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'ths_moneyflow', 'daily_trade', 'stock_daily', '18:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'ths_moneyflow');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'ths_concept_moneyflow', 'daily_trade', '', '18:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'ths_concept_moneyflow');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'ths_industry_moneyflow', 'daily_trade', '', '18:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'ths_industry_moneyflow');

-- P3概念板块（2张）
INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'ths_concept_member', 'special_ths_member', 'ths_index_basic', '09:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'ths_concept_member');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'ths_index_daily', 'daily_trade', 'trade_calendar,ths_index_basic', '18:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'ths_index_daily');

-- P4游资（2张）
INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'hots_user', 'none', '', '09:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'hots_user');

INSERT INTO global_cursor (table_name, cursor_strategy, dependencies, fetch_after_time)
SELECT 'hots_trader_detail', 'daily_trade', '', '18:00'
WHERE NOT EXISTS (SELECT 1 FROM global_cursor WHERE table_name = 'hots_trader_detail');