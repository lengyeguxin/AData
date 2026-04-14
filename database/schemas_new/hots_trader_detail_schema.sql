-- hots_trader_detail (游资交易明细)
-- API接口: hots_trader_detail
-- 数据来源: Tushare API

COMMENT ON TABLE hots_trader_detail IS '游资交易明细';

CREATE TABLE IF NOT EXISTS hots_trader_detail (
    account VARCHAR(50),  -- 账户
    ts_code VARCHAR(10),  -- TS代码
    trade_date DATE,  -- 交易日期
    buy_amount REAL,  -- 买入金额
    sell_amount REAL,  -- 卖出金额
    net_amount REAL,  -- 净金额
    buy_vol REAL,  -- 买入量
    sell_vol REAL,  -- 卖出量
    net_vol REAL,  -- 净量
    reason VARCHAR(500),  -- 原因
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN hots_trader_detail.account IS '账户';
COMMENT ON COLUMN hots_trader_detail.ts_code IS 'TS代码';
COMMENT ON COLUMN hots_trader_detail.trade_date IS '交易日期';
COMMENT ON COLUMN hots_trader_detail.buy_amount IS '买入金额';
COMMENT ON COLUMN hots_trader_detail.sell_amount IS '卖出金额';
COMMENT ON COLUMN hots_trader_detail.net_amount IS '净金额';
COMMENT ON COLUMN hots_trader_detail.buy_vol IS '买入量';
COMMENT ON COLUMN hots_trader_detail.sell_vol IS '卖出量';
COMMENT ON COLUMN hots_trader_detail.net_vol IS '净量';
COMMENT ON COLUMN hots_trader_detail.reason IS '原因';
COMMENT ON COLUMN hots_trader_detail.updated_at IS '更新时间';

ALTER TABLE hots_trader_detail ADD PRIMARY KEY (account, ts_code, trade_date);

CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_account ON hots_trader_detail(account);
CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_ts_code ON hots_trader_detail(ts_code);
CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_trade_date ON hots_trader_detail(trade_date);