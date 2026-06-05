"""
AData数据库初始化脚本

功能：
1. 创建数据库文件（如果不存在）
2. 执行所有Schema文件创建完整表结构
3. 初始化游标表（global_cursor）

使用方法：
    python code/backend/init_db.py                    # 使用默认配置初始化
    python code/backend/init_db.py --config custom.yaml  # 使用自定义配置
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


def initialize_database(db_config: dict, force: bool = False) -> Database:
    """
    初始化数据库

    Args:
        db_config: 数据库配置字典
        force: 是否强制重建（删除已有表）

    Returns:
        Database实例
    """
    logger.info("=" * 80)
    logger.info("开始初始化PostgreSQL数据库")
    logger.info("=" * 80)

    logger.info(f"数据库: {db_config['host']}:{db_config['port']}/{db_config['database']}")

    # 创建数据库实例
    db = Database(db_config)

    # 查询现有表（PostgreSQL使用public schema）
    result = db.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    existing_tables = [row[0] for row in result]

    # 期望的22张表（global_cursor + 21张数据表）
    expected_table_count = 22

    if len(existing_tables) >= expected_table_count and not force:
        logger.info(f"数据库已有完整Schema（{len(existing_tables)}张表）")
        logger.info("如需重建，请使用 --force 参数")
        return db

    # 强制重建模式：删除所有表
    if force and len(existing_tables) > 0:
        logger.warning(f"强制重建模式：删除{len(existing_tables)}张已有表")
        for table_name in existing_tables:
            db.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
        logger.info("所有表已删除")

    # 执行Schema文件
    logger.info(f"当前表数: {len(existing_tables)}, 期望: {expected_table_count}")
    logger.info("开始执行Schema文件...")

    schema_dir = project_root / 'database' / 'schemas'
    schema_files = sorted(schema_dir.glob('*_schema.sql'))

    logger.info(f"找到{len(schema_files)}个Schema文件")

    for schema_file in schema_files:
        logger.info(f"执行: {schema_file.name}")
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        try:
            db.execute(schema_sql)
        except Exception as e:
            # PostgreSQL: 如果表已存在，跳过
            if "already exists" in str(e).lower():
                logger.info(f"  表已存在，跳过: {schema_file.name}")
            else:
                logger.error(f"  Schema执行失败: {e}")
                raise

    # 验证表数量
    result2 = db.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    final_tables = [row[0] for row in result2]

    logger.info("=" * 80)
    logger.info("✓ Schema初始化完成")
    logger.info(f"  表数量: {len(final_tables)}")
    logger.info("=" * 80)

    return db


def initialize_cursors(db_config: dict, config_dir: str):
    """初始化游标表"""
    logger.info("初始化游标表...")

    cursor_manager = GlobalCursorManager(db_config, config_dir)
    cursor_manager.initialize()

    # 查询游标表数据
    db = Database(db_config)
    cursor_count = db.execute("SELECT COUNT(*) FROM global_cursor")[0][0]

    logger.info(f"✓ 游标表初始化完成（{cursor_count}条记录）")


def main():
    """主入口"""
    parser = argparse.ArgumentParser(description='AData数据库初始化')
    parser.add_argument('--config', default='code/backend/config/config.yaml', help='配置文件路径')
    parser.add_argument('--force', action='store_true', help='强制重建数据库（删除已有文件）')

    args = parser.parse_args()

    logger.info("=" * 80)
    logger.info("AData数据库初始化")
    logger.info("=" * 80)
    logger.info(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if args.force:
        logger.warning("⚠️  强制重建模式已启用，已有数据库将被删除！")
    else:
        logger.info("安全模式：如需重建，请使用 --force 参数")

    # 1. 加载配置
    try:
        config = load_config(args.config)
    except Exception as e:
        logger.error(f"配置加载失败: {e}")
        sys.exit(1)

    # 2. 初始化数据库
    db_config = config.get('database', {})

    if not db_config:
        logger.error("配置文件缺少database配置")
        sys.exit(1)

    try:
        db = initialize_database(db_config, args.force)
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        sys.exit(1)

    # 3. 初始化游标
    try:
        config_dir = str(Path(args.config).parent)
        initialize_cursors(db_config, config_dir)
    except Exception as e:
        logger.error(f"游标初始化失败: {e}")
        sys.exit(1)

    logger.info("=" * 80)
    logger.info("✓ 数据库初始化完成")
    logger.info(f"  数据库: {db_config['host']}:{db_config['port']}/{db_config['database']}")
    logger.info("=" * 80)
    logger.info("现在可以启动main.py了：")
    logger.info("  python code/backend/main.py")
    logger.info("=" * 80)


if __name__ == '__main__':
    main()
