---
name: zxm-generator
description: This skill generates ZhiXi mindmap files (.zxm) from Markdown with inline decorations. Use `<<{JSON}>>` at line end for styling (colors, icons, progress, etc.). Supports learning notes, knowledge systems, project planning, concept analysis, tech architecture, and troubleshooting scenarios. Trigger phrases include "生成 zxm", "知犀导图", "思维导图文件".
license: MIT
---

# ZXM 思维导图生成器

将 Markdown 转换为知犀思维导图原生文件（.zxm）。

**核心特性**：单文件内联装饰
- Markdown 定义结构
- `<<{JSON}>>` 添加装饰（可选）
- 一个文件搞定一切

---

## 通用设计原则

### Tony Buzan 法则

- 从中心向外发散，模拟放射性思维
- 节点使用关键词/短语，避免长段落
- 使用颜色和图标增强记忆
- 分支层级递进，从粗到细

### Miller's Law（7±2）

- 工作记忆容量 5-9 个项目
- 主分支控制在 **3-7 个**
- 超过 7 个会增加认知负荷

### 层级原则

- **横向**：同级节点平行、互斥
- **纵向**：父子节点递进、深入
- **深度**：建议 2-5 层，避免过深

---

## 场景路由

### Step 0: 判断场景并加载指南

根据用户需求判断场景类型，**读取对应的场景指南**：

| 场景 | 特征 | 加载文件 |
|------|------|----------|
| **学习笔记** | 学习技术、整理课程、复习备考 | `references/scenarios/learning-notes.md` |
| **知识体系** | 领域图谱、系统梳理、知识框架 | `references/scenarios/knowledge-system.md` |
| **项目规划** | 任务拆解、方案设计、需求分析 | `references/scenarios/project-planning.md` |
| **概念分析** | 深度理解、技术对比、问题分析 | `references/scenarios/concept-analysis.md` |
| **技术方案** | 架构设计、模块设计、技术选型 | `references/scenarios/tech-architecture.md` |
| **故障排查** | 问题诊断、根因分析、排查流程 | `references/scenarios/troubleshooting.md` |

**执行步骤**：
1. 分析用户需求，判断最匹配的场景
2. 使用 Read 工具加载对应场景文件
3. 按场景指南中的规范生成思维导图

**默认场景**：学习笔记（如无法明确判断）

---

## 工作流程

### Step 1: 创建输出目录

在**当前工作目录**创建文件夹：

```
./{主题名称}/
├── {主题名称}.md       # Markdown 源文件
└── {主题名称}.zxm      # 生成的思维导图
```

### Step 2: 编写 Markdown

使用标题层级（`#`）+ 内联装饰（`<<{...}>>`）：

```markdown
# 主题名称 <<{"theme":"ai-classical1","bg":"#4A90D9","fc":"#FFF","bold":true}>>
## 一级分支 <<{"priority":1,"mark":"flag"}>>
### 二级节点
### 重点节点 <<{"star":5}>>
## 一级分支 <<{"priority":2}>>
### 二级节点
```

**规则**：
- `#` 数量 = 层级深度
- 每行一个节点
- 行末 `<<{JSON}>>` 添加装饰（可选）
- 无装饰的节点保持纯净
- 按场景指南中的维度组织内容

### Step 3: 生成 ZXM 文件

```bash
uv run zxm_generator.py 主题.md -o 主题.zxm
```

### Step 4: 打开文件

```bash
open "./{主题名称}/{主题名称}.zxm"
```

---

## 内联装饰语法

### 全局配置（在根节点设置）

```markdown
# 主题 <<{"theme":"ai-classical1","template":"right","bg":"#4A90D9"}>>
```

| 字段 | 说明 | 可选值 |
|------|------|--------|
| `theme` | 主题风格 | `ai-classical1`(推荐), `classical2`, `dark` |
| `template` | 布局方向 | `right`, `left`, `both`, `tree`, `org` |

### 样式字段

| 字段 | 作用 | 示例 |
|------|------|------|
| `bg` | 背景色 | `"#4A90D9"` |
| `fc` | 字体色 | `"#FFFFFF"` |
| `bold` | 加粗 | `true` |

### 功能字段

| 字段 | 作用 | 范围/格式 |
|------|------|-----------|
| `priority` | 优先级 ①②③ | 1-20 |
| `star` | 星级 ★★★ | 1-10 |
| `progress` | 进度条 | 1-9 |
| `todo` | 待办 | `"done"`/`"undone"` |
| `note` | 备注（支持 `\n` 换行） | 文本 |
| `link` | 链接 | URL |

### 图标字段

| 字段 | 常用值 |
|------|--------|
| `mark` | `flag`, `star`, `check`, `warning`, `target`, `trophy`, `lightbulb`, `fire` |
| `expression` | `cool`, `happy`, `sad` |
| `avatar` | `avatar-blue`, `avatar-green`, `avatar-orange` |

完整列表见 `references/schema.md`。

---

## 自检清单

**通用检查**：
- [ ] 主分支 3-7 个？
- [ ] 层级深度 2-5 层？
- [ ] 同级节点互斥、平行？
- [ ] 内联装饰 JSON 格式正确？

**场景检查**：参照所加载的场景指南

**验证命令**：
```bash
uv run zxm_generator.py 主题.md --validate
```

---

## 参考资源

- DSL 规范：`references/schema.md`
- 场景指南：`references/scenarios/*.md`
- 生成器脚本：`scripts/zxm_generator.py`
