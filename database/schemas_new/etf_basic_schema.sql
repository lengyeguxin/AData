-- etf_basic (ETF基本信息)
-- API接口: etf_basic
-- API字段数: 14

COMMENT ON TABLE etf_basic IS 'ETF基本信息';

CREATE TABLE IF NOT EXISTS etf_basic (
    ts_code VARCHAR(10) PRIMARY KEY,  -- TS代码
    csname VARCHAR(100),  -- csname
    extname VARCHAR(100),  -- extname
    cname VARCHAR(100),  -- cname
    index_code VARCHAR(10),  -- index_code
    index_name VARCHAR(100),  -- index_name
    setup_date DATE,  -- setup_date
    list_date DATE,  -- 上市日期
    list_status VARCHAR(10),  -- list_status
    exchange REAL,  -- 交易所
    mgr_name VARCHAR(100),  -- mgr_name
    custod_name VARCHAR(100),  -- custod_name
    mgt_fee REAL,  -- mgt_fee
    etf_type REAL,  -- etf_type
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN etf_basic.ts_code IS 'TS代码';
COMMENT ON COLUMN etf_basic.list_date IS '上市日期';
COMMENT ON COLUMN etf_basic.exchange IS '交易所';

-- 索引
CREATE INDEX IF NOT EXISTS idx_etf_basic_code ON etf_basic(ts_code);
