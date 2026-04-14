-- ths_index_basic (同花顺指数基本信息)
-- API接口: ths_index_basic
-- API字段数: 6


CREATE TABLE IF NOT EXISTS ths_index_basic (
    ts_code VARCHAR(20) PRIMARY KEY,  -- 代码
    name VARCHAR(100),  -- 名称
    count VARCHAR(100),  -- 成分个数
    exchange VARCHAR(20),  -- 交易所
    list_date DATE,  -- 上市日期
    type VARCHAR(20),  -- N概念指数S特色指数
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);


-- 索引
CREATE INDEX IF NOT EXISTS idx_ths_index_basic_code ON ths_index_basic(ts_code);
