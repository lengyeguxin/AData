-- hots_user (游资账户)
-- API接口: hots_user
-- API字段数: 3

CREATE TABLE IF NOT EXISTS hots_user (
    name VARCHAR(100) PRIMARY KEY,  -- 游资名称
    "desc" VARCHAR(100),  -- 说明
    orgs VARCHAR(100),  -- 关联机构
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON TABLE hots_user IS '游资账户';

COMMENT ON COLUMN hots_user.name IS '游资名称';
COMMENT ON COLUMN hots_user."desc" IS '说明';
COMMENT ON COLUMN hots_user.orgs IS '关联机构';
COMMENT ON COLUMN hots_user.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_hots_user_name ON hots_user(name);
CREATE INDEX IF NOT EXISTS idx_hots_user_orgs ON hots_user(orgs);
