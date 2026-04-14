-- dividend (分红送股数据)
-- API接口: dividend
-- 数据来源: Tushare API

COMMENT ON TABLE dividend IS '分红送股数据';

CREATE TABLE IF NOT EXISTS dividend (
    ts_code VARCHAR(10),  -- TS代码
    ann_date DATE,  -- 公告日期
    end_date DATE,  -- 分红年度
    div_proc VARCHAR(20),  -- 实施进度
    stk_div REAL,  -- 送股比例
    stk_bo_rate REAL,  -- 送股比例
    stk_co_rate REAL,  -- 转增比例
    cash_div REAL,  -- 现金分红
    cash_div_tax REAL,  -- 扣税后现金分红
    record_date DATE,  -- 股权登记日
    ex_date DATE,  -- 除权除息日
    pay_date DATE,  -- 派息日
    stk_lim_date DATE,  -- 限售股上市日
    dilist_date DATE,  -- 退市日期
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN dividend.ts_code IS 'TS代码';
COMMENT ON COLUMN dividend.ann_date IS '公告日期';
COMMENT ON COLUMN dividend.end_date IS '分红年度';
COMMENT ON COLUMN dividend.div_proc IS '实施进度';
COMMENT ON COLUMN dividend.stk_div IS '送股比例';
COMMENT ON COLUMN dividend.stk_bo_rate IS '送股比例';
COMMENT ON COLUMN dividend.stk_co_rate IS '转增比例';
COMMENT ON COLUMN dividend.cash_div IS '现金分红';
COMMENT ON COLUMN dividend.cash_div_tax IS '扣税后现金分红';
COMMENT ON COLUMN dividend.record_date IS '股权登记日';
COMMENT ON COLUMN dividend.ex_date IS '除权除息日';
COMMENT ON COLUMN dividend.pay_date IS '派息日';
COMMENT ON COLUMN dividend.stk_lim_date IS '限售股上市日';
COMMENT ON COLUMN dividend.dilist_date IS '退市日期';
COMMENT ON COLUMN dividend.updated_at IS '更新时间';

ALTER TABLE dividend ADD PRIMARY KEY (ts_code, end_date, ann_date);

CREATE INDEX IF NOT EXISTS idx_dividend_code ON dividend(ts_code);
CREATE INDEX IF NOT EXISTS idx_dividend_end_date ON dividend(end_date);
CREATE INDEX IF NOT EXISTS idx_dividend_ann_date ON dividend(ann_date);