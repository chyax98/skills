# doc2slides + Slidev 集成技术规范

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    doc2slides 工作流                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  用户输入文档 (Markdown/PDF/URL)                               │
│           ↓                                                   │
│  Claude (doc2slides skill) 分析 + 生成                         │
│           ↓                                                   │
│  输出: slides.md (Slidev 格式)                                 │
│           ↓                                                   │
│  doc2slides CLI (基于 Slidev)                                 │
│           ↓                                                   │
│  ┌─────────────────────────────────────┐                    │
│  │  渲染选项:                            │                    │
│  │  - HTML (开发/预览)                   │                    │
│  │  - PDF (分享)                        │                    │
│  │  - PPTX (PowerPoint)                 │                    │
│  │  - PNG (图片序列)                     │                    │
│  └─────────────────────────────────────┘                    │
│           ↓                                                   │
│  用户可以切换主题,无需重新生成内容                               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 输出格式规范

### 基础格式 (Slidev 兼容)

```markdown
---
theme: doc2slides-midnight
title: "TypeScript 完整教程"
author: "Claude"
date: "2025-10-23"
layout: cover
---

# TypeScript 完整教程
## 从入门到精通

---
layout: default
---

# 为什么需要 TypeScript?

JavaScript 是动态类型语言:

- 运行时错误难以预防
- 重构困难
- IDE 智能提示有限

TypeScript 提供静态类型检查。

---
layout: two-cols
---

# 类型注解

::left::

基础类型:

```typescript
let name: string = "Alice"
let age: number = 30
let isActive: boolean = true
```

::right::

联合类型:

```typescript
let id: string | number
id = "abc"  // ✅
id = 123    // ✅
```

---
layout: center
class: text-center
---

# 谢谢观看!

---
```

### 支持的 Layout 类型

| Layout | 用途 | 示例 |
|--------|------|------|
| `cover` | 封面页 | 标题 + 副标题 |
| `default` | 标准内容页 | 正文 + 代码 |
| `center` | 居中内容 | 重点强调 |
| `two-cols` | 左右分栏 | 对比展示 |
| `section` | 章节分隔 | 大标题过渡 |
| `quote` | 引用页 | 名人名言 |
| `fact` | 数据展示 | 统计数字 |
| `image-right` | 图文混排 | 图片在右 |
| `image-left` | 图文混排 | 图片在左 |

## 主题系统规范

### 主题包结构

```
@doc2slides/theme-midnight/
├── package.json
├── layouts/
│   ├── cover.vue
│   ├── default.vue
│   ├── two-cols.vue
│   └── ...
├── styles/
│   ├── index.css
│   ├── code.css
│   └── layouts.css
├── setup/
│   └── main.ts
└── README.md
```

### 核心设计原则

参考 doc2slides-style.css 的设计哲学:

```css
/* 基础底色 + 非必要不调整原则 */

:root {
  --bg-primary: #ffffff;
  --text-primary: #2c3e50;
  --accent-color: #42b983;
  --code-bg: #f6f8fa;
}

.slidev-layout {
  font-size: 20px;  /* 基础字体 - 严格固定 */
  padding: 30px 40px;
}

/* 代码块 - 支持滚动 */
pre {
  max-height: 80vh;
  overflow-y: auto;
  overflow-x: hidden;
  font-size: 0.8em;  /* 16px */
}
```

### 4 个预设主题

#### 1. midnight (深色专业)
```css
:root {
  --bg-primary: #1a1a2e;
  --bg-secondary: #16213e;
  --text-primary: #eee;
  --accent-color: #0f3460;
  --highlight: #e94560;
}
```

#### 2. warm (暖色温馨)
```css
:root {
  --bg-primary: #fff8f0;
  --bg-secondary: #ffe4d6;
  --text-primary: #5d4037;
  --accent-color: #ff6f00;
  --highlight: #ff8a65;
}
```

#### 3. focus (极简聚焦)
```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f5;
  --text-primary: #212121;
  --accent-color: #2196f3;
  --highlight: #64b5f6;
}
```

#### 4. vibrant (活力多彩)
```css
:root {
  --bg-primary: #f3e5f5;
  --bg-secondary: #e1bee7;
  --text-primary: #4a148c;
  --accent-color: #7b1fa2;
  --highlight: #ab47bc;
}
```

## CLI 命令规范

### 基础命令

```bash
# 开发模式 (实时预览)
doc2slides dev slides.md --theme midnight --port 3030

# 导出 HTML
doc2slides export slides.md --format html --theme warm

# 导出 PDF
doc2slides export slides.md --format pdf --theme focus

# 导出 PPTX
doc2slides export slides.md --format pptx --theme vibrant

# 导出 PNG 序列
doc2slides export slides.md --format png --theme midnight
```

### 高级选项

```bash
# 自定义主题路径
doc2slides dev slides.md --theme ./my-theme.css

# 批量转换
doc2slides batch *.md --format pdf --output ./output

# 主题预览
doc2slides themes list
doc2slides themes preview midnight
```

