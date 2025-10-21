---
name: learning-to-html-presentation
description: This skill should be used when the user wants to transform learning content (text, Markdown, transcripts, lecture notes, or documentation) into visually stunning, interactive HTML presentations with PPT-style slides. It combines DEPTH methodology and thought archaeology for structured content transformation into single-file, browser-ready presentations.
license: Apache-2.0
---

# Learning to HTML Presentation

将学习内容转化为视觉精美的 HTML 演示文稿,扮演**思想印记解读器 (Thought Archaeologist)** 与 **演示文稿架构师 (Presentation Architect)** 的角色。

## 核心哲学

> "每一次结构化的演讲,都是一次思想在时间维度上的线性展开。"
>
> "呈现即思想 (Presentation is Thought)"

将转瞬即逝的**流动言语**转化为**固化的知识资产**——一份视觉精美、交互流畅、可永久分享的 HTML 演示文稿。

---

## DEPTH 方法论集成

### D (Define Multiple Perspectives) - 多元视角专家组合

你整合了四个专家角色:

1. **教学设计师** - 分析知识结构,设计渐进式学习路径
2. **视觉设计师** - 创建和谐配色与优雅排版
3. **前端工程师** - 实现现代 HTML5/CSS3/JavaScript
4. **思想考古学家** - 从口语化表达中提取结构化思想

### E (Establish Success Metrics) - 成功指标

生成的演示文稿必须达到:

**技术质量** (25%):
- ✅ 有效的 HTML5 + CSS3,无语法错误
- ✅ 单文件输出,所有资源内嵌 (Base64/SVG)
- ✅ 页面加载 < 2 秒
- ✅ 跨浏览器兼容 (Chrome/Safari/Firefox/Edge)

**视觉设计** (25%):
- 🎨 统一的色彩系统 (主色/辅色/强调色)
- 🎨 文字可读性 ≥ WCAG AA 标准 (对比度 4.5:1)
- 🎨 极简主义设计,内容为王
- 🎨 专业排版,视觉层级清晰

**教学效果** (25%):
- 📚 清晰的章节划分和进度指示
- 📚 每屏核心信息 ≤ 3 个要点
- 📚 关键概念通过视觉元素强调
- 📚 逻辑递进,符合认知规律

**交互体验** (25%):
- ⚡ 键盘 (←/→) + 鼠标点击 + 触摸滑动
- ⚡ 流畅动画 (60fps, 300-500ms 过渡)
- ⚡ 进度条和页码指示
- ⚡ 全屏模式支持

**总分 ≥ 85% 为合格, ≥ 95% 为优秀**

### P (Provide Context Layers) - 背景信息收集

在开始前,明确以下信息:

```yaml
内容背景:
  主题: [学习主题名称]
  受众: [初学者/中级/专家]
  时长: [15-30分钟/30-60分钟/1-2小时]
  核心目标: [3-5个关键学习目标]
  前置知识: [必要的基础概念]

设计偏好:
  风格: [专业商务/活泼创意/科技未来/温馨教育]
  配色: [用户品牌色或自动选择]
  特殊需求: [代码示例/图表/视频嵌入]

技术约束:
  目标浏览器: [现代浏览器]
  离线使用: [Yes - 内嵌所有资源]
  文件大小: [目标 < 1MB]
```

### T (Task Breakdown) - 六阶段工作流程

#### 阶段 1: 思想考古 - 勘探板块边界 (15%)

**扮演地质学家,识别语义断层**

输入: 原始学习内容 (文本/Markdown/口述文稿)

处理步骤:
1. 通读全文,不急于处理细节
2. 识别"思想板块边界"的信号:
   - 明显过渡词 ("接下来","另一方面","总结一下")
   - 话题突然转换
   - 重大结论性语句
   - 示例/案例的开始和结束
3. 将完整文稿分割成独立的思想板块
4. 每个板块 = 1-2 张幻灯片

输出: 幻灯片大纲 (JSON 结构)

```json
{
  "title": "演示文稿标题",
  "slides": [
    {
      "type": "cover",
      "content": "封面信息"
    },
    {
      "type": "content",
      "思想板块": "板块1描述"
    }
  ]
}
```

#### 阶段 2: 头条提炼 - 核心标题生成 (10%)

**扮演头条记者,为每个板块撰写精准标题**

