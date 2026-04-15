# Frontend - A股数据库监控面板

基于Streamlit构建的A股数据库监控和可视化系统。

## 项目结构

```
frontend/
├── run_dashboard.py          # Dashboard启动脚本（使用配置文件）
├── config/                   # 配置目录
│   └── config.yaml          # 前端配置文件（可选）
└── dashboard/               # Dashboard应用目录
    ├── app.py              # 主应用文件
    ├── config/             # Dashboard独立配置目录
    │   ├── dashboard_config.yaml      # Dashboard专用配置文件
    │   ├── dashboard_config_manager.py # 配置管理器
    │   └── __init__.py
    ├── components/         # 组件目录
    │   ├── overview.py
    │   ├── table_list.py
    │   ├── table_detail.py
    │   ├── charts.py
    │   ├── fetch_control.py
    │   └── settings.py
    ├── utils/             # 工具目录
    ├── database/          # 数据库模块
    ├── metadata.py        # 元数据查询
    ├── config_manager.py  # 旧的配置管理器（兼容用）
    └── requirements.txt   # Dashboard依赖
```

## 快速启动

### 使用run_dashboard.py启动（推荐）

```bash
cd /home/my/claude-project/AData/code/frontend
python3 run_dashboard.py
```

或使用绝对路径：

```bash
python3 /home/my/claude-project/AData/code/frontend/run_dashboard.py
```

### 直接使用streamlit启动

```bash
cd /home/my/claude-project/AData/code/frontend/dashboard
streamlit run app.py
```

## 配置说明

Dashboard使用独立的配置文件 `dashboard/config/dashboard_config.yaml`，不依赖后端数据拉取服务的配置。

### 主要配置项

#### 数据库配置
```yaml
database:
  path: database/adata_snapshot.db  # 快照数据库路径（只读）
  type: duckdb                      # 数据库类型
```

**重要**：Dashboard只使用快照数据库（`adata_snapshot.db`），避免多个项目间的数据冲突。

#### 服务器配置
```yaml
server:
  host: localhost    # 监听地址（run_dashboard.py中可以覆盖）
  port: 8501       # 监听端口（run_dashboard.py中可以覆盖）
  debug: false     # 是否开启调试模式
```

#### 日志配置
```yaml
logging:
  level: INFO               # 日志级别
  file: logs/dashboard.log  # 日志文件路径
  max_size: 10MB           # 单个日志文件最大大小
  backup_count: 5          # 保留的日志文件备份数量
```

## 访问地址

启动后，可以通过以下地址访问：

- **本地访问**: http://localhost:8501
- **局域网访问**: 如需从其他设备访问，修改配置文件中的host为`0.0.0.0`

## 功能特性

- 📊 **整体概览**：查看数据库整体状态和统计信息
- 📋 **数据表列表**：浏览所有数据表，查看表详情和数据
- 📈 **图表分析**：数据可视化和趋势分析
- ⚙️ **数据拉取控制**：控制后端数据拉取服务（需要权限）
- 🔧 **系统配置**：查看和修改系统配置

## 依赖安装

```bash
cd /home/my/claude-project/AData/code/frontend/dashboard
pip install -r requirements.txt
```

## run_dashboard.py vs 其他启动方式的区别

### run_dashboard.py（推荐）

1. **读取配置文件**：从`dashboard/config/dashboard_config.yaml`读取配置
2. **灵活启动**：可以覆盖配置文件中的host和port
3. **统一入口**：作为frontend目录的标准启动方式
4. **环境变量设置**：自动设置Streamlit环境变量

### 直接使用streamlit run app.py

1. **不读取配置**：使用Streamlit默认配置或命令行参数
2. **完全手动**：需要手动指定所有参数
3. **适合开发**：快速测试时使用

## 故障排查

### 问题：数据库文件不存在

**症状**：Dashboard启动时提示数据库文件不存在

**解决**：
- 检查后端服务是否正在运行
- 检查快照数据库文件是否存在：`/home/my/claude-project/AData/database/adata_snapshot.db`
- 等待后端服务生成快照文件

### 问题：端口被占用

**症状**：启动失败，提示端口被占用

**解决**：
- 修改配置文件 `dashboard/config/dashboard_config.yaml` 中的 `server.port`
- 或者停止占用该端口的进程

### 问题：配置文件加载失败

**症状**：启动时提示无法加载配置文件，使用默认配置

**解决**：
- 检查配置文件是否存在：`dashboard/config/dashboard_config.yaml`
- 检查配置文件格式是否正确（YAML格式）

## 配置管理器使用示例

```python
from dashboard.config import get_dashboard_config_manager

# 获取配置实例
config = get_dashboard_config_manager()

# 使用配置
db_path = config.get_database_path()     # 数据库路径
log_level = config.get_log_level()        # 日志级别
port = config.get_server_port()           # 服务器端口
theme = config.get_theme()                # UI主题
```

## 注意事项

1. **数据库文件**：Dashboard依赖快照数据库文件（`adata_snapshot.db`），请确保后端服务已运行并生成快照。

2. **只读模式**：Dashboard使用只读模式访问数据库，不会修改数据库内容。

3. **端口配置**：默认端口8501，如需修改可以在配置文件中更改。

4. **防火墙**：如果需要从其他设备访问，请确保服务器防火墙允许对应端口的访问。

## 版本历史

- **v1.1.0** (2026-04-15)
  - 使用独立的配置管理系统
  - 只使用快照数据库（避免多项目冲突）
  - 更新run_dashboard.py支持配置文件
  - 移除重复的启动脚本

- **v1.0.0** (2026-04-11)
  - 初始版本
  - 基本的Dashboard功能
