# Claude Skills 构建规范 - 快速参考

这是 Claude Skills 的完整构建规范和最佳实践指南。

---

## 📋 目录

1. [核心规范](#核心规范)
2. [文件结构](#文件结构)
3. [SKILL.md 规范](#skillmd-规范)
4. [资源目录规范](#资源目录规范)
5. [命名规范](#命名规范)
6. [最佳实践](#最佳实践)
7. [质量检查清单](#质量检查清单)
8. [常见错误](#常见错误)

---

## 核心规范

### 必需元素

每个 Skill **必须**包含:
- ✅ `SKILL.md` - 核心文件,包含 YAML frontmatter 和 Markdown 指令
- ✅ `name` - Skill 名称 (YAML frontmatter)
- ✅ `description` - 触发说明 (YAML frontmatter,第三人称)

### 强烈推荐

- 📖 `README.md` - 用户使用文档
- 📄 `LICENSE.txt` - 许可证文件

### 可选资源

- 📂 `scripts/` - 可执行脚本
- 📚 `references/` - 参考文档
- 🎨 `assets/` - 输出资源

---

## 文件结构

### 标准结构

```
skill-name/
├── SKILL.md              ⭐ 核心文件 (必需)
├── README.md             📖 使用文档 (推荐)
├── LICENSE.txt           📄 许可证 (推荐)
├── scripts/              📂 可执行脚本 (可选)
│   └── example.py
├── references/           📚 参考文档 (可选)
│   └── api_spec.md
└── assets/               🎨 输出资源 (可选)
    ├── templates/
    ├── styles/
    └── examples/
```

### 扩展结构 (复杂 Skill)

```
skill-name/
├── SKILL.md
├── README.md
├── INSTALLATION.md       # 安装指南
├── QUICKSTART.md         # 快速开始
├── LICENSE.txt
├── scripts/
│   ├── main.py
│   └── utils.py
├── references/
│   ├── api_spec.md
│   └── workflow.md
├── assets/
│   ├── templates/
│   │   ├── template1.html
│   │   └── template2.md
│   ├── styles/
│   │   └── base.css
│   └── examples/
│       └── example.html
└── docs/                 # 开发文档 (可选)
    ├── README.md
    └── DESIGN.md
```

---

## SKILL.md 规范

### YAML Frontmatter

**格式**:
```yaml
---
name: skill-name
description: This skill should be used when...
license: Apache-2.0
---
```

**name 规范**:
- ✅ 小写字母
- ✅ 用连字符 `-` 分隔单词
- ✅ 描述性强
- ❌ 不使用下划线
- ❌ 不使用驼峰命名

**示例**:
```yaml
✅ name: learning-to-html-presentation
✅ name: pdf-editor
✅ name: markdown-to-pdf

❌ name: MySkill
❌ name: skill_name
❌ name: pdfEditor
```

**description 规范**:
- ✅ 使用第三人称("This skill should be used when...")
- ✅ 明确说明触发场景
- ✅ 具体描述功能
- ✅ 长度适中 (50-200 字)
- ❌ 不使用第二人称("Use this when you...")
- ❌ 不使用祈使句("Transform documents...")

**优秀示例**:
```yaml
# ✅ 优秀
description: This skill should be used when the user wants to transform learning content (text, Markdown, transcripts) into visually stunning HTML presentations with PPT-style slides.

# ✅ 优秀
description: This skill should be used when Claude needs to create, edit, or analyze PowerPoint presentations (.pptx files) including layouts, comments, and speaker notes.

# ⚠️ 可接受但可改进
description: This skill helps create presentations from documents.

# ❌ 错误
description: Use this skill to make presentations.

# ❌ 错误
description: Transform learning content into presentations.
```

### Markdown 内容规范

**写作风格**:
- ✅ 使用祈使句/不定式 ("To create X, do Y")
- ✅ 客观、指令性语言
- ❌ 避免第二人称 ("你应该...")
- ❌ 避免对话式语气

**示例**:
```markdown
# ✅ 正确
To create a presentation, provide learning content in text or Markdown format.

# ✅ 正确
Transform learning content by following these steps:
1. Analyze content structure
2. Extract key points
3. Generate HTML output

# ❌ 错误
You should provide learning content to create a presentation.

# ❌ 错误
Hi! Let's create a presentation together. You'll need to...
```

**推荐结构**:
```markdown
# Skill Name

## Overview
Brief introduction to the skill's purpose and value.

## When to Use
Clear explanation of trigger scenarios and use cases.

## How It Works
### Step 1: First Step
Detailed instructions...

### Step 2: Second Step
Detailed instructions...

## Resources
(If applicable) Explanation of bundled resources.

## Examples
2-3 concrete usage examples.

## Technical Details
(Optional) Implementation details.
```

---

## 资源目录规范

### scripts/ - 可执行脚本

**何时使用**:
- ✅ 需要确定性执行的代码
- ✅ 重复编写相同逻辑的代码
- ✅ 性能敏感的操作
- ✅ 外部工具集成

**示例场景**:
```python
# scripts/rotate_pdf.py
# 用于: PDF 旋转操作,避免每次重写

# scripts/generate_chart.py
# 用于: 数据可视化,确保一致性

# scripts/validate_schema.py
# 用于: 数据验证,确定性检查
```

**优势**:
- Token 高效 (可执行而无需读入上下文)
- 确定性结果
- 可重用性高

**注意事项**:
- Claude 可能需要读取脚本进行调试或环境适配
- 提供清晰的使用说明和注释
- 包含错误处理

### references/ - 参考文档

**何时使用**:
- ✅ 详细的 API 规范
- ✅ 数据库 Schema
- ✅ 公司政策文档
- ✅ 详细工作流程指南
- ✅ 领域知识库

**示例场景**:
```markdown
# references/api_spec.md
# 用于: API 集成时查阅规范

# references/database_schema.md
# 用于: 数据库操作时参考结构

# references/company_policies.md
# 用于: 生成符合公司规范的内容

# references/workflow.md
# 用于: 复杂流程的详细说明
```

**优势**:
- 保持 SKILL.md 简洁
- 按需加载,节省上下文
- 便于维护和更新

**最佳实践**:
- 信息不重复 (SKILL.md 或 references,选其一)
- 详细信息优先放 references
- 大文件 (>10k 词) 提供 grep 模式
- SKILL.md 中说明如何使用 references

### assets/ - 输出资源

**何时使用**:
- ✅ 模板文件 (HTML/CSS/JS)
- ✅ 图片资源 (logo/icons)
- ✅ 字体文件
- ✅ 样板代码
- ✅ 示例文件

**示例场景**:
```
# assets/templates/email-template.html
# 用于: 生成格式化的邮件

# assets/logo.png
# 用于: 品牌文档生成

# assets/frontend-boilerplate/
# 用于: 快速搭建前端项目

# assets/examples/sample-output.pdf
# 用于: 展示输出效果
```

**优势**:
- 不占用上下文窗口
- 可直接复制或修改使用
- 版本化管理资源

**组织建议**:
```
assets/
├── templates/      # 模板文件
├── styles/         # CSS 样式
├── scripts/        # JS 脚本 (用于输出,非执行脚本)
├── images/         # 图片资源
├── fonts/          # 字体文件
└── examples/       # 示例输出
```

---

## 命名规范

### Skill 名称

**规则**:
- 小写字母
- 连字符分隔
- 描述性强
- 避免缩写 (除非广为人知)

**示例**:
```
✅ markdown-to-pdf
✅ learning-to-html-presentation
✅ database-schema-analyzer
✅ pdf-editor

❌ md2pdf (不清晰)
❌ MySkill (驼峰)
❌ skill_builder (下划线)
❌ s1 (无意义)
```

### 文件命名

**原则**:
- 清晰描述文件内容
- 使用小写或小写连字符
- 避免空格

**示例**:
```
✅ api_specification.md
✅ user-authentication.md
✅ generate_report.py
✅ email-template.html

❌ doc.md (不清晰)
❌ File 1.md (空格)
❌ SPEC.MD (全大写)
```

### 目录命名

**规则**:
- 使用复数形式 (scripts/, templates/)
- 小写字母
- 描述性强

**示例**:
```
✅ scripts/
✅ references/
✅ templates/
✅ examples/

❌ script/ (单数)
❌ Scripts/ (大写)
❌ ref/ (缩写)
```

---

## 最佳实践

### 1. 渐进式信息披露

**三层加载系统**:
1. **Metadata** - 始终在上下文 (~100 词)
2. **SKILL.md body** - Skill 触发时加载 (<5k 词)
3. **Bundled resources** - 按需加载 (无限制)

**示例**:
```markdown
# SKILL.md (简洁)
## Overview
Brief intro...

## How to Use
Core workflow...

For detailed API specs, see references/api_spec.md
For database schema, see references/database.md

---

# references/api_spec.md (详细)
[10k+ 词的详细 API 文档]

# references/database.md (详细)
[详细的数据库 Schema 和关系]
```

### 2. 单一职责原则

每个资源文件只做一件事:
```
✅ scripts/convert_to_pdf.py        - 只负责转换
✅ scripts/validate_markdown.py     - 只负责验证

❌ scripts/do_everything.py         - 功能过多
```

### 3. 示例驱动开发

提供具体、可执行的示例:
```markdown
## Examples

### Example 1: Convert Markdown to PDF
Input:
```
# My Document
This is a test.
```

Output: `my-document.pdf` with cover, TOC, and formatted content.

### Example 2: Technical Report
Input: Technical specification in Markdown
Output: Professional PDF with syntax highlighting
```

### 4. 错误处理

在 scripts 中包含清晰的错误处理:
```python
# ✅ 好的错误处理
try:
    result = process_file(input_path)
except FileNotFoundError:
    print(f"Error: File not found: {input_path}")
    sys.exit(1)
except ValidationError as e:
    print(f"Validation failed: {e}")
    sys.exit(2)

# ❌ 差的错误处理
result = process_file(input_path)  # 可能崩溃
```

### 5. 文档一致性

确保所有文档风格一致:
- 使用相同的术语
- 统一的格式
- 一致的示例风格

---

## 质量检查清单

### 文件结构检查

```yaml
✅ 必需文件:
  - [ ] SKILL.md 存在
  - [ ] YAML frontmatter 格式正确
  - [ ] name 符合命名规范
  - [ ] description 使用第三人称

✅ 推荐文件:
  - [ ] README.md 存在且完整
  - [ ] LICENSE.txt 包含有效许可证

✅ 可选资源:
  - [ ] scripts/ 目录结构合理 (如有)
  - [ ] references/ 目录结构合理 (如有)
  - [ ] assets/ 目录结构合理 (如有)
```

### SKILL.md 质量检查

```yaml
✅ YAML Frontmatter:
  - [ ] name: 小写连字符格式
  - [ ] description: 第三人称,50-200 字
  - [ ] description 明确说明触发场景
  - [ ] license: 有效的许可证标识 (如有)

✅ Markdown 内容:
  - [ ] 使用祈使句/不定式风格
  - [ ] 避免第二人称
  - [ ] 结构清晰 (Overview → How to Use → Examples)
  - [ ] 包含 2-3 个具体示例
  - [ ] 如有资源,清晰说明如何使用

✅ 技术质量:
  - [ ] 无 Markdown 语法错误
  - [ ] 链接有效
  - [ ] 代码块有语言标识
  - [ ] 格式统一美观
```

### README.md 质量检查

```yaml
✅ 内容完整性:
  - [ ] Skill 简介
  - [ ] 安装步骤
  - [ ] 使用示例
  - [ ] 特性说明
  - [ ] 常见问题 (可选)

✅ 用户友好性:
  - [ ] 语言通俗易懂
  - [ ] 示例具体可执行
  - [ ] 步骤清晰
  - [ ] 提供快速开始指南
```

### 资源文件检查

```yaml
✅ scripts/:
  - [ ] 每个脚本有清晰的注释
  - [ ] 包含使用说明
  - [ ] 错误处理完善
  - [ ] 在 SKILL.md 中有引用说明

✅ references/:
  - [ ] 文档结构合理
  - [ ] 内容详尽准确
  - [ ] 在 SKILL.md 中说明如何使用
  - [ ] 避免与 SKILL.md 重复

✅ assets/:
  - [ ] 资源文件完整可用
  - [ ] 目录组织清晰
  - [ ] 在 SKILL.md 中有说明
  - [ ] 文件命名规范
```

---

## 常见错误

### 1. Description 错误

```yaml
# ❌ 错误: 使用第二人称
description: Use this skill when you want to create presentations.

# ✅ 正确: 使用第三人称
description: This skill should be used when the user wants to create presentations.

---

# ❌ 错误: 过于模糊
description: This skill helps with documents.

# ✅ 正确: 具体明确
description: This skill should be used when the user wants to transform Markdown documents into professionally formatted PDF reports with custom styling.

---

# ❌ 错误: 使用祈使句
description: Transform learning content into presentations.

# ✅ 正确: 使用陈述句
description: This skill should be used when transforming learning content into presentations.
```

### 2. 命名错误

```yaml
# ❌ 错误的 Skill 名称
name: MyAwesomeSkill       # 驼峰命名
name: pdf_converter        # 下划线
name: PDFTool              # 大写
name: s1                   # 无意义

# ✅ 正确的 Skill 名称
name: pdf-converter
name: markdown-to-html
name: document-analyzer
```

### 3. 文档风格错误

```markdown
# ❌ 错误: 使用第二人称
You should provide a Markdown file to convert.

# ✅ 正确: 使用祈使句
Provide a Markdown file to convert.

---

# ❌ 错误: 对话式语气
Hey! Let's create a presentation. First, you'll need to...

# ✅ 正确: 指令式语气
To create a presentation, provide learning content in the following format:
```

### 4. 资源组织错误

```
# ❌ 错误: 混乱的目录结构
skill-name/
├── file1.md
├── script.py
├── doc.md
├── template.html
└── stuff/

# ✅ 正确: 清晰的目录结构
skill-name/
├── SKILL.md
├── README.md
├── scripts/
│   └── convert.py
├── references/
│   └── api_spec.md
└── assets/
    └── templates/
        └── default.html
```

### 5. 信息重复错误

```markdown
# ❌ 错误: SKILL.md 和 references/ 重复内容
# SKILL.md
## API Specification
[10k 词的详细 API 文档]

# references/api_spec.md
[完全相同的 10k 词 API 文档]

---

# ✅ 正确: SKILL.md 简洁,references/ 详细
# SKILL.md
## API Integration
For API integration, refer to the detailed specification in references/api_spec.md

Key endpoints:
- POST /convert - Convert documents
- GET /status - Check conversion status

# references/api_spec.md
[详细的 API 文档]
```

---

## 快速参考表

### Skill 元素速查

| 元素 | 必需性 | 位置 | 说明 |
|------|--------|------|------|
| SKILL.md | ✅ 必需 | 根目录 | 核心文件 |
| name | ✅ 必需 | YAML frontmatter | 小写连字符 |
| description | ✅ 必需 | YAML frontmatter | 第三人称,50-200 字 |
| README.md | 📖 推荐 | 根目录 | 用户文档 |
| LICENSE.txt | 📄 推荐 | 根目录 | 许可证 |
| scripts/ | 📂 可选 | 根目录 | 可执行脚本 |
| references/ | 📚 可选 | 根目录 | 参考文档 |
| assets/ | 🎨 可选 | 根目录 | 输出资源 |

### 写作风格速查

| 场景 | ✅ 使用 | ❌ 避免 |
|------|--------|--------|
| description | 第三人称 | 第二人称 |
| SKILL.md 指令 | 祈使句/不定式 | 对话式 |
| README.md | 用户友好 | 过于技术 |
| 示例 | 具体可执行 | 抽象模糊 |

### 命名规范速查

| 类型 | 格式 | 示例 | 错误示例 |
|------|------|------|----------|
| Skill 名称 | 小写连字符 | pdf-editor | PDFEditor, pdf_editor |
| 文件名 | 小写/小写连字符 | api_spec.md | API-SPEC.MD |
| 目录名 | 复数小写 | scripts/ | Script/, SCRIPTS/ |

---

## 相关资源

- [Claude Skills 官方文档](https://docs.anthropic.com/claude/docs/skills)
- [Agent Skills 规范](../agent_skills_spec.md)
- [Skill Creator Skill](../skill-creator/SKILL.md)
- [官方 Skills 示例](https://github.com/anthropics/skills)
- [交互式构建命令](.claude/commands/build-skill.md)

---

**最后更新**: 2025-10-21
**版本**: 1.0.0
**维护者**: chyax98
