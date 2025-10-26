# Code Analyzer 架构设计

## 核心设计理念

### 1. 主 Skill + 子 Skill 模式

```
code-analyzer (主 Skill)
├── init-project (子 Skill) - 项目初始化
└── analyze-commits (执行分析) - 主工作流
```

**职责分离**:

- **init-project**: 首次使用,建立项目上下文
- **analyze-commits**: 分析具体提交,依赖项目上下文

### 2. 项目上下文 (Project Context)

**概念**: 项目的元信息,分析时的前置知识

**内容**:

```json
{
  "project_name": "user-service",
  "techstack": "java-springboot",
  "version": "3.2.0",
  "build_tool": "maven",
  "modules": ["user-service", "order-service"],
  "key_packages": [
    "com.example.controller",
    "com.example.service",
    "com.example.repository"
  ],
  "serena_indexed": true,
  "last_index_time": "2025-10-26 10:30:00",
  "template_path": "templates/java-springboot/"
}
```

**存储位置**: `.code-analyzer/project-context.json`

### 3. 两阶段工作流

```
阶段 1: 初始化 (首次使用)
├─ init-project skill 触发
├─ 扫描项目结构
├─ 识别技术栈
├─ 建立 Serena 索引
├─ 生成 project-context.json
└─ 输出: "项目已初始化,可以开始分析"

阶段 2: 分析 (后续使用)
├─ analyze-commits 触发
├─ 读取 project-context.json
├─ 执行 6 步工作流
├─ 增量更新 Serena 索引
└─ 输出: 测试分析报告
```

## 架构优势

### 1. 解耦技术栈

**模板独立性**:

```
templates/
├── java-springboot/
│   ├── init.md          # 初始化逻辑
│   ├── defect-rules.md  # 缺陷检测规则
│   └── prompts.md       # 提示词模板
├── python-django/
│   ├── init.md
│   ├── defect-rules.md
│   └── prompts.md
└── nodejs-express/
    ├── init.md
    ├── defect-rules.md
    └── prompts.md
```

**新增技术栈**: 只需添加新的 template 目录,无需修改核心工作流。

### 2. 状态持久化

**project-context.json**:

- 避免重复扫描
- 加速后续分析
- 支持增量索引

### 3. 职责清晰

| 组件 | 职责 | 输入 | 输出 |
|------|------|------|------|
| init-project | 项目初始化 | 项目路径 | project-context.json |
| analyze-commits | 提交分析 | Git 范围 + 需求 | 测试分析报告 |
| templates/{stack}/ | 技术栈规则 | - | 规则定义 |
| workflows/ | 通用流程 | - | 流程定义 |
| integrations/ | MCP 工具 | - | 工具使用指南 |

## 详细设计

### init-project Skill

**触发条件**:

```
触发词:
- "初始化项目"
- "建立代码索引"
- "首次使用 code-analyzer"

自动触发:
- 如果 .code-analyzer/project-context.json 不存在
```

**工作流程**:

```
Step 1: 扫描项目结构
├─ 识别项目类型 (Java/Python/Node.js)
├─ 识别构建工具 (Maven/Gradle/npm)
└─ 识别项目模块

Step 2: 识别技术栈
├─ 检查依赖文件 (pom.xml/requirements.txt/package.json)
├─ 识别框架 (SpringBoot/Django/Express)
├─ 识别版本
└─ 加载对应模板

Step 3: 扫描核心包
├─ 识别 Controller 包
├─ 识别 Service 包
├─ 识别 Repository 包
└─ 识别实体包

Step 4: 建立 Serena 索引
├─ 检查 Serena 状态
├─ 创建全量索引 (2-5分钟)
└─ 记录索引时间

Step 5: 生成项目上下文
├─ 汇总所有信息
├─ 保存到 .code-analyzer/project-context.json
└─ 输出初始化报告
```

**输出示例**:

```markdown
# 项目初始化完成

## 项目信息

- **项目名称**: user-service
- **技术栈**: Java + SpringBoot 3.2.0
- **构建工具**: Maven
- **模块数量**: 1 个

## 核心包结构

- Controller: `com.example.controller` (8 个文件)
- Service: `com.example.service` (12 个文件)
- Repository: `com.example.repository` (6 个文件)
- Entity: `com.example.entity` (10 个文件)

## Serena 索引

- **状态**: ✅ 已完成
- **耗时**: 3分15秒
- **索引文件**: 36 个
- **索引行数**: 8,542 行

## 项目上下文

已保存到被分析项目根目录: `{被分析项目}/.code-analyzer/project-context.json`

## 下一步

现在可以使用 `code-analyzer` 分析提交了:

\`\`\`
分析本分支近3次提交

需求: 用户登录优化
...
\`\`\`
```

### analyze-commits 主工作流

**触发条件**:

```
触发词:
- "分析本分支近X次提交"
- "分析 feature/xxx 分支的提交"
- "代码审查"
- "提测检查"
```

**前置检查**:

