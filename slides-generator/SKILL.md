---
name: slides-generator
description: 通用幻灯片生成器 - 将任意输入(文件/URL/主题/文本)智能转换为 Slidev 幻灯片。自动识别需求类型,选择最佳处理模式,规范化输出后统一使用 md2ppt 工具链渲染。
license: Apache-2.0
---

# Slides Generator - 智能幻灯片生成器

**设计理念**: 用户需求 → 规范 Markdown → md2ppt → Slidev 幻灯片

**唯一目标**: 无论用户输入什么,最终输出符合 INPUT_SPEC.md 的 Markdown,交给 md2ppt 渲染

---

## 🎯 核心架构

```
┌────────────────────────────────────────────┐
│           前链路 (本 Skill)                │
│  需求识别 → 模式选择 → 内容处理 → 规范化  │
└──────────────────┬─────────────────────────┘
                   │
         规范 Markdown
    (符合 INPUT_SPEC.md 的标准输入)
                   │
                   ▼
┌────────────────────────────────────────────┐
│         后链路 (md2ppt CLI)                │
│  读取 → 智能分页 → Slidev 渲染 → 预览     │
└────────────────────────────────────────────┘
```

**职责分离**:
- **本 Skill**: 只管生成规范 Markdown,不管渲染
- **md2ppt**: 只管读取规范 Markdown,不管内容

**关键文件**:
- `INPUT_SPEC.md` - 输入规范 (本 skill 内部)
- `FRONTEND_SPEC.md` - 前链路规范 (本 skill 内部)
- `/Users/Apple/dev/md2ppt` - md2ppt CLI 工具

---

## 🚀 触发识别

### 关键词

**明确触发**:
```
"生成幻灯片"
"制作 PPT"
"转换为 slides"
"创建演示文稿"
"做个教程"
```

**隐含触发**:
```
"把 XXX 做成可展示的"
"学习 XXX,需要材料"
"整理一下这个文档"
```

---

## 📊 智能模式选择

### 自动判断

```javascript
function selectMode(userInput) {
  // 判断输入类型
  if (isFile(userInput) || isURL(userInput)) {
    return 'TRANSFORM_MODE';  // 转换现有内容
  }

  // 判断是否需要深度教学
  if (hasTeachingKeywords(userInput)) {
    return 'GENERATE_DEEP';  // 深度教学
  }

  return 'GENERATE_STANDARD';  // 标准生成
}
```

### 模式对比

| 模式 | 触发 | 输入 | 输出规模 | 时间 | 场景 |
|------|------|------|---------|------|------|
| **转换** | 文件/URL | 现有文档 | 原结构 | 2-5分钟 | 快速格式化 |
| **生成-标准** | 主题词 | 搜集资料 | 50-100张 | 10-15分钟 | 快速了解 |
| **生成-深度** | 主题+教学 | 系统设计 | 100-200张 | 20-30分钟 | 深入学习 |

---

## 🔄 模式 1: 转换模式 (TRANSFORM)

### 适用场景

```
用户: "将 tutorial.md 转换为幻灯片"
用户: "把这个 URL 做成 PPT"
用户: "这段代码做成演示"
```

### 工作流程

**第 1 步: 获取内容**

| 输入 | 工具 | 操作 |
|------|------|------|
| `.md` 文件 | Read | 读取文件内容 |
| URL | Tavily Extract | 提取网页内容 |
| 文本 | 直接处理 | 内存操作 |

**第 2 步: 调用 input2slides v2.0**

```bash
cd /Users/Apple/.claude/skills/input2slides/cli

node index-v2.js <input> \
  --auto-format \
  --check-quality \
  --auto-fix \
  --max-line-width 100 \
  -o normalized.md
```

**关键参数**:
- `--max-line-width 100`: 符合 INPUT_SPEC.md 代码行宽要求
- `--auto-format`: 智能代码格式化
- `--check-quality`: 7 种质量检查
- `--auto-fix`: 自动修复问题

**第 3 步: 验证输出**

检查 `normalized.md` 是否符合本 skill 的 `INPUT_SPEC.md`:
- [ ] UTF-8 编码
- [ ] 代码行宽 ≤100 字符
- [ ] 代码块有语言标识
- [ ] Frontmatter YAML 正确
- [ ] 标题层级连续

