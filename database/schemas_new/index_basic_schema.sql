-- index_basic (指数基本信息)
-- API接口: index_basic
-- API字段数: 8

COMMENT ON TABLE index_basic IS '指数基本信息';

CREATE TABLE IF NOT EXISTS index_basic (
    ts_code VARCHAR(10) PRIMARY KEY,  -- TS代码
    name VARCHAR(100),  -- 名称
    market VARCHAR(20),  -- 市场类型
    publisher VARCHAR(50),  -- 发布方
    category VARCHAR(20),  -- 类别
    base_date DATE,  -- 基期
    base_point REAL,  -- 基点
    list_date DATE,  -- 上市日期
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN index_basic.ts_code IS 'TS代码';
COMMENT ON COLUMN index_basic.name IS '名称';
COMMENT ON COLUMN index_basic.market IS '市场类型';
COMMENT ON COLUMN index_basic.publisher IS '发布方';
COMMENT ON COLUMN index_basic.category IS '类别';
COMMENT ON COLUMN index_basic.base_date IS '基期';
COMMENT ON COLUMN index_basic.base_point IS '基点';
COMMENT ON COLUMN index_basic.list_date IS '上市日期';

-- 索引
CREATE INDEX IF NOT EXISTS idx_index_basic_code ON index_basic(ts_code);