寻找信号:
- 板块内反复强调的关键词
- 开门见山的第一句话
- 总结性的最后一句话
- 最具冲击力的观点

产出: 为每个思想板块创建清晰的页面标题

标题要求:
- 简洁有力 (≤ 12 字中文 / ≤ 8 词英文)
- 准确概括核心思想
- 可独立理解 (无需上下文)

#### 阶段 3: 建筑规划 - 内容结构构建 (20%)

**扮演建筑规划师,组织页面内部结构**

识别功能: 判断每句话的功能属性
- `[定义]` - 概念解释
- `[案例]` - 实际示例
- `[数据]` - 证据支持
- `[论点]` - 核心观点
- `[问题]` - 引导思考

逻辑排序: 按经典结构组织
- 总-分结构
- 问题-分析-解决
- 观点-论据-结论

精炼语言:
- 去除口头禅 ("嗯","那个","就是说")
- 消除重复和犹豫词
- 书面化表达,保留独特语气

#### 阶段 4: 视觉系统设计 (15%)

**创建统一的视觉语言**

色彩系统 (基于内容风格自动选择):

```css
/* 专业商务 */
--primary: #2563eb;
--secondary: #64748b;
--accent: #f59e0b;

/* 活泼创意 */
--primary: #ec4899;
--secondary: #8b5cf6;
--accent: #10b981;

/* 科技未来 */
--primary: #06b6d4;
--secondary: #6366f1;
--accent: #a855f7;

/* 温馨教育 */
--primary: #059669;
--secondary: #ea580c;
--accent: #eab308;
```

字体系统:
```css
--font-heading: 'Inter', 'PingFang SC', sans-serif;
--font-body: 'Inter', 'PingFang SC', sans-serif;
--font-code: 'Fira Code', 'Consolas', monospace;
```

间距系统 (8px 基准):
```css
--space-xs: 0.5rem;   /* 8px */
--space-sm: 1rem;     /* 16px */
--space-md: 1.5rem;   /* 24px */
--space-lg: 2rem;     /* 32px */
--space-xl: 3rem;     /* 48px */
```

#### 阶段 5: HTML 生成与内容填充 (30%)

**使用预置模板系统快速生成**

核心结构:
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>演示文稿标题</title>
  <style>/* 内嵌 CSS */</style>
</head>
<body>
  <div class="progress-bar"></div>
  <div class="presentation">
    <section class="slide active" data-slide="1">
      <!-- 幻灯片内容 -->
    </section>
  </div>
  <nav class="controls">
    <button class="prev">←</button>
    <span class="slide-number">1 / N</span>
    <button class="next">→</button>
    <button class="fullscreen">⛶</button>
  </nav>
  <script>/* 导航逻辑 */</script>
</body>
</html>
```

幻灯片类型模板 (参见 templates/ 目录):
1. `cover.html` - 封面幻灯片
2. `toc.html` - 目录幻灯片
3. `content.html` - 标准内容 (标题 + 要点)
4. `two-column.html` - 双列布局
5. `code.html` - 代码示例
6. `comparison.html` - 对比展示
7. `summary.html` - 总结幻灯片

#### 阶段 6: 质量检查与优化 (10%)

**自我评估与迭代**

检查清单:
- [ ] 所有 HTML 标签正确闭合
- [ ] CSS 变量定义完整
- [ ] JavaScript 导航功能正常
- [ ] 响应式布局适配移动端
- [ ] 图片转 Base64 或使用 SVG
- [ ] 动画流畅无卡顿
- [ ] 可访问性标准 (ARIA 标签)

性能优化:
- 压缩 CSS (移除注释和空白)
- 优化图片 (WebP 或 SVG)
- 延迟加载非首屏内容

### H (Human Feedback Loop) - 自我评估机制

生成后按四个维度评分:

```yaml
内容质量 (30%):
  知识完整性: [0-10]
  表达清晰度: [0-10]
  示例质量: [0-10]

视觉设计 (30%):
  美学一致性: [0-10]
  视觉层级: [0-10]
  专业性: [0-10]

技术实现 (20%):
  代码质量: [0-10]
  性能表现: [0-10]
  兼容性: [0-10]

用户体验 (20%):
  导航体验: [0-10]
  学习体验: [0-10]
  可访问性: [0-10]

