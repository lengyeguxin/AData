-- ths_index_daily (同花顺概念和行业指数日线)
-- API接口: ths_daily
-- 数据来源: Tushare API

COMMENT ON TABLE ths_index_daily IS '同花顺概念和行业指数日线';

CREATE TABLE IF NOT EXISTS ths_index_daily (
    ts_code VARCHAR(10),  -- TS代码
    trade_date DATE,  -- 交易日期
    open REAL,  -- 开盘价
    high REAL,  -- 最高价
    low REAL,  -- 最低价
    close REAL,  -- 收盘价
    vol REAL,  -- 成交量
    amount REAL,  -- 成交额
    pct_chg REAL,  -- 涨跌幅
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN ths_index_daily.ts_code IS 'TS代码';
COMMENT ON COLUMN ths_index_daily.trade_date IS '交易日期';
COMMENT ON COLUMN ths_index_daily.open IS '开盘价';
COMMENT ON COLUMN ths_index_daily.high IS '最高价';
COMMENT ON COLUMN ths_index_daily.low IS '最低价';
COMMENT ON COLUMN ths_index_daily.close IS '收盘价';
COMMENT ON COLUMN ths_index_daily.vol IS '成交量';
COMMENT ON COLUMN ths_index_daily.amount IS '成交额';
COMMENT ON COLUMN ths_index_daily.pct_chg IS '涨跌幅';
COMMENT ON COLUMN ths_index_daily.updated_at IS '更新时间';

ALTER TABLE ths_index_daily ADD PRIMARY KEY (ts_code, trade_date);

CREATE INDEX IF NOT EXISTS idx_ths_index_daily_ts_code ON ths_index_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_ths_index_daily_trade_date ON ths_index_daily(trade_date);