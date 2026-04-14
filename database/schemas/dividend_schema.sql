-- dividend (分红送股数据)
-- API接口: dividend
-- API字段数: 16

CREATE TABLE IF NOT EXISTS dividend (
    ts_code VARCHAR(20),  -- TS代码
    end_date DATE,  -- 分红年度
    ann_date DATE,  -- 预案公告日
    div_proc VARCHAR(20),  -- 实施进度
    stk_div REAL,  -- 每股送转
    stk_bo_rate REAL,  -- 每股送股比例
    stk_co_rate REAL,  -- 每股转增比例
    cash_div REAL,  -- 每股分红（税后）
    cash_div_tax REAL,  -- 每股分红（税前）
    record_date DATE,  -- 股权登记日
    ex_date DATE,  -- 除权除息日
    pay_date DATE,  -- 派息日
    div_listdate VARCHAR(100),  -- 红股上市日
    imp_ann_date DATE,  -- 实施公告日
    base_date DATE,  -- 基准日
    base_share REAL,  -- 基准股本（万）
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    PRIMARY KEY (ts_code, end_date, ann_date)
);

COMMENT ON TABLE dividend IS '分红送股数据';

COMMENT ON COLUMN dividend.ts_code IS 'TS代码';
COMMENT ON COLUMN dividend.end_date IS '分红年度';
COMMENT ON COLUMN dividend.ann_date IS '预案公告日';
COMMENT ON COLUMN dividend.div_proc IS '实施进度';
COMMENT ON COLUMN dividend.stk_div IS '每股送转';
COMMENT ON COLUMN dividend.stk_bo_rate IS '每股送股比例';
COMMENT ON COLUMN dividend.stk_co_rate IS '每股转增比例';
COMMENT ON COLUMN dividend.cash_div IS '每股分红（税后）';
COMMENT ON COLUMN dividend.cash_div_tax IS '每股分红（税前）';
COMMENT ON COLUMN dividend.record_date IS '股权登记日';
COMMENT ON COLUMN dividend.ex_date IS '除权除息日';
COMMENT ON COLUMN dividend.pay_date IS '派息日';
COMMENT ON COLUMN dividend.div_listdate IS '红股上市日';
COMMENT ON COLUMN dividend.imp_ann_date IS '实施公告日';
COMMENT ON COLUMN dividend.base_date IS '基准日';
COMMENT ON COLUMN dividend.base_share IS '基准股本（万）';
COMMENT ON COLUMN dividend.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_dividend_code ON dividend(ts_code);
CREATE INDEX IF NOT EXISTS idx_dividend_end_date ON dividend(end_date);
CREATE INDEX IF NOT EXISTS idx_dividend_ann_date ON dividend(ann_date);
