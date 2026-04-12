"""
数据拉取控制组件

提供数据拉取控制界面，包括游标管理、拉取状态控制等
"""

import streamlit as st
import sys
sys.path.append('code/backend')
from dashboard.config_manager import ConfigManager


def render_fetch_control(config_manager: ConfigManager):
    """渲染数据拉取控制页面"""
    st.header("🔄 数据拉取控制")

    # ========== 第一部分：控制面板 ==========
    st.subheader("控制面板")

    # 获取当前配置
    fetch_config = config_manager.get_fetch_config()
    is_enabled = fetch_config.get('enabled', True)

    col1, col2, col3 = st.columns(3)

    with col1:
        # 状态显示
        status_color = "🟢" if is_enabled else "🔴"
        status_text = "运行中" if is_enabled else "已停止"
        st.metric("拉取状态", f"{status_color} {status_text}")

    with col2:
        # 开关按钮
        if is_enabled:
            if st.button("⏸️ 暂停拉取", type="secondary", use_container_width=True):
                config_manager.update_section('fetch', {'enabled': False})
                st.success("✅ 数据拉取已暂停")
                st.rerun()
        else:
            if st.button("▶️ 开始拉取", type="primary", use_container_width=True):
                config_manager.update_section('fetch', {'enabled': True})
                st.success("✅ 数据拉取已启动")
                st.rerun()

    with col3:
        # 重置游标按钮
        if st.button("🔄 重置所有游标", type="secondary", use_container_width=True):
            if st.session_state.get('confirm_reset'):
                # 执行重置
                # 注意：实际执行需要GlobalCursorManager类，这里暂时显示提示
                st.warning("⚠️ 游标重置功能需要GlobalCursorManager支持，将在后端实现后启用")
                st.session_state.confirm_reset = False
            else:
                st.session_state.confirm_reset = True
                st.warning("⚠️ 再次点击确认重置")

    st.markdown("---")

    # ========== 第二部分：游标状态 ==========
    st.subheader("游标状态")

    # 显示提示信息
    st.info("""
    **游标状态监控功能需要后端支持**

    游标状态页面将在GlobalCursorManager实现后显示：
    - 每张表的游标值（最后完成的日期）
    - 拉取状态（pending/running/success/failed）
    - 最后拉取时间和记录数
    - 按游标类型分组（daily/monthly/yearly/once）

    后端开发完成后，此页面将自动启用。
    """)

    # 占位符：显示游标类型说明
    with st.expander("游标策略说明", expanded=True):
        st.markdown("""
        **游标类型分类：**

        1. **无游标（none）**
           - 全量拉取，不记录进度
           - 适用表：stock_basic、index_basic、etf_basic、etf_index、hots_user、ths_index_basic

        2. **按天记录（daily_trade）**
           - 每交易日拉取，游标记录最后完成日期
           - 适用表：stock_daily、stock_daily_basic、stock_weekly、stock_monthly、index_daily、etf_daily、etf_adj_factor、hots_trader_detail、ths_moneyflow、ths_concept_moneyflow、ths_industry_moneyflow、ths_index_daily

        3. **按天记录（daily_natural）**
           - 每自然日拉取，不受交易日历限制
           - 适用表：fina_indicator、income、balancesheet、cashflow、express、express_brief、dividend

        4. **按年记录（yearly）**
           - 每年拉取一次，游标记录年份
           - 适用表：trade_calendar

        5. **特殊游标（special_ths_member）**
           - 遍历指数列表，游标记录当前指数代码
           - 适用表：ths_concept_member
        """)

    st.markdown("---")

    # ========== 第三部分：单表控制 ==========
    st.subheader("单表控制")

    # 显示提示信息
    st.info("""
    **单表控制功能需要后端支持**

    单表控制功能将在GlobalCursorManager实现后启用：
    - 查看单张表的游标详情
    - 重置单个表的游标
    - 手动触发单表拉取

    后端开发完成后，此功能将自动启用。
    """)

    # 显示表列表（静态展示）
    from dashboard.utils.table_info import TABLE_INFO

    with st.expander("数据表列表", expanded=False):
        st.markdown(f"**共 {len(TABLE_INFO)} 张数据表**")

        # 按优先级分组显示
        categories = {
            'P0': '核心数据（前置表）',
            'P1行情': '行情数据',
            'P2财务': '财务数据',
            'P3资金流向(THS)': '资金流向',
            'P3概念板块': '概念板块',
            'P4游资': '游资数据'
        }

        tables_by_category = {}
        for table_name, info in TABLE_INFO.items():
            cat = info['category']
            if cat not in tables_by_category:
                tables_by_category[cat] = []
            tables_by_category[cat].append({
                'table_name': table_name,
                'chinese_name': info['chinese_name']
            })

        for category, category_desc in categories.items():
            if category in tables_by_category:
                st.markdown(f"**{category} - {category_desc}**")

                tables = tables_by_category[category]
                for table in tables:
                    st.markdown(f"- {table['chinese_name']} ({table['table_name']})")

                st.markdown("")