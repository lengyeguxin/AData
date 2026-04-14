-- etf_index (ETF基准指数)
-- API接口: etf_index
-- API字段数: 8

CREATE TABLE IF NOT EXISTS etf_index (
    ts_code VARCHAR(20) PRIMARY KEY,  -- 指数代码
    indx_name VARCHAR(100),  -- 指数全称
    indx_csname VARCHAR(100),  -- 指数简称
    pub_party_name VARCHAR(100),  -- 指数发布机构
    pub_date DATE,  -- 指数发布日期
    base_date DATE,  -- 指数基日
    bp REAL,  -- 指数基点(点)
    adj_circle VARCHAR(100),  -- 指数成份证券调整周期
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON TABLE etf_index IS 'ETF基准指数';

COMMENT ON COLUMN etf_index.ts_code IS '指数代码';
COMMENT ON COLUMN etf_index.indx_name IS '指数全称';
COMMENT ON COLUMN etf_index.indx_csname IS '指数简称';
COMMENT ON COLUMN etf_index.pub_party_name IS '指数发布机构';
COMMENT ON COLUMN etf_index.pub_date IS '指数发布日期';
COMMENT ON COLUMN etf_index.base_date IS '指数基日';
COMMENT ON COLUMN etf_index.bp IS '指数基点(点)';
COMMENT ON COLUMN etf_index.adj_circle IS '指数成份证券调整周期';
COMMENT ON COLUMN etf_index.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_etf_index_code ON etf_index(ts_code);
