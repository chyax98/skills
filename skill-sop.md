# Skill 构建 SOP

基于官方 anthropics/skills 仓库规范整理。

## 核心原则（官方）

**1. 简洁为王（Concise is Key）**
- 默认假设 Claude 已经很聪明
- 只添加 Claude 不知道的上下文
- 每条信息都要证明其 token 成本合理性
- 优先简洁示例，而非冗长解释

**2. 设置适当的自由度**
- **高自由度**（文本指令）：多种方法可行，依赖上下文决策
- **中等自由度**（伪代码/脚本+参数）：有偏好模式，允许变化
- **低自由度**（固定脚本）：操作脆弱易错，需严格遵循

**3. 渐进式披露（Progressive Disclosure）**
- Level 1：元数据（name + description）- 始终在上下文（~100词）
- Level 2：SKILL.md 主体 - 触发后加载（<5k词）
- Level 3：捆绑资源 - 按需加载（无限制）

---

## Skill 类型

### 工具型 Skill（Tool-oriented）
- **特点**：提供 API 参考、代码片段、快速入门
- **代表**：pdf, docx, xlsx, pptx
- **结构**：概述 → 快速开始 → 常用操作 → 参考文件
- **风格**：简洁直接，代码示例为主

### 流程型 Skill（Workflow-oriented）
- **特点**：多步骤流程，决策树，阶段划分
- **代表**：mcp-builder, doc-coauthoring, webapp-testing
- **结构**：阶段 → 步骤 → 检查点 → 迭代
- **风格**：过程性指导，清晰的执行顺序

---

## 标准结构

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter（必需）
│   │   ├── name（必需）
│   │   └── description（必需）
│   └── Markdown 指令（必需）
└── 捆绑资源（可选）
    ├── scripts/          # 可执行代码
    ├── references/       # 按需加载的文档
    └── assets/           # 输出中使用的文件
```

### SKILL.md 编写规范

**Frontmatter**：
```yaml
---
name: skill-name
description: 清晰描述做什么和何时使用（第三人称）
license: Apache-2.0
---
```

**正文风格**：
- 使用命令式/祈使式语气（"Use", "Create", "Follow"）
- 避免第二人称（不要"你应该"）
- 保持简洁（<500 行为佳）

**组织方式**：
- 工具型：概述 → 快速开始 → 按功能组织 → 参考
- 流程型：概述 → Phase/Stage 阶段化 → 检查清单 → 参考

---

## 创建流程

### 1. 收集使用场景

收集 3-5 个具体使用案例：
- 用户会说什么话触发？
- 期望产出是什么？
- 有哪些变化点？

### 2. 识别可复用资源

逐例分析：
- 需要哪些脚本？（重复编写的代码）
- 需要哪些参考？（schema、API 文档、规范）
- 需要哪些资产？（模板、图片、字体）

### 3. 初始化 Skill

```bash
scripts/init_skill.py skill-name --path output-dir
```

生成骨架，删除不需要的示例文件。

### 4. 编写 SKILL.md

**工具型 Skill**：
```markdown
# Skill Name

## Overview
简短说明（1-2 句话）

## Quick Start
```python
# 最简单的用法
```

## Common Tasks
### Task 1
代码示例

### Task 2
代码示例

## Reference Files
- reference.md - 详细文档
```

**流程型 Skill**：
```markdown
# Skill Name

## Overview
简短说明

## Workflow

### Phase 1: 阶段名称
1. 步骤说明
2. ...

**Output**: xxx

### Phase 2: 阶段名称
...

**Verification Checklist**:
- [ ] 检查项 1
- [ ] 检查项 2

## Reference Files
...
```

### 5. 关键要素

**必须包含**：
- 清晰的触发条件
- 执行步骤或使用方法
- 输出格式示例
- 参考文件指向

**流程型必须包含**：
- 阶段化流程（Phase/Stage）
- 验证检查清单（Checklist）
- 成功标准
- 决策树（如有条件分支）

**不要包含**：
- DEPTH 框架标记（不要显式标注）
- 多角色协作（除非真需要 sub-agent）
- 过度理论解释
- README/CHANGELOG 等无关文档

---

## 验收标准

**格式验收**：
- [ ] Frontmatter 完整（name + description）
- [ ] description 清晰说明何时使用
- [ ] SKILL.md < 500 行（主体）
- [ ] 使用命令式语气

**内容验收**：
- [ ] 提供清晰的执行步骤或使用方法
- [ ] 代码示例可直接使用
- [ ] 参考文件明确指向
- [ ] 避免冗余解释

**流程型额外验收**：
- [ ] 有阶段化流程（Phase/Stage）
- [ ] 有验证检查清单
- [ ] 有成功标准
- [ ] 关键步骤有 CRITICAL/MANDATORY 标记

---

## 最佳实践

**简洁优先**：
- 代码示例 > 文字说明
- 步骤清单 > 冗长叙述
- 决策树 > 复杂条件描述

**Reference 分离**：
- SKILL.md 保持精简
- 详细内容放 references/
- 明确说明何时读取

**示例丰富**：
- 每个功能 1-2 个完整示例
- 使用 ❌/✅ 对比展示正确用法
- 提供输出格式模板

**避免过度设计**：
- 不要引入复杂框架（除非确有必要）
- 不要过度强调（适度使用"必须"、"禁止"）
- 不要学院派（直接给方法，不要长篇理论）

---

## 常见问题

**Q: 何时使用 DEPTH 框架？**
A: DEPTH 是设计指南，不是执行框架。理解其思想（多视角、任务分解、检查标准），但不要在 SKILL.md 中显式标注 (DEPTH: X)。

**Q: 是否需要多角色协作？**
A: 仅在真正需要 sub-agent 的场景（如独立测试、并行评估）。大部分 skill 是单一 Claude 实例执行。

**Q: 检查清单应该多详细？**
A: 必须详细完备，这是质量保障的核心。每个检查项都要明确，包含修正动作。

**Q: 示例应该多少？**
A: 适度即可。每个功能/阶段 1-2 个完整示例，避免过多占用篇幅。

