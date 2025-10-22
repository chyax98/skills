# Java Git Defect Analyzer

> 基于需求文档对比的 Java 代码缺陷分析工具

一个强大的 Claude Skill,用于分析 Java 项目的 Git 提交,识别功能缺陷、高影响 Bug 和代码质量问题。核心特性是**需求驱动分析**——对比需求文档与代码实现,确保功能正确性。

## ✨ 核心功能

### 🎯 功能缺陷检测 (PRIMARY)
- **功能完整性验证**: 检查需求功能是否完全实现
- **业务逻辑验证**: 对比代码执行流程与需求描述
- **实现偏差识别**: 发现代码行为与需求不符的地方
- **需求覆盖率分析**: 生成需求实现覆盖矩阵

### 🔴 高影响缺陷检测
- **NPE 风险**: 未检查 null 的方法调用
- **资源泄漏**: 未关闭的数据库连接、文件流
- **SQL 注入**: 字符串拼接构造 SQL 查询
- **硬编码密钥**: 密码、API 密钥硬编码在代码中
- **并发问题**: 双重检查锁定、竞态条件

### 📊 智能优先级分类
- **🔴 CRITICAL**: 功能缺陷、严重安全问题 → 阻止发布
- **🟠 HIGH**: 功能偏差、高影响 Bug → 合并前修复
- **🟡 MEDIUM**: 中等影响问题 → 下一迭代
- **🟢 LOW**: 代码质量问题 → 技术债务

## 🚀 快速开始

### 安装

1. 将此 Skill 复制到 Claude Skills 目录:
   ```bash
   cp -r java-git-defect-analyzer ~/.claude/skills/
   ```

2. 确保 Python 3.8+ 已安装:
   ```bash
   python3 --version
   ```

3. 安装依赖 (可选,脚本会自动检查):
   ```bash
   pip install GitPython
   ```

### 基本使用

#### 1. 触发 Skill

在 Claude Code 中输入:
```
review-java
```

#### 2. 提供输入

Claude 会请求以下信息:

**必需输入**:
- **需求文档**: 文件路径或直接粘贴需求文本
- **Git Commit**: commit hash 或 `HEAD` (默认)

**示例交互**:
```
You: review-java

Claude: 请提供以下信息:
        1. 需求文档 (文件路径或直接粘贴)
        2. Git commit reference (默认: HEAD)

You: 需求文档: docs/feature-login.md
     Commit: HEAD

Claude: [开始分析...]
```

#### 3. 查看分析报告

Claude 会生成详细的 Markdown 报告,包含:
- 执行摘要 (总问题数、严重程度分布)
- 功能缺陷详细列表 (带修复建议)
- 高影响 Bug 列表 (带代码示例)
- 需求覆盖率分析表

## 📋 使用示例

### 示例 1: 功能缺失检测

**需求文档** (`feature-login.md`):
```markdown
# 用户登录功能

## 功能要求
1. 支持手机号和邮箱两种登录方式
2. 登录成功后记录登录日志 (时间、IP、设备)
3. 发送登录通知邮件
```

**Git Commit**: 实现了登录逻辑,但缺少日志记录

**分析结果**:
```markdown
## 🔴 CRITICAL - 功能缺失

### 缺失功能: 登录日志记录
- **Requirement**: 登录成功后记录登录日志 (时间、IP、设备)
- **Implementation Status**: ❌ 完全缺失
- **Impact**: 无法追踪用户登录行为,影响安全审计
- **Location**: `UserController.java:45`
- **Fix Suggestion**:
  ```java
  @PostMapping("/login")
  public ResponseEntity<UserVO> login(@RequestBody LoginRequest request) {
      User user = authService.authenticate(request);

      // ✅ 添加日志记录
      LoginLog log = new LoginLog();
      log.setUserId(user.getId());
      log.setLoginTime(LocalDateTime.now());
      log.setIpAddress(request.getRemoteAddr());
      log.setDeviceInfo(request.getHeader("User-Agent"));
      loginLogService.save(log);

      return ResponseEntity.ok(userMapper.toVO(user));
  }
  ```
```

---

### 示例 2: 高影响 Bug 检测

**代码提交**: 新增用户查询功能

**分析结果**:
```markdown
## 🟠 HIGH - NPE 风险

### NPE 风险: 未检查 null
- **Type**: NPE Risk
- **Location**: `UserService.java:23`
- **Problem**: `findById()` 可能返回 null, 直接调用 `getUsername()` 会抛出 NPE
- **Current Code**:
  ```java
  public String getUserById(Long id) {
      User user = userRepository.findById(id);
      return user.getUsername(); // ❌ NPE Risk
  }
  ```
- **Fix Suggestion**:
  ```java
  public String getUserById(Long id) {
      User user = userRepository.findById(id);
      if (user == null) {
          throw new UserNotFoundException("User not found: " + id);
      }
      return user.getUsername();
  }
  ```
```

---

### 示例 3: 需求覆盖率分析

**分析结果**:
```markdown
## Requirement Coverage Analysis

| 需求功能点 | 实现状态 | 问题说明 |
|-----------|---------|---------|
| 手机号登录 | ✅ 完整实现 | - |
| 邮箱登录 | ⚠️ 部分实现 | 缺少邮箱格式验证 |
| 登录日志记录 | ❌ 缺失 | 未实现日志记录逻辑 |
| 登录通知邮件 | ❌ 缺失 | 未实现邮件发送 |

**Coverage Score**: 2.5/10
```

