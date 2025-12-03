---
name: mindmap-generator
description: This skill should be used when converting text, files, URLs, or code repositories into structured Markdown mindmaps. It provides format validation, structure review, and scenario-specific templates for concept analysis, technical architecture, process flows, and knowledge systems.
license: Apache-2.0
---

# 思维导图生成器

## 概述

将任意输入（文本、文件、URL、代码仓库）转换为结构化 Markdown 思维导图。

**核心能力**：
- 深度内容分析与概念提取
- 维度化思维框架设计
- 多场景模板支持
- 可选的格式验证工具

**适用场景**：概念分析、技术架构、流程梳理、知识体系构建

**触发短语**：
- "生成思维导图"、"转成脑图"、"mindmap"、"创建知识地图"

---

## 一、核心原则：思维导图 vs 文档大纲

### 1.1 什么是真正的思维导图

思维导图采用**放射性思维**（Radiant Thinking）——思想从中心概念向外辐射，如同神经连接。

| 特性 | 思维导图 | 文档大纲 |
|------|---------|---------|
| 目的 | 映射思维模式和概念关系 | 组织写作结构 |
| 结构 | 放射状，从中心向外 | 线性，自上而下 |
| 思维 | 发散思维，多维度同时探索 | 顺序思维，按阅读顺序 |
| 组织 | 按关系分组 | 按呈现顺序 |

### 1.2 关键区别

❌ **错误做法**（文档结构）：
```
# 主题
## 介绍           ← 文章开头
## 背景           ← 文章铺垫
## 主要内容
## 学习路径       ← 教程结构
## 参考资源       ← 文档附录
## 总结           ← 文章结尾
```

✅ **正确做法**（概念映射）：
```
# 核心概念
## What（定义）
## Why（价值）
## How（实现）
## When（场景）
## Relationships（关联）
## Limitations（约束）
```

### 1.3 禁止使用的文档式章节

- ❌ 介绍/背景/概述 → 融入 What/Why 维度
- ❌ 学习路径 → 融入 How 维度
- ❌ 参考资源 → 融入 Relationships 维度
- ❌ 总结要点 → 提取到核心维度
- ❌ 最佳实践 → 融入 How 维度

---

## 二、维度思维框架

根据主题类型选择合适的维度框架：

### 2.1 概念/技术类

| 维度 | 探索方向 |
|------|---------|
| What | 核心特征、定义 |
| Why | 解决的问题、价值 |
| How | 使用方式、实现模式 |
| When | 使用场景、时机 |
| Relationships | 相关概念、生态系统 |
| Limitations | 约束、权衡 |

### 2.2 流程/工作流类

| 维度 | 探索方向 |
|------|---------|
| Phases | 主要阶段 |
| Actors | 参与角色 |
| Resources | 所需资源 |
| Outputs | 交付产物 |
| Risks | 潜在风险 |

### 2.3 系统/架构类

| 维度 | 探索方向 |
|------|---------|
| Components | 核心组件 |
| Interactions | 组件交互 |
| Data Flow | 数据流转 |
| Technology | 技术栈 |
| Quality | 性能、安全 |

### 2.4 问题分析类

| 维度 | 探索方向 |
|------|---------|
| Symptoms | 现象表现 |
| Causes | 根本原因 |
| Impact | 影响范围 |
| Solutions | 解决方案 |
| Prevention | 预防措施 |

---

## 三、格式规范

### 3.1 标题层级

```markdown
# 一级 - 核心主题（全文唯一）
## 二级 - 主要分支（3-7 个）
### 三级 - 子分支
#### 四级 - 详细内容
##### 五级 - 细节（谨慎使用）
###### 六级 - 最大深度（避免）
```

### 3.2 内容标准

| 标准 | 说明 |
|------|------|
| 简洁 | 每节点 1-2 行 |
| 逻辑 | 同级并列，父子递进 |
| 完整 | 覆盖主题核心维度 |
| 清晰 | 表达明确，避免歧义 |
| 代码格式 | 代码/语法用反引号包裹 |

### 3.3 代码格式化

**重要**：所有代码元素必须用反引号包裹，防止思维导图软件 HTML 编码问题。

```markdown
✅ 正确：`func()`、`Literal["dev"]`、`BaseModel`
❌ 错误：func()、Literal['dev']（单引号易被编码为 &#39;）
```

---

## 四、工作流程

### Step 1: 收集背景信息

明确以下信息后再开始生成：

- **主题领域**：技术/商业/科学/艺术
- **目标受众**：入门/中级/专家
- **主要目的**：学习/规划/分析/展示
- **深度要求**：概览/详细/专家级
- **特殊约束**：任何特定要求

