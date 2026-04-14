-- income (利润表)
-- API接口: income_vip
-- API字段数: 94

COMMENT ON TABLE income IS '利润表';

CREATE TABLE IF NOT EXISTS income (
    ts_code VARCHAR(10),  -- TS代码
    ann_date DATE,  -- 公告日期
    f_ann_date DATE,  -- 实际公告日期
    end_date DATE,  -- 报告期
    report_type REAL,  -- 报告类型
    comp_type REAL,  -- 公司类型
    end_type REAL,  -- 报告期类型
    basic_eps REAL,  -- basic_eps
    diluted_eps REAL,  -- diluted_eps
    total_revenue INTEGER,  -- total_revenue
    revenue REAL,  -- revenue
    int_income REAL,  -- 利息收入
    prem_earned REAL,  -- 已赚保费
    comm_income REAL,  -- 手续费及佣金收入
    n_commis_income REAL,  -- 收入
    n_oth_income REAL,  -- 收入
    n_oth_b_income REAL,  -- 收入
    prem_income REAL,  -- 收入
    out_prem REAL,  -- out_prem
    une_prem_reser REAL,  -- une_prem_reser
    reins_income REAL,  -- 收入
    n_sec_tb_income REAL,  -- 收入
    n_sec_uw_income REAL,  -- 收入
    n_asset_mg_income REAL,  -- 收入
    oth_b_income REAL,  -- 收入
    fv_value_chg_gain REAL,  -- 公允价值变动收益
    invest_income REAL,  -- 投资收益
    ass_invest_income REAL,  -- 收入
    forex_gain REAL,  -- 汇兑收益
    total_cogs INTEGER,  -- total_cogs
    oper_cost REAL,  -- 营业成本
    int_exp REAL,  -- 利息支出
    comm_exp REAL,  -- 费用
    biz_tax_surchg REAL,  -- biz_tax_surchg
    sell_exp REAL,  -- 费用
    admin_exp REAL,  -- 费用
    fin_exp REAL,  -- 费用
    assets_impair_loss REAL,  -- 资产
    prem_refund REAL,  -- prem_refund
    compens_payout REAL,  -- 应付
    reser_insur_liab REAL,  -- 负债
    div_payt REAL,  -- 应付
    reins_exp REAL,  -- 费用
    oper_exp REAL,  -- 费用
    compens_payout_refu REAL,  -- 应付
    insur_reser_refu REAL,  -- insur_reser_refu
    reins_cost_refund REAL,  -- reins_cost_refund
    other_bus_cost REAL,  -- other_bus_cost
    operate_profit REAL,  -- 比率
    non_oper_income REAL,  -- 收入
    non_oper_exp REAL,  -- 费用
    nca_disploss REAL,  -- nca_disploss
    total_profit REAL,  -- total_profit
    income_tax REAL,  -- 收入
    n_income REAL,  -- 收入
    n_income_attr_p REAL,  -- 收入
    minority_gain REAL,  -- minority_gain
    oth_compr_income REAL,  -- 收入
    t_compr_income REAL,  -- 收入
    compr_inc_attr_p REAL,  -- compr_inc_attr_p
    compr_inc_attr_m_s REAL,  -- compr_inc_attr_m_s
    ebit REAL,  -- ebit
    ebitda REAL,  -- ebitda
    insurance_exp REAL,  -- 费用
    undist_profit REAL,  -- undist_profit
    distable_profit REAL,  -- distable_profit
    rd_exp REAL,  -- 费用
    fin_exp_int_exp REAL,  -- 费用
    fin_exp_int_inc REAL,  -- 费用
    transfer_surplus_rese REAL,  -- transfer_surplus_rese
    transfer_housing_imprest REAL,  -- transfer_housing_imprest
    transfer_oth REAL,  -- transfer_oth
    adj_lossgain REAL,  -- adj_lossgain
    withdra_legal_surplus REAL,  -- withdra_legal_surplus
    withdra_legal_pubfund REAL,  -- withdra_legal_pubfund
    withdra_biz_devfund REAL,  -- withdra_biz_devfund
    withdra_rese_fund REAL,  -- withdra_rese_fund
    withdra_oth_ersu REAL,  -- withdra_oth_ersu
    workers_welfare REAL,  -- workers_welfare
    distr_profit_shrhder REAL,  -- distr_profit_shrhder
    prfshare_payable_dvd REAL,  -- 应付
    comshare_payable_dvd REAL,  -- 应付
    capit_comstock_div REAL,  -- capit_comstock_div
    net_after_nr_lp_correct REAL,  -- net_after_nr_lp_correct
    credit_impa_loss REAL,  -- 信用减值损失
    net_expo_hedging_benefits REAL,  -- 费用
    oth_impair_loss_assets REAL,  -- 资产
    total_opcost REAL,  -- total_opcost
    amodcost_fin_assets REAL,  -- 资产
    oth_income REAL,  -- 收入
    asset_disp_income REAL,  -- 收入
    continued_net_profit REAL,  -- 持续经营净利润
    end_net_profit REAL,  -- 终止经营净利润
    update_flag VARCHAR(10),  -- 更新标识
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE income ADD PRIMARY KEY (ts_code, end_date, report_type);

COMMENT ON COLUMN income.ts_code IS 'TS代码';
COMMENT ON COLUMN income.ann_date IS '公告日期';
COMMENT ON COLUMN income.f_ann_date IS '实际公告日期';
COMMENT ON COLUMN income.end_date IS '报告期';
COMMENT ON COLUMN income.report_type IS '报告类型';
COMMENT ON COLUMN income.comp_type IS '公司类型';
COMMENT ON COLUMN income.end_type IS '报告期类型';
COMMENT ON COLUMN income.int_income IS '利息收入';
COMMENT ON COLUMN income.prem_earned IS '已赚保费';
COMMENT ON COLUMN income.comm_income IS '手续费及佣金收入';
COMMENT ON COLUMN income.n_commis_income IS '收入';
COMMENT ON COLUMN income.n_oth_income IS '收入';
COMMENT ON COLUMN income.n_oth_b_income IS '收入';
COMMENT ON COLUMN income.prem_income IS '收入';
COMMENT ON COLUMN income.reins_income IS '收入';
COMMENT ON COLUMN income.n_sec_tb_income IS '收入';
COMMENT ON COLUMN income.n_sec_uw_income IS '收入';
COMMENT ON COLUMN income.n_asset_mg_income IS '收入';
COMMENT ON COLUMN income.oth_b_income IS '收入';
COMMENT ON COLUMN income.fv_value_chg_gain IS '公允价值变动收益';
COMMENT ON COLUMN income.invest_income IS '投资收益';
COMMENT ON COLUMN income.ass_invest_income IS '收入';
COMMENT ON COLUMN income.forex_gain IS '汇兑收益';
COMMENT ON COLUMN income.oper_cost IS '营业成本';
COMMENT ON COLUMN income.int_exp IS '利息支出';
COMMENT ON COLUMN income.comm_exp IS '费用';
COMMENT ON COLUMN income.sell_exp IS '费用';
COMMENT ON COLUMN income.admin_exp IS '费用';
COMMENT ON COLUMN income.fin_exp IS '费用';
COMMENT ON COLUMN income.assets_impair_loss IS '资产';
COMMENT ON COLUMN income.compens_payout IS '应付';
COMMENT ON COLUMN income.reser_insur_liab IS '负债';
COMMENT ON COLUMN income.div_payt IS '应付';
COMMENT ON COLUMN income.reins_exp IS '费用';
COMMENT ON COLUMN income.oper_exp IS '费用';
COMMENT ON COLUMN income.compens_payout_refu IS '应付';
COMMENT ON COLUMN income.operate_profit IS '比率';
COMMENT ON COLUMN income.non_oper_income IS '收入';
COMMENT ON COLUMN income.non_oper_exp IS '费用';
COMMENT ON COLUMN income.income_tax IS '收入';
COMMENT ON COLUMN income.n_income IS '收入';
COMMENT ON COLUMN income.n_income_attr_p IS '收入';
COMMENT ON COLUMN income.oth_compr_income IS '收入';
COMMENT ON COLUMN income.t_compr_income IS '收入';
COMMENT ON COLUMN income.insurance_exp IS '费用';
COMMENT ON COLUMN income.rd_exp IS '费用';
COMMENT ON COLUMN income.fin_exp_int_exp IS '费用';
COMMENT ON COLUMN income.fin_exp_int_inc IS '费用';
COMMENT ON COLUMN income.prfshare_payable_dvd IS '应付';
COMMENT ON COLUMN income.comshare_payable_dvd IS '应付';
COMMENT ON COLUMN income.credit_impa_loss IS '信用减值损失';
COMMENT ON COLUMN income.net_expo_hedging_benefits IS '费用';
COMMENT ON COLUMN income.oth_impair_loss_assets IS '资产';
COMMENT ON COLUMN income.amodcost_fin_assets IS '资产';
COMMENT ON COLUMN income.oth_income IS '收入';
COMMENT ON COLUMN income.asset_disp_income IS '收入';
COMMENT ON COLUMN income.continued_net_profit IS '持续经营净利润';
COMMENT ON COLUMN income.end_net_profit IS '终止经营净利润';
COMMENT ON COLUMN income.update_flag IS '更新标识';

-- 索引
CREATE INDEX IF NOT EXISTS idx_income_date ON income(end_date);
CREATE INDEX IF NOT EXISTS idx_income_code ON income(ts_code);
CREATE INDEX IF NOT EXISTS idx_income_ann_date ON income(ann_date);
