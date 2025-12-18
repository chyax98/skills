---
name: test-case-generator
description: 从需求文档生成结构化测试用例。按模块逐个生成并即时校验，独立审查查漏补缺，输出 JSONL/Excel/XMind 格式。触发词：生成测试用例、需求转用例、测试用例生成。
---

# 测试用例生成器

**执行要求**：严格按 Step 1 → 2 → 3 → 4 顺序执行

## 输出结构

```
./                                # 当前工作目录
└── {需求名称}/                    # 工作区（自动创建）
    ├── modules.jsonl             # Step 1: 模块规划
    ├── cases/                    # Step 2: 各模块用例
    │   ├── M01-用户登录.jsonl
    │   └── ...
    ├── cases.jsonl               # Step 4: 合并后用例
    ├── cases.xlsx                # Step 4: Excel 格式
    ├── cases.xmind               # Step 4: XMind 格式
    ├── review-report.md          # Step 3: 审查报告
    └── stats-report.md           # Step 4: 统计报告
```

**输入**：需求文档（用户提供路径）

**工作区命名**：从文档标题提取，如 `# 用户管理系统` → 工作区为 `./用户管理系统/`

---

## Step 1: 需求理解与规划

**执行者**：主 Agent（不可委托）

**输入**：需求文档

**处理流程**：

1. **读取需求文档**，理解完整业务
2. **划分功能模块**（≤8 个），按功能内聚、边界清晰原则
3. **识别测试项**：
   - 每个用户可执行的操作 = 1 个测试项
   - 每个系统自动行为 = 1 个测试项
   - 每个 CRUD 操作 = 各 1 个测试项
   - 每个关键业务规则 = 1 个测试项
4. **评估业务价值**：高（核心流程）/ 中（辅助功能）/ 低（边缘功能）
5. **规划生成顺序**：基础模块优先，被依赖方先生成
6. **分配 module_id**：M01, M02, M03...
7. **提取模块 prd**：该模块的需求原文
8. **输出 modules.jsonl**

**Module Schema**：
```typescript
interface Module {
  module_id: string;           // M01, M02, ...
  module_name: string;         // ≤15 字符
  order: number;               // 生成顺序
  test_items: Array<{
    item: string;              // 测试项名称
    business_value: "高" | "中" | "低";
  }>;
  prd: string;                 // 该模块需求原文
}
```

**输出示例**：
```jsonl
{"module_id":"M01","module_name":"用户登录","order":1,"test_items":[{"item":"账号密码登录","business_value":"高"},{"item":"手机验证码登录","business_value":"高"}],"prd":"## 用户登录\n支持账号密码和手机验证码两种登录方式..."}
```

**Step 1 完成后**：使用 TodoWrite 创建各模块的生成任务

---

## Step 2: 逐模块生成用例

**执行者**：主 Agent（不可委托，保持全局上下文）

**前置准备**：
- 首次生成前，读取 `{skill_dir}/assets/cases.jsonl` 了解用例格式示例

**核心循环**：

```python
for module in sorted(modules, key=lambda m: m.order):
    # 1. 更新 TodoWrite：标记当前模块 in_progress

    # 2. 场景分析
    scenarios = analyze_scenarios(module)

    # 3. 生成用例
    cases = generate_cases(module, scenarios)

    # 4. 写入 cases/{module_id}-{module_name}.jsonl

    # 5. 即时检验（编码+格式+覆盖）
    issues = validate_module()

    # 6. 有问题则修复，循环直到通过
    while issues:
        fix_issues(issues)
        issues = validate_module()

    # 7. 更新 TodoWrite：标记当前模块 completed
```

### 场景分析维度

| 场景类型 | 分析内容 | 覆盖要求 |
|---------|---------|---------|
| 正向场景 | 正常流程，合法输入 | **所有测试项必须** |
| 边界场景 | 最大/最小/空值/长度边界 | **所有测试项必须** |
| 异常场景 | 错误输入、失败处理 | **所有测试项必须** |
| 性能场景 | 并发、大数据量 | 需求有要求时 |
| 安全场景 | 认证、授权、注入防护 | 涉及敏感操作时 |

**场景覆盖策略**：
- 核心功能（business_value=高）：正向 + 边界 + 异常 + 性能/安全（如适用）
- 辅助功能（business_value=中）：正向 + 边界 + 异常
- 边缘功能（business_value=低）：正向 + 主要异常

