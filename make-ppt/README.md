# Make-PPT

AI 驱动的专业 HTML 演示文稿生成器

## 概述

Make-PPT 是一个智能的演示文稿生成工具,能够:
- 📚 自动收集学习资料 (网页搜索、URL 提取、官方文档、本地文件)
- 📝 生成结构化、内容充实的 Markdown
- 🎨 渲染为美观的 HTML 交互式幻灯片
- ⚡ 一句话即可完成整个流程

## 快速开始

### 安装

```bash
npm install -g reveal-md
```

### 基础使用

```
使用 make-ppt 生成关于 [主题] 的 PPT
```

示例:
```
使用 make-ppt 生成关于 React Hooks 的 60 分钟 PPT
```

详见 [QUICKSTART.md](./QUICKSTART.md) 获取完整指南。

## 特性

### 智能资料收集

| 输入类型 | 处理方式 |
|---------|---------|
| 主题关键词 | SearXNG 搜索 top 3 |
| URL 链接 | Tavily 提取内容 |
| 官方文档 | Context7 查询 |
| 本地文件 | 直接读取 |

### 内容质量保证

- **内容密度**: 时长(分钟) × 0.8 = 幻灯片数量
- **深度要求**: 每个核心概念 ≥ 3 张幻灯片
- **结构完整**: 定义 + 解释 + 示例

### 渐进式展示

使用 reveal.js fragment 特性实现逐步展示,提升演讲效果。

## 目录结构

```
make-ppt/
├── SKILL.md          # 核心 AI 指令
├── README.md         # 项目说明
├── QUICKSTART.md     # 快速入门
├── LICENSE.txt       # Apache-2.0 许可证
├── templates/        # Markdown 模板
│   ├── basic.md      # 基础模板
│   └── technical.md  # 技术模板
├── examples/         # 示例文件
│   └── demo-feynman-learning.html
└── output/           # 生成结果
    ├── slides.md     # 生成的 Markdown
    └── html/         # 渲染的 HTML
        └── index.html
```

## 输出格式

生成的 HTML 幻灯片支持:
- ←/→ 或空格键导航
- Esc 查看全局视图
- F 全屏模式
- S 演讲者模式

## 主题选择

支持多种内置主题:
- `black` (默认)
- `white`
- `league`
- `sky`
- `beige`

## 技术栈

- **AI 引擎**: Claude (资料收集、内容生成)
- **渲染引擎**: reveal-md / reveal.js
- **格式**: Markdown → HTML

## 工作流程

```
用户请求 → 收集资料 → AI 生成 Markdown → reveal-md 渲染 → HTML 输出
```

## 许可证

Apache-2.0 - 详见 [LICENSE.txt](./LICENSE.txt)

## 相关项目

- [reveal.js](https://revealjs.com/) - HTML 演示文稿框架
- [reveal-md](https://github.com/webpro/reveal-md) - Markdown 转 reveal.js