**第 4 步: 调用 md2ppt**

```bash
cd /Users/Apple/dev/md2ppt
npm run build -- /Users/Apple/.claude/skills/input2slides/cli/normalized.md --open
```

### 完整示例

```
用户: "将 react-hooks.md 转换为幻灯片"

助手:
[步骤 1] 📖 读取文件
  ✅ Read(/path/to/react-hooks.md)

[步骤 2] 🔄 规范化处理
  ✅ 调用 input2slides v2.0
  ✅ 代码格式化完成
  ✅ 质量检查通过
  ✅ 输出: normalized.md

[步骤 3] ✅ 验证
  ✅ UTF-8 编码
  ✅ 代码行宽 ≤100
  ✅ Frontmatter 正确
  ✅ 标题层级连续

[步骤 4] 🎬 渲染
  ✅ 调用 md2ppt CLI
  ✅ Slidev 已启动: http://localhost:30301

📊 结果:
  - 输入: 150 行 Markdown
  - 输出: 25 张幻灯片
  - 章节: 5 章
  - 代码示例: 12 个
```

---

## 🎓 模式 2: 生成模式 (GENERATE)

### 适用场景

```
用户: "生成 TypeScript 教程"
用户: "创建 FastAPI 学习幻灯片,需要深入讲解"
用户: "关于 React Hooks 的演示,30 分钟演讲用"
```

### 工作流程

**第 1 步: 需求识别与模板选择**

根据用户输入,识别场景并加载对应模板:

| 场景 | 触发特征 | 模板文件 | 预期规模 |
|------|---------|---------|---------|
| **教学** | 库名/框架名 + "学习"/"教程" | `templates/teaching.md` | 100-150张 |
| **调研** | "调研"/"分析"/"对比" | `templates/research.md` | 50-80张 |
| **算法** | "LeetCode"/"算法题" | `templates/algorithm.md` | 60-100张 |
| **项目** | "源码"/"架构"/"解析" | `templates/project-analysis.md` | 80-120张 |

**识别步骤**:
1. 读取对应模板文件
2. 理解模板中的策略指导
3. 根据模板的交互策略向用户确认信息

**第 2 步: 用户交互确认**

根据模板的"交互策略"部分,向用户确认必要信息:

**教学场景示例**:
- "这个教程是给什么水平的人看?" (初学者/中级/高级)
- "希望多深入?" (快速了解/深入掌握/实战应用)

**调研场景示例**:
- "调研的目的是什么?" (技术选型/理论研究/趋势预测)
- "需要多深入的调研?" (概览级/标准级/深度级)

**第 3 步: 信息搜索**

根据模板的"信息搜索策略"部分,并行执行搜索:

```javascript
// 示例: 教学场景
Promise.all([
  // Context7: 官方文档 (最高优先级)
  mcp__context7__resolve_library_id({
    libraryName: topic
  }).then(result =>
    mcp__context7__get_library_docs({
      context7CompatibleLibraryID: result.id,
      tokens: 5000
    })
  ),

  // SearXNG: 教程和示例 (高优先级)
  mcp__searxng__searxng_web_search({
    query: `${topic} tutorial 2025`,
    max_results: 5
  }),

  // Tavily: 最佳实践 (中优先级)
  mcp__tavily_mcp__tavily_search({
    query: `${topic} best practices`,
    search_depth: 'advanced'
  })
])
```

**质量标准**:
- ✅ 内容完整 (非代码片段)
- ✅ 版本最新 (2025年或最新)
- ✅ 代码可运行
- ✅ 概念准确

**第 4 步: 内容生成**

根据模板的"内容生成策略"部分生成内容。

**示例: 教学场景 - 五段式展开**

每个核心概念按 5 个阶段展开 (5-8 张幻灯片):

1. **💡 为什么需要?** (1-2张)
   - 描述问题场景
   - 展示传统做法的痛点

2. **✅ 如何使用?** (2-3张)
   - 提供完整可运行的代码示例
   - 说明核心优势

3. **🔍 执行原理** (1张)
   - Mermaid 流程图
   - 关键步骤解析