---

### 优先级判定规则

| 业务价值 | 场景类型 | 优先级 | 说明 |
|---------|---------|-------|------|
| 高 | 正向场景 | **P1** | 核心功能冒烟测试，每次构建必测 |
| 高 | 异常/边界 | **P3** | 核心功能健壮性，版本回归必测 |
| 中 | 正向场景 | **P2** | 基本功能验证，每日回归 |
| 中 | 异常/边界 | **P4** | 基本功能健壮性，完整回归 |
| 低 | 任意场景 | **P5** | 不常用功能，发布前测试 |

**优先级分布目标**：P1(10-20%) P2(25-35%) P3(20-30%) P4(15-25%) P5(5-10%)

> 如需了解更多优先级判定示例和特殊场景处理，读取 `{skill_dir}/assets/priority-guide.md`

---

### 测试类型

本 skill 主要生成**功能测试**用例，非功能测试（安全、性能等）按需补充。

| 测试类型 | 适用场景 |
|---------|---------|
| **功能测试** | 业务逻辑验证（主体） |
| 安全性测试 | 认证授权、攻击防护 |
| 性能测试 | 响应时间、并发能力 |
| 易用性测试 | 用户体验、界面交互 |
| 兼容性测试 | 跨环境运行 |
| 稳定性测试 | 长期运行稳定性 |
| 集成测试 | 模块间协作 |
| 可靠性测试 | 故障恢复、容错 |
| 可维护性测试 | 运维能力 |
| 可移植性测试 | 跨平台迁移 |
| 埋点测试 | 数据上报 |
| AI效果测试 | AI模型输出 |
| 硬件效果测试 | 硬件交互 |

> 详细说明和示例见 `{skill_dir}/assets/test-type-guide.md`

---

### TestCase Schema

```typescript
interface TestCase {
  id: string;                  // M01-001 格式
  name: string;                // 以"验证"开头，主谓宾格式
  module_name: string;         // ≤15 字符
  test_item: string;           // 所属测试项（与 modules.jsonl 中 item 匹配）
  priority: "P1" | "P2" | "P3" | "P4" | "P5";
  test_type: string;           // 主要是"功能测试"
  is_negative: boolean;        // 异常/边界场景 = true，正向场景 = false
  preconditions: string[];     // 前置条件（具体明确）
  steps: Array<{
    action: string;            // 操作步骤（具体可执行）
    expected?: string;         // 预期结果（可选，仅在需要验证时填写）
  }>;
  notes?: string;              // 备注（可选）
}
```

---

### 用例生成规范

**ID 格式**：`{module_id}-{seq:03d}`（如 M01-001, M01-002）

**用例名称**：主谓宾格式，以"验证"开头
```
✅ 验证用户使用正确密码成功登录系统
✅ 验证用户输入错误密码时登录失败并提示错误信息
✅ 验证系统拒绝超过20字符的用户名
❌ 登录测试
❌ 密码错误
```

### 可执行性原则

生成**黑盒测试用例**，确保测试人员可执行：

| 要素 | 要求 | 正确 | 错误 |
|-----|------|------|------|
| 步骤 | 基于界面/系统入口操作 | "点击提交按钮" | "调用 API 接口" |
| 预期 | 通过界面可验证的结果 | "提示'保存成功'" | "数据库插入记录" |
| 验证 | 不依赖查代码/日志/数据库 | "列表显示新数据" | "检查后台日志" |

**禁止生成**：
- 步骤涉及：调用接口、执行 SQL、查看代码、修改配置文件
- 预期涉及：数据库字段值、日志内容、缓存状态、接口响应码

---

**步骤描述**：具体可执行，避免模糊

**预期结果原则**：只在验证点写预期，过渡步骤省略
```
✅ action: "打开登录页面"
   （无预期 - 过渡步骤）

✅ action: "输入用户名 testuser"
   （无预期 - 过渡步骤）

✅ action: "输入密码 Test@123456"
   （无预期 - 过渡步骤）

✅ action: "点击登录按钮"
   expected: "登录成功，跳转到系统首页，显示用户昵称"
   （有预期 - 这是验证点）

✅ action: "输入21个字符的用户名 abcdefghijklmnopqrstu"
   expected: "提示\"用户名长度不能超过20字符\""
   （有预期 - 边界验证点）

❌ action: "输入用户名 testuser"
   expected: "用户名输入框显示 testuser"
   （废话 - 不需要验证输入框能显示）

❌ action: "输入正确的用户名"
   expected: "正常显示"
   （模糊 - action 和 expected 都不具体）
```

