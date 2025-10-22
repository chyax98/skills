# LeetCode Narrative Learning

> 将算法题转化为沉浸式叙事学习体验

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE.txt)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Skill](https://img.shields.io/badge/skill-Claude%20Code-purple.svg)](https://docs.anthropic.com/claude/docs/skills)

---

## ✨ 特性

- 📖 **叙事化讲解**: 用故事化语言构建知识,而非机械堆砌
- 💡 **思维演进**: 从暴力法到优化解,展示完整的思考路径
- 🐍 **Python 实现**: 详细注释的完整代码
- 🔗 **举一反三**: 精选 5 道相关题目,构建知识网络
- 📚 **参考资料**: 书籍/文章/视频等拓展学习资源
- 🧠 **心智模型**: ASCII Art 可视化思维框架
- 🎨 **优雅呈现**: 古典人文风格的 HTML 幻灯片

---

## 🚀 快速开始

### 安装

1. 克隆仓库到 Claude Code Skills 目录:

```bash
cd ~/.claude/skills  # 或你的 Claude Code skills 目录
git clone <repository-url> leetcode-narrative-learning
```

2. 验证安装:

```bash
ls leetcode-narrative-learning/SKILL.md
```

### 使用

在 Claude Code 中,提供完整的 LeetCode 题目描述:

```
讲讲这道题:

[LeetCode 1] Two Sum

给定一个整数数组 nums 和一个整数目标值 target,
请你在该数组中找出和为目标值 target 的那两个整数,
并返回它们的数组下标。

你可以假设每种输入只会对应一个答案。但是,数组中同一个元素不能使用两遍。

你可以按任意顺序返回答案。

示例 1:
输入: nums = [2,7,11,15], target = 9
输出: [0,1]
解释: 因为 nums[0] + nums[1] == 9,返回 [0, 1]。

...
```

Claude 将:
1. 分析题目的核心思想
2. 设计叙事化的学习路径
3. 生成优雅的 HTML 幻灯片
4. 输出文件到当前目录

---

## 📖 幻灯片结构

生成的 HTML 幻灯片包含 7-10 页:

### 第 1 页: 封面
- 题目名称
- 难度标签
- 一句话本质描述

### 第 2 页: 问题的故事
- 用故事化语言重新描述问题
- 阐明问题的实际意义
- 提出核心问题

### 第 3 页: 思维起点 - 暴力法
- 最直观的思路
- 暴力解法的代码实现
- 复杂度分析
- "瓶颈在哪里?"

### 第 4 页: 核心洞察
- 思想的转折点
- 用比喻或故事阐明关键 insight
- 思维模型的可视化

### 第 5 页: 优化解法
- 完整代码实现 (Python)
- 逐行注释讲解
- 复杂度分析

### 第 6 页: 举一反三
- 核心思想的抽象总结
- 5 道精选相关题目 (难度递进)

### 第 7 页: 理论基础与拓展
- 相关数据结构/算法原理
- 参考资料 (书籍/文章/视频)

### 第 8 页: 心智模型 (ASCII Art)
- 通用的解题框架
- 可视化思维模型

### 第 9 页: 总结与启发
- 核心思想回顾
- 关键 takeaway
- 下一步学习建议

---

## 🎨 视觉风格

### 字体
- 主字体: Noto Serif SC (古典宋体)
- 代码字体: JetBrains Mono

### 色彩
- 背景: 深色调 (#1a1a1a)
- 主文字: 暖色调 (#e8d5b7)
- 强调: 琥珀色 (#ffb86c)
- 代码: Dracula 主题

### 特点
- 舒适的行间距 (1.8-2.0)
- 充足的留白
- 知识沉淀感
- 人文气息

---

## 🛠️ 技术细节

### 目录结构

```
leetcode-narrative-learning/
├── SKILL.md                              # Skill 核心指令
├── README.md                             # 本文档
├── LICENSE.txt                           # Apache 2.0 许可证
├── scripts/
│   └── generate_learning_slides.py       # HTML 生成脚本
├── references/
│   ├── algorithm_patterns.md             # 算法模式库
│   └── thinking_frameworks.md            # 思维框架库
└── assets/
    ├── templates/
    │   └── narrative-slide-template.html # HTML 模板
    ├── css/
    │   └── narrative-learning.css        # 样式文件
    └── js/
        └── (reveal.js 从 CDN 加载)
```

### 依赖

- **Python**: 3.8+ (使用标准库,无外部依赖)
- **浏览器**: 现代浏览器 (Chrome/Firefox/Safari/Edge)
- **网络**: 首次加载需要网络 (加载 reveal.js 和字体)

### 输出

- 单文件 HTML (包含所有样式和脚本引用)
- 文件名: `{题目名称}_narrative_learning.html`
- 位置: 当前工作目录

---

## 📚 使用示例

### 示例 1: Two Sum

**输入**:
```
讲讲 Two Sum 这道题:

给定一个整数数组 nums 和一个整数目标值 target...
```

**输出**:
```
✅ 已生成叙事式学习幻灯片: two_sum_narrative_learning.html

幻灯片包含:
  📖 问题的故事化阐述
  💡 暴力法 → 哈希表的思维演进
  🐍 Python 完整实现 + 详细注释
  🔗 5 道相关题目推荐
  📚 精选参考资料
  🧠 空间换时间思维模型 (ASCII Art)
  ✨ 核心 takeaway 总结

用浏览器打开即可开始探索! 🚀
```

### 示例 2: 二叉树最大深度

**输入**:
```
深入学习这道题:

[LeetCode 104] Maximum Depth of Binary Tree

给定一个二叉树,找出其最大深度...
```

**输出**:
```
✅ 已生成: maximum_depth_of_binary_tree_narrative_learning.html

核心思想: 递归思维 + 分治策略
相关题目: 5 道树的递归问题
心智模型: 递归三要素框架
```

---

## 🎓 学习建议

### 最佳实践

1. **提供完整题目**: 包括题目描述、示例、约束条件
2. **安静环境**: 全身心投入学习
3. **做笔记**: 记录关键 insight 和思考过程
4. **举一反三**: 尝试相关题目巩固理解
5. **查阅参考资料**: 深化理论基础

### 学习路径

```
1. 阅读生成的 HTML 幻灯片
   ↓
2. 理解核心思想和思维演进
   ↓
3. 自己实现代码 (不看答案)
   ↓
4. 对照讲解,找出差距
   ↓
5. 尝试相关题目 (举一反三)
   ↓
6. 查阅参考资料,深化理解
   ↓
7. 总结心智模型,形成框架
```

---

## 🤝 贡献

欢迎贡献!

### 贡献方式

1. **算法模式库**: 补充 `references/algorithm_patterns.md`
2. **思维框架**: 添加新的框架到 `references/thinking_frameworks.md`
3. **样式改进**: 优化 CSS 视觉效果
4. **功能增强**: 改进生成脚本

### 提交 PR

```bash
git checkout -b feature/your-feature
git commit -am "Add: your feature description"
git push origin feature/your-feature
```

---

## 📄 许可证

Apache License 2.0

详见 [LICENSE.txt](LICENSE.txt)

---

## 🙏 致谢

### 灵感来源

- 叙事可视化方法论
- 费曼学习法
- 认知心理学研究

### 技术栈

- [Reveal.js](https://revealjs.com/) - HTML 幻灯片框架
- [Highlight.js](https://highlightjs.org/) - 代码高亮
- [Google Fonts](https://fonts.google.com/) - 字体资源

---

## 📧 联系

有问题或建议? 欢迎:

- 提交 [Issue](https://github.com/your-repo/issues)
- 发起 [Discussion](https://github.com/your-repo/discussions)
- 提交 Pull Request

---

## 🌟 核心理念

> **故事承载思想,叙事激活学习。**

我们相信,知识不应该是冰冷的代码和枯燥的理论,而应该是引人入胜的故事。当你在阅读这些幻灯片时,你不是在"学习算法",而是在"探索思想的世界"。

让我们一起,用叙事的力量,重新定义算法学习。

---

**Happy Learning! 🚀📚✨**
