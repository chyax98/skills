# Learning to HTML Presentation - 安装指南

## Claude Code 安装步骤

### 方法 1: 从 GitHub 仓库安装 (推荐)

```bash
# 1. 克隆仓库
git clone https://github.com/chyax98/skills.git

# 2. 进入目录
cd skills

# 3. 复制 skill 到 Claude Code skills 目录
cp -r learning-to-html-presentation ~/.claude/skills/
```

### 方法 2: 手动安装

1. 下载本 skill 文件夹
2. 将整个 `learning-to-html-presentation` 文件夹复制到:
   - macOS/Linux: `~/.claude/skills/`
   - Windows: `%USERPROFILE%\.claude\skills\`

### 方法 3: 使用 Claude Code Marketplace

如果 skill 已发布到 marketplace:

```bash
# 在 Claude Code 中运行
claude skills install chyax98-skills/learning-to-html-presentation
```

## 验证安装

安装完成后,在 Claude Code 中输入:

```
请使用 learning-to-html-presentation skill 创建一个关于 React Hooks 的演示文稿
```

如果 Claude 识别并使用了 skill,说明安装成功!

## Claude.ai (Web) 安装

1. 访问 [Claude.ai](https://claude.ai)
2. 进入 Settings → Skills
3. 点击 "Upload Skill"
4. 上传整个 `learning-to-html-presentation` 文件夹的 ZIP 文件

## API 使用

参考 [Skills API 文档](https://docs.anthropic.com/claude/docs/skills-api)

## 故障排查

### Skill 未被识别

**检查项**:
- ✅ 文件夹名称必须是 `learning-to-html-presentation`
- ✅ SKILL.md 文件必须包含正确的 YAML frontmatter
- ✅ 文件夹位置正确 (~/.claude/skills/)

**解决方法**:
```bash
# 检查 skill 是否在正确位置
ls ~/.claude/skills/learning-to-html-presentation/

# 应该看到:
# SKILL.md  README.md  templates/  scripts/  assets/  references/
```

### 权限问题

```bash
# macOS/Linux
chmod -R 755 ~/.claude/skills/learning-to-html-presentation/

# Windows (以管理员运行 PowerShell)
icacls "%USERPROFILE%\.claude\skills\learning-to-html-presentation" /grant Everyone:F /T
```

### Claude Code 未启用 Skills

确保 Claude Code 已启用 Skills 功能:
- 检查 Claude Code 版本 ≥ 1.0
- 在设置中启用 Skills

## 更新 Skill

```bash
# 进入 skill 目录
cd ~/.claude/skills/learning-to-html-presentation/

# 拉取最新版本
git pull origin main
```

## 卸载

```bash
# macOS/Linux
rm -rf ~/.claude/skills/learning-to-html-presentation/

# Windows
rmdir /s "%USERPROFILE%\.claude\skills\learning-to-html-presentation"
```

## 技术支持

遇到问题?
- 查看 [README.md](./README.md) 了解使用方法
- 查看 [QUICKSTART.md](./QUICKSTART.md) 快速入门
- 提交 Issue 到 GitHub 仓库
