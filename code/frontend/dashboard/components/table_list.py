"""
表列表展示组件

展示所有数据表的详细信息，支持筛选、排序和查看详情
"""

import streamlit as st
from typing import List, Dict
from dashboard.metadata import DatabaseMetadata


def render_table_list(metadata: DatabaseMetadata):
    """
    渲染表列表页面

    Args:
        metadata: 数据库元数据查询器
    """
    st.header("数据表列表")

    # 筛选器
    col1, col2, col3 = st.columns(3)

    with col1:
        category_filter = st.selectbox(
            "选择分类",
            ["全部", "P0基础", "P1行情", "P2财务", "P3资金流向(THS)", "P3概念板块", "P4游资", "系统表", "P5滚动"],
            key="category_filter"
        )

    with col2:
        sort_by = st.selectbox(
            "排序方式",
            ["表名", "记录数", "最新数据时间", "表大小"],
            key="sort_by"
        )

    with col3:
        sort_order = st.selectbox(
            "排序顺序",
            ["降序", "升序"],
            key="sort_order"
        )

    st.markdown("---")

    # 获取表信息
    tables_info = metadata.get_all_tables_info()

    if not tables_info:
        st.warning("未找到任何数据表")
        return

    # 筛选
    if category_filter != "全部":
        tables_info = [t for t in tables_info if t['category'] == category_filter]

    # 排序
    reverse = (sort_order == "降序")

    if sort_by == "表名":
        tables_info.sort(key=lambda x: x['table_name'], reverse=reverse)
    elif sort_by == "记录数":
        tables_info.sort(key=lambda x: x['row_count'], reverse=reverse)
    elif sort_by == "最新数据时间":
        tables_info.sort(key=lambda x: x['latest_date'] or "", reverse=reverse)
    elif sort_by == "表大小":
        tables_info.sort(key=lambda x: x['size_mb'], reverse=reverse)

    # 显示统计信息
    st.write(f"**共 {len(tables_info)} 张表**")

    st.markdown("---")

    # CSS样式：固定宽度字段对齐
    st.markdown("""
    <style>
    .table-row {
        font-family: 'Courier New', Consolas, monospace;
        font-size: 14px;
        padding: 10px 0;
        border-bottom: 1px solid #e0e0e0;
    }
    .table-row:hover {
        background-color: #f8f9fa;
    }
    .field-name {
        display: inline-block;
        min-width: 320px;
        max-width: 320px;
        font-weight: bold;
    }
    .field-category {
        display: inline-block;
        min-width: 100px;
        max-width: 100px;
    }
    .field-count {
        display: inline-block;
        min-width: 120px;
        max-width: 120px;
        text-align: right;
    }
    .field-size {
        display: inline-block;
        min-width: 120px;
        max-width: 120px;
        text-align: right;
    }
    .field-date {
        display: inline-block;
        min-width: 140px;
        max-width: 140px;
    }
    .field-freq {
        display: inline-block;
        min-width: 120px;
        max-width: 120px;
    }
    .separator {
        color: #999;
        margin: 0 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 显示表列表
    for table in tables_info:
        # 格式化记录数
        row_count = table['row_count']
        if row_count >= 10000000:
            count_str = f"{row_count / 10000000:.2f}千万"
        elif row_count >= 10000:
            count_str = f"{row_count / 10000:.2f}万"
        else:
            count_str = f"{row_count:,}"

        # 格式化表大小
        size_mb = table['size_mb']
        if size_mb >= 1024:
            size_str = f"{size_mb / 1024:.2f} GB"
        else:
            size_str = f"{size_mb:.2f} MB"

        # 显示对齐的信息行
        info_html = f"""
        <div class="table-row">
            <span class="field-name">📊 {table['table_name']} ({table['chinese_name']})</span>
            <span class="separator">│</span>
            <span class="field-category">🏷️ {table['category']}</span>
            <span class="separator">│</span>
            <span class="field-count">📝 {count_str}条</span>
            <span class="separator">│</span>
            <span class="field-size">💾 {size_str}</span>
            <span class="separator">│</span>
            <span class="field-date">📅 {table['latest_date'] or '无数据'}</span>
            <span class="separator">│</span>
            <span class="field-freq">⏰ {table['update_frequency']}</span>
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)

        # 使用expander显示详情（可以点击展开）
        with st.expander("📋 查看表结构详情", expanded=False):
            # 表描述
            if table['description']:
                st.info(f"💡 **描述**: {table['description']}")

            # 获取表结构
            schema = metadata.get_table_schema(table['table_name'])

            if schema:
                st.markdown("**表结构**:")

                # 构建表结构数据
                schema_data = []
                for col in schema:
                    schema_data.append({
                        '字段名': col['column_name'],
                        '类型': col['data_type'],
                        '可空': '✓' if col['is_nullable'] else '✗',
                        '说明': col.get('comment', '-')
                    })

                # 显示为表格
                st.dataframe(
                    schema_data,
                    use_container_width=True,
                    hide_index=True,
                    height=min(400, 50 + len(schema_data) * 35)
                )

                # 导出选项
                col1, col2 = st.columns(2)

                with col1:
                    # CSV导出
                    import pandas as pd
                    df = pd.DataFrame(schema_data)
                    csv = df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        label="📥 导出CSV",
                        data=csv,
                        file_name=f"{table['table_name']}_schema.csv",
                        mime='text/csv',
                        key=f"csv_{table['table_name']}"
                    )

                with col2:
                    # Markdown导出
                    md_content = f"# {table['table_name']} 表结构\n\n"
                    md_content += f"**中文名**: {table['chinese_name']}\n\n"
                    md_content += f"**分类**: {table['category']}\n\n"
                    if table['description']:
                        md_content += f"**描述**: {table['description']}\n\n"
                    md_content += f"**更新频率**: {table['update_frequency']}\n\n"
                    md_content += "## 字段列表\n\n"
                    md_content += "| 字段名 | 类型 | 可空 | 说明 |\n"
                    md_content += "|--------|------|------|------|\n"
                    for col in schema:
                        md_content += f"| {col['column_name']} | {col['data_type']} | {'✓' if col['is_nullable'] else '✗'} | {col.get('comment', '-')} |\n"

                    st.download_button(
                        label="📄 导出Markdown",
                        data=md_content,
                        file_name=f"{table['table_name']}_schema.md",
                        mime='text/markdown',
                        key=f"md_{table['table_name']}"
                    )
            else:
                st.warning("⚠️ 无法获取表结构信息")