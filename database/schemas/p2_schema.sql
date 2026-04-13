-- P2财务表（共7张）
-- 按自然日每日拉取，游标记录公告日期（ann_date）
-- 使用VIP接口（fina_indicator_vip、income_vip、balancesheet_vip、cashflow_vip、forecast_vip、express_vip）

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

-- 2. income（利润表）
CREATE TABLE IF NOT EXISTS income (
    ts_code VARCHAR(10),
    ann_date DATE,
    f_ann_date DATE,
    end_date DATE,
    report_type VARCHAR(10),
    comp_type VARCHAR(10),
    end_type VARCHAR(10),         -- 报告期类型
    update_flag VARCHAR(10),      -- 更新标识

    -- 营业收入与成本
    total_revenue REAL,
    revenue REAL,
    operate_profit REAL,
    total_cogs REAL,
    interest_income REAL,

    -- 利润指标
    profit_dedt REAL,
    sell_exp REAL,
    admin_exp REAL,
    fin_exp REAL,
    asset_impair_loss REAL,
    non_oper_income REAL,
    non_oper_exp REAL,
    total_profit REAL,
    income_tax REAL,
    n_income REAL,
    n_income_attr_p REAL,
    minority_gain REAL,

    -- 每股指标
    basic_eps REAL,
    diluted_eps REAL,

    -- 其他综合收益
    oth_compr_income REAL,
    t_compr_income REAL,
    compr_inc_attr_p REAL,
    compr_inc_attr_m_s REAL,

    -- 现金流相关
    ebit REAL,
    ebitda REAL,
    rd_exp REAL,
    fin_exp_int_exp REAL,
    fin_exp_int_income REAL,
    transfer_surplus_reserve REAL,
    transfer_risk_reserve REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, end_date, report_type)
);

CREATE INDEX IF NOT EXISTS idx_income_date ON income(end_date);
CREATE INDEX IF NOT EXISTS idx_income_code ON income(ts_code);
CREATE INDEX IF NOT EXISTS idx_income_ann_date ON income(ann_date);

-- 3. balancesheet（资产负债表）
CREATE TABLE IF NOT EXISTS balancesheet (
    ts_code VARCHAR(10),
    ann_date DATE,
    f_ann_date DATE,
    end_date DATE,
    report_type VARCHAR(10),
    comp_type VARCHAR(10),
    end_type VARCHAR(10),         -- 报告期类型
    update_flag VARCHAR(10),      -- 更新标识

    -- 流动资产
    total_cur_assets REAL,
    money_cap REAL,
    trad_asset REAL,
    notes_receiv REAL,
    accounts_receiv REAL,
    adv_payment REAL,
    other_receiv REAL,
    inventories REAL,
    amor_exp REAL,
    long_ampay_dep_rec_asim REAL,

    -- 非流动资产
    total_nca REAL,
    fix_assets REAL,
    cip REAL,
    const_materials REAL,
    intang_assets REAL,
    goodwill REAL,
    long_deferred_exp REAL,
    defer_tax_assets REAL,

    -- 资产总计
    total_assets REAL,

    -- 流动负债
    total_cur_liab REAL,
    st_borr REAL,
    notes_payable REAL,
    accounts_pay REAL,
    adv_receipts REAL,
    payroll_pay REAL,
    taxes_payable REAL,
    interest_payable REAL,
    div_payable REAL,
    other_payable REAL,

    -- 非流动负债
    total_ncl REAL,
    long_borr REAL,
    bonds_payable REAL,
    long_deferred_rev REAL,
    defer_tax_liab REAL,

    -- 负债合计
    total_liab REAL,

    -- 股东权益
    cap_rese REAL,
    undistr_porfit REAL,
    minority_int_ratio REAL,
    total_hldr_eqy_exc_min_int REAL,
    total_hldr_eqy_inc_min_int REAL,
    total_liab_hldr_eqy REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, end_date, report_type)
);

CREATE INDEX IF NOT EXISTS idx_balance_date ON balancesheet(end_date);
CREATE INDEX IF NOT EXISTS idx_balance_code ON balancesheet(ts_code);
CREATE INDEX IF NOT EXISTS idx_balance_ann_date ON balancesheet(ann_date);

