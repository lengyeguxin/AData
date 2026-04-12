-- P0基础表（前置表，共6张）
-- 按固定顺序拉取：trade_calendar → stock_basic → index_basic → ths_index_basic → etf_basic → etf_index

-- 1. trade_calendar（交易日历）
CREATE TABLE IF NOT EXISTS trade_calendar (
    exchange VARCHAR(10),
    cal_date DATE,
    is_open INTEGER,
    pretrade_date DATE,

    -- 联合主键（exchange + cal_date）
    PRIMARY KEY (exchange, cal_date),

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_trade_cal_date ON trade_calendar(cal_date);
CREATE INDEX IF NOT EXISTS idx_trade_cal_exchange ON trade_calendar(exchange);

-- 2. stock_basic（股票列表）
CREATE TABLE IF NOT EXISTS stock_basic (
    ts_code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    industry VARCHAR(50),
    market VARCHAR(10),
    list_date DATE,
    delist_date DATE,
    is_hs VARCHAR(2),

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_stock_basic_code ON stock_basic(ts_code);
CREATE INDEX IF NOT EXISTS idx_stock_basic_market ON stock_basic(market);

-- 3. index_basic（指数列表）
CREATE TABLE IF NOT EXISTS index_basic (
    ts_code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    fullname VARCHAR(100),
    market VARCHAR(10),
    publisher VARCHAR(50),
    index_type VARCHAR(20),
    category VARCHAR(20),
    base_date DATE,
    base_point REAL,
    list_date DATE,
    weight_rule VARCHAR(20),
    description TEXT,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_index_basic_code ON index_basic(ts_code);
CREATE INDEX IF NOT EXISTS idx_index_basic_market ON index_basic(market);

-- 4. ths_index_basic（同花顺概念和行业指数）
CREATE TABLE IF NOT EXISTS ths_index_basic (
    ts_code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    fullname VARCHAR(100),
    exchange VARCHAR(10),
    type VARCHAR(10),  -- N=概念, S=特色
    list_date DATE,
    weight_rule VARCHAR(20),
    description TEXT,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ths_index_basic_code ON ths_index_basic(ts_code);
CREATE INDEX IF NOT EXISTS idx_ths_index_basic_type ON ths_index_basic(type);

-- 5. etf_basic（ETF基本信息）
CREATE TABLE IF NOT EXISTS etf_basic (
    ts_code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50),
    fullname VARCHAR(100),
    fund_type VARCHAR(20),
    fund_manager VARCHAR(50),
    list_date DATE,
    issue_date DATE,
    delist_date DATE,
    issue_amount REAL,
    m_fee REAL,
    c_fee REAL,
    benchmark VARCHAR(200),
    status VARCHAR(10),
    invest_type VARCHAR(20),
    type VARCHAR(20),
    trustee VARCHAR(50),
    perf_benchmark VARCHAR(200),

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_etf_basic_code ON etf_basic(ts_code);
CREATE INDEX IF NOT EXISTS idx_etf_basic_type ON etf_basic(fund_type);

-- 6. etf_index（ETF基准指数）
CREATE TABLE IF NOT EXISTS etf_index (
    ts_code VARCHAR(10) PRIMARY KEY,  -- ETF代码
    index_code VARCHAR(10),           -- 跟踪指数代码
    index_name VARCHAR(50),           -- 跟踪指数名称
    tracking_type VARCHAR(20),        -- 跟踪类型
    tracking_ratio REAL,              -- 跟踪比例
    invest_type VARCHAR(20),          -- 投资类型

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_etf_index_code ON etf_index(ts_code);
CREATE INDEX IF NOT EXISTS idx_etf_index_index_code ON etf_index(index_code);