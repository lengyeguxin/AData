-- cashflow (现金流量表)
-- API接口: cashflow_vip
-- API字段数: 97

COMMENT ON TABLE cashflow IS '现金流量表';

CREATE TABLE IF NOT EXISTS cashflow (
    ts_code VARCHAR(10),  -- TS代码
    ann_date DATE,  -- 公告日期
    f_ann_date DATE,  -- 实际公告日期
    end_date DATE,  -- 报告期
    comp_type REAL,  -- 公司类型
    report_type REAL,  -- 报告类型
    end_type REAL,  -- 报告期类型
    net_profit REAL,  -- 净利润
    finan_exp REAL,  -- 财务费用
    c_fr_sale_sg REAL,  -- c_fr_sale_sg
    recp_tax_rends REAL,  -- 应收
    n_depos_incr_fi REAL,  -- n_depos_incr_fi
    n_incr_loans_cb REAL,  -- n_incr_loans_cb
    n_inc_borr_oth_fi REAL,  -- n_inc_borr_oth_fi
    prem_fr_orig_contr REAL,  -- prem_fr_orig_contr
    n_incr_insured_dep REAL,  -- n_incr_insured_dep
    n_reinsur_prem REAL,  -- n_reinsur_prem
    n_incr_disp_tfa REAL,  -- n_incr_disp_tfa
    ifc_cash_incr REAL,  -- ifc_cash_incr
    n_incr_disp_faas REAL,  -- n_incr_disp_faas
    n_incr_loans_oth_bank REAL,  -- n_incr_loans_oth_bank
    n_cap_incr_repur REAL,  -- n_cap_incr_repur
    c_fr_oth_operate_a REAL,  -- 比率
    c_inf_fr_operate_a REAL,  -- 比率
    c_paid_goods_s REAL,  -- c_paid_goods_s
    c_paid_to_for_empl REAL,  -- c_paid_to_for_empl
    c_paid_for_taxes REAL,  -- c_paid_for_taxes
    n_incr_clt_loan_adv REAL,  -- n_incr_clt_loan_adv
    n_incr_dep_cbob REAL,  -- n_incr_dep_cbob
    c_pay_claims_orig_inco REAL,  -- 应付
    pay_handling_chrg REAL,  -- 应付
    pay_comm_insur_plcy REAL,  -- 应付
    oth_cash_pay_oper_act REAL,  -- 应付
    st_cash_out_act REAL,  -- st_cash_out_act
    n_cashflow_act REAL,  -- n_cashflow_act
    oth_recp_ral_inv_act REAL,  -- 应收
    c_disp_withdrwl_invest REAL,  -- c_disp_withdrwl_invest
    c_recp_return_invest REAL,  -- 应收
    n_recp_disp_fiolta REAL,  -- 应收
    n_recp_disp_sobu REAL,  -- 应收
    stot_inflows_inv_act REAL,  -- stot_inflows_inv_act
    c_pay_acq_const_fiolta REAL,  -- 应付
    c_paid_invest REAL,  -- c_paid_invest
    n_disp_subs_oth_biz REAL,  -- n_disp_subs_oth_biz
    oth_pay_ral_inv_act REAL,  -- 应付
    n_incr_pledge_loan REAL,  -- n_incr_pledge_loan
    stot_out_inv_act REAL,  -- stot_out_inv_act
    n_cashflow_inv_act REAL,  -- n_cashflow_inv_act
    c_recp_borrow REAL,  -- 应收
    proc_issue_bonds REAL,  -- proc_issue_bonds
    oth_cash_recp_ral_fnc_act REAL,  -- 应收
    stot_cash_in_fnc_act REAL,  -- stot_cash_in_fnc_act
    free_cashflow REAL,  -- free_cashflow
    c_prepay_amt_borr REAL,  -- 应付
    c_pay_dist_dpcp_int_exp REAL,  -- 费用
    incl_dvd_profit_paid_sc_ms REAL,  -- incl_dvd_profit_paid_sc_ms
    oth_cashpay_ral_fnc_act REAL,  -- 应付
    stot_cashout_fnc_act REAL,  -- stot_cashout_fnc_act
    n_cash_flows_fnc_act REAL,  -- n_cash_flows_fnc_act
    eff_fx_flu_cash REAL,  -- eff_fx_flu_cash
    n_incr_cash_cash_equ REAL,  -- n_incr_cash_cash_equ
    c_cash_equ_beg_period REAL,  -- c_cash_equ_beg_period
    c_cash_equ_end_period REAL,  -- c_cash_equ_end_period
    c_recp_cap_contrib REAL,  -- 应收
    incl_cash_rec_saims REAL,  -- incl_cash_rec_saims
    uncon_invest_loss REAL,  -- uncon_invest_loss
    prov_depr_assets REAL,  -- 资产
    depr_fa_coga_dpba REAL,  -- depr_fa_coga_dpba
    amort_intang_assets REAL,  -- 资产
    lt_amort_deferred_exp REAL,  -- 费用
    decr_deferred_exp REAL,  -- 费用
    incr_acc_exp REAL,  -- 费用
    loss_disp_fiolta REAL,  -- loss_disp_fiolta
    loss_scr_fa REAL,  -- loss_scr_fa
    loss_fv_chg REAL,  -- loss_fv_chg
    invest_loss REAL,  -- invest_loss
    decr_def_inc_tax_assets REAL,  -- 资产
    incr_def_inc_tax_liab REAL,  -- 负债
    decr_inventories REAL,  -- decr_inventories
    decr_oper_payable REAL,  -- 应付
    incr_oper_payable REAL,  -- 应付
    others REAL,  -- others
    im_net_cashflow_oper_act REAL,  -- im_net_cashflow_oper_act
    conv_debt_into_cap REAL,  -- conv_debt_into_cap
    conv_copbonds_due_within_1y REAL,  -- conv_copbonds_due_within_1y
    fa_fnc_leases REAL,  -- fa_fnc_leases
    im_n_incr_cash_equ REAL,  -- im_n_incr_cash_equ
    net_dism_capital_add REAL,  -- net_dism_capital_add
    net_cash_rece_sec REAL,  -- net_cash_rece_sec
    credit_impa_loss REAL,  -- 信用减值损失
    use_right_asset_dep REAL,  -- use_right_asset_dep
    oth_loss_asset REAL,  -- oth_loss_asset
    end_bal_cash REAL,  -- end_bal_cash
    beg_bal_cash REAL,  -- beg_bal_cash
    end_bal_cash_equ REAL,  -- end_bal_cash_equ
    beg_bal_cash_equ REAL,  -- beg_bal_cash_equ
    update_flag VARCHAR(10),  -- 更新标识
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE cashflow ADD PRIMARY KEY (ts_code, end_date, report_type);

COMMENT ON COLUMN cashflow.ts_code IS 'TS代码';
COMMENT ON COLUMN cashflow.ann_date IS '公告日期';
COMMENT ON COLUMN cashflow.f_ann_date IS '实际公告日期';
COMMENT ON COLUMN cashflow.end_date IS '报告期';
COMMENT ON COLUMN cashflow.comp_type IS '公司类型';
COMMENT ON COLUMN cashflow.report_type IS '报告类型';
COMMENT ON COLUMN cashflow.end_type IS '报告期类型';
COMMENT ON COLUMN cashflow.net_profit IS '净利润';
COMMENT ON COLUMN cashflow.finan_exp IS '财务费用';
COMMENT ON COLUMN cashflow.recp_tax_rends IS '应收';
COMMENT ON COLUMN cashflow.c_fr_oth_operate_a IS '比率';
COMMENT ON COLUMN cashflow.c_inf_fr_operate_a IS '比率';
COMMENT ON COLUMN cashflow.c_pay_claims_orig_inco IS '应付';
COMMENT ON COLUMN cashflow.pay_handling_chrg IS '应付';
COMMENT ON COLUMN cashflow.pay_comm_insur_plcy IS '应付';
COMMENT ON COLUMN cashflow.oth_cash_pay_oper_act IS '应付';
COMMENT ON COLUMN cashflow.oth_recp_ral_inv_act IS '应收';
COMMENT ON COLUMN cashflow.c_recp_return_invest IS '应收';
COMMENT ON COLUMN cashflow.n_recp_disp_fiolta IS '应收';
COMMENT ON COLUMN cashflow.n_recp_disp_sobu IS '应收';
COMMENT ON COLUMN cashflow.c_pay_acq_const_fiolta IS '应付';
COMMENT ON COLUMN cashflow.oth_pay_ral_inv_act IS '应付';
COMMENT ON COLUMN cashflow.c_recp_borrow IS '应收';
COMMENT ON COLUMN cashflow.oth_cash_recp_ral_fnc_act IS '应收';
COMMENT ON COLUMN cashflow.c_prepay_amt_borr IS '应付';
COMMENT ON COLUMN cashflow.c_pay_dist_dpcp_int_exp IS '费用';
COMMENT ON COLUMN cashflow.oth_cashpay_ral_fnc_act IS '应付';
COMMENT ON COLUMN cashflow.c_recp_cap_contrib IS '应收';
COMMENT ON COLUMN cashflow.prov_depr_assets IS '资产';
COMMENT ON COLUMN cashflow.amort_intang_assets IS '资产';
COMMENT ON COLUMN cashflow.lt_amort_deferred_exp IS '费用';
COMMENT ON COLUMN cashflow.decr_deferred_exp IS '费用';
COMMENT ON COLUMN cashflow.incr_acc_exp IS '费用';
COMMENT ON COLUMN cashflow.decr_def_inc_tax_assets IS '资产';
COMMENT ON COLUMN cashflow.incr_def_inc_tax_liab IS '负债';
COMMENT ON COLUMN cashflow.decr_oper_payable IS '应付';
COMMENT ON COLUMN cashflow.incr_oper_payable IS '应付';
COMMENT ON COLUMN cashflow.credit_impa_loss IS '信用减值损失';
COMMENT ON COLUMN cashflow.update_flag IS '更新标识';

-- 索引
CREATE INDEX IF NOT EXISTS idx_cashflow_date ON cashflow(end_date);
CREATE INDEX IF NOT EXISTS idx_cashflow_code ON cashflow(ts_code);
CREATE INDEX IF NOT EXISTS idx_cashflow_ann_date ON cashflow(ann_date);
