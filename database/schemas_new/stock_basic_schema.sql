-- stock_basic (股票列表)
-- API接口: stock_basic
-- API字段数: 11

COMMENT ON TABLE stock_basic IS '股票列表';

CREATE TABLE IF NOT EXISTS stock_basic (
    ts_code VARCHAR(10) PRIMARY KEY,  -- TS代码
    symbol REAL,  -- symbol
    name VARCHAR(100),  -- 名称
    area REAL,  -- area
    industry VARCHAR(50),  -- 行业
    cnspell REAL,  -- cnspell
    market VARCHAR(20),  -- 市场类型
    list_status VARCHAR(10),  -- list_status
    list_date DATE,  -- 上市日期
    act_name VARCHAR(100),  -- act_name
    act_ent_type REAL,  -- act_ent_type
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN stock_basic.ts_code IS 'TS代码';
COMMENT ON COLUMN stock_basic.name IS '名称';
COMMENT ON COLUMN stock_basic.industry IS '行业';
COMMENT ON COLUMN stock_basic.market IS '市场类型';
COMMENT ON COLUMN stock_basic.list_date IS '上市日期';

-- 索引
CREATE INDEX IF NOT EXISTS idx_stock_basic_code ON stock_basic(ts_code);
