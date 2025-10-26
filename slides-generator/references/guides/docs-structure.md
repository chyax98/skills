# Slides Generator 文档结构说明

## 📁 文档体系

### 核心文档

```
slides-generator/
├── SKILL.md                    # Skill 主文档
├── SLIDEV_QUICK_REF.md        # Slidev 快速参考 (精简)
├── SLIDEV_DOCS_INDEX.md       # Slidev 文档索引 (完整)
├── FRONTEND_SPEC.md            # 前端处理规范
├── README.md                   # 项目说明
└── slidev-docs/                # Slidev 官方文档 (81个)
    ├── guide/                  # 使用指南 (14个)
    ├── builtin/                # 内置功能 (3个)
    ├── features/               # 特性详解 (44个)
    ├── custom/                 # 自定义配置 (15个)
    └── resources/              # 资源合集 (5个)
```

---

## 📖 文档使用指南

### 1. 快速开始

**场景**: 首次使用，需要快速了解 Slidev

**推荐阅读**:
1. `SLIDEV_QUICK_REF.md` - 5分钟快速参考
2. `slidev-docs/guide/syntax.md` - 详细语法

### 2. 功能查找

**场景**: 需要实现特定功能

**查找路径**:
1. 打开 `SLIDEV_DOCS_INDEX.md`
2. 在"按功能类别"部分查找
3. 找到对应的官方文档路径

**示例**:
- 需要代码高亮 → `slidev-docs/features/line-highlighting.md`
- 需要两列布局 → `slidev-docs/builtin/layouts.md`
- 需要 Mermaid 图表 → `slidev-docs/features/mermaid.md`

### 3. 场景学习

**场景**: 按使用场景系统学习

**学习路径**:
1. 打开 `SLIDEV_DOCS_INDEX.md`
2. 查看"按使用场景"部分
3. 按场景分类查找相关文档

**示例场景**:
- 制作技术演示
- 制作教学课件
- 自定义样式
- 开发主题/插件

### 4. 完整学习

**场景**: 系统深入学习 Slidev

**学习路径**:
1. 阅读 `SLIDEV_DOCS_INDEX.md` 的"初学者路径"
2. 按顺序阅读 guide/ 目录文档
3. 根据需求阅读 features/ 目录文档
4. 进阶阅读 custom/ 目录文档

---

## 🎯 文档特点

### SLIDEV_QUICK_REF.md (快速参考)

**特点**:
- ✅ 精简，5-10分钟阅读完
- ✅ 涵盖最常用的80%功能
- ✅ 直接引用官方文档路径
- ✅ 快速决策表格

**适用场景**:
- 快速查阅语法
- 需要快速决策
- 忘记具体语法时

### SLIDEV_DOCS_INDEX.md (完整索引)

**特点**:
- ✅ 81个官方文档的完整分类
- ✅ 按场景/功能/优先级分类
- ✅ 提供学习路径建议
- ✅ 包含文档统计

**适用场景**:
- 查找特定功能的文档
- 按场景学习
- 系统了解 Slidev 能力

### slidev-docs/ (官方文档)

**特点**:
- ✅ 完整的 Slidev 官方文档副本
- ✅ 81个详细文档
- ✅ 按目录清晰分类
- ✅ 最权威的参考

**适用场景**:
- 深入了解某个功能
- 查看完整的配置选项
- 解决复杂问题

---

## 🔄 文档更新策略

### 官方文档同步

**更新来源**: `slidev-docs/` 目录
- 从 Slidev GitHub 仓库同步
- 使用 `sync-docs.sh` 脚本

**更新频率**: 按需更新
- Slidev 有重大更新时同步
- 发现文档缺失时补充

### 快速参考更新

**更新文档**: `SLIDEV_QUICK_REF.md`
- 根据官方文档变化更新
- 保持精简，只更新核心内容

**更新触发**:
- 官方文档增加重要功能
- 用户反馈常用功能遗漏

### 索引文档更新

**更新文档**: `SLIDEV_DOCS_INDEX.md`
- 官方文档目录结构变化时更新
- 文档数量变化时更新统计

