"""
修复trade_calendar表PRIMARY KEY定义
从单字段主键改为联合主键(exchange, cal_date)
"""

import duckdb
from pathlib import Path

db_path = Path(__file__).parent.parent.parent.parent / 'database' / 'adata.db'

print("=" * 80)
print("修复trade_calendar表PRIMARY KEY定义")
print("=" * 80)
print(f"数据库路径: {db_path}")

# 连接数据库
conn = duckdb.connect(str(db_path))

print("\n步骤1: 备份trade_calendar数据...")
result = conn.execute("SELECT COUNT(*) FROM trade_calendar").fetchone()
original_count = result[0]
print(f"  原始数据量: {original_count}条")

if original_count > 0:
    # 创建临时备份表
    conn.execute("""
        CREATE TABLE IF NOT EXISTS trade_calendar_backup AS
        SELECT * FROM trade_calendar
    """)
    print("  ✅ 数据已备份到trade_calendar_backup")

print("\n步骤2: 删除旧的trade_calendar表...")
conn.execute("DROP TABLE IF EXISTS trade_calendar")
print("  ✅ 旧表已删除")

print("\n步骤3: 创建新表（联合主键：exchange + cal_date）...")
conn.execute("""
    CREATE TABLE trade_calendar (
        exchange VARCHAR(10),
        cal_date DATE,
        is_open INTEGER,
        pretrade_date DATE,

        PRIMARY KEY (exchange, cal_date),

        updated_at TIMESTAMP DEFAULT NOW()
    )
""")
print("  ✅ 新表已创建")

print("\n步骤4: 恢复数据...")
if original_count > 0:
    conn.execute("""
        INSERT INTO trade_calendar
        SELECT exchange, cal_date, is_open, pretrade_date, updated_at
        FROM trade_calendar_backup
    """)
    print("  ✅ 数据已恢复")

    print("\n步骤5: 清理备份表...")
    conn.execute("DROP TABLE trade_calendar_backup")
    print("  ✅ 备份表已删除")

print("\n步骤6: 创建索引...")
conn.execute("CREATE INDEX IF NOT EXISTS idx_trade_cal_date ON trade_calendar(cal_date)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_trade_cal_exchange ON trade_calendar(exchange)")
print("  ✅ 索引已创建")

print("\n步骤7: 验证修复结果...")
result = conn.execute("SELECT COUNT(*) FROM trade_calendar").fetchone()
final_count = result[0]
print(f"  最终数据量: {final_count}条")

if final_count == original_count:
    print("  ✅ 数据完整性验证通过")
    print("=" * 80)
    print("✅ trade_calendar表PRIMARY KEY修复完成")
    print("=" * 80)
else:
    print(f"  ❌ 数据丢失！原始{original_count}条，最终{final_count}条")
    print("=" * 80)
    print("❌ trade_calendar表PRIMARY KEY修复失败")
    print("=" * 80)

conn.close()