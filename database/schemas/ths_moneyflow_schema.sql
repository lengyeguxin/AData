-- ths_moneyflow (个股资金流向)
-- API接口: ths_moneyflow
-- API字段数: 13

CREATE TABLE IF NOT EXISTS ths_moneyflow (
    trade_date DATE,  -- 交易日期
    ts_code VARCHAR(20),  -- 股票代码
    name VARCHAR(100),  -- 股票名称
    pct_change REAL,  -- 涨跌幅
    latest REAL,  -- 最新价
    net_amount REAL,  -- 资金净流入(万元)
    net_d5_amount REAL,  -- 5日主力净额(万元)
    buy_lg_amount REAL,  -- 今日大单净流入额(万元)
    buy_lg_amount_rate REAL,  -- 今日大单净流入占比(%)
    buy_md_amount REAL,  -- 今日中单净流入额(万元)
    buy_md_amount_rate REAL,  -- 今日中单净流入占比(%)
    buy_sm_amount REAL,  -- 今日小单净流入额(万元)
    buy_sm_amount_rate REAL,  -- 今日小单净流入占比(%)
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    PRIMARY KEY (ts_code, trade_date)
);

COMMENT ON TABLE ths_moneyflow IS '个股资金流向';

COMMENT ON COLUMN ths_moneyflow.trade_date IS '交易日期';
COMMENT ON COLUMN ths_moneyflow.ts_code IS '股票代码';
COMMENT ON COLUMN ths_moneyflow.name IS '股票名称';
COMMENT ON COLUMN ths_moneyflow.pct_change IS '涨跌幅';
COMMENT ON COLUMN ths_moneyflow.latest IS '最新价';
COMMENT ON COLUMN ths_moneyflow.net_amount IS '资金净流入(万元)';
COMMENT ON COLUMN ths_moneyflow.net_d5_amount IS '5日主力净额(万元)';
COMMENT ON COLUMN ths_moneyflow.buy_lg_amount IS '今日大单净流入额(万元)';
COMMENT ON COLUMN ths_moneyflow.buy_lg_amount_rate IS '今日大单净流入占比(%)';
COMMENT ON COLUMN ths_moneyflow.buy_md_amount IS '今日中单净流入额(万元)';
COMMENT ON COLUMN ths_moneyflow.buy_md_amount_rate IS '今日中单净流入占比(%)';
COMMENT ON COLUMN ths_moneyflow.buy_sm_amount IS '今日小单净流入额(万元)';
COMMENT ON COLUMN ths_moneyflow.buy_sm_amount_rate IS '今日小单净流入占比(%)';
COMMENT ON COLUMN ths_moneyflow.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_ths_moneyflow_code ON ths_moneyflow(ts_code);
CREATE INDEX IF NOT EXISTS idx_ths_moneyflow_date ON ths_moneyflow(trade_date);
