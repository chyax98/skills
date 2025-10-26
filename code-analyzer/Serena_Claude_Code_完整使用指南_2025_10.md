# Serena MCP Server 在 Claude Code 中的完整使用指南

> **最后更新**: 2025年10月 | **版本**: 基于社区最新实践
> 这是一份详尽的 Serena 使用文档，涵盖安装、配置、核心特性、常见问题及最佳实践

---

## 📋 目录

1. [什么是 Serena](#什么是-serena)
2. [核心特性与优势](#核心特性与优势)
3. [安装与配置](#安装与配置)
4. [Claude Code 集成](#claude-code-集成)
5. [核心功能详解](#核心功能详解)
6. [界面与监控](#界面与监控)
7. [配置系统详解](#配置系统详解)
8. [最佳实践](#最佳实践)
9. [常见问题解决](#常见问题解决)
10. [社区使用案例](#社区使用案例)

---

## 什么是 Serena

**Serena** 是一个开源的 AI 编码代理工具包，通过 **MCP (Model Context Protocol)** 将大语言模型转变为具备专业 IDE 能力的编程助手。

### 核心定位

```
传统 AI 编程工具：基于文本搜索 (grep/RAG)
                ↓ 短板
         • 无法理解代码结构
         • 容易误读符号关系
         • 大型项目性能差

Serena：基于 LSP (Language Server Protocol)
                ↓ 优势
         • 符号级代码理解
         • 精确的引用查找
         • IDE 级别的操作能力
```

### 为什么选择 Serena

✅ **完全免费开源** - 无需 API 订阅费用
✅ **符号级理解** - 基于 LSP，像 IDE 一样理解代码
✅ **多语言支持** - 支持 20+ 种编程语言
✅ **模型无关** - 可与 Claude、GPT、Gemini 等任意模型配合
✅ **节省 Token** - 社区报告可节省高达 70% 的 token 使用量
✅ **提升质量** - 精确的代码操作显著提高生成代码质量

---

## 核心特性与优势

### 1. 语义代码分析能力

#### LSP 驱动的智能理解

Serena 通过语言服务器协议 (LSP) 实现了 IDE 级别的代码理解：

```
传统方式                      Serena 方式
───────────────────────      ──────────────────────
grep "function login"        find_symbol(name="login", type="function")
  ↓ 问题                       ↓ 结果
• 匹配注释中的文本            • 精确定位函数定义
• 字符串中的误匹配            • 查找所有引用位置
• 无法区分定义和调用          • 理解符号间关系
```

#### 支持的操作类型

| 工具名称 | 功能说明 | 使用场景 |
|---------|---------|---------|
| `find_symbol` | 全局/局部符号搜索 | 查找函数、类、变量定义 |
| `find_referencing_symbols` | 查找符号引用 | 了解代码依赖关系 |
| `get_symbols_overview` | 文件符号概览 | 快速了解文件结构 |
| `replace_symbol_body` | 替换符号定义 | 精确修改函数/类实现 |
| `insert_after_symbol` | 符号后插入代码 | 在函数/类后添加内容 |
| `insert_before_symbol` | 符号前插入代码 | 在定义前添加注释/装饰器 |

### 2. 多语言支持矩阵

Serena 通过集成各语言的 LSP 实现，提供开箱即用的支持：

#### Tier 1: 完全支持（无需额外配置）
- **Python** - 使用 Pylance/Pyright
- **TypeScript/JavaScript** - 使用 tsserver
- **Go** - 自动安装 gopls
- **Rust** - 使用 rust-analyzer (需 rustup)
- **PHP** - 使用 Intelephense
- **Ruby** - 使用 ruby-lsp (可选 Solargraph)

#### Tier 2: 需要语言环境
- **Java** - 需要 JDK (启动较慢)
- **C#** - 使用 OmniSharp
- **C/C++** - 使用 clangd
- **Swift** - 需要 Xcode/Swift 工具链
- **Kotlin** - 使用官方 kotlin-lsp (pre-alpha)

#### Tier 3: 实验性支持
- **Elixir** - 需要 NextLS + Elixir (不支持 Windows)
- **Erlang** - 需要 erlang_ls (可能较慢)
- **Perl** - 需要 Perl::LanguageServer
- **Markdown** - 使用 marksman (文档项目)

### 3. 记忆系统 (Memory System)

#### 项目知识持久化

Serena 在 `.serena/memories/` 目录中存储项目知识：

```
项目根目录/
├── .serena/
│   ├── project.yml          # 项目配置
│   ├── memories/            # 记忆文件目录
│   │   ├── project_structure.md      # 项目结构概览
│   │   ├── build_and_test.md         # 构建与测试指令
│   │   ├── architecture_overview.md  # 架构说明
│   │   └── custom_memory.md          # 自定义记忆
│   └── logs/                # 日志目录
```

#### 记忆工具

- `write_memory(name, content)` - 写入记忆
- `read_memory(name)` - 读取记忆
- `list_memories()` - 列出所有记忆
- `delete_memory(name)` - 删除记忆

#### 使用建议

```python
# 第一次使用项目时，让 AI 进行 onboarding
"请对这个项目进行 onboarding 并创建记忆"

# 在后续会话中
"读取项目结构记忆"
"根据构建记忆运行测试"

# 添加自定义知识
"将当前的重构计划写入记忆，命名为 refactoring_plan"
```

### 4. 项目索引系统

#### 为什么需要索引？

```
未索引项目                    已索引项目
──────────────              ──────────────
首次工具调用: 30-60秒        首次工具调用: 1-3秒
  ↓ 原因                      ↓ 原因
• 实时解析所有文件           • 预加载符号表
• 构建符号依赖图             • 缓存语法树
• 启动语言服务器             • 即时查询
```

#### 索引命令

```bash
# 在项目目录下执行
uvx --from git+https://github.com/oraios/serena serena project index

# 或使用本地安装
uv run --directory /path/to/serena serena project index
```

#### 索引最佳时机

✅ **应该索引的项目**
- 文件数量 > 100
- 代码行数 > 10,000
- 需要频繁使用 Serena 的项目
- 复杂的依赖关系

❌ **可以不索引的项目**
- 小型脚本项目 (< 50 文件)
- 一次性分析任务
- 原型或演示项目

---

## 安装与配置

### 前置要求

#### 1. 安装 uv 包管理器

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**验证安装:**
```bash
uv --version
uvx --version
```

#### 2. 确保 Claude Code 已安装

从 [claude.ai/code](https://claude.ai/code) 下载并安装最新版本。

---

## Claude Code 集成

### 快速集成（推荐方式）

在您的项目目录下运行：

```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project $(pwd)
```

### 配置详解

#### 参数说明

```bash
claude mcp add serena          # MCP 服务器名称
  -- uvx                       # 使用 uvx 运行
  --from git+https://...       # 从 GitHub 仓库安装
  serena start-mcp-server      # 启动 MCP 服务器
  --context ide-assistant      # 使用 IDE 助手上下文 (重要!)
  --project $(pwd)             # 自动激活当前项目
```

#### 上下文 (Context) 选择

| 上下文 | 适用场景 | 工具集 |
|--------|---------|--------|
| `ide-assistant` | Claude Code, Cursor, Cline | 禁用 shell 工具（使用宿主的） |
| `desktop-app` | Claude Desktop | 完整工具集（包括 shell） |
| `codex` | OpenAI Codex CLI | Codex 兼容模式 |
| `agent` | Agno, 独立代理 | 自主代理工具集 |

**⚠️ 重要**: 在 Claude Code 中**必须**使用 `--context ide-assistant`，否则工具冲突会导致功能异常。

### Windows 用户特别说明

#### 路径格式问题

Windows 用户在配置时需要注意路径格式：

**错误示例:**
```bash
# ❌ 不要使用反斜杠
--project C:\Users\username\project

# ❌ $(pwd) 在 Windows 中可能无法解析
--project $(pwd)
```

**正确示例:**
```bash
# ✅ 使用正斜杠
--project C:/Users/username/project

# ✅ 或者使用固定路径
--project E:/code/myproject
```

#### Git 配置

Windows 用户必须配置 Git 的换行符处理：

```bash
# 全局配置（推荐）
git config --global core.autocrlf true

# 或仅当前仓库
git config core.autocrlf true
```

原因：Serena 使用系统原生换行符写入文件，不配置会导致 `git diff` 显示大量无意义的换行符变化。

### 验证安装

#### 1. 检查 MCP 连接状态

在 Claude Code 中运行：
```
/mcp
```

应该看到 `serena` 显示为已连接状态（绿色勾号）。

#### 2. 查看可用工具

```
列出 Serena 的所有工具
```

应该看到类似输出：
```
可用的 Serena 工具:
- find_symbol
- find_referencing_symbols
- get_symbols_overview
- replace_symbol_body
...
```

#### 3. 测试基本功能

```
使用 Serena 查找这个项目中的所有 class 定义
```

如果返回了符号列表，说明安装成功！

### 指令加载（Claude Code v1.0.52+）

**最新版本（≥ v1.0.52）**: 自动读取 Serena 指令，无需手动操作。

**旧版本**: 需要手动触发指令读取：
```
/mcp__serena__initial_instructions
```
或
```
读取 Serena 的初始指令
```

---

## 核心功能详解

### 1. 项目激活与管理

#### 自动激活（推荐）

在配置时使用 `--project $(pwd)` 参数，Serena 会在启动时自动激活当前项目。

#### 手动激活

```bash
# 通过绝对路径激活
激活项目 /Users/username/myproject

# 通过项目名称激活（需要之前激活过）
激活项目 myproject
```

#### 项目配置文件

首次激活后，Serena 会在项目根目录生成 `.serena/project.yml`：

```yaml
# 项目名称（用于后续引用）
name: myproject

# 语言配置（自动检测，也可手动指定）
language: python  # python, typescript, go, rust, java, etc.

# 忽略文件规则
ignore_all_files_in_gitignore: true
ignored_paths:
  - "node_modules/**"
  - "dist/**"
  - "*.pyc"

# 只读模式（禁用所有编辑工具）
read_only: false

# 语言服务器特定配置
language_server_settings:
  python:
    venv_path: ".venv"
```

### 2. Onboarding（项目学习）

#### 什么是 Onboarding？

Onboarding 是 Serena 首次使用项目时进行的自动学习过程：

```
Onboarding 流程
──────────────────────────────────────
1. 📂 分析项目结构
   • 识别主要目录
   • 确定项目类型
   • 检测技术栈

2. 🔍 提取关键信息
   • 入口文件
   • 核心模块
   • 配置文件

3. 🧪 识别开发流程
   • 构建命令
   • 测试命令
   • 运行方式

4. 💾 创建记忆文件
   • project_structure.md
   • build_and_test.md
   • architecture_overview.md
```

#### 手动触发 Onboarding

```
请对当前项目进行 onboarding
```

#### 检查 Onboarding 状态

```
检查项目是否已完成 onboarding
```

#### Onboarding 后的最佳实践

1. **审查记忆文件** - 检查 `.serena/memories/` 中生成的文件
2. **补充信息** - 手动添加自定义记忆
3. **新建会话** - Onboarding 会消耗大量上下文，建议在新会话中继续工作

### 3. 符号级代码操作

#### 查找符号定义

```python
# 示例：查找所有名为 "authenticate" 的函数
find_symbol(name="authenticate", symbol_type="function")

# 返回结果
[
  {
    "file": "src/auth/login.py",
    "line": 45,
    "name": "authenticate",
    "type": "function",
    "scope": "module"
  },
  ...
]
```

**使用场景**:
- 快速定位函数/类定义
- 了解同名符号的分布
- 重构前的影响分析

#### 查找符号引用

```python
# 示例：查找所有调用 authenticate 函数的位置
find_referencing_symbols(
    file="src/auth/login.py",
    line=45
)

# 返回结果
[
  {"file": "src/api/routes.py", "line": 123},
  {"file": "tests/test_auth.py", "line": 67},
  ...
]
```

**使用场景**:
- 评估修改影响范围
- 追踪函数使用情况
- 安全删除未使用代码

#### 获取文件符号概览

```python
# 示例：查看文件的顶层结构
get_symbols_overview(file="src/models/user.py")

# 返回类似
"""
Class: User (line 10-45)
  Method: __init__ (line 12-15)
  Method: authenticate (line 17-23)
  Property: email (line 25)

Function: create_user (line 48-60)
Function: validate_email (line 62-70)
"""
```

**使用场景**:
- 快速了解文件内容
- 规划代码修改
- 生成文档大纲

#### 精确编辑符号

```python
# 替换函数实现
replace_symbol_body(
    file="src/auth/login.py",
    line=45,  # authenticate 函数的行号
    new_body="""
    def authenticate(username, password):
        # 新的实现
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            return user
        raise AuthenticationError("Invalid credentials")
    """
)
```

```python
# 在函数后插入新代码
insert_after_symbol(
    file="src/auth/login.py",
    line=45,
    content="""

    def logout(user):
        '''Log out the user and clear session'''
        session.clear()
        return True
    """
)
```

**优势对比**:

| 操作方式 | 传统字符串替换 | Serena 符号编辑 |
|---------|---------------|----------------|
| 精确度 | ❌ 容易误匹配 | ✅ 精确定位 |
| 安全性 | ❌ 可能破坏代码 | ✅ 语法感知 |
| 可靠性 | ❌ 依赖上下文 | ✅ 基于结构 |
| Token 消耗 | 高（需要读取大段代码） | 低（直接操作符号） |

### 4. 文件系统操作

虽然 Serena 专注于符号级操作，但仍提供必要的文件工具：

```python
# 列出目录内容
list_dir(path="src/", recursive=True)

# 查找文件
find_file(pattern="*.py", paths=["src/", "tests/"])

# 搜索文本模式
search_for_pattern(pattern="TODO", paths=["src/"])

# 读取文件
read_file(file="src/config.py")

# 创建/覆盖文件
create_text_file(file="new_module.py", content="...")

# 正则替换
replace_regex(
    file="config.py",
    pattern=r"DEBUG = False",
    replacement="DEBUG = True"
)
```

### 5. Shell 命令执行

**⚠️ 注意**: 在 `ide-assistant` 上下文中（Claude Code 默认），Serena 的 shell 工具被**禁用**，因为 Claude Code 有自己的 shell 工具。

在 `desktop-app` 上下文中（Claude Desktop），可以使用：

```python
execute_shell_command("pytest tests/")
```

---

## 界面与监控

### Web Dashboard（默认启用）

#### 访问方式

启动 Serena 后，浏览器会自动打开：
```
http://localhost:24282/dashboard/index.html
```

如果默认端口被占用，会使用更高端口号（24283, 24284...）。

#### 功能特性

1. **实时日志查看**
   - 所有工具调用记录
   - 语言服务器状态
   - 错误和警告信息

2. **工具使用统计**（需在配置中启用）
   ```yaml
   # ~/.serena/serena_config.yml
   record_tool_usage_stats: true
   ```

   显示：
   - 各工具调用次数
   - 执行时间统计
   - 成功/失败率

3. **服务器管理**
   - 查看当前配置
   - 手动关闭服务器
   - 查看活跃项目

#### 为什么需要手动关闭？

Claude Desktop 等客户端在退出时可能无法正确终止子进程，导致 Serena 服务器成为僵尸进程。Dashboard 提供的关闭功能确保资源正确释放。

### GUI 工具（可选）

#### 平台支持

- ✅ **Windows**: 完全支持
- ⚠️ **Linux**: 可能可用（依赖 GTK）
- ❌ **macOS**: 不支持

#### 启用方式

编辑 `~/.serena/serena_config.yml`:

```yaml
# 启用 GUI 工具
enable_gui_tool: true

# 同时可以保留 dashboard
enable_dashboard: true
```

---

## 配置系统详解

### 配置层级

Serena 使用四层配置系统（按优先级从高到低）：

```
1. 命令行参数
   ↓ 覆盖
2. 项目配置 (.serena/project.yml)
   ↓ 覆盖
3. 用户配置 (~/.serena/serena_config.yml)
   ↓ 覆盖
4. 上下文和模式 (内置默认)
```

### 用户级配置

位置: `~/.serena/serena_config.yml`

```yaml
# 编辑命令
# uvx --from git+https://github.com/oraios/serena serena config edit

# ============ 界面配置 ============
enable_dashboard: true
dashboard_port: 24282
enable_gui_tool: false

# ============ 工具配置 ============
record_tool_usage_stats: true

# 包含的可选工具
included_optional_tools:
  - execute_shell_command  # 仅在 desktop-app 上下文
  - initial_instructions   # 旧版 Claude Code

# 排除的默认工具
excluded_tools: []

# ============ 项目列表 ============
projects:
  - name: myproject
    path: /path/to/myproject
    language: python
  - name: webapp
    path: /path/to/webapp
    language: typescript

# ============ 语言服务器配置 ============
language_server_configs:
  python:
    binary_path: null  # null = 自动检测
    additional_args: []

  rust:
    binary_path: ~/.cargo/bin/rust-analyzer
```

### 项目级配置

位置: `<项目根目录>/.serena/project.yml`

```yaml
# 自动生成命令
# uvx --from git+https://github.com/oraios/serena serena project generate-yml

name: myproject

# 语言配置
language: python  # 或 typescript, go, rust, java, etc.

# 忽略规则（类似 .gitignore 语法）
ignore_all_files_in_gitignore: true
ignored_paths:
  - "**/__pycache__/**"
  - "*.pyc"
  - ".venv/**"
  - "dist/**"
  - "build/**"

# 只读模式（禁用所有编辑功能）
read_only: false

# 语言特定配置
language_server_settings:
  python:
    venv_path: .venv
    python_path: .venv/bin/python

  typescript:
    tsconfig: tsconfig.json
```

### 上下文 (Contexts)

定义 Serena 的运行环境和工具集：

| 上下文 | 系统提示 | 工具集 | 使用场景 |
|--------|---------|--------|---------|
| `ide-assistant` | 协作助手模式 | 禁用 shell 和基础编辑 | Claude Code, Cursor, Cline |
| `desktop-app` | 完整代理模式 | 所有工具（含 shell） | Claude Desktop |
| `codex` | Codex 兼容模式 | 兼容性工具集 | OpenAI Codex CLI |
| `agent` | 自主代理模式 | 完整自主工具集 | Agno, 独立脚本 |

**自定义上下文**:

```bash
# 创建自定义上下文
uvx --from git+https://github.com/oraios/serena serena context create my-context

# 编辑
uvx --from git+https://github.com/oraios/serena serena context edit my-context
```

### 模式 (Modes)

运行时行为调整，可以动态切换：

| 模式 | 说明 | 典型组合 |
|-----|------|---------|
| `planning` | 专注规划和分析 | `planning` + `one-shot` |
| `editing` | 专注代码修改 | `editing` + `interactive` |
| `interactive` | 交互式对话 | 默认模式 |
| `one-shot` | 单次完整响应 | 用于报告生成 |
| `no-onboarding` | 跳过 onboarding | 已知项目 |

**动态切换模式**:

```
切换到 planning 和 one-shot 模式
```

---

## 最佳实践

### 1. 项目准备

#### ✅ 做这些

```bash
# 1. 确保 Git 状态干净
git status  # 应该看到 "nothing to commit, working tree clean"

# 2. 索引大型项目
uvx --from git+https://github.com/oraios/serena serena project index

# 3. 配置 .gitignore
echo ".serena/logs/" >> .gitignore

# 4. Windows 用户配置 Git
git config core.autocrlf true
```

#### ❌ 避免这些

- ❌ 在脏 Git 状态下开始大型重构
- ❌ 跳过项目索引（对于大型项目）
- ❌ 将 `.serena/logs/` 提交到版本控制
- ❌ 忽略代码结构问题（巨型文件、God Class）

### 2. 提示词策略

#### 高效使用 Serena 的提示词模式

**❌ 低效提示**:
```
帮我看看 auth.py 这个文件，找到登录相关的代码并修改一下
```
问题：需要读取整个文件，消耗大量 token。

**✅ 高效提示**:
```
使用 find_symbol 找到 auth.py 中的 login 函数，
然后用 replace_symbol_body 添加日志记录功能
```
优势：直接符号操作，token 使用量降低 70%。

#### 分阶段工作流

**第一阶段：规划（planning 模式）**
```
请切换到 planning 和 one-shot 模式

分析这个项目的用户认证系统，生成以下内容：
1. 主要组件和它们的职责
2. 数据流图
3. 安全风险点
4. 改进建议

将分析结果写入记忆，命名为 auth_system_analysis
```

**第二阶段：实施（新会话，editing 模式）**
```
读取 auth_system_analysis 记忆

根据分析结果，实施以下改进：
1. 添加 JWT 令牌验证
2. 实现密码哈希
3. 添加速率限制

每完成一个功能后运行测试
```

### 3. 上下文管理

#### 识别上下文压力信号

- 响应变慢
- 开始遗漏之前的指令
- 重复读取相同内容

#### 应对策略

```python
# 策略 1: 使用记忆系统
"将当前的实现计划写入记忆，命名为 implementation_plan"
# 开始新会话
"读取 implementation_plan 记忆并继续实施"

# 策略 2: 使用准备工具
"使用 prepare_for_new_conversation 工具生成会话摘要"
# 复制摘要到新会话

# 策略 3: 明确指示节省上下文
"只查看函数签名，不要读取函数体"
"使用 get_symbols_overview 而不是 read_file"
```

### 4. 代码质量保障

#### 结构化代码

```python
# ✅ 推荐：模块化、有类型提示
def authenticate_user(
    username: str,
    password: str
) -> Optional[User]:
    """
    Authenticate a user with credentials.

    Args:
        username: User's username
        password: Plain text password

    Returns:
        User object if authentication successful, None otherwise
    """
    # 实现...

# ❌ 避免：巨型函数、无类型提示
def process(data):
    # 500 行代码...
```

Serena 的符号识别依赖清晰的代码结构。

#### 测试驱动开发

```bash
# 最佳实践流程
1. 确保现有测试通过
   pytest tests/

2. 让 Serena 实施修改
   "使用 TDD 方式添加新功能..."

3. Serena 自动运行测试
   （在 desktop-app 上下文中）

4. 迭代直到测试通过
```

#### 日志和调试

```python
# 帮助 Serena 自我纠错的代码
import logging

logger = logging.getLogger(__name__)

def risky_operation():
    try:
        result = perform_operation()
        logger.info(f"Operation successful: {result}")
        return result
    except Exception as e:
        logger.error(f"Operation failed: {e}", exc_info=True)
        raise
```

### 5. 性能优化技巧

#### Token 节省策略

| 操作 | Token 消耗 | 建议 |
|------|-----------|------|
| `read_file(large_file.py)` | 高（~5000） | 使用 `get_symbols_overview` |
| `grep "pattern"` | 高 | 使用 `find_symbol` |
| `find_symbol` + `replace_symbol_body` | 低（~500） | ✅ 首选 |
| 重复读取相同文件 | 浪费 | 使用记忆系统 |

#### 并行化符号查找

```python
# ✅ 高效：让 Serena 并行查找
"同时查找以下符号：
1. UserController 类
2. authenticate 函数
3. validate_token 函数"

# ❌ 低效：串行查找
"先找 UserController"
# 等待响应...
"再找 authenticate"
# 等待响应...
```

---

## 常见问题解决

### 问题 1: 连接失败

**症状**:
```
[ERROR] MCP server "serena" Connection failed
```

**解决方案**:

```bash
# 1. 检查 uv/uvx 是否正确安装
uv --version
uvx --version

# 2. 手动测试 Serena 启动
uvx --from git+https://github.com/oraios/serena serena start-mcp-server --transport stdio

# 应该看到类似输出：
# INFO - Starting MCP server...
# INFO - Loaded tools (36): ...

# 3. Windows 用户：检查路径格式
# 确保使用正斜杠 / 而不是反斜杠 \

# 4. 检查 Claude Code 配置
# ~/.claude.json 中 serena 配置是否正确

# 5. 查看日志
# Windows: %USERPROFILE%\.serena\logs\
# macOS/Linux: ~/.serena/logs/
```

### 问题 2: 工具无法使用

**症状**:
```
Serena 已连接但工具调用失败
```

**解决方案**:

```bash
# 1. 确认项目已激活
"当前激活的项目是什么？"

# 如果未激活：
"激活项目 /path/to/project"

# 2. 检查语言服务器状态
# 在 Dashboard 中查看语言服务器是否正常启动

# 3. 重启语言服务器（如果支持）
"重启语言服务器"

# 4. 验证语言配置
cat .serena/project.yml
# 检查 language 字段是否正确

# 5. 对于 Go/Rust 等，确保依赖已安装
# Go: go install golang.org/x/tools/gopls@latest
# Rust: rustup component add rust-analyzer
```

### 问题 3: 索引失败或缓慢

**症状**:
```
索引耗时过长或中途失败
```

**解决方案**:

```yaml
# 1. 排除不必要的目录
# 编辑 .serena/project.yml
ignored_paths:
  - "node_modules/**"
  - "dist/**"
  - "build/**"
  - ".venv/**"
  - "**/__pycache__/**"
  - "*.min.js"
  - "vendor/**"

# 2. 检查磁盘空间
df -h  # Linux/macOS
# Windows: Get-PSDrive

# 3. 增加索引超时（如果支持）
# language_server_settings:
#   timeout: 300  # 秒

# 4. 手动清理缓存
rm -rf .serena/cache/
```

### 问题 4: Windows 特定问题

#### 换行符问题

**症状**: `git diff` 显示整个文件都变了

**解决**:
```bash
git config --global core.autocrlf true
```

#### 路径解析问题

**症状**: `$(pwd)` 无法识别

**解决**: 使用固定绝对路径
```json
{
  "args": [
    "...",
    "--project",
    "C:/Users/username/project"  // 使用正斜杠
  ]
}
```

#### PowerShell 执行策略

**症状**: 无法运行 uvx 命令

**解决**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 问题 5: Java 语言服务器问题

**症状**: Java 项目启动极慢或超时

**原因**: Eclipse JDT LS 首次启动需要下载依赖和索引

**解决**:

```bash
# 1. 耐心等待首次启动（可能需要 5-10 分钟）

# 2. 确保有 .project 或 pom.xml / build.gradle
ls -la | grep -E 'pom.xml|build.gradle|.project'

# 3. 预先索引（Maven 项目）
mvn dependency:resolve

# 4. 查看详细日志
tail -f ~/.serena/logs/*/mcp_*.txt

# 5. 如果持续失败，临时使用 read_only 模式
# .serena/project.yml
read_only: true
```

### 问题 6: 记忆无法读取

**症状**:
```
"找不到记忆 xxx"
```

**解决**:

```bash
# 1. 检查记忆文件是否存在
ls .serena/memories/

# 2. 列出所有可用记忆
"列出所有记忆"

# 3. 检查文件权限
ls -l .serena/memories/

# 4. 手动创建记忆文件
echo "# 自定义记忆内容" > .serena/memories/my_memory.md

# 5. 重新进行 onboarding
"重新执行项目 onboarding"
```

### 问题 7: Dashboard 无法访问

**症状**: 浏览器无法打开 `http://localhost:24282`

**解决**:

```bash
# 1. 检查端口是否被占用
# macOS/Linux:
lsof -i :24282

# Windows:
netstat -ano | findstr :24282

# 2. 查看实际使用的端口
# 检查 Serena 启动日志
tail ~/.serena/logs/*/mcp_*.txt
# 查找类似: "Dashboard available at http://localhost:24283"

# 3. 防火墙设置
# 确保允许 localhost 连接

# 4. 禁用 Dashboard（如果不需要）
# ~/.serena/serena_config.yml
enable_dashboard: false

# 5. 切换到 GUI 工具（Windows）
enable_gui_tool: true
enable_dashboard: false
```

---

## 社区使用案例

### 案例 1: 大型 Web 应用重构

**背景**: 一个包含 500+ 文件的 Vue.js 项目需要将组件从 Options API 迁移到 Composition API。

**Serena 使用策略**:

```bash
# 1. 项目准备
cd myproject
git checkout -b feature/composition-api-migration
uvx --from git+https://github.com/oraios/serena serena project index

# 2. 第一阶段：分析（planning 模式）
"切换到 planning 和 one-shot 模式

分析项目中所有 Vue 组件，识别：
1. 使用 Options API 的组件列表
2. 组件间的依赖关系
3. 迁移风险评估
4. 推荐的迁移顺序

将分析结果写入记忆 migration_plan"

# 3. 第二阶段：逐步迁移（新会话）
"读取 migration_plan 记忆

按照推荐顺序，从 UserProfile 组件开始迁移到 Composition API：
1. 找到组件定义
2. 转换 data 为 ref/reactive
3. 转换 methods 为独立函数
4. 转换 computed 为 computed()
5. 更新测试
6. 验证功能"

# 4. 批量处理（后续组件）
"继续迁移下一批 5 个低耦合组件：
- ProductCard
- CategoryList
- SearchBar
- PaginationControls
- LoadingSpinner"
```

**结果**:
- Token 使用量比传统方式节省 **65%**
- 迁移过程中代码质量更高（符号精确操作）
- 完成时间从预计 2 周缩短到 **4 天**

### 案例 2: 开源项目贡献

**背景**: 首次贡献到大型 Python 开源项目，需要添加新功能。

**Serena 使用流程**:

```python
# 1. 项目 Onboarding
"对这个项目进行 onboarding，重点了解：
- 项目结构和模块职责
- 贡献指南要求
- 测试流程
- 代码风格规范"

# 2. 功能探索
"使用 find_symbol 找到所有与 'authentication' 相关的类和函数
分析它们的职责和交互方式
生成一个架构图"

# 3. 实施新功能
"根据 contributing.md 的要求，添加 OAuth2 支持：
1. 在合适的位置添加 OAuth2Provider 类
2. 集成到现有认证流程
3. 添加配置选项
4. 编写单元测试
5. 更新文档"

# 4. 代码审查准备
"分析我的修改对现有代码的影响：
1. 找到所有引用了被修改符号的位置
2. 验证向后兼容性
3. 生成修改摘要用于 PR 描述"
```

**社区反馈**:
- PR 质量显著提高，一次性通过审查
- 未引入破坏性变更
- 完整的测试覆盖

### 案例 3: Bug 修复与调试

**背景**: 生产环境报告了一个难以复现的认证 bug。

**Serena 调试流程**:

```bash
# 1. 问题定位
"根据错误日志 'Token验证失败'，使用 Serena 追踪：
1. 找到 validate_token 函数的定义
2. 查找所有调用 validate_token 的位置
3. 分析 token 的生命周期
4. 识别可能的竞态条件"

# 2. 根因分析
"在 find_referencing_symbols 的结果中，发现有两个地方修改 token：
- login_handler (line 45)
- refresh_token_handler (line 120)

分析两者是否存在并发问题"

# 3. 修复实施
"在 validate_token 函数中添加线程锁：
1. 使用 replace_symbol_body 修改函数
2. 添加 threading.Lock 保护
3. 添加调试日志
4. 编写并发测试用例"

# 4. 验证
"运行新增的并发测试 100 次，确保无竞态条件"
```

**成果**:
- 准确定位问题根因
- 修复未引入新 bug
- 添加了防止类似问题的测试

### 案例 4: 代码质量改进

**背景**: 技术债务清理，重构遗留代码。

**Serena 质量审查流程**:

```yaml
# System Prompt for Code Quality Review
角色: 代码质量审查专家

使用 Serena 工具进行系统化审查：

1. 复杂度分析
   - 使用 find_symbol 找到所有函数
   - 识别超过 50 行的函数
   - 标记圈复杂度高的代码

2. 依赖分析
   - 使用 find_referencing_symbols 找到高耦合模块
   - 识别循环依赖
   - 建议解耦方案

3. 重复代码检测
   - 查找相似的函数签名
   - 提取公共逻辑

4. 测试覆盖
   - 找到所有没有对应测试的公共函数
   - 生成测试文件建议

5. 文档完整性
   - 检查所有公共 API 的文档字符串
   - 标记缺失或不完整的文档
```

**实际执行**:

```bash
"按照代码质量审查流程，分析 src/services/ 目录
生成审查报告，包括：
- 高优先级改进项（P0）
- 中优先级改进项（P1）
- 低优先级改进项（P2）
每项包含文件位置、问题描述、改进建议"
```

**结果**:
- 识别 **23 个**高优先级问题
- 重构 **12 个**巨型函数
- 测试覆盖率从 45% 提升到 **78%**
- 代码行数减少 **15%**（通过去重）

---

## 进阶技巧

### 1. 自定义工作流

#### 创建项目专用上下文

```bash
# 创建自定义上下文
uvx --from git+https://github.com/oraios/serena serena context create web-dev

# 编辑配置
# ~/.serena/web-dev.yml
```

```yaml
# web-dev.yml - Web 开发专用上下文
name: web-dev
description: "Web 开发专用配置"

system_prompt: |
  你是一个专业的 Web 开发助手，使用 Serena 进行：
  - 前后端代码分析
  - API 设计和实现
  - 数据库 schema 管理
  - 性能优化

  工作原则：
  - 优先使用 TypeScript 类型安全
  - 遵循 RESTful API 设计规范
  - 所有 API 必须有错误处理
  - 数据库操作使用事务

excluded_tools:
  - execute_shell_command  # 禁用 shell（由宿主处理）

included_optional_tools:
  - initial_instructions
```

#### 使用自定义上下文

```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context web-dev --project $(pwd)
```

### 2. 多项目管理

#### 配置多项目环境

```yaml
# ~/.serena/serena_config.yml
projects:
  - name: frontend
    path: /home/user/work/webapp-frontend
    language: typescript

  - name: backend
    path: /home/user/work/webapp-backend
    language: python

  - name: mobile
    path: /home/user/work/mobile-app
    language: swift
```

#### 快速切换项目

```bash
# 在 Claude Code 对话中
"激活项目 backend"
# 工作一段时间后
"激活项目 frontend"
```

### 3. 集成其他 MCP 服务器

Serena 可以与其他 MCP 服务器协同工作：

```json
// ~/.claude.json 或 Claude Desktop 配置
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": [
        "--from", "git+https://github.com/oraios/serena",
        "serena", "start-mcp-server",
        "--context", "ide-assistant",
        "--project", "/path/to/project"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-api-key"
      }
    }
  }
}
```

**协同场景**:
- **Serena** - 代码理解和编辑
- **filesystem** - 额外的文件系统操作
- **brave-search** - 在线文档查询

---

## 性能对比数据

### Token 使用量对比（社区数据）

| 操作场景 | 传统方式 | 使用 Serena | 节省比例 |
|---------|---------|------------|---------|
| 查找函数定义 | ~3000 tokens | ~500 tokens | **83%** |
| 修改单个函数 | ~5000 tokens | ~800 tokens | **84%** |
| 重构模块 | ~15000 tokens | ~4000 tokens | **73%** |
| Bug 修复（含追踪） | ~8000 tokens | ~2000 tokens | **75%** |
| 代码审查 | ~20000 tokens | ~6000 tokens | **70%** |

**平均节省**: **70-75%** token

### 速度提升

| 项目规模 | 未索引首次调用 | 索引后首次调用 | 后续调用 |
|---------|--------------|--------------|---------|
| 小型 (< 100 文件) | 5-10秒 | 1-2秒 | < 1秒 |
| 中型 (100-500 文件) | 20-40秒 | 2-5秒 | < 1秒 |
| 大型 (500-2000 文件) | 60-120秒 | 5-10秒 | 1-2秒 |
| 超大型 (> 2000 文件) | 120+秒 | 10-20秒 | 2-3秒 |

**建议**: 文件数 > 100 的项目务必进行索引。

---

## 社区资源

### 官方资源

- **GitHub**: [oraios/serena](https://github.com/oraios/serena)
- **文档**: README.md（英文）
- **更新日志**: [CHANGELOG.md](https://github.com/oraios/serena/blob/main/CHANGELOG.md)
- **路线图**: [roadmap.md](https://github.com/oraios/serena/blob/main/roadmap.md)

### 视频教程

- **AI Labs**: [Claude Code 性能优化](https://www.youtube.com/watch?v=wYWyJNs1HVk)
- **中文教程**: [Cursor+Serena 最佳组合](https://www.youtube.com/watch?v=DZ-gLebVnmg)
- **实战演示**: [Website Bug 修复](https://www.youtube.com/watch?v=pQiEymVgihU)

### 博客文章

- [Serena 架构解析（英文）](https://medium.com/@souradip1000/deconstructing-serenas-mcp-powered-semantic-code-understanding-architecture-75802515d116)
- [Claude Code 深度体验（中文）](https://blog.csdn.net/lovely_yoshino/article/details/149152190)
- [Serena 完整教程（中文）](https://leekoko.com/blog/serena-mcp-complete-guide)

### 常见 Issues

参考 [GitHub Issues](https://github.com/oraios/serena/issues) 中的常见问题：

- [#494 - Claude Code 连接失败](https://github.com/oraios/serena/issues/494)
- [#568 - 配置问题汇总](https://github.com/oraios/serena/issues/568)
- [#486 - Linux ARM64 配置](https://github.com/oraios/serena/issues/486)

---

## 总结

### 何时使用 Serena

✅ **强烈推荐的场景**:
- 大型项目（> 100 文件）
- 复杂代码库重构
- 跨模块功能实现
- 代码审查和质量改进
- 开源项目贡献

⚠️ **可选场景**:
- 中小型项目（10-100 文件）
- 单文件脚本
- 快速原型开发

❌ **不推荐场景**:
- 全新项目从零开始（结构尚未形成）
- 非常小的修改（< 10 行）
- 纯文本文件处理

### 核心价值总结

1. **Token 经济性** - 节省 70%+ token 使用量
2. **精确性** - 符号级操作，减少错误
3. **可维护性** - 结构化修改，保持代码质量
4. **学习曲线** - 理解项目结构更快
5. **免费开源** - 无订阅费用，社区驱动

### 下一步行动

```bash
# 1. 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 在项目中添加 Serena
cd /path/to/your/project
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project $(pwd)

# 3. 索引项目（可选但推荐）
uvx --from git+https://github.com/oraios/serena serena project index

# 4. 开始使用！
"使用 Serena 分析这个项目的代码结构"
```

---

## 附录：完整工具清单

### 默认工具（18个）

| 工具名 | 类别 | 说明 |
|-------|------|------|
| `find_symbol` | 符号查询 | 全局/局部符号搜索 |
| `find_referencing_symbols` | 符号查询 | 查找符号引用 |
| `get_symbols_overview` | 符号查询 | 文件符号概览 |
| `replace_symbol_body` | 符号编辑 | 替换符号定义 |
| `insert_after_symbol` | 符号编辑 | 符号后插入 |
| `insert_before_symbol` | 符号编辑 | 符号前插入 |
| `read_file` | 文件操作 | 读取文件 |
| `create_text_file` | 文件操作 | 创建/覆盖文件 |
| `list_dir` | 文件操作 | 列出目录 |
| `find_file` | 文件操作 | 查找文件 |
| `search_for_pattern` | 文件操作 | 文本搜索 |
| `replace_regex` | 文件操作 | 正则替换 |
| `write_memory` | 记忆系统 | 写入记忆 |
| `read_memory` | 记忆系统 | 读取记忆 |
| `list_memories` | 记忆系统 | 列出记忆 |
| `delete_memory` | 记忆系统 | 删除记忆 |
| `onboarding` | 项目管理 | 项目学习 |
| `check_onboarding_performed` | 项目管理 | 检查学习状态 |

### 可选工具（上下文相关）

| 工具名 | 默认状态 | 启用上下文 |
|-------|---------|-----------|
| `execute_shell_command` | 禁用 | `desktop-app`, `agent` |
| `initial_instructions` | 禁用 | 手动启用（旧版 Claude Code） |
| `restart_language_server` | 禁用 | 手动启用 |
| `delete_lines` | 禁用 | 手动启用 |
| `replace_lines` | 禁用 | 手动启用 |
| `insert_at_line` | 禁用 | 手动启用 |

---

**文档版本**: v1.0 (2025-10)
**贡献者**: 基于社区使用经验和官方文档整理
**反馈**: 欢迎在 [GitHub Issues](https://github.com/oraios/serena/issues) 提出建议

---

希望这份文档能帮助您充分发挥 Serena 的强大能力！🚀
