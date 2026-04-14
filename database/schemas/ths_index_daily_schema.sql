-- ths_index_daily (同花顺指数日线行情)
-- API接口: ths_index_daily
-- API字段数: 14

CREATE TABLE IF NOT EXISTS ths_index_daily (
    ts_code VARCHAR(20),  -- TS指数代码
    trade_date DATE,  -- 交易日
    close REAL,  -- 收盘点位
    open REAL,  -- 开盘点位
    high REAL,  -- 最高点位
    low REAL,  -- 最低点位
    pre_close REAL,  -- 昨日收盘点
    avg_price REAL,  -- 平均价
    change REAL,  -- 涨跌点位
    pct_change REAL,  -- 涨跌幅
    vol REAL,  -- 成交量（手）
    turnover_rate REAL,  -- 换手率（%）
    total_mv REAL,  -- 总市值（元）
    float_mv REAL,  -- 流通市值（元）
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    PRIMARY KEY (ts_code, trade_date)
);



-- 索引
CREATE INDEX IF NOT EXISTS idx_ths_index_daily_code ON ths_index_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_ths_index_daily_date ON ths_index_daily(trade_date);
