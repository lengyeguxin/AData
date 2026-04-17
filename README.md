# AData - A股数据库系统

完整的A股数据采集、存储和可视化系统，基于DuckDB和Streamlit构建。

## 项目简介

AData是一个专门为A股市场设计的数据管理系统，提供：

- 📊 **数据采集**：通过Tushare API自动采集A股历史数据、财务数据、指数数据等
- 🗄️ **高效存储**：基于DuckDB的高性能列式数据库
- 📈 **实时监控**：Streamlit Dashboard可视化监控界面
- 🔄 **定时更新**：支持每日/每周/每月自动更新数据
- 💾 **双快照架构**：快照同时备份到多个位置，支持多Dashboard实例
- ⏸️ **断点续传**：支持从中断处继续数据导入

## 项目结构

```
AData/
├── code/
│   ├── backend/                 # 后端服务
│   │   ├── main.py             # 主启动入口
│   │   ├── init_db.py          # 数据库初始化脚本
│   │   ├── config/             # 配置文件
│   │   │   ├── config.yaml     # 主配置文件（需配置token）
│   │   │   ├── config.yaml.example  # 配置文件示例
│   │   │   └── table_config.yaml  # 数据表配置
│   │   ├── scripts/            # 工具脚本
│   │   │   ├── setup_database.py      # 数据库设置
│   │   │   ├── verify_schema.py       # Schema验证
│   │   │   └── generate_phase2_summary.py  # 摘要生成
│   │   └── src/                # 源代码
│   │       ├── core/           # 核心模块
│   │       │   ├── database.py         # 数据库封装
│   │       │   ├── tushare_api.py      # API接口
│   │       │   ├── data_fetcher.py     # 数据拉取
│   │       │   └── global_cursor_manager.py  # 游标管理
│   │       ├── collectors/     # 数据采集器
│   │       └── scheduler/      # 任务调度器
│   │
│   └── frontend/                # 前端Dashboard
│       ├── run_dashboard.py    # Dashboard启动脚本
│       └── dashboard/           # Dashboard应用
│           ├── app.py          # 主应用
│           ├── config/         # Dashboard配置
│           ├── components/     # UI组件
│           └── metadata.py     # 元数据查询
│
├── database/                    # 数据库文件目录
│   ├── adata.db                # 主数据库
│   └── schemas/                # 数据库Schema文件
│
├── docs/                        # 项目文档
│   ├── README.md                # 文档索引
│   ├── ARCHITECTURE.md          # 架构设计文档
│   └── DEPLOYMENT.md            # 部署运维文档
├── design-doc/                  # 设计文档
│   └── 数据表信息汇总.csv       # 数据表汇总
│
├── logs/                        # 日志目录
├── .claude/                     # Claude记忆系统
├── CLAUDE.md                    # 项目配置
└── README.md                    # 本文件
```

## 快速开始

### 1. 环境准备

确保已安装Python 3.8+：

```bash
python3 --version
```

### 2. 配置Tushare Token

复制配置文件并填入您的Tushare Token：

```bash
cd /home/my/claude-project/AData
cp code/backend/config/config.yaml.example code/backend/config/config.yaml
```

编辑 `code/backend/config/config.yaml`，将 `YOUR_TUSHARE_TOKEN_HERE` 替换为您的实际token：

```yaml
tushare:
  token: 您的实际token  # 在这里替换
```

> 💡 获取Tushare Token：访问 https://tushare.pro 注册账号

### 3. 初始化数据库

首次部署需要初始化数据库（仅执行一次）：

```bash
python3 code/backend/init_db.py
```

此操作会创建27张数据表和游标表。

### 4. 启动后端服务

启动数据采集和定时任务：

```bash
python3 code/backend/main.py
```

后端会自动：
- 拉取最新数据
- 启动定时任务（每日18点更新日数据）
- 定期创建快照（每30分钟）

### 5. 启动前端Dashboard

在另一个终端启动Dashboard：

```bash
python3 code/frontend/run_dashboard.py
```

访问 http://localhost:8501 查看数据监控界面。

## 核心功能

### 数据采集

系统支持采集以下类型的数据：

