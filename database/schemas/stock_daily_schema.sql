-- stock_daily (股票日线行情)
-- API接口: stock_daily
-- API字段数: 11

COMMENT ON TABLE stock_daily IS '股票日线行情';

CREATE TABLE IF NOT EXISTS stock_daily (
    ts_code VARCHAR(20),  -- 股票代码
    trade_date DATE,  -- 交易日期
    open REAL,  -- 开盘价
    high REAL,  -- 最高价
    low REAL,  -- 最低价
    close REAL,  -- 收盘价
    pre_close REAL,  -- 昨收价【除权价】
    change REAL,  -- 涨跌额
    pct_chg REAL,  -- 涨跌幅（%） 【基于除权后的昨收计算的涨跌幅：（今收-除权昨收）/除权昨收 】
    vol REAL,  -- 成交量 （手）
    amount REAL,  -- 成交额 （千元）
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE stock_daily ADD PRIMARY KEY (ts_code, trade_date);

COMMENT ON COLUMN stock_daily.ts_code IS '股票代码';
COMMENT ON COLUMN stock_daily.trade_date IS '交易日期';
COMMENT ON COLUMN stock_daily.open IS '开盘价';
COMMENT ON COLUMN stock_daily.high IS '最高价';
COMMENT ON COLUMN stock_daily.low IS '最低价';
COMMENT ON COLUMN stock_daily.close IS '收盘价';
COMMENT ON COLUMN stock_daily.pre_close IS '昨收价【除权价】';
COMMENT ON COLUMN stock_daily.change IS '涨跌额';
COMMENT ON COLUMN stock_daily.pct_chg IS '涨跌幅（%） 【基于除权后的昨收计算的涨跌幅：（今收-除权昨收）/除权昨收 】';
COMMENT ON COLUMN stock_daily.vol IS '成交量 （手）';
COMMENT ON COLUMN stock_daily.amount IS '成交额 （千元）';
COMMENT ON COLUMN stock_daily.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_stock_daily_code ON stock_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_stock_daily_date ON stock_daily(trade_date);
