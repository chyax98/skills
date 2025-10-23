# Markdown to Slides 工具调研报告

## 调研目标

为 doc2slides 项目寻找可复用或改造的开源 Markdown 转 PPT 工具,避免重复造轮子。

调研重点:
1. 是否支持 CLI 渲染
2. 主题系统的可定制性
3. 导出格式支持
4. 架构是否支持内容与渲染分离
5. 活跃度和社区支持

---

## 主流工具对比

### 1. Slidev ⭐⭐⭐⭐⭐

**官网**: https://sli.dev/
**GitHub**: https://github.com/slidevjs/slidev (30K+ stars)
**技术栈**: Vue 3 + Vite + UnoCSS

#### 核心特性

**✅ 优势**:
- **现代化架构**: 基于 Vite + Vue 3,开发体验极佳
- **强大的主题系统**:
  - 官方主题: default, seriph, apple-basic, bricks, shibainu 等
  - 社区主题丰富 (Theme Gallery)
  - 支持通过 npm 分享主题
  - CSS + Vue 组件自定义
- **CLI 支持完善**:
  - `slidev` - 开发服务器
  - `slidev export` - 导出 PDF/PNG/PPTX
  - `slidev build` - 构建静态 SPA
- **丰富的功能**:
  - Vue 组件支持
  - UnoCSS 实时样式
  - Monaco Editor 代码编辑
  - Shiki 语法高亮
  - Mermaid/PlantUML 图表
  - LaTeX 数学公式
  - 录屏和摄像头支持
- **导出格式**: HTML (SPA), PDF, PNG, PPTX
- **Markdown 语法**:
  ```markdown
  ---
  theme: seriph
  title: My Presentation
  ---

  # Slide 1

  Content here

  ---
  layout: center
  background: /bg.png
  ---

  # Slide 2
  ```

**❌ 劣势**:
- **重量级**: 完整的 Vue 3 应用,打包体积较大
- **学习曲线**: 需要了解 Vue 生态才能深度定制
- **依赖复杂**: Node.js 生态依赖较多

#### 架构分析

```
Markdown (slides.md)
    ↓ (解析)
Slidev Parser → AST
    ↓ (渲染)
Vue Components + UnoCSS
    ↓ (导出)
HTML / PDF / PPTX
```

**关键设计**:
- **Frontmatter**: YAML 配置每页幻灯片
- **Layouts**: 预定义布局组件
- **Themes**: CSS + Vue 组件打包为 npm 包
- **Plugins**: Vite 插件系统扩展

---

### 2. Marp ⭐⭐⭐⭐

**官网**: https://marp.app/
**GitHub**: https://github.com/marp-team/marp (7K+ stars)
**核心**: https://github.com/marp-team/marp-core (6K+ stars)

#### 核心特性

**✅ 优势**:
- **轻量级**: 基于 Marpit 框架,输出最小化 HTML/CSS
- **CLI 工具强大** (marp-cli):
  - 导出 HTML, PDF, PPTX
  - Watch 模式
  - 服务器模式
- **VS Code 集成完善**: 官方插件体验好
- **主题系统**:
  - 内置 3 个主题: default, gaia, uncover
  - CSS 自定义主题
  - 社区主题: Awesome Marp, Marp Community Themes
- **导出格式**: HTML, PDF, PPTX
- **Markdown 语法**:
  ```markdown
  ---
  marp: true
  theme: gaia
  paginate: true
  ---

  # Slide 1

  ---

  # Slide 2
  ```

**❌ 劣势**:
- **功能相对简单**: 不支持 Vue/React 组件
- **交互性弱**: 主要是静态内容
- **主题定制**: 仅限 CSS,没有组件化支持
- **社区规模**: 相比 Slidev 较小

#### 架构分析

```
Markdown (.md)
    ↓ (解析)
Marpit Parser → HTML + CSS
    ↓ (导出)
HTML / PDF / PPTX (via Puppeteer)
```

**关键设计**:
- **Marpit 框架**: 独立的 Markdown → HTML/CSS 转换器
- **Directives**: `<!-- directive: value -->` 配置
- **CSS Theming**: 纯 CSS 主题系统
- **Portable**: 输出纯 HTML/CSS,无框架依赖

