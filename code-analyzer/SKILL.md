---
name: code-analyzer
description: This skill should be used when performing shift-left testing and pre-deployment code reviews. It analyzes Git diffs to detect defects (SQL injection, N+1 queries, etc.), validates requirement implementation, determines impact scope, and generates comprehensive test analysis reports. Supports Java + SpringBoot, Python, JavaScript/TypeScript + Node.js, Flutter + Dart, and Kotlin + Android. Trigger phrases include "分析提交", "代码审查", "提测检查", "回归范围分析".
license: Apache-2.0
---

# Code Analyzer - 精准测试代码审查工具

**测试左移工具** - 在提测前识别问题,确定回归测试范围,输出测试分析报告。

## 设计理念

```
Git 提交变更 → 缺陷检测 + 需求验证 + 影响分析 → 测试分析报告
```

**职责定位**:

- 面向测试工程师,不是开发代码质量工具
- 关注提测前最后一道防线
- 自动化确定回归测试范围

## 多角色协作框架 (DEPTH: D)

Generate comprehensive test analysis through expert role collaboration:

**Test Analyst**:
- Parse Git diff and identify changed files/methods
- Analyze impact scope and determine regression test range
- Evaluate risk level and prioritize testing efforts

**Security Reviewer**:
- Detect security vulnerabilities (SQL injection, XSS, etc.)
- Identify sensitive information leakage
- Verify authentication and authorization logic

**Code Quality Inspector**:
- Detect code quality issues (NPE, resource leaks, etc.)
- Identify performance problems (N+1 queries)
- Check exception handling and error management

**Requirements Validator**:
- Compare code changes against requirement specifications
- Identify missing or incomplete implementations
- Detect business logic errors

## 核心功能

基于 Git diff 分析代码变更:

1. 🔍 **缺陷识别** - N+1查询、SQL注入、空指针、事务失效等常见缺陷
2. 🎯 **需求验证** - 代码是否实现需求,是否有多余实现
3. 📊 **影响范围** - 直接影响/间接影响模块,确定回归测试范围
4. ⚠️ **风险评估** - 高/中/低风险分级,提供测试优先级建议
5. 📝 **测试报告** - 结构化测试分析报告,面向测试工程师

## 使用场景

**目标用户**: 测试工程师、测试开发、研发人员(提测前自查)

**典型场景**:

```
测试工程师收到提测单:
  - 开发说: "登录功能优化完成,可以测试了"
  - 使用 code-analyzer 分析近期提交
  - 查看报告:
    ✓ 发现2个SQL注入风险
    ✓ 发现1个N+1查询问题
    ✓ 影响3个模块: 登录、用户、订单
    ✓ 回归范围: 需重测登录、用户信息、订单创建
  - 结果: 打回开发修复缺陷,避免测试浪费
```

## 触发条件

```
分析本分支近3次提交

需求: 用户登录优化
【需求描述】
支持手机号+验证码登录,保留原有用户名密码登录...
```

或者:

```
分析 feature/login 分支的提交

需求: 登录优化
...
```

## 工作流程

### 步骤 0: 背景信息收集 (DEPTH: P)

Before analyzing code changes, collect essential context:

**Required Information**:
1. **Requirement Description**: Detailed requirement or feature description
2. **Git Range**: Specify branch or commit range to analyze (e.g., `HEAD~5..HEAD`, `feature/login`)
3. **Analysis Depth**: Quick scan or comprehensive analysis
4. **Priority Focus**: Security/Performance/Functionality

**Information Gathering**:
- When requirement is provided: Extract key features and expected behaviors
- When context is unclear: Ask for clarification
- When analyzing branch: Automatically determine commit range

### 步骤 1: 代码变更提取

**Test Analyst Role**:

提取 Git diff 变更信息,识别修改的文件和方法。

**详细流程**: @references/workflows/step1-code-change.md

### 步骤 2: 技术栈识别

**Test Analyst Role**:

自动识别项目技术栈,加载对应缺陷检测规则。

| 技术栈 | 识别特征 | 规则模板 |
|--------|---------|---------|
| Java + SpringBoot | pom.xml + @SpringBootApplication | @templates/java-springboot/ |
| Python | requirements.txt / pyproject.toml / setup.py | @templates/python/ |
| JavaScript/TypeScript + Node.js | package.json + Node modules | @templates/javascript-typescript/ |
| Flutter + Dart | pubspec.yaml + .dart 文件 | @templates/flutter-dart/ |
| Kotlin + Android | build.gradle + .kt 文件 + AndroidManifest.xml | @templates/kotlin-android/ |

