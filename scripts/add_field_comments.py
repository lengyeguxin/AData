"""
批量执行SQL字段注释脚本
执行COMMENT ON COLUMN语句为所有表字段添加中文注释
"""

import duckdb
import sys
from pathlib import Path

# 项目根目录
project_root = Path(__file__).parent.parent
db_path = project_root / 'database' / 'adata.db'

def execute_comments_sql(sql_file: str):
    """执行注释SQL文件"""
    print(f"执行字段注释SQL: {sql_file}")

    # 连接数据库
    conn = duckdb.connect(str(db_path))

    # 读取SQL文件
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # 分割SQL语句（每条COMMENT ON语句单独执行）
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip() and not stmt.strip().startswith('--')]

    success_count = 0
    failed_count = 0

    for stmt in statements:
        if stmt:
            try:
                conn.execute(stmt)
                success_count += 1
            except Exception as e:
                print(f"失败: {stmt[:50]}... - {e}")
                failed_count += 1

    conn.close()

    print(f"✅ 成功执行 {success_count} 条语句")
    if failed_count > 0:
        print(f"❌ 失败 {failed_count} 条语句")

    return success_count, failed_count

if __name__ == '__main__':
    # 执行P0表注释
    sql_file = project_root / 'database' / 'schemas' / 'p0_comments.sql'

    if sql_file.exists():
        success, failed = execute_comments_sql(str(sql_file))
        print(f"\n完成！成功{success}条，失败{failed}条")
    else:
        print(f"❌ SQL文件不存在: {sql_file}")
        sys.exit(1)