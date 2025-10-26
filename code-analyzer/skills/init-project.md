---
name: init-project
description: code-analyzer 项目初始化子 Skill - 扫描项目结构,识别技术栈,建立 Serena 索引,生成项目上下文
parent: code-analyzer
---

# init-project - 项目初始化

**职责**: 首次使用 code-analyzer 时,建立项目上下文。

## 触发条件

### 自动触发

- `.code-analyzer/project-context.json` 不存在时,自动调用

### 手动触发

```
触发词:
- "初始化项目"
- "建立代码索引"
- "首次使用 code-analyzer"
```

## 工作流程

### Step 1: 扫描项目结构

**目标**: 识别项目类型和构建工具

**检查文件**:

```bash
# Java 项目
ls pom.xml build.gradle

# Python 项目
ls requirements.txt setup.py pyproject.toml manage.py

# Node.js 项目
ls package.json
```

**输出**:

```
项目类型: Java
构建工具: Maven
项目根目录: /path/to/project
```

### Step 2: 识别技术栈

**加载模板注册表**: @templates/registry.json

**匹配逻辑**:

```
for each template in registry:
  检查 detect_files 是否存在
  检查 detect_pattern 是否匹配
  如果匹配 → 加载该模板
```

**示例** (Java + SpringBoot):

```bash
# 检查文件
pom.xml 存在? ✓

# 检查模式
grep -q "spring-boot-starter" pom.xml
匹配? ✓

# 加载模板
techstack: java-springboot
template_path: templates/java-springboot/
```

**输出**:

```
技术栈: Java + SpringBoot 3.2.0
模板路径: templates/java-springboot/
```

### Step 3: 扫描核心包

**Java 项目**:

```bash
# 查找 Controller 包
find src -name "*Controller.java" | head -1 | xargs dirname

# 查找 Service 包
find src -name "*Service.java" | head -1 | xargs dirname

# 查找 Repository 包
find src -name "*Repository.java" | head -1 | xargs dirname

# 查找 Entity 包
find src -name "*Entity.java" -o -name "*DTO.java" | head -1 | xargs dirname
```

**输出**:

```
核心包:
- Controller: com.example.controller (8 个文件)
- Service: com.example.service (12 个文件)
- Repository: com.example.repository (6 个文件)
- Entity: com.example.entity (10 个文件)
```

### Step 4: 建立 Serena 索引

**检查 Serena 状态**:

```
Serena 查询: "检查当前项目是否已建立索引"
```

**创建索引**:

```
Serena 命令: "为当前项目创建代码索引"
```

**提示用户**:

```
正在建立 Serena 索引...
预计耗时: 2-5 分钟
请稍候...
```

**输出**:

```
Serena 索引:
- 状态: ✅ 已完成
- 耗时: 3分15秒
- 索引文件: 36 个
- 索引行数: 8,542 行
- 索引时间: 2025-10-26 10:30:00
```

### Step 5: 生成项目上下文

**汇总信息**:

```json
{
  "project_name": "user-service",
  "project_path": "/path/to/project",
  "techstack": "java-springboot",
  "framework_version": "3.2.0",
  "build_tool": "maven",
  "modules": ["user-service"],
  "key_packages": {
    "controller": "com.example.controller",
    "service": "com.example.service",
    "repository": "com.example.repository",
    "entity": "com.example.entity"
  },
  "serena_indexed": true,
  "last_index_time": "2025-10-26 10:30:00",
  "template_path": "templates/java-springboot/",
  "created_at": "2025-10-26 10:30:00"
}
```

**保存到文件**:

```bash
mkdir -p .code-analyzer
echo '{...}' > .code-analyzer/project-context.json
```

**输出位置**: `.code-analyzer/project-context.json`

### Step 6: 输出初始化报告

生成 Markdown 格式的初始化报告:

```markdown
# 项目初始化完成 ✅

## 项目信息

- **项目名称**: user-service
- **项目路径**: /path/to/project
- **技术栈**: Java + SpringBoot 3.2.0
- **构建工具**: Maven
- **模块数量**: 1 个

## 核心包结构

- **Controller**: `com.example.controller` (8 个文件)
- **Service**: `com.example.service` (12 个文件)
- **Repository**: `com.example.repository` (6 个文件)
- **Entity**: `com.example.entity` (10 个文件)

## Serena 索引

- **状态**: ✅ 已完成
- **耗时**: 3分15秒
- **索引文件**: 36 个
- **索引行数**: 8,542 行
- **索引时间**: 2025-10-26 10:30:00

## 项目上下文

已保存到: `.code-analyzer/project-context.json`

## 缺陷检测规则

已加载: `templates/java-springboot/defect-rules.md`

支持检测:
- ✅ SQL 注入
- ✅ N+1 查询
- ✅ 事务失效
- ✅ 空指针风险
- ✅ 资源泄漏
- ✅ 异常吞没
- ✅ 敏感信息泄露
- ✅ 循环依赖

## 下一步

现在可以使用 `code-analyzer` 分析提交了:

\`\`\`
分析本分支近3次提交

需求: 用户登录优化
支持手机号+验证码登录,保留原有用户名密码登录...
\`\`\`
```

## MCP 工具使用

### Serena MCP

**索引创建**:

```
Serena 命令: "为当前项目创建代码索引"
```

**索引检查**:

```
Serena 查询: "检查当前项目索引状态"
```

## 输出文件

### .code-analyzer/project-context.json

**格式**: JSON

**内容**: 项目元信息

**用途**: 后续分析时读取,避免重复扫描

**示例**: @examples/project-context.json

## 技术栈特定逻辑

每个技术栈的初始化逻辑定义在:

```
templates/{techstack}/init.md
```

**示例**:

- Java + SpringBoot: @templates/java-springboot/init.md
- Python + Django: @templates/python-django/init.md
- Node.js + Express: @templates/nodejs-express/init.md

## 注意事项

1. **首次耗时**: Serena 索引需要 2-5 分钟,请耐心等待
2. **项目编译**: 确保项目可正常编译,否则索引可能失败
3. **依赖完整**: 确保项目依赖已安装 (mvn install / npm install)
4. **本地操作**: 所有操作在本地完成,不上传到云端

## 常见问题

**Q: 如何重新初始化?**

A: 删除 `.code-analyzer/project-context.json` 后重新调用。

**Q: 如果识别错技术栈怎么办?**

A: 手动编辑 `project-context.json`,修改 `techstack` 字段。

**Q: 多模块项目如何处理?**

A: 当前版本在项目根目录初始化,支持多模块识别。

## 集成到主 Skill

在 `code-analyzer` 主 Skill 中:

```markdown
### 前置检查

在执行分析前,自动检查项目上下文:

1. 检查 `.code-analyzer/project-context.json` 是否存在
2. 如果不存在 → 自动调用 `init-project` 子 Skill
3. 如果存在 → 读取上下文,继续分析
```

---

**版本**: 1.0.0
**父 Skill**: code-analyzer
**更新**: 2025-10-26
