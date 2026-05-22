"""
AData后端启动入口

功能：
1. 加载配置文件
2. 初始化Database、API、游标管理器
3. 自动数据拉取（如果enabled=true）
4. 启动定时任务调度器（定时快照、定时拉取）
5. Dashboard启动（可选）

使用方法：
    python code/backend/init_db.py                 # 首次部署：初始化数据库（仅执行一次）
    python code/backend/main.py                    # 启动后端（拉取数据+定时任务）
    python code/backend/main.py --fetch            # 仅拉取数据（一次性）
    python code/backend/main.py --scheduler        # 仅启动定时任务
    python code/backend/main.py --no-fetch         # 跳过初始拉取
    python code/backend/main.py --snapshot         # 立即创建快照

注意：首次部署请先运行 init_db.py 初始化数据库，再运行 main.py 启动服务
"""

import sys
import yaml
import argparse
from pathlib import Path
from datetime import datetime
import structlog

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
backend_path = project_root / 'code' / 'backend'
sys.path.insert(0, str(backend_path))

from src.core.database import Database
from src.core.tushare_api import TushareAPI
from src.core.global_cursor_manager import GlobalCursorManager
from src.core.logger import get_logger
from src.core.data_fetcher import DataFetcher
from src.scheduler.scheduler import DataScheduler

logger = get_logger(__name__)


def load_config(config_path: str) -> dict:
    """加载配置文件"""
    config_file = Path(config_path)
    if not config_file.exists():
        logger.error(f"配置文件不存在: {config_path}")
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    logger.info(f"配置文件加载成功: {config_path}")
    return config


def initialize_database(db_config: dict) -> Database:
    """
    连接PostgreSQL数据库并验证Schema完整性

    注意：此函数不会创建表结构。如需初始化数据库，请先运行：
        python code/backend/init_db.py
    """
    logger.info(f"连接PostgreSQL数据库: {db_config['host']}:{db_config['port']}/{db_config['database']}")

    db = Database(db_config)

    # 检查数据库是否有完整的表结构（28张表）
    result = db.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    existing_tables = [row[0] for row in result]

    # 期望的28张表（global_cursor + 27张数据表）
    expected_table_count = 28

    if len(existing_tables) < expected_table_count:
        logger.error("=" * 80)
        logger.error("❌ 数据库Schema不完整")
        logger.error("=" * 80)
        logger.error(f"数据库: {db_config['database']}")
        logger.error(f"现有表数: {len(existing_tables)}, 期望: {expected_table_count}")
        logger.error("")
        logger.error("请运行初始化脚本：")
        logger.error("  python code/backend/init_db.py")
        logger.error("=" * 80)
        raise RuntimeError(f"数据库Schema不完整（{len(existing_tables)}表），请运行 init_db.py")

    logger.info(f"✓ PostgreSQL连接成功（{len(existing_tables)}张表）")

    return db




def main():
    """主入口"""
    parser = argparse.ArgumentParser(description='AData后端启动')
    parser.add_argument('--config', default='code/backend/config/config.yaml', help='配置文件路径')
    parser.add_argument('--fetch', action='store_true', help='仅拉取数据（一次性）')
    parser.add_argument('--scheduler', action='store_true', help='仅启动定时任务调度器')
    parser.add_argument('--no-fetch', action='store_true', help='跳过初始数据拉取')

    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("AData后端启动")
    logger.info("=" * 80)
    logger.info(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. 加载配置
    try:
        config = load_config(args.config)
    except Exception as e:
        logger.error(f"配置加载失败: {e}")
        sys.exit(1)

    # 2. 初始化数据库和游标
    db_config = config.get('database', {})
    if not db_config:
        logger.error("配置文件缺少database配置")
        sys.exit(1)

    db = initialize_database(db_config)

    # 初始化游标表
    cursor_manager = GlobalCursorManager(db_config, str(Path(args.config).parent))
    cursor_manager.initialize()
    logger.info("游标表初始化完成")

    # 3. 初始化API
    api = TushareAPI(config['tushare'])
    logger.info(f"TushareAPI已初始化: {config['tushare']['api_url']}")

    # 模式1：仅拉取数据（一次性）
    if args.fetch:
        logger.info("启动模式：仅拉取数据（一次性）")
        fetcher = DataFetcher(db_config, config)
        logger.info("开始拉取数据...")
        fetcher.start()
        logger.info("✓ 数据拉取完成")
        return

    # 模式2：仅启动定时任务调度器
    if args.scheduler:
        logger.info("启动模式：仅启动定时任务调度器")
        scheduler = DataScheduler(config)
        scheduler.start()
        logger.info("✓ 定时任务调度器已启动，按Ctrl+C停止")

        # 查看任务状态
        status = scheduler.get_jobs_status()
        logger.info("定时任务状态：")
        for job_id, job_info in status.items():
            logger.info(f"  {job_info['name']}: 下次执行 {job_info['next_run_time']}")

        # 保持运行
        try:
            import time
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            scheduler.stop()
            logger.info("✓ 定时任务调度器已停止")
        return

    # 模式3：集成启动（默认）
    logger.info("启动模式：集成启动（先拉取数据，再启动调度器）")

    # 4. 项目启动时，先进行一次数据拉取
    fetch_enabled = config.get('fetch', {}).get('enabled', True)

    if not args.no_fetch and fetch_enabled:
        logger.info("项目启动，开始首次数据拉取...")
        logger.info("设置 running=True（数据正在拉取）")

        # 使用DataFetcher拉取数据（会自动设置running状态）
        fetcher = DataFetcher(db_config, config)
        fetcher.start()
        logger.info("✓ 首次数据拉取完成（running=False）")
    else:
        logger.info("首次数据拉取已禁用（fetch.enabled=false 或 --no-fetch）")

    # 6. 启动定时任务调度器（快照/checkpoint立即运行，数据拉取按check_interval检查）
    scheduler_config = config.get('scheduler', {})
    if scheduler_config.get('enabled', True):
        logger.info("启动定时任务调度器...")
        scheduler = DataScheduler(config)
        scheduler.start()
        logger.info("✓ 定时任务调度器已启动")

        # 查看任务状态
        status = scheduler.get_jobs_status()
        logger.info("定时任务状态：")
        for job_id, job_info in status.items():
            logger.info(f"  {job_info['name']}: 下次执行 {job_info['next_run_time']}")

        # 调度器会每隔check_interval检查running状态并执行数据拉取
        logger.info("调度器将每隔check_interval分钟检查running状态并拉取数据")
        logger.info("  - running=True → 跳过（任务正在运行）")
        logger.info("  - running=False → 启动拉取（任务未运行）")
        logger.info("按Ctrl+C停止...")

        # 保持运行
        try:
            import time
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            scheduler.stop()
            logger.info("✓ 定时任务调度器已停止")
    else:
        logger.info("定时任务已禁用（scheduler.enabled=false）")

    logger.info("=" * 80)
    logger.info("✓ AData后端启动完成")
    logger.info("=" * 80)


if __name__ == '__main__':
    main()