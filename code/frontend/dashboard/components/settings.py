"""
系统配置组件

提供配置管理界面，包括Tushare token、数据拉取参数等
"""

import streamlit as st
from dashboard.config_manager import ConfigManager
from dashboard.utils.table_info import TABLE_INFO


def render_settings(config_manager: ConfigManager):
    """
    渲染系统配置页面

    Args:
        config_manager: 配置管理器
    """
    st.header("⚙️ 系统配置")

    # 创建标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Tushare配置",
        "数据导入配置",
        "数据表管理",
        "调度配置",
        "快照配置"
    ])

    # ========== Tab 1: Tushare配置 ==========
    with tab1:
        render_tushare_settings(config_manager)

    # ========== Tab 2: 数据导入配置 ==========
    with tab2:
        render_import_settings(config_manager)

    # ========== Tab 3: 数据表管理 ==========
    with tab3:
        render_table_management(config_manager)

    # ========== Tab 4: 调度配置 ==========
    with tab4:
        render_scheduler_settings(config_manager)

    # ========== Tab 5: 快照配置 ==========
    with tab5:
        render_snapshot_settings(config_manager)


def render_tushare_settings(config_manager: ConfigManager):
    """渲染Tushare配置"""
    st.subheader("Tushare API 配置")

    tushare_config = config_manager.get_tushare_config()

    with st.form("tushare_config_form"):
        token = st.text_input(
            "API Token",
            value=tushare_config.get('token', ''),
            type="password",
            help="Tushare Pro API Token，从tushare.pro获取"
        )

        api_url = st.text_input(
            "API URL",
            value=tushare_config.get('api_url', 'http://api.tushare.pro'),
            help="Tushare API地址"
        )

        rate_limit = st.number_input(
            "速率限制（次/分钟）",
            min_value=1,
            max_value=500,
            value=tushare_config.get('rate_limit', 500),
            help="每分钟API调用次数限制，1万积分支持500次/分钟"
        )

        submitted = st.form_submit_button("保存配置", type="primary")

        if submitted:
            success = config_manager.update_section('tushare', {
                'token': token,
                'api_url': api_url,
                'rate_limit': rate_limit
            })

            if success:
                st.success("✅ Tushare配置已保存")
                st.rerun()
            else:
                st.error("❌ 配置保存失败")

    # 显示帮助信息
    st.markdown("---")
    st.markdown("""
    **💡 获取Tushare Token：**
    1. 访问 [Tushare Pro](https://tushare.pro)
    2. 注册账号并登录
    3. 在个人中心获取API Token
    4. 根据积分等级查看速率限制：
       - 120积分：200次/分钟
       - 2000积分：400次/分钟
       - 5000积分：500次/分钟
       - 10000积分及以上：500次/分钟
    """)


