#!/bin/bash
# 数据库重建脚本
# 使用新的schema文件重建完整数据库

set -e  # 遇到错误立即退出

echo "========================================"
echo "数据库重建脚本"
echo "========================================"
echo ""

# 数据库路径
DB_PATH="database/adata.db"
BACKUP_PATH="database/adata.db.backup_before_rebuild_$(date +%Y%m%d_%H%M%S)"

# 备份旧数据库
if [ -f "$DB_PATH" ]; then
    echo "备份旧数据库到: $BACKUP_PATH"
    cp "$DB_PATH" "$BACKUP_PATH"
    echo "✓ 备份完成"
    echo ""
fi

# 删除旧数据库
if [ -f "$DB_PATH" ]; then
    echo "删除旧数据库..."
    rm "$DB_PATH"
    rm -f "${DB_PATH}.wal"
    echo "✓ 删除完成"
    echo ""
fi

# 创建新数据库
echo "创建新数据库..."
duckdb "$DB_PATH" "SELECT 1;" > /dev/null 2>&1
echo "✓ 数据库创建成功: $DB_PATH"
echo ""

# 加载所有schema文件
echo "加载Schema文件..."
SCHEMA_DIR="database/schemas"
SCHEMA_COUNT=0

for schema_file in "$SCHEMA_DIR"/*_schema.sql; do
    if [ -f "$schema_file" ]; then
        table_name=$(basename "$schema_file" _schema.sql)
        echo "  加载: $table_name"
        duckdb "$DB_PATH" < "$schema_file" > /dev/null 2>&1
        SCHEMA_COUNT=$((SCHEMA_COUNT + 1))
    fi
done

echo ""
echo "✓ 已加载 $SCHEMA_COUNT 个Schema文件"
echo ""

# 验证表创建
echo "验证数据库表..."
TABLE_COUNT=$(duckdb "$DB_PATH" -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'main';" | tail -1)
echo "✓ 已创建 $TABLE_COUNT 张表"
echo ""

# 显示表列表
echo "表列表:"
duckdb "$DB_PATH" -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY table_name;" | tail -n +2
echo ""

echo "========================================"
echo "✓ 数据库重建完成"
echo "  数据库路径: $DB_PATH"
echo "  表数量: $TABLE_COUNT"
echo "  备份位置: $BACKUP_PATH"
echo "========================================"