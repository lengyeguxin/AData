-- etf_daily (ETF日线行情)
-- API接口: fund_daily
-- API字段数: 11

COMMENT ON TABLE etf_daily IS 'ETF日线行情';

CREATE TABLE IF NOT EXISTS etf_daily (
    ts_code VARCHAR(10),  -- TS代码
    trade_date DATE,  -- 交易日期
    pre_close REAL,  -- 昨收价
    open REAL,  -- 开盘价
    high REAL,  -- 最高价
    low REAL,  -- 最低价
    close REAL,  -- 收盘价
    change REAL,  -- change
    pct_chg REAL,  -- pct_chg
    vol REAL,  -- 成交量
    amount REAL,  -- 成交额
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE etf_daily ADD PRIMARY KEY (ts_code, trade_date);

COMMENT ON COLUMN etf_daily.ts_code IS 'TS代码';
COMMENT ON COLUMN etf_daily.trade_date IS '交易日期';
COMMENT ON COLUMN etf_daily.pre_close IS '昨收价';
COMMENT ON COLUMN etf_daily.open IS '开盘价';
COMMENT ON COLUMN etf_daily.high IS '最高价';
COMMENT ON COLUMN etf_daily.low IS '最低价';
COMMENT ON COLUMN etf_daily.close IS '收盘价';
COMMENT ON COLUMN etf_daily.vol IS '成交量';
COMMENT ON COLUMN etf_daily.amount IS '成交额';

-- 索引
CREATE INDEX IF NOT EXISTS idx_etf_daily_code ON etf_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_etf_daily_date ON etf_daily(trade_date);