---

### 3. reveal-md ⭐⭐⭐

**GitHub**: https://github.com/webpro/reveal-md (5K+ stars)
**基础**: reveal.js (68K+ stars)

#### 核心特性

**✅ 优势**:
- **基于 reveal.js**: 继承强大的演示功能
  - 2D/3D 幻灯片导航
  - PDF 导出
  - 演讲者备注
  - 丰富的过渡效果
- **CLI 工具**:
  - `reveal-md slides.md` - 开发服务器
  - `reveal-md slides.md --print slides.pdf` - 导出 PDF
- **主题丰富**: reveal.js 官方主题 (10+ 个)
- **Markdown 友好**: 完全基于 Markdown
- **导出格式**: HTML, PDF

**❌ 劣势**:
- **没有 PPTX 导出**: 只能导出 HTML 和 PDF
- **主题定制**: 需要了解 reveal.js 的 CSS 结构
- **维护状态**: 更新频率较低
- **功能限制**: 很多 reveal.js 高级功能需要直接写 HTML

#### 架构分析

```
Markdown (.md)
    ↓ (解析)
reveal-md Parser → reveal.js HTML
    ↓ (渲染/导出)
Browser (live server) / PDF (print-pdf)
```

---

### 4. mdx-deck ⭐⭐⭐

**GitHub**: https://github.com/jxnblk/mdx-deck (11K+ stars)
**技术栈**: React + MDX

#### 核心特性

**✅ 优势**:
- **React 组件支持**: 可以在幻灯片中使用任何 React 组件
- **MDX 语法**: Markdown + JSX
  ```mdx
  import { Box } from 'theme-ui'

  # Slide 1

  <Box color="tomato">Hello</Box>

  ---

  # Slide 2
  ```
- **主题系统**: 基于 Theme UI
- **导出**: HTML, PDF

**❌ 劣势**:
- **维护停滞**: 最后更新 2021 年
- **React 依赖**: 必须了解 React 生态
- **没有 PPTX 导出**
- **CLI 功能有限**

---

## 对比总结表

| 特性 | Slidev | Marp | reveal-md | mdx-deck |
|------|--------|------|-----------|----------|
| **活跃度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ |
| **CLI 支持** | ✅ 完善 | ✅ 完善 | ✅ 基础 | ⚠️ 有限 |
| **主题系统** | ⭐⭐⭐⭐⭐ (npm + CSS + Vue) | ⭐⭐⭐⭐ (CSS only) | ⭐⭐⭐ (reveal.js themes) | ⭐⭐⭐ (Theme UI) |
| **导出格式** | HTML, PDF, PNG, PPTX | HTML, PDF, PPTX | HTML, PDF | HTML, PDF |
| **学习曲线** | 中等 (Vue) | 简单 | 简单 | 中等 (React) |
| **轻量级** | ❌ 重 | ✅ 轻 | ⚠️ 中 | ❌ 重 |
| **组件化** | ✅ Vue | ❌ | ❌ | ✅ React |
| **代码高亮** | ⭐⭐⭐⭐⭐ Shiki | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **图表支持** | ✅ Mermaid, PlantUML | ✅ Mermaid | ⚠️ 有限 | ⚠️ 有限 |
| **数学公式** | ✅ KaTeX | ⚠️ 需插件 | ✅ MathJax | ⚠️ 需插件 |
| **文档质量** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **社区规模** | 大 | 中 | 小 | 小 (停滞) |

---

## 推荐方案分析

### 方案 A: 基于 Slidev 改造 ⭐⭐⭐⭐⭐

**适合场景**: 需要强大功能和现代化体验

**改造思路**:
1. **保留 Slidev 核心**: 使用 Slidev 的解析器和渲染引擎
2. **定制主题系统**: 创建 doc2slides 专用主题包
3. **简化 CLI**: 包装 Slidev CLI,提供更简单的接口
4. **协议设计**: Markdown + YAML frontmatter (已是 Slidev 原生格式)

**优势**:
- ✅ 完整的生态系统和活跃社区
- ✅ 强大的主题系统,易于扩展
- ✅ 支持所有主流导出格式
- ✅ 文档完善,开发体验好

