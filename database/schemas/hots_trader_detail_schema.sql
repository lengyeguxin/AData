-- hots_trader_detail (游资交易明细)
-- API接口: hots_trader_detail
-- API字段数: 9

COMMENT ON TABLE hots_trader_detail IS '游资交易明细';

CREATE TABLE IF NOT EXISTS hots_trader_detail (
    trade_date DATE,  -- 交易日期
    ts_code VARCHAR(20),  -- 股票代码
    ts_name VARCHAR(100),  -- 股票名称
    buy_amount REAL,  -- 买入金额（元）
    sell_amount REAL,  -- 卖出金额（元）
    net_amount REAL,  -- 净买卖（元）
    hm_name VARCHAR(100),  -- 游资名称
    hm_orgs VARCHAR(100),  -- 关联机构（一般为营业部或机构专用）
    tag VARCHAR(100),  -- 标签
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE hots_trader_detail ADD PRIMARY KEY (account, ts_code, trade_date);

COMMENT ON COLUMN hots_trader_detail.trade_date IS '交易日期';
COMMENT ON COLUMN hots_trader_detail.ts_code IS '股票代码';
COMMENT ON COLUMN hots_trader_detail.ts_name IS '股票名称';
COMMENT ON COLUMN hots_trader_detail.buy_amount IS '买入金额（元）';
COMMENT ON COLUMN hots_trader_detail.sell_amount IS '卖出金额（元）';
COMMENT ON COLUMN hots_trader_detail.net_amount IS '净买卖（元）';
COMMENT ON COLUMN hots_trader_detail.hm_name IS '游资名称';
COMMENT ON COLUMN hots_trader_detail.hm_orgs IS '关联机构（一般为营业部或机构专用）';
COMMENT ON COLUMN hots_trader_detail.tag IS '标签';
COMMENT ON COLUMN hots_trader_detail.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_account ON hots_trader_detail(account);
CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_code ON hots_trader_detail(ts_code);
CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_date ON hots_trader_detail(trade_date);