**前置条件**：具体明确
```
✅ "系统已部署并可正常访问"
✅ "存在测试账号 testuser/Test@123456"
✅ "用户已登录系统"
✅ "购物车中有商品"
❌ "系统正常"
❌ "用户已登录"（缺少具体账号信息）
```

---

### 用例示例

```jsonl
# 正向用例
{"id":"M01-001","name":"验证用户使用正确密码成功登录系统","module_name":"用户登录","test_item":"账号密码登录","priority":"P1","test_type":"功能测试","is_negative":false,"preconditions":["系统已部署并可正常访问","存在测试账号 testuser/Test@123456"],"steps":[{"action":"打开系统登录页面"},{"action":"输入用户名 testuser"},{"action":"输入密码 Test@123456"},{"action":"点击登录按钮","expected":"登录成功，跳转到系统首页，显示用户昵称"}]}

# 反向用例（异常）
{"id":"M01-002","name":"验证用户输入错误密码时登录失败","module_name":"用户登录","test_item":"账号密码登录","priority":"P3","test_type":"功能测试","is_negative":true,"preconditions":["系统已部署并可正常访问","存在测试账号 testuser/Test@123456"],"steps":[{"action":"打开系统登录页面"},{"action":"输入用户名 testuser"},{"action":"输入错误密码 wrongpassword"},{"action":"点击登录按钮","expected":"登录失败，提示\"用户名或密码错误\""}]}

# 反向用例（边界）
{"id":"M01-003","name":"验证系统拒绝超过20字符的用户名","module_name":"用户登录","test_item":"账号密码登录","priority":"P3","test_type":"功能测试","is_negative":true,"preconditions":["系统已部署并可正常访问"],"steps":[{"action":"打开系统登录页面"},{"action":"输入21个字符的用户名 abcdefghijklmnopqrstu"},{"action":"点击登录按钮","expected":"提示\"用户名长度不能超过20字符\""}]}

# 安全测试用例
{"id":"M01-010","name":"验证系统防止SQL注入攻击","module_name":"用户登录","test_item":"账号密码登录","priority":"P1","test_type":"安全性测试","is_negative":true,"preconditions":["系统已部署并可正常访问"],"steps":[{"action":"打开系统登录页面"},{"action":"在用户名输入框输入 ' OR '1'='1"},{"action":"输入任意密码"},{"action":"点击登录按钮","expected":"登录失败，返回正常错误提示，不会绕过认证"}]}
```

---

### 即时检验（每个模块必做）

```bash
# 1. 编码检查（必须无乱码）
grep -n '�' cases/{module}.jsonl
# 无输出 = 通过；有输出 = 显示行号，必须修复

# 2. 格式校验
python {skill_dir}/scripts/validate.py cases/{module}.jsonl --strict

# 3. 覆盖检查（人工确认）
# - 该模块每个 test_item 是否都有用例？
# - 是否至少有 1 个正向 + 1 个异常/边界？
```

### 断点恢复

```
如果中途中断：
1. 检查 cases/ 目录，确认已完成的模块
2. 检查 TodoWrite 状态
3. 从下一个未完成的模块继续
已生成的 .jsonl 文件不会丢失
```

---

## Step 3: 全量审查

**执行者**：Task Agent（主 Agent 启动）

**目的**：脚本扫描发现可疑点，Agent 裁决是否需要修复

**启动方式**：

```python
Task(
    subagent_type="general-purpose",
    prompt=read_file("{skill_dir}/assets/review-prompt.md")
           .replace("{workspace}", workspace_path)
           .replace("{skill_dir}", skill_dir_path)
)
```

**审查流程**：
1. **脚本扫描**：`validate.py --strict --audit --modules` 输出待审查项
2. **Agent 裁决**：逐项判断是否需要修复
3. **输出报告**：`{workspace}/review-report.md`

---

## Step 4: 合并与导出

**执行者**：主 Agent + 脚本

