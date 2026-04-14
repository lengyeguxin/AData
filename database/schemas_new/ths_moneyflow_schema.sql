-- ths_moneyflow (个股资金流向)
-- API接口: ths_moneyflow
-- 数据来源: Tushare API

COMMENT ON TABLE ths_moneyflow IS '个股资金流向';

CREATE TABLE IF NOT EXISTS ths_moneyflow (
    ts_code VARCHAR(10),  -- TS代码
    trade_date DATE,  -- 交易日期
    name VARCHAR(50),  -- 股票名称
    pct_change REAL,  -- 涨跌幅
    latest REAL,  -- 最新数据
    net_amount REAL,  -- 净金额
    net_d5_amount REAL,  -- 5日净金额
    buy_lg_amount REAL,  -- 大单买入金额
    buy_lg_amount_rate REAL,  -- 大单买入金额占比
    buy_md_amount REAL,  -- 中单买入金额
    buy_md_amount_rate REAL,  -- 中单买入金额占比
    buy_sm_amount REAL,  -- 小单买入金额
    buy_sm_amount_rate REAL,  -- 小单买入金额占比
    sell_lg_amount REAL,  -- 大单卖出金额
    sell_lg_amount_rate REAL,  -- 大单卖出金额占比
    sell_md_amount REAL,  -- 中单卖出金额
    sell_md_amount_rate REAL,  -- 中单卖出金额占比
    sell_sm_amount REAL,  -- 小单卖出金额
    sell_sm_amount_rate REAL,  -- 小单卖出金额占比
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN ths_moneyflow.ts_code IS 'TS代码';
COMMENT ON COLUMN ths_moneyflow.trade_date IS '交易日期';
COMMENT ON COLUMN ths_moneyflow.name IS '股票名称';
COMMENT ON COLUMN ths_moneyflow.pct_change IS '涨跌幅';
COMMENT ON COLUMN ths_moneyflow.latest IS '最新数据';
COMMENT ON COLUMN ths_moneyflow.net_amount IS '净金额';
COMMENT ON COLUMN ths_moneyflow.net_d5_amount IS '5日净金额';
COMMENT ON COLUMN ths_moneyflow.buy_lg_amount IS '大单买入金额';
COMMENT ON COLUMN ths_moneyflow.buy_lg_amount_rate IS '大单买入金额占比';
COMMENT ON COLUMN ths_moneyflow.buy_md_amount IS '中单买入金额';
COMMENT ON COLUMN ths_moneyflow.buy_md_amount_rate IS '中单买入金额占比';
COMMENT ON COLUMN ths_moneyflow.buy_sm_amount IS '小单买入金额';
COMMENT ON COLUMN ths_moneyflow.buy_sm_amount_rate IS '小单买入金额占比';
COMMENT ON COLUMN ths_moneyflow.sell_lg_amount IS '大单卖出金额';
COMMENT ON COLUMN ths_moneyflow.sell_lg_amount_rate IS '大单卖出金额占比';
COMMENT ON COLUMN ths_moneyflow.sell_md_amount IS '中单卖出金额';
COMMENT ON COLUMN ths_moneyflow.sell_md_amount_rate IS '中单卖出金额占比';
COMMENT ON COLUMN ths_moneyflow.sell_sm_amount IS '小单卖出金额';
COMMENT ON COLUMN ths_moneyflow.sell_sm_amount_rate IS '小单卖出金额占比';
COMMENT ON COLUMN ths_moneyflow.updated_at IS '更新时间';

ALTER TABLE ths_moneyflow ADD PRIMARY KEY (ts_code, trade_date);

CREATE INDEX IF NOT EXISTS idx_ths_moneyflow_ts_code ON ths_moneyflow(ts_code);
CREATE INDEX IF NOT EXISTS idx_ths_moneyflow_trade_date ON ths_moneyflow(trade_date);
CREATE INDEX IF NOT EXISTS idx_ths_moneyflow_name ON ths_moneyflow(name);