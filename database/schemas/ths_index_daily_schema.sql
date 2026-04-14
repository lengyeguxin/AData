-- ths_index_daily (同花顺指数日线行情)
-- API接口: ths_index_daily
-- API字段数: 14

COMMENT ON TABLE ths_index_daily IS '同花顺指数日线行情';

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
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE ths_index_daily ADD PRIMARY KEY (ts_code, trade_date);

COMMENT ON COLUMN ths_index_daily.ts_code IS 'TS指数代码';
COMMENT ON COLUMN ths_index_daily.trade_date IS '交易日';
COMMENT ON COLUMN ths_index_daily.close IS '收盘点位';
COMMENT ON COLUMN ths_index_daily.open IS '开盘点位';
COMMENT ON COLUMN ths_index_daily.high IS '最高点位';
COMMENT ON COLUMN ths_index_daily.low IS '最低点位';
COMMENT ON COLUMN ths_index_daily.pre_close IS '昨日收盘点';
COMMENT ON COLUMN ths_index_daily.avg_price IS '平均价';
COMMENT ON COLUMN ths_index_daily.change IS '涨跌点位';
COMMENT ON COLUMN ths_index_daily.pct_change IS '涨跌幅';
COMMENT ON COLUMN ths_index_daily.vol IS '成交量（手）';
COMMENT ON COLUMN ths_index_daily.turnover_rate IS '换手率（%）';
COMMENT ON COLUMN ths_index_daily.total_mv IS '总市值（元）';
COMMENT ON COLUMN ths_index_daily.float_mv IS '流通市值（元）';
COMMENT ON COLUMN ths_index_daily.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_ths_index_daily_code ON ths_index_daily(ts_code);
CREATE INDEX IF NOT EXISTS idx_ths_index_daily_date ON ths_index_daily(trade_date);