-- 4. cashflow（现金流量表）
CREATE TABLE IF NOT EXISTS cashflow (
    ts_code VARCHAR(10),
    ann_date DATE,
    f_ann_date DATE,
    end_date DATE,
    report_type VARCHAR(10),
    comp_type VARCHAR(10),
    end_type VARCHAR(10),         -- 报告期类型
    update_flag VARCHAR(10),      -- 更新标识

    -- 经营活动现金流
    n_cashflow_act REAL,
    cash_recp_sg_and_rs REAL,
    recp_tax_rends REAL,
    cash_pay_for_tax REAL,
    cash_pay_acq_const_fi REAL,
    cash_pay_for_depos REAL,
    cash_recp_loan_rel_fi REAL,
    free_cashflow REAL,

    -- 投资活动现金流
    n_cash_flows_inv_act REAL,
    c_fr_sale_sg REAL,
    c_fr_for_sale REAL,
    c_fr_disp_withdrw_invest REAL,
    c_recp_return_invest REAL,
    c_recp_loan_rel_fi REAL,
    c_fr_oth_inv_act REAL,
    n_cashflow_inv_act REAL,
    c_pay_for_acq_fi REAL,
    c_pay_for_invest REAL,
    c_pay_oth_inv_act REAL,

    -- 筹资活动现金流
    n_cash_flows_fnc_act REAL,
    c_fr_cap_contr REAL,
    c_fr_borrow REAL,
    c_fr_oth_fnc_act REAL,
    n_cashflow_fnc_act REAL,
    c_pay_for_dist_dpcp_int_exp REAL,
    c_pay_for_loan_rel_fi REAL,
    c_pay_oth_fnc_act REAL,

    -- 其他
    n_incr_cash_cash_equ REAL,
    effect_forex_cash REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, end_date, report_type)
);

CREATE INDEX IF NOT EXISTS idx_cashflow_date ON cashflow(end_date);
CREATE INDEX IF NOT EXISTS idx_cashflow_code ON cashflow(ts_code);
CREATE INDEX IF NOT EXISTS idx_cashflow_ann_date ON cashflow(ann_date);

-- 5. express（业绩预告）
CREATE TABLE IF NOT EXISTS express (
    ts_code VARCHAR(10),
    ann_date DATE,
    end_date DATE,
    report_type VARCHAR(10),
    comp_type VARCHAR(10),
    end_type VARCHAR(10),         -- 报告期类型
    update_flag VARCHAR(10),      -- 更新标识

    -- 业绩预告类型
    type VARCHAR(20),

    -- 业绩预告摘要
    summary VARCHAR(500),

    -- 预测指标
    n_income_min REAL,
    n_income_max REAL,
    n_income_min_last REAL,
    n_income_max_last REAL,

    -- 变动幅度
    p_change_min REAL,
    p_change_max REAL,
    p_change_min_last REAL,
    p_change_max_last REAL,

    -- 上年同期
    n_income_last REAL,
    p_change_last REAL,

    -- 业绩变动原因
    change_reason VARCHAR(1000),

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, end_date, ann_date)
);

CREATE INDEX IF NOT EXISTS idx_express_date ON express(end_date);
CREATE INDEX IF NOT EXISTS idx_express_code ON express(ts_code);
CREATE INDEX IF NOT EXISTS idx_express_ann_date ON express(ann_date);

-- 6. express_brief（业绩快报）
CREATE TABLE IF NOT EXISTS express_brief (
    ts_code VARCHAR(10),
    ann_date DATE,
    end_date DATE,
    report_type VARCHAR(10),
    comp_type VARCHAR(10),
    end_type VARCHAR(10),         -- 报告期类型
    update_flag VARCHAR(10),      -- 更新标识

    -- 营业收入
    total_revenue REAL,
    revenue REAL,

    -- 营业利润
    operate_profit REAL,
    total_profit REAL,

    -- 净利润
    n_income REAL,
    n_income_attr_p REAL,

    -- 每股指标
    basic_eps REAL,
    diluted_eps REAL,

    -- 扣除非经常性损益后的净利润
    n_income_cut REAL,

    -- 同比增长
    yoy_sales REAL,
    yoy_dedu_np REAL,
    yoy_eps REAL,
    yoy_op REAL,
    yoy_tp REAL,
    yoy_np REAL,
    yoy_np_cut REAL,

    -- 环比增长
    qoq_sales REAL,
    qoq_dedu_np REAL,
    qoq_eps REAL,
    qoq_op REAL,
    qoq_tp REAL,
    qoq_np REAL,
    qoq_np_cut REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, end_date, ann_date)
);

CREATE INDEX IF NOT EXISTS idx_express_brief_date ON express_brief(end_date);
CREATE INDEX IF NOT EXISTS idx_express_brief_code ON express_brief(ts_code);
CREATE INDEX IF NOT EXISTS idx_express_brief_ann_date ON express_brief(ann_date);

-- 7. dividend（分红送股）
CREATE TABLE IF NOT EXISTS dividend (
    ts_code VARCHAR(10),
    ann_date DATE,
    record_date DATE,
    ex_date DATE,
    pay_date DATE,
    div_proc VARCHAR(20),
    stk_div REAL,
    stk_bo_rate REAL,
    stk_co_rate REAL,
    cash_div REAL,
    cash_div_tax REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, ann_date, record_date)
);

