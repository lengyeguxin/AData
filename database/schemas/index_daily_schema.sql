-- index_daily (指数日线行情)
-- API接口: index_daily
-- API字段数: 11

CREATE TABLE IF NOT EXISTS index_daily (
    ts_code VARCHAR(20),  -- TS指数代码
    trade_date DATE,  -- 交易日
    close REAL,  -- 收盘点位
    open REAL,  -- 开盘点位
    high REAL,  -- 最高点位
    low REAL,  -- 最低点位
    pre_close REAL,  -- 昨日收盘点
    change REAL,  -- 涨跌点
    pct_chg REAL,  -- 涨跌幅（%）
    vol REAL,  -- 成交量（手）
    amount REAL,  -- 成交额（千元）
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    PRIMARY KEY (ts_code, trade_date)
);

COMMENT ON TABLE index_daily IS '指数日线行情';

COMMENT ON COLUMN index_daily.ts_code IS 'TS指数代码';
COMMENT ON COLUMN index_daily.trade_date IS '交易日';
COMMENT ON COLUMN index_daily.close IS '收盘点位';
COMMENT ON COLUMN index_daily.open IS '开盘点位';
COMMENT ON COLUMN index_daily.high IS '最高点位';
COMMENT ON COLUMN index_daily.low IS '最低点位';
COMMENT ON COLUMN index_daily.pre_close IS '昨日收盘点';
COMMENT ON COLUMN index_daily.change IS '涨跌点';
COMMENT ON COLUMN index_daily.pct_chg IS '涨跌幅（%）';
COMMENT ON COLUMN index_daily.vol IS '成交量（手）';
COMMENT ON COLUMN index_daily.amount IS '成交额（千元）';
COMMENT ON COLUMN index_daily.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_index_daily_code ON index_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_index_daily_date ON index_daily(trade_date);
