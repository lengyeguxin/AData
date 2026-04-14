-- stock_weekly (股票周线行情)
-- API接口: stock_weekly
-- API字段数: 21

CREATE TABLE IF NOT EXISTS stock_weekly (
    ts_code VARCHAR(20),  -- 股票代码
    trade_date DATE,  -- 交易日期（每周五或者月末日期）
    end_date DATE,  -- 计算截至日期
    freq VARCHAR(100),  -- 频率(周week,月month)
    open REAL,  -- (周/月)开盘价
    high REAL,  -- (周/月)最高价
    low REAL,  -- (周/月)最低价
    close REAL,  -- (周/月)收盘价
    pre_close REAL,  -- 上一(周/月)收盘价【除权价，前复权】
    open_qfq REAL,  -- 前复权(周/月)开盘价
    high_qfq REAL,  -- 前复权(周/月)最高价
    low_qfq REAL,  -- 前复权(周/月)最低价
    close_qfq REAL,  -- 前复权(周/月)收盘价
    open_hfq REAL,  -- 后复权(周/月)开盘价
    high_hfq REAL,  -- 后复权(周/月)最高价
    low_hfq REAL,  -- 后复权(周/月)最低价
    close_hfq REAL,  -- 后复权(周/月)收盘价
    vol REAL,  -- (周/月)成交量
    amount REAL,  -- (周/月)成交额
    change REAL,  -- (周/月)涨跌额
    pct_chg REAL,  -- (周/月)涨跌幅 【基于除权后的昨收计算的涨跌幅：（今收-除权昨收）/除权昨收 】
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    PRIMARY KEY (ts_code, trade_date)
);



-- 索引
CREATE INDEX IF NOT EXISTS idx_stock_weekly_code ON stock_weekly(ts_code);
CREATE INDEX IF NOT EXISTS idx_stock_weekly_date ON stock_weekly(trade_date);
