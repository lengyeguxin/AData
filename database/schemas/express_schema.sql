-- express (业绩快报)
-- API接口: express
-- API字段数: 12


CREATE TABLE IF NOT EXISTS express (
    ts_code VARCHAR(20),  -- TS股票代码
    ann_date DATE,  -- 公告日期
    end_date DATE,  -- 报告期
    type VARCHAR(20),  -- 业绩预告类型(预增/预减/扭亏/首亏/续亏/续盈/略增/略减)
    p_change_min REAL,  -- 预告净利润变动幅度下限（%）
    p_change_max REAL,  -- 预告净利润变动幅度上限（%）
    net_profit_min REAL,  -- 预告净利润下限（万元）
    net_profit_max REAL,  -- 预告净利润上限（万元）
    last_parent_net REAL,  -- 上年同期归属母公司净利润
    first_ann_date DATE,  -- 首次公告日
    summary VARCHAR(100),  -- 业绩预告摘要
    change_reason VARCHAR(500),  -- 业绩变动原因
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE express ADD PRIMARY KEY (ts_code, end_date, ann_date);


-- 索引
CREATE INDEX IF NOT EXISTS idx_express_code ON express(ts_code);
CREATE INDEX IF NOT EXISTS idx_express_end_date ON express(end_date);
CREATE INDEX IF NOT EXISTS idx_express_ann_date ON express(ann_date);
