#!/usr/bin/env python3
"""
数据库重建脚本 - 直接在根目录执行
"""

import duckdb
import os
import shutil
from pathlib import Path
from datetime import datetime

def rebuild_database():
    """重建数据库"""
    print("=" * 60)
    print("数据库重建脚本")
    print("=" * 60)
    print()

    # 数据库路径（根目录）
    db_path = Path("database/adata.db")
    backup_dir = Path("database")

    # 备份旧数据库
    if db_path.exists():
        backup_name = f"adata.db.backup_before_rebuild_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = backup_dir / backup_name
        print(f"备份旧数据库到: {backup_path}")
        shutil.copy2(db_path, backup_path)
        print("✓ 备份完成")
        print()

        # 删除旧数据库
        print("删除旧数据库...")
        db_path.unlink()
        wal_path = Path(str(db_path) + ".wal")
        if wal_path.exists():
            wal_path.unlink()
        print("✓ 删除完成")
        print()

    # 创建新数据库
    print("创建新数据库...")
    conn = duckdb.connect(str(db_path))
    print(f"✓ 数据库创建成功: {db_path}")
    print()

    # 加载所有schema文件
    print("加载Schema文件...")
    schema_dir = Path("database/schemas")
    schema_files = sorted(schema_dir.glob("*_schema.sql"))
    schema_count = 0
    error_count = 0

    for schema_file in schema_files:
        table_name = schema_file.stem.replace("_schema", "")
        print(f"  加载: {table_name}")

        try:
            # 读取schema SQL
            with open(schema_file, 'r', encoding='utf-8') as f:
                sql = f.read()

            # 执行SQL
            conn.execute(sql)
            schema_count += 1
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            error_count += 1

    print()
    print(f"✓ 已加载 {schema_count} 个Schema文件")
    if error_count > 0:
        print(f"⚠️ 失败 {error_count} 个")
    print()

    # 验证表创建
    print("验证数据库表...")
    result = conn.execute("""
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_schema = 'main'
    """).fetchone()
    table_count = result[0]
    print(f"✓ 已创建 {table_count} 张表")
    print()

    # 显示表列表
    print("表列表:")
    tables = conn.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'main'
        ORDER BY table_name
    """).fetchall()

    for i, (table_name,) in enumerate(tables, 1):
        print(f"  {i}. {table_name}")

    print()

    # 统计信息
    print("=" * 60)
    print("✓ 数据库重建完成")
    print(f"  数据库路径: {db_path}")
    print(f"  表数量: {table_count}")
    if db_path.exists():
        print(f"  文件大小: {db_path.stat().st_size / 1024:.2f} KB")
    print("=" * 60)

    conn.close()

if __name__ == '__main__':
    rebuild_database()