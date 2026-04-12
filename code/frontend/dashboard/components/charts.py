"""
图表可视化组件

使用Plotly创建各种数据可视化图表
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dashboard.metadata import DatabaseMetadata


def render_charts(metadata: DatabaseMetadata):
    """
    渲染图表分析页面

    Args:
        metadata: 数据库元数据查询器
    """
    st.header("数据分析图表")

    # 获取所有表信息
    tables_info = metadata.get_all_tables_info()

    if not tables_info:
        st.warning("未找到任何数据表")
        return

    df = pd.DataFrame(tables_info)

    # ========== 第一行：数据量分布 ==========
    st.subheader("📊 数据量分布")
    col1, col2 = st.columns(2)

    with col1:
        # 各表记录数条形图（Top 20）
        df_top = df.nlargest(20, 'row_count').sort_values('row_count', ascending=True)

        fig = px.bar(
            df_top,
            x='row_count',
            y='table_name',
            orientation='h',
            title='记录数 Top 20',
            hover_data=['chinese_name', 'category'],
            color='category',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 分类总记录数饼图
        category_totals = df.groupby('category')['row_count'].sum().reset_index()

        fig = px.pie(
            category_totals,
            values='row_count',
            names='category',
            title='各分类总记录数占比',
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ========== 第二行：数据更新时间 ==========
    st.subheader("📅 数据更新情况")

    # 最新数据时间条形图
    df_time = df[df['latest_date'].notna()].copy()
    df_time = df_time.sort_values('latest_date', ascending=True)

    if not df_time.empty:
        fig = px.bar(
            df_time,
            x='latest_date',
            y='table_name',
            orientation='h',
            title='各表最新数据时间',
            hover_data=['chinese_name', 'category'],
            color='category',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=800, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无数据时间信息")

    st.markdown("---")

    # ========== 第三行：存储空间分布 ==========
    st.subheader("💾 存储空间分布")

    # 表大小Treemap
    df_size = df[df['size_mb'] > 0].copy()

    if not df_size.empty:
        fig = px.treemap(
            df_size,
            path=['category', 'table_name'],
            values='size_mb',
            title='各表存储空间占比',
            hover_data=['chinese_name', 'row_count'],
            color='row_count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无存储空间信息")

    st.markdown("---")

    # ========== 第四行：统计摘要 ==========
    st.subheader("📈 统计摘要")

    col1, col2, col3 = st.columns(3)

    with col1:
        # 各分类平均记录数
        avg_by_category = df.groupby('category')['row_count'].mean().reset_index()
        avg_by_category.columns = ['分类', '平均记录数']

        fig = px.bar(
            avg_by_category,
            x='分类',
            y='平均记录数',
            title='各分类平均记录数',
            color='分类',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 各分类表大小总和
        size_by_category = df.groupby('category')['size_mb'].sum().reset_index()
        size_by_category.columns = ['分类', '总大小(MB)']

        fig = px.bar(
            size_by_category,
            x='分类',
            y='总大小(MB)',
            title='各分类存储空间',
            color='分类',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        # 各分类表数量
        count_by_category = df['category'].value_counts().reset_index()
        count_by_category.columns = ['分类', '表数量']

        fig = px.pie(
            count_by_category,
            values='表数量',
            names='分类',
            title='各分类表数量占比',
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)