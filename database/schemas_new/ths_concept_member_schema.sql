-- ths_concept_member (同花顺概念板块成分)
-- API接口: ths_member
-- 数据来源: Tushare API

COMMENT ON TABLE ths_concept_member IS '同花顺概念板块成分';

CREATE TABLE IF NOT EXISTS ths_concept_member (
    ts_code VARCHAR(10),  -- 概念代码
    con_code VARCHAR(10),  -- 成分股代码
    in_date DATE,  -- 纳入日期
    out_date DATE,  -- 剔除日期
    is_new VARCHAR(2),  -- 是否新纳入
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN ths_concept_member.ts_code IS '概念代码';
COMMENT ON COLUMN ths_concept_member.con_code IS '成分股代码';
COMMENT ON COLUMN ths_concept_member.in_date IS '纳入日期';
COMMENT ON COLUMN ths_concept_member.out_date IS '剔除日期';
COMMENT ON COLUMN ths_concept_member.is_new IS '是否新纳入';
COMMENT ON COLUMN ths_concept_member.updated_at IS '更新时间';

ALTER TABLE ths_concept_member ADD PRIMARY KEY (ts_code, con_code);

CREATE INDEX IF NOT EXISTS idx_ths_concept_member_ts_code ON ths_concept_member(ts_code);
CREATE INDEX IF NOT EXISTS idx_ths_concept_member_con_code ON ths_concept_member(con_code);
CREATE INDEX IF NOT EXISTS idx_ths_concept_member_in_date ON ths_concept_member(in_date);