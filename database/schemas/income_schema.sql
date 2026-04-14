-- income (利润表)
-- API接口: income
-- API字段数: 94


CREATE TABLE IF NOT EXISTS income (
    ts_code VARCHAR(20),  -- TS代码
    ann_date DATE,  -- 公告日期
    f_ann_date DATE,  -- 实际公告日期
    end_date DATE,  -- 报告期
    report_type VARCHAR(20),  -- 报告类型 见底部表
    comp_type VARCHAR(20),  -- 公司类型(1一般工商业2银行3保险4证券)
    end_type VARCHAR(20),  -- 报告期类型
    basic_eps REAL,  -- 基本每股收益
    diluted_eps REAL,  -- 稀释每股收益
    total_revenue REAL,  -- 营业总收入
    revenue REAL,  -- 营业收入
    int_income REAL,  -- 利息收入
    prem_earned REAL,  -- 已赚保费
    comm_income REAL,  -- 手续费及佣金收入
    n_commis_income REAL,  -- 手续费及佣金净收入
    n_oth_income REAL,  -- 其他经营净收益
    n_oth_b_income REAL,  -- 加:其他业务净收益
    prem_income REAL,  -- 保险业务收入
    out_prem REAL,  -- 减:分出保费
    une_prem_reser REAL,  -- 提取未到期责任准备金
    reins_income REAL,  -- 其中:分保费收入
    n_sec_tb_income REAL,  -- 代理买卖证券业务净收入
    n_sec_uw_income REAL,  -- 证券承销业务净收入
    n_asset_mg_income REAL,  -- 受托客户资产管理业务净收入
    oth_b_income REAL,  -- 其他业务收入
    fv_value_chg_gain REAL,  -- 加:公允价值变动净收益
    invest_income REAL,  -- 加:投资净收益
    ass_invest_income REAL,  -- 其中:对联营企业和合营企业的投资收益
    forex_gain REAL,  -- 加:汇兑净收益
    total_cogs REAL,  -- 营业总成本
    oper_cost REAL,  -- 减:营业成本
    int_exp REAL,  -- 减:利息支出
    comm_exp REAL,  -- 减:手续费及佣金支出
    biz_tax_surchg REAL,  -- 减:营业税金及附加
    sell_exp REAL,  -- 减:销售费用
    admin_exp REAL,  -- 减:管理费用
    fin_exp REAL,  -- 减:财务费用
    assets_impair_loss REAL,  -- 减:资产减值损失
    prem_refund REAL,  -- 退保金
    compens_payout REAL,  -- 赔付总支出
    reser_insur_liab REAL,  -- 提取保险责任准备金
    div_payt REAL,  -- 保户红利支出
    reins_exp REAL,  -- 分保费用
    oper_exp REAL,  -- 营业支出
    compens_payout_refu REAL,  -- 减:摊回赔付支出
    insur_reser_refu REAL,  -- 减:摊回保险责任准备金
    reins_cost_refund REAL,  -- 减:摊回分保费用
    other_bus_cost REAL,  -- 其他业务成本
    operate_profit REAL,  -- 营业利润
    non_oper_income REAL,  -- 加:营业外收入
    non_oper_exp REAL,  -- 减:营业外支出
    nca_disploss REAL,  -- 其中:减:非流动资产处置净损失
    total_profit REAL,  -- 利润总额
    income_tax REAL,  -- 所得税费用
    n_income REAL,  -- 净利润(含少数股东损益)
    n_income_attr_p REAL,  -- 净利润(不含少数股东损益)
    minority_gain REAL,  -- 少数股东损益
    oth_compr_income REAL,  -- 其他综合收益
    t_compr_income REAL,  -- 综合收益总额
    compr_inc_attr_p REAL,  -- 归属于母公司(或股东)的综合收益总额
    compr_inc_attr_m_s REAL,  -- 归属于少数股东的综合收益总额
    ebit REAL,  -- 息税前利润
    ebitda REAL,  -- 息税折旧摊销前利润
    insurance_exp REAL,  -- 保险业务支出
    undist_profit REAL,  -- 年初未分配利润
    distable_profit REAL,  -- 可分配利润
    rd_exp REAL,  -- 研发费用
    fin_exp_int_exp REAL,  -- 财务费用:利息费用
    fin_exp_int_inc REAL,  -- 财务费用:利息收入
    transfer_surplus_rese REAL,  -- 盈余公积转入
    transfer_housing_imprest REAL,  -- 住房周转金转入
    transfer_oth REAL,  -- 其他转入
    adj_lossgain REAL,  -- 调整以前年度损益
    withdra_legal_surplus REAL,  -- 提取法定盈余公积
    withdra_legal_pubfund REAL,  -- 提取法定公益金
    withdra_biz_devfund REAL,  -- 提取企业发展基金
    withdra_rese_fund REAL,  -- 提取储备基金
    withdra_oth_ersu REAL,  -- 提取任意盈余公积金
    workers_welfare REAL,  -- 职工奖金福利
    distr_profit_shrhder REAL,  -- 可供股东分配的利润
    prfshare_payable_dvd REAL,  -- 应付优先股股利
    comshare_payable_dvd REAL,  -- 应付普通股股利
    capit_comstock_div REAL,  -- 转作股本的普通股股利
    net_after_nr_lp_correct REAL,  -- 扣除非经常性损益后的净利润（更正前）
    credit_impa_loss REAL,  -- 信用减值损失
    net_expo_hedging_benefits REAL,  -- 净敞口套期收益
    oth_impair_loss_assets REAL,  -- 其他资产减值损失
    total_opcost REAL,  -- 营业总成本（二）
    amodcost_fin_assets REAL,  -- 以摊余成本计量的金融资产终止确认收益
    oth_income REAL,  -- 其他收益
    asset_disp_income REAL,  -- 资产处置收益
    continued_net_profit REAL,  -- 持续经营净利润
    end_net_profit REAL,  -- 终止经营净利润
    update_flag VARCHAR(100),  -- 更新标识
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键


-- 索引
CREATE INDEX IF NOT EXISTS idx_income_date ON income(end_date);
CREATE INDEX IF NOT EXISTS idx_income_code ON income(ts_code);
CREATE INDEX IF NOT EXISTS idx_income_ann_date ON income(ann_date);