> 🚀 **扩展性**: 架构支持多语言扩展,详见 @ARCHITECTURE.md "扩展示例"

**详细流程**: @references/workflows/step2-techstack-detect.md

### 步骤 3: 缺陷检测 (DEPTH: T)

**Security Reviewer & Code Quality Inspector Roles**:

按技术栈规则检测常见缺陷(N+1、SQL注入等):

**Task Breakdown**:
1. **Security Vulnerabilities**: SQL injection, XSS, command injection, sensitive data exposure
2. **Resource Management**: Resource leaks, connection management, file handling
3. **Error Handling**: Exception handling, Promise rejections, error propagation
4. **Concurrency Issues**: Race conditions, thread safety, async/await problems
5. **Performance**: N+1 queries, inefficient algorithms, memory leaks
6. **Type Safety**: Type annotations, null/undefined checks, type conversions

**详细流程**: @references/workflows/step3-defect-detect.md

**检测规则**: 根据技术栈加载对应规则
- Java + SpringBoot: @templates/java-springboot/defect-rules.md
- Python: @templates/python/defect-rules.md
- JavaScript/TypeScript: @templates/javascript-typescript/defect-rules.md
- Flutter + Dart: @templates/flutter-dart/defect-rules.md
- Kotlin + Android: @templates/kotlin-android/defect-rules.md

### 步骤 4: 需求验证

**Requirements Validator Role**:

对比需求文档和代码实现,识别未实现/多余实现。

**详细流程**: @references/workflows/step4-requirement-verify.md

### 步骤 5: 影响范围分析

**Test Analyst Role**:

使用 Serena MCP 追踪调用链,确定回归测试范围。

**详细流程**: @references/workflows/step5-impact-analysis.md

**MCP 集成**: @references/integrations/serena-mcp.md

### 步骤 6: 风险评估与报告生成 (DEPTH: E)

**Test Analyst Role**:

综合评估风险等级,生成测试分析报告。

**Success Criteria**:
1. **Defect Coverage**: All critical security and quality issues identified
2. **Requirement Compliance**: All requirement features validated
3. **Impact Analysis**: Complete regression test scope determined
4. **Risk Assessment**: Accurate risk level and priority assigned
5. **Report Quality**: Clear, actionable recommendations provided

**详细流程**: @references/workflows/step6-report-generate.md

**报告格式**: @references/specs/report-format.md

### 步骤 7: 自我评估 (DEPTH: H)

**All Roles**:

Before finalizing the report, perform self-evaluation:

**Analysis Completeness Check**:
- All changed files analyzed?
- All code patterns checked against defect rules?
- Requirement features fully validated?
- Impact scope comprehensively traced?

**Quality Assurance**:
- Defect descriptions clear and具体?
- Fix recommendations actionable?
- Regression test scope reasonable?
- Risk assessment justified?

**Technical Accuracy**:
- Security vulnerabilities correctly identified?
- Code quality issues accurately detected?
- Requirement validation logically sound?
- No false positives in critical findings?

**Report Usability**:
- Organized for test engineers?
- Key findings highlighted?
- Recommendations prioritized?
- Examples and evidence provided?

**Action on Assessment**:
- If critical issues missed: Review analysis steps
- If report unclear: Improve explanations and structure
- If passed: Finalize and output report

## 输出

**测试分析报告** 保存到被分析项目的根目录:

```
{被分析项目根目录}/analysis-reports/{需求名称}/{分支名}-{日期时间}.md
```

**示例**:
```
实际项目: /home/user/myproject/
报告路径: /home/user/myproject/analysis-reports/用户登录优化/feature-login-20251026-153022.md
```

**报告内容**:

- 📋 基本信息(分支、提交、文件数)
- 🔍 缺陷清单(严重度分级)
- 🎯 需求实现情况
- 📊 影响范围分析
- ⚠️ 回归测试建议
- 💡 测试重点建议

## 技术栈支持

当前支持 5 种主流技术栈:

### Java + SpringBoot

识别特征:
- 存在 `pom.xml` 或 `build.gradle`
- 包含 `spring-boot-starter` 依赖
- 代码中有 `@SpringBootApplication` 注解

