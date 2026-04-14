-- hots_trader_detail (游资交易明细)
-- API接口: hots_trader_detail
-- API字段数: 9


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


-- 索引
CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_code ON hots_trader_detail(ts_code);
CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_date ON hots_trader_detail(trade_date);