- **基础数据**：股票基本信息、指数基本信息、交易日历
- **行情数据**：日行情、分钟行情、指数行情
- **财务数据**：资产负债表、利润表、现金流量表、财务指标
- **市场数据**：资金流向、龙虎榜、概念板块
- **ETF数据**：ETF基本信息、行情、复权因子

### 定时任务

- **日数据更新**：每日18:00自动更新日行情、日线数据
- **周数据更新**：每周五19:00更新周线数据
- **月数据更新**：每月20:00更新月线数据
- **快照创建**：每30分钟自动创建快照备份

### 双快照架构

快照同时备份到两个位置，支持：
- 主快照：`database/adata_snapshot.db`（AData项目）
- 副快照：`/path/to/AIStock/database/adata_snapshot.db`（AIStock项目）

Dashboard使用快照数据库（只读），不影响主数据库的写入操作。

## 运行模式

### 后端运行模式

```bash
# 完整启动（数据拉取+定时任务）
python3 code/backend/main.py

# 仅拉取数据（一次性）
python3 code/backend/main.py --fetch

# 仅启动定时任务
python3 code/backend/main.py --scheduler

# 跳过初始拉取
python3 code/backend/main.py --no-fetch

# 立即创建快照
python3 code/backend/main.py --snapshot
```

### 前端运行模式

```bash
# 使用启动脚本（推荐）
python3 code/frontend/run_dashboard.py

# 直接使用streamlit
cd code/frontend/dashboard
streamlit run app.py
```

## 配置说明

### 主配置文件 (config.yaml)

#### 数据库配置
```yaml
database:
  path: database/adata.db    # 主数据库路径
  type: duckdb                # 数据库类型
```

#### Tushare API配置
```yaml
tushare:
  token: YOUR_TOKEN           # API Token
  api_url: http://8.136.22.187:8010/  # API地址
  rate_limit: 500            # 每分钟请求限制
  timeout: 60                # 超时时间（秒）
```

#### 数据拉取配置
```yaml
fetch:
  enabled: true              # 是否启用数据拉取
  start_date: "20210101"     # 最早数据时间
  check_interval: 60         # 检测间隔（分钟）
  max_retries: 2             # 失败重试次数
```

#### 快照配置
```yaml
snapshot:
  enabled: true              # 是否启用快照
  interval: 30               # 快照间隔（分钟）
  locations:                 # 快照位置（支持多个）
    - database/adata_snapshot.db
    - /path/to/other/location/snapshot.db
```

#### 调度器配置
```yaml
scheduler:
  daily_update_time: "18:00"  # 日数据更新时间
  weekly_update_time: "19:00" # 周数据更新时间
  monthly_update_time: "20:00" # 月数据更新时间
```

## 常见问题

### Q1: 首次启动报错"数据库文件不存在"

**解决**：先运行数据库初始化脚本

```bash
python3 code/backend/init_db.py
```

### Q2: API请求失败

**解决**：检查以下几点
1. 确认Tushare Token已正确配置
2. 检查网络连接和API地址是否可访问
3. 确认Tushare账户积分是否充足
4. 查看日志文件 `logs/adata.log` 了解详细错误

### Q3: Dashboard无法显示数据

**解决**：
1. 确认后端服务正在运行
2. 确认快照数据库文件存在：`database/adata_snapshot.db`
3. 等待后端服务生成快照（首次启动需要拉取数据）

### Q4: 端口被占用

**解决**：修改Dashboard配置文件中的端口号

```yaml
# code/frontend/dashboard/config/dashboard_config.yaml
server:
  port: 8502  # 改为其他端口
```

### Q5: 如何重新初始化数据库

**解决**：强制重新初始化

```bash
python3 code/backend/init_db.py --force
```

> ⚠️ 警告：此操作会删除现有数据库和所有数据，请谨慎操作

## 数据表结构

系统包含27张数据表，涵盖：

