-- trade_calendar (交易日历)
-- API接口: trade_calendar
-- API字段数: 4


CREATE TABLE IF NOT EXISTS trade_calendar (
    exchange VARCHAR(20),  -- 交易所 SSE上交所 SZSE深交所
    cal_date DATE,  -- 日历日期
    is_open VARCHAR(100),  -- 是否交易 0休市 1交易
    pretrade_date DATE,  -- 上一个交易日
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键


-- 索引
CREATE INDEX IF NOT EXISTS idx_trade_calendar_date ON trade_calendar(cal_date);
CREATE INDEX IF NOT EXISTS idx_trade_calendar_exchange ON trade_calendar(exchange);
