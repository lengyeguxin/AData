"""
Dashboard配置模块

提供Dashboard专用的配置管理功能
"""

from .dashboard_config_manager import (
    DashboardConfigManager,
    get_dashboard_config_manager
)

__all__ = [
    'DashboardConfigManager',
    'get_dashboard_config_manager'
]

# 默认配置文件路径
DEFAULT_CONFIG_PATH = "config/dashboard_config.yaml"
