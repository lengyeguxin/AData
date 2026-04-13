"""
AData后端启动入口

功能：
1. 加载配置文件
2. 初始化Database、API、游标管理器
3. 自动数据拉取（如果enabled=true）
4. 定时快照生成
5. 启动调度器（定时任务）

使用方法：
    python code/backend/main.py
    python code/backend/main.py --no-fetch  # 跳过初始拉取
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


def initialize_database(db_path: str) -> Database:
    """初始化数据库"""
    logger.info(f"初始化数据库: {db_path}")
    db = Database(db_path)
    return db


def create_snapshot(db_path: str, snapshot_locations: list) -> bool:
    """创建快照（双位置备份）"""
    import shutil
    from datetime import datetime

    logger.info(f"开始创建快照: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        db_file = Path(db_path)
        if not db_file.exists():
            logger.warning(f"数据库文件不存在，跳过快照: {db_path}")
            return False

        # 创建快照到多个位置
        for location in snapshot_locations:
            snapshot_path = Path(location)
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(db_file, snapshot_path)
            logger.info(f"快照已创建: {snapshot_path}")

        logger.info("✓ 快照创建成功（双位置备份）")
        return True

    except Exception as e:
        logger.error(f"快照创建失败: {e}")
        return False


def main():
    """主入口"""
    parser = argparse.ArgumentParser(description='AData后端启动')
    parser.add_argument('--config', default='code/backend/config/config.yaml', help='配置文件路径')
    parser.add_argument('--no-fetch', action='store_true', help='跳过初始数据拉取')
    parser.add_argument('--snapshot', action='store_true', help='立即创建快照')

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
    db_path = str(project_root / 'database' / 'adata.db')
    db = initialize_database(db_path)

    # 初始化游标表
    cursor_manager = GlobalCursorManager(db_path, str(Path(args.config).parent))
    cursor_manager.initialize()
    logger.info("游标表初始化完成")

    # 3. 初始化API
    api = TushareAPI(config['tushare'])
    logger.info(f"TushareAPI已初始化: {config['tushare']['api_url']}")

    # 4. 检查数据拉取开关
    fetch_enabled = config.get('fetch', {}).get('enabled', True)

    if not args.no_fetch and fetch_enabled:
        logger.info("数据拉取已启用（fetch.enabled=true）")
        logger.info("提示：完整DataFetcher功能将在后续版本实现")
        logger.info("当前版本：仅初始化游标系统，具体拉取需手动执行Collector")
    else:
        logger.info("数据拉取已禁用（fetch.enabled=false 或 --no-fetch）")

    # 5. 立即创建快照（如果指定）
    if args.snapshot:
        snapshot_config = config.get('snapshot', {})
        if snapshot_config.get('enabled', True):
            snapshot_locations = snapshot_config.get('locations', ['database/adata_snapshot.db'])
            create_snapshot(db_path, snapshot_locations)
        else:
            logger.info("快照功能已禁用（snapshot.enabled=false）")

    # 6. 启动调度器（定时任务）
    # TODO: 开发Scheduler完整功能（Phase 3后续开发）

    logger.info("=" * 80)
    logger.info("✓ AData后端初始化完成")
    logger.info("=" * 80)
    logger.info("下一步操作:")
    logger.info("  1. 手动测试Collector: python code/backend/src/collectors/daily_collector.py")
    logger.info("  2. 创建快照: python code/backend/main.py --snapshot")
    logger.info("  3. 查看游标状态: SELECT * FROM global_cursor;")
    logger.info("=" * 80)


if __name__ == '__main__':
    main()