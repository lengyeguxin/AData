-- P2财务表（共7张）
-- 按自然日每日拉取，游标记录公告日期（ann_date）
-- 使用VIP接口（fina_indicator_vip、income_vip、balancesheet_vip、cashflow_vip、forecast_vip、express_vip）

-- 1. fina_indicator（财务指标）
-- 完整字段定义（对照Tushare官方文档：https://tushare.pro/document/2?doc_id=79）
CREATE TABLE IF NOT EXISTS fina_indicator (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    ann_date DATE,  -- 公告日期
    end_date DATE,  -- 计算截至日期

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
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, end_date)
);

CREATE INDEX IF NOT EXISTS idx_fina_date ON fina_indicator(ann_date);
CREATE INDEX IF NOT EXISTS idx_fina_code ON fina_indicator(ts_code);
CREATE INDEX IF NOT EXISTS idx_fina_end_date ON fina_indicator(end_date);

-- 2. income（利润表）
CREATE TABLE IF NOT EXISTS income (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    ann_date DATE,  -- 公告日期
    f_ann_date DATE,  -- 实际公告日期
    end_date DATE,  -- 计算截至日期
    report_type VARCHAR(10),  -- 报告类型
    comp_type VARCHAR(10),  -- 公司类型
    end_type VARCHAR(10),         -- 报告期类型
    update_flag VARCHAR(10),      -- 更新标识

    -- 营业收入与成本
    total_revenue REAL,  -- 营业总收入
    revenue REAL,  -- 营业收入
    operate_profit REAL,  -- 营业利润
    total_cogs REAL,  -- 营业总成本
    interest_income REAL,  -- 利息收入

    -- 利润指标
    profit_dedt REAL,  -- 扣除非经常损益后的净利润
    sell_exp REAL,  -- 销售费用
    admin_exp REAL,  -- 管理费用
    fin_exp REAL,  -- 财务费用
    asset_impair_loss REAL,  -- 资产减值损失
    non_oper_income REAL,  -- 营业外收入
    non_oper_exp REAL,  -- 营业外支出
    total_profit REAL,  -- 利润总额
    income_tax REAL,  -- 所得税
    n_income REAL,  -- 净利润
    n_income_attr_p REAL,  -- 归属母公司所有者的净利润
    minority_gain REAL,  -- 少数股东损益

    -- 每股指标
    basic_eps REAL,  -- 基本每股收益
    diluted_eps REAL,  -- 稀释每股收益

    -- 其他综合收益
    oth_compr_income REAL,  -- 其他综合收益
    t_compr_income REAL,  -- 综合收益总额
    compr_inc_attr_p REAL,  -- 归属母公司所有者的综合收益
    compr_inc_attr_m_s REAL,  -- 归属少数股东的综合收益

    -- 现金流相关
    ebit REAL,  -- 息税前利润
    ebitda REAL,  -- 息税折旧摊销前利润
    rd_exp REAL,  -- 研发费用
    fin_exp_int_exp REAL,  -- 财务费用-利息支出
    fin_exp_int_income REAL,  -- 财务费用-利息收入
    transfer_surplus_reserve REAL,  -- 盈余公积转入
    transfer_risk_reserve REAL,  -- 风险准备转入

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, end_date, report_type)
);

CREATE INDEX IF NOT EXISTS idx_income_date ON income(end_date);
CREATE INDEX IF NOT EXISTS idx_income_code ON income(ts_code);
CREATE INDEX IF NOT EXISTS idx_income_ann_date ON income(ann_date);

