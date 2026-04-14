-- hots_user (游资账户)
-- API接口: hots_user
-- 数据来源: Tushare API

COMMENT ON TABLE hots_user IS '游资账户';

CREATE TABLE IF NOT EXISTS hots_user (
    account VARCHAR(50),  -- 账户
    trader_name VARCHAR(100),  -- 游资名称
    broker_name VARCHAR(100),  -- 券商名称
    license VARCHAR(20),  -- 许可证
    reg_date DATE,  -- 注册日期
    status VARCHAR(10),  -- 状态
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

COMMENT ON COLUMN hots_user.account IS '账户';
COMMENT ON COLUMN hots_user.trader_name IS '游资名称';
COMMENT ON COLUMN hots_user.broker_name IS '券商名称';
COMMENT ON COLUMN hots_user.license IS '许可证';
COMMENT ON COLUMN hots_user.reg_date IS '注册日期';
COMMENT ON COLUMN hots_user.status IS '状态';
COMMENT ON COLUMN hots_user.updated_at IS '更新时间';

ALTER TABLE hots_user ADD PRIMARY KEY (account);

CREATE INDEX IF NOT EXISTS idx_hots_user_account ON hots_user(account);
CREATE INDEX IF NOT EXISTS idx_hots_user_broker_name ON hots_user(broker_name);
CREATE INDEX IF NOT EXISTS idx_hots_user_trader_name ON hots_user(trader_name);