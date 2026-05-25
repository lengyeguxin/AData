-- hots_user (游资账户)
-- API接口: hots_user
-- API字段数: 3

CREATE TABLE IF NOT EXISTS hots_user (
    name VARCHAR(100) PRIMARY KEY,  -- 游资名称
    description TEXT,  -- 说明（原desc列，desc是DuckDB保留关键字）
    orgs TEXT,  -- 关联机构
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 表注释
COMMENT ON TABLE hots_user IS '游资账户信息表 - 记录热门游资账户的基本信息';

-- 字段注释
COMMENT ON COLUMN hots_user.name IS '游资名称 - 游资账户的唯一标识';
COMMENT ON COLUMN hots_user.description IS '游资说明 - 对游资账户的详细描述信息';
COMMENT ON COLUMN hots_user.orgs IS '关联机构 - 与游资账户关联的机构列表';
COMMENT ON COLUMN hots_user.updated_at IS '更新时间 - 记录的最后更新时间';



-- 索引
