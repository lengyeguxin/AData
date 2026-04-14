-- ths_concept_moneyflow (同花顺概念板块资金流向)
-- API接口: ths_moneyflow
-- 数据来源: Tushare API

COMMENT ON TABLE ths_concept_moneyflow IS '同花顺概念板块资金流向';

CREATE TABLE IF NOT EXISTS ths_concept_moneyflow (
    ts_code VARCHAR(10),  -- 概念代码
    trade_date DATE,  -- 交易日期
    name VARCHAR(50),  -- 概念名称
    lead_stock VARCHAR(50),  -- 龙头股票
    close_price REAL,  -- 收盘价
    pct_change REAL,  -- 涨跌幅
    industry_index REAL,  -- 行业指数
    company_num INTEGER,  -- 公司数量
    pct_change_stock REAL,  -- 股票涨跌幅
    net_buy_amount REAL,  -- 净买入金额
    net_sell_amount REAL,  -- 净卖出金额
    net_amount REAL,  -- 净金额
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN ths_concept_moneyflow.ts_code IS '概念代码';
COMMENT ON COLUMN ths_concept_moneyflow.trade_date IS '交易日期';
COMMENT ON COLUMN ths_concept_moneyflow.name IS '概念名称';
COMMENT ON COLUMN ths_concept_moneyflow.lead_stock IS '龙头股票';
COMMENT ON COLUMN ths_concept_moneyflow.close_price IS '收盘价';
COMMENT ON COLUMN ths_concept_moneyflow.pct_change IS '涨跌幅';
COMMENT ON COLUMN ths_concept_moneyflow.industry_index IS '行业指数';
COMMENT ON COLUMN ths_concept_moneyflow.company_num IS '公司数量';
COMMENT ON COLUMN ths_concept_moneyflow.pct_change_stock IS '股票涨跌幅';
COMMENT ON COLUMN ths_concept_moneyflow.net_buy_amount IS '净买入金额';
COMMENT ON COLUMN ths_concept_moneyflow.net_sell_amount IS '净卖出金额';
COMMENT ON COLUMN ths_concept_moneyflow.net_amount IS '净金额';
COMMENT ON COLUMN ths_concept_moneyflow.updated_at IS '更新时间';

ALTER TABLE ths_concept_moneyflow ADD PRIMARY KEY (ts_code, trade_date);

CREATE INDEX IF NOT EXISTS idx_ths_concept_moneyflow_ts_code ON ths_concept_moneyflow(ts_code);
CREATE INDEX IF NOT EXISTS idx_ths_concept_moneyflow_trade_date ON ths_concept_moneyflow(trade_date);
CREATE INDEX IF NOT EXISTS idx_ths_concept_moneyflow_name ON ths_concept_moneyflow(name);