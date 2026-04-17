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


def initialize_database(db_path: str, force: bool = False) -> Database:
    """
    初始化数据库

    Args:
        db_path: 数据库文件路径
        force: 是否强制重建（删除已有数据库）

    Returns:
        Database实例
    """
    logger.info("=" * 80)
    logger.info("开始初始化数据库")
    logger.info("=" * 80)

    db_file = Path(db_path)

    # 如果强制重建，删除已有数据库
    if force and db_file.exists():
        logger.warning(f"强制重建模式：删除已有数据库文件 {db_file}")
        db_file.unlink()
        logger.info("数据库文件已删除")

    # 创建数据库实例
    logger.info(f"数据库路径: {db_path}")
    db = Database(db_path)

    # 查询现有表
    result = db.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'")
    existing_tables = [row[0] for row in result]

    # 期望的28张表（global_cursor + 27张数据表）
    expected_table_count = 28

    if len(existing_tables) >= expected_table_count and not force:
        logger.info(f"数据库已有完整Schema（{len(existing_tables)}张表）")
        logger.info("如需重建，请使用 --force 参数")
        return db

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
            # 如果表已存在，跳过（DuckDB CREATE TABLE IF NOT EXISTS）
            if "Table with name" in str(e) and "already exists" in str(e):
                logger.info(f"  表已存在，跳过: {schema_file.name}")
            else:
                logger.error(f"  Schema执行失败: {e}")
                raise

    # 验证表数量
    result2 = db.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'")
    final_tables = [row[0] for row in result2]

    logger.info("=" * 80)
    logger.info("✓ Schema初始化完成")
    logger.info(f"  表数量: {len(final_tables)}")
    logger.info("=" * 80)

    return db


def initialize_cursors(db_path: str, config_dir: str):
    """初始化游标表"""
    logger.info("初始化游标表...")

    cursor_manager = GlobalCursorManager(db_path, config_dir)
    cursor_manager.initialize()

    # 查询游标表数据
    db = Database(db_path)
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
    db_path_config = config.get('database', {}).get('path', 'database/adata.db')
    db_path = str(project_root / db_path_config)

    try:
        db = initialize_database(db_path, args.force)
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        sys.exit(1)

    # 3. 初始化游标
    try:
        config_dir = str(Path(args.config).parent)
        initialize_cursors(db_path, config_dir)
    except Exception as e:
        logger.error(f"游标初始化失败: {e}")
        sys.exit(1)

    logger.info("=" * 80)
    logger.info("✓ 数据库初始化完成")
    logger.info(f"  数据库路径: {db_path}")
    logger.info("=" * 80)
    logger.info("现在可以启动main.py了：")
    logger.info("  python code/backend/main.py")
    logger.info("=" * 80)


if __name__ == '__main__':
    main()
