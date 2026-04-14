-- ths_index_basic (同花顺指数基本信息)
-- API接口: ths_index
-- API字段数: 6

COMMENT ON TABLE ths_index_basic IS '同花顺指数基本信息';

CREATE TABLE IF NOT EXISTS ths_index_basic (
    ts_code VARCHAR(10) PRIMARY KEY,  -- TS代码
    name VARCHAR(100),  -- 名称
    count REAL,  -- count
    exchange REAL,  -- 交易所
    list_date DATE,  -- 上市日期
    type REAL,  -- type
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN ths_index_basic.ts_code IS 'TS代码';
COMMENT ON COLUMN ths_index_basic.name IS '名称';
COMMENT ON COLUMN ths_index_basic.exchange IS '交易所';
COMMENT ON COLUMN ths_index_basic.list_date IS '上市日期';

-- 索引
CREATE INDEX IF NOT EXISTS idx_ths_index_basic_code ON ths_index_basic(ts_code);
