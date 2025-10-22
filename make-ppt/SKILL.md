---
name: make-ppt
description: Use this skill when the user wants to create professional HTML presentation slides. Automatically collects learning materials from various sources (web search, URLs, documentation, local files), generates rich Markdown content following content density rules, and renders to beautiful HTML slides using reveal-md.
license: Apache-2.0
---

# 执行流程

按照以下 5 个步骤完成 PPT 生成：

## 步骤 1: 收集学习资料

根据用户输入类型，自动获取内容：

| 用户输入 | 处理方式 |
|---------|---------|
| **主题关键词** | 用 SearXNG 搜索 top 3 结果，提取内容 |
| **URL 链接** | 用 Tavily Extract 提取 markdown |
| **官方文档** | 用 Context7 MCP 查询 |
| **本地文件** | 用 Read 工具读取 |
| **已有内容** | 直接使用 |

## 步骤 2: 生成充实的 Markdown

**内容密度规则**：时长(分钟) × 0.8 = 幻灯片数量

**质量要求**：
- 每个核心概念 ≥ 3 张幻灯片
- 包含：定义 + 解释 + 示例
- 使用 fragment 实现渐进式展示

**Markdown 格式规范**：

```markdown
---
theme: black
---

# {主题标题}

{副标题}

---

## 目录

1. {章节 1}
2. {章节 2}

---

### {概念名称}

**定义**：{简洁定义}

<!-- .element: class="fragment" -->

- 要点 1 <!-- .element: class="fragment" -->
- 要点 2 <!-- .element: class="fragment" -->

---

\`\`\`javascript
// 代码示例
function example() {}
\`\`\`

---
```

## 步骤 3: 保存 Markdown

使用 Write 工具保存到：
```
/Users/Apple/dev/skills/make-ppt/output/slides.md
```

## 步骤 4: 渲染 HTML

使用 Bash 工具执行：

```bash
cd /Users/Apple/dev/skills/make-ppt && \
mkdir -p output/html && \
npx reveal-md output/slides.md --static output/html --theme black
```

## 步骤 5: 交付成果

告诉用户：

```
✅ PPT 生成完成！

📁 文件: /Users/Apple/dev/skills/make-ppt/output/html/index.html

🚀 双击打开，使用 ←/→ 导航
```

---

# 快速模板参考

### 封面模板
```markdown
# {标题}
{副标题}
---
```

### 内容模板
```markdown
### {小标题}
- 要点 <!-- .element: class="fragment" -->
---
```

### 代码模板
```markdown
\`\`\`{lang}
{code}
\`\`\`
---
```
