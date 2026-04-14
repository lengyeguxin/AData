-- hots_user (游资账户)
-- API接口: hots_user
-- API字段数: 3


CREATE TABLE IF NOT EXISTS hots_user (
    name VARCHAR(100),  -- 游资名称
    desc VARCHAR(100),  -- 说明
    orgs VARCHAR(100),  -- 关联机构
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);


-- 索引
CREATE INDEX IF NOT EXISTS idx_hots_user_account ON hots_user(account);
CREATE INDEX IF NOT EXISTS idx_hots_user_broker_name ON hots_user(broker_name);