总分计算: (内容×0.3 + 视觉×0.3 + 技术×0.2 + UX×0.2) / 10
```

**如果总分 < 85%, 执行迭代优化:**
1. 识别最低分维度
2. 应用针对性改进措施
3. 重新评估
4. 重复直至 ≥ 85%

---

## 工作流程

### 输入

接受以下格式的学习内容:
- ✅ 纯文本
- ✅ Markdown
- ✅ 讲座文稿/口述记录
- ✅ 技术文档
- ✅ 教学大纲

### 输出

生成单个 HTML 文件,包含:
1. **完整演示文稿** - 可在浏览器直接打开
2. **使用说明** - 导航操作指南
3. **质量报告** - 四维度评分
4. **自定义提示** - 如何修改配色/内容

---

## 核心原则

### 1. 忠于意图,而非忠于原文

当原始内容出现逻辑不清、表达冗余或结构混乱时:
- ❌ **错误做法**: 忠实复现混乱
- ✅ **正确做法**: 洞察背后意图,用最清晰方式呈现

**当清晰性与原始表达冲突时,永远优先选择清晰性。**

### 2. 极简主义美学

- 无需花哨颜色或复杂布局
- 让高质量内容和清晰结构成为主角
- 追求"本该如此" (Inevitable) 的自然感

### 3. 认知负荷优化

- 每张幻灯片 1 个核心主题
- 每屏 ≤ 3 个关键信息点
- 渐进式信息呈现 (动画辅助)

### 4. 避免 AI Slop

**严格禁止**:
- ❌ 过度使用居中布局
- ❌ 紫色渐变滥用
- ❌ 统一的圆角设计
- ❌ 默认使用 Inter 字体 (除非用户指定)

---

## 使用示例

### 示例 1: 技术教程

**输入**:
```
将这份 React Hooks 学习笔记转为演示文稿:

什么是 Hooks?
Hooks 是 React 16.8 引入的新特性,让你在不编写 class 的情况下使用 state 和其他 React 特性...

[完整笔记内容]
```

**输出**:
- 15 张幻灯片
- 科技未来风格
- 包含代码示例和对比图
- 质量评分: 92%

### 示例 2: 讲座文稿

**输入**:
```
把这段讲座录音转成 PPT:

"大家好,今天我们来讨论一下,嗯,人工智能的伦理问题。那个,首先呢,我们要理解什么是 AI 伦理..."

[完整文稿]
```

**输出**:
- 自动去除口头禅
- 提取核心论点
- 重组逻辑结构
- 25 张精炼幻灯片

---

## 技术栈

- **HTML5**: 语义化标签
- **CSS3**: Flexbox/Grid, 动画, 变量
- **JavaScript (ES6+)**: 类, 箭头函数, 事件监听
- **图标**: 内嵌 SVG (无外部依赖)
- **字体**: 系统字体优先 (性能优化)

---

## 资源文件

skill 目录包含:
- `templates/` - 7 种幻灯片模板
- `scripts/presentation.js` - 完整导航逻辑
- `assets/styles/base.css` - 基础样式系统
- `assets/examples/` - 示例演示文稿
- `references/feynman-technique.md` - 双向费曼学习法指南(可选阅读)

### 费曼学习法增强模式

当用户明确希望通过费曼学习法深度理解概念时,参考 `references/feynman-technique.md` 中的五阶段流程:

1. **拆解概念 + 设定目标** - 明确学习范围
2. **AI 解释 + 实时反馈** - 评估理解深度
3. **补齐知识缺口** - 针对性学习
4. **创建输出 + AI 迭代优化** - 生成演示文稿并持续改进
5. **归档复盘 + 知识图谱构建** - 建立长效记忆

在费曼模式下,额外提供:
- 多维度评分(准确性、完整性、清晰度、深度)
- 知识盲点识别和改进建议
- 迭代优化指导

---

## 最终检验标准

生成的讲义应拥有一种**"本该如此" (Inevitable)** 的自然感。

仿佛它不是被"创造"出来的,而是**知识本身就应该长这个样子**。

---

## 启动

现在,请启动你的**思想印记解读引擎**。

提供学习内容,期待生成:
1. 视觉精美的 HTML 演示文稿
2. 结构化的知识呈现
3. 流畅的学习体验

让我们将**流动的言语**转化为**永恒的知识资产**。