```bash
# 1. 最终格式检验
python {skill_dir}/scripts/validate.py {workspace}/cases/*.jsonl --strict

# 2. 合并所有模块
python {skill_dir}/scripts/merge.py {workspace}/cases/*.jsonl \
    -o {workspace}/cases.jsonl --sort-by module

# 3. 导出 Excel
python {skill_dir}/scripts/to_excel.py {workspace}/cases.jsonl \
    -o {workspace}/cases.xlsx

# 4. 导出 XMind（可选）
python {skill_dir}/scripts/to_xmind.py {workspace}/cases.jsonl \
    -o {workspace}/cases.xmind --name "{需求名称}"

# 5. 生成统计报告
python {skill_dir}/scripts/stats.py {workspace}/cases.jsonl \
    --modules {workspace}/modules.jsonl -o {workspace}/stats-report.md
```

**输出确认**：

```markdown
## 生成完成

| 文件 | 说明 |
|------|------|
| modules.jsonl | 模块规划（N 个模块） |
| cases/*.jsonl | 各模块用例（中间产物） |
| cases.jsonl | 合并用例（N 条） |
| cases.xlsx | Excel 格式 |
| cases.xmind | XMind 思维导图 |
| review-report.md | 审查报告 |
| stats-report.md | 统计报告 |
```

---

## 质量检查清单

### 完整性
- [ ] 每个 test_item 至少 1 正向 + 1 异常/边界
- [ ] 核心功能（business_value=高）覆盖更多场景

### 格式规范
- [ ] ID 格式 `{module_id}-{seq:03d}`，连续无跳号
- [ ] 用例名称以"验证"开头
- [ ] test_item 与 modules.jsonl 中的 item 匹配
- [ ] priority 为 P1-P5
- [ ] test_type 为上述 13 种之一
- [ ] steps 至少 1 条，至少 1 条有 expected
- [ ] `grep -n '�' cases/*.jsonl` 无乱码

### 内容质量
- [ ] 步骤具体可执行，预期可验证
- [ ] 黑盒可执行：步骤基于界面，预期通过界面可验证，无需查库/看日志
- [ ] 禁用词：正确、正常、合适、成功、失败、应该
- [ ] 反向用例标记 is_negative: true

---

## 成功标准

| 指标 | 目标值 |
|------|-------|
| 测试项覆盖率 | 100% |
| 场景覆盖 | 每个测试项至少 1 正向 + 1 异常/边界 |
| 格式校验 | 0 错误 |
| 编码检查 | 0 乱码 |
| 优先级分布 | 合理即可 |

---

## 工具脚本

**环境**：Python 3.9+，依赖 `jsonschema`、`xmind`、`openpyxl`

**路径**：脚本在 `{skill_dir}/scripts/`，使用绝对路径调用

| 脚本 | 功能 |
|-----|------|
| validate.py | 验证格式 + 审查模式（`--audit` 输出待审查项） |
| merge.py | 合并多个 JSONL 文件 |
| to_excel.py | 转换为 Excel |
| to_xmind.py | 转换为 XMind 思维导图 |
| stats.py | 生成统计报告 |

---

## 按需读取的参考文档

以下文档在特定场景下读取，不要一开始就全部加载：

| 文档 | 读取时机 | 内容 |
|------|---------|------|
| `assets/priority-guide.md` | 判定优先级时遇到特殊场景 | 优先级判定决策树、特殊场景处理、常见错误 |
| `assets/test-type-guide.md` | 选择测试类型时需要更多指导 | 各测试类型详细说明和更多示例 |
| `assets/cases.jsonl` | Step 2 首次生成前 | 完整的用例格式示例（10条） |
| `assets/modules.jsonl` | Step 1 需要模块规划示例时 | 模块规划格式示例 |
| `assets/review-prompt.md` | Step 3 启动审查 Agent 时 | 审查 Agent 的完整提示词 |

---

## 注意事项

1. **主 Agent 执行 Step 1、2、4**，只有 Step 3 使用 Task Agent
2. **用例 ID 全局唯一**，模块前缀保证天然无冲突
3. **每个模块生成后立即检验**，不要等到最后
4. **保持全局上下文**，生成时参考前面模块的风格
5. **断点可恢复**，已生成的文件不会丢失
6. **按需读取参考文档**，不要一开始就加载所有 assets
