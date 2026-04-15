"""
Dashboard配置管理模块

负责读取和管理Dashboard专用的配置
不依赖后端数据拉取服务的配置
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
import structlog

logger = structlog.get_logger()


class DashboardConfigManager:
    """Dashboard配置管理器"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化Dashboard配置管理器

        Args:
            config_path: 配置文件路径（默认使用config/dashboard_config.yaml）
        """
        if config_path is None:
            # 默认使用dashboard/config目录下的配置文件
            config_dir = Path(__file__).parent
            self.config_path = config_dir / "dashboard_config.yaml"
        else:
            self.config_path = Path(config_path)

        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件

        Returns:
            配置字典
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    logger.info("Dashboard configuration loaded", path=str(self.config_path))
                    return config
            else:
                logger.warning("Dashboard configuration file not found, using defaults",
                             path=str(self.config_path))
                return self._get_default_config()
        except Exception as e:
            logger.error("Failed to load dashboard configuration", error=str(e))
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置

        Returns:
            默认配置字典
        """
        return {
            'database': {
                'path': 'database/adata_snapshot.db',
                'type': 'duckdb'
            },
            'logging': {
                'level': 'INFO',
                'file': 'logs/dashboard.log',
                'max_size': '10MB',
                'backup_count': 5,
                'format': 'json'
            },
            'server': {
                'host': '0.0.0.0',
                'port': 5000,
                'debug': False,
                'reload': False
            },
            'performance': {
                'cache': {
                    'enabled': True,
                    'ttl': 300,
                    'max_size': 1000
                },
                'pagination': {
                    'default_page_size': 100,
                    'max_page_size': 1000
                },
                'timeout': {
                    'default': 30,
                    'max': 300
                }
            },
            'ui': {
                'theme': 'light',
                'page_title': 'AData数据可视化平台',
                'refresh_interval': 60,
                'show_table_row_count': True,
                'enable_table_filter': True
            },
            'security': {
                'enable_cors': True,
                'allowed_origins': ['*'],
                'max_request_size': '10MB'
            }
        }

    def save_config(self) -> bool:
        """
        保存配置到文件

        Returns:
            是否成功保存
        """
        try:
            # 确保配置目录存在
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)

            logger.info("Dashboard configuration saved", path=str(self.config_path))
            return True
        except Exception as e:
            logger.error("Failed to save dashboard configuration", error=str(e))
            return False

    def update_section(self, section: str, values: Dict[str, Any]) -> bool:
        """
        更新配置的某个部分

        Args:
            section: 配置部分名称（如'database'、'logging'）
            values: 新的配置值

        Returns:
            是否成功更新
        """
        try:
            if section not in self.config:
                self.config[section] = {}

            self.config[section].update(values)
            return self.save_config()
        except Exception as e:
            logger.error("Failed to update dashboard configuration section",
                        section=section, error=str(e))
            return False

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        获取配置的某个部分

        Args:
            section: 配置部分名称

        Returns:
            配置字典
        """
        return self.config.get(section, {})

    # ==================== 数据库配置相关方法 ====================

    def get_database_config(self) -> Dict[str, Any]:
        """
        获取数据库配置

        Returns:
            数据库配置字典
        """
        return self.get_section('database')

    def get_database_path(self) -> str:
        """
        获取数据库路径

        Returns:
            快照数据库路径
        """
        return self.get_database_config().get('path', 'database/adata_snapshot.db')

    def get_database_type(self) -> str:
        """
        获取数据库类型

        Returns:
            数据库类型（如 'duckdb'）
        """
        return self.get_database_config().get('type', 'duckdb')

    # ==================== 日志配置相关方法 ====================

    def get_logging_config(self) -> Dict[str, Any]:
        """
        获取日志配置

        Returns:
            日志配置字典
        """
        return self.get_section('logging')

    def get_log_level(self) -> str:
        """获取日志级别"""
        return self.get_logging_config().get('level', 'INFO')

    def get_log_file(self) -> str:
        """获取日志文件路径"""
        return self.get_logging_config().get('file', 'logs/dashboard.log')

    # ==================== 服务器配置相关方法 ====================

    def get_server_config(self) -> Dict[str, Any]:
        """
        获取服务器配置

        Returns:
            服务器配置字典
        """
        return self.get_section('server')

    def get_server_host(self) -> str:
        """获取服务器监听地址"""
        return self.get_server_config().get('host', '0.0.0.0')

    def get_server_port(self) -> int:
        """获取服务器监听端口"""
        return self.get_server_config().get('port', 5000)

    def is_debug_mode(self) -> bool:
        """是否开启调试模式"""
        return self.get_server_config().get('debug', False)

    # ==================== 性能配置相关方法 ====================

    def get_performance_config(self) -> Dict[str, Any]:
        """
        获取性能配置

        Returns:
            性能配置字典
        """
        return self.get_section('performance')

    def get_cache_config(self) -> Dict[str, Any]:
        """获取查询缓存配置"""
        return self.get_performance_config().get('cache', {})

    def is_cache_enabled(self) -> bool:
        """是否启用查询缓存"""
        return self.get_cache_config().get('enabled', True)

    def get_pagination_config(self) -> Dict[str, Any]:
        """获取分页配置"""
        return self.get_performance_config().get('pagination', {})

    def get_default_page_size(self) -> int:
        """获取默认每页条数"""
        return self.get_pagination_config().get('default_page_size', 100)

    def get_max_page_size(self) -> int:
        """获取最大每页条数"""
        return self.get_pagination_config().get('max_page_size', 1000)

    def get_query_timeout(self) -> int:
        """获取默认查询超时（秒）"""
        timeout_config = self.get_performance_config().get('timeout', {})
        return timeout_config.get('default', 30)

    def get_max_query_timeout(self) -> int:
        """获取最大查询超时（秒）"""
        timeout_config = self.get_performance_config().get('timeout', {})
        return timeout_config.get('max', 300)

    # ==================== UI配置相关方法 ====================

    def get_ui_config(self) -> Dict[str, Any]:
        """
        获取UI配置

        Returns:
            UI配置字典
        """
        return self.get_section('ui')

    def get_theme(self) -> str:
        """获取主题"""
        return self.get_ui_config().get('theme', 'light')

    def get_page_title(self) -> str:
        """获取页面标题"""
        return self.get_ui_config().get('page_title', 'AData数据可视化平台')

    def get_refresh_interval(self) -> int:
        """获取数据自动刷新间隔（秒），0表示不自动刷新"""
        return self.get_ui_config().get('refresh_interval', 60)

    def is_table_row_count_visible(self) -> bool:
        """是否显示表行数统计"""
        return self.get_ui_config().get('show_table_row_count', True)

    def is_table_filter_enabled(self) -> bool:
        """是否启用表筛选功能"""
        return self.get_ui_config().get('enable_table_filter', True)

    # ==================== 安全配置相关方法 ====================

    def get_security_config(self) -> Dict[str, Any]:
        """
        获取安全配置

        Returns:
            安全配置字典
        """
        return self.get_section('security')

    def is_cors_enabled(self) -> bool:
        """是否启用CORS"""
        return self.get_security_config().get('enable_cors', True)

    def get_allowed_origins(self) -> List[str]:
        """获取允许的跨域来源"""
        return self.get_security_config().get('allowed_origins', ['*'])


# 全局配置管理器实例（单例模式）
_config_manager_instance: Optional[DashboardConfigManager] = None


def get_dashboard_config_manager(config_path: Optional[str] = None) -> DashboardConfigManager:
    """
    获取Dashboard配置管理器实例（单例模式）

    Args:
        config_path: 配置文件路径（仅在第一次调用时生效）

    Returns:
        Dashboard配置管理器实例
    """
    global _config_manager_instance

    if _config_manager_instance is None:
        _config_manager_instance = DashboardConfigManager(config_path)

    return _config_manager_instance
