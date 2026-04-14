-- ths_concept_member (同花顺概念板块成分)
-- API接口: ths_concept_member
-- API字段数: 7

CREATE TABLE IF NOT EXISTS ths_concept_member (
    ts_code VARCHAR(20),  -- 指数代码
    con_code VARCHAR(20),  -- 股票代码
    con_name VARCHAR(100),  -- 股票名称
    weight REAL,  -- 权重(暂无)
    in_date DATE,  -- 纳入日期(暂无)
    out_date DATE,  -- 剔除日期(暂无)
    is_new VARCHAR(100),  -- 是否最新Y是N否
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    PRIMARY KEY (ts_code, con_code)
);



-- 索引
CREATE INDEX IF NOT EXISTS idx_ths_concept_member_ts_code ON ths_concept_member(ts_code);
CREATE INDEX IF NOT EXISTS idx_ths_concept_member_con_code ON ths_concept_member(con_code);
