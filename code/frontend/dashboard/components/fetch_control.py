"""
数据拉取控制组件

提供数据拉取控制界面，包括游标管理、拉取状态控制等
"""

import streamlit as st
import sys
from pathlib import Path

# 添加backend到路径
project_root = Path(__file__).parent.parent.parent.parent
backend_path = project_root / 'backend'
sys.path.insert(0, str(backend_path))

from dashboard.config_manager import ConfigManager
from src.core.global_cursor_manager import GlobalCursorManager
from src.core.database import Database
import duckdb


def render_fetch_control(config_manager: ConfigManager):
    """渲染数据拉取控制页面"""
    st.header("🔄 数据拉取控制")

    # 初始化游标管理器（使用绝对路径）
    db_path = str(project_root / 'database' / 'adata.db')
    config_path = str(backend_path / 'config')
    cursor_manager = GlobalCursorManager(db_path, config_path)

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
                try:
                    with Database(db_path) as db:
                        db.execute("UPDATE global_cursor SET cursor_value=NULL, status='pending', last_fetch_time=NULL, last_record_count=0")
                    st.success("✅ 所有游标已重置")
                    st.session_state.confirm_reset = False
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 重置失败: {e}")
            else:
                st.session_state.confirm_reset = True
                st.warning("⚠️ 再次点击确认重置")

    st.markdown("---")

    # ========== 第二部分：游标状态 ==========
    st.subheader("游标状态")

    # 获取所有游标
    try:
        cursors = cursor_manager.get_all_cursors()

        # 按游标类型分组
        cursors_by_type = {}
        for cursor in cursors:
            cursor_type = cursor['cursor_type']
            if cursor_type not in cursors_by_type:
                cursors_by_type[cursor_type] = []
            cursors_by_type[cursor_type].append(cursor)

        # 显示每组游标
        for cursor_type, type_name in [
            ('daily', '按天更新'),
            ('monthly', '按月更新'),
            ('yearly', '按年更新'),
            ('once', '一次性更新')
        ]:
            if cursor_type in cursors_by_type:
                with st.expander(f"{type_name} ({len(cursors_by_type[cursor_type])}张表)", expanded=True):
                    # 显示表格
                    display_data = []
                    for cursor in cursors_by_type[cursor_type]:
                        status_emoji = {
                            'pending': '⏳',
                            'running': '🔄',
                            'success': '✅',
                            'failed': '❌'
                        }.get(cursor['status'], '❓')

                        display_data.append({
                            '表名': cursor['table_name'],
                            '游标值': cursor['cursor_value'] or '未初始化',
                            '状态': f"{status_emoji} {cursor['status']}",
                            '最后拉取时间': cursor['last_fetch_time'] or '从未拉取',
                            '记录数': cursor['last_record_count']
                        })

                    st.dataframe(display_data, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 游标状态读取失败: {e}")
        st.info("""
        **游标状态读取失败**

        可能原因：
        - 数据库未初始化（请运行 scripts/setup_database.py）
        - global_cursor表不存在
        - 数据库路径配置错误

        请检查数据库状态后再重试。
        """)

    st.markdown("---")

    # ========== 第三部分：单表控制 ==========
    st.subheader("单表控制")

    # 选择表
    try:
        cursors = cursor_manager.get_all_cursors()
        table_names = [cursor['table_name'] for cursor in cursors]
        selected_table = st.selectbox("选择表", table_names)

        if selected_table:
            cursor = cursor_manager.get_cursor(selected_table)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**表名：** {cursor['table_name']}")
                st.markdown(f"**游标类型：** {cursor['cursor_type']}")
                st.markdown(f"**游标值：** {cursor['cursor_value']}")
                st.markdown(f"**状态：** {cursor['status']}")

            with col2:
                st.markdown(f"**前置依赖：** {', '.join(cursor['dependencies']) or '无'}")
                st.markdown(f"**截至时间：** {cursor['fetch_after_time']}")
                st.markdown(f"**最后拉取：** {cursor['last_fetch_time'] or '从未拉取'}")
                st.markdown(f"**记录数：** {cursor['last_record_count']}")

            # 单表操作按钮
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🔄 重置 {selected_table} 游标"):
                    try:
                        with Database(db_path) as db:
                            db.execute(
                                "UPDATE global_cursor SET cursor_value=NULL, status='pending', last_fetch_time=NULL, last_record_count=0 WHERE table_name=?",
                                (selected_table,)
                            )
                        st.success(f"✅ {selected_table} 游标已重置")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 重置失败: {e}")

            with col2:
                if st.button(f"▶️ 立即拉取 {selected_table}"):
                    st.info("请在后端控制台手动触发拉取，或等待定时调度")

    except Exception as e:
        st.error(f"❌ 单表控制加载失败: {e}")