-- fina_indicator (财务指标)
-- API接口: fina_indicator_vip
-- API字段数: 108

COMMENT ON TABLE fina_indicator IS '财务指标';

CREATE TABLE IF NOT EXISTS fina_indicator (
    ts_code VARCHAR(10),  -- TS代码
    ann_date DATE,  -- 公告日期
    end_date DATE,  -- 报告期
    eps REAL,  -- eps
    dt_eps REAL,  -- dt_eps
    total_revenue_ps INTEGER,  -- total_revenue_ps
    revenue_ps REAL,  -- revenue_ps
    capital_rese_ps REAL,  -- capital_rese_ps
    surplus_rese_ps REAL,  -- surplus_rese_ps
    undist_profit_ps REAL,  -- undist_profit_ps
    extra_item REAL,  -- 非经常性损益项目
    profit_dedt REAL,  -- profit_dedt
    gross_margin REAL,  -- gross_margin
    current_ratio REAL,  -- 比率
    quick_ratio REAL,  -- 比率
    cash_ratio REAL,  -- 比率
    ar_turn REAL,  -- ar_turn
    ca_turn REAL,  -- ca_turn
    fa_turn REAL,  -- fa_turn
    assets_turn REAL,  -- 资产
    op_income REAL,  -- 收入
    ebit REAL,  -- ebit
    ebitda REAL,  -- ebitda
    fcff REAL,  -- fcff
    fcfe REAL,  -- fcfe
    current_exint REAL,  -- current_exint
    noncurrent_exint REAL,  -- noncurrent_exint
    interestdebt REAL,  -- interestdebt
    netdebt REAL,  -- netdebt
    tangible_asset REAL,  -- tangible_asset
    working_capital REAL,  -- working_capital
    networking_capital REAL,  -- networking_capital
    invest_capital REAL,  -- invest_capital
    retained_earnings REAL,  -- retained_earnings
    diluted2_eps REAL,  -- diluted2_eps
    bps REAL,  -- bps
    ocfps REAL,  -- ocfps
    retainedps REAL,  -- retainedps
    cfps REAL,  -- cfps
    ebit_ps REAL,  -- ebit_ps
    fcff_ps REAL,  -- fcff_ps
    fcfe_ps REAL,  -- fcfe_ps
    netprofit_margin REAL,  -- 净利润率
    grossprofit_margin REAL,  -- 毛利润率
    cogs_of_sales REAL,  -- cogs_of_sales
    expense_of_sales REAL,  -- 费用
    profit_to_gr REAL,  -- profit_to_gr
    saleexp_to_gr REAL,  -- 费用
    adminexp_of_gr REAL,  -- 费用
    finaexp_of_gr REAL,  -- 费用
    impai_ttm REAL,  -- impai_ttm
    gc_of_gr REAL,  -- gc_of_gr
    op_of_gr REAL,  -- op_of_gr
    ebit_of_gr REAL,  -- ebit_of_gr
    roe REAL,  -- roe
    roe_waa REAL,  -- roe_waa
    roe_dt REAL,  -- roe_dt
    roa REAL,  -- roa
    npta REAL,  -- npta
    roic REAL,  -- roic
    roe_yearly REAL,  -- roe_yearly
    roa2_yearly REAL,  -- roa2_yearly
    debt_to_assets REAL,  -- 资产
    assets_to_eqt REAL,  -- 资产
    dp_assets_to_eqt REAL,  -- 资产
    ca_to_assets REAL,  -- 流动资产/总资产
    nca_to_assets REAL,  -- 非流动资产/总资产
    tbassets_to_totalassets REAL,  -- 资产
    int_to_talcap REAL,  -- int_to_talcap
    eqt_to_talcapital REAL,  -- eqt_to_talcapital
    currentdebt_to_debt REAL,  -- currentdebt_to_debt
    longdeb_to_debt REAL,  -- longdeb_to_debt
    ocf_to_shortdebt REAL,  -- ocf_to_shortdebt
    debt_to_eqt REAL,  -- debt_to_eqt
    eqt_to_debt REAL,  -- eqt_to_debt
    eqt_to_interestdebt REAL,  -- eqt_to_interestdebt
    tangibleasset_to_debt REAL,  -- tangibleasset_to_debt
    tangasset_to_intdebt REAL,  -- tangasset_to_intdebt
    tangibleasset_to_netdebt REAL,  -- tangibleasset_to_netdebt
    ocf_to_debt REAL,  -- ocf_to_debt
    turn_days REAL,  -- turn_days
    roa_yearly REAL,  -- roa_yearly
    roa_dp REAL,  -- roa_dp
    fixed_assets REAL,  -- 资产
    profit_to_op REAL,  -- profit_to_op
    q_saleexp_to_gr REAL,  -- 费用
    q_gc_to_gr REAL,  -- q_gc_to_gr
    q_roe REAL,  -- q_roe
    q_dt_roe REAL,  -- q_dt_roe
    q_npta REAL,  -- q_npta
    q_ocf_to_sales REAL,  -- q_ocf_to_sales
    basic_eps_yoy REAL,  -- basic_eps_yoy
    dt_eps_yoy REAL,  -- dt_eps_yoy
    cfps_yoy REAL,  -- cfps_yoy
    op_yoy REAL,  -- op_yoy
    ebt_yoy REAL,  -- ebt_yoy
    netprofit_yoy REAL,  -- netprofit_yoy
    dt_netprofit_yoy REAL,  -- dt_netprofit_yoy
    ocf_yoy REAL,  -- ocf_yoy
    roe_yoy REAL,  -- roe_yoy
    bps_yoy REAL,  -- bps_yoy
    assets_yoy REAL,  -- 资产
    eqt_yoy REAL,  -- eqt_yoy
    tr_yoy REAL,  -- tr_yoy
    or_yoy REAL,  -- or_yoy
    q_sales_yoy REAL,  -- q_sales_yoy
    q_op_qoq REAL,  -- q_op_qoq
    equity_yoy REAL,  -- equity_yoy
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE fina_indicator ADD PRIMARY KEY (ts_code, end_date);

COMMENT ON COLUMN fina_indicator.ts_code IS 'TS代码';
COMMENT ON COLUMN fina_indicator.ann_date IS '公告日期';
COMMENT ON COLUMN fina_indicator.end_date IS '报告期';
COMMENT ON COLUMN fina_indicator.extra_item IS '非经常性损益项目';
COMMENT ON COLUMN fina_indicator.current_ratio IS '比率';
COMMENT ON COLUMN fina_indicator.quick_ratio IS '比率';
COMMENT ON COLUMN fina_indicator.cash_ratio IS '比率';
COMMENT ON COLUMN fina_indicator.assets_turn IS '资产';
COMMENT ON COLUMN fina_indicator.op_income IS '收入';
COMMENT ON COLUMN fina_indicator.netprofit_margin IS '净利润率';
COMMENT ON COLUMN fina_indicator.grossprofit_margin IS '毛利润率';
COMMENT ON COLUMN fina_indicator.expense_of_sales IS '费用';
COMMENT ON COLUMN fina_indicator.saleexp_to_gr IS '费用';
COMMENT ON COLUMN fina_indicator.adminexp_of_gr IS '费用';
COMMENT ON COLUMN fina_indicator.finaexp_of_gr IS '费用';
COMMENT ON COLUMN fina_indicator.debt_to_assets IS '资产';
COMMENT ON COLUMN fina_indicator.assets_to_eqt IS '资产';
COMMENT ON COLUMN fina_indicator.dp_assets_to_eqt IS '资产';
COMMENT ON COLUMN fina_indicator.ca_to_assets IS '流动资产/总资产';
COMMENT ON COLUMN fina_indicator.nca_to_assets IS '非流动资产/总资产';
COMMENT ON COLUMN fina_indicator.tbassets_to_totalassets IS '资产';
COMMENT ON COLUMN fina_indicator.fixed_assets IS '资产';
COMMENT ON COLUMN fina_indicator.q_saleexp_to_gr IS '费用';
COMMENT ON COLUMN fina_indicator.assets_yoy IS '资产';

-- 索引
CREATE INDEX IF NOT EXISTS idx_fina_indicator_date ON fina_indicator(end_date);
CREATE INDEX IF NOT EXISTS idx_fina_indicator_code ON fina_indicator(ts_code);
CREATE INDEX IF NOT EXISTS idx_fina_indicator_ann_date ON fina_indicator(ann_date);
