# DuckDB数据查看指南

**问题：** DuckDB作为嵌入式数据库，没有独立数据库服务器和GUI工具（如pgAdmin），不便于直接查看数据。

**解决方案：** 提供多种数据查看方法，满足不同需求。

---

## 方法1：Python脚本查看（推荐）

### 工具位置
`scripts/view_duckdb_data.py`

### 功能
- ✅ 列出所有表
- ✅ 查看单表数据（支持WHERE条件、LIMIT限制、排序）
- ✅ 自定义SQL查询
- ✅ 导出数据到CSV
- ✅ 显示表统计信息（表结构、记录数、日期范围）

### 使用示例

```bash
cd /home/my/claude-project/AData

# 1. 查看所有表
python3 scripts/view_duckdb_data.py --list-tables

# 2. 查看stock_daily最新20条
python3 scripts/view_duckdb_data.py --table stock_daily --limit 20

# 3. 查看特定股票数据（平安银行）
python3 scripts/view_duckdb_data.py --table stock_daily \
  --where "ts_code='000001.SZ'" \
  --limit 20

# 4. 查看特定日期数据
python3 scripts/view_duckdb_data.py --table stock_daily \
  --where "trade_date='2026-04-09'" \
  --limit 50

# 5. 自定义SQL查询（市场统计）
python3 scripts/view_duckdb_data.py --sql \
  "SELECT trade_date, COUNT(*) as stock_count, AVG(pct_chg) as avg_change
   FROM stock_daily
   WHERE trade_date >= '2026-04-01'
   GROUP BY trade_date
   ORDER BY trade_date DESC
   LIMIT 10"

# 6. 导出数据到CSV
python3 scripts/view_duckdb_data.py --table stock_daily \
  --export tmp/stock_daily_export.csv \
  --limit 1000

# 7. 查看表统计信息
python3 scripts/view_duckdb_data.py --table stock_daily --stats
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--list-tables` | 列出所有表 | `--list-tables` |
| `--table` | 指定表名 | `--table stock_daily` |
| `--limit` | 显示记录数限制 | `--limit 20` |
| `--where` | WHERE条件 | `--where "ts_code='000001.SZ'"` |
| `--order-by` | 排序字段 | `--order-by "trade_date DESC"` |
| `--sql` | 自定义SQL查询 | `--sql "SELECT ..."` |
| `--export` | 导出CSV文件路径 | `--export tmp/output.csv` |
| `--stats` | 显示表统计信息 | `--stats` |

---

## 方法2：DuckDB CLI命令行工具

### 安装

```bash
# Ubuntu/Debian
wget https://github.com/duckdb/duckdb/releases/download/v0.10.0/duckdb_cli-linux-amd64.zip
unzip duckdb_cli-linux-amd64.zip
sudo mv duckdb /usr/local/bin/

# 或使用Python安装
pip install duckdb-cli
```

### 使用示例

```bash
# 启动DuckDB CLI（交互式）
duckdb database/adata.db

# DuckDB CLI交互示例
D SELECT table_name FROM duckdb_tables();
D SELECT * FROM stock_daily LIMIT 10;
D DESCRIBE stock_daily;

# 直接执行SQL（非交互）
duckdb database/adata.db -c "SELECT COUNT(*) FROM stock_daily"

# 导出数据到CSV
duckdb database/adata.db -c "COPY stock_daily TO 'stock_daily.csv' (HEADER, DELIMITER ',')"
```

---

## 方法3：DBeaver GUI工具（推荐可视化）

### 安装DBeaver

```bash
# Ubuntu/Debian
sudo snap install dbeaver-ce

# 或下载安装包
wget https://dbeaver.io/files/dbeaver-ce-latest-linux.deb
sudo dpkg -i dbeaver-ce-latest-linux.deb
```

### 配置DuckDB连接

1. 打开DBeaver
2. 点击"新建连接" → 选择"DuckDB"
3. 配置连接：
   - **数据库路径：** `/home/my/claude-project/AData/database/adata.db`
   - **驱动：** DuckDB JDBC驱动（DBeaver会自动下载）
4. 测试连接 → 连接成功后可查看所有表和数据

### DBeaver功能
- ✅ 可视化查看表结构
- ✅ 数据表格显示（支持排序、筛选）
- ✅ SQL编辑器（语法高亮、自动补全）
- ✅ 数据导出（CSV、Excel、SQL）
- ✅ ER图生成（表关系可视化）

---

## 方法4：使用Dashboard查看（已集成）

### 启动Dashboard

```bash
cd /home/my/claude-project/AData/code/frontend
python3 -m streamlit run dashboard/app.py
```

访问：http://localhost:8501

### Dashboard查看功能

**数据表列表页面：**
- 查看所有表列表
- 查看表结构详情（字段名、类型、说明）
- 查看表数据记录数、最新数据时间
- 按分类筛选表（P0基础、P1行情、P2财务等）

**整体概览页面：**
- 数据库统计信息
- 总表数、总记录数
- 大表记录数排行

**图表分析页面：**
- 数据分布可视化
- 按日期、股票代码分组统计

---

## 方法5：导出数据到PostgreSQL（如需pgAdmin）

### 场景
如果需要使用pgAdmin等专业数据库管理工具，可导出数据到PostgreSQL。

### 导出步骤

**Step 1：导出DuckDB数据到CSV**

```bash
python3 scripts/view_duckdb_data.py --table stock_daily \
  --export tmp/stock_daily_export.csv
```

**Step 2：导入PostgreSQL**