4. **🎯 最佳实践与陷阱** (1-2张)
   - 正确 vs 错误示例
   - 常见错误分析

5. **🔧 实战建议** (1张)
   - 适用场景
   - 性能建议

**第 5 步: 规范化输出 (关键!)**

**必须保证**:

1. **代码行宽检查**:
```python
def validate_code_line_width(markdown):
    for block in extract_code_blocks(markdown):
        for i, line in enumerate(block.split('\n')):
            if len(line) > 100:
                raise ValueError(f"代码块第{i+1}行超过100字符")
```

2. **标题层级检查**:
```python
def validate_heading_hierarchy(markdown):
    headings = extract_headings(markdown)
    for i in range(len(headings)-1):
        if headings[i+1].level > headings[i].level + 1:
            raise ValueError("标题层级跳跃")
```

3. **Frontmatter 生成**:
```yaml
---
theme: default
highlighter: shiki
lineNumbers: false
title: {主题标题}
---
```

4. **代码块语言标识**:
```python
def ensure_code_language(markdown):
    # 所有 ``` 后必须有语言标识
    pattern = r'^```$'  # 无语言标识
    if re.search(pattern, markdown, re.MULTILINE):
        # 自动检测语言
        return fix_missing_language(markdown)
```

**第 6 步: 质量评分**

根据模板的"质量标准"部分进行评分:

```yaml
教学完整性 (40%):
  - 概念解释完整 (10分)
  - "为什么"深度 (10分)
  - 逻辑递进性 (10分)
  - 前后呼应 (10分)

内容深度 (30%):
  - 详细程度 (10分)
  - 原理分析 (10分)
  - 对比展示 (10分)

实践价值 (20%):
  - 代码完整性 (10分)
  - 可运行性 (10分)

视觉辅助 (10%):
  - 流程图清晰度 (10分)

总分 ≥ 85% 合格
```

**如果 <85%**: 识别最低维度,优化后重新评分

**第 7 步: 调用 md2ppt**

```bash
cd /Users/Apple/dev/md2ppt
npm run build -- /path/to/normalized.md --open
```

### 完整示例

```
用户: "生成 TypeScript 深度教程,面向有 JavaScript 基础的开发者"

助手:
[步骤 1] 🎯 场景识别
  ✅ 识别为: 教学场景
  ✅ 加载模板: templates/teaching.md

[步骤 2] 💬 需求确认
  - 主题: TypeScript
  - 受众: 中级 (有 JS 基础)
  - 深度: 深入级
  - 模式: 学习模式 (100-150张)
  ✅ 确认

[步骤 3] 📚 素材搜集 (并行)
  ✅ Context7: /microsoft/TypeScript
  ✅ SearXNG: TypeScript 2025 教程
  ✅ Tavily: TypeScript 官方文档
  📊 搜集到 12 篇高质量资料

[步骤 4] 🏗️ 架构设计
  ✅ 8 个章节
  ✅ 每章 5-8 个概念
  ✅ 五段式展开
  ✅ 预计 120-150 张

[步骤 5] ✍️ 生成内容
  ✅ 章节 1: 基础类型 (18张)
  ✅ 章节 2: 函数与接口 (22张)
  ✅ 章节 3: 泛型 (20张)
  ✅ 章节 4: 高级类型 (25张)
  ✅ 章节 5: 装饰器 (18张)
  ✅ 章节 6: 模块系统 (15张)
  ✅ 章节 7: 实战案例 (20张)
  ✅ 章节 8: 最佳实践 (12张)
  📊 共 150 张幻灯片

[步骤 6] 🔧 规范化处理
  ✅ 代码行宽检查 (≤100)
  ✅ 标题层级验证
  ✅ Frontmatter 生成
  ✅ 代码块语言标识
  ✅ 输出: typescript-tutorial.md

[步骤 7] 📊 质量评分
  - 教学完整性: 39/40 ⭐
  - 内容深度: 28/30 ⭐
  - 实践价值: 19/20 ⭐
  - 视觉辅助: 9/10 ⭐
  ✅ 总分: 95/100 (优秀)

[步骤 8] 🎬 渲染
  ✅ 调用 md2ppt CLI
  ✅ Slidev 已启动: http://localhost:30301

