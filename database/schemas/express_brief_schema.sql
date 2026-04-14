-- express_brief (业绩快报摘要)
-- API接口: express_brief
-- API字段数: 32

CREATE TABLE IF NOT EXISTS express_brief (
    ts_code VARCHAR(20),  -- TS股票代码
    ann_date DATE,  -- 公告日期
    end_date DATE,  -- 报告期
    revenue REAL,  -- 营业收入(元)
    operate_profit REAL,  -- 营业利润(元)
    total_profit REAL,  -- 利润总额(元)
    n_income REAL,  -- 净利润(元)
    total_assets REAL,  -- 总资产(元)
    total_hldr_eqy_exc_min_int REAL,  -- 股东权益合计(不含少数股东权益)(元)
    diluted_eps REAL,  -- 每股收益(摊薄)(元)
    diluted_roe REAL,  -- 净资产收益率(摊薄)(%)
    yoy_net_profit REAL,  -- 去年同期修正后净利润
    bps REAL,  -- 每股净资产
    yoy_sales REAL,  -- 同比增长率:营业收入
    yoy_op REAL,  -- 同比增长率:营业利润
    yoy_tp REAL,  -- 同比增长率:利润总额
    yoy_dedu_np REAL,  -- 同比增长率:归属母公司股东的净利润
    yoy_eps REAL,  -- 同比增长率:基本每股收益
    yoy_roe REAL,  -- 同比增减:加权平均净资产收益率
    growth_assets REAL,  -- 比年初增长率:总资产
    yoy_equity REAL,  -- 比年初增长率:归属母公司的股东权益
    growth_bps REAL,  -- 比年初增长率:归属于母公司股东的每股净资产
    or_last_year REAL,  -- 去年同期营业收入
    op_last_year REAL,  -- 去年同期营业利润
    tp_last_year REAL,  -- 去年同期利润总额
    np_last_year REAL,  -- 去年同期净利润
    eps_last_year REAL,  -- 去年同期每股收益
    open_net_assets REAL,  -- 期初净资产
    open_bps REAL,  -- 期初每股净资产
    perf_summary VARCHAR(100),  -- 业绩简要说明
    is_audit VARCHAR(100),  -- 是否审计： 1是 0否
    remark VARCHAR(100),  -- 备注
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    PRIMARY KEY (ts_code, end_date, ann_date)
);

COMMENT ON TABLE express_brief IS '业绩快报摘要';

COMMENT ON COLUMN express_brief.ts_code IS 'TS股票代码';
COMMENT ON COLUMN express_brief.ann_date IS '公告日期';
COMMENT ON COLUMN express_brief.end_date IS '报告期';
COMMENT ON COLUMN express_brief.revenue IS '营业收入(元)';
COMMENT ON COLUMN express_brief.operate_profit IS '营业利润(元)';
COMMENT ON COLUMN express_brief.total_profit IS '利润总额(元)';
COMMENT ON COLUMN express_brief.n_income IS '净利润(元)';
COMMENT ON COLUMN express_brief.total_assets IS '总资产(元)';
COMMENT ON COLUMN express_brief.total_hldr_eqy_exc_min_int IS '股东权益合计(不含少数股东权益)(元)';
COMMENT ON COLUMN express_brief.diluted_eps IS '每股收益(摊薄)(元)';
COMMENT ON COLUMN express_brief.diluted_roe IS '净资产收益率(摊薄)(%)';
COMMENT ON COLUMN express_brief.yoy_net_profit IS '去年同期修正后净利润';
COMMENT ON COLUMN express_brief.bps IS '每股净资产';
COMMENT ON COLUMN express_brief.yoy_sales IS '同比增长率:营业收入';
COMMENT ON COLUMN express_brief.yoy_op IS '同比增长率:营业利润';
COMMENT ON COLUMN express_brief.yoy_tp IS '同比增长率:利润总额';
COMMENT ON COLUMN express_brief.yoy_dedu_np IS '同比增长率:归属母公司股东的净利润';
COMMENT ON COLUMN express_brief.yoy_eps IS '同比增长率:基本每股收益';
COMMENT ON COLUMN express_brief.yoy_roe IS '同比增减:加权平均净资产收益率';
COMMENT ON COLUMN express_brief.growth_assets IS '比年初增长率:总资产';
COMMENT ON COLUMN express_brief.yoy_equity IS '比年初增长率:归属母公司的股东权益';
COMMENT ON COLUMN express_brief.growth_bps IS '比年初增长率:归属于母公司股东的每股净资产';
COMMENT ON COLUMN express_brief.or_last_year IS '去年同期营业收入';
COMMENT ON COLUMN express_brief.op_last_year IS '去年同期营业利润';
COMMENT ON COLUMN express_brief.tp_last_year IS '去年同期利润总额';
COMMENT ON COLUMN express_brief.np_last_year IS '去年同期净利润';
COMMENT ON COLUMN express_brief.eps_last_year IS '去年同期每股收益';
COMMENT ON COLUMN express_brief.open_net_assets IS '期初净资产';
COMMENT ON COLUMN express_brief.open_bps IS '期初每股净资产';
COMMENT ON COLUMN express_brief.perf_summary IS '业绩简要说明';
COMMENT ON COLUMN express_brief.is_audit IS '是否审计： 1是 0否';
COMMENT ON COLUMN express_brief.remark IS '备注';
COMMENT ON COLUMN express_brief.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_express_brief_code ON express_brief(ts_code);
CREATE INDEX IF NOT EXISTS idx_express_brief_end_date ON express_brief(end_date);
CREATE INDEX IF NOT EXISTS idx_express_brief_ann_date ON express_brief(ann_date);
