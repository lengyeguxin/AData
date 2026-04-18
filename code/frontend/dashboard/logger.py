"""
Dashboard日志系统

提供Dashboard专用的日志记录功能，日志输出到独立的文件
"""

import logging
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


def setup_dashboard_logger(config_path: Optional[str] = None) -> logging.Logger:
    """
    设置Dashboard日志系统

    Args:
        config_path: 配置文件路径（可选，默认使用dashboard/config/dashboard_config.yaml）

    Returns:
        Logger实例
    """
    logger = logging.getLogger('dashboard')

    # 如果logger已配置，直接返回
    if logger.handlers:
        return logger

    # 加载配置文件
    if config_path is None:
        # 默认配置文件路径
        config_path = str(Path(__file__).parent / 'dashboard_config.yaml')

    log_config = _load_logging_config(config_path)

    # 设置日志级别
    level = log_config.get('level', 'INFO')
    logger.setLevel(getattr(logging, level))

    # 创建日志目录
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    # 从配置读取日志文件路径
    log_file_name = log_config.get('file', 'dashboard.log')
    error_log_file_name = log_config.get('error_file', 'dashboard-error.log')

    log_file = log_dir / Path(log_file_name).name
    error_log_file = log_dir / Path(error_log_file_name).name

    # 主文件处理器（INFO及以上级别）
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # ERROR文件处理器（只记录ERROR及以上级别）
    error_file_handler = logging.FileHandler(error_log_file, encoding='utf-8')
    error_file_handler.setLevel(logging.ERROR)

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    error_file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(error_file_handler)
    logger.addHandler(console_handler)

    return logger


def _load_logging_config(config_path: str) -> Dict[str, Any]:
    """
    从配置文件加载日志配置

    Args:
        config_path: 配置文件路径

    Returns:
        日志配置字典
    """
    try:
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config.get('logging', {})
        else:
            # 配置文件不存在，返回默认配置
            return {
                'level': 'INFO',
                'file': 'dashboard.log',
                'error_file': 'dashboard-error.log'
            }
    except Exception as e:
        # 加载失败，返回默认配置
        return {
            'level': 'INFO',
            'file': 'dashboard.log',
            'error_file': 'dashboard-error.log'
        }


def get_dashboard_logger() -> logging.Logger:
    """
    获取Dashboard Logger实例（单例模式）

    Returns:
        Logger实例
    """
    return setup_dashboard_logger()