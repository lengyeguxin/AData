-- P0基础表（前置表，共6张）
-- 按固定顺序拉取：trade_calendar → stock_basic → index_basic → ths_index_basic → etf_basic → etf_index

-- 1. trade_calendar（交易日历）
CREATE TABLE IF NOT EXISTS trade_calendar (
    exchange VARCHAR(10),          -- 交易所代码（SSE=上交所,SZSE=深交所）
    cal_date DATE,                 -- 交易日期
    is_open INTEGER,               -- 是否交易（0=休市,1=交易）
    pretrade_date DATE,            -- 上一交易日

    -- 联合主键（exchange + cal_date）
    PRIMARY KEY (exchange, cal_date),

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

CREATE INDEX IF NOT EXISTS idx_trade_cal_date ON trade_calendar(cal_date);
CREATE INDEX IF NOT EXISTS idx_trade_cal_exchange ON trade_calendar(exchange);

-- 2. stock_basic（股票列表）
CREATE TABLE IF NOT EXISTS stock_basic (
    ts_code VARCHAR(10) PRIMARY KEY,  -- 股票代码（TS格式）
    name VARCHAR(50),                 -- 股票名称
    industry VARCHAR(50),             -- 所属行业
    market VARCHAR(10),               -- 市场类型（主板/中小板/创业板/科创板）
    list_date DATE,                   -- 上市日期
    delist_date DATE,                 -- 退市日期
    is_hs VARCHAR(2),                 -- 是否沪深港通标的（N=否,H=沪股通,S=深股通）

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

CREATE INDEX IF NOT EXISTS idx_stock_basic_code ON stock_basic(ts_code);
CREATE INDEX IF NOT EXISTS idx_stock_basic_market ON stock_basic(market);

-- 3. index_basic（指数列表）
CREATE TABLE IF NOT EXISTS index_basic (
    ts_code VARCHAR(10) PRIMARY KEY,  -- 指数代码（TS格式）
    name VARCHAR(50),                 -- 指数简称
    fullname VARCHAR(100),            -- 指数全称
    market VARCHAR(10),               -- 市场类型
    publisher VARCHAR(50),            -- 发布方
    index_type VARCHAR(20),           -- 指数类型
    category VARCHAR(20),             -- 指数类别
    base_date DATE,                   -- 基期
    base_point REAL,                  -- 基点
    list_date DATE,                   -- 发布日期
    weight_rule VARCHAR(20),          -- 加权方法
    description TEXT,                 -- 描述

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

CREATE INDEX IF NOT EXISTS idx_index_basic_code ON index_basic(ts_code);
CREATE INDEX IF NOT EXISTS idx_index_basic_market ON index_basic(market);

-- 4. ths_index_basic（同花顺概念和行业指数）
CREATE TABLE IF NOT EXISTS ths_index_basic (
    ts_code VARCHAR(10) PRIMARY KEY,  -- 指数代码（TI格式）
    name VARCHAR(50),                 -- 指数简称
    fullname VARCHAR(100),            -- 指数全称
    exchange VARCHAR(10),             -- 交易所
    type VARCHAR(10),                 -- 指数类型（N=概念,S=特色）
    list_date DATE,                   -- 发布日期
    weight_rule VARCHAR(20),          -- 加权方法
    description TEXT,                 -- 描述

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

CREATE INDEX IF NOT EXISTS idx_ths_index_basic_code ON ths_index_basic(ts_code);
CREATE INDEX IF NOT EXISTS idx_ths_index_basic_type ON ths_index_basic(type);

-- 5. etf_basic（ETF基本信息）
CREATE TABLE IF NOT EXISTS etf_basic (
    ts_code VARCHAR(10) PRIMARY KEY,  -- ETF代码（TS格式）
    name VARCHAR(50),                 -- ETF简称
    fullname VARCHAR(100),            -- ETF全称
    fund_type VARCHAR(20),            -- 基金类型
    fund_manager VARCHAR(50),         -- 基金经理
    list_date DATE,                   -- 上市日期
    issue_date DATE,                  -- 发行日期
    delist_date DATE,                 -- 退市日期
    issue_amount REAL,                -- 发行份额（万份）
    m_fee REAL,                       -- 管理费（%）
    c_fee REAL,                       -- 托管费（%）
    benchmark VARCHAR(200),           -- 跟踪标的
    status VARCHAR(10),               -- 状态
    invest_type VARCHAR(20),          -- 投资类型
    type VARCHAR(20),                 -- ETF类型
    trustee VARCHAR(50),              -- 托管人
    perf_benchmark VARCHAR(200),      -- 业绩比较基准

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
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