-- 3. balancesheet（资产负债表）
CREATE TABLE IF NOT EXISTS balancesheet (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    ann_date DATE,  -- 公告日期
    f_ann_date DATE,  -- 实际公告日期
    end_date DATE,  -- 计算截至日期
    report_type VARCHAR(10),  -- 报告类型
    comp_type VARCHAR(10),  -- 公司类型
    end_type VARCHAR(10),         -- 报告期类型
    update_flag VARCHAR(10),      -- 更新标识

    -- 流动资产
    total_cur_assets REAL,  -- 流动资产合计
    money_cap REAL,  -- 货币资金
    trad_asset REAL,  -- 交易性金融资产
    notes_receiv REAL,  -- 应收票据
    accounts_receiv REAL,  -- 应收账款
    adv_payment REAL,  -- 预付款项
    other_receiv REAL,  -- 其他应收款
    inventories REAL,  -- 存货
    amor_exp REAL,  -- 长期待摊费用
    long_ampay_dep_rec_asim REAL,  -- 长期应收款项

    -- 非流动资产
    total_nca REAL,  -- 非流动资产合计
    fix_assets REAL,  -- 固定资产
    cip REAL,  -- 在建工程
    const_materials REAL,  -- 工程物资
    intang_assets REAL,  -- 无形资产
    goodwill REAL,  -- 商誉
    long_deferred_exp REAL,  -- 长期待摊费用
    defer_tax_assets REAL,  -- 递延所得税资产

    -- 资产总计
    total_assets REAL,  -- 资产总计

    -- 流动负债
    total_cur_liab REAL,  -- 流动负债合计
    st_borr REAL,  -- 短期借款
    notes_payable REAL,  -- 应付票据
    accounts_pay REAL,  -- 应付账款
    adv_receipts REAL,  -- 预收款项
    payroll_pay REAL,  -- 应付职工薪酬
    taxes_payable REAL,  -- 应交税费
    interest_payable REAL,  -- 应付利息
    div_payable REAL,  -- 应付股利
    other_payable REAL,  -- 其他应付款

    -- 非流动负债
    total_ncl REAL,  -- 非流动负债合计
    long_borr REAL,  -- 长期借款
    bonds_payable REAL,  -- 应付债券
    long_deferred_rev REAL,  -- 长期递延收益
    defer_tax_liab REAL,  -- 递延所得税负债

    -- 负债合计
    total_liab REAL,  -- 负债合计

    -- 股东权益
    cap_rese REAL,  -- 资本公积
    undistr_porfit REAL,  -- 未分配利润
    minority_int_ratio REAL,  -- 少数股东权益比例
    total_hldr_eqy_exc_min_int REAL,  -- 所有者权益合计(不含少数股东权益)
    total_hldr_eqy_inc_min_int REAL,  -- 所有者权益合计(含少数股东权益)
    total_liab_hldr_eqy REAL,  -- 负债和股东权益总计

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, end_date, report_type)
);

CREATE INDEX IF NOT EXISTS idx_balance_date ON balancesheet(end_date);
CREATE INDEX IF NOT EXISTS idx_balance_code ON balancesheet(ts_code);
CREATE INDEX IF NOT EXISTS idx_balance_ann_date ON balancesheet(ann_date);

-- 4. cashflow（现金流量表）
CREATE TABLE IF NOT EXISTS cashflow (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    ann_date DATE,  -- 公告日期
    f_ann_date DATE,  -- 实际公告日期
    end_date DATE,  -- 计算截至日期
    report_type VARCHAR(10),  -- 报告类型
    comp_type VARCHAR(10),  -- 公司类型
    end_type VARCHAR(10),         -- 报告期类型
    update_flag VARCHAR(10),      -- 更新标识

    -- 经营活动现金流
    n_cashflow_act REAL,  -- 经营活动现金流量净额
    cash_recp_sg_and_rs REAL,  -- 销售商品提供劳务收到的现金
    recp_tax_rends REAL,
    cash_pay_for_tax REAL,  -- 支付的各项税费
    cash_pay_acq_const_fi REAL,  -- 购建固定资产、无形资产和其他长期资产支付的现金
    cash_pay_for_depos REAL,  -- 支付存款净增加额
    cash_recp_loan_rel_fi REAL,  -- 取得借款收到的现金
    free_cashflow REAL,  -- 自由现金流

    -- 投资活动现金流
    n_cash_flows_inv_act REAL,  -- 投资活动现金流量净额
    c_fr_sale_sg REAL,  -- 销售商品提供劳务收到的现金
    c_fr_for_sale REAL,  -- 处置固定资产、无形资产和其他长期资产收回的现金净额
    c_fr_disp_withdrw_invest REAL,  -- 处置子公司及其他营业单位收到的现金净额
    c_recp_return_invest REAL,  -- 收回投资收到的现金
    c_recp_loan_rel_fi REAL,  -- 取得借款收到的现金
    c_fr_oth_inv_act REAL,  -- 收到其他与投资活动有关的现金
    n_cashflow_inv_act REAL,
    c_pay_for_acq_fi REAL,  -- 购建固定资产、无形资产和其他长期资产支付的现金
    c_pay_for_invest REAL,  -- 投资支付的现金
    c_pay_oth_inv_act REAL,  -- 支付其他与投资活动有关的现金

    -- 筹资活动现金流
    n_cash_flows_fnc_act REAL,  -- 筹资活动现金流量净额
    c_fr_cap_contr REAL,  -- 吸收投资收到的现金
    c_fr_borrow REAL,  -- 取得借款收到的现金
    c_fr_oth_fnc_act REAL,  -- 收到其他与筹资活动有关的现金
    n_cashflow_fnc_act REAL,  -- 筹资活动现金流量净额
    c_pay_for_dist_dpcp_int_exp REAL,  -- 分配股利、利润或偿付利息支付的现金
    c_pay_for_loan_rel_fi REAL,  -- 偿还债务支付的现金
    c_pay_oth_fnc_act REAL,  -- 支付其他与筹资活动有关的现金

    -- 其他
    n_incr_cash_cash_equ REAL,
    effect_forex_cash REAL,  -- 汇率变动对现金的影响

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, end_date, report_type)
);

