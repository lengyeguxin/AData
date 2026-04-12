"""
整体概览组件

展示数据库的整体统计信息
"""

import streamlit as st
import plotly.express as px
from typing import Dict
from dashboard.metadata import DatabaseMetadata


def render_overview(metadata: DatabaseMetadata):
    """
    渲染整体概览页面

    Args:
        metadata: 数据库元数据查询器
    """
    st.header("数据库概览")

    # 获取数据库统计信息
    stats = metadata.get_database_stats()

    # 第一行：关键指标卡片
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="总表数",
            value=f"{stats['total_tables']}"
        )

    with col2:
        total_rows = stats['total_rows']
        if total_rows >= 10000000:
            value_str = f"{total_rows / 10000000:.2f}千万"
        elif total_rows >= 10000:
            value_str = f"{total_rows / 10000:.2f}万"
        else:
            value_str = f"{total_rows:,}"
        st.metric(
            label="总记录数",
            value=value_str
        )

    with col3:
        st.metric(
            label="数据库大小",
            value=f"{stats['total_size_mb']:.2f} MB"
        )

    with col4:
        st.metric(
            label="最新数据时间",
            value=stats['newest_data'] or "未知"
        )

    st.markdown("---")

    # 第二行：分类统计
    st.subheader("表分类统计")

    categories = stats['categories']
    if categories:
        col1, col2 = st.columns(2)

        with col1:
            # 分类计数表格
            st.write("**各类别表数量**")
            for category, count in sorted(categories.items()):
                st.write(f"- **{category}**: {count}张表")

        with col2:
            # 分类饼图
            fig = px.pie(
                values=list(categories.values()),
                names=list(categories.keys()),
                title="表分类分布",
                hole=0.3
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无分类数据")

    st.markdown("---")

    # 第三行：数据时间范围
    st.subheader("数据时间范围")
    col1, col2 = st.columns(2)

    with col1:
        st.info(f"**最早数据**: {stats['oldest_data'] or '未知'}")

    with col2:
        st.success(f"**最新数据**: {stats['newest_data'] or '未知'}")