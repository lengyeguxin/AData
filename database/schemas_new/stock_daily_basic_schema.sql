-- stock_daily_basic (股票每日指标)
-- API接口: daily_basic
-- API字段数: 18

COMMENT ON TABLE stock_daily_basic IS '股票每日指标';

CREATE TABLE IF NOT EXISTS stock_daily_basic (
    ts_code VARCHAR(10),  -- TS代码
    trade_date DATE,  -- 交易日期
    circ_mv REAL,  -- 流通市值
    close REAL,  -- 收盘价
    dv_ratio REAL,  -- 股息率
    dv_ttm REAL,  -- 股息率TTM
    float_share REAL,  -- float_share
    free_share REAL,  -- 流通股本
    pb REAL,  -- 市净率
    pe REAL,  -- 市盈率
    pe_ttm REAL,  -- 市盈率TTM
    ps REAL,  -- 市销率
    ps_ttm REAL,  -- 市销率TTM
    total_mv REAL,  -- 总市值
    total_share REAL,  -- 总股本
    turnover_rate REAL,  -- 换手率
    turnover_rate_f REAL,  -- 比率
    volume_ratio REAL,  -- 量比
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE stock_daily_basic ADD PRIMARY KEY (ts_code, trade_date);

COMMENT ON COLUMN stock_daily_basic.ts_code IS 'TS代码';
COMMENT ON COLUMN stock_daily_basic.trade_date IS '交易日期';
COMMENT ON COLUMN stock_daily_basic.circ_mv IS '流通市值';
COMMENT ON COLUMN stock_daily_basic.close IS '收盘价';
COMMENT ON COLUMN stock_daily_basic.dv_ratio IS '股息率';
COMMENT ON COLUMN stock_daily_basic.dv_ttm IS '股息率TTM';
COMMENT ON COLUMN stock_daily_basic.free_share IS '流通股本';
COMMENT ON COLUMN stock_daily_basic.pb IS '市净率';
COMMENT ON COLUMN stock_daily_basic.pe IS '市盈率';
COMMENT ON COLUMN stock_daily_basic.pe_ttm IS '市盈率TTM';
COMMENT ON COLUMN stock_daily_basic.ps IS '市销率';
COMMENT ON COLUMN stock_daily_basic.ps_ttm IS '市销率TTM';
COMMENT ON COLUMN stock_daily_basic.total_mv IS '总市值';
COMMENT ON COLUMN stock_daily_basic.total_share IS '总股本';
COMMENT ON COLUMN stock_daily_basic.turnover_rate IS '换手率';
COMMENT ON COLUMN stock_daily_basic.turnover_rate_f IS '比率';
COMMENT ON COLUMN stock_daily_basic.volume_ratio IS '量比';

-- 索引
CREATE INDEX IF NOT EXISTS idx_stock_daily_basic_code ON stock_daily_basic(ts_code);
CREATE INDEX IF NOT EXISTS idx_stock_daily_basic_date ON stock_daily_basic(trade_date);
