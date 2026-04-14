-- cashflow (现金流量表)
-- API接口: cashflow
-- API字段数: 97


CREATE TABLE IF NOT EXISTS cashflow (
    ts_code VARCHAR(20),  -- TS股票代码
    ann_date DATE,  -- 公告日期
    f_ann_date DATE,  -- 实际公告日期
    end_date DATE,  -- 报告期
    comp_type VARCHAR(20),  -- 公司类型(1一般工商业2银行3保险4证券)
    report_type VARCHAR(20),  -- 报表类型
    end_type VARCHAR(20),  -- 报告期类型
    net_profit REAL,  -- 净利润
    finan_exp REAL,  -- 财务费用
    c_fr_sale_sg REAL,  -- 销售商品、提供劳务收到的现金
    recp_tax_rends REAL,  -- 收到的税费返还
    n_depos_incr_fi REAL,  -- 客户存款和同业存放款项净增加额
    n_incr_loans_cb REAL,  -- 向中央银行借款净增加额
    n_inc_borr_oth_fi REAL,  -- 向其他金融机构拆入资金净增加额
    prem_fr_orig_contr REAL,  -- 收到原保险合同保费取得的现金
    n_incr_insured_dep REAL,  -- 保户储金净增加额
    n_reinsur_prem REAL,  -- 收到再保业务现金净额
    n_incr_disp_tfa REAL,  -- 处置交易性金融资产净增加额
    ifc_cash_incr REAL,  -- 收取利息和手续费净增加额
    n_incr_disp_faas REAL,  -- 处置可供出售金融资产净增加额
    n_incr_loans_oth_bank REAL,  -- 拆入资金净增加额
    n_cap_incr_repur REAL,  -- 回购业务资金净增加额
    c_fr_oth_operate_a REAL,  -- 收到其他与经营活动有关的现金
    c_inf_fr_operate_a REAL,  -- 经营活动现金流入小计
    c_paid_goods_s REAL,  -- 购买商品、接受劳务支付的现金
    c_paid_to_for_empl REAL,  -- 支付给职工以及为职工支付的现金
    c_paid_for_taxes REAL,  -- 支付的各项税费
    n_incr_clt_loan_adv REAL,  -- 客户贷款及垫款净增加额
    n_incr_dep_cbob REAL,  -- 存放央行和同业款项净增加额
    c_pay_claims_orig_inco REAL,  -- 支付原保险合同赔付款项的现金
    pay_handling_chrg REAL,  -- 支付手续费的现金
    pay_comm_insur_plcy REAL,  -- 支付保单红利的现金
    oth_cash_pay_oper_act REAL,  -- 支付其他与经营活动有关的现金
    st_cash_out_act REAL,  -- 经营活动现金流出小计
    n_cashflow_act REAL,  -- 经营活动产生的现金流量净额
    oth_recp_ral_inv_act REAL,  -- 收到其他与投资活动有关的现金
    c_disp_withdrwl_invest REAL,  -- 收回投资收到的现金
    c_recp_return_invest REAL,  -- 取得投资收益收到的现金
    n_recp_disp_fiolta REAL,  -- 处置固定资产、无形资产和其他长期资产收回的现金净额
    n_recp_disp_sobu REAL,  -- 处置子公司及其他营业单位收到的现金净额
    stot_inflows_inv_act REAL,  -- 投资活动现金流入小计
    c_pay_acq_const_fiolta REAL,  -- 购建固定资产、无形资产和其他长期资产支付的现金
    c_paid_invest REAL,  -- 投资支付的现金
    n_disp_subs_oth_biz REAL,  -- 取得子公司及其他营业单位支付的现金净额
    oth_pay_ral_inv_act REAL,  -- 支付其他与投资活动有关的现金
    n_incr_pledge_loan REAL,  -- 质押贷款净增加额
    stot_out_inv_act REAL,  -- 投资活动现金流出小计
    n_cashflow_inv_act REAL,  -- 投资活动产生的现金流量净额
    c_recp_borrow REAL,  -- 取得借款收到的现金
    proc_issue_bonds REAL,  -- 发行债券收到的现金
    oth_cash_recp_ral_fnc_act REAL,  -- 收到其他与筹资活动有关的现金
    stot_cash_in_fnc_act REAL,  -- 筹资活动现金流入小计
    free_cashflow REAL,  -- 企业自由现金流量
    c_prepay_amt_borr REAL,  -- 偿还债务支付的现金
    c_pay_dist_dpcp_int_exp REAL,  -- 分配股利、利润或偿付利息支付的现金
    incl_dvd_profit_paid_sc_ms REAL,  -- 其中:子公司支付给少数股东的股利、利润
    oth_cashpay_ral_fnc_act REAL,  -- 支付其他与筹资活动有关的现金
    stot_cashout_fnc_act REAL,  -- 筹资活动现金流出小计
    n_cash_flows_fnc_act REAL,  -- 筹资活动产生的现金流量净额
    eff_fx_flu_cash REAL,  -- 汇率变动对现金的影响
    n_incr_cash_cash_equ REAL,  -- 现金及现金等价物净增加额
    c_cash_equ_beg_period REAL,  -- 期初现金及现金等价物余额
    c_cash_equ_end_period REAL,  -- 期末现金及现金等价物余额
    c_recp_cap_contrib REAL,  -- 吸收投资收到的现金
    incl_cash_rec_saims REAL,  -- 其中:子公司吸收少数股东投资收到的现金
    uncon_invest_loss REAL,  -- 未确认投资损失
    prov_depr_assets REAL,  -- 加:资产减值准备
    depr_fa_coga_dpba REAL,  -- 固定资产折旧、油气资产折耗、生产性生物资产折旧
    amort_intang_assets REAL,  -- 无形资产摊销
    lt_amort_deferred_exp REAL,  -- 长期待摊费用摊销
    decr_deferred_exp REAL,  -- 待摊费用减少
    incr_acc_exp REAL,  -- 预提费用增加
    loss_disp_fiolta REAL,  -- 处置固定、无形资产和其他长期资产的损失
    loss_scr_fa REAL,  -- 固定资产报废损失
    loss_fv_chg REAL,  -- 公允价值变动损失
    invest_loss REAL,  -- 投资损失
    decr_def_inc_tax_assets REAL,  -- 递延所得税资产减少
    incr_def_inc_tax_liab REAL,  -- 递延所得税负债增加
    decr_inventories REAL,  -- 存货的减少
    decr_oper_payable REAL,  -- 经营性应收项目的减少
    incr_oper_payable REAL,  -- 经营性应付项目的增加
    others REAL,  -- 其他
    im_net_cashflow_oper_act REAL,  -- 经营活动产生的现金流量净额(间接法)
    conv_debt_into_cap REAL,  -- 债务转为资本
    conv_copbonds_due_within_1y REAL,  -- 一年内到期的可转换公司债券
    fa_fnc_leases REAL,  -- 融资租入固定资产
    im_n_incr_cash_equ REAL,  -- 现金及现金等价物净增加额(间接法)
    net_dism_capital_add REAL,  -- 拆出资金净增加额
    net_cash_rece_sec REAL,  -- 代理买卖证券收到的现金净额(元)
    credit_impa_loss REAL,  -- 信用减值损失
    use_right_asset_dep REAL,  -- 使用权资产折旧
    oth_loss_asset REAL,  -- 其他资产减值损失
    end_bal_cash REAL,  -- 现金的期末余额
    beg_bal_cash REAL,  -- 减:现金的期初余额
    end_bal_cash_equ REAL,  -- 加:现金等价物的期末余额
    beg_bal_cash_equ REAL,  -- 减:现金等价物的期初余额
    update_flag VARCHAR(100),  -- 更新标志(1最新）
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE cashflow ADD PRIMARY KEY (ts_code, end_date, report_type);


-- 索引
CREATE INDEX IF NOT EXISTS idx_cashflow_date ON cashflow(end_date);
CREATE INDEX IF NOT EXISTS idx_cashflow_code ON cashflow(ts_code);
CREATE INDEX IF NOT EXISTS idx_cashflow_ann_date ON cashflow(ann_date);
