-- 1. fina_indicator（财务指标）
-- 完整字段定义（对照Tushare官方文档：https://tushare.pro/document/2?doc_id=79）
CREATE TABLE IF NOT EXISTS fina_indicator (
    ts_code VARCHAR(10),
    ann_date DATE,
    end_date DATE,

    -- 每股指标
    eps REAL,                    -- 每股收益
    dt_eps REAL,                 -- 每股收益(扣非)
    total_revenue_ps REAL,       -- 每股营业总收入
    revenue_ps REAL,             -- 每股营业收入
    capital_rese_ps REAL,        -- 每股资本公积
    surplus_rese_ps REAL,        -- 每股盈余公积
    undist_profit_ps REAL,       -- 每股未分配利润
    diluted2_eps REAL,           -- 每股收益(稀释2)
    bps REAL,                    -- 每股净资产
    ocfps REAL,                  -- 每股经营现金流
    retainedps REAL,             -- 每股留存收益
    cfps REAL,                   -- 每股现金流
    ebit_ps REAL,                -- 每股EBIT
    fcff_ps REAL,                -- 每股企业自由现金流
    fcfe_ps REAL,                -- 每股股东自由现金流

    -- 盈利能力指标
    roe REAL,                    -- 净资产收益率
    roe_waa REAL,                -- 加权平均净资产收益率
    roe_dt REAL,                 -- 净资产收益率(扣非)
    roa REAL,                    -- 总资产报酬率
    npta REAL,                   -- 总资产净利润
    roic REAL,                   -- 投入资本回报率
    roe_yearly REAL,             -- 净资产收益率(年化)
    roa2_yearly REAL,            -- 总资产报酬率2(年化)
    roe_avg REAL,                -- 平均净资产收益率
    roa_yearly REAL,             -- 总资产净利润(年化)
    roa_dp REAL,                 -- 总资产净利润(双季)
    roic_yearly REAL,            -- 投入资本回报率(年化)

    -- 营运能力指标
    invturn_days REAL,           -- 存货周转天数
    arturn_days REAL,            -- 应收账款周转天数
    inv_turn REAL,               -- 存货周转率
    ar_turn REAL,                -- 应收账款周转率
    ca_turn REAL,                -- 流动资产周转率
    fa_turn REAL,                -- 固定资产周转率
    assets_turn REAL,            -- 总资产周转率
    turn_days REAL,              -- 营业周期
    total_fa_trun REAL,          -- 固定资产周转率(TTM)

    -- 偿债能力指标
    current_ratio REAL,          -- 流动比率
    quick_ratio REAL,            -- 速动比率
    cash_ratio REAL,             -- 现金比率
    debt_to_assets REAL,         -- 资产负债率
    assets_to_eqt REAL,          -- 权益乘数
    dp_assets_to_eqt REAL,       -- 权益乘数(双季)
    debt_to_eqt REAL,            -- 产权比率
    eqt_to_debt REAL,            -- 产权比率倒数

    -- 现金流指标
    fcff REAL,                   -- 企业自由现金流
    fcfe REAL,                   -- 股东自由现金流
    ocf_to_debt REAL,            -- 现金债务覆盖率
    ocf_to_interestdebt REAL,    -- 现金利息债务覆盖率
    ocf_to_netdebt REAL,         -- 现金净债务覆盖率
    ocf_to_shortdebt REAL,       -- 现金短期债务覆盖率

    -- 其他重要指标
    gross_margin REAL,           -- 毛利率
    ebit REAL,                   -- 息税前利润
    ebitda REAL,                 -- 息税折旧摊销前利润
    profit_dedt REAL,            -- 扣除非经常损益后的净利润
    working_capital REAL,        -- 营运资本
    networking_capital REAL,     -- 净营运资本
    invest_capital REAL,         -- 投入资本
    retained_earnings REAL,      -- 留存收益
    tangible_asset REAL,         -- 有形资产
    interestdebt REAL,           -- 利息债务
    netdebt REAL,                -- 净债务
    fixed_assets REAL,           -- 固定资产

    -- 同比增长指标
    basic_eps_yoy REAL,          -- 基本每股收益同比增长
    dt_eps_yoy REAL,             -- 扣非每股收益同比增长
    cfps_yoy REAL,               -- 每股现金流同比增长
    op_yoy REAL,                 -- 营业利润同比增长
    ebt_yoy REAL,                -- 利润总额同比增长
    netprofit_yoy REAL,          -- 净利润同比增长
    dt_netprofit_yoy REAL,       -- 扣非净利润同比增长
    ocf_yoy REAL,                -- 经营现金流同比增长
    roe_yoy REAL,                -- 净资产收益率同比增长
    bps_yoy REAL,                -- 每股净资产同比增长
    assets_yoy REAL,             -- 总资产同比增长
    eqt_yoy REAL,                -- 净资产同比增长
    tr_yoy REAL,                 -- 营业总收入同比增长
    or_yoy REAL,                 -- 营业收入同比增长
    equity_yoy REAL,             -- 股东权益同比增长

    -- 单季度指标(q_开头)
    q_opincome REAL,             -- 单季度营业利润
    q_investincome REAL,         -- 单季度投资收益
    q_dtprofit REAL,             -- 单季度扣非净利润
    q_eps REAL,                  -- 单季度每股收益
    q_netprofit_margin REAL,     -- 单季度净利润率
    q_gsprofit_margin REAL,      -- 单季度毛利率
    q_roe REAL,                  -- 单季度ROE
    q_dt_roe REAL,               -- 单季度扣非ROE
    q_opprofit_margin REAL,      -- 单季度营业利润率
    q_ebit_margin REAL,          -- 单季度EBIT利润率
    q_ebitda_margin REAL,        -- 单季度EBITDA利润率
    q_opincome_yoy REAL,         -- 单季度营业利润同比增长
    q_investincome_yoy REAL,     -- 单季度投资收益同比增长
    q_dtprofit_yoy REAL,         -- 单季度扣非净利润同比增长
    q_eps_yoy REAL,              -- 单季度每股收益同比增长
    q_netprofit_yoy REAL,        -- 单季度净利润同比增长

    -- 其他
    rd_exp REAL,                 -- 研发费用
    update_flag VARCHAR(10),     -- 更新标识

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, end_date)
);

CREATE INDEX IF NOT EXISTS idx_fina_date ON fina_indicator(ann_date);
CREATE INDEX IF NOT EXISTS idx_fina_code ON fina_indicator(ts_code);
CREATE INDEX IF NOT EXISTS idx_fina_end_date ON fina_indicator(end_date);