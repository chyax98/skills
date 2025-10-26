# 路径说明文档

## 重要概念澄清

### code-analyzer skill 目录 vs 被分析项目目录

**code-analyzer skill 目录** (本目录):
```
/Users/Apple/dev/skills/code-analyzer/
├── SKILL.md
├── README.md
├── references/
├── templates/
└── ...
```

**被分析的实际项目目录** (用户项目):
```
/home/user/myproject/           # 或任意其他路径
├── src/
├── pom.xml
├── .git/
└── ...
```

## 路径使用规则

### 1. 报告保存位置

❌ **错误理解**: 报告保存在 code-analyzer skill 目录下
```
/Users/Apple/dev/skills/code-analyzer/analysis-reports/  # 错误!
```

✅ **正确理解**: 报告保存在**被分析项目的根目录**下
```
/home/user/myproject/analysis-reports/用户登录优化/feature-login-20251026-153022.md
```

### 2. 项目上下文保存位置

❌ **错误理解**: 保存在 skill 目录下
```
/Users/Apple/dev/skills/code-analyzer/.code-analyzer/project-context.json  # 错误!
```

✅ **正确理解**: 保存在**被分析项目的根目录**下
```
/home/user/myproject/.code-analyzer/project-context.json
```

### 3. Serena 索引位置

Serena MCP 的索引保存在**被分析项目的根目录**下:
```
/home/user/myproject/.serena/
```

## 工作流程示例

假设用户要分析的项目路径是: `/home/user/e-commerce/`

### 步骤 1: 用户在项目目录调用 skill

```bash
cd /home/user/e-commerce/
# 在 Claude Code 中调用
分析本分支近3次提交
需求: 支付流程优化
```

### 步骤 2: code-analyzer 执行分析

- 读取: `/home/user/e-commerce/.git/` (Git 历史)
- 创建/读取: `/home/user/e-commerce/.code-analyzer/project-context.json` (项目上下文)
- 使用 Serena 索引: `/home/user/e-commerce/.serena/` (如果已存在)

### 步骤 3: 生成报告

报告保存在:
```
/home/user/e-commerce/analysis-reports/支付流程优化/feature-payment-20251026-153022.md
```

## 文档中的路径表示

### 相对路径表示

文档中使用 `./` 或 `{被分析项目}/` 表示**被分析项目的根目录**:

```markdown
# 文档中的写法
./analysis-reports/{需求名称}/

# 实际含义
{被分析项目根目录}/analysis-reports/{需求名称}/

# 具体例子
/home/user/myproject/analysis-reports/登录优化/
```

### @ 引用表示

`@` 开头的路径是 skill 内部文档引用:

```markdown
@references/workflows/step1-code-change.md
# 指向:
/Users/Apple/dev/skills/code-analyzer/references/workflows/step1-code-change.md
```

## 总结

| 内容类型 | 保存位置 | 示例路径 |
|---------|---------|---------|
| **测试分析报告** | 被分析项目 | `/home/user/myproject/analysis-reports/` |
| **项目上下文** | 被分析项目 | `/home/user/myproject/.code-analyzer/project-context.json` |
| **Serena 索引** | 被分析项目 | `/home/user/myproject/.serena/` |
| **skill 文档** | skill 目录 | `/Users/Apple/dev/skills/code-analyzer/` |
| **检测规则模板** | skill 目录 | `/Users/Apple/dev/skills/code-analyzer/templates/` |

---

**关键原则**: code-analyzer 是一个**分析工具**,所有分析结果(报告、上下文)都保存在**被分析的目标项目**中,不污染 skill 本身的目录。
