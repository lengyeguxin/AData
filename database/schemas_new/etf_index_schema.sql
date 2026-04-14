-- etf_index (ETF基准指数)
-- API接口: etf_index
-- API字段数: 8

COMMENT ON TABLE etf_index IS 'ETF基准指数';

CREATE TABLE IF NOT EXISTS etf_index (
    ts_code VARCHAR(10) PRIMARY KEY,  -- TS代码
    indx_name VARCHAR(100),  -- indx_name
    indx_csname VARCHAR(100),  -- indx_csname
    pub_party_name VARCHAR(100),  -- pub_party_name
    pub_date DATE,  -- pub_date
    base_date DATE,  -- 基期
    bp REAL,  -- bp
    adj_circle REAL,  -- adj_circle
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN etf_index.ts_code IS 'TS代码';
COMMENT ON COLUMN etf_index.base_date IS '基期';

-- 索引
CREATE INDEX IF NOT EXISTS idx_etf_index_code ON etf_index(ts_code);