📊 最终结果:
  - 文件: typescript-tutorial.md
  - 幻灯片数: 150 张
  - 章节: 8 章
  - 代码示例: 45 个
  - 流程图: 12 个
  - 预计学习时长: 3-4 小时
```

---

## 🛠️ 工具链

### 前链路工具

**转换模式**:
- 工具: `/Users/Apple/.claude/skills/input2slides/cli/index-v2.js`
- 功能: 格式化现有内容

**生成模式**:
- 工具: 本 Skill 的模板系统
- 功能: 从头生成教学内容

### 后链路工具

**md2ppt CLI**:
- 位置: `/Users/Apple/dev/md2ppt`
- 功能: 读取规范 Markdown → 智能分页 → Slidev 渲染

### 规范文档

**INPUT_SPEC.md**:
- 位置: 本 skill 目录 (`INPUT_SPEC.md`)
- 作用: 定义规范 Markdown 的标准

**FRONTEND_SPEC.md**:
- 位置: 本 skill 目录 (`FRONTEND_SPEC.md`)
- 作用: 前链路处理流程和规范化要求

---

## ✅ 规范化检查清单

### 必须符合 INPUT_SPEC.md

**文件格式**:
- [ ] UTF-8 编码
- [ ] LF 换行符
- [ ] 开头有 Frontmatter
- [ ] Frontmatter 与内容间空一行

**标题规范**:
- [ ] ATX 风格 (`# 标题`)
- [ ] 层级连续 (H1 → H2 → H3, 无跳跃)
- [ ] 同级标题 >1 个才作为章节

**代码块规范**:
- [ ] 所有代码块有语言标识 (```python, ```javascript)
- [ ] 代码块正确闭合 (三个反引号)
- [ ] 代码行宽 ≤100 字符
- [ ] 超长行已智能换行

**Frontmatter 规范**:
- [ ] YAML 语法正确
- [ ] 仅包含 Slidev 官方字段
- [ ] 必需字段: theme, title

**禁止项**:
- [ ] 无 HTML 标签 (除 Slidev 指令)
- [ ] 无内联样式
- [ ] 无表格跨度语法
- [ ] 无脚注
- [ ] 无 TOC 指令

---

## 🔍 自动验证

**验证脚本**:

```bash
#!/bin/bash
# validate_normalized.sh

MD_FILE=$1

# 检查编码
if ! file $MD_FILE | grep -q "UTF-8"; then
    echo "❌ 编码错误: 非 UTF-8"
    exit 1
fi

# 检查 Frontmatter
if ! head -1 $MD_FILE | grep -q "^---$"; then
    echo "❌ Frontmatter 缺失"
    exit 1
fi

# 检查代码块闭合
code_blocks=$(grep -c '```' $MD_FILE)
if [ $((code_blocks % 2)) -ne 0 ]; then
    echo "❌ 代码块未闭合"
    exit 1
fi

echo "✅ 验证通过"
```

---

## 📖 使用示例

### 示例 1: 快速转换

```
用户: "将 tutorial.md 转换为幻灯片"

助手:
[转换模式]
✅ 读取 tutorial.md
✅ input2slides v2.0 处理
✅ 规范化完成
✅ md2ppt 渲染
🎉 完成! http://localhost:30301
```

### 示例 2: 标准生成

```
用户: "生成 React Hooks 教程,快速了解"

助手:
需求确认:
- 主题: React Hooks
- 受众: 初学者
- 深度: 标准 (快速了解)
- 模式: 标准生成 (50-100张)

[生成模式-标准]
✅ 素材搜集 (并行)
✅ 生成 8 章节 × 6张 = 48张
✅ 规范化输出
✅ md2ppt 渲染
🎉 完成! 48张幻灯片
```

### 示例 3: 深度教学

```
用户: "创建 FastAPI 深度教程,需要详细讲解依赖注入、中间件、数据库操作,面向有 Python 基础的开发者"

助手:
需求确认:
- 主题: FastAPI (依赖注入, 中间件, 数据库操作)
- 受众: 中级 (有 Python 基础)
- 深度: 深入级
- 模式: 学习模式 (100-150张)

