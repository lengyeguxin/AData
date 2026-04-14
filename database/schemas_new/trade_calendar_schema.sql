-- trade_calendar (交易日历)
-- API接口: trade_cal
-- API字段数: 4

COMMENT ON TABLE trade_calendar IS '交易日历';

CREATE TABLE IF NOT EXISTS trade_calendar (
    exchange REAL,  -- 交易所
    cal_date DATE,  -- cal_date
    is_open REAL,  -- 是否交易
    pretrade_date DATE,  -- 上一交易日
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE trade_calendar ADD PRIMARY KEY (exchange, cal_date);

COMMENT ON COLUMN trade_calendar.exchange IS '交易所';
COMMENT ON COLUMN trade_calendar.is_open IS '是否交易';
COMMENT ON COLUMN trade_calendar.pretrade_date IS '上一交易日';

-- 索引
CREATE INDEX IF NOT EXISTS idx_trade_calendar_date ON trade_calendar(cal_date);
CREATE INDEX IF NOT EXISTS idx_trade_calendar_exchange ON trade_calendar(exchange);
