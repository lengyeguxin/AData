-- etf_daily (ETF日线行情)
-- API接口: etf_daily
-- API字段数: 11

CREATE TABLE IF NOT EXISTS etf_daily (
    ts_code VARCHAR(20),  -- TS代码
    trade_date DATE,  -- 交易日期
    open REAL,  -- 开盘价(元)
    high REAL,  -- 最高价(元)
    low REAL,  -- 最低价(元)
    close REAL,  -- 收盘价(元)
    pre_close REAL,  -- 昨收盘价(元)
    change REAL,  -- 涨跌额(元)
    pct_chg REAL,  -- 涨跌幅(%)
    vol REAL,  -- 成交量(手)
    amount REAL,  -- 成交额(千元)
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    PRIMARY KEY (ts_code, trade_date)
);

COMMENT ON TABLE etf_daily IS 'ETF日线行情';

COMMENT ON COLUMN etf_daily.ts_code IS 'TS代码';
COMMENT ON COLUMN etf_daily.trade_date IS '交易日期';
COMMENT ON COLUMN etf_daily.open IS '开盘价(元)';
COMMENT ON COLUMN etf_daily.high IS '最高价(元)';
COMMENT ON COLUMN etf_daily.low IS '最低价(元)';
COMMENT ON COLUMN etf_daily.close IS '收盘价(元)';
COMMENT ON COLUMN etf_daily.pre_close IS '昨收盘价(元)';
COMMENT ON COLUMN etf_daily.change IS '涨跌额(元)';
COMMENT ON COLUMN etf_daily.pct_chg IS '涨跌幅(%)';
COMMENT ON COLUMN etf_daily.vol IS '成交量(手)';
COMMENT ON COLUMN etf_daily.amount IS '成交额(千元)';
COMMENT ON COLUMN etf_daily.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_etf_daily_code ON etf_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_etf_daily_date ON etf_daily(trade_date);
