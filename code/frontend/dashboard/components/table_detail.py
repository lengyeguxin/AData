"""
表详情展示组件

展示表的详细结构信息，包括字段名、类型、注释等
"""

import streamlit as st
import pandas as pd
from dashboard.metadata import DatabaseMetadata
from dashboard.utils.table_info import get_table_info


def render_table_detail(metadata: DatabaseMetadata):
    """
    渲染表详情页面

    Args:
        metadata: 数据库元数据查询器
    """
    # 获取选中的表名
    selected_table = st.session_state.get('selected_table')

    if not selected_table:
        st.info("👈 请从表列表中选择一个表查看详情")
        return

    # 返回按钮
    if st.button("← 返回表列表"):
        st.session_state['selected_table'] = None
        st.session_state['current_page'] = 'table_list'
        st.rerun()

    st.markdown("---")

    # 获取表信息
    table_info = get_table_info(selected_table)

    # 显示表标题
    st.header(f"表结构: {selected_table}")
    st.subheader(f"{table_info['chinese_name']}")

    # 显示表基本信息
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**分类**: {table_info['category']}")
        st.write(f"**描述**: {table_info['description']}")
    with col2:
        st.write(f"**更新频率**: {table_info['update_frequency']}")
        st.write(f"**时间字段**: {table_info['date_field']}")

    st.markdown("---")

    # 获取表结构
    schema = metadata.get_table_schema(selected_table)

    if not schema:
        st.warning("无法获取表结构信息")
        return

    # 显示为DataFrame
    df = pd.DataFrame(schema)

    # 重命名列以提高可读性
    df.columns = ['字段名', '数据类型', '是否可空', '字段说明']

    st.dataframe(
        df,
        use_container_width=True,
        height=min(600, 50 + len(df) * 35),  # 动态调整高度
        hide_index=True
    )

    # 导出功能
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        # 导出CSV
        csv = df.to_csv(index=False).encode('utf-8-sig')  # 使用utf-8-sig以支持Excel打开
        st.download_button(
            label="📥 导出CSV",
            data=csv,
            file_name=f"{selected_table}_schema.csv",
            mime='text/csv'
        )

    with col2:
        # 导出Markdown
        markdown_content = _generate_markdown_table(selected_table, table_info, df)
        st.download_button(
            label="📥 导出Markdown",
            data=markdown_content,
            file_name=f"{selected_table}_schema.md",
            mime='text/markdown'
        )


def _generate_markdown_table(table_name: str, table_info: dict, df: pd.DataFrame) -> str:
    """
    生成Markdown格式的表结构文档

    Args:
        table_name: 表名
        table_info: 表信息
        df: 表结构DataFrame

    Returns:
        Markdown格式字符串
    """
    lines = [
        f"# {table_name} - {table_info['chinese_name']}",
        "",
        f"**分类**: {table_info['category']}",
        "",
        f"**描述**: {table_info['description']}",
        "",
        f"**更新频率**: {table_info['update_frequency']}",
        "",
        "## 表结构",
        "",
        "| 字段名 | 数据类型 | 是否可空 | 字段说明 |",
        "|--------|----------|----------|----------|"
    ]

    for _, row in df.iterrows():
        lines.append(f"| {row['字段名']} | {row['数据类型']} | {row['是否可空']} | {row['字段说明']} |")

    return "\n".join(lines)