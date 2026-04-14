-- etf_adj_factor (ETF复权因子)
-- API接口: adj_factor
-- 数据来源: Tushare API

COMMENT ON TABLE etf_adj_factor IS 'ETF复权因子';

CREATE TABLE IF NOT EXISTS etf_adj_factor (
    ts_code VARCHAR(10),  -- TS代码
    trade_date DATE,  -- 交易日期
    adj_factor REAL,  -- 复权因子
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN etf_adj_factor.ts_code IS 'TS代码';
COMMENT ON COLUMN etf_adj_factor.trade_date IS '交易日期';
COMMENT ON COLUMN etf_adj_factor.adj_factor IS '复权因子';
COMMENT ON COLUMN etf_adj_factor.updated_at IS '更新时间';

ALTER TABLE etf_adj_factor ADD PRIMARY KEY (ts_code, trade_date);

CREATE INDEX IF NOT EXISTS idx_etf_adj_factor_code ON etf_adj_factor(ts_code);
CREATE INDEX IF NOT EXISTS idx_etf_adj_factor_date ON etf_adj_factor(trade_date);