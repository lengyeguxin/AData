-- etf_basic (ETF基本信息)
-- API接口: etf_basic
-- API字段数: 14

COMMENT ON TABLE etf_basic IS 'ETF基本信息';

CREATE TABLE IF NOT EXISTS etf_basic (
    ts_code VARCHAR(20) PRIMARY KEY,  -- 基金交易代码
    csname VARCHAR(100),  -- ETF中文简称
    extname VARCHAR(100),  -- ETF扩位简称(对应交易所简称)
    cname VARCHAR(100),  -- 基金中文全称
    index_code VARCHAR(20),  -- ETF基准指数代码
    index_name VARCHAR(100),  -- ETF基准指数中文全称
    setup_date DATE,  -- 设立日期（格式：YYYYMMDD）
    list_date DATE,  -- 上市日期（格式：YYYYMMDD）
    list_status VARCHAR(20),  -- 存续状态（L上市 D退市 P待上市）
    exchange VARCHAR(20),  -- 交易所（上交所SH 深交所SZ）
    mgr_name VARCHAR(100),  -- 基金管理人简称
    custod_name VARCHAR(100),  -- 基金托管人名称
    mgt_fee REAL,  -- 基金管理人收取的费用
    etf_type VARCHAR(20),  -- 基金投资通道类型（境内、QDII）
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN etf_basic.ts_code IS '基金交易代码';
COMMENT ON COLUMN etf_basic.csname IS 'ETF中文简称';
COMMENT ON COLUMN etf_basic.extname IS 'ETF扩位简称(对应交易所简称)';
COMMENT ON COLUMN etf_basic.cname IS '基金中文全称';
COMMENT ON COLUMN etf_basic.index_code IS 'ETF基准指数代码';
COMMENT ON COLUMN etf_basic.index_name IS 'ETF基准指数中文全称';
COMMENT ON COLUMN etf_basic.setup_date IS '设立日期（格式：YYYYMMDD）';
COMMENT ON COLUMN etf_basic.list_date IS '上市日期（格式：YYYYMMDD）';
COMMENT ON COLUMN etf_basic.list_status IS '存续状态（L上市 D退市 P待上市）';
COMMENT ON COLUMN etf_basic.exchange IS '交易所（上交所SH 深交所SZ）';
COMMENT ON COLUMN etf_basic.mgr_name IS '基金管理人简称';
COMMENT ON COLUMN etf_basic.custod_name IS '基金托管人名称';
COMMENT ON COLUMN etf_basic.mgt_fee IS '基金管理人收取的费用';
COMMENT ON COLUMN etf_basic.etf_type IS '基金投资通道类型（境内、QDII）';
COMMENT ON COLUMN etf_basic.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_etf_basic_code ON etf_basic(ts_code);