def render_import_settings(config_manager: ConfigManager):
    """渲染数据导入配置"""
    st.subheader("历史数据导入配置")

    import_config = config_manager.get_import_config()

    with st.form("import_config_form"):
        start_date = st.text_input(
            "起始日期",
            value=import_config.get('start_date', '20210101'),
            help="历史数据起始日期，格式：YYYYMMDD"
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            batch_size = st.number_input(
                "批次大小",
                min_value=10,
                max_value=500,
                value=import_config.get('batch_size', 100),
                help="每批获取的股票数量"
            )

        with col2:
            concurrent_workers = st.number_input(
                "并发线程数",
                min_value=1,
                max_value=20,
                value=import_config.get('concurrent_workers', 10),
                help="并发工作线程数量，建议不超过20"
            )

        submitted = st.form_submit_button("保存配置", type="primary")

        if submitted:
            # 验证日期格式
            if len(start_date) != 8:
                st.error("❌ 日期格式错误，请使用YYYYMMDD格式")
            else:
                success = config_manager.update_section('history_import', {
                    'start_date': start_date,
                    'batch_size': batch_size,
                    'concurrent_workers': concurrent_workers
                })

                if success:
                    st.success("✅ 数据导入配置已保存")
                    st.rerun()
                else:
                    st.error("❌ 配置保存失败")

    # 显示当前配置状态
    st.markdown("---")
    st.info(f"""
    **当前配置摘要：**
    - 数据起始时间：{import_config.get('start_date', 'N/A')}
    - 批次大小：{import_config.get('batch_size', 100)} 只股票
    - 并发线程数：{import_config.get('concurrent_workers', 10)}
    """)


def render_table_management(config_manager: ConfigManager):
    """渲染数据表管理"""
    st.subheader("数据表拉取配置")

    st.markdown("""
    选择需要拉取的数据表。未启用的表将不会在数据导入时更新。
    """)

    # 按分类显示表（使用最新分类标准）
    categories = {
        'P0基础': '基础数据（交易日历、股票列表、指数列表、ETF列表等）',
        'P1行情': '行情数据（日线、周线、月线、指数日线、ETF日线等）',
        'P2财务': '财务数据（利润表、资产负债表、现金流量表、业绩预告等）',
        'P3资金流向(THS)': '同花顺资金流向（个股资金流、概念资金流、行业资金流）',
        'P3概念板块': '同花顺概念板块（概念成分、指数日线）',
        'P4游资': '游资数据（游资账户、游资交易明细）',
        '系统表': '系统表（全局游标表）',
        'P5滚动': '滚动数据（按月分表）'
    }

    # 获取当前启用状态
    enabled_tables = config_manager.get_enabled_tables()

    # 如果没有设置，默认显示所有表都启用
    all_tables = []
    for table_name, info in TABLE_INFO.items():
        is_enabled = table_name in enabled_tables if enabled_tables else True
        all_tables.append({
            'table_name': table_name,
            'chinese_name': info['chinese_name'],
            'category': info['category'],
            'enabled': is_enabled
        })

    # 按分类分组
    tables_by_category = {}
    for table in all_tables:
        cat = table['category']
        if cat not in tables_by_category:
            tables_by_category[cat] = []
        tables_by_category[cat].append(table)

    # 创建表单
    with st.form("table_management_form"):
        new_enabled_tables = []

        for category, category_desc in categories.items():
            if category in tables_by_category:
                st.markdown(f"**{category} - {category_desc}**")

                tables = tables_by_category[category]
                col_count = 3
                cols = st.columns(col_count)

                for idx, table in enumerate(tables):
                    col_idx = idx % col_count
                    with cols[col_idx]:
                        is_enabled = st.checkbox(
                            f"{table['chinese_name']} ({table['table_name']})",
                            value=table['enabled'],
                            key=f"table_{table['table_name']}"
                        )

                        if is_enabled:
                            new_enabled_tables.append(table['table_name'])

                st.markdown("")  # 添加间距

        submitted = st.form_submit_button("保存配置", type="primary")

        if submitted:
            success = config_manager.set_enabled_tables(new_enabled_tables)

            if success:
                st.success(f"✅ 数据表配置已保存，共启用 {len(new_enabled_tables)} 个表")
                st.rerun()
            else:
                st.error("❌ 配置保存失败")

    # 显示统计信息
    st.markdown("---")
    current_enabled = enabled_tables if enabled_tables else list(TABLE_INFO.keys())
    st.info(f"""
    **当前状态：**
    - 总表数：{len(TABLE_INFO)}
    - 已启用：{len(current_enabled)}
    - 未启用：{len(TABLE_INFO) - len(current_enabled)}
    """)


def render_scheduler_settings(config_manager: ConfigManager):
    """渲染调度配置"""
    st.subheader("自动调度配置")

    scheduler_config = config_manager.get_scheduler_config()

    with st.form("scheduler_config_form"):
        st.markdown("设置定时任务执行时间（24小时制）")

        col1, col2, col3 = st.columns(3)

        with col1:
            daily_update_time = st.text_input(
                "日数据更新时间",
                value=scheduler_config.get('daily_update_time', '18:00'),
                help="每日数据更新时间，格式：HH:MM"
            )

        with col2:
            weekly_update_time = st.text_input(
                "周数据更新时间",
                value=scheduler_config.get('weekly_update_time', '18:00'),
                help="每周数据更新时间，格式：HH:MM"
            )

        with col3:
            monthly_update_time = st.text_input(
                "月数据更新时间",
                value=scheduler_config.get('monthly_update_time', '18:00'),
                help="每月数据更新时间，格式：HH:MM"
            )

        submitted = st.form_submit_button("保存配置", type="primary")

        if submitted:
            # 验证时间格式
            time_format_valid = True
            for time_str in [daily_update_time, weekly_update_time, monthly_update_time]:
                try:
                    hour, minute = time_str.split(':')
                    if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
                        time_format_valid = False
                        break
                except:
                    time_format_valid = False
                    break

            if not time_format_valid:
                st.error("❌ 时间格式错误，请使用HH:MM格式（如18:00）")
            else:
                success = config_manager.update_section('scheduler', {
                    'daily_update_time': daily_update_time,
                    'weekly_update_time': weekly_update_time,
                    'monthly_update_time': monthly_update_time
                })

                if success:
                    st.success("✅ 调度配置已保存")
                    st.rerun()
                else:
                    st.error("❌ 配置保存失败")

    # 显示调度状态
    st.markdown("---")
    st.info(f"""
    **当前调度配置：**
    - 日数据更新：每日 {scheduler_config.get('daily_update_time', '18:00')}
    - 周数据更新：每周五 {scheduler_config.get('weekly_update_time', '18:00')}
    - 月数据更新：每月最后一天 {scheduler_config.get('monthly_update_time', '18:00')}
    """)


def render_snapshot_settings(config_manager: ConfigManager):
    """渲染快照配置（新增）"""
    st.subheader("快照配置")

    snapshot_config = config_manager.get_snapshot_config()

    with st.form("snapshot_config_form"):
        enabled = st.checkbox(
            "启用快照",
            value=snapshot_config.get('enabled', True),
            help="定时生成数据库快照"
        )

        interval = st.number_input(
            "快照间隔（分钟）",
            min_value=10,
            max_value=120,
            value=snapshot_config.get('interval', 30),
            help="快照生成间隔，默认30分钟"
        )

        locations = st.text_area(
            "快照位置（换行分隔）",
            value="\n".join(snapshot_config.get('locations', [])),
            help="快照文件保存位置，每行一个路径"
        )

        submitted = st.form_submit_button("保存配置", type="primary")

        if submitted:
            success = config_manager.update_section('snapshot', {
                'enabled': enabled,
                'interval': interval,
                'locations': locations.split('\n')
            })

            if success:
                st.success("✅ 快照配置已保存")
                st.rerun()
            else:
                st.error("❌ 配置保存失败")

    # 显示快照位置信息
    st.markdown("---")
    st.info(f"""
    **当前快照配置：**
    - 快照状态：{'启用' if snapshot_config.get('enabled', True) else '禁用'}
    - 快照间隔：每 {snapshot_config.get('interval', 30)} 分钟
    - 快照位置：
      - {snapshot_config.get('locations', ['database/adata_snapshot.db'])[0]}
      - {snapshot_config.get('locations', ['database/adata_snapshot.db'])[1] if len(snapshot_config.get('locations', [])) > 1 else '未设置'}
    """)