```
检查 1: project-context.json 是否存在
├─ 存在 → 继续
└─ 不存在 → 自动调用 init-project

检查 2: Serena 索引是否最新
├─ 24小时内 → 增量更新 (10-30秒)
└─ 超过24小时 → 全量索引 (2-5分钟)
```

**工作流程**:

```
Step 1: 代码变更提取 (workflows/step1-code-change.md)
Step 2: 技术栈识别 (读取 project-context.json)
Step 3: 缺陷检测 (templates/{techstack}/defect-rules.md)
Step 4: 需求验证 (integrations/sequential-mcp.md)
Step 5: 影响分析 (integrations/serena-mcp.md)
Step 6: 报告生成 (specs/report-format.md)
```

## 模板解耦机制

### 模板注册

**templates/registry.json**:

```json
{
  "templates": [
    {
      "id": "java-springboot",
      "name": "Java + SpringBoot",
      "detect_files": ["pom.xml", "build.gradle"],
      "detect_pattern": "spring-boot-starter",
      "init_workflow": "templates/java-springboot/init.md",
      "defect_rules": "templates/java-springboot/defect-rules.md",
      "prompts": "templates/java-springboot/prompts.md"
    },
    {
      "id": "python-django",
      "name": "Python + Django",
      "detect_files": ["requirements.txt", "manage.py"],
      "detect_pattern": "Django",
      "init_workflow": "templates/python-django/init.md",
      "defect_rules": "templates/python-django/defect-rules.md",
      "prompts": "templates/python-django/prompts.md"
    }
  ]
}
```

### 新增技术栈步骤

**Step 1**: 创建模板目录

```bash
mkdir -p templates/rust-actix
```

**Step 2**: 编写规则文件

```
templates/rust-actix/
├── init.md           # 初始化逻辑 (如何识别项目)
├── defect-rules.md   # 缺陷检测规则
└── prompts.md        # 提示词模板
```

**Step 3**: 注册到 registry.json

```json
{
  "id": "rust-actix",
  "name": "Rust + Actix",
  "detect_files": ["Cargo.toml"],
  "detect_pattern": "actix-web",
  "init_workflow": "templates/rust-actix/init.md",
  "defect_rules": "templates/rust-actix/defect-rules.md",
  "prompts": "templates/rust-actix/prompts.md"
}
```

**Step 4**: 测试

```
初始化项目 (自动识别 Rust + Actix)
分析近3次提交 (自动加载 rust-actix 规则)
```

## 文件组织

```
code-analyzer/
├── SKILL.md                    # 主 Skill 入口
├── ARCHITECTURE.md             # 架构设计 (本文档)
├── README.md                   # 快速开始
│
├── skills/                     # 子 Skills
│   ├── init-project.md         # 项目初始化 Skill
│   └── analyze-commits.md      # 分析提交 Skill (可选,复用 SKILL.md)
│
├── references/
│   ├── workflows/              # 6 步通用工作流
│   ├── integrations/           # MCP 工具集成
│   └── specs/                  # 规范定义
│
├── templates/                  # 技术栈模板 (解耦)
│   ├── registry.json           # 模板注册表
│   ├── java-springboot/
│   ├── python-django/
│   └── nodejs-express/
│
└── examples/                   # 示例
    ├── project-context.json    # 项目上下文示例
    └── sample-report.md        # 报告示例
```

## 用户体验

### 首次使用

```
用户: "分析本分支近3次提交,需求: 用户登录优化"

code-analyzer:
  → 检测到未初始化
  → 自动调用 init-project
  → "正在初始化项目..."
  → "识别技术栈: Java + SpringBoot 3.2.0"
  → "建立 Serena 索引 (预计 3 分钟)..."
  → "索引完成,已保存项目上下文"
  → 执行分析工作流
  → 输出测试分析报告
```

### 后续使用

```
用户: "分析本分支近3次提交,需求: 支付流程优化"

code-analyzer:
  → 读取项目上下文
  → "检测到技术栈: Java + SpringBoot"
  → "增量更新 Serena 索引 (15秒)..."
  → 执行分析工作流
  → 输出测试分析报告
```

## 核心优势总结

1. **解耦技术栈**: 新增语言/框架只需添加 template,不改核心流程
2. **状态持久化**: 项目上下文避免重复扫描,加速后续分析
3. **职责清晰**: init-project 负责初始化,analyze-commits 负责分析
4. **自动化友好**: 自动检测未初始化,自动调用 init-project
5. **增量优化**: Serena 索引支持增量更新,节省时间
6. **模板驱动**: 所有技术栈特定逻辑在 template 中,易于扩展

## 下一步实施

1. ✅ 创建 skills/init-project.md 子 Skill
2. ✅ 创建 templates/registry.json 注册表
3. ✅ 为每个 template 添加 init.md
4. ✅ 更新 SKILL.md,说明两阶段工作流
5. ✅ 创建示例 project-context.json

---

**版本**: 1.0.0
**设计日期**: 2025-10-26
**设计者**: AI 架构分析
