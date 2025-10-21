# Learning to HTML Presentation Skill

将学习内容转换为视觉精美、交互流畅的 HTML 演示文稿的 Claude Skill。

## 特性

### 🎯 核心能力

- **智能内容分析** - 自动识别思想板块边界,提取核心论点
- **结构化转换** - 将口语化表达转为精炼的幻灯片内容
- **视觉设计** - 4 种预置主题,专业配色系统
- **流畅交互** - 键盘/鼠标/触摸多种导航方式
- **单文件输出** - 所有资源内嵌,双击即用

### 🧠 方法论

融合两大提示词工程方法论:

1. **DEPTH 方法论**
   - Define Multiple Perspectives (多元视角专家)
   - Establish Success Metrics (明确成功指标)
   - Provide Context Layers (充分背景信息)
   - Task Breakdown (系统化任务拆解)
   - Human Feedback Loop (自我评估迭代)

2. **思想印记解读器**
   - 思想考古学 - 从杂乱口述中提取清晰结构
   - 头条提炼 - 为每个板块生成精准标题
   - 建筑规划 - 构建逻辑化的内容组织

## 使用方法

### 在 Claude Code 中使用

1. **安装 Skill**

```bash
# Skill 已安装在 ~/.claude/skills/learning-to-html-presentation
```

2. **调用 Skill**

```
请使用 learning-to-html-presentation skill 将这份 React 教程转为演示文稿:

[粘贴你的学习内容]
```

3. **自定义选项**

```
请生成一份科技未来风格的演示文稿,目标受众是初学者:

主题: TypeScript 类型系统
时长: 30 分钟
风格: 科技未来
```

### 在 Claude.ai 中使用

1. 在设置中启用 Skills
2. 上传此 skill 文件夹
3. 在对话中提及 skill 名称即可

### 通过 API 使用

参考 [Skills API 文档](https://docs.claude.com/en/api/skills-guide)

## 输入格式

支持多种学习内容格式:

- ✅ **纯文本** - 学习笔记、讲义
- ✅ **Markdown** - 结构化文档
- ✅ **口述文稿** - 讲座录音转录
- ✅ **技术文档** - README、教程
- ✅ **教学大纲** - 课程计划

## 输出内容

生成一个完整的 HTML 文件,包含:

1. **演示文稿本体** - 可在浏览器直接打开
2. **导航系统** - 支持键盘/鼠标/触摸
3. **进度指示** - 进度条和页码
4. **响应式布局** - 桌面/平板/手机适配

## 幻灯片类型

### 1. 封面幻灯片
- 标题 + 副标题
- 作者和日期
- 渐入动画

### 2. 目录幻灯片
- 章节编号列表
- 清晰的视觉层级

### 3. 内容幻灯片
- 标题 + 要点列表
- 最多 3-4 个核心信息
- 逐条渐入动画

### 4. 双列布局
- 对比展示
- 图文并茂
- 左右对称

### 5. 代码示例
- 语法高亮
- 代码说明
- 可复制格式

### 6. 对比幻灯片
- ❌ 不推荐 vs ✅ 推荐
- 红绿配色区分
- 直观对比

### 7. 总结幻灯片
- 核心要点回顾
- 编号卡片设计
- 视觉化总结

## 视觉主题

### 专业商务 (默认)
```css
--primary: #2563eb;  /* 蓝色 */
--accent: #f59e0b;   /* 橙色 */
```

### 活泼创意
```css
--primary: #ec4899;  /* 粉色 */
--accent: #10b981;   /* 绿色 */
```

### 科技未来
```css
--primary: #06b6d4;  /* 青色 */
--accent: #a855f7;   /* 紫色 */
```

### 温馨教育
```css
--primary: #059669;  /* 深绿 */
--accent: #eab308;   /* 黄色 */
```

## 导航操作

### 键盘快捷键
- `→` / `空格` / `PageDown` - 下一页
- `←` / `PageUp` - 上一页
- `Home` - 第一页
- `End` - 最后一页
- `F` / `F11` - 全屏切换

### 鼠标操作
- 点击左侧 1/3 - 上一页
- 点击右侧 1/3 - 下一页
- 点击底部按钮 - 导航控制

### 触摸操作
- 左滑 - 下一页
- 右滑 - 上一页

## 质量标准

生成的演示文稿会按四个维度自动评分:

### 内容质量 (30%)
- 知识完整性
- 表达清晰度
- 示例质量

### 视觉设计 (30%)
- 美学一致性
- 视觉层级
- 专业性

### 技术实现 (20%)
- 代码质量
- 性能表现
- 兼容性

### 用户体验 (20%)
- 导航体验
- 学习体验
- 可访问性

**总分 ≥ 85% 为合格, ≥ 95% 为优秀**

## 文件结构

```
learning-to-html-presentation/
├── SKILL.md              # Skill 主文件 (方法论和指令)
├── README.md             # 使用文档 (本文件)
├── LICENSE.txt           # 许可证
├── QUICKSTART.md         # 快速开始指南
├── templates/            # 幻灯片模板
│   ├── cover.html
│   ├── toc.html
│   ├── content.html
│   ├── two-column.html
│   ├── code.html
│   ├── comparison.html
│   └── summary.html
├── scripts/              # JavaScript 脚本
│   └── presentation.js  # 导航和交互逻辑
├── assets/               # 资源文件
│   ├── styles/          # CSS 样式
│   │   └── base.css     # 基础样式系统
│   └── examples/        # 示例文件
│       └── example-presentation.html
└── references/           # 参考文档
    └── feynman-technique.md  # 双向费曼学习法指南
```

## 最佳实践

### 内容准备

1. **清晰的结构** - 使用标题分隔章节
2. **精炼表达** - 每个要点 ≤ 30 字
3. **关键概念** - 突出核心知识点
4. **实际示例** - 包含代码或案例

### 设计建议

1. **极简主义** - 避免过度装饰
2. **一致性** - 统一的配色和字体
3. **留白** - 充足的空间让内容呼吸
4. **对比度** - 确保文字可读性

### 性能优化

1. **图片优化** - 使用 SVG 或压缩的 WebP
2. **代码压缩** - 移除注释和空白
3. **资源内嵌** - 减少外部请求
4. **渐进增强** - 核心功能优先

## 示例

查看 `assets/examples/example-presentation.html` 了解完整示例。

在浏览器中打开即可体验:
```bash
open assets/examples/example-presentation.html
```

## 技术栈

- **HTML5** - 语义化标签
- **CSS3** - Flexbox/Grid, 动画, 变量
- **JavaScript (ES6+)** - 类, 箭头函数, 事件监听
- **无外部依赖** - 纯原生实现

## 浏览器兼容性

- ✅ Chrome 90+
- ✅ Safari 14+
- ✅ Firefox 88+
- ✅ Edge 90+

## 许可证

Apache-2.0

## 反馈与贡献

如有问题或建议,欢迎通过 Claude 对话反馈。