CREATE INDEX IF NOT EXISTS idx_cashflow_date ON cashflow(end_date);
CREATE INDEX IF NOT EXISTS idx_cashflow_code ON cashflow(ts_code);
CREATE INDEX IF NOT EXISTS idx_cashflow_ann_date ON cashflow(ann_date);

-- 5. express（业绩预告）
CREATE TABLE IF NOT EXISTS express (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    ann_date DATE,  -- 公告日期
    end_date DATE,  -- 计算截至日期
    report_type VARCHAR(10),  -- 报告类型
    comp_type VARCHAR(10),  -- 公司类型
    end_type VARCHAR(10),         -- 报告期类型
    update_flag VARCHAR(10),      -- 更新标识

    -- 业绩预告类型
    type VARCHAR(20),  -- 指数类型（N=概念S=特色）

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
    change_reason VARCHAR(1000),  -- 变动原因

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, end_date, ann_date)
);

CREATE INDEX IF NOT EXISTS idx_express_date ON express(end_date);
CREATE INDEX IF NOT EXISTS idx_express_code ON express(ts_code);
CREATE INDEX IF NOT EXISTS idx_express_ann_date ON express(ann_date);

-- 6. express_brief（业绩快报）
CREATE TABLE IF NOT EXISTS express_brief (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    ann_date DATE,  -- 公告日期
    end_date DATE,  -- 计算截至日期
    report_type VARCHAR(10),  -- 报告类型
    comp_type VARCHAR(10),  -- 公司类型
    end_type VARCHAR(10),         -- 报告期类型
    update_flag VARCHAR(10),      -- 更新标识

    -- 营业收入
    total_revenue REAL,  -- 营业总收入
    revenue REAL,  -- 营业收入

    -- 营业利润
    operate_profit REAL,  -- 营业利润
    total_profit REAL,  -- 利润总额

    -- 净利润
    n_income REAL,  -- 净利润
    n_income_attr_p REAL,  -- 归属母公司所有者的净利润

    -- 每股指标
    basic_eps REAL,  -- 基本每股收益
    diluted_eps REAL,  -- 稀释每股收益

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
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, end_date, ann_date)
);

CREATE INDEX IF NOT EXISTS idx_express_brief_date ON express_brief(end_date);
CREATE INDEX IF NOT EXISTS idx_express_brief_code ON express_brief(ts_code);
CREATE INDEX IF NOT EXISTS idx_express_brief_ann_date ON express_brief(ann_date);

-- 7. dividend（分红送股）
CREATE TABLE IF NOT EXISTS dividend (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    ann_date DATE,  -- 公告日期
    record_date DATE,  -- 除权日
    ex_date DATE,  -- 除权除息日
    pay_date DATE,  -- 派息日
    div_proc VARCHAR(20),  -- 分红进度
    stk_div REAL,  -- 送股比例
    stk_bo_rate REAL,  -- 送股比例
    stk_co_rate REAL,  -- 转增比例
    cash_div REAL,  -- 现金分红
    cash_div_tax REAL,  -- 扣税后现金分红

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, ann_date, record_date)
);

CREATE INDEX IF NOT EXISTS idx_dividend_date ON dividend(ann_date);
CREATE INDEX IF NOT EXISTS idx_dividend_code ON dividend(ts_code);


-- P3资金流向(THS)表（共3张）
-- 按交易日每日拉取，使用同花顺数据接口