---

## 📊 文档统计

### 数量统计

- **总文档数**: 81 个官方文档
  - guide/: 14 个
  - builtin/: 3 个
  - features/: 44 个
  - custom/: 15 个
  - resources/: 5 个

### 优先级分布

- ⭐⭐⭐ 必读: ~10 个
- ⭐⭐ 推荐: ~15 个
- ⭐ 可选: ~56 个

---

## 🎯 推荐使用方式

### 日常使用

```
需要快速查语法
    ↓
SLIDEV_QUICK_REF.md
    ↓
找不到？
    ↓
SLIDEV_DOCS_INDEX.md (按功能查找)
    ↓
找到对应的官方文档路径
    ↓
slidev-docs/xxx.md (详细阅读)
```

### 系统学习

```
第一次使用
    ↓
SLIDEV_DOCS_INDEX.md (查看学习路径)
    ↓
按路径阅读 guide/ 目录
    ↓
根据需求阅读 features/ 目录
    ↓
需要自定义时阅读 custom/ 目录
```

### 功能开发

```
需要实现某功能
    ↓
SLIDEV_DOCS_INDEX.md (按功能查找)
    ↓
slidev-docs/features/xxx.md (详细了解)
    ↓
slidev-docs/custom/xxx.md (查看配置)
    ↓
实现功能
```

---

## 💡 最佳实践

### 初学者

1. **第1步**: 阅读 `SLIDEV_QUICK_REF.md`
2. **第2步**: 阅读 `slidev-docs/guide/syntax.md`
3. **第3步**: 阅读 `slidev-docs/builtin/layouts.md`
4. **第4步**: 实践并查阅 `SLIDEV_DOCS_INDEX.md`

### 进阶用户

1. 熟练使用 `SLIDEV_QUICK_REF.md`
2. 根据需求查阅 `features/` 目录
3. 自定义配置查阅 `custom/` 目录

### 主题开发者

1. 阅读 `slidev-docs/guide/write-theme.md`
2. 阅读 `slidev-docs/custom/` 所有配置文档
3. 参考 `slidev-docs/resources/theme-gallery.md`

---

## 🔍 快速导航

### 语法相关

- 基础语法: `slidev-docs/guide/syntax.md`
- 动画: `slidev-docs/guide/animations.md`
- 代码高亮: `slidev-docs/features/line-highlighting.md`

### 布局相关

- 内置布局: `slidev-docs/builtin/layouts.md`
- 两列布局: Slot 语法见 `slidev-docs/features/slot-sugar.md`
- 自定义布局: `slidev-docs/guide/write-layout.md`

### 功能相关

- 代码演进: `slidev-docs/features/shiki-magic-move.md`
- Mermaid: `slidev-docs/features/mermaid.md`
- LaTeX: `slidev-docs/features/latex.md`
- 引入幻灯片: `slidev-docs/features/importing-slides.md`

### 配置相关

- 配置总览: `slidev-docs/custom/index.md`
- 目录结构: `slidev-docs/custom/directory-structure.md`
- UnoCSS: `slidev-docs/custom/config-unocss.md`

---

## 📝 维护说明

### 文档维护者

**职责**:
1. 定期同步官方文档
2. 更新快速参考和索引
3. 收集用户反馈并改进

### 同步流程

```bash
# 1. 同步官方文档
cd slidev-docs
./sync-docs.sh

# 2. 检查文档变化
git diff

# 3. 更新索引（如有目录结构变化）
# 手动更新 SLIDEV_DOCS_INDEX.md

# 4. 更新快速参考（如有重要功能）
# 手动更新 SLIDEV_QUICK_REF.md
```

---

## 🆘 问题反馈

### 文档问题

- 文档缺失或过时
- 索引分类不合理
- 快速参考内容遗漏

### 反馈方式

1. 在项目中提 Issue
2. 直接修改并提交 PR

---

**最后更新**: 2025-10-26
**文档版本**: v2.0.0
**官方文档版本**: 基于 Slidev 官方最新文档