## 🛠️ 高级用法

### 自定义优先级配置

编辑 `assets/priority_matrix.json` 调整严重程度评分:

```json
{
  "defect_pattern_mapping": {
    "functional_defects": {
      "missing_functionality": {
        "severity": "CRITICAL",
        "score": 10
      }
    }
  }
}
```

### 扩展缺陷检测规则

在 `references/` 目录添加新的缺陷模式:

1. 编辑 `references/functional_defect_patterns.md`
2. 添加新模式定义:
   ```markdown
   ## 7. 新缺陷类型

   ### 定义
   ...

   ### 检测规则
   ...
   ```

3. 更新 `scripts/defect_detector.py` 添加检测逻辑

### 分析特定提交范围

```bash
# 分析最近 5 次提交
python scripts/analyze_commit.py HEAD~5..HEAD

# 分析特定分支
python scripts/analyze_commit.py feature/login

# 对比两个提交
python scripts/analyze_commit.py abc123..def456
```

## 📂 项目结构

```
java-git-defect-analyzer/
├── SKILL.md                        # Claude 核心指令文件
├── README.md                       # 本文档
├── LICENSE.txt                     # Apache 2.0 许可证
├── scripts/
│   ├── analyze_commit.py          # Git 提交分析引擎
│   ├── requirement_matcher.py     # 需求匹配分析器
│   └── defect_detector.py         # 缺陷检测引擎
├── references/
│   ├── functional_defect_patterns.md    # 功能缺陷模式库
│   ├── requirement_checklist.md         # 需求验证清单
│   ├── critical_bugs.md                 # 高影响 Bug 检测规则
│   └── low_priority_issues.md           # 低优先级问题参考
└── assets/
    └── priority_matrix.json        # 优先级评分配置
```

## 🎯 最佳实践

### ✅ 推荐场景

1. **Pre-merge PR Review**: 合并前验证功能完整性
2. **Feature Acceptance**: 验收新功能是否符合需求
3. **Sprint Review**: 评估代码质量和技术债务
4. **Refactoring Verification**: 确保重构未破坏功能

### ⚠️ 使用建议

1. **提供清晰的需求文档**: 详细的需求描述能提高分析准确性
2. **聚焦单一功能的提交**: 分析范围过大会降低结果可读性
3. **结合人工 Review**: 自动分析可能有误报,需人工验证
4. **持续使用追踪趋势**: 在开发过程中持续使用,而非仅在最终审查

### 🚫 不适用场景

- 没有明确需求文档的探索性开发
- 纯重构提交 (无功能变更)
- 配置文件修改

## 🔧 故障排查

### 问题: 脚本执行失败

**错误**: `ModuleNotFoundError: No module named 'git'`

**解决**:
```bash
pip install GitPython
```

---

### 问题: Git 命令找不到

**错误**: `command not found: git`

**解决**: 确保 Git 已安装并在 PATH 中
```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt-get install git
```

---

### 问题: 需求匹配不准确

**原因**: 需求文档格式不清晰或关键词过少

**改进建议**:
- 使用明确的操作动词 (记录、发送、验证、生成)
- 采用结构化格式 (Markdown 标题、编号列表)
- 避免模糊描述,使用具体功能点

---

### 问题: 误报过多

**原因**: 静态分析规则过于严格

**解决**:
1. 编辑 `assets/priority_matrix.json` 调整评分权重
2. 在 `references/` 文档中添加例外说明
3. 结合人工判断,筛选真实问题

## 🤝 贡献指南

欢迎贡献新的缺陷检测模式!

1. Fork 本 Skill
2. 在 `references/` 中添加新模式文档
3. 在 `scripts/defect_detector.py` 中实现检测逻辑
4. 提交 Pull Request

## 📄 许可证

Apache License 2.0

## 🙋 常见问题

### Q1: 这个 Skill 能完全替代人工代码审查吗?

**A**: 不能。这是一个**辅助工具**,能自动发现常见问题,但不能替代人工审查的上下文理解和经验判断。最佳实践是将自动分析结果作为 Review 的起点。

### Q2: 分析需要多长时间?

**A**: 取决于提交规模:
- 小型提交 (1-3 文件): < 10 秒
- 中型提交 (5-10 文件): 30 秒 - 1 分钟
- 大型提交 (>20 文件): 2-5 分钟

### Q3: 支持其他编程语言吗?

**A**: 当前版本专注于 Java。如需支持其他语言 (Python, JavaScript, Go),可以:
1. 复制 Skill 并重命名
2. 修改 `scripts/` 中的检测规则
3. 更新 `references/` 中的语言特定模式

### Q4: 如何集成到 CI/CD 流程?

**A**: 可以在 CI 中调用脚本:
```yaml
# .github/workflows/code-review.yml
- name: Analyze Code Quality
  run: |
    python scripts/analyze_commit.py ${{ github.sha }} > report.json
    python scripts/requirement_matcher.py --requirement docs/requirements.md --commit ${{ github.sha }}
```

### Q5: 需求文档必须是 Markdown 格式吗?

**A**: 不是必须的。支持:
- Markdown (.md)
- 纯文本 (.txt)
- 直接粘贴的文本

关键是内容结构清晰,使用明确的功能描述。

## 📞 支持

遇到问题或有改进建议?
- 提交 Issue
- 查看 `SKILL.md` 了解详细用法
- 参考 `references/` 中的模式库

---

**Happy Coding! 让每一次提交都符合需求规格!** 🚀