```bash
# 安装PostgreSQL（如未安装）
sudo apt install postgresql postgresql-contrib

# 创建数据库
sudo -u postgres psql
CREATE DATABASE adata;

# 导入数据
psql -U postgres -d adata -c "\copy stock_daily FROM 'tmp/stock_daily_export.csv' CSV HEADER"
```

**Step 3：使用pgAdmin查看**

```bash
# 安装pgAdmin
sudo apt install pgadmin4

# 启动pgAdmin
pgadmin4
```

访问：http://localhost:5050

配置连接：
- **主机：** localhost
- **端口：** 5432
- **数据库：** adata
- **用户：** postgres

---

## 方法6：VS Code插件（推荐开发调试）

### 安装VS Code DuckDB插件

1. 打开VS Code
2. 安装插件：**DuckDB SQL Runner**（或搜索"duckdb"）
3. 配置数据库路径：`/home/my/claude-project/AData/database/adata.db`

### VS Code查看数据

- ✅ 在VS Code中直接执行SQL查询
- ✅ 查看查询结果（表格显示）
- ✅ 语法高亮、自动补全

---

## 数据查看对比

| 方法 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| Python脚本 | 轻量、灵活、可定制 | 无GUI、需命令行 | 快速查询、数据分析 |
| DuckDB CLI | 官方工具、功能完整 | 命令行交互、无GUI | 命令行用户、批量导出 |
| DBeaver | 可视化GUI、功能强大 | 需安装、较重 | 长期查看、数据管理 |
| Dashboard | 已集成、可视化 | 查询功能有限 | 快速查看表概览 |
| PostgreSQL导出 | pgAdmin专业工具 | 需安装PG、导出耗时 | 生产环境、企业级管理 |
| VS Code插件 | 开发集成、便捷 | 查询功能有限 | 开发调试 |

---

## 推荐方案

### 开发阶段（当前）

**推荐：Python脚本 + Dashboard**

理由：
- Python脚本灵活快速，适合数据分析
- Dashboard已集成，适合快速查看概览
- 无需安装额外工具

```bash
# 快速查看数据（推荐）
python3 scripts/view_duckdb_data.py --table stock_daily --limit 50

# 可视化查看（推荐）
python3 -m streamlit run dashboard/app.py
```

---

### 长期使用（推荐可视化）

**推荐：DBeaver**

理由：
- 免费开源，功能强大
- 支持DuckDB直接连接
- 可视化GUI，类似pgAdmin体验
- 支持数据导出、ER图、SQL编辑器

```bash
# 安装DBeaver
sudo snap install dbeaver-ce

# 配置连接DuckDB
数据库路径: /home/my/claude-project/AData/database/adata.db
```

---

## 常见查询示例

### 1. 查看股票日线数据

```bash
# 查看平安银行最近20天
python3 scripts/view_duckdb_data.py --table stock_daily \
  --where "ts_code='000001.SZ'" \
  --order-by "trade_date DESC" \
  --limit 20

# 查看最新一天所有股票
python3 scripts/view_duckdb_data.py --table stock_daily \
  --where "trade_date='2026-04-09'" \
  --limit 100
```

### 2. 查看财务数据

```bash
# 查看利润表最新公告
python3 scripts/view_duckdb_data.py --table income \
  --order-by "ann_date DESC" \
  --limit 20

# 查看特定股票财务数据
python3 scripts/view_duckdb_data.py --table income \
  --where "ts_code='000001.SZ'" \
  --limit 10
```

### 3. 统计分析

```bash
# 市场涨跌统计
python3 scripts/view_duckdb_data.py --sql \
  "SELECT trade_date, COUNT(*) as stock_count,
          AVG(pct_chg) as avg_change,
          COUNT(CASE WHEN pct_chg > 0 THEN 1 END) as up_count,
          COUNT(CASE WHEN pct_chg < 0 THEN 1 END) as down_count
   FROM stock_daily
   WHERE trade_date >= '2026-04-01'
   GROUP BY trade_date
   ORDER BY trade_date DESC
   LIMIT 10"

# 行业分布
python3 scripts/view_duckdb_data.py --sql \
  "SELECT industry, COUNT(*) as stock_count
   FROM stock_basic
   GROUP BY industry
   ORDER BY stock_count DESC
   LIMIT 20"
```

---

## 数据导出常用场景

### 导出单个表

```bash
python3 scripts/view_duckdb_data.py --table stock_daily \
  --export tmp/stock_daily_202604.csv \
  --where "trade_date >= '2026-04-01'"
```

### 导出多个表（批量）

```bash
# 创建批量导出脚本
for table in stock_daily stock_daily_basic income fina_indicator; do
  python3 scripts/view_duckdb_data.py --table $table \
    --export tmp/${table}_export.csv
done
```

---

## 总结

**DuckDB数据查看痛点解决：**

✅ **Python脚本：** `scripts/view_duckdb_data.py`（灵活快速）
✅ **DuckDB CLI：** 官方命令行工具（功能完整）
✅ **DBeaver：** 可视化GUI工具（推荐长期使用）
✅ **Dashboard：** 已集成可视化（快速概览）
✅ **PostgreSQL导出：** pgAdmin专业管理（企业级）
✅ **VS Code插件：** 开发集成查看（便捷调试）

**推荐当前使用：** Python脚本 + Dashboard（无需额外安装）

**推荐长期使用：** DBeaver（免费强大，类似pgAdmin体验）

---

**数据查看工具创建：** Claude Code Agent
**创建时间：** 2026-04-14
**工具位置：** scripts/view_duckdb_data.py