# 更新日志

## [2.2.0] - 2025-10-26

### ✨ 新增

#### 脚本工具集

**1. validate-slides.sh - 幻灯片验证工具**
- 7大类验证检查 (14个检查点)
- 文件信息统计 (大小、行数)
- 详细模式 (`--verbose`) 显示错误行号
- JSON 输出模式 (计划中)
- 彩色输出增强可读性

**2. auto-fix-slides.sh - 自动修复工具**
- 自动修复代码块语言标识
- 自动添加分隔符空行
- 自动添加 Mermaid scale 参数
- 自动备份原文件 (`.bak`)
- 预演模式 (`--dry-run`)

**3. preview-slides.sh - 一键预览工具**
- 集成验证→修复→预览流程
- 自动修复失败项
- 智能启动 Slidev
- 强制预览模式 (`--force`)

**4. 规划和文档**
- `scripts/SCRIPTS_PLAN.md` - 未来脚本规划
- `scripts/README.md` - 脚本使用文档

#### 文档增强

**规范文档**
- `validation-workflow.md` - 验证工作流程详解
- 常见问题修复方法
- Agent 集成指南

**规则文档**
- `slidev-core-rules.md` - 增加内容溢出防止规则
- 三层解决方案: 拆分 > 滚动 > 缩放
- 详细的缩放建议表格

**配置文档**
- `slidev-config.md` - 字体和样式配置指南 (441行)
- `slidev-themes.md` - 主题选择指南
- 默认配置优化 (theme: seriph, 中文字体)

### 🔧 改进

**SKILL.md**
- 添加步骤 6: 规范验证
- 更新步骤编号
- 更新 description 包含验证

**README.md**
- 添加"验证和修复工具"章节
- 3个脚本的快速使用指南
- 更新"添加新模板"流程

**references/README.md**
- 添加 `validation-workflow.md` 引用

### 🐛 修复

**validate-slides.sh**
- 移除 `set -e` 避免意外退出
- 修复代码块计数逻辑
- 改进换行符检查
- 增强错误输出

### 📊 测试结果

测试文件: `morphllm-mcp-teaching-20251026.md` (140+ 页幻灯片)

**validate-slides.sh**:
- ✅ 成功识别 6 个代码块问题
- ✅ 详细模式正确显示行号
- ✅ 验证耗时 < 2秒

**auto-fix-slides.sh**:
- ✅ 成功修复 12 处问题
- ✅ 预演模式正常工作
- ✅ 自动备份功能正常

**preview-slides.sh**:
- ✅ 流程集成正常
- ✅ 自动修复触发正确

---

## [2.1.0] - 2025-10-26

### ✨ 新增

- 按需加载架构设计
- `references/` 目录结构
- 完整的 Slidev 官方文档 (81个)
- 文档分类索引

### 🔧 改进

- Token 消耗降低 50-70%
- SKILL.md 结构优化
- README.md 完全重写

---

## [2.0.0] - 2025-10-26

### ✨ 新增

- 四大场景模板
  - 教学 (teaching.md)
  - 调研 (research.md)
  - 算法 (algorithm.md)
  - 项目解析 (project-analysis.md)

- 核心工作流
  - 素材获取
  - 场景识别
  - 内容生成
  - 自动预览

### 🔧 改进

- 统一输出目录: `~/note-vsc/slides/`
- 标准命名格式: `主题-场景-日期.md`
- 自动 Slidev 预览

---

## [1.0.0] - 2025-10-25

### ✨ 初始版本

- 基础幻灯片生成功能
- md2ppt 集成
- 简单模板系统
