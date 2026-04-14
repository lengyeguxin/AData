-- fina_indicator (财务指标)
-- API接口: fina_indicator
-- API字段数: 167

COMMENT ON TABLE fina_indicator IS '财务指标';

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
    updated_at TIMESTAMP DEFAULT NOW()  -- 更新时间
);

-- 复合主键
ALTER TABLE fina_indicator ADD PRIMARY KEY (ts_code, end_date);

COMMENT ON COLUMN fina_indicator.ts_code IS 'TS代码';
COMMENT ON COLUMN fina_indicator.ann_date IS '公告日期';
COMMENT ON COLUMN fina_indicator.end_date IS '报告期';
COMMENT ON COLUMN fina_indicator.eps IS '基本每股收益';
COMMENT ON COLUMN fina_indicator.dt_eps IS '稀释每股收益';
COMMENT ON COLUMN fina_indicator.total_revenue_ps IS '每股营业总收入';
COMMENT ON COLUMN fina_indicator.revenue_ps IS '每股营业收入';
COMMENT ON COLUMN fina_indicator.capital_rese_ps IS '每股资本公积';
COMMENT ON COLUMN fina_indicator.surplus_rese_ps IS '每股盈余公积';
COMMENT ON COLUMN fina_indicator.undist_profit_ps IS '每股未分配利润';
COMMENT ON COLUMN fina_indicator.extra_item IS '非经常性损益';
COMMENT ON COLUMN fina_indicator.profit_dedt IS '扣除非经常性损益后的净利润（扣非净利润）';
COMMENT ON COLUMN fina_indicator.gross_margin IS '毛利';
COMMENT ON COLUMN fina_indicator.current_ratio IS '流动比率';
COMMENT ON COLUMN fina_indicator.quick_ratio IS '速动比率';
COMMENT ON COLUMN fina_indicator.cash_ratio IS '保守速动比率';
COMMENT ON COLUMN fina_indicator.invturn_days IS '存货周转天数';
COMMENT ON COLUMN fina_indicator.arturn_days IS '应收账款周转天数';
COMMENT ON COLUMN fina_indicator.inv_turn IS '存货周转率';
COMMENT ON COLUMN fina_indicator.ar_turn IS '应收账款周转率';
COMMENT ON COLUMN fina_indicator.ca_turn IS '流动资产周转率';
COMMENT ON COLUMN fina_indicator.fa_turn IS '固定资产周转率';
COMMENT ON COLUMN fina_indicator.assets_turn IS '总资产周转率';
COMMENT ON COLUMN fina_indicator.op_income IS '经营活动净收益';
COMMENT ON COLUMN fina_indicator.valuechange_income IS '价值变动净收益';
COMMENT ON COLUMN fina_indicator.interst_income IS '利息费用';
COMMENT ON COLUMN fina_indicator.daa IS '折旧与摊销';
COMMENT ON COLUMN fina_indicator.ebit IS '息税前利润';
COMMENT ON COLUMN fina_indicator.ebitda IS '息税折旧摊销前利润';
COMMENT ON COLUMN fina_indicator.fcff IS '企业自由现金流量';
COMMENT ON COLUMN fina_indicator.fcfe IS '股权自由现金流量';
COMMENT ON COLUMN fina_indicator.current_exint IS '无息流动负债';
COMMENT ON COLUMN fina_indicator.noncurrent_exint IS '无息非流动负债';
COMMENT ON COLUMN fina_indicator.interestdebt IS '带息债务';
COMMENT ON COLUMN fina_indicator.netdebt IS '净债务';
COMMENT ON COLUMN fina_indicator.tangible_asset IS '有形资产';
COMMENT ON COLUMN fina_indicator.working_capital IS '营运资金';
COMMENT ON COLUMN fina_indicator.networking_capital IS '营运流动资本';
COMMENT ON COLUMN fina_indicator.invest_capital IS '全部投入资本';
COMMENT ON COLUMN fina_indicator.retained_earnings IS '留存收益';
COMMENT ON COLUMN fina_indicator.diluted2_eps IS '期末摊薄每股收益';
COMMENT ON COLUMN fina_indicator.bps IS '每股净资产';
COMMENT ON COLUMN fina_indicator.ocfps IS '每股经营活动产生的现金流量净额';
COMMENT ON COLUMN fina_indicator.retainedps IS '每股留存收益';
COMMENT ON COLUMN fina_indicator.cfps IS '每股现金流量净额';
COMMENT ON COLUMN fina_indicator.ebit_ps IS '每股息税前利润';
COMMENT ON COLUMN fina_indicator.fcff_ps IS '每股企业自由现金流量';
COMMENT ON COLUMN fina_indicator.fcfe_ps IS '每股股东自由现金流量';
COMMENT ON COLUMN fina_indicator.netprofit_margin IS '销售净利率';
COMMENT ON COLUMN fina_indicator.grossprofit_margin IS '销售毛利率';
COMMENT ON COLUMN fina_indicator.cogs_of_sales IS '销售成本率';
COMMENT ON COLUMN fina_indicator.expense_of_sales IS '销售期间费用率';
COMMENT ON COLUMN fina_indicator.profit_to_gr IS '净利润/营业总收入';
COMMENT ON COLUMN fina_indicator.saleexp_to_gr IS '销售费用/营业总收入';
COMMENT ON COLUMN fina_indicator.adminexp_of_gr IS '管理费用/营业总收入';
COMMENT ON COLUMN fina_indicator.finaexp_of_gr IS '财务费用/营业总收入';
COMMENT ON COLUMN fina_indicator.impai_ttm IS '资产减值损失/营业总收入';
COMMENT ON COLUMN fina_indicator.gc_of_gr IS '营业总成本/营业总收入';
COMMENT ON COLUMN fina_indicator.op_of_gr IS '营业利润/营业总收入';
COMMENT ON COLUMN fina_indicator.ebit_of_gr IS '息税前利润/营业总收入';
COMMENT ON COLUMN fina_indicator.roe IS '净资产收益率';
COMMENT ON COLUMN fina_indicator.roe_waa IS '加权平均净资产收益率';
COMMENT ON COLUMN fina_indicator.roe_dt IS '净资产收益率(扣除非经常损益)';
COMMENT ON COLUMN fina_indicator.roa IS '总资产报酬率';
COMMENT ON COLUMN fina_indicator.npta IS '总资产净利润';
COMMENT ON COLUMN fina_indicator.roic IS '投入资本回报率';
COMMENT ON COLUMN fina_indicator.roe_yearly IS '年化净资产收益率';
COMMENT ON COLUMN fina_indicator.roa2_yearly IS '年化总资产报酬率';
COMMENT ON COLUMN fina_indicator.roe_avg IS '平均净资产收益率(增发条件)';
COMMENT ON COLUMN fina_indicator.opincome_of_ebt IS '经营活动净收益/利润总额';
COMMENT ON COLUMN fina_indicator.investincome_of_ebt IS '价值变动净收益/利润总额';
COMMENT ON COLUMN fina_indicator.n_op_profit_of_ebt IS '营业外收支净额/利润总额';
COMMENT ON COLUMN fina_indicator.tax_to_ebt IS '所得税/利润总额';
COMMENT ON COLUMN fina_indicator.dtprofit_to_profit IS '扣除非经常损益后的净利润/净利润';
COMMENT ON COLUMN fina_indicator.salescash_to_or IS '销售商品提供劳务收到的现金/营业收入';
COMMENT ON COLUMN fina_indicator.ocf_to_or IS '经营活动产生的现金流量净额/营业收入';
COMMENT ON COLUMN fina_indicator.ocf_to_opincome IS '经营活动产生的现金流量净额/经营活动净收益';
COMMENT ON COLUMN fina_indicator.capitalized_to_da IS '资本支出/折旧和摊销';
COMMENT ON COLUMN fina_indicator.debt_to_assets IS '资产负债率';
COMMENT ON COLUMN fina_indicator.assets_to_eqt IS '权益乘数';
COMMENT ON COLUMN fina_indicator.dp_assets_to_eqt IS '权益乘数(杜邦分析)';
COMMENT ON COLUMN fina_indicator.ca_to_assets IS '流动资产/总资产';
COMMENT ON COLUMN fina_indicator.nca_to_assets IS '非流动资产/总资产';
COMMENT ON COLUMN fina_indicator.tbassets_to_totalassets IS '有形资产/总资产';
COMMENT ON COLUMN fina_indicator.int_to_talcap IS '带息债务/全部投入资本';
COMMENT ON COLUMN fina_indicator.eqt_to_talcapital IS '归属于母公司的股东权益/全部投入资本';
COMMENT ON COLUMN fina_indicator.currentdebt_to_debt IS '流动负债/负债合计';
COMMENT ON COLUMN fina_indicator.longdeb_to_debt IS '非流动负债/负债合计';
COMMENT ON COLUMN fina_indicator.ocf_to_shortdebt IS '经营活动产生的现金流量净额/流动负债';
COMMENT ON COLUMN fina_indicator.debt_to_eqt IS '产权比率';
COMMENT ON COLUMN fina_indicator.eqt_to_debt IS '归属于母公司的股东权益/负债合计';
COMMENT ON COLUMN fina_indicator.eqt_to_interestdebt IS '归属于母公司的股东权益/带息债务';
COMMENT ON COLUMN fina_indicator.tangibleasset_to_debt IS '有形资产/负债合计';
COMMENT ON COLUMN fina_indicator.tangasset_to_intdebt IS '有形资产/带息债务';
COMMENT ON COLUMN fina_indicator.tangibleasset_to_netdebt IS '有形资产/净债务';
COMMENT ON COLUMN fina_indicator.ocf_to_debt IS '经营活动产生的现金流量净额/负债合计';
COMMENT ON COLUMN fina_indicator.ocf_to_interestdebt IS '经营活动产生的现金流量净额/带息债务';
COMMENT ON COLUMN fina_indicator.ocf_to_netdebt IS '经营活动产生的现金流量净额/净债务';
COMMENT ON COLUMN fina_indicator.ebit_to_interest IS '已获利息倍数(EBIT/利息费用)';
COMMENT ON COLUMN fina_indicator.longdebt_to_workingcapital IS '长期债务与营运资金比率';
COMMENT ON COLUMN fina_indicator.ebitda_to_debt IS '息税折旧摊销前利润/负债合计';
COMMENT ON COLUMN fina_indicator.turn_days IS '营业周期';
COMMENT ON COLUMN fina_indicator.roa_yearly IS '年化总资产净利率';
COMMENT ON COLUMN fina_indicator.roa_dp IS '总资产净利率(杜邦分析)';
COMMENT ON COLUMN fina_indicator.fixed_assets IS '固定资产合计';
COMMENT ON COLUMN fina_indicator.profit_prefin_exp IS '扣除财务费用前营业利润';
COMMENT ON COLUMN fina_indicator.non_op_profit IS '非营业利润';
COMMENT ON COLUMN fina_indicator.op_to_ebt IS '营业利润／利润总额';
COMMENT ON COLUMN fina_indicator.nop_to_ebt IS '非营业利润／利润总额';
COMMENT ON COLUMN fina_indicator.ocf_to_profit IS '经营活动产生的现金流量净额／营业利润';
COMMENT ON COLUMN fina_indicator.cash_to_liqdebt IS '货币资金／流动负债';
COMMENT ON COLUMN fina_indicator.cash_to_liqdebt_withinterest IS '货币资金／带息流动负债';
COMMENT ON COLUMN fina_indicator.op_to_liqdebt IS '营业利润／流动负债';
COMMENT ON COLUMN fina_indicator.op_to_debt IS '营业利润／负债合计';
COMMENT ON COLUMN fina_indicator.roic_yearly IS '年化投入资本回报率';
COMMENT ON COLUMN fina_indicator.total_fa_trun IS '固定资产合计周转率';
COMMENT ON COLUMN fina_indicator.profit_to_op IS '利润总额／营业收入';
COMMENT ON COLUMN fina_indicator.q_opincome IS '经营活动单季度净收益';
COMMENT ON COLUMN fina_indicator.q_investincome IS '价值变动单季度净收益';
COMMENT ON COLUMN fina_indicator.q_dtprofit IS '扣除非经常损益后的单季度净利润';
COMMENT ON COLUMN fina_indicator.q_eps IS '每股收益(单季度)';
COMMENT ON COLUMN fina_indicator.q_netprofit_margin IS '销售净利率(单季度)';
COMMENT ON COLUMN fina_indicator.q_gsprofit_margin IS '销售毛利率(单季度)';
COMMENT ON COLUMN fina_indicator.q_exp_to_sales IS '销售期间费用率(单季度)';
COMMENT ON COLUMN fina_indicator.q_profit_to_gr IS '净利润／营业总收入(单季度)';
COMMENT ON COLUMN fina_indicator.q_saleexp_to_gr IS '销售费用／营业总收入 (单季度)';
COMMENT ON COLUMN fina_indicator.q_adminexp_to_gr IS '管理费用／营业总收入 (单季度)';
COMMENT ON COLUMN fina_indicator.q_finaexp_to_gr IS '财务费用／营业总收入 (单季度)';
COMMENT ON COLUMN fina_indicator.q_impair_to_gr_ttm IS '资产减值损失／营业总收入(单季度)';
COMMENT ON COLUMN fina_indicator.q_gc_to_gr IS '营业总成本／营业总收入 (单季度)';
COMMENT ON COLUMN fina_indicator.q_op_to_gr IS '营业利润／营业总收入(单季度)';
COMMENT ON COLUMN fina_indicator.q_roe IS '净资产收益率(单季度)';
COMMENT ON COLUMN fina_indicator.q_dt_roe IS '净资产单季度收益率(扣除非经常损益)';
COMMENT ON COLUMN fina_indicator.q_npta IS '总资产净利润(单季度)';
COMMENT ON COLUMN fina_indicator.q_opincome_to_ebt IS '经营活动净收益／利润总额(单季度)';
COMMENT ON COLUMN fina_indicator.q_investincome_to_ebt IS '价值变动净收益／利润总额(单季度)';
COMMENT ON COLUMN fina_indicator.q_dtprofit_to_profit IS '扣除非经常损益后的净利润／净利润(单季度)';
COMMENT ON COLUMN fina_indicator.q_salescash_to_or IS '销售商品提供劳务收到的现金／营业收入(单季度)';
COMMENT ON COLUMN fina_indicator.q_ocf_to_sales IS '经营活动产生的现金流量净额／营业收入(单季度)';
COMMENT ON COLUMN fina_indicator.q_ocf_to_or IS '经营活动产生的现金流量净额／经营活动净收益(单季度)';
COMMENT ON COLUMN fina_indicator.basic_eps_yoy IS '基本每股收益同比增长率(%)';
COMMENT ON COLUMN fina_indicator.dt_eps_yoy IS '稀释每股收益同比增长率(%)';
COMMENT ON COLUMN fina_indicator.cfps_yoy IS '每股经营活动产生的现金流量净额同比增长率(%)';
COMMENT ON COLUMN fina_indicator.op_yoy IS '营业利润同比增长率(%)';
COMMENT ON COLUMN fina_indicator.ebt_yoy IS '利润总额同比增长率(%)';
COMMENT ON COLUMN fina_indicator.netprofit_yoy IS '归属母公司股东的净利润同比增长率(%)';
COMMENT ON COLUMN fina_indicator.dt_netprofit_yoy IS '归属母公司股东的净利润-扣除非经常损益同比增长率(%)';
COMMENT ON COLUMN fina_indicator.ocf_yoy IS '经营活动产生的现金流量净额同比增长率(%)';
COMMENT ON COLUMN fina_indicator.roe_yoy IS '净资产收益率(摊薄)同比增长率(%)';
COMMENT ON COLUMN fina_indicator.bps_yoy IS '每股净资产相对年初增长率(%)';
COMMENT ON COLUMN fina_indicator.assets_yoy IS '资产总计相对年初增长率(%)';
COMMENT ON COLUMN fina_indicator.eqt_yoy IS '归属母公司的股东权益相对年初增长率(%)';
COMMENT ON COLUMN fina_indicator.tr_yoy IS '营业总收入同比增长率(%)';
COMMENT ON COLUMN fina_indicator.or_yoy IS '营业收入同比增长率(%)';
COMMENT ON COLUMN fina_indicator.q_gr_yoy IS '营业总收入同比增长率(%)(单季度)';
COMMENT ON COLUMN fina_indicator.q_gr_qoq IS '营业总收入环比增长率(%)(单季度)';
COMMENT ON COLUMN fina_indicator.q_sales_yoy IS '营业收入同比增长率(%)(单季度)';
COMMENT ON COLUMN fina_indicator.q_sales_qoq IS '营业收入环比增长率(%)(单季度)';
COMMENT ON COLUMN fina_indicator.q_op_yoy IS '营业利润同比增长率(%)(单季度)';
COMMENT ON COLUMN fina_indicator.q_op_qoq IS '营业利润环比增长率(%)(单季度)';
COMMENT ON COLUMN fina_indicator.q_profit_yoy IS '净利润同比增长率(%)(单季度)';
COMMENT ON COLUMN fina_indicator.q_profit_qoq IS '净利润环比增长率(%)(单季度)';
COMMENT ON COLUMN fina_indicator.q_netprofit_yoy IS '归属母公司股东的净利润同比增长率(%)(单季度)';
COMMENT ON COLUMN fina_indicator.q_netprofit_qoq IS '归属母公司股东的净利润环比增长率(%)(单季度)';
COMMENT ON COLUMN fina_indicator.equity_yoy IS '净资产同比增长率';
COMMENT ON COLUMN fina_indicator.rd_exp IS '研发费用';
COMMENT ON COLUMN fina_indicator.update_flag IS '更新标识';
COMMENT ON COLUMN fina_indicator.updated_at IS '更新时间';

-- 索引
CREATE INDEX IF NOT EXISTS idx_fina_indicator_date ON fina_indicator(end_date);
CREATE INDEX IF NOT EXISTS idx_fina_indicator_code ON fina_indicator(ts_code);
CREATE INDEX IF NOT EXISTS idx_fina_indicator_ann_date ON fina_indicator(ann_date);
