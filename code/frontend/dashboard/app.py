"""
A股数据库监控面板 - 主应用

基于Streamlit构建的数据库监控和可视化系统
"""

import streamlit as st
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 初始化Dashboard日志系统
from dashboard.logger import setup_dashboard_logger
setup_dashboard_logger()

from dashboard.metadata import DatabaseMetadata
from dashboard.config import get_dashboard_config_manager
from dashboard.components.overview import render_overview
from dashboard.components.table_list import render_table_list
from dashboard.components.table_detail import render_table_detail
from dashboard.components.charts import render_charts
from dashboard.components.settings import render_settings
from dashboard.components.fetch_control import render_fetch_control


# 页面配置
st.set_page_config(
    page_title="A股数据库监控",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "A股数据库监控系统 - 监控数据库状态和数据质量"
    }
)

# 应用标题
st.title("📊 A股数据库监控面板")
st.markdown("---")

# 侧边栏 - 导航
st.sidebar.title("导航")

# 初始化session state
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'overview'

if 'selected_table' not in st.session_state:
    st.session_state['selected_table'] = None

# 页面映射
page_mapping = {
    "整体概览": "overview",
    "数据表列表": "table_list",
    "图表分析": "charts",
    "数据拉取控制": "fetch_control",
    "系统配置": "settings"
}

page_mapping_reverse = {v: k for k, v in page_mapping.items()}

# 导航回调函数
def on_navigation_change():
    """当导航改变时调用"""
    selected = st.session_state['navigation_select']
    st.session_state['current_page'] = page_mapping[selected]

# 页面选择
# 如果是table_detail页面，应该显示"数据表列表"选项
display_page = st.session_state['current_page']
if display_page == 'table_detail':
    display_page = 'table_list'

# 获取当前显示的页面名称
current_view = page_mapping_reverse.get(display_page, "整体概览")

selected_view = st.sidebar.radio(
    "选择视图",
    ["整体概览", "数据表列表", "图表分析", "数据拉取控制", "系统配置"],
    index=["整体概览", "数据表列表", "图表分析", "数据拉取控制", "系统配置"].index(current_view),
    key="navigation_select",
    on_change=on_navigation_change
)

# 侧边栏信息
st.sidebar.markdown("---")
st.sidebar.markdown("### 数据库信息")

# 获取配置管理器（用于获取数据库路径）
dashboard_config = get_dashboard_config_manager()
db_path = dashboard_config.get_database_path()

# 获取元数据查询器（提前获取，用于显示信息）
metadata_temp = DatabaseMetadata(db_path, use_snapshot=True)
db_display_path = metadata_temp.db_path
snapshot_status = "快照副本只读" if metadata_temp.using_snapshot else "主数据库"

st.sidebar.info(f"""
**数据库**: {db_display_path}

**模式**: {snapshot_status}

**总表数**: 查看"整体概览"

**更新时间**: 快照创建时
""")

# 缓存元数据查询器（整个会话期间只创建一次）
@st.cache_resource
def get_metadata():
    """缓存元数据查询器（使用快照数据库）"""
    # 从Dashboard配置管理器获取数据库路径
    dashboard_config = get_dashboard_config_manager()
    db_path = dashboard_config.get_database_path()

    # 创建元数据查询器，使用快照模式
    metadata = DatabaseMetadata(db_path, use_snapshot=True)

    # 显示提示信息
    if metadata.using_snapshot:
        st.sidebar.success("✅ 使用快照数据库读取数据（只读模式）")

    return metadata

@st.cache_resource
def get_config_manager():
    """缓存配置管理器（使用旧的ConfigManager用于数据拉取控制等）"""
    # 保留旧的ConfigManager以兼容数据拉取控制等功能
    from dashboard.config_manager import ConfigManager
    return ConfigManager("../../backend/config/config.yaml")

# 获取元数据查询器和配置管理器
metadata = get_metadata()
config_manager = get_config_manager()
dashboard_config = get_dashboard_config_manager()

# 根据选择渲染不同页面
try:
    if st.session_state['current_page'] == 'overview':
        render_overview(metadata)

    elif st.session_state['current_page'] == 'table_list':
        render_table_list(metadata)

    elif st.session_state['current_page'] == 'table_detail':
        render_table_detail(metadata)

    elif st.session_state['current_page'] == 'charts':
        render_charts(metadata)

    elif st.session_state['current_page'] == 'fetch_control':
        render_fetch_control(config_manager)

    elif st.session_state['current_page'] == 'settings':
        render_settings(config_manager)

except Exception as e:
    st.error(f"页面加载失败: {e}")
    with st.expander("查看错误详情"):
        import traceback
        st.code(traceback.format_exc())

# 页脚
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    A股数据库监控系统 v1.0.0<br>
    Powered by Streamlit & DuckDB
</div>
""", unsafe_allow_html=True)