**信息来源**：
- 用户直接提供 → 直接使用
- 上下文不清 → 询问澄清
- 需要研究 → 使用 SearXNG MCP 搜索

### Step 2: 研究与分析内容

根据输入类型进行内容提取：

| 输入类型 | 分析方法 |
|---------|---------|
| 文本描述 | 直接解析内容 |
| 文件路径 | 使用 Read 工具读取 |
| URL | 使用 SearXNG MCP 获取 |
| 代码仓库 | 分析目录结构和代码组织 |

**分析要点**：
1. 识别核心概念和定义
2. 提取概念间的关系
3. 收集用例和示例
4. 记录约束和限制

详细策略参见 `references/content-analysis.md`

### Step 3: 设计维度框架

根据主题类型选择维度框架（见第二节），设计原则：

- 使用 3-7 个主要分支（认知负荷限制）
- 每个分支探索一个维度
- 避免顺序/时间线组织（除非分析流程）
- 聚焦概念关系，而非阅读顺序

### Step 4: 结构化内容

按维度组织内容：

1. **中心主题**（H1）：2-5 词核心概念
2. **主要分支**（H2）：3-7 个维度视角
3. **子分支**（H3-H4）：各维度下的详细概念
4. **支撑细节**（H5-H6）：示例、具体内容（谨慎使用）

**组织原则**：
- 横向思维：同级节点平行（相同抽象层次）
- 纵向思维：父子节点递进（逐步深入）
- 平衡：各主要分支深度相近
- 简洁：每节点最多 1-2 行

详细策略参见 `references/content-structuring.md`

### Step 5: 自检与保存

**哲学检查**：
- ✅ 采用放射性思维结构？
- ✅ 使用维度化组织？
- ❌ 包含文档式章节？
- ✅ 展示概念关系而非顺序叙述？

**质量检查**：
- 主要分支：3-7 个？
- 分支深度：2-5 层？
- 节点内容：1-2 行？
- 代码元素：反引号包裹？

**可选验证**（脚本辅助）：
```bash
./scripts/validate-mindmap.sh <file-path>   # 格式验证
./scripts/review-mindmap.sh <file-path>     # 结构审查
```

---

## 五、输出配置

**路径优先级**：
1. 用户指定路径 → 使用用户路径
2. 未指定 → `./mindmap/`（当前工作目录下，自动创建）

**文件命名**：`{主题}-{类型}-{日期}.md`
- 示例：`react-hooks-concept-20251204.md`
- 自动清理特殊字符

**注意**：输出基于当前工作目录 `$PWD`，非 skill 安装目录

---

## 六、模板库

根据场景按需参考：

| 场景 | 模板文件 | 适用情况 |
|------|---------|---------|
| 概念分析 | `assets/templates/concept-analysis.md` | 解释概念、技术、理论 |
| 技术架构 | `assets/templates/technical-architecture.md` | 系统设计、架构分析 |
| 流程梳理 | `assets/templates/process-flow.md` | 工作流程、操作步骤 |
| 知识体系 | `assets/templates/knowledge-system.md` | 学习地图、知识整理 |

---

## 七、常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 层级过深 | 过度细分 | 合并相似节点，限制 4-5 层 |
| 节点过长 | 细节过多 | 提取关键词，详情移至文档 |
| 逻辑混乱 | 分类标准不一 | 重新审视维度，统一标准 |
| HTML 编码 | 特殊字符未包裹 | 代码元素用反引号，优先双引号 |

---

## 八、工具脚本

脚本为**可选辅助工具**，核心生成依赖 AI 分析能力。

### 格式验证

```bash
./scripts/validate-mindmap.sh <file-path>
# 选项：-v (详细) -s (严格) --no-color
```

检查：标题层级、格式规范、Markdown 语法

### 结构审查

```bash
./scripts/review-mindmap.sh <file-path>
# 选项：-v (详细) -s (摘要) -j (JSON)
```

检查：内容规模、结构平衡、单子节点、同级数量

详细错误代码参见 `references/validation-checklist.md`

---

## 参考资源

### 指南
- 内容分析：`references/content-analysis.md`
- 结构化策略：`references/content-structuring.md`

### 规范
- 格式规则：`references/mindmap-format-rules.md`
- 验证清单：`references/validation-checklist.md`

### 模板
- 概念分析：`assets/templates/concept-analysis.md`
- 技术架构：`assets/templates/technical-architecture.md`
- 流程梳理：`assets/templates/process-flow.md`
- 知识体系：`assets/templates/knowledge-system.md`
