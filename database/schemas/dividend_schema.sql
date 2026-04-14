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
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE dividend ADD PRIMARY KEY (ts_code, end_date, ann_date);


-- 索引
CREATE INDEX IF NOT EXISTS idx_dividend_code ON dividend(ts_code);
CREATE INDEX IF NOT EXISTS idx_dividend_end_date ON dividend(end_date);
CREATE INDEX IF NOT EXISTS idx_dividend_ann_date ON dividend(ann_date);
