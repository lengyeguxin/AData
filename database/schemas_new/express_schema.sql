-- express (业绩快报)
-- API接口: express
-- 数据来源: Tushare API

COMMENT ON TABLE express IS '业绩快报';

CREATE TABLE IF NOT EXISTS express (
    ts_code VARCHAR(10),  -- TS代码
    ann_date DATE,  -- 公告日期
    f_ann_date DATE,  -- 实际公告日期
    end_date DATE,  -- 报告期
    report_type VARCHAR(10),  -- 报告类型
    comp_type VARCHAR(10),  -- 公司类型
    end_type VARCHAR(10),  -- 报告期类型
    total_revenue REAL,  -- 营业总收入
    revenue REAL,  -- 营业收入
    operate_profit REAL,  -- 营业利润
    total_profit REAL,  -- 利润总额
    n_income REAL,  -- 几利润
    n_income_attr_p REAL,  -- 归属母公司所有者的净利润
    basic_eps REAL,  -- 基本每股收益
    diluted_eps REAL,  -- 稀释每股收益
    yoy_sales REAL,  -- 营业收入同比增长
    yoy_dedu_np REAL,  -- 扣非净利润同比增长
    yoy_eps REAL,  -- 每股收益同比增长
    yoy_op REAL,  -- 营业利润同比增长
    yoy_tp REAL,  -- 利润总额同比增长
    yoy_np REAL,  -- 净利润同比增长
    yoy_np_cut REAL,  -- 扣非净利润同比增长
    qoq_sales REAL,  -- 营业收入环比增长
    qoq_dedu_np REAL,  -- 扣非净利润环比增长
    qoq_eps REAL,  -- 每股收益环比增长
    qoq_op REAL,  -- 营业利润环比增长
    qoq_tp REAL,  -- 利润总额环比增长
    qoq_np REAL,  -- 净利润环比增长
    qoq_np_cut REAL,  -- 扣非净利润环比增长
    n_income_cut REAL,  -- 扣除非经常性损益后的净利润
    update_flag VARCHAR(10),  -- 更新标识
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN express.ts_code IS 'TS代码';
COMMENT ON COLUMN express.ann_date IS '公告日期';
COMMENT ON COLUMN express.f_ann_date IS '实际公告日期';
COMMENT ON COLUMN express.end_date IS '报告期';
COMMENT ON COLUMN express.report_type IS '报告类型';
COMMENT ON COLUMN express.comp_type IS '公司类型';
COMMENT ON COLUMN express.end_type IS '报告期类型';
COMMENT ON COLUMN express.total_revenue IS '营业总收入';
COMMENT ON COLUMN express.revenue IS '营业收入';
COMMENT ON COLUMN express.operate_profit IS '营业利润';
COMMENT ON COLUMN express.total_profit IS '利润总额';
COMMENT ON COLUMN express.n_income IS '净利润';
COMMENT ON COLUMN express.n_income_attr_p IS '归属母公司所有者的净利润';
COMMENT ON COLUMN express.basic_eps IS '基本每股收益';
COMMENT ON COLUMN express.diluted_eps IS '稀释每股收益';
COMMENT ON COLUMN express.yoy_sales IS '营业收入同比增长';
COMMENT ON COLUMN express.yoy_dedu_np IS '扣非净利润同比增长';
COMMENT ON COLUMN express.yoy_eps IS '每股收益同比增长';
COMMENT ON COLUMN express.yoy_op IS '营业利润同比增长';
COMMENT ON COLUMN express.yoy_tp IS '利润总额同比增长';
COMMENT ON COLUMN express.yoy_np IS '净利润同比增长';
COMMENT ON COLUMN express.yoy_np_cut IS '扣非净利润同比增长';
COMMENT ON COLUMN express.qoq_sales IS '营业收入环比增长';
COMMENT ON COLUMN express.qoq_dedu_np IS '扣非净利润环比增长';
COMMENT ON COLUMN express.qoq_eps IS '每股收益环比增长';
COMMENT ON COLUMN express.qoq_op IS '营业利润环比增长';
COMMENT ON COLUMN express.qoq_tp IS '利润总额环比增长';
COMMENT ON COLUMN express.qoq_np IS '净利润环比增长';
COMMENT ON COLUMN express.qoq_np_cut IS '扣非净利润环比增长';
COMMENT ON COLUMN express.n_income_cut IS '扣除非经常性损益后的净利润';
COMMENT ON COLUMN express.update_flag IS '更新标识';
COMMENT ON COLUMN express.updated_at IS '更新时间';

ALTER TABLE express ADD PRIMARY KEY (ts_code, end_date, ann_date);

CREATE INDEX IF NOT EXISTS idx_express_code ON express(ts_code);
CREATE INDEX IF NOT EXISTS idx_express_end_date ON express(end_date);
CREATE INDEX IF NOT EXISTS idx_express_ann_date ON express(ann_date);