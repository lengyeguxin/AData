"""
Dashboard配置管理器使用示例

展示如何在Dashboard中使用新的配置管理器
"""

# 方式1：使用默认配置文件
from dashboard.config import get_dashboard_config_manager

# 获取全局配置管理器实例（单例模式）
config = get_dashboard_config_manager()

# 方式2：指定配置文件路径
# from dashboard.config.dashboard_config_manager import DashboardConfigManager
# config = DashboardConfigManager(config_path="/path/to/custom_config.yaml")


# ==================== 数据库配置 ====================
db_config = config.get_database_config()
print(f"数据库类型: {config.get_database_type()}")

# 获取快照数据库路径（Dashboard只使用快照，避免多个项目间的数据冲突）
db_path = config.get_database_path()
print(f"数据库路径: {db_path}")


# ==================== 日志配置 ====================
log_level = config.get_log_level()
log_file = config.get_log_file()
print(f"日志级别: {log_level}, 日志文件: {log_file}")


# ==================== 服务器配置 ====================
host = config.get_server_host()
port = config.get_server_port()
debug = config.is_debug_mode()
print(f"服务器地址: {host}:{port}, 调试模式: {debug}")


# ==================== 性能配置 ====================
if config.is_cache_enabled():
    cache_config = config.get_cache_config()
    print(f"缓存已启用, TTL: {cache_config.get('ttl')}秒")

page_size = config.get_default_page_size()
max_page_size = config.get_max_page_size()
print(f"分页配置: 默认{page_size}条/页, 最大{max_page_size}条/页")

timeout = config.get_query_timeout()
print(f"查询超时: {timeout}秒")


# ==================== UI配置 ====================
theme = config.get_theme()
title = config.get_page_title()
refresh_interval = config.get_refresh_interval()
print(f"主题: {theme}, 标题: {title}")
print(f"自动刷新间隔: {refresh_interval}秒" if refresh_interval > 0 else "不自动刷新")


# ==================== 安全配置 ====================
if config.is_cors_enabled():
    origins = config.get_allowed_origins()
    print(f"CORS已启用, 允许的来源: {origins}")


# ==================== 动态更新配置 ====================

# 更新服务器配置
config.update_section('server', {
    'port': 8080,
    'debug': True
})

# 更新UI配置
config.update_section('ui', {
    'theme': 'dark',
    'refresh_interval': 30
})

# 保存配置
config.save_config()
print("配置已更新并保存")


# ==================== 在Flask应用中使用示例 ====================
"""
from flask import Flask
from dashboard.config import get_dashboard_config_manager

# 初始化配置
config = get_dashboard_config_manager()

# 创建Flask应用
app = Flask(__name__)

# 使用配置
app.run(
    host=config.get_server_host(),
    port=config.get_server_port(),
    debug=config.is_debug_mode()
)
"""
