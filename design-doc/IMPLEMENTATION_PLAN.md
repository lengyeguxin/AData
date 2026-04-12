# AData项目实施计划

## 当前状态（2026-04-11）

**已完成：**
- ✅ Phase 5 Dashboard移植改造（已完成所有修改）
  - 移除settings.py的end_date字段
  - 新增快照配置（snapshot interval配置）
  - 创建fetch_control.py页面
  - 集成到app.py导航

**部分完成：**
- ⚠️ Phase 1 项目结构重组（部分完成）
  - ✅ 创建code/frontend/dashboard/目录
  - ✅ 创建database/schemas/目录
  - ✅ 创建global_cursor_schema.sql
  - ✅ 创建p0_schema.sql、p1_schema.sql、p2_schema.sql
  - ⏳ 待完成：创建config/目录、创建scripts/目录、创建tests/目录

**未开始：**
- ⏳ Phase 2 核心类开发（关键路径）
- ⏳ Phase 3 配置系统增强
- ⏳ Phase 4 后端启动流程
- ⏳ Phase 6 数据迁移（暂缓）
- ⏳ Phase 7 测试验证

---

## 推荐实施顺序（基于依赖关系）

### 🔴 最高优先级：核心基础（必须先完成）

#### Phase 2: 核心类开发（关键路径）
**工期：** 2-3周
**重要性：** 所有后续功能的基础

**核心类列表：**
1. **GlobalCursorManager** (`code/backend/src/core/global_cursor_manager.py`)
   - 游标管理核心类
   - 统一游标策略（5种游标类型）
   - 游标判断逻辑（should_fetch、get_next_fetch_date）
   - 18点时间判断
   - 游标更新时机判断（财务表允许无数据更新）

2. **DataFetcher** (`code/backend/src/core/data_fetcher.py`)
   - 统一数据拉取控制器
   - 启动流程：判断进度、断点续传
   - 数据存在性检查（避免重复爬取）
   - 前置表依赖检查
   - 按日期遍历拉取

3. **BaseCollector** (`code/backend/src/collectors/base_collector.py`)
   - Collector基类（消除代码冗余）
   - 通用collect、transform、save方法
   - 数据存在性检查

**依赖：**
- 需要先创建config/config.yaml（基础配置）
- 需要先初始化数据库（执行SQL schema）

---

### 🟠 第二优先级：项目基础设施

#### Phase 1: 项目结构重组（剩余工作）
**工期：** 1周
**重要性：** 为核心类提供运行环境

**待完成任务：**
1. 创建config/目录
   - config.yaml（主配置）
   - table_config.yaml（表配置）

2. 创建scripts/目录
   - setup_database.py（初始化数据库）
   - verify_schema.py（验证表结构）

3. 初始化数据库
   - 执行SQL schema创建27张表
   - 创建global_cursor表并初始化游标记录

4. 创建tests/目录
   - test_cursor_manager.py
   - test_fetcher.py
   - test_collectors.py

**依赖：**
- 无依赖，可立即执行

---

### 🟡 第三优先级：配置系统

#### Phase 3: 配置系统增强
**工期：** 1周
**重要性：** 配置化控制所有参数

**任务：**
1. 创建table_config.yaml
   - 27张表的详细配置
   - 游标策略、依赖关系、API参数

2. 增强config.yaml
   - fetch.enabled（数据拉取开关）
   - snapshot.interval（快照间隔）
   - scheduler配置

3. 增强ConfigManager
   - 支持游标管理
   - 支持fetch.enabled开关

**依赖：**
- 依赖Phase 1（config目录创建）
- 依赖Phase 2（GlobalCursorManager需要读取配置）

---

### 🟢 第四优先级：后端集成

#### Phase 4: 后端启动流程
**工期：** 1周
**重要性：** 整合所有组件

**任务：**
1. 创建main.py
   - 启动入口
   - 初始化数据库
   - 启动DataFetcher（默认开启）
   - 启动Scheduler

2. 创建SnapshotManager
   - 定时快照任务
   - 双位置快照

3. 创建Scheduler任务
   - 快照定时任务（每30分钟）
   - 数据拉取定时任务

**依赖：**
- 依赖Phase 1（数据库初始化）
- 依赖Phase 2（GlobalCursorManager、DataFetcher）
- 依赖Phase 3（配置文件）

---

### 🔵 第五优先级：测试验证

#### Phase 7: 测试验证
**工期：** 1周
**重要性：** 确保系统稳定运行

**测试内容：**
1. 游标系统测试
   - 游标初始化
   - 游标判断逻辑
   - 游标更新时机

2. 断点续传测试
   - 修改游标值
   - 重启后从游标+1开始拉取

3. 数据存在性检查测试
   - 手动导入一天数据
   - 重启后跳过该日期

4. Dashboard集成测试
   - fetch_control页面功能
   - 快照配置功能

**依赖：**
- 依赖Phase 2-4全部完成

---