CREATE INDEX IF NOT EXISTS idx_dividend_date ON dividend(ann_date);
CREATE INDEX IF NOT EXISTS idx_dividend_code ON dividend(ts_code);


-- P3资金流向(THS)表（共3张）
-- 按交易日每日拉取，使用同花顺数据接口

-- 8. ths_moneyflow（个股资金流向）
CREATE TABLE IF NOT EXISTS ths_moneyflow (
    ts_code VARCHAR(10),
    trade_date DATE,
    name VARCHAR(50),
    pct_change REAL,
    latest REAL,
    net_amount REAL,
    net_d5_amount REAL,
    buy_lg_amount REAL,
    buy_lg_amount_rate REAL,
    buy_md_amount REAL,
    buy_md_amount_rate REAL,
    buy_sm_amount REAL,
    buy_sm_amount_rate REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_ths_moneyflow_date ON ths_moneyflow(trade_date);
CREATE INDEX IF NOT EXISTS idx_ths_moneyflow_code ON ths_moneyflow(ts_code);

-- 9. ths_concept_moneyflow（同花顺概念板块资金流向）
CREATE TABLE IF NOT EXISTS ths_concept_moneyflow (
    ts_code VARCHAR(10),
    trade_date DATE,
    name VARCHAR(50),
    lead_stock VARCHAR(50),
    close_price REAL,
    pct_change REAL,
    industry_index REAL,
    company_num INTEGER,
    pct_change_stock REAL,
    net_buy_amount REAL,
    net_sell_amount REAL,
    net_amount REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_ths_concept_moneyflow_date ON ths_concept_moneyflow(trade_date);
CREATE INDEX IF NOT EXISTS idx_ths_concept_moneyflow_code ON ths_concept_moneyflow(ts_code);

-- 10. ths_industry_moneyflow（同花顺行业资金流向）
CREATE TABLE IF NOT EXISTS ths_industry_moneyflow (
    ts_code VARCHAR(10),
    trade_date DATE,
    industry VARCHAR(50),
    lead_stock VARCHAR(50),
    close REAL,
    pct_change REAL,
    company_num INTEGER,
    pct_change_stock REAL,
    close_price REAL,
    net_buy_amount REAL,
    net_sell_amount REAL,
    net_amount REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_ths_industry_moneyflow_date ON ths_industry_moneyflow(trade_date);
CREATE INDEX IF NOT EXISTS idx_ths_industry_moneyflow_code ON ths_industry_moneyflow(ts_code);


-- P3概念板块表（共2张）
-- 特殊游标策略（遍历指数列表）

-- 11. ths_concept_member（同花顺概念板块成分）
CREATE TABLE IF NOT EXISTS ths_concept_member (
    ts_code VARCHAR(10),        -- 概念代码
    con_code VARCHAR(10),       -- 成分股代码
    in_date DATE,
    out_date DATE,
    is_new VARCHAR(2),

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, con_code)
);

CREATE INDEX IF NOT EXISTS idx_ths_concept_member_code ON ths_concept_member(con_code);
CREATE INDEX IF NOT EXISTS idx_ths_concept_member_ts_code ON ths_concept_member(ts_code);

-- 12. ths_index_daily（同花顺概念和行业指数日线）
CREATE TABLE IF NOT EXISTS ths_index_daily (
    ts_code VARCHAR(10),
    trade_date DATE,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    vol REAL,
    amount REAL,
    pct_chg REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_ths_index_daily_date ON ths_index_daily(trade_date);
CREATE INDEX IF NOT EXISTS idx_ths_index_daily_code ON ths_index_daily(ts_code);


-- P4游资表（共2张）
-- hots_user：无游标，全量拉取
-- hots_trader_detail：按交易日拉取

-- 13. hots_user（游资账户）
CREATE TABLE IF NOT EXISTS hots_user (
    account VARCHAR(50) PRIMARY KEY,
    trader_name VARCHAR(100),
    broker_name VARCHAR(100),
    license VARCHAR(20),
    reg_date DATE,
    status VARCHAR(10),

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_hots_user_account ON hots_user(account);
CREATE INDEX IF NOT EXISTS idx_hots_user_broker ON hots_user(broker_name);

-- 14. hots_trader_detail（游资交易）
CREATE TABLE IF NOT EXISTS hots_trader_detail (
    account VARCHAR(50),
    ts_code VARCHAR(10),
    trade_date DATE,
    buy_amount REAL,
    sell_amount REAL,
    net_amount REAL,
    buy_vol REAL,
    sell_vol REAL,
    net_vol REAL,
    reason VARCHAR(500),

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (account, ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_date ON hots_trader_detail(trade_date);
CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_code ON hots_trader_detail(ts_code);
CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_account ON hots_trader_detail(account);