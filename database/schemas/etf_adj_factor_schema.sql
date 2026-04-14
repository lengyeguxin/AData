-- etf_adj_factor (ETF复权因子)
-- API接口: etf_adj_factor
-- API字段数: 3

COMMENT ON TABLE etf_adj_factor IS 'ETF复权因子';

CREATE TABLE IF NOT EXISTS etf_adj_factor (
    ts_code VARCHAR(20),  -- ts基金代码
    trade_date DATE,  -- 交易日期
    adj_factor REAL,  -- 复权因子
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE etf_adj_factor ADD PRIMARY KEY (ts_code, trade_date);

COMMENT ON COLUMN etf_adj_factor.ts_code IS 'ts基金代码';
COMMENT ON COLUMN etf_adj_factor.trade_date IS '交易日期';
COMMENT ON COLUMN etf_adj_factor.adj_factor IS '复权因子';
COMMENT ON COLUMN etf_adj_factor.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_etf_adj_factor_code ON etf_adj_factor(ts_code);
CREATE INDEX IF NOT EXISTS idx_etf_adj_factor_date ON etf_adj_factor(trade_date);
