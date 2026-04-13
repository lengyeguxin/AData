-- ============================================
-- P0表字段注释补充（使用COMMENT ON COLUMN语法）
-- ============================================

-- 1. trade_calendar（交易日历）
COMMENT ON COLUMN trade_calendar.exchange IS '交易所代码（SSE=上交所,SZSE=深交所）';
COMMENT ON COLUMN trade_calendar.cal_date IS '交易日期';
COMMENT ON COLUMN trade_calendar.is_open IS '是否交易（0=休市,1=交易）';
COMMENT ON COLUMN trade_calendar.pretrade_date IS '上一交易日';
COMMENT ON COLUMN trade_calendar.updated_at IS '更新时间';

-- 2. stock_basic（股票列表）
COMMENT ON COLUMN stock_basic.ts_code IS '股票代码（TS格式）';
COMMENT ON COLUMN stock_basic.name IS '股票名称';
COMMENT ON COLUMN stock_basic.industry IS '所属行业';
COMMENT ON COLUMN stock_basic.market IS '市场类型（主板/中小板/创业板/科创板）';
COMMENT ON COLUMN stock_basic.list_date IS '上市日期';
COMMENT ON COLUMN stock_basic.delist_date IS '退市日期';
COMMENT ON COLUMN stock_basic.is_hs IS '是否沪深港通标的（N=否,H=沪股通,S=深股通）';
COMMENT ON COLUMN stock_basic.updated_at IS '更新时间';

-- 3. index_basic（指数列表）
COMMENT ON COLUMN index_basic.ts_code IS '指数代码（TS格式）';
COMMENT ON COLUMN index_basic.name IS '指数简称';
COMMENT ON COLUMN index_basic.fullname IS '指数全称';
COMMENT ON COLUMN index_basic.market IS '市场类型';
COMMENT ON COLUMN index_basic.publisher IS '发布方';
COMMENT ON COLUMN index_basic.index_type IS '指数类型';
COMMENT ON COLUMN index_basic.category IS '指数类别';
COMMENT ON COLUMN index_basic.base_date IS '基期';
COMMENT ON COLUMN index_basic.base_point IS '基点';
COMMENT ON COLUMN index_basic.list_date IS '发布日期';
COMMENT ON COLUMN index_basic.weight_rule IS '加权方法';
COMMENT ON COLUMN index_basic.description IS '描述';
COMMENT ON COLUMN index_basic.updated_at IS '更新时间';

-- 4. ths_index_basic（同花顺指数列表）
COMMENT ON COLUMN ths_index_basic.ts_code IS '指数代码（TI格式）';
COMMENT ON COLUMN ths_index_basic.name IS '指数简称';
COMMENT ON COLUMN ths_index_basic.fullname IS '指数全称';
COMMENT ON COLUMN ths_index_basic.exchange IS '交易所';
COMMENT ON COLUMN ths_index_basic.type IS '指数类型（N=概念指数,S=特色指数）';
COMMENT ON COLUMN ths_index_basic.list_date IS '发布日期';
COMMENT ON COLUMN ths_index_basic.weight_rule IS '加权方法';
COMMENT ON COLUMN ths_index_basic.description IS '描述';
COMMENT ON COLUMN ths_index_basic.updated_at IS '更新时间';

-- 5. etf_basic（ETF基本信息）
COMMENT ON COLUMN etf_basic.ts_code IS 'ETF代码（TS格式）';
COMMENT ON COLUMN etf_basic.name IS 'ETF简称';
COMMENT ON COLUMN etf_basic.fullname IS 'ETF全称';
COMMENT ON COLUMN etf_basic.fund_type IS '基金类型';
COMMENT ON COLUMN etf_basic.fund_manager IS '基金经理';
COMMENT ON COLUMN etf_basic.list_date IS '上市日期';
COMMENT ON COLUMN etf_basic.issue_date IS '发行日期';
COMMENT ON COLUMN etf_basic.delist_date IS '退市日期';
COMMENT ON COLUMN etf_basic.issue_amount IS '发行份额（万份）';
COMMENT ON COLUMN etf_basic.m_fee IS '管理费（%）';
COMMENT ON COLUMN etf_basic.c_fee IS '托管费（%）';
COMMENT ON COLUMN etf_basic.benchmark IS '跟踪标的';
COMMENT ON COLUMN etf_basic.status IS '状态';
COMMENT ON COLUMN etf_basic.invest_type IS '投资类型';
COMMENT ON COLUMN etf_basic.type IS 'ETF类型';
COMMENT ON COLUMN etf_basic.trustee IS '托管人';
COMMENT ON COLUMN etf_basic.perf_benchmark IS '业绩比较基准';
COMMENT ON COLUMN etf_basic.updated_at IS '更新时间';

-- 6. etf_index（ETF指数）
COMMENT ON COLUMN etf_index.ts_code IS 'ETF代码（TS格式）';
COMMENT ON COLUMN etf_index.name IS 'ETF名称';
COMMENT ON COLUMN etf_index.updated_at IS '更新时间';