"""
日志系统

提供统一的日志记录功能
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def get_logger(name: str) -> logging.Logger:
    """
    获取Logger实例

    Args:
        name: Logger名称

    Returns:
        Logger实例
    """
    logger = logging.getLogger(name)

    # 如果logger已配置，直接返回
    if logger.handlers:
        return logger

    # 设置日志级别
    logger.setLevel(logging.INFO)

    # 创建日志目录
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    # 主日志文件路径
    log_file = log_dir / 'adata.log'

    # ERROR日志文件路径
    error_log_file = log_dir / 'ERROR.log'

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