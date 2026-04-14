-- stock_daily_basic (股票每日指标)
-- API接口: stock_daily_basic
-- API字段数: 18

CREATE TABLE IF NOT EXISTS stock_daily_basic (
    ts_code VARCHAR(20),  -- TS股票代码
    trade_date DATE,  -- 交易日期
    close REAL,  -- 当日收盘价
    turnover_rate REAL,  -- 换手率（%）
    turnover_rate_f REAL,  -- 换手率（自由流通股）
    volume_ratio REAL,  -- 量比
    pe REAL,  -- 市盈率（总市值/净利润， 亏损的PE为空）
    pe_ttm REAL,  -- 市盈率（TTM，亏损的PE为空）
    pb REAL,  -- 市净率（总市值/净资产）
    ps REAL,  -- 市销率
    ps_ttm REAL,  -- 市销率（TTM）
    dv_ratio REAL,  -- 股息率 （%）
    dv_ttm REAL,  -- 股息率（TTM）（%）
    total_share REAL,  -- 总股本 （万股）
    float_share REAL,  -- 流通股本 （万股）
    free_share REAL,  -- 自由流通股本 （万）
    total_mv REAL,  -- 总市值 （万元）
    circ_mv REAL,  -- 流通市值（万元）
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    PRIMARY KEY (ts_code, trade_date)
);



-- 索引
CREATE INDEX IF NOT EXISTS idx_stock_daily_basic_code ON stock_daily_basic(ts_code);
CREATE INDEX IF NOT EXISTS idx_stock_daily_basic_date ON stock_daily_basic(trade_date);
