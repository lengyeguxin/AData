-- fina_indicator (财务指标)
-- API接口: fina_indicator
-- API字段数: 167

CREATE TABLE IF NOT EXISTS fina_indicator (
    ts_code VARCHAR(20),  -- TS代码
    ann_date DATE,  -- 公告日期
    end_date DATE,  -- 报告期
    eps REAL,  -- 基本每股收益
    dt_eps REAL,  -- 稀释每股收益
    total_revenue_ps REAL,  -- 每股营业总收入
    revenue_ps REAL,  -- 每股营业收入
    capital_rese_ps REAL,  -- 每股资本公积
    surplus_rese_ps REAL,  -- 每股盈余公积
    undist_profit_ps REAL,  -- 每股未分配利润
    extra_item REAL,  -- 非经常性损益
    profit_dedt REAL,  -- 扣除非经常性损益后的净利润（扣非净利润）
    gross_margin REAL,  -- 毛利
    current_ratio REAL,  -- 流动比率
    quick_ratio REAL,  -- 速动比率
    cash_ratio REAL,  -- 保守速动比率
    invturn_days REAL,  -- 存货周转天数
    arturn_days REAL,  -- 应收账款周转天数
    inv_turn REAL,  -- 存货周转率
    ar_turn REAL,  -- 应收账款周转率
    ca_turn REAL,  -- 流动资产周转率
    fa_turn REAL,  -- 固定资产周转率
    assets_turn REAL,  -- 总资产周转率
    op_income REAL,  -- 经营活动净收益
    valuechange_income REAL,  -- 价值变动净收益
    interst_income REAL,  -- 利息费用
    daa REAL,  -- 折旧与摊销
    ebit REAL,  -- 息税前利润
    ebitda REAL,  -- 息税折旧摊销前利润
    fcff REAL,  -- 企业自由现金流量
    fcfe REAL,  -- 股权自由现金流量
    current_exint REAL,  -- 无息流动负债
    noncurrent_exint REAL,  -- 无息非流动负债
    interestdebt REAL,  -- 带息债务
    netdebt REAL,  -- 净债务
    tangible_asset REAL,  -- 有形资产
    working_capital REAL,  -- 营运资金
    networking_capital REAL,  -- 营运流动资本
    invest_capital REAL,  -- 全部投入资本
    retained_earnings REAL,  -- 留存收益
    diluted2_eps REAL,  -- 期末摊薄每股收益
    bps REAL,  -- 每股净资产
    ocfps REAL,  -- 每股经营活动产生的现金流量净额
    retainedps REAL,  -- 每股留存收益
    cfps REAL,  -- 每股现金流量净额
    ebit_ps REAL,  -- 每股息税前利润
    fcff_ps REAL,  -- 每股企业自由现金流量
    fcfe_ps REAL,  -- 每股股东自由现金流量
    netprofit_margin REAL,  -- 销售净利率
    grossprofit_margin REAL,  -- 销售毛利率
    cogs_of_sales REAL,  -- 销售成本率
    expense_of_sales REAL,  -- 销售期间费用率
    profit_to_gr REAL,  -- 净利润/营业总收入
    saleexp_to_gr REAL,  -- 销售费用/营业总收入
    adminexp_of_gr REAL,  -- 管理费用/营业总收入
    finaexp_of_gr REAL,  -- 财务费用/营业总收入
    impai_ttm REAL,  -- 资产减值损失/营业总收入
    gc_of_gr REAL,  -- 营业总成本/营业总收入
    op_of_gr REAL,  -- 营业利润/营业总收入
    ebit_of_gr REAL,  -- 息税前利润/营业总收入
    roe REAL,  -- 净资产收益率
    roe_waa REAL,  -- 加权平均净资产收益率
    roe_dt REAL,  -- 净资产收益率(扣除非经常损益)
    roa REAL,  -- 总资产报酬率
    npta REAL,  -- 总资产净利润
    roic REAL,  -- 投入资本回报率
    roe_yearly REAL,  -- 年化净资产收益率
    roa2_yearly REAL,  -- 年化总资产报酬率
    roe_avg REAL,  -- 平均净资产收益率(增发条件)
    opincome_of_ebt REAL,  -- 经营活动净收益/利润总额
    investincome_of_ebt REAL,  -- 价值变动净收益/利润总额
    n_op_profit_of_ebt REAL,  -- 营业外收支净额/利润总额
    tax_to_ebt REAL,  -- 所得税/利润总额
    dtprofit_to_profit REAL,  -- 扣除非经常损益后的净利润/净利润
    salescash_to_or REAL,  -- 销售商品提供劳务收到的现金/营业收入
    ocf_to_or REAL,  -- 经营活动产生的现金流量净额/营业收入
    ocf_to_opincome REAL,  -- 经营活动产生的现金流量净额/经营活动净收益
    capitalized_to_da REAL,  -- 资本支出/折旧和摊销
    debt_to_assets REAL,  -- 资产负债率
    assets_to_eqt REAL,  -- 权益乘数
    dp_assets_to_eqt REAL,  -- 权益乘数(杜邦分析)
    ca_to_assets REAL,  -- 流动资产/总资产
    nca_to_assets REAL,  -- 非流动资产/总资产
    tbassets_to_totalassets REAL,  -- 有形资产/总资产
    int_to_talcap REAL,  -- 带息债务/全部投入资本
    eqt_to_talcapital REAL,  -- 归属于母公司的股东权益/全部投入资本
    currentdebt_to_debt REAL,  -- 流动负债/负债合计
    longdeb_to_debt REAL,  -- 非流动负债/负债合计
    ocf_to_shortdebt REAL,  -- 经营活动产生的现金流量净额/流动负债
    debt_to_eqt REAL,  -- 产权比率
    eqt_to_debt REAL,  -- 归属于母公司的股东权益/负债合计
    eqt_to_interestdebt REAL,  -- 归属于母公司的股东权益/带息债务
    tangibleasset_to_debt REAL,  -- 有形资产/负债合计
    tangasset_to_intdebt REAL,  -- 有形资产/带息债务
    tangibleasset_to_netdebt REAL,  -- 有形资产/净债务
    ocf_to_debt REAL,  -- 经营活动产生的现金流量净额/负债合计
    ocf_to_interestdebt REAL,  -- 经营活动产生的现金流量净额/带息债务
    ocf_to_netdebt REAL,  -- 经营活动产生的现金流量净额/净债务
    ebit_to_interest REAL,  -- 已获利息倍数(EBIT/利息费用)
    longdebt_to_workingcapital REAL,  -- 长期债务与营运资金比率
    ebitda_to_debt REAL,  -- 息税折旧摊销前利润/负债合计
    turn_days REAL,  -- 营业周期
    roa_yearly REAL,  -- 年化总资产净利率
    roa_dp REAL,  -- 总资产净利率(杜邦分析)
    fixed_assets REAL,  -- 固定资产合计
    profit_prefin_exp REAL,  -- 扣除财务费用前营业利润
    non_op_profit REAL,  -- 非营业利润
    op_to_ebt REAL,  -- 营业利润／利润总额
    nop_to_ebt REAL,  -- 非营业利润／利润总额
    ocf_to_profit REAL,  -- 经营活动产生的现金流量净额／营业利润
    cash_to_liqdebt REAL,  -- 货币资金／流动负债
    cash_to_liqdebt_withinterest REAL,  -- 货币资金／带息流动负债
    op_to_liqdebt REAL,  -- 营业利润／流动负债
    op_to_debt REAL,  -- 营业利润／负债合计
    roic_yearly REAL,  -- 年化投入资本回报率
    total_fa_trun REAL,  -- 固定资产合计周转率
    profit_to_op REAL,  -- 利润总额／营业收入
    q_opincome REAL,  -- 经营活动单季度净收益
    q_investincome REAL,  -- 价值变动单季度净收益
    q_dtprofit REAL,  -- 扣除非经常损益后的单季度净利润
    q_eps REAL,  -- 每股收益(单季度)
    q_netprofit_margin REAL,  -- 销售净利率(单季度)
    q_gsprofit_margin REAL,  -- 销售毛利率(单季度)
    q_exp_to_sales REAL,  -- 销售期间费用率(单季度)
    q_profit_to_gr REAL,  -- 净利润／营业总收入(单季度)
    q_saleexp_to_gr REAL,  -- 销售费用／营业总收入 (单季度)
    q_adminexp_to_gr REAL,  -- 管理费用／营业总收入 (单季度)
    q_finaexp_to_gr REAL,  -- 财务费用／营业总收入 (单季度)
    q_impair_to_gr_ttm REAL,  -- 资产减值损失／营业总收入(单季度)
    q_gc_to_gr REAL,  -- 营业总成本／营业总收入 (单季度)
    q_op_to_gr REAL,  -- 营业利润／营业总收入(单季度)
    q_roe REAL,  -- 净资产收益率(单季度)
    q_dt_roe REAL,  -- 净资产单季度收益率(扣除非经常损益)
    q_npta REAL,  -- 总资产净利润(单季度)
    q_opincome_to_ebt REAL,  -- 经营活动净收益／利润总额(单季度)
    q_investincome_to_ebt REAL,  -- 价值变动净收益／利润总额(单季度)
    q_dtprofit_to_profit REAL,  -- 扣除非经常损益后的净利润／净利润(单季度)
    q_salescash_to_or REAL,  -- 销售商品提供劳务收到的现金／营业收入(单季度)
    q_ocf_to_sales REAL,  -- 经营活动产生的现金流量净额／营业收入(单季度)
    q_ocf_to_or REAL,  -- 经营活动产生的现金流量净额／经营活动净收益(单季度)
    basic_eps_yoy REAL,  -- 基本每股收益同比增长率(%)
    dt_eps_yoy REAL,  -- 稀释每股收益同比增长率(%)
    cfps_yoy REAL,  -- 每股经营活动产生的现金流量净额同比增长率(%)
    op_yoy REAL,  -- 营业利润同比增长率(%)
    ebt_yoy REAL,  -- 利润总额同比增长率(%)
    netprofit_yoy REAL,  -- 归属母公司股东的净利润同比增长率(%)
    dt_netprofit_yoy REAL,  -- 归属母公司股东的净利润-扣除非经常损益同比增长率(%)
    ocf_yoy REAL,  -- 经营活动产生的现金流量净额同比增长率(%)
    roe_yoy REAL,  -- 净资产收益率(摊薄)同比增长率(%)
    bps_yoy REAL,  -- 每股净资产相对年初增长率(%)
    assets_yoy REAL,  -- 资产总计相对年初增长率(%)
    eqt_yoy REAL,  -- 归属母公司的股东权益相对年初增长率(%)
    tr_yoy REAL,  -- 营业总收入同比增长率(%)
    or_yoy REAL,  -- 营业收入同比增长率(%)
    q_gr_yoy REAL,  -- 营业总收入同比增长率(%)(单季度)
    q_gr_qoq REAL,  -- 营业总收入环比增长率(%)(单季度)
    q_sales_yoy REAL,  -- 营业收入同比增长率(%)(单季度)
    q_sales_qoq REAL,  -- 营业收入环比增长率(%)(单季度)
    q_op_yoy REAL,  -- 营业利润同比增长率(%)(单季度)
    q_op_qoq REAL,  -- 营业利润环比增长率(%)(单季度)
    q_profit_yoy REAL,  -- 净利润同比增长率(%)(单季度)
    q_profit_qoq REAL,  -- 净利润环比增长率(%)(单季度)
    q_netprofit_yoy REAL,  -- 归属母公司股东的净利润同比增长率(%)(单季度)
    q_netprofit_qoq REAL,  -- 归属母公司股东的净利润环比增长率(%)(单季度)
    equity_yoy REAL,  -- 净资产同比增长率
    rd_exp REAL,  -- 研发费用
    update_flag VARCHAR(100),  -- 更新标识
    updated_at TIMESTAMP DEFAULT NOW(),  -- 更新时间
    PRIMARY KEY (ts_code, end_date)
);



-- 索引
CREATE INDEX IF NOT EXISTS idx_fina_indicator_date ON fina_indicator(end_date);
CREATE INDEX IF NOT EXISTS idx_fina_indicator_code ON fina_indicator(ts_code);
CREATE INDEX IF NOT EXISTS idx_fina_indicator_ann_date ON fina_indicator(ann_date);
