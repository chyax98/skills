# chyax98 的 Claude Skills 收藏

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Skills](https://img.shields.io/badge/custom_skills-1-orange)

**基于官方 Anthropic Skills 的个人定制技能库**

[安装方法](#-安装方法) • [自定义 Skills](#-自定义-skills) • [官方 Skills](#-官方-skills)

</div>

---

## 📖 关于此仓库

这是 [Anthropic Skills](https://github.com/anthropics/skills) 的个人 fork，包含：
- ✅ **所有官方示例 Skills** - Anthropic 提供的完整技能库
- ✅ **自定义 Skills** - 我个人开发的专业技能
- ✅ **插件市场配置** - 可通过 Claude Code 直接安装

---

## 🚀 安装方法

### 通过 Claude Code 插件市场

```bash
# 1. 添加我的插件市场
/plugin marketplace add chyax98/skills

# 2. 安装我的自定义 Skills
/plugin install learning-skills@chyax98-skills

# 3. 或安装官方 Skills
/plugin install example-skills@chyax98-skills
/plugin install document-skills@chyax98-skills
```

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/chyax98/skills.git

# 复制特定 skill 到 Claude skills 目录
cp -r skills/learning-to-html-presentation ~/.claude/skills/
```

---

## ✨ 自定义 Skills

### learning-to-html-presentation

**将学习内容转换为精美的 HTML 演示文稿**

<div align="center">
  <img src="https://img.shields.io/badge/Type-Learning%20%26%20Presentation-blueviolet" />
  <img src="https://img.shields.io/badge/Output-HTML-orange" />
  <img src="https://img.shields.io/badge/Themes-4-brightgreen" />
</div>

#### 核心特性

- 🧠 **智能分析** - 自动识别内容结构，提取核心论点
- 🎨 **4 种主题** - 专业商务/活泼创意/科技未来/温馨教育
- ⚡ **流畅交互** - 键盘/鼠标/触摸导航，60fps 动画
- 📱 **全平台适配** - 桌面/平板/手机完美响应
- 📄 **单文件输出** - 所有资源内嵌，双击即用
- 📊 **质量评分** - 四维度自动评估（≥85% 合格）

#### 快速使用

```
使用 learning-to-html-presentation skill 将这个 React 教程转为演示文稿:

什么是 Hooks?
Hooks 是 React 16.8 引入的新特性...

[你的学习内容]
```

**输出**: 完整的 HTML 演示文稿，包含：
- ✅ 精美的幻灯片设计
- ✅ 流畅的过渡动画
- ✅ 完整的导航功能
- ✅ 质量评分报告

#### 方法论

融合两大提示词工程方法论:

1. **DEPTH 方法论**
   - Define Multiple Perspectives (多元专家视角)
   - Establish Success Metrics (明确成功指标)
   - Provide Context Layers (充分背景信息)
   - Task Breakdown (系统化任务拆解)
   - Human Feedback Loop (自我评估迭代)

2. **思想印记解读器**
   - 思想考古学 - 从口述中提取清晰结构
   - 头条提炼 - 生成精准核心标题
   - 建筑规划 - 构建逻辑化内容组织

#### 幻灯片模板

- 📄 **封面** - 标题页面，渐入动画
- 📋 **目录** - 编号章节列表
- 📝 **内容** - 标题 + 要点列表
- 📊 **双列** - 对比展示布局
- 💻 **代码** - 语法高亮示例
- ⚖️ **对比** - ❌ 不推荐 vs ✅ 推荐
- 📌 **总结** - 编号核心要点

#### 文档

- [完整文档](./learning-to-html-presentation/README.md)
- [快速上手](./learning-to-html-presentation/QUICKSTART.md)
- [示例演示](./learning-to-html-presentation/examples/example-presentation.html)

---

## 🎓 官方 Skills

此仓库包含所有 Anthropic 官方示例 Skills：

### 创意与设计
- **algorithmic-art** - 使用 p5.js 创建生成艺术
- **canvas-design** - 设计精美的 PNG 和 PDF 视觉艺术
- **slack-gif-creator** - 创建适合 Slack 的动画 GIF

### 开发与技术
- **artifacts-builder** - 使用 React、Tailwind CSS 构建复杂 HTML artifacts
- **mcp-server** - 创建高质量 MCP 服务器指南
- **webapp-testing** - 使用 Playwright 测试本地 Web 应用

### 企业与沟通
- **brand-guidelines** - 应用 Anthropic 品牌颜色和排版
- **internal-comms** - 撰写内部沟通文档
- **theme-factory** - 为 artifacts 应用专业主题

### Meta Skills
- **skill-creator** - 创建有效技能的指南
- **template-skill** - 新技能的基础模板

### 文档处理
- **xlsx** - Excel 电子表格处理
- **docx** - Word 文档处理
- **pptx** - PowerPoint 演示文稿处理
- **pdf** - PDF 文档处理

详细信息请参见官方文档：[Anthropic Skills Repository](https://github.com/anthropics/skills)

---

## 🛠️ 为此仓库贡献

### 添加你的自定义 Skill

1. **创建 Skill 文件夹**

```bash
cd ~/dev/skills
mkdir my-new-skill
cd my-new-skill
```

2. **创建 SKILL.md**

```markdown
---
name: my-new-skill
description: 描述这个 skill 的功能和使用场景
---

# My New Skill

[Claude 的指令...]
```

3. **更新 marketplace.json**

编辑 `.claude-plugin/marketplace.json`，在 `learning-skills` 插件中添加:

```json
{
  "name": "learning-skills",
  "skills": [
    "./learning-to-html-presentation",
    "./my-new-skill"
  ]
}
```

4. **测试并提交**

```bash
# 本地测试
/plugin marketplace add file:///Users/Apple/dev/skills
/plugin install learning-skills

# 提交到 GitHub
git add .
git commit -m "feat: add my-new-skill"
git push origin main
```

---

## 📚 学习资源

### 官方文档
- [什么是 Skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [在 Claude 中使用 Skills](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [创建自定义 Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Agent Skills 工程博客](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

### 开发资源
- [Agent Skills 规范](./agent_skills_spec.md)
- [官方 Skills 仓库](https://github.com/anthropics/skills)

---

## 🔄 更新与维护

### 同步官方更新

```bash
# 添加官方仓库为 upstream
cd ~/dev/skills
git remote add upstream https://github.com/anthropics/skills.git

# 拉取官方更新
git fetch upstream
git merge upstream/main

# 解决冲突（如果有）
# ...

# 推送到你的 fork
git push origin main
```

### 更新自定义 Skills

```bash
# 修改 skill
# ...

# 提交更新
git add .
git commit -m "feat: update learning-to-html-presentation

- 添加新的幻灯片模板
- 改进动画性能
- 修复移动端布局问题
"

# 更新版本号
# 编辑 .claude-plugin/marketplace.json: "version": "1.1.0"

# 创建版本标签
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main --tags
```

---

## 📜 许可证

- **官方 Skills**: 遵循 [Anthropic Skills 许可证](./THIRD_PARTY_NOTICES.md)
- **自定义 Skills**: Apache License 2.0
- 详见各 skill 目录中的 `LICENSE.txt` 文件

---

## 🙏 致谢

- 基于 [Anthropic Skills Framework](https://github.com/anthropics/skills)
- 灵感来源于 DEPTH 方法论和思想考古学原理
- 感谢 Claude Code 团队

---

## 📞 联系方式

- **Issues**: [GitHub Issues](https://github.com/chyax98/skills/issues)
- **Discussions**: [GitHub Discussions](https://github.com/chyax98/skills/discussions)
- **更新通知**: Watch 此仓库获取最新动态

---

<div align="center">

**为 Claude Code 社区制作 ❤️**

[⭐ Star 此仓库](https://github.com/chyax98/skills) 如果觉得有用！

</div>
