# Learning to HTML Presentation - 文档中心

这个目录包含 skill 的开发文档和设计参考。

## 📚 文档索引

### 核心文档 (主目录)

1. **[SKILL.md](../SKILL.md)** ⭐ 核心文件
   - Skill 主文件,包含完整的方法论和指令
   - DEPTH 方法论集成
   - 六阶段工作流程
   - 费曼学习法增强模式

2. **[README.md](../README.md)** 📖 使用手册
   - Skill 特性介绍
   - 安装方法
   - 使用示例
   - 幻灯片类型说明
   - 质量标准

3. **[INSTALLATION.md](../INSTALLATION.md)** 🔧 安装指南
   - Claude Code 安装步骤
   - Claude.ai 安装方法
   - API 使用说明
   - 故障排查

4. **[QUICKSTART.md](../QUICKSTART.md)** ⚡ 快速开始
   - 5 分钟入门
   - 基础示例
   - 常见场景

5. **[LICENSE.txt](../LICENSE.txt)** 📄 许可证
   - Apache 2.0 许可证

### 参考文档 (references/)

1. **[feynman-technique.md](../references/feynman-technique.md)** 🎓 学习方法
   - 双向费曼学习法完整指南
   - 五阶段实施流程
   - AI 辅助反馈循环
   - 与演示文稿生成的整合

### 开发文档 (本目录)

1. **[DESIGN_PRINCIPLES.md](./DESIGN_PRINCIPLES.md)** 🎨 设计原则
   - DEPTH 方法论详解
   - 思想印记解读器哲学
   - 原始提示词方案
   - 设计决策参考

2. **[github-skills-deployment-checklist.md](./github-skills-deployment-checklist.md)** 🚀 部署清单
   - GitHub Skills 部署步骤
   - Marketplace 配置
   - 发布流程

## 📂 完整文件结构

```
learning-to-html-presentation/
├── SKILL.md                          # ⭐ Skill 核心文件
├── README.md                         # 📖 使用手册
├── INSTALLATION.md                   # 🔧 安装指南
├── QUICKSTART.md                     # ⚡ 快速开始
├── LICENSE.txt                       # 📄 许可证
│
├── templates/                        # 幻灯片模板
│   ├── cover.html                   # 封面模板
│   ├── toc.html                     # 目录模板
│   ├── content.html                 # 内容模板
│   ├── two-column.html              # 双列模板
│   ├── code.html                    # 代码模板
│   ├── comparison.html              # 对比模板
│   └── summary.html                 # 总结模板
│
├── scripts/                          # JavaScript 脚本
│   └── presentation.js              # 导航和交互逻辑
│
├── assets/                           # 资源文件
│   ├── styles/                      # CSS 样式
│   │   └── base.css                 # 基础样式系统
│   └── examples/                    # 示例文件
│       └── example-presentation.html # 完整示例
│
├── references/                       # 参考文档
│   └── feynman-technique.md         # 费曼学习法指南
│
└── docs/                             # 开发文档 (本目录)
    ├── README.md                    # 文档索引 (本文件)
    ├── DESIGN_PRINCIPLES.md         # 设计原则和方法论
    └── github-skills-deployment-checklist.md # 部署清单
```

## 🎯 文档使用场景

### 👤 普通用户

**推荐阅读顺序**:
1. [README.md](../README.md) - 了解 Skill 功能
2. [INSTALLATION.md](../INSTALLATION.md) - 安装 Skill
3. [QUICKSTART.md](../QUICKSTART.md) - 快速上手
4. [feynman-technique.md](../references/feynman-technique.md) - 深度学习模式(可选)

### 🔧 Skill 开发者

**推荐阅读顺序**:
1. [DESIGN_PRINCIPLES.md](./DESIGN_PRINCIPLES.md) - 理解设计理念
2. [SKILL.md](../SKILL.md) - 研究 Skill 实现
3. [github-skills-deployment-checklist.md](./github-skills-deployment-checklist.md) - 部署到 GitHub

### 📚 贡献者

**推荐阅读**:
- [SKILL.md](../SKILL.md) - 核心逻辑
- [DESIGN_PRINCIPLES.md](./DESIGN_PRINCIPLES.md) - 方法论基础
- [README.md](../README.md) - 用户文档规范

## 💡 快速链接

- [官方 Skills 文档](https://docs.anthropic.com/claude/docs/skills)
- [Agent Skills 博客](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Skills 仓库](https://github.com/anthropics/skills)
- [Claude Code 文档](https://docs.claude.com/claude-code)

## 🔄 文档更新

**最后更新**: 2025-10-21
**版本**: 1.0.0
**维护者**: chyax98

如有文档问题或改进建议,请提交 Issue 到 GitHub 仓库。
