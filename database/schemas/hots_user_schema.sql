-- hots_user (游资账户)
-- API接口: hots_user
-- API字段数: 3


CREATE TABLE IF NOT EXISTS hots_user (
    name VARCHAR(100),  -- 游资名称
    description VARCHAR(100),  -- 说明（原desc列，desc是DuckDB保留关键字）
    orgs VARCHAR(100),  -- 关联机构
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);


-- 索引