**劣势**:
- ❌ 依赖较重,不够轻量
- ❌ 需要 Node.js 环境

**实施成本**: ⭐⭐ (低,主要是主题定制)

---

### 方案 B: 基于 Marp 改造 ⭐⭐⭐⭐

**适合场景**: 需要轻量级、纯 Markdown 方案

**改造思路**:
1. **使用 Marp Core**: 基于 Marpit 框架
2. **扩展主题**: 创建自定义 CSS 主题
3. **CLI 包装**: 基于 marp-cli 构建
4. **协议设计**: 标准 Markdown + Marp directives

**优势**:
- ✅ 轻量级,输出纯 HTML/CSS
- ✅ CLI 工具成熟
- ✅ 支持 PPTX 导出
- ✅ 学习曲线平缓

**劣势**:
- ❌ 功能相对简单
- ❌ 不支持组件化
- ❌ 交互性较弱

**实施成本**: ⭐ (极低,主要是主题开发)

---

### 方案 C: 基于 reveal-md 改造 ⭐⭐⭐

**适合场景**: 需要强大演示功能

**改造思路**:
1. **使用 reveal.js + reveal-md**
2. **自定义 reveal.js 主题**
3. **扩展 reveal-md 功能**

**优势**:
- ✅ reveal.js 生态强大
- ✅ 演示功能丰富

**劣势**:
- ❌ 没有 PPTX 导出
- ❌ 维护不够活跃
- ❌ 定制相对复杂

**实施成本**: ⭐⭐⭐ (中等)

---

### 方案 D: 从零构建 ⭐⭐

**不推荐**: 重复造轮子,成本高,收益低

---

## 最终推荐

### 🏆 推荐方案: Slidev + 自定义主题

**理由**:
1. **生态成熟**: 30K+ stars,活跃维护,文档完善
2. **架构先进**: Vue 3 + Vite,开发体验最佳
3. **功能完整**: 支持所有需求 (CLI, 主题, 导出格式)
4. **易于扩展**: 清晰的主题和插件系统
5. **符合需求**: 完美支持"内容生成 ↔ 渲染分离"架构

### 实施路线图

#### Phase 1: 协议设计 (基于 Slidev 格式)
```markdown
---
theme: doc2slides-midnight  # 自定义主题
layout: cover
---

# 标题幻灯片

---
layout: default
---

# 内容页

正文内容

---
layout: two-cols
---

# 左右分栏

::left::
左侧内容

::right::
右侧内容
```

#### Phase 2: 主题开发
- 创建 `@doc2slides/theme-midnight`
- 创建 `@doc2slides/theme-warm`
- 创建 `@doc2slides/theme-focus`
- 创建 `@doc2slides/theme-vibrant`

#### Phase 3: CLI 工具
```bash
# 基于 Slidev CLI 包装
doc2slides render slides.md --theme midnight --output slides.html
doc2slides export slides.md --format pdf --output slides.pdf
doc2slides preview slides.md --theme warm
```

#### Phase 4: Claude 集成
- Claude (doc2slides skill) 生成符合 Slidev 格式的 Markdown
- 用户使用 CLI 渲染,切换主题无需重新生成

---

## 备选方案: Marp

如果 Slidev 过于重量级,可以考虑 Marp:

**优势**:
- 更轻量,输出纯 HTML/CSS
- 学习成本更低
- 同样支持 CLI 和 PPTX 导出

**劣势**:
- 功能相对简单
- 主题系统仅限 CSS

**适用场景**:
- 纯文本+代码的技术分享
- 需要最小化依赖的环境
- 不需要复杂交互和组件

---

## 结论

✅ **推荐采用 Slidev 作为基础框架**

**核心优势**:
1. 无需重复造轮子,生态成熟
2. 主题系统强大且易于扩展
3. CLI 工具完善,支持所有导出格式
4. 架构设计完美契合"内容与渲染分离"理念
5. 活跃维护,社区支持好

**下一步**:
1. 创建 doc2slides 主题包规范
2. 开发 4-5 个预设主题
3. 包装 Slidev CLI 为 doc2slides CLI
4. 更新 doc2slides skill 以生成 Slidev 兼容格式