[生成模式-深度]
✅ 素材搜集 (并行)
  - Context7: /tiangolo/fastapi
  - SearXNG: FastAPI 2025 tutorial
  - Tavily: FastAPI dependency injection
✅ 架构设计
  - 10 个章节
  - 五段式展开
  - 预计 120 张
✅ 生成内容 (120张)
✅ 规范化处理
✅ 质量评分: 94/100 ✨
✅ md2ppt 渲染
🎉 完成! 120张深度教学幻灯片
```

---

## ⚙️ 配置文件

### input2slides 配置

**文件**: `/Users/Apple/.claude/skills/input2slides/cli/.input2slidesrc.json`

```json
{
  "output": "normalized.md",
  "maxLineWidth": 100,
  "autoFormat": true,
  "checkQuality": true,
  "autoFix": true,
  "stats": true,
  "frontmatter": {
    "theme": "default",
    "highlighter": "shiki",
    "lineNumbers": false
  }
}
```

---

## 🎯 质量保证

### 输出质量等级

**Level 1: 基础合规** (必须)
- ✅ UTF-8 编码
- ✅ 代码行宽 ≤100
- ✅ Frontmatter 正确
- ✅ 标题层级连续

**Level 2: 内容质量** (生成模式)
- ✅ 教学完整性 ≥38/40
- ✅ 内容深度 ≥27/30
- ✅ 实践价值 ≥17/20
- ✅ 视觉辅助 ≥8/10

**Level 3: 用户体验** (后链路)
- ✅ 自动分页正确
- ✅ 代码高亮正常
- ✅ Mermaid 渲染正常

---

## 🚨 错误处理

### 常见问题

**问题 1: 代码行宽超限**

```
❌ 代码块第 23 行超过 100 字符
```

**解决**: 自动智能换行

```javascript
// 超长行
const result = someLongFunction(param1, param2, param3, param4);

// 自动修复为
const result = someLongFunction(
  param1, param2,
  param3, param4
);
```

---

**问题 2: 标题层级跳跃**

```
❌ 标题层级跳跃: H2 → H4
```

**解决**: 插入中间层级

```markdown
## H2
### H3  ← 插入
#### H4
```

---

**问题 3: 代码块未闭合**

```
❌ 代码块数量为奇数
```

**解决**: 自动补全闭合

---

**问题 4: 质量评分过低**

```
⚠️ 质量评分: 72/100 (不合格)
```

**解决**: 识别最低维度,优化后重新生成

---

## 📚 参考文档

**规范文档**:
- `INPUT_SPEC.md` - 输入规范 (本 skill 内部)
- `FRONTEND_SPEC.md` - 前链路规范 (本 skill 内部)

**外部工具**:
- `/Users/Apple/dev/md2ppt/CLAUDE.md` - md2ppt 项目规范

**工具文档**:
- `/Users/Apple/.claude/skills/input2slides/CLI_V2_GUIDE.md` - v2.0 完整指南

**模板文件**:
- `/Users/Apple/.claude/skills/slides-generator/templates/teaching.md` - 教学模板
- `/Users/Apple/.claude/skills/slides-generator/templates/research.md` - 调研模板
- `/Users/Apple/.claude/skills/slides-generator/templates/algorithm.md` - 算法模板
- `/Users/Apple/.claude/skills/slides-generator/templates/project-analysis.md` - 项目解析模板

---

## 🎉 总结

**本 Skill 的唯一目标**:
1. 识别用户需求
2. 选择最佳模式
3. 生成规范 Markdown (符合 INPUT_SPEC.md)
4. 调用 md2ppt 渲染
5. 交付 Slidev 幻灯片

**关键原则**:
- ✅ 前链路只管内容,不管渲染
- ✅ 后链路只管渲染,不管内容
- ✅ 中间用 INPUT_SPEC.md 解耦
- ✅ 所有模式最终都输出规范 Markdown
- ✅ 统一使用 md2ppt 渲染

**核心优势**:
- 🎯 智能模式选择
- 🔄 自动规范化输出
- ✅ 质量保证机制
- 🚀 统一工具链
- 📊 详细统计信息

---

**最后更新**: 2025-10-26
**版本**: 1.0.0
