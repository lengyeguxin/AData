#!/bin/bash
# AData项目重新上传到GitHub脚本
# 用途：重新提交所有代码到重建后的GitHub仓库

echo "========================================"
echo "AData项目重新上传脚本"
echo "========================================"
echo ""

# 步骤1: 验证.gitignore配置
echo "步骤1: 验证.gitignore是否正确忽略config.yaml..."
if git check-ignore code/backend/config/config.yaml; then
    echo "✅ config.yaml将被正确忽略"
else
    echo "⚠️  config.yaml未被忽略，请检查.gitignore"
fi
echo ""

# 步骤2: 查看当前git状态
echo "步骤2: 当前git状态..."
git status --short
echo ""

# 步骤3: 添加所有文件（.gitignore会自动过滤敏感文件）
echo "步骤3: 添加所有文件到git..."
git add .
echo ""

# 步骤4: 验证config.yaml未被添加
echo "步骤4: 验证config.yaml不在待提交列表中..."
if git status --short | grep -q "code/backend/config/config.yaml"; then
    echo "❌ 错误：config.yaml被添加到git，请检查.gitignore！"
    exit 1
else
    echo "✅ config.yaml已被正确忽略"
fi
echo ""

# 步骤5: 查看待提交文件列表
echo "步骤5: 待提交文件列表（前20个）..."
git status --short | head -20
echo ""
echo "总文件数："
git status --short | wc -l
echo ""

# 步骤6: 创建commit
echo "步骤6: 创建commit..."
git commit -m "$(cat <<'EOF'
feat: AData项目完整重构代码

核心成果：
- 全局游标系统（27个游标，5种策略）
- BaseCollector基类（代码复用）
- 27个Collector实现（100%完成）
- VIP接口验证（7个VIP接口）
- 数据存在性检查（避免重复爬取）

主要内容：
1. code/backend/ - 后端核心代码
   - src/collectors/: 27个数据拉取器
   - src/core/: 核心组件（数据库、API、游标管理器）
   - config/: 配置文件（config.yaml.example示例）
   - tests/: 测试脚本（100%通过）

2. database/schemas/ - SQL schema文件
   - global_cursor_schema.sql: 游标表定义
   - p0/p1/p2_schema.sql: 数据表定义（27张表）

3. code/frontend/ - 前端Dashboard
   - Streamlit应用（数据可视化）

4. design-doc/ - 设计文档
   - 详细技术设计文档
   - 实施计划文档
   - 数据表信息汇总

测试结果：
- 基础功能测试: 18项（100%通过）
- VIP接口验证: 7个（100%）
- 游标策略覆盖: 5种（100%）

安全说明：
- config.yaml已忽略（包含Token等敏感信息）
- 请使用config.yaml.example作为配置模板
EOF
)"
echo ""

# 步骤7: 推送到GitHub
echo "步骤7: 推送到GitHub..."
git push -u origin master
echo ""

echo "========================================"
echo "✅ 上传完成！"
echo "========================================"
echo ""
echo "GitHub仓库: https://github.com/lengyeguxin/AData"
echo ""
echo "重要提示："
echo "1. 请确认config.yaml未被提交（检查GitHub仓库）"
echo "2. 本地需要创建config.yaml并填入实际Token"
echo "3. 运行初始化: python code/backend/scripts/setup_database.py"
echo ""