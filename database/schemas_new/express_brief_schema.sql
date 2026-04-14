-- express_brief (业绩快报摘要)
-- API接口: express_brief
-- 数据来源: Tushare API

COMMENT ON TABLE express_brief IS '业绩快报摘要';

CREATE TABLE IF NOT EXISTS express_brief (
    ts_code VARCHAR(10),  -- TS代码
    ann_date DATE,  -- 公告日期
    end_date DATE,  -- 报告期
    report_type VARCHAR(10),  -- 报告类型
    comp_type VARCHAR(10),  -- 公司类型
    revenue REAL,  -- 营业收入
    operate_profit REAL,  -- 营业利润
    total_profit REAL,  -- 利润总额
    n_income REAL,  -- 净利润
    total_assets REAL,  -- 总资产
    total_hldr_eqy_exc_min_int REAL,  -- 所有者权益合计
    basic_eps REAL,  -- 基本每股收益
    bps REAL,  -- 每股净资产
    yoy_sales REAL,  -- 营业收入同比增长
    yoy_op REAL,  -- 营业利润同比增长
    yoy_tp REAL,  -- 利润总额同比增长
    yoy_np REAL,  -- 净利润同比增长
    yoy_eps REAL,  -- 每股收益同比增长
    yoy_ta REAL,  -- 总资产同比增长
    yoy_hldr_eqy REAL,  -- 所有者权益同比增长
    qoq_sales REAL,  -- 营业收入环比增长
    qoq_op REAL,  -- 营业利润环比增长
    qoq_tp REAL,  -- 利润总额环比增长
    qoq_np REAL,  -- 净利润环比增长
    qoq_eps REAL,  -- 每股收益环比增长
    qoq_ta REAL,  -- 总资产环比增长
    qoq_hldr_eqy REAL,  -- 所有者权益环比增长
    update_flag VARCHAR(10),  -- 更新标识
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN express_brief.ts_code IS 'TS代码';
COMMENT ON COLUMN express_brief.ann_date IS '公告日期';
COMMENT ON COLUMN express_brief.end_date IS '报告期';
COMMENT ON COLUMN express_brief.report_type IS '报告类型';
COMMENT ON COLUMN express_brief.comp_type IS '公司类型';
COMMENT ON COLUMN express_brief.revenue IS '营业收入';
COMMENT ON COLUMN express_brief.operate_profit IS '营业利润';
COMMENT ON COLUMN express_brief.total_profit IS '利润总额';
COMMENT ON COLUMN express_brief.n_income IS '净利润';
COMMENT ON COLUMN express_brief.total_assets IS '总资产';
COMMENT ON COLUMN express_brief.total_hldr_eqy_exc_min_int IS '所有者权益合计';
COMMENT ON COLUMN express_brief.basic_eps IS '基本每股收益';
COMMENT ON COLUMN express_brief.bps IS '每股净资产';
COMMENT ON COLUMN express_brief.yoy_sales IS '营业收入同比增长';
COMMENT ON COLUMN express_brief.yoy_op IS '营业利润同比增长';
COMMENT ON COLUMN express_brief.yoy_tp IS '利润总额同比增长';
COMMENT ON COLUMN express_brief.yoy_np IS '净利润同比增长';
COMMENT ON COLUMN express_brief.yoy_eps IS '每股收益同比增长';
COMMENT ON COLUMN express_brief.yoy_ta IS '总资产同比增长';
COMMENT ON COLUMN express_brief.yoy_hldr_eqy IS '所有者权益同比增长';
COMMENT ON COLUMN express_brief.qoq_sales IS '营业收入环比增长';
COMMENT ON COLUMN express_brief.qoq_op IS '营业利润环比增长';
COMMENT ON COLUMN express_brief.qoq_tp IS '利润总额环比增长';
COMMENT ON COLUMN express_brief.qoq_np IS '净利润环比增长';
COMMENT ON COLUMN express_brief.qoq_eps IS '每股收益环比增长';
COMMENT ON COLUMN express_brief.qoq_ta IS '总资产环比增长';
COMMENT ON COLUMN express_brief.qoq_hldr_eqy IS '所有者权益环比增长';
COMMENT ON COLUMN express_brief.update_flag IS '更新标识';
COMMENT ON COLUMN express_brief.updated_at IS '更新时间';

ALTER TABLE express_brief ADD PRIMARY KEY (ts_code, end_date, ann_date);

CREATE INDEX IF NOT EXISTS idx_express_brief_code ON express_brief(ts_code);
CREATE INDEX IF NOT EXISTS idx_express_brief_end_date ON express_brief(end_date);
CREATE INDEX IF NOT EXISTS idx_express_brief_ann_date ON express_brief(ann_date);