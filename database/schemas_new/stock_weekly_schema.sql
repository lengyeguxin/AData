-- stock_weekly (股票周线行情)
-- API接口: weekly
-- 数据来源: Tushare API

COMMENT ON TABLE stock_weekly IS '股票周线行情';

CREATE TABLE IF NOT EXISTS stock_weekly (
    ts_code VARCHAR(10),  -- TS代码
    trade_date DATE,  -- 交易日期
    end_date DATE,  -- 周结束日期
    freq VARCHAR(10),  -- 频率
    pre_close REAL,  -- 上一周期收盘价
    open REAL,  -- 开盘价
    high REAL,  -- 最高价
    low REAL,  -- 最低价
    close REAL,  -- 收盘价
    change REAL,  -- 涨跌额
    pct_chg REAL,  -- 涨跌幅
    vol REAL,  -- 成交量
    amount REAL,  -- 成交额
    open_qfq REAL,  -- 前复权开盘价
    high_qfq REAL,  -- 前复权最高价
    low_qfq REAL,  -- 前复权最低价
    close_qfq REAL,  -- 前复权收盘价
    open_hfq REAL,  -- 后复权开盘价
    high_hfq REAL,  -- 后复权最高价
    low_hfq REAL,  -- 后复权最低价
    close_hfq REAL,  -- 后复权收盘价
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN stock_weekly.ts_code IS 'TS代码';
COMMENT ON COLUMN stock_weekly.trade_date IS '交易日期';
COMMENT ON COLUMN stock_weekly.end_date IS '周结束日期';
COMMENT ON COLUMN stock_weekly.freq IS '频率';
COMMENT ON COLUMN stock_weekly.pre_close IS '上一周期收盘价';
COMMENT ON COLUMN stock_weekly.open IS '开盘价';
COMMENT ON COLUMN stock_weekly.high IS '最高价';
COMMENT ON COLUMN stock_weekly.low IS '最低价';
COMMENT ON COLUMN stock_weekly.close IS '收盘价';
COMMENT ON COLUMN stock_weekly.change IS '涨跌额';
COMMENT ON COLUMN stock_weekly.pct_chg IS '涨跌幅';
COMMENT ON COLUMN stock_weekly.vol IS '成交量';
COMMENT ON COLUMN stock_weekly.amount IS '成交额';
COMMENT ON COLUMN stock_weekly.open_qfq IS '前复权开盘价';
COMMENT ON COLUMN stock_weekly.high_qfq IS '前复权最高价';
COMMENT ON COLUMN stock_weekly.low_qfq IS '前复权最低价';
COMMENT ON COLUMN stock_weekly.close_qfq IS '前复权收盘价';
COMMENT ON COLUMN stock_weekly.open_hfq IS '后复权开盘价';
COMMENT ON COLUMN stock_weekly.high_hfq IS '后复权最高价';
COMMENT ON COLUMN stock_weekly.low_hfq IS '后复权最低价';
COMMENT ON COLUMN stock_weekly.close_hfq IS '后复权收盘价';
COMMENT ON COLUMN stock_weekly.updated_at IS '更新时间';

ALTER TABLE stock_weekly ADD PRIMARY KEY (ts_code, trade_date);

CREATE INDEX IF NOT EXISTS idx_stock_weekly_code ON stock_weekly(ts_code);
CREATE INDEX IF NOT EXISTS idx_stock_weekly_date ON stock_weekly(trade_date);
CREATE INDEX IF NOT EXISTS idx_stock_weekly_end_date ON stock_weekly(end_date);