## Claude Skill 输出规范

### 1. 分段输出策略

**问题**: 长文档一次性生成易导致失败或超时

**解决方案**: 分段生成 + Write 工具

```markdown
# doc2slides Skill 生成策略

## Step 1: 生成大纲
首先分析文档,生成幻灯片大纲,并写入 slides-outline.md

## Step 2: 逐段生成内容
根据大纲,每次生成 5-10 页幻灯片:
- Write slides-part1.md (封面 + 前言 + 第1章)
- Write slides-part2.md (第2-3章)
- Write slides-part3.md (第4-5章)
- ...

## Step 3: 合并文件
使用 bash 命令合并所有分段:
cat slides-part*.md > slides.md

## Step 4: 验证和优化
检查最终 slides.md 格式是否符合 Slidev 规范
```

### 2. 输出格式检查清单

**Claude 生成后必须自检**:

```markdown
✅ 检查项:
- [ ] Frontmatter 格式正确 (YAML)
- [ ] 每页用 `---` 分隔
- [ ] Layout 类型拼写正确
- [ ] 代码块有语言标识
- [ ] 图片路径存在或使用占位符
- [ ] 没有超长单行代码 (>100 字符)
- [ ] 标题层级合理 (h1 → h2 → h3)
```

### 3. 错误处理

**Claude 应提示用户**:

```markdown
⚠️ 警告示例:

"检测到代码块过长 (80+ 行),已自动添加滚动支持。
建议手动检查是否需要拆分为多页。"

"图片路径 '/images/demo.png' 不存在,已使用占位符。
请手动替换为实际图片路径。"

"检测到复杂表格,可能需要调整布局。
建议使用 layout: two-cols 或自定义 CSS。"
```

## 与现有 doc2slides skill 的集成

### 修改点

#### 1. 更新输出格式
- ❌ 旧: 自定义 `:::slide` 语法
- ✅ 新: Slidev 原生 Markdown + frontmatter

#### 2. 移除自定义渲染逻辑
- ❌ 旧: 内置 reveal.js + 自定义 CSS
- ✅ 新: 依赖 Slidev CLI

#### 3. 保留核心功能
- ✅ 文档分析和内容提取
- ✅ 结构化和分段逻辑
- ✅ 布局约束和样式规范
- ✅ 增量生成和状态恢复

### 迁移路径

```markdown
Phase 1: 双格式支持 (过渡期)
- 同时支持旧格式 (:::slide) 和新格式 (Slidev)
- 用户可选择输出格式

Phase 2: 逐步迁移
- 新项目默认使用 Slidev 格式
- 提供转换工具: old-format → Slidev

Phase 3: 完全切换
- 移除旧格式支持
- 全面使用 Slidev 生态
```

## 开发任务清单

### P0: 核心功能 (必需)
- [ ] 安装和配置 Slidev
- [ ] 创建 4 个基础主题包
- [ ] 包装 CLI 命令 (dev, export)
- [ ] 更新 doc2slides skill 输出格式
- [ ] 编写用户文档

### P1: 增强功能 (重要)
- [ ] 主题切换器 (Web UI)
- [ ] 批量转换工具
- [ ] 模板库 (常见场景)
- [ ] VS Code 插件集成

### P2: 优化体验 (可选)
- [ ] 主题预览页面
- [ ] 在线演示
- [ ] 社区主题市场
- [ ] AI 辅助布局优化

## 技术债务和风险

### 潜在问题

1. **Slidev 依赖重**: Node.js + Vue 3 生态
   - 缓解: 提供 Docker 镜像
   - 备选: Marp 作为轻量级方案

2. **学习曲线**: 用户需要了解基本 Slidev 语法
   - 缓解: 详细文档 + 模板库
   - 工具: 自动格式检查和修复

3. **版本兼容**: Slidev 更新可能破坏主题
   - 缓解: 锁定 Slidev 版本
   - 测试: CI 自动化测试

### 性能考虑

- **首次启动慢**: Vite 需要预构建依赖
  - 解决: 预构建缓存
- **大型项目**: 100+ 页幻灯片性能下降
  - 解决: 分段构建 + 懒加载

## 总结

### 为什么选择 Slidev?

1. ✅ **生态成熟**: 30K stars,活跃维护
2. ✅ **架构先进**: 现代前端技术栈
3. ✅ **功能完整**: CLI + 主题 + 导出
4. ✅ **易于扩展**: 清晰的插件系统
5. ✅ **符合目标**: 完美支持内容与渲染分离

### 实施成本

- **技术风险**: ⭐⭐ (低,成熟方案)
- **开发成本**: ⭐⭐ (中,主要是主题开发)
- **维护成本**: ⭐ (低,依赖 Slidev 生态)

### 预期收益

- ✅ 避免重复造轮子
- ✅ 强大的主题系统
- ✅ 完善的导出能力
- ✅ 活跃的社区支持
- ✅ 现代化开发体验
