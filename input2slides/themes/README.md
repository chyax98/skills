# Marp 主题说明

当前 learn2slides 使用内联 `style` 在 frontmatter 中定义样式。

未来可以扩展为独立主题文件，使用方式：

```yaml
---
marp: true
theme: learn2slides-midnight
---
```

## 主题开发计划

### 1. midnight.css - 深色专业
- 背景: 深色渐变
- 文字: 浅色
- 强调: 红色
- 适合: 技术分享、编程教程

### 2. warm.css - 暖色温馨
- 背景: 暖色渐变
- 文字: 深棕色
- 强调: 橙色
- 适合: 教学场景、设计内容

### 3. focus.css - 极简聚焦
- 背景: 纯白
- 文字: 纯黑
- 强调: 蓝色
- 适合: 内容密集、学术报告

## 当前使用方式

在 SKILL.md 的 Step 3 中，直接在 frontmatter 嵌入 style：

```yaml
---
marp: true
theme: default
style: |
  section {
    font-size: 20px;
    ...
  }
---
```

这种方式简单直接，无需额外文件。