| 表名 | 说明 | 更新频率 |
|------|------|----------|
| stock_basic | 股票基本信息 | 每日 |
| trade_calendar | 交易日历 | 每日 |
| stock_daily_basic | 股票日行情（基本） | 每日 |
| daily | 股票日行情 | 每日 |
| weekly | 股票周行情 | 每周 |
| monthly | 股票月行情 | 每月 |
| income | 利润表 | 每季度 |
| balancesheet | 资产负债表 | 每季度 |
| cashflow | 现金流量表 | 每季度 |
| fina_indicator | 财务指标 | 每季度 |
| dividend | 分红数据 | 每日 |
| index_basic | 指数基本信息 | 每日 |
| index_daily | 指数日行情 | 每日 |
| ths_concept_member | 同花顺概念股成分 | 每日 |
| hots_user | 龙虎榜用户 | 每日 |
| ... | ... | ... |

完整数据表信息参见：[design-doc/数据表信息汇总.csv](design-doc/数据表信息汇总.csv)

## 技术架构

### 后端技术栈
- **Python 3.8+**：主要开发语言
- **DuckDB**：高性能列式数据库
- **Tushare API**：A股数据源
- **APScheduler**：定时任务调度
- **PyYAML**：配置文件解析
- **structlog**：结构化日志

### 前端技术栈
- **Streamlit**：数据可视化框架
- **Plotly**：交互式图表

### 设计特点

1. **线程安全**：写操作加锁，保证DuckDB单写模型
2. **并发读取**：读操作无锁，支持多线程并发
3. **断点续传**：基于游标的增量采集，支持中断恢复
4. **双快照**：快照同时更新多个位置，支持高可用
5. **配置驱动**：所有行为通过配置文件控制

## 开发指南

### 添加新的数据采集器

1. 在 `code/backend/src/collectors/` 创建新的采集器文件
2. 继承 `BaseCollector` 类
3. 实现 `fetch` 和 `save` 方法
4. 在 `table_config.yaml` 中注册表配置

### 自定义调度任务

修改 `code/backend/config/config.yaml` 中的调度器配置：

```yaml
scheduler:
  custom_update_time: "21:00"  # 自定义更新时间
```

### 扩展Dashboard功能

在 `code/frontend/dashboard/components/` 添加新的组件文件，然后在 `app.py` 中引用。

## 监控和维护

### 查看日志

```bash
# 后端日志
tail -f logs/adata.log

# Dashboard日志
tail -f logs/dashboard.log
```

### 检查数据完整性

```bash
# 验证数据库Schema
python3 code/backend/scripts/verify_schema.py
```

### 生成数据摘要

```bash
# 生成数据表摘要
python3 code/backend/scripts/generate_phase2_summary.py
```

## 性能优化

### 数据库优化
- 使用DuckDB的列式存储，适合分析查询
- 支持并行查询，提高大数据量查询性能
- 自动索引优化，加速查询

### API调用优化
- 内置限流控制，避免超出Tush API限制
- 智能重试机制，处理网络抖动
- 批量请求优化，减少API调用次数

## 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

本项目仅供学习交流使用。数据来源于Tushare，请遵守Tushare的使用协议。

## 联系方式

- 问题反馈：提交Issue
- 技术讨论：欢迎交流

## 项目文档

完整的技术文档请查看 [docs/](docs/) 目录：

- 📖 [docs/README.md](docs/README.md) - 文档索引和快速导航
- 🏗️ [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - 架构设计文档
- 🚀 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - 部署运维文档

### 文档包含内容

**架构设计文档**：
- 系统架构和模块设计
- 核心组件详解
- 数据流和存储设计
- 性能优化和安全设计

**部署运维文档**：
- 多种部署方式（本地/Docker/云服务器）
- 配置说明和监控指南
- 备份恢复和故障排查
- 性能优化和安全加固

## 更新日志

### v2.0.0 (2026-04-17)
- 重新组织项目文档
- 完善README说明
- 添加运行模式说明
- 补充常见问题解答

### v1.1.0 (2026-04-15)
- 实现双快照架构
- Dashboard独立配置系统
- 快照更新间隔调整为30分钟
- 支持多Dashboard实例

### v1.0.0 (2026-04-11)
- 初始版本发布
- 基础数据采集功能
- Streamlit Dashboard
- 定时任务调度
