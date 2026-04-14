-- balancesheet (资产负债表)
-- API接口: balancesheet
-- API字段数: 158


CREATE TABLE IF NOT EXISTS balancesheet (
    ts_code VARCHAR(20),  -- TS股票代码
    ann_date DATE,  -- 公告日期
    f_ann_date DATE,  -- 实际公告日期
    end_date DATE,  -- 报告期
    report_type VARCHAR(20),  -- 报表类型
    comp_type VARCHAR(20),  -- 公司类型(1一般工商业2银行3保险4证券)
    end_type VARCHAR(20),  -- 报告期类型
    total_share REAL,  -- 期末总股本
    cap_rese REAL,  -- 资本公积金
    undistr_porfit REAL,  -- 未分配利润
    surplus_rese REAL,  -- 盈余公积金
    special_rese REAL,  -- 专项储备
    money_cap REAL,  -- 货币资金
    trad_asset REAL,  -- 交易性金融资产
    notes_receiv REAL,  -- 应收票据
    accounts_receiv INTEGER,  -- 应收账款
    oth_receiv REAL,  -- 其他应收款
    prepayment REAL,  -- 预付款项
    div_receiv REAL,  -- 应收股利
    int_receiv REAL,  -- 应收利息
    inventories REAL,  -- 存货
    amor_exp REAL,  -- 待摊费用
    nca_within_1y REAL,  -- 一年内到期的非流动资产
    sett_rsrv REAL,  -- 结算备付金
    loanto_oth_bank_fi REAL,  -- 拆出资金
    premium_receiv REAL,  -- 应收保费
    reinsur_receiv REAL,  -- 应收分保账款
    reinsur_res_receiv REAL,  -- 应收分保合同准备金
    pur_resale_fa REAL,  -- 买入返售金融资产
    oth_cur_assets REAL,  -- 其他流动资产
    total_cur_assets REAL,  -- 流动资产合计
    fa_avail_for_sale REAL,  -- 可供出售金融资产
    htm_invest REAL,  -- 持有至到期投资
    lt_eqt_invest REAL,  -- 长期股权投资
    invest_real_estate REAL,  -- 投资性房地产
    time_deposits REAL,  -- 定期存款
    oth_assets REAL,  -- 其他资产
    lt_rec REAL,  -- 长期应收款
    fix_assets REAL,  -- 固定资产
    cip REAL,  -- 在建工程
    const_materials REAL,  -- 工程物资
    fixed_assets_disp REAL,  -- 固定资产清理
    produc_bio_assets REAL,  -- 生产性生物资产
    oil_and_gas_assets REAL,  -- 油气资产
    intan_assets REAL,  -- 无形资产
    r_and_d REAL,  -- 研发支出
    goodwill REAL,  -- 商誉
    lt_amor_exp REAL,  -- 长期待摊费用
    defer_tax_assets REAL,  -- 递延所得税资产
    decr_in_disbur REAL,  -- 发放贷款及垫款
    oth_nca REAL,  -- 其他非流动资产
    total_nca REAL,  -- 非流动资产合计
    cash_reser_cb REAL,  -- 现金及存放中央银行款项
    depos_in_oth_bfi REAL,  -- 存放同业和其它金融机构款项
    prec_metals REAL,  -- 贵金属
    deriv_assets REAL,  -- 衍生金融资产
    rr_reins_une_prem REAL,  -- 应收分保未到期责任准备金
    rr_reins_outstd_cla REAL,  -- 应收分保未决赔款准备金
    rr_reins_lins_liab REAL,  -- 应收分保寿险责任准备金
    rr_reins_lthins_liab REAL,  -- 应收分保长期健康险责任准备金
    refund_depos REAL,  -- 存出保证金
    ph_pledge_loans REAL,  -- 保户质押贷款
    refund_cap_depos REAL,  -- 存出资本保证金
    indep_acct_assets REAL,  -- 独立账户资产
    client_depos REAL,  -- 其中：客户资金存款
    client_prov REAL,  -- 其中：客户备付金
    transac_seat_fee REAL,  -- 其中:交易席位费
    invest_as_receiv REAL,  -- 应收款项类投资
    total_assets REAL,  -- 资产总计
    lt_borr REAL,  -- 长期借款
    st_borr REAL,  -- 短期借款
    cb_borr REAL,  -- 向中央银行借款
    depos_ib_deposits REAL,  -- 吸收存款及同业存放
    loan_oth_bank REAL,  -- 拆入资金
    trading_fl REAL,  -- 交易性金融负债
    notes_payable REAL,  -- 应付票据
    acct_payable REAL,  -- 应付账款
    adv_receipts REAL,  -- 预收款项
    sold_for_repur_fa REAL,  -- 卖出回购金融资产款
    comm_payable REAL,  -- 应付手续费及佣金
    payroll_payable REAL,  -- 应付职工薪酬
    taxes_payable REAL,  -- 应交税费
    int_payable REAL,  -- 应付利息
    div_payable REAL,  -- 应付股利
    oth_payable REAL,  -- 其他应付款
    acc_exp REAL,  -- 预提费用
    deferred_inc REAL,  -- 递延收益
    st_bonds_payable REAL,  -- 应付短期债券
    payable_to_reinsurer REAL,  -- 应付分保账款
    rsrv_insur_cont REAL,  -- 保险合同准备金
    acting_trading_sec REAL,  -- 代理买卖证券款
    acting_uw_sec REAL,  -- 代理承销证券款
    non_cur_liab_due_1y REAL,  -- 一年内到期的非流动负债
    oth_cur_liab REAL,  -- 其他流动负债
    total_cur_liab REAL,  -- 流动负债合计
    bond_payable REAL,  -- 应付债券
    lt_payable REAL,  -- 长期应付款
    specific_payables REAL,  -- 专项应付款
    estimated_liab REAL,  -- 预计负债
    defer_tax_liab REAL,  -- 递延所得税负债
    defer_inc_non_cur_liab REAL,  -- 递延收益-非流动负债
    oth_ncl REAL,  -- 其他非流动负债
    total_ncl REAL,  -- 非流动负债合计
    depos_oth_bfi REAL,  -- 同业和其它金融机构存放款项
    deriv_liab REAL,  -- 衍生金融负债
    depos REAL,  -- 吸收存款
    agency_bus_liab REAL,  -- 代理业务负债
    oth_liab REAL,  -- 其他负债
    prem_receiv_adva REAL,  -- 预收保费
    depos_received REAL,  -- 存入保证金
    ph_invest REAL,  -- 保户储金及投资款
    reser_une_prem REAL,  -- 未到期责任准备金
    reser_outstd_claims REAL,  -- 未决赔款准备金
    reser_lins_liab REAL,  -- 寿险责任准备金
    reser_lthins_liab REAL,  -- 长期健康险责任准备金
    indept_acc_liab REAL,  -- 独立账户负债
    pledge_borr REAL,  -- 其中:质押借款
    indem_payable REAL,  -- 应付赔付款
    policy_div_payable REAL,  -- 应付保单红利
    total_liab REAL,  -- 负债合计
    treasury_share REAL,  -- 减:库存股
    ordin_risk_reser REAL,  -- 一般风险准备
    forex_differ REAL,  -- 外币报表折算差额
    invest_loss_unconf REAL,  -- 未确认的投资损失
    minority_int REAL,  -- 少数股东权益
    total_hldr_eqy_exc_min_int REAL,  -- 股东权益合计(不含少数股东权益)
    total_hldr_eqy_inc_min_int REAL,  -- 股东权益合计(含少数股东权益)
    total_liab_hldr_eqy REAL,  -- 负债及股东权益总计
    lt_payroll_payable REAL,  -- 长期应付职工薪酬
    oth_comp_income REAL,  -- 其他综合收益
    oth_eqt_tools REAL,  -- 其他权益工具
    oth_eqt_tools_p_shr REAL,  -- 其他权益工具(优先股)
    lending_funds REAL,  -- 融出资金
    acc_receivable REAL,  -- 应收款项
    st_fin_payable REAL,  -- 应付短期融资款
    payables REAL,  -- 应付款项
    hfs_assets REAL,  -- 持有待售的资产
    hfs_sales REAL,  -- 持有待售的负债
    cost_fin_assets REAL,  -- 以摊余成本计量的金融资产
    fair_value_fin_assets REAL,  -- 以公允价值计量且其变动计入其他综合收益的金融资产
    cip_total REAL,  -- 在建工程(合计)(元)
    oth_pay_total REAL,  -- 其他应付款(合计)(元)
    long_pay_total REAL,  -- 长期应付款(合计)(元)
    debt_invest REAL,  -- 债权投资(元)
    oth_debt_invest REAL,  -- 其他债权投资(元)
    oth_eq_invest REAL,  -- 其他权益工具投资(元)
    oth_illiq_fin_assets REAL,  -- 其他非流动金融资产(元)
    oth_eq_ppbond REAL,  -- 其他权益工具:永续债(元)
    receiv_financing REAL,  -- 应收款项融资
    use_right_assets REAL,  -- 使用权资产
    lease_liab REAL,  -- 租赁负债
    contract_assets REAL,  -- 合同资产
    contract_liab REAL,  -- 合同负债
    accounts_receiv_bill INTEGER,  -- 应收票据及应收账款
    accounts_pay INTEGER,  -- 应付票据及应付账款
    oth_rcv_total REAL,  -- 其他应收款(合计)（元）
    fix_assets_total REAL,  -- 固定资产(合计)(元)
    update_flag VARCHAR(100),  -- 更新标识
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE balancesheet ADD PRIMARY KEY (ts_code, end_date, report_type);


-- 索引
CREATE INDEX IF NOT EXISTS idx_balancesheet_date ON balancesheet(end_date);
CREATE INDEX IF NOT EXISTS idx_balancesheet_code ON balancesheet(ts_code);
CREATE INDEX IF NOT EXISTS idx_balancesheet_ann_date ON balancesheet(ann_date);
