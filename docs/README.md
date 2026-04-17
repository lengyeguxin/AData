# AData 项目文档

欢迎使用AData项目文档！本目录包含AData项目的完整技术文档。

## 📚 文档列表

### [架构设计文档](./ARCHITECTURE.md)

**适合读者**：架构师、技术负责人、高级开发者

**内容概要**：
- 项目概述和设计目标
- 系统架构和模块划分
- 核心组件设计详解
- 数据流和存储设计
- 配置管理和错误处理
- 性能优化和安全设计
- 扩展性和监控设计

**推荐阅读场景**：
- 了解系统整体架构
- 设计新功能或重构现有功能
- 代码审查和技术评审
- 排查系统级问题

---

### [部署运维文档](./DEPLOYMENT.md)

**适合读者**：运维工程师、DevOps工程师、开发者

**内容概要**：
- 环境要求和软件依赖
- 多种部署方式（本地/Docker/云服务器）
- 配置文件详解
- 监控和维护指南
- 备份和恢复策略
- 故障排查手册
- 性能优化建议
- 安全加固方案
- 升级和迁移指南

**推荐阅读场景**：
- 首次部署AData系统
- 日常运维和维护
- 故障诊断和处理
- 性能调优和安全加固
- 系统升级和数据迁移

---

## 🚀 快速导航

### 我想...

- 🏠 **了解项目**
  - 阅读 [架构设计文档](./ARCHITECTURE.md) 的"项目概述"章节

- 🎯 **快速部署**
  - 阅读 [部署运维文档](./DEPLOYMENT.md) 的"环境要求"和"本地部署"章节

- 🐳 **使用Docker部署**
  - 阅读 [部署运维文档](./DEPLOYMENT.md) 的"Docker部署"章节

- ☁️ **部署到云服务器**
  - 阅读 [部署运维文档](./DEPLOYMENT.md) 的"云服务器部署"章节

- 🔧 **配置系统**
  - 阅读 [部署运维文档](./DEPLOYMENT.md) 的"配置说明"章节

- 📊 **监控系统**
  - 阅读 [部署运维文档](./DEPLOYMENT.md) 的"监控和维护"章节

- 🛡️ **加固安全**
  - 阅读 [部署运维文档](./DEPLOYMENT.md) 的"安全加固"章节

- 🐛 **解决问题**
  - 阅读 [部署运维文档](./DEPLOYMENT.md) 的"故障排查"章节

- ⚡ **优化性能**
  - 阅读 [部署运维文档](./DEPLOYMENT.md) 的"性能优化"章节

- 💾 **备份数据**
  - 阅读 [部署运维文档](./DEPLOYMENT.md) 的"备份和恢复"章节

- 🔨 **开发新功能**
  - 阅读 [架构设计文档](./ARCHITECTURE.md) 的"扩展设计"章节

- 📈 **理解数据流**
  - 阅读 [架构设计文档](./ARCHITECTURE.md) 的"数据流设计"章节

---

## 📋 文档结构

```
docs/
├── README.md           # 本文件 - 文档索引
├── ARCHITECTURE.md    # 架构设计文档
└── DEPLOYMENT.md      # 部署运维文档
```

---

## 🎓 学习路径

### 新手入门路径

1. **第一步**：了解项目
   - [架构设计文档](./ARCHITECTURE.md) - 项目概述

2. **第二步**：准备环境
   - [部署运维文档](./DEPLOYMENT.md) - 环境要求

3. **第三步**：本地部署
   - [部署运维文档](./DEPLOYMENT.md) - 本地部署

4. **第四步**：配置和启动
   - [部署运维文档](./DEPLOYMENT.md) - 配置说明

5. **第五步**：监控和维护
   - [部署运维文档](./DEPLOYMENT.md) - 监控和维护

### 进阶开发路径

1. **第一步**：深入理解架构
   - [架构设计文档](./ARCHITECTURE.md) - 系统架构
   - [架构设计文档](./ARCHITECTURE.md) - 核心组件设计

2. **第二步**：生产部署
   - [部署运维文档](./DEPLOYMENT.md) - Docker部署
   - [部署运维文档](./DEPLOYMENT.md) - 云服务器部署

