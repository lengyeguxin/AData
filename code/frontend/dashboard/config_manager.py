"""
配置管理模块

负责读取、更新和管理系统配置
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List
import logging

# 使用Dashboard专用logger
from dashboard.logger import get_dashboard_logger

logger = get_dashboard_logger()


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: str = "../config/config.yaml"):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径（默认使用backend配置）
        """
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
                    logger.info(f"Configuration loaded from {self.config_path}")
                    return config
            else:
                logger.warning(f"Configuration file not found: {self.config_path}")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """
        获取默认配置

        Returns:
            默认配置字典
        """
        return {
            'tushare': {
                'token': '',
                'api_url': 'http://api.tushare.pro',
                'rate_limit': 500
            },
            'dashboard': {
                'database': {
                    'path': 'database/adata_snapshot.db',
                    'fallback': 'database/adata.db',
                    'use_snapshot': True
                }
            },
            'database': {
                'path': 'database/adata.db',
                'type': 'duckdb'
            },
            'fetch': {
                'enabled': True,
                'start_date': '20210101',
                'check_interval': 60
            },
            'snapshot': {
                'enabled': True,
                'interval': 60,
                'locations': [
                    'database/adata_snapshot.db',
                    '/home/my/claude-project/AiStock/database/adata_snapshot.db'
                ]
            },
            'history_import': {
                'start_date': '20210101',
                'batch_size': 100,
                'concurrent_workers': 10
            },
            'scheduler': {
                'daily_update_time': '18:00',
                'weekly_update_time': '18:00',
                'monthly_update_time': '18:00'
            },
            'data_collection': {
                'enabled_tables': []
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

            logger.info(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False

    def update_section(self, section: str, values: Dict[str, Any]) -> bool:
        """
        更新配置的某个部分

        Args:
            section: 配置部分名称（如'tushare'、'database'）
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
            logger.error(f"Failed to update configuration section {section}: {e}")
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

    def get_tushare_config(self) -> Dict[str, Any]:
        """获取Tushare配置"""
        return self.get_section('tushare')

    def get_import_config(self) -> Dict[str, Any]:
        """获取数据导入配置"""
        return self.get_section('history_import')

    def get_scheduler_config(self) -> Dict[str, Any]:
        """获取调度配置"""
        return self.get_section('scheduler')

    def get_fetch_config(self) -> Dict[str, Any]:
        """获取数据拉取配置"""
        return self.get_section('fetch')

    def get_snapshot_config(self) -> Dict[str, Any]:
        """获取快照配置"""
        return self.get_section('snapshot')

    def get_dashboard_database_config(self) -> Dict[str, Any]:
        """
        获取Dashboard数据库配置（读写分离）

        Returns:
            Dashboard数据库配置字典 {
                'path': 快照数据库路径,
                'fallback': 主数据库路径（备用）,
                'use_snapshot': 是否使用快照模式
            }
        """
        dashboard_config = self.get_section('dashboard')
        if 'database' in dashboard_config:
            return dashboard_config['database']
        else:
            # 如果没有配置dashboard.database，使用默认快照配置
            return {
                'path': 'database/adata_snapshot.db',
                'fallback': 'database/adata.db',
                'use_snapshot': True
            }

    def get_enabled_tables(self) -> List[str]:
        """
        获取已启用的数据表列表

        Returns:
            启用的表名列表
        """
        data_collection = self.get_section('data_collection')
        return data_collection.get('enabled_tables', [])

    def set_enabled_tables(self, tables: List[str]) -> bool:
        """
        设置已启用的数据表列表

        Args:
            tables: 表名列表

        Returns:
            是否成功设置
        """
        return self.update_section('data_collection', {'enabled_tables': tables})

    def is_table_enabled(self, table_name: str) -> bool:
        """
        检查某个表是否启用

        Args:
            table_name: 表名

        Returns:
            是否启用
        """
        enabled_tables = self.get_enabled_tables()
        # 如果没有设置enabled_tables，默认所有表都启用
        if not enabled_tables:
            return True
        return table_name in enabled_tables

    def get_all_tables_with_status(self) -> List[Dict[str, Any]]:
        """
        获取所有表及其启用状态

        Returns:
            表信息列表，包含表名、中文名、分类、启用状态
        """
        from dashboard.utils.table_info import TABLE_INFO, get_rolling_table_info

        enabled_tables = self.get_enabled_tables()
        all_tables = []

        # 添加固定表
        for table_name, info in TABLE_INFO.items():
            is_enabled = table_name in enabled_tables if enabled_tables else True
            all_tables.append({
                'table_name': table_name,
                'chinese_name': info['chinese_name'],
                'category': info['category'],
                'enabled': is_enabled
            })

        # 添加滚动表（如果存在）
        # 这里可以动态查询数据库获取滚动表

        return all_tables