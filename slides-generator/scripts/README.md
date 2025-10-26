# Scripts 工具集

**设计理念**: 简单、可靠、必要

## 📋 脚本列表

### 1. validate-slides.sh ✅
**用途**: 验证幻灯片是否符合 Slidev 规范

**使用**:
```bash
# 基础验证
./scripts/validate-slides.sh slides.md

# 详细模式 (显示具体行号)
./scripts/validate-slides.sh slides.md --verbose

# 查看帮助
./scripts/validate-slides.sh --help
```

**验证项目** (7大类):
1. 文件格式 (UTF-8 编码、换行符)
2. Frontmatter 配置 (theme, title, fonts)
3. 分页规则 (---前后空行)
4. 代码块规范 (语言标识)
5. Mermaid 图表 (scale 参数)
6. 内容溢出防止 (滚动/缩放)
7. 内容质量 (空白页、标题)

**退出码**:
- `0`: 所有检查通过
- `1`: 有检查失败

---

### 2. preview.sh 🚀
**用途**: 快速启动 Slidev 预览

**使用**:
```bash
./scripts/preview.sh slides.md
```

**功能**:
- 检查文件是否存在
- 检查 Slidev 是否安装
- 启动 Slidev 预览服务器
- 自动打开浏览器

---

## 🔄 推荐工作流

### Agent 生成场景

```bash
# 1. Agent 生成幻灯片
# → 输出到 ~/note-vsc/slides/xxx.md

# 2. 验证规范
./scripts/validate-slides.sh ~/note-vsc/slides/xxx.md --verbose

# 3a. 如果通过 → 启动预览
./scripts/preview.sh ~/note-vsc/slides/xxx.md

# 3b. 如果失败 → Agent 分析错误
# → 改进生成逻辑
# → 重新生成
# → 重新验证
```

### 手动编辑场景

```bash
# 1. 编辑 slides.md

# 2. 验证修改
./scripts/validate-slides.sh slides.md --verbose

# 3. 如果有错误 → 查看详细信息 → 手动修复

# 4. 重新验证通过后 → 预览
./scripts/preview.sh slides.md
```

---

## 🎯 设计原则

**简单性**:
- 少即是多
- 简单的脚本更可靠

**正确性**:
- Agent 应该生成正确的内容
- 验证提供反馈促进改进

**实用性**:
- 解决真实问题
- 90% 场景够用就好
