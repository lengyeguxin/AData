-- balancesheet (资产负债表)
-- API接口: balancesheet_vip
-- API字段数: 158

COMMENT ON TABLE balancesheet IS '资产负债表';

CREATE TABLE IF NOT EXISTS balancesheet (
    ts_code VARCHAR(10),  -- TS代码
    ann_date DATE,  -- 公告日期
    f_ann_date DATE,  -- 实际公告日期
    end_date DATE,  -- 报告期
    report_type REAL,  -- 报告类型
    comp_type REAL,  -- 公司类型
    end_type REAL,  -- 报告期类型
    total_share REAL,  -- 总股本
    cap_rese REAL,  -- cap_rese
    undistr_porfit REAL,  -- undistr_porfit
    surplus_rese REAL,  -- 盈余公积
    special_rese REAL,  -- 专项储备
    money_cap REAL,  -- money_cap
    trad_asset REAL,  -- trad_asset
    notes_receiv REAL,  -- 应收
    accounts_receiv REAL,  -- 应收
    oth_receiv REAL,  -- 其他应收款
    prepayment REAL,  -- 预付款项
    div_receiv REAL,  -- 应收股利
    int_receiv REAL,  -- 应收利息
    inventories REAL,  -- inventories
    amor_exp REAL,  -- 费用
    nca_within_1y REAL,  -- nca_within_1y
    sett_rsrv REAL,  -- sett_rsrv
    loanto_oth_bank_fi REAL,  -- loanto_oth_bank_fi
    premium_receiv REAL,  -- 应收
    reinsur_receiv REAL,  -- 应收
    reinsur_res_receiv REAL,  -- 应收
    pur_resale_fa REAL,  -- pur_resale_fa
    oth_cur_assets REAL,  -- 资产
    total_cur_assets REAL,  -- 资产
    fa_avail_for_sale REAL,  -- fa_avail_for_sale
    htm_invest REAL,  -- htm_invest
    lt_eqt_invest REAL,  -- lt_eqt_invest
    invest_real_estate REAL,  -- invest_real_estate
    time_deposits REAL,  -- time_deposits
    oth_assets REAL,  -- 资产
    lt_rec REAL,  -- 长期应收款
    fix_assets REAL,  -- 资产
    cip REAL,  -- cip
    const_materials REAL,  -- const_materials
    fixed_assets_disp REAL,  -- 固定资产清理
    produc_bio_assets REAL,  -- 生产性生物资产
    oil_and_gas_assets REAL,  -- 油气资产
    intan_assets REAL,  -- 无形资产
    r_and_d REAL,  -- 研发支出
    goodwill REAL,  -- goodwill
    lt_amor_exp REAL,  -- 长期待摊费用
    defer_tax_assets REAL,  -- 资产
    decr_in_disbur REAL,  -- decr_in_disbur
    oth_nca REAL,  -- oth_nca
    total_nca INTEGER,  -- total_nca
    cash_reser_cb REAL,  -- cash_reser_cb
    depos_in_oth_bfi REAL,  -- depos_in_oth_bfi
    prec_metals REAL,  -- prec_metals
    deriv_assets REAL,  -- 资产
    rr_reins_une_prem REAL,  -- rr_reins_une_prem
    rr_reins_outstd_cla REAL,  -- rr_reins_outstd_cla
    rr_reins_lins_liab REAL,  -- 负债
    rr_reins_lthins_liab REAL,  -- 负债
    refund_depos REAL,  -- refund_depos
    ph_pledge_loans REAL,  -- ph_pledge_loans
    refund_cap_depos REAL,  -- refund_cap_depos
    indep_acct_assets REAL,  -- 资产
    client_depos REAL,  -- client_depos
    client_prov REAL,  -- client_prov
    transac_seat_fee REAL,  -- transac_seat_fee
    invest_as_receiv REAL,  -- 应收
    total_assets REAL,  -- 资产
    lt_borr REAL,  -- lt_borr
    st_borr REAL,  -- st_borr
    cb_borr REAL,  -- cb_borr
    depos_ib_deposits REAL,  -- depos_ib_deposits
    loan_oth_bank REAL,  -- loan_oth_bank
    trading_fl REAL,  -- trading_fl
    notes_payable REAL,  -- 应付
    acct_payable REAL,  -- 应付
    adv_receipts REAL,  -- adv_receipts
    sold_for_repur_fa REAL,  -- sold_for_repur_fa
    comm_payable REAL,  -- 应付
    payroll_payable REAL,  -- 应付
    taxes_payable REAL,  -- 应付
    int_payable REAL,  -- 应付
    div_payable REAL,  -- 应付
    oth_payable REAL,  -- 应付
    acc_exp REAL,  -- 费用
    deferred_inc REAL,  -- deferred_inc
    st_bonds_payable REAL,  -- 应付
    payable_to_reinsurer REAL,  -- 应付
    rsrv_insur_cont REAL,  -- rsrv_insur_cont
    acting_trading_sec REAL,  -- acting_trading_sec
    acting_uw_sec REAL,  -- acting_uw_sec
    non_cur_liab_due_1y REAL,  -- 负债
    oth_cur_liab REAL,  -- 负债
    total_cur_liab REAL,  -- 负债
    bond_payable REAL,  -- 应付
    lt_payable REAL,  -- 应付
    specific_payables REAL,  -- 应付
    estimated_liab REAL,  -- 负债
    defer_tax_liab REAL,  -- 负债
    defer_inc_non_cur_liab REAL,  -- 负债
    oth_ncl REAL,  -- oth_ncl
    total_ncl INTEGER,  -- total_ncl
    depos_oth_bfi REAL,  -- depos_oth_bfi
    deriv_liab REAL,  -- 负债
    depos REAL,  -- depos
    agency_bus_liab REAL,  -- 负债
    oth_liab REAL,  -- 负债
    prem_receiv_adva REAL,  -- 应收
    depos_received REAL,  -- 应收
    ph_invest REAL,  -- ph_invest
    reser_une_prem REAL,  -- reser_une_prem
    reser_outstd_claims REAL,  -- reser_outstd_claims
    reser_lins_liab REAL,  -- 负债
    reser_lthins_liab REAL,  -- 负债
    indept_acc_liab REAL,  -- 负债
    pledge_borr REAL,  -- pledge_borr
    indem_payable REAL,  -- 应付
    policy_div_payable REAL,  -- 应付
    total_liab REAL,  -- 负债
    treasury_share REAL,  -- 库存股
    ordin_risk_reser REAL,  -- ordin_risk_reser
    forex_differ REAL,  -- forex_differ
    invest_loss_unconf REAL,  -- invest_loss_unconf
    minority_int REAL,  -- 少数股东权益
    total_hldr_eqy_exc_min_int INTEGER,  -- total_hldr_eqy_exc_min_int
    total_hldr_eqy_inc_min_int INTEGER,  -- total_hldr_eqy_inc_min_int
    total_liab_hldr_eqy REAL,  -- 负债
    lt_payroll_payable REAL,  -- 应付
    oth_comp_income REAL,  -- 收入
    oth_eqt_tools REAL,  -- oth_eqt_tools
    oth_eqt_tools_p_shr REAL,  -- oth_eqt_tools_p_shr
    lending_funds REAL,  -- lending_funds
    acc_receivable REAL,  -- 应收
    st_fin_payable REAL,  -- 应付
    payables REAL,  -- 应付
    hfs_assets REAL,  -- 资产
    hfs_sales REAL,  -- hfs_sales
    cost_fin_assets REAL,  -- 资产
    fair_value_fin_assets REAL,  -- 资产
    cip_total INTEGER,  -- cip_total
    oth_pay_total REAL,  -- 应付
    long_pay_total REAL,  -- 应付
    debt_invest REAL,  -- debt_invest
    oth_debt_invest REAL,  -- oth_debt_invest
    oth_eq_invest REAL,  -- oth_eq_invest
    oth_illiq_fin_assets REAL,  -- 资产
    oth_eq_ppbond REAL,  -- oth_eq_ppbond
    receiv_financing REAL,  -- 应收
    use_right_assets REAL,  -- 使用权资产
    lease_liab REAL,  -- 租赁负债
    contract_assets REAL,  -- 合同资产
    contract_liab REAL,  -- 合同负债
    accounts_receiv_bill REAL,  -- 应收
    accounts_pay REAL,  -- 应付
    oth_rcv_total INTEGER,  -- oth_rcv_total
    fix_assets_total REAL,  -- 资产
    update_flag VARCHAR(10),  -- 更新标识
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE balancesheet ADD PRIMARY KEY (ts_code, end_date, report_type);

COMMENT ON COLUMN balancesheet.ts_code IS 'TS代码';
COMMENT ON COLUMN balancesheet.ann_date IS '公告日期';
COMMENT ON COLUMN balancesheet.f_ann_date IS '实际公告日期';
COMMENT ON COLUMN balancesheet.end_date IS '报告期';
COMMENT ON COLUMN balancesheet.report_type IS '报告类型';
COMMENT ON COLUMN balancesheet.comp_type IS '公司类型';
COMMENT ON COLUMN balancesheet.end_type IS '报告期类型';
COMMENT ON COLUMN balancesheet.total_share IS '总股本';
COMMENT ON COLUMN balancesheet.surplus_rese IS '盈余公积';
COMMENT ON COLUMN balancesheet.special_rese IS '专项储备';
COMMENT ON COLUMN balancesheet.notes_receiv IS '应收';
COMMENT ON COLUMN balancesheet.accounts_receiv IS '应收';
COMMENT ON COLUMN balancesheet.oth_receiv IS '其他应收款';
COMMENT ON COLUMN balancesheet.prepayment IS '预付款项';
COMMENT ON COLUMN balancesheet.div_receiv IS '应收股利';
COMMENT ON COLUMN balancesheet.int_receiv IS '应收利息';
COMMENT ON COLUMN balancesheet.amor_exp IS '费用';
COMMENT ON COLUMN balancesheet.premium_receiv IS '应收';
COMMENT ON COLUMN balancesheet.reinsur_receiv IS '应收';
COMMENT ON COLUMN balancesheet.reinsur_res_receiv IS '应收';
COMMENT ON COLUMN balancesheet.oth_cur_assets IS '资产';
COMMENT ON COLUMN balancesheet.total_cur_assets IS '资产';
COMMENT ON COLUMN balancesheet.oth_assets IS '资产';
COMMENT ON COLUMN balancesheet.lt_rec IS '长期应收款';
COMMENT ON COLUMN balancesheet.fix_assets IS '资产';
COMMENT ON COLUMN balancesheet.fixed_assets_disp IS '固定资产清理';
COMMENT ON COLUMN balancesheet.produc_bio_assets IS '生产性生物资产';
COMMENT ON COLUMN balancesheet.oil_and_gas_assets IS '油气资产';
COMMENT ON COLUMN balancesheet.intan_assets IS '无形资产';
COMMENT ON COLUMN balancesheet.r_and_d IS '研发支出';
COMMENT ON COLUMN balancesheet.lt_amor_exp IS '长期待摊费用';
COMMENT ON COLUMN balancesheet.defer_tax_assets IS '资产';
COMMENT ON COLUMN balancesheet.deriv_assets IS '资产';
COMMENT ON COLUMN balancesheet.rr_reins_lins_liab IS '负债';
COMMENT ON COLUMN balancesheet.rr_reins_lthins_liab IS '负债';
COMMENT ON COLUMN balancesheet.indep_acct_assets IS '资产';
COMMENT ON COLUMN balancesheet.invest_as_receiv IS '应收';
COMMENT ON COLUMN balancesheet.total_assets IS '资产';
COMMENT ON COLUMN balancesheet.notes_payable IS '应付';
COMMENT ON COLUMN balancesheet.acct_payable IS '应付';
COMMENT ON COLUMN balancesheet.comm_payable IS '应付';
COMMENT ON COLUMN balancesheet.payroll_payable IS '应付';
COMMENT ON COLUMN balancesheet.taxes_payable IS '应付';
COMMENT ON COLUMN balancesheet.int_payable IS '应付';
COMMENT ON COLUMN balancesheet.div_payable IS '应付';
COMMENT ON COLUMN balancesheet.oth_payable IS '应付';
COMMENT ON COLUMN balancesheet.acc_exp IS '费用';
COMMENT ON COLUMN balancesheet.st_bonds_payable IS '应付';
COMMENT ON COLUMN balancesheet.payable_to_reinsurer IS '应付';
COMMENT ON COLUMN balancesheet.non_cur_liab_due_1y IS '负债';
COMMENT ON COLUMN balancesheet.oth_cur_liab IS '负债';
COMMENT ON COLUMN balancesheet.total_cur_liab IS '负债';
COMMENT ON COLUMN balancesheet.bond_payable IS '应付';
COMMENT ON COLUMN balancesheet.lt_payable IS '应付';
COMMENT ON COLUMN balancesheet.specific_payables IS '应付';
COMMENT ON COLUMN balancesheet.estimated_liab IS '负债';
COMMENT ON COLUMN balancesheet.defer_tax_liab IS '负债';
COMMENT ON COLUMN balancesheet.defer_inc_non_cur_liab IS '负债';
COMMENT ON COLUMN balancesheet.deriv_liab IS '负债';
COMMENT ON COLUMN balancesheet.agency_bus_liab IS '负债';
COMMENT ON COLUMN balancesheet.oth_liab IS '负债';
COMMENT ON COLUMN balancesheet.prem_receiv_adva IS '应收';
COMMENT ON COLUMN balancesheet.depos_received IS '应收';
COMMENT ON COLUMN balancesheet.reser_lins_liab IS '负债';
COMMENT ON COLUMN balancesheet.reser_lthins_liab IS '负债';
COMMENT ON COLUMN balancesheet.indept_acc_liab IS '负债';
COMMENT ON COLUMN balancesheet.indem_payable IS '应付';
COMMENT ON COLUMN balancesheet.policy_div_payable IS '应付';
COMMENT ON COLUMN balancesheet.total_liab IS '负债';
COMMENT ON COLUMN balancesheet.treasury_share IS '库存股';
COMMENT ON COLUMN balancesheet.minority_int IS '少数股东权益';
COMMENT ON COLUMN balancesheet.total_liab_hldr_eqy IS '负债';
COMMENT ON COLUMN balancesheet.lt_payroll_payable IS '应付';
COMMENT ON COLUMN balancesheet.oth_comp_income IS '收入';
COMMENT ON COLUMN balancesheet.acc_receivable IS '应收';
COMMENT ON COLUMN balancesheet.st_fin_payable IS '应付';
COMMENT ON COLUMN balancesheet.payables IS '应付';
COMMENT ON COLUMN balancesheet.hfs_assets IS '资产';
COMMENT ON COLUMN balancesheet.cost_fin_assets IS '资产';
COMMENT ON COLUMN balancesheet.fair_value_fin_assets IS '资产';
COMMENT ON COLUMN balancesheet.oth_pay_total IS '应付';
COMMENT ON COLUMN balancesheet.long_pay_total IS '应付';
COMMENT ON COLUMN balancesheet.oth_illiq_fin_assets IS '资产';
COMMENT ON COLUMN balancesheet.receiv_financing IS '应收';
COMMENT ON COLUMN balancesheet.use_right_assets IS '使用权资产';
COMMENT ON COLUMN balancesheet.lease_liab IS '租赁负债';
COMMENT ON COLUMN balancesheet.contract_assets IS '合同资产';
COMMENT ON COLUMN balancesheet.contract_liab IS '合同负债';
COMMENT ON COLUMN balancesheet.accounts_receiv_bill IS '应收';
COMMENT ON COLUMN balancesheet.accounts_pay IS '应付';
COMMENT ON COLUMN balancesheet.fix_assets_total IS '资产';
COMMENT ON COLUMN balancesheet.update_flag IS '更新标识';

-- 索引
CREATE INDEX IF NOT EXISTS idx_balancesheet_date ON balancesheet(end_date);
CREATE INDEX IF NOT EXISTS idx_balancesheet_code ON balancesheet(ts_code);
CREATE INDEX IF NOT EXISTS idx_balancesheet_ann_date ON balancesheet(ann_date);
