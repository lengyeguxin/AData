-- index_daily (指数日线行情)
-- API接口: index_daily
-- API字段数: 11

COMMENT ON TABLE index_daily IS '指数日线行情';

CREATE TABLE IF NOT EXISTS index_daily (
    ts_code VARCHAR(10),  -- TS代码
    trade_date DATE,  -- 交易日期
    close REAL,  -- 收盘价
    open REAL,  -- 开盘价
    high REAL,  -- 最高价
    low REAL,  -- 最低价
    pre_close REAL,  -- 昨收价
    change REAL,  -- change
    pct_chg REAL,  -- pct_chg
    vol REAL,  -- 成交量
    amount REAL,  -- 成交额
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE index_daily ADD PRIMARY KEY (ts_code, trade_date);

COMMENT ON COLUMN index_daily.ts_code IS 'TS代码';
COMMENT ON COLUMN index_daily.trade_date IS '交易日期';
COMMENT ON COLUMN index_daily.close IS '收盘价';
COMMENT ON COLUMN index_daily.open IS '开盘价';
COMMENT ON COLUMN index_daily.high IS '最高价';
COMMENT ON COLUMN index_daily.low IS '最低价';
COMMENT ON COLUMN index_daily.pre_close IS '昨收价';
COMMENT ON COLUMN index_daily.vol IS '成交量';
COMMENT ON COLUMN index_daily.amount IS '成交额';

-- 索引
CREATE INDEX IF NOT EXISTS idx_index_daily_code ON index_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_index_daily_date ON index_daily(trade_date);