缺陷规则: @templates/java-springboot/defect-rules.md

### Python

识别特征:
- 存在 `requirements.txt`, `pyproject.toml`, 或 `setup.py`
- `.py` 文件
- 常见框架导入 (FastAPI, Django, Flask)

缺陷规则: @templates/python/defect-rules.md

### JavaScript/TypeScript + Node.js

识别特征:
- 存在 `package.json`
- `.js`, `.ts`, `.jsx`, `.tsx` 文件
- Node.js 模块 (`require`, `import`)

缺陷规则: @templates/javascript-typescript/defect-rules.md

### Flutter + Dart

识别特征:
- 存在 `pubspec.yaml`
- `.dart` 文件
- Flutter SDK 依赖
- 常见包 (get, dio, hive)

缺陷规则: @templates/flutter-dart/defect-rules.md

**MagicFrame App 特定**:
- GetX 状态管理
- Dio 网络请求
- Hive 本地存储
- Firebase Analytics

### Kotlin + Android

识别特征:
- 存在 `build.gradle` (kotlin-android plugin)
- `.kt` 文件
- `AndroidManifest.xml`
- 常见库 (androidx, coroutines, room)

缺陷规则: @templates/kotlin-android/defect-rules.md

**MagicFrame Android 特定**:
- Repository + ViewModel 架构
- Room 数据库
- Coroutines + Flow
- MQTT IoT 消息处理
- WorkManager 后台任务

## MCP 工具集成

### Serena MCP 🔴 必需

**用途**:

- 代码索引(首次使用自动建立)
- 依赖分析(调用链、影响范围)
- 缺陷扫描(语义级检测)

**智能索引**:

- 首次: 自动全量索引(2-5分钟)
- 后续: 增量更新(10-30秒)

### Sequential MCP 🟡 推荐

**用途**:

- 需求验证推理
- 影响范围推导
- 风险评估决策

详细说明: @references/integrations/serena-mcp.md, @references/integrations/sequential-mcp.md

## 缺陷检测能力

### 通用缺陷类型 (所有语言)

**🔴 Blocker (阻断级)**:
- ✅ **SQL 注入** - 字符串拼接构造 SQL
- ✅ **命令注入** - 不安全的系统命令执行
- ✅ **敏感信息泄露** - 硬编码密码、密钥

**🟠 Critical (严重级)**:
- ✅ **资源泄漏** - 未正确关闭资源
- ✅ **不安全的反序列化** - 可执行任意代码

**🟡 Major (重要级)**:
- ✅ **异常处理不当** - 异常吞没、未处理
- ✅ **并发问题** - 竞态条件、线程安全
- ✅ **类型错误** - 类型注解缺失或不正确

**🟢 Minor (次要级)**:
- ✅ **N+1 查询** - 循环中执行数据库查询
- ✅ **性能问题** - 低效算法、内存泄漏

**功能缺陷检测**:
- ✅ **功能完全缺失** - 需求要求的功能未实现
- ✅ **功能实现不完整** - 缺少逻辑分支或边界条件
- ✅ **业务逻辑错误** - 流程顺序错误、规则实现错误

### 语言特定缺陷

**Java + SpringBoot**:
- NPE 风险、事务失效、Spring 特定问题
- 详细规则: @templates/java-springboot/defect-rules.md

**Python**:
- eval/exec 代码注入、pickle 反序列化、类型提示缺失
- 详细规则: @templates/python/defect-rules.md

**JavaScript/TypeScript**:
- XSS、原型污染、Promise 未处理、TypeScript any 滥用
- 详细规则: @templates/javascript-typescript/defect-rules.md

## 报告示例

### 示例 1: Java SpringBoot 项目