-- 8. ths_moneyflow（个股资金流向）
CREATE TABLE IF NOT EXISTS ths_moneyflow (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期
    name VARCHAR(50),  -- 股票名称
    pct_change REAL,
    latest REAL,  -- 最新数据
    net_amount REAL,
    net_d5_amount REAL,
    buy_lg_amount REAL,  -- 大单买入金额
    buy_lg_amount_rate REAL,  -- 大单买入金额占比
    buy_md_amount REAL,  -- 中单买入金额
    buy_md_amount_rate REAL,  -- 中单买入金额占比
    buy_sm_amount REAL,  -- 小单买入金额
    buy_sm_amount_rate REAL,  -- 小单买入金额占比

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_ths_moneyflow_date ON ths_moneyflow(trade_date);
CREATE INDEX IF NOT EXISTS idx_ths_moneyflow_code ON ths_moneyflow(ts_code);

-- 9. ths_concept_moneyflow（同花顺概念板块资金流向）
CREATE TABLE IF NOT EXISTS ths_concept_moneyflow (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期
    name VARCHAR(50),  -- 股票名称
    lead_stock VARCHAR(50),  -- 龙头股票
    close_price REAL,  -- 收盘价
    pct_change REAL,
    industry_index REAL,  -- 行业指数
    company_num INTEGER,  -- 公司数量
    pct_change_stock REAL,
    net_buy_amount REAL,
    net_sell_amount REAL,
    net_amount REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_ths_concept_moneyflow_date ON ths_concept_moneyflow(trade_date);
CREATE INDEX IF NOT EXISTS idx_ths_concept_moneyflow_code ON ths_concept_moneyflow(ts_code);

-- 10. ths_industry_moneyflow（同花顺行业资金流向）
CREATE TABLE IF NOT EXISTS ths_industry_moneyflow (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期
    industry VARCHAR(50),  -- 所属行业
    lead_stock VARCHAR(50),  -- 龙头股票
    close REAL,  -- 收盘价
    pct_change REAL,
    company_num INTEGER,  -- 公司数量
    pct_change_stock REAL,
    close_price REAL,  -- 收盘价
    net_buy_amount REAL,
    net_sell_amount REAL,
    net_amount REAL,

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

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
    in_date DATE,  -- 纳入日期
    out_date DATE,
    is_new VARCHAR(2),  -- 是否新纳入

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, con_code)
);

CREATE INDEX IF NOT EXISTS idx_ths_concept_member_code ON ths_concept_member(con_code);
CREATE INDEX IF NOT EXISTS idx_ths_concept_member_ts_code ON ths_concept_member(ts_code);

-- 12. ths_index_daily（同花顺概念和行业指数日线）
CREATE TABLE IF NOT EXISTS ths_index_daily (
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期
    open REAL,  -- 开盘价
    high REAL,  -- 最高价
    low REAL,  -- 最低价
    close REAL,  -- 收盘价
    vol REAL,  -- 成交量（手）
    amount REAL,  -- 成交额（千元）
    pct_chg REAL,  -- 涨跌幅（%）

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_ths_index_daily_date ON ths_index_daily(trade_date);
CREATE INDEX IF NOT EXISTS idx_ths_index_daily_code ON ths_index_daily(ts_code);


-- P4游资表（共2张）
-- hots_user：无游标，全量拉取
-- hots_trader_detail：按交易日拉取

-- 13. hots_user（游资账户）
CREATE TABLE IF NOT EXISTS hots_user (
    account VARCHAR(50) PRIMARY KEY,  -- 账户
    trader_name VARCHAR(100),
    broker_name VARCHAR(100),  -- 券商名称
    license VARCHAR(20),  -- 许可证
    reg_date DATE,
    status VARCHAR(10),  -- 状态

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

CREATE INDEX IF NOT EXISTS idx_hots_user_account ON hots_user(account);
CREATE INDEX IF NOT EXISTS idx_hots_user_broker ON hots_user(broker_name);

-- 14. hots_trader_detail（游资交易）
CREATE TABLE IF NOT EXISTS hots_trader_detail (
    account VARCHAR(50),  -- 账户
    ts_code VARCHAR(10),  -- 股票代码/指数代码/ETF代码
    trade_date DATE,  -- 交易日期
    buy_amount REAL,  -- 买入金额
    sell_amount REAL,  -- 卖出金额
    net_amount REAL,
    buy_vol REAL,  -- 买入量
    sell_vol REAL,  -- 卖出量
    net_vol REAL,
    reason VARCHAR(500),

    -- 更新时间
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间

    PRIMARY KEY (account, ts_code, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_date ON hots_trader_detail(trade_date);
CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_code ON hots_trader_detail(ts_code);
CREATE INDEX IF NOT EXISTS idx_hots_trader_detail_account ON hots_trader_detail(account);