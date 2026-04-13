-- P1行情表（共7张）
-- 按交易日每日拉取，游标记录最后完成的日期

-- 1. stock_daily（日线行情）
CREATE TABLE IF NOT EXISTS stock_daily (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期

    -- 未复权数据
    pre_close REAL,           -- 昨收价（除权价）
    open REAL,  -- 开盘价
    high REAL,  -- 最高价
    low REAL,  -- 最低价
    close REAL,  -- 收盘价
    change REAL,              -- 涨跌额
    pct_chg REAL,             -- 涨跌幅（%）
    vol REAL,                 -- 成交量（手）
    amount REAL,              -- 成交额（千元）

    -- 复权因子
    adj_factor REAL,  -- 复权因子

    -- 前复权数据
    open_adj REAL,  -- 前复权开盘价
    high_adj REAL,  -- 前复权最高价
    low_adj REAL,  -- 前复权最低价
    close_adj REAL,  -- 前复权收盘价

    -- 异常标记
    is_suspended BOOLEAN DEFAULT FALSE,  -- 是否停牌
    is_abnormal BOOLEAN DEFAULT FALSE,  -- 是否异常

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_daily_date ON stock_daily(trade_date);
CREATE INDEX IF NOT EXISTS idx_daily_code ON stock_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_daily_date_code ON stock_daily(trade_date, ts_code);

-- 2. stock_daily_basic（每日指标）
CREATE TABLE IF NOT EXISTS stock_daily_basic (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期
    close REAL,               -- 当日收盘价

    -- 估值指标
    pe REAL,  -- 市盈率（总市值/净利润）
    pe_ttm REAL,  -- 市盈率TTM（总市值/最近12个月净利润）
    pb REAL,  -- 市净率（总市值/净资产）
    ps REAL,  -- 市销率（总市值/营业收入）
    ps_ttm REAL,  -- 市销率TTM
    dv_ratio REAL,            -- 股息率（%）
    dv_ttm REAL,              -- 股息率TTM（%）

    -- 市值指标
    total_mv REAL,  -- 总市值（万元）
    circ_mv REAL,  -- 流通市值（万元）

    -- 股本指标（万股）
    total_share REAL,         -- 总股本
    float_share REAL,         -- 流通股本
    free_share REAL,          -- 自由流通股本

    -- 交易指标
    turnover_rate REAL,       -- 换手率（%）
    turnover_rate_f REAL,     -- 换手率（自由流通股）
    volume_ratio REAL,        -- 量比

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_basic_date ON stock_daily_basic(trade_date);
CREATE INDEX IF NOT EXISTS idx_basic_code ON stock_daily_basic(ts_code);
CREATE INDEX IF NOT EXISTS idx_basic_date_code ON stock_daily_basic(trade_date, ts_code);

-- 3. stock_weekly（周线行情）
CREATE TABLE IF NOT EXISTS stock_weekly (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期
    end_date DATE,            -- 计算截至日期
    freq VARCHAR(10),         -- 频率（week）

    -- 未复权数据
    pre_close REAL,           -- 上一周期收盘价
    open REAL,  -- 开盘价
    high REAL,  -- 最高价
    low REAL,  -- 最低价
    close REAL,  -- 收盘价
    change REAL,              -- 涨跌额
    pct_chg REAL,             -- 涨跌幅（%）
    vol REAL,  -- 成交量（手）
    amount REAL,  -- 成交额（千元）

    -- 前复权数据
    open_qfq REAL,  -- 前复权开盘价
    high_qfq REAL,  -- 前复权最高价
    low_qfq REAL,  -- 前复权最低价
    close_qfq REAL,  -- 前复权收盘价

    -- 后复权数据
    open_hfq REAL,  -- 后复权开盘价
    high_hfq REAL,  -- 后复权最高价
    low_hfq REAL,  -- 后复权最低价
    close_hfq REAL,  -- 后复权收盘价

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_weekly_date ON stock_weekly(trade_date);
CREATE INDEX IF NOT EXISTS idx_weekly_code ON stock_weekly(ts_code);
CREATE INDEX IF NOT EXISTS idx_weekly_date_code ON stock_weekly(trade_date, ts_code);

-- 4. stock_monthly（月线行情）
CREATE TABLE IF NOT EXISTS stock_monthly (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期
    end_date DATE,            -- 计算截至日期
    freq VARCHAR(10),         -- 频率（month）

    -- 未复权数据
    pre_close REAL,           -- 上一周期收盘价
    open REAL,  -- 开盘价
    high REAL,  -- 最高价
    low REAL,  -- 最低价
    close REAL,  -- 收盘价
    change REAL,              -- 涨跌额
    pct_chg REAL,             -- 涨跌幅（%）
    vol REAL,  -- 成交量（手）
    amount REAL,  -- 成交额（千元）

    -- 前复权数据
    open_qfq REAL,  -- 前复权开盘价
    high_qfq REAL,  -- 前复权最高价
    low_qfq REAL,  -- 前复权最低价
    close_qfq REAL,  -- 前复权收盘价

    -- 后复权数据
    open_hfq REAL,  -- 后复权开盘价
    high_hfq REAL,  -- 后复权最高价
    low_hfq REAL,  -- 后复权最低价
    close_hfq REAL,  -- 后复权收盘价

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_monthly_date ON stock_monthly(trade_date);
CREATE INDEX IF NOT EXISTS idx_monthly_code ON stock_monthly(ts_code);
CREATE INDEX IF NOT EXISTS idx_monthly_date_code ON stock_monthly(trade_date, ts_code);

-- 5. index_daily（指数日线）
CREATE TABLE IF NOT EXISTS index_daily (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期
    pre_close REAL,           -- 昨日收盘点
    open REAL,  -- 开盘价
    high REAL,  -- 最高价
    low REAL,  -- 最低价
    close REAL,  -- 收盘价
    change REAL,              -- 涨跌点
    pct_chg REAL,             -- 涨跌幅（%）
    vol REAL,  -- 成交量（手）
    amount REAL,  -- 成交额（千元）

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_index_daily_date ON index_daily(trade_date);
CREATE INDEX IF NOT EXISTS idx_index_daily_code ON index_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_index_daily_date_code ON index_daily(trade_date, ts_code);

-- 6. etf_daily（ETF日线行情）
CREATE TABLE IF NOT EXISTS etf_daily (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期
    pre_close REAL,           -- 昨日收盘价
    open REAL,  -- 开盘价
    high REAL,  -- 最高价
    low REAL,  -- 最低价
    close REAL,  -- 收盘价
    change REAL,              -- 涨跌额
    pct_chg REAL,             -- 涨跌幅（%）
    vol REAL,  -- 成交量（手）
    amount REAL,  -- 成交额（千元）

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_etf_daily_date ON etf_daily(trade_date);
CREATE INDEX IF NOT EXISTS idx_etf_daily_code ON etf_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_etf_daily_date_code ON etf_daily(trade_date, ts_code);

-- 7. etf_adj_factor（ETF复权因子）
CREATE TABLE IF NOT EXISTS etf_adj_factor (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期
    adj_factor REAL,  -- 复权因子

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_etf_adj_date ON etf_adj_factor(trade_date);
CREATE INDEX IF NOT EXISTS idx_etf_adj_code ON etf_adj_factor(ts_code);
CREATE INDEX IF NOT EXISTS idx_etf_adj_date_code ON etf_adj_factor(trade_date, ts_code);