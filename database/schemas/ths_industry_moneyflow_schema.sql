-- ths_industry_moneyflow (同花顺行业资金流向)
-- API接口: ths_industry_moneyflow
-- API字段数: 12

CREATE TABLE IF NOT EXISTS ths_industry_moneyflow (
    trade_date DATE,  -- 交易日期
    ts_code VARCHAR(20),  -- 板块代码
    industry VARCHAR(100),  -- 板块名称
    lead_stock VARCHAR(100),  -- 领涨股票名称
    close REAL,  -- 收盘指数
    pct_change REAL,  -- 指数涨跌幅
    company_num VARCHAR(100),  -- 公司数量
    pct_change_stock REAL,  -- 领涨股涨跌幅
    close_price REAL,  -- 领涨股最新价
    net_buy_amount REAL,  -- 流入资金(亿元)
    net_sell_amount REAL,  -- 流出资金(亿元)
    net_amount REAL,  -- 净额(亿元)
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    PRIMARY KEY (ts_code, trade_date)
);

COMMENT ON TABLE ths_industry_moneyflow IS '同花顺行业资金流向';

COMMENT ON COLUMN ths_industry_moneyflow.trade_date IS '交易日期';
COMMENT ON COLUMN ths_industry_moneyflow.ts_code IS '板块代码';
COMMENT ON COLUMN ths_industry_moneyflow.industry IS '板块名称';
COMMENT ON COLUMN ths_industry_moneyflow.lead_stock IS '领涨股票名称';
COMMENT ON COLUMN ths_industry_moneyflow.close IS '收盘指数';
COMMENT ON COLUMN ths_industry_moneyflow.pct_change IS '指数涨跌幅';
COMMENT ON COLUMN ths_industry_moneyflow.company_num IS '公司数量';
COMMENT ON COLUMN ths_industry_moneyflow.pct_change_stock IS '领涨股涨跌幅';
COMMENT ON COLUMN ths_industry_moneyflow.close_price IS '领涨股最新价';
COMMENT ON COLUMN ths_industry_moneyflow.net_buy_amount IS '流入资金(亿元)';
COMMENT ON COLUMN ths_industry_moneyflow.net_sell_amount IS '流出资金(亿元)';
COMMENT ON COLUMN ths_industry_moneyflow.net_amount IS '净额(亿元)';
COMMENT ON COLUMN ths_industry_moneyflow.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_ths_industry_moneyflow_code ON ths_industry_moneyflow(ts_code);
CREATE INDEX IF NOT EXISTS idx_ths_industry_moneyflow_date ON ths_industry_moneyflow(trade_date);
