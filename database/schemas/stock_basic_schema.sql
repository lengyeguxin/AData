-- stock_basic (股票列表)
-- API接口: stock_basic
-- API字段数: 17

CREATE TABLE IF NOT EXISTS stock_basic (
    ts_code VARCHAR(20) PRIMARY KEY,  -- TS代码
    symbol VARCHAR(20),  -- 股票代码
    name VARCHAR(100),  -- 股票名称
    area VARCHAR(20),  -- 地域
    industry VARCHAR(50),  -- 所属行业
    fullname VARCHAR(100),  -- 股票全称
    enname VARCHAR(100),  -- 英文全称
    cnspell VARCHAR(100),  -- 拼音缩写
    market VARCHAR(20),  -- 市场类型（主板/创业板/科创板/CDR）
    exchange VARCHAR(20),  -- 交易所代码
    curr_type VARCHAR(20),  -- 交易货币
    list_status VARCHAR(20),  -- 上市状态 L上市 D退市 G过会未交易 P暂停上市
    list_date DATE,  -- 上市日期
    delist_date DATE,  -- 退市日期
    is_hs VARCHAR(100),  -- 是否沪深港通标的，N否 H沪股通 S深股通
    act_name VARCHAR(100),  -- 实控人名称
    act_ent_type VARCHAR(20),  -- 实控人企业性质
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON TABLE stock_basic IS '股票列表';

COMMENT ON COLUMN stock_basic.ts_code IS 'TS代码';
COMMENT ON COLUMN stock_basic.symbol IS '股票代码';
COMMENT ON COLUMN stock_basic.name IS '股票名称';
COMMENT ON COLUMN stock_basic.area IS '地域';
COMMENT ON COLUMN stock_basic.industry IS '所属行业';
COMMENT ON COLUMN stock_basic.fullname IS '股票全称';
COMMENT ON COLUMN stock_basic.enname IS '英文全称';
COMMENT ON COLUMN stock_basic.cnspell IS '拼音缩写';
COMMENT ON COLUMN stock_basic.market IS '市场类型（主板/创业板/科创板/CDR）';
COMMENT ON COLUMN stock_basic.exchange IS '交易所代码';
COMMENT ON COLUMN stock_basic.curr_type IS '交易货币';
COMMENT ON COLUMN stock_basic.list_status IS '上市状态 L上市 D退市 G过会未交易 P暂停上市';
COMMENT ON COLUMN stock_basic.list_date IS '上市日期';
COMMENT ON COLUMN stock_basic.delist_date IS '退市日期';
COMMENT ON COLUMN stock_basic.is_hs IS '是否沪深港通标的，N否 H沪股通 S深股通';
COMMENT ON COLUMN stock_basic.act_name IS '实控人名称';
COMMENT ON COLUMN stock_basic.act_ent_type IS '实控人企业性质';
COMMENT ON COLUMN stock_basic.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_stock_basic_code ON stock_basic(ts_code);