### ⚪ ~~最后优先级：数据迁移~~

#### ~~Phase 6: 数据迁移~~（已移除）
**原因：** 用户明确要求不考虑数据迁移，重点在于开发和测试每个表的数据拉取、断点续传。

**替代方案：**
- 从空白数据库开始
- 测试每个表的数据拉取功能
- 验证断点续传机制
- 确保数据质量可控

---

## 实施路线图

```
Week 1: Phase 1（剩余工作） + Phase 2开始
  - 创建config/目录和配置文件
  - 初始化数据库（执行SQL schema）
  - 开始开发GlobalCursorManager

Week 2-3: Phase 2完成 + Phase 3开始
  - 完成GlobalCursorManager、DataFetcher、BaseCollector
  - 创建table_config.yaml
  - 增强ConfigManager

Week 4: Phase 3完成 + Phase 4开始
  - 完成配置系统
  - 创建main.py启动入口
  - 创建SnapshotManager

Week 5: Phase 4完成 + Phase 7开始
  - 完成后端集成
  - 开始测试验证（重点：每个表的数据拉取和断点续传）
  - **每次测试生成报告到/tmp下，并通知用户查看**

Week 6: Phase 7完成
  - 完成所有测试
  - 系统稳定运行
  - 数据质量验证通过
```

**重要：**
- ❌ Phase 6（数据迁移）已移除
- ✅ 重点在于开发和测试每个表的数据拉取功能
- ✅ 严格按照文档开发（特别是接口文档地址）
- ✅ 每次测试生成报告到/tmp，并通知用户查看

---

## 关键路径分析

**最短路径（必须顺序执行）：**

1. Phase 1（基础设施） → 1周
   - 创建config/目录
   - 初始化数据库
   - 创建scripts/目录

2. Phase 2（核心类） → 2-3周 ⭐ **关键路径**
   - GlobalCursorManager（1周）
   - DataFetcher（1周）
   - BaseCollector（0.5周）

3. Phase 4（后端集成） → 1周
   - main.py
   - SnapshotManager

4. Phase 7（测试验证） → 1周
   - 完整系统测试

**总工期：** 5-6周（不含Phase 6数据迁移）

**并行工作：**
- Phase 3（配置系统）可在Phase 2期间并行完成
- Phase 5（Dashboard）已提前完成

---

## 验收标准

### Phase 1验收
- ✅ database/adata.db数据库文件已创建
- ✅ 27张表结构已创建（通过verify_schema.py验证）
- ✅ global_cursor表已初始化（27条记录）
- ✅ config/config.yaml、config/table_config.yaml已创建

### Phase 2验收
- ✅ GlobalCursorManager类可正常判断游标
- ✅ DataFetcher可启动并判断拉取进度
- ✅ BaseCollector可拉取并保存数据
- ✅ 数据存在性检查正常工作（避免重复爬取）

### Phase 3验收
- ✅ table_config.yaml包含27张表的配置
- ✅ ConfigManager可读取所有配置
- ✅ fetch.enabled开关可通过Dashboard控制

### Phase 4验收
- ✅ main.py可正常启动
- ✅ DataFetcher默认开启拉取
- ✅ SnapshotManager每30分钟生成快照
- ✅ 快照在两个位置生成

### Phase 7验收
- ✅ 游标系统测试通过（断点续传）
- ✅ Dashboard集成测试通过（fetch_control页面）
- ✅ 系统稳定运行1周以上

---

## 立即可执行的任务（本周）

### 1. 创建config目录和配置文件
```bash
mkdir -p config
```

创建以下文件：
- config/config.yaml（主配置）
- config/table_config.yaml（表配置）

### 2. 初始化数据库
创建脚本：
- scripts/setup_database.py（执行SQL schema）

执行：
```bash
python scripts/setup_database.py
```

验证：
```bash
python scripts/verify_schema.py
```

### 3. 开始开发GlobalCursorManager
创建文件：
- code/backend/src/core/global_cursor_manager.py

---

## 总结

**推荐顺序：**
1. **Phase 1（剩余）** → 创建基础设施（本周完成）
2. **Phase 2** → 核心类开发（2-3周，关键路径） ⭐
3. **Phase 3** → 配置系统（1周，可并行）
4. **Phase 4** → 后端集成（1周）
5. **Phase 7** → 测试验证（1周）
6. **Phase 6** → 数据迁移（暂缓）

**总工期：** 5-6周（不含Phase 6）

**关键成功因素：**
- GlobalCursorManager类质量（决定整个系统稳定性）
- 数据存在性检查逻辑（避免重复爬取）
- 游标更新时机判断（财务表允许无数据更新）

**风险：**
- 游标策略复杂度（5种策略需仔细处理）
- 前置表依赖顺序（必须按固定顺序拉取）
- 18点时间判断（需确保Tushare数据已更新）

---

**文档版本：** 1.0
**最后更新：** 2026-04-11
**作者：** Claude Code Assistant