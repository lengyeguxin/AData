-- etf_adj_factor (ETF复权因子)
-- API接口: etf_adj_factor
-- API字段数: 3


CREATE TABLE IF NOT EXISTS etf_adj_factor (
    ts_code VARCHAR(20),  -- ts基金代码
    trade_date DATE,  -- 交易日期
    adj_factor REAL,  -- 复权因子
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键


-- 索引
CREATE INDEX IF NOT EXISTS idx_etf_adj_factor_code ON etf_adj_factor(ts_code);
CREATE INDEX IF NOT EXISTS idx_etf_adj_factor_date ON etf_adj_factor(trade_date);