```markdown
# 测试分析报告: 用户登录优化

## 📋 基本信息

- 分支: feature/login-opt
- 技术栈: Java + SpringBoot
- 提交数: 3 次
- 变更文件: 8 个
- 分析时间: 2025-10-26 15:30

## 🔴 发现缺陷(3个)

### 高风险(2个)

**1. SQL 注入风险**

- 文件: `UserRepository.java:78`
- 代码: `String sql = "SELECT * FROM user WHERE name = '" + name + "'";`
- 影响: 恶意输入可绕过认证
- 建议: 使用参数化查询 `@Query("... WHERE name = :name")`

**2. N+1 查询问题**

- 文件: `OrderService.java:45`
- 代码: 循环中调用 `userRepository.findById()`
- 影响: 性能严重下降
- 建议: 使用批量查询 `findAllById()`

### 中风险(1个)

**3. 事务可能失效**

- 文件: `UserService.java:23`
- 问题: 同类内部调用 @Transactional 方法
- 建议: 拆分到不同 Service 或注入自身代理

## 🎯 需求实现情况

✅ **已实现**(2/3)

- ✅ 支持手机号登录
- ✅ 支持验证码登录

❌ **未实现**(1/3)

- ❌ 第三方登录(微信、支付宝)

## 📊 影响范围分析

**直接影响模块**(3个):

- `UserController` - 新增手机号登录接口
- `UserService` - 登录逻辑变更
- `SmsService` - 验证码发送

**间接影响模块**(2个):

- `OrderController` - 调用了 UserService
- `AdminController` - 调用了 UserService

**回归测试建议范围**:

1. ✅ 登录功能(用户名密码登录、手机号登录)
2. ✅ 用户信息查询
3. ✅ 订单创建(依赖登录态)
4. ⚠️ 管理后台登录(受影响但优先级低)

## ⚠️ 风险评估

**综合风险等级**: 🔴 高风险

**原因**:

- 存在2个高风险缺陷(SQL注入、N+1查询)
- 核心登录逻辑变更,影响面大
- 未实现部分需求

**测试建议**:

1. **优先**: 修复SQL注入和N+1查询问题
2. **重点**: 全面测试登录功能(各种场景)
3. **回归**: 测试订单、用户信息等依赖模块
4. **补充**: 确认第三方登录是否必需

## 💡 测试重点

1. **安全测试**: SQL注入、XSS、认证绕过
2. **性能测试**: 大量用户并发登录
3. **功能测试**: 手机号登录各种场景(验证码过期、重复发送等)
4. **兼容测试**: 原有用户名密码登录不受影响
```

### 示例 2: Python 项目

```markdown
# 测试分析报告: API 安全加固

## 📋 基本信息

- 分支: feature/api-security
- 技术栈: Python + FastAPI
- 提交数: 4 次
- 变更文件: 6 个
- 分析时间: 2025-10-26 16:45

## 🔴 发现缺陷(3个)

### 高风险(2个)

**1. SQL 注入风险**

- 文件: `api/users.py:23`
- 代码: `query = f"SELECT * FROM users WHERE email = '{email}'"`
- 影响: 恶意输入可窃取数据
- 建议: 使用参数化查询 `cursor.execute("SELECT * FROM users WHERE email = %s", (email,))`

**2. 敏感信息泄露**

- 文件: `config.py:12`
- 代码: `DATABASE_URL = "postgresql://admin:password123@localhost/db"`
- 影响: 密码泄露
- 建议: 使用环境变量 `os.getenv("DATABASE_URL")`

### 中风险(1个)

**3. 资源泄漏**

- 文件: `utils/file_handler.py:34`
- 代码: `file = open("data.json", "r")` 未关闭
- 影响: 文件描述符耗尽
- 建议: 使用 `with open("data.json") as file:`

## 🎯 需求实现情况

✅ **已实现**(3/3)

- ✅ API 认证机制
- ✅ 输入验证
- ✅ 错误处理优化

## 📊 影响范围分析

**直接影响模块**(2个):

- `api/users.py` - 用户查询接口
- `api/auth.py` - 认证逻辑

**回归测试建议范围**:

1. ✅ 用户登录/注册
2. ✅ API 认证
3. ✅ 数据查询接口

## ⚠️ 风险评估

**综合风险等级**: 🔴 高风险

**原因**:

- SQL注入和敏感信息泄露为阻断级缺陷
- 核心认证逻辑变更

**测试建议**:

1. **优先**: 修复 SQL 注入和密码泄露
2. **重点**: 安全测试(SQL注入、认证绕过)
3. **补充**: 验证环境变量配置正确
```

### 示例 3: JavaScript/TypeScript 项目