3. **第三步**：系统优化
   - [架构设计文档](./ARCHITECTURE.md) - 性能优化
   - [部署运维文档](./DEPLOYMENT.md) - 性能优化

4. **第四步**：功能扩展
   - [架构设计文档](./ARCHITECTURE.md) - 扩展设计

5. **第五步**：生产运维
   - [部署运维文档](./DEPLOYMENT.md) - 安全加固
   - [部署运维文档](./DEPLOYMENT.md) - 升级和迁移

---

## 🔍 关键概念速查

### 核心组件

| 组件 | 说明 | 文档位置 |
|------|------|----------|
| Database | 数据库封装 | [ARCHITECTURE.md#3.1](./ARCHITECTURE.md#31-数据库封装-database) |
| TushareAPI | API接口封装 | [ARCHITECTURE.md#3.2](./ARCHITECTURE.md#32-api接口封装-tushareapi) |
| DataFetcher | 数据拉取控制器 | [ARCHITECTURE.md#3.3](./ARCHITECTURE.md#33-数据拉取控制器-datafetcher) |
| GlobalCursorManager | 游标管理器 | [ARCHITECTURE.md#3.4](./ARCHITECTURE.md#34-游标管理器-globalcursormanager) |
| BaseCollector | 采集器基类 | [ARCHITECTURE.md#3.5](./ARCHITECTURE.md#35-采集器基类-basecollector) |
| DataScheduler | 定时任务调度器 | [ARCHITECTURE.md#3.6](./ARCHITECTURE.md#36-定时任务调度器-datascheduler) |

### 关键特性

| 特性 | 说明 | 文档位置 |
|------|------|----------|
| 断点续传 | 基于游标的增量采集 | [ARCHITECTURE.md#4.2](./ARCHITECTURE.md#42-断点续传机制) |
| 双快照架构 | 支持高可用和多实例 | [ARCHITECTURE.md#4.3](./ARCHITECTURE.md#43-双快照架构) |
| 优先级管理 | 五级优先级数据拉取 | [ARCHITECTURE.md#3.3](./ARCHITECTURE.md#33-数据拉取控制器-datafetcher) |
| 依赖检查 | 确保前置表已拉取 | [ARCHITECTURE.md#3.3](./ARCHITECTURE.md#33-数据拉取控制器-datafetcher) |

---

## 📞 获取帮助

### 常见问题

- [部署运维文档 - 常见问题](./DEPLOYMENT.md#10-常见问题)

### 故障排查

- [部署运维文档 - 故障排查](./DEPLOYMENT.md#6-故障排查)

### 日志分析

- [部署运维文档 - 日志监控](./DEPLOYMENT.md#4.1-日志监控)

---

## 🤝 贡献指南

欢迎贡献文档！

1. 保持文档的准确性和时效性
2. 使用清晰的标题和结构
3. 提供具体的示例和命令
4. 包含适当的注意事项和警告
5. 保持文档风格的统一性

---

## 📝 文档更新日志

### v1.0.0 (2026-04-17)

- ✅ 初始版本
- ✅ 创建架构设计文档 (ARCHITECTURE.md)
- ✅ 创建部署运维文档 (DEPLOYMENT.md)
- ✅ 创建文档索引 (README.md)

---

## 🔗 相关资源

### 项目文档

- [项目根目录 README](../README.md)
- [CLAUDE.md](../CLAUDE.md)

### 外部资源

- [DuckDB官方文档](https://duckdb.org/docs/)
- [Streamlit官方文档](https://docs.streamlit.io/)
- [Tushare API文档](https://tushare.pro/document/)

---

## 💡 文档使用技巧

### 搜索技巧

- 使用浏览器或编辑器的搜索功能（Ctrl+F / Cmd+F）
- 搜索关键词：组件名、配置项、错误信息等

### 跨文档导航

- 文档间的章节链接使用相对路径
- 点击链接可以快速跳转到相关章节

### 本地阅读

推荐使用Markdown阅读器或IDE查看文档：
- VSCode + Markdown Preview Enhanced
- Typora
- Markdown编辑器

---

如有任何问题或建议，欢迎反馈！
