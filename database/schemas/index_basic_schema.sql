-- index_basic (指数基本信息)
-- API接口: index_basic
-- API字段数: 13

COMMENT ON TABLE index_basic IS '指数基本信息';

CREATE TABLE IF NOT EXISTS index_basic (
    ts_code VARCHAR(20) PRIMARY KEY,  -- TS代码
    name VARCHAR(100),  -- 简称
    fullname VARCHAR(100),  -- 指数全称
    market VARCHAR(20),  -- 市场
    publisher VARCHAR(100),  -- 发布方
    index_type VARCHAR(20),  -- 指数风格
    category VARCHAR(100),  -- 指数类别
    base_date DATE,  -- 基期
    base_point REAL,  -- 基点
    list_date DATE,  -- 发布日期
    weight_rule VARCHAR(100),  -- 加权方式
    desc VARCHAR(100),  -- 描述
    exp_date DATE,  -- 终止日期
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN index_basic.ts_code IS 'TS代码';
COMMENT ON COLUMN index_basic.name IS '简称';
COMMENT ON COLUMN index_basic.fullname IS '指数全称';
COMMENT ON COLUMN index_basic.market IS '市场';
COMMENT ON COLUMN index_basic.publisher IS '发布方';
COMMENT ON COLUMN index_basic.index_type IS '指数风格';
COMMENT ON COLUMN index_basic.category IS '指数类别';
COMMENT ON COLUMN index_basic.base_date IS '基期';
COMMENT ON COLUMN index_basic.base_point IS '基点';
COMMENT ON COLUMN index_basic.list_date IS '发布日期';
COMMENT ON COLUMN index_basic.weight_rule IS '加权方式';
COMMENT ON COLUMN index_basic.desc IS '描述';
COMMENT ON COLUMN index_basic.exp_date IS '终止日期';
COMMENT ON COLUMN index_basic.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_index_basic_code ON index_basic(ts_code);