```markdown
# 测试分析报告: 前端表单优化

## 📋 基本信息

- 分支: feature/form-validation
- 技术栈: TypeScript + React + Node.js
- 提交数: 5 次
- 变更文件: 10 个
- 分析时间: 2025-10-26 17:20

## 🔴 发现缺陷(4个)

### 高风险(2个)

**1. XSS 漏洞**

- 文件: `components/UserProfile.tsx:45`
- 代码: `dangerouslySetInnerHTML={{ __html: user.bio }}`
- 影响: 恶意脚本执行
- 建议: 使用 DOMPurify 清理: `DOMPurify.sanitize(user.bio)`

**2. 命令注入风险**

- 文件: `api/export.ts:67`
- 代码: `exec(\`pdfgen ${filename}\`)`
- 影响: 服务器被控制
- 建议: 使用 `execFile("pdfgen", [filename])`

### 中风险(2个)

**3. Promise 未处理拒绝**

- 文件: `api/orders.ts:89`
- 代码: `app.post("/order", async (req, res) => { const order = await createOrder(...) })`
- 影响: 未捕获错误导致进程崩溃
- 建议: 添加 `try/catch` 或使用 `next(error)`

**4. TypeScript any 滥用**

- 文件: `utils/validation.ts:23`
- 代码: `function processData(data: any): any`
- 影响: 类型安全丢失
- 建议: 定义接口 `interface FormData { ... }`

## 🎯 需求实现情况

✅ **已实现**(2/2)

- ✅ 表单验证逻辑
- ✅ 错误提示优化

## 📊 影响范围分析

**直接影响模块**(3个):

- `components/UserProfile.tsx` - 用户资料显示
- `api/export.ts` - 导出功能
- `api/orders.ts` - 订单处理

**回归测试建议范围**:

1. ✅ 用户资料编辑和显示
2. ✅ 数据导出功能
3. ✅ 订单创建流程

## ⚠️ 风险评估

**综合风险等级**: 🔴 高风险

**原因**:

- XSS 和命令注入为阻断级安全漏洞
- 涉及前后端关键功能

**测试建议**:

1. **优先**: 修复 XSS 和命令注入
2. **重点**: 安全测试(XSS、命令注入、输入验证)
3. **回归**: 表单提交、数据导出完整流程测试
4. **补充**: TypeScript 类型检查(开启 strict 模式)
```

## 使用示例

### 示例 1: 分析近期提交

```
分析本分支近5次提交

需求: 支付流程优化
优化支付流程,支持微信、支付宝、银行卡三种支付方式...
```

**执行流程**:

1. 解析 Git 范围: `HEAD~5..HEAD`
2. Serena 索引检查(如需要则自动索引)
3. 分析变更 + 识别缺陷 + 影响分析
4. 生成报告: `./analysis-reports/支付流程优化/feature-payment-20251026-153022.md`

### 示例 2: 分析特定分支

```
对比 feature/cache 和 main 分支

需求: 引入 Redis 缓存,优化查询性能
```

## 注意事项

1. **首次使用**: Serena MCP 需要建立索引,耗时 2-5 分钟
2. **需求文档**: 提供详细需求可提高验证准确度
3. **报告位置**: 在**被分析项目的根目录**下的 `analysis-reports/` 目录(不是 skill 目录)
4. **技术栈**: 支持 Java + SpringBoot, Python, JavaScript/TypeScript + Node.js, Flutter + Dart, Kotlin + Android
5. **语言混用**: 项目包含多种语言时,自动应用所有适用规则
6. **MagicFrame 项目**: 针对 magic_frame_app (Flutter) 和 magic_frame_android (Kotlin) 有专门的检测规则

## 资源引用

### 工作流程文档

- 代码变更提取: @references/workflows/step1-code-change.md
- 技术栈识别: @references/workflows/step2-techstack-detect.md
- 缺陷检测: @references/workflows/step3-defect-detect.md
- 需求验证: @references/workflows/step4-requirement-verify.md
- 影响范围分析: @references/workflows/step5-impact-analysis.md
- 报告生成: @references/workflows/step6-report-generate.md

### 缺陷检测规则

- Java + SpringBoot: @templates/java-springboot/defect-rules.md
- Python: @templates/python/defect-rules.md
- JavaScript/TypeScript: @templates/javascript-typescript/defect-rules.md
- Flutter + Dart: @templates/flutter-dart/defect-rules.md
- Kotlin + Android: @templates/kotlin-android/defect-rules.md

### MCP 集成说明

- Serena MCP: @references/integrations/serena-mcp.md
- Sequential MCP: @references/integrations/sequential-mcp.md

---

**版本**: 1.0.0
**创建**: 2025-10-27
**定位**: 测试左移工具,提测前代码审查
