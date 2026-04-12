-- P1行情表（共7张）
-- 按交易日每日拉取，游标记录最后完成的日期

-- 1. stock_daily（日线行情）
CREATE TABLE IF NOT EXISTS stock_daily (
    ts_code VARCHAR(10),
    trade_date DATE,

    -- 未复权数据
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    vol REAL,
    amount REAL,
    pct_chg REAL,

    -- 复权因子
    adj_factor REAL,

    -- 前复权数据
    open_adj REAL,
    high_adj REAL,
    low_adj REAL,
    close_adj REAL,

    -- 异常标记
    is_suspended BOOLEAN DEFAULT FALSE,
    is_abnormal BOOLEAN DEFAULT FALSE,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_daily_date ON stock_daily(trade_date);
CREATE INDEX IF NOT EXISTS idx_daily_code ON stock_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_daily_date_code ON stock_daily(trade_date, ts_code);

-- 2. stock_daily_basic（每日指标）
CREATE TABLE IF NOT EXISTS stock_daily_basic (
    ts_code VARCHAR(10),
    trade_date DATE,

    -- 估值指标
    pe REAL,
    pe_ttm REAL,
    pb REAL,
    ps REAL,
    ps_ttm REAL,
    dv_ratio REAL,

    -- 市值指标
    total_mv REAL,
    circ_mv REAL,

    -- 交易指标
    turnover_rate REAL,
    volume_ratio REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_basic_date ON stock_daily_basic(trade_date);
CREATE INDEX IF NOT EXISTS idx_basic_code ON stock_daily_basic(ts_code);
CREATE INDEX IF NOT EXISTS idx_basic_date_code ON stock_daily_basic(trade_date, ts_code);

-- 3. stock_weekly（周线行情）
CREATE TABLE IF NOT EXISTS stock_weekly (
    ts_code VARCHAR(10),
    trade_date DATE,

    -- 未复权数据
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    vol REAL,
    amount REAL,

    -- 复权因子
    adj_factor REAL,

    -- 前复权数据
    open_adj REAL,
    high_adj REAL,
    low_adj REAL,
    close_adj REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_weekly_date ON stock_weekly(trade_date);
CREATE INDEX IF NOT EXISTS idx_weekly_code ON stock_weekly(ts_code);
CREATE INDEX IF NOT EXISTS idx_weekly_date_code ON stock_weekly(trade_date, ts_code);

-- 4. stock_monthly（月线行情）
CREATE TABLE IF NOT EXISTS stock_monthly (
    ts_code VARCHAR(10),
    trade_date DATE,

    -- 未复权数据
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    vol REAL,
    amount REAL,

    -- 复权因子
    adj_factor REAL,

    -- 前复权数据
    open_adj REAL,
    high_adj REAL,
    low_adj REAL,
    close_adj REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_monthly_date ON stock_monthly(trade_date);
CREATE INDEX IF NOT EXISTS idx_monthly_code ON stock_monthly(ts_code);
CREATE INDEX IF NOT EXISTS idx_monthly_date_code ON stock_monthly(trade_date, ts_code);

-- 5. index_daily（指数日线）
CREATE TABLE IF NOT EXISTS index_daily (
    ts_code VARCHAR(10),
    trade_date DATE,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    vol REAL,
    amount REAL,
    pct_chg REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_index_daily_date ON index_daily(trade_date);
CREATE INDEX IF NOT EXISTS idx_index_daily_code ON index_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_index_daily_date_code ON index_daily(trade_date, ts_code);

-- 6. etf_daily（ETF日线行情）
CREATE TABLE IF NOT EXISTS etf_daily (
    ts_code VARCHAR(10),
    trade_date DATE,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    vol REAL,
    amount REAL,
    pct_chg REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_etf_daily_date ON etf_daily(trade_date);
CREATE INDEX IF NOT EXISTS idx_etf_daily_code ON etf_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_etf_daily_date_code ON etf_daily(trade_date, ts_code);

-- 7. etf_adj_factor（ETF复权因子）
CREATE TABLE IF NOT EXISTS etf_adj_factor (
    ts_code VARCHAR(10),
    trade_date DATE,
    adj_factor REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_etf_adj_date ON etf_adj_factor(trade_date);
CREATE INDEX IF NOT EXISTS idx_etf_adj_code ON etf_adj_factor(ts_code);
CREATE INDEX IF NOT EXISTS idx_etf_adj_date_code ON etf_adj_factor(trade_date, ts_code);