---
name: test-case-generator
description: 根据需求文档生成完整的测试用例体系。This skill should be used when users need to generate comprehensive test cases from requirement documents, including test point extraction, module organization, and quality validation. Supports PRD parsing, test point decomposition, parallel test case generation, and quality review.
license: Proprietary
---

# 测试用例生成器

## 概述

根据需求文档自动生成结构化的测试用例体系（JSONL 格式），包含测试点拆分、用例生成、质量审查和多格式导出。

## 适用场景

当用户提供需求文档并需要：
- 生成系统化的测试点和测试用例
- 按模块组织测试用例
- 导出为 JSONL/XMind 格式
- 进行测试覆盖度分析

## 输出结构

```
需求名称/
├── prd.md                    # 规范化需求文档
├── test-points.jsonl         # 测试点文件
├── cases/                    # [中间态] 各模块用例
│   ├── 用户注册.jsonl
│   ├── 用户登录.jsonl
│   └── ...
├── cases.jsonl               # 合并后的测试用例
├── cases.xmind               # XMind 思维导图
└── stats-report.md           # 统计报告
```

## Schema 定义

### 测试点 Schema

```typescript
interface TestPoint {
  id: string;                  // 格式："TP-001"
  module_name: string;         // 测试项（被测对象），≤15字符
  name: string;                // 测试场景名称
  scene: string;               // 场景描述，1-2 句话
  check: string;               // 验证点，1-2 句话
  tags: string[];              // 标签列表
  business_value: "高" | "中" | "低";
}
```

**标签定义**：
- 功能重要性：核心功能、基本功能、不常用功能
- 场景类型：正向场景、边界场景、异常场景、性能场景、安全场景

**示例**：
```jsonl
{"id":"TP-001","module_name":"用户注册","name":"正常注册流程","scene":"用户首次使用系统，输入正确的用户名和密码进行注册","check":"系统成功创建新用户账号","tags":["核心功能","正向场景"],"business_value":"高"}
{"id":"TP-002","module_name":"用户登录","name":"密码错误处理","scene":"用户输入正确的用户名但密码错误","check":"系统提示密码错误，记录失败次数","tags":["核心功能","异常场景"],"business_value":"高"}
```

### 测试用例 Schema

```typescript
interface TestCase {
  id: string;                  // 格式："TC-001"
  name: string;                // 用例名称（主谓宾格式）
  module_name: string;         // 测试项（被测对象），≤15字符
  test_point_name: string;     // 测试场景
  priority: "P1" | "P2" | "P3" | "P4" | "P5";
  test_type: string;           // 测试类型（13种）
  is_negative: boolean;        // 是否反向用例
  preconditions: string[];     // 前置条件
  steps: Array<{
    action: string;            // 操作步骤
    expected: string;          // 预期结果
  }>;
  notes?: string;              // 备注（可选）
}
```

**示例**：
```jsonl
{"id":"TC-001","name":"验证用户成功登录系统","module_name":"用户登录","test_point_name":"正常登录流程","priority":"P1","test_type":"功能测试","is_negative":false,"preconditions":["系统已部署","存在有效账号"],"steps":[{"action":"打开登录页面","expected":"页面正常显示"},{"action":"输入正确的用户名密码","expected":"输入成功"},{"action":"点击登录按钮","expected":"登录成功，跳转主页"}],"notes":"核心功能正向用例"}
```

## 优先级定义

| 优先级 | 定义 | 示例 |
|-------|-----|-----|
| P1 | 核心功能正向测试（冒烟） | 用户登录成功 |
| P2 | 基本功能正向测试 | 修改个人信息 |
| P3 | 核心功能反向测试（错误/边界） | 密码错误登录失败 |
| P4 | 基本功能反向测试（异常/边界） | 头像格式错误 |
| P5 | 不常用功能正反向测试 | 管理员导出报表 |

详细说明参见 `references/priority-guide.md`

## 测试类型

| 类别 | 测试类型 | 说明 |
|-----|---------|-----|
| 基础 | 功能测试 | 验证功能正确性 |
| 基础 | 易用性测试 | 验证用户体验 |
| 基础 | 兼容性测试 | 验证跨环境运行 |
| 基础 | 性能测试 | 验证性能指标 |
| 基础 | 安全性测试 | 验证安全防护 |
| 基础 | 稳定性测试 | 验证长期运行 |
| 基础 | 集成测试 | 验证模块协作 |
| 扩展 | 可靠性测试 | 验证故障恢复 |
| 扩展 | 可维护性测试 | 验证运维能力 |
| 扩展 | 可移植性测试 | 验证迁移能力 |
| 扩展 | 埋点测试 | 验证数据上报 |
| 扩展 | AI效果测试 | 验证 AI 输出 |
| 扩展 | 硬件效果测试 | 验证硬件交互 |

详细说明参见 `references/test-type-guide.md`

## 工作流程

### Step 1: 需求文档解析

1. 读取需求文档（Markdown/Word/PDF）
2. 识别需求疑问点和模糊描述
3. 与用户交互确认需求细节
4. 生成规范化的 prd.md

**疑问识别维度**：
- 术语不一致（同一概念多种叫法）
- 需求模糊（"快速响应"具体多少秒？）
- 逻辑矛盾（A 功能和 B 功能冲突）
- 缺失信息（边界值、异常处理未定义）

**引导式提问格式**：

发现疑问后，使用以下格式向用户确认：

```markdown
## 需求确认

在分析需求文档时，发现以下 {N} 个待确认点：

### 1. [模块名] - [问题类型]
**原文**："{引用需求原文}"
**疑问**：{具体问题描述}
**建议选项**：
- A: {选项A}
- B: {选项B}
- C: 其他（请说明）

### 2. [模块名] - [问题类型]
...

请逐一确认，或告诉我哪些需要进一步讨论。
```

**提问原则**：
- 每次最多提 5 个问题，避免信息过载
- 提供选项而非开放式提问，降低用户负担
- 按模块分组，便于用户定位
- 用户确认后，更新 prd.md 并标注"[已确认]"

### Step 2: 测试点拆分

使用 Think Harder 进行深度分析，按以下思考链逐步拆解：

**思考链框架**：

```
1. 模块提取
   └─ 从 prd.md 中列出所有功能模块
   └─ 示例：用户注册、用户登录、个人信息、权限管理...

2. 逐模块分析（对每个模块问自己）
   ├─ 正向场景：用户正常使用时会怎么操作？
   ├─ 边界场景：输入的边界值是什么？（最大/最小/空值）
   ├─ 异常场景：可能出现什么错误？如何处理？
   ├─ 性能场景：是否需要并发/压力测试？
   └─ 安全场景：是否涉及认证、注入、越权？

3. 业务价值评估
   ├─ 高：核心业务流程（登录、支付、下单）
   ├─ 中：辅助功能（修改信息、查询记录）
   └─ 低：边缘功能（高级设置、管理员报表）

4. 标签组合
   └─ 功能重要性 × 场景类型 = 测试点标签
   └─ 示例：["核心功能", "异常场景"]
```

**拆分原则**：
- 每个模块至少覆盖 1 个正向 + 1 个异常场景
- 核心模块（业务价值=高）需覆盖全部 5 种场景类型
- 测试点粒度：1 个场景 = 1 个测试点，不要合并

**输出**：test-points.jsonl

### Step 3: 测试用例生成

基于测试点生成详细测试用例：

1. 每个测试点生成 1-3 条用例
2. 设计具体操作步骤和预期结果
3. 判断优先级和测试类型
4. 标记是否为反向用例

**并发策略**：

使用 Task agent 并行生成，按完整模块分配（最多 6 个 agent）：

```
1. 模块分组
   ├─ 将测试点按 module_name 分组，得到 M 个模块
   ├─ 每个模块必须完整分配给同一个 agent（不可拆分）
   └─ agent 数量 N = min(M, 6)

2. 分配策略
   ├─ M ≤ 6：每个 agent 负责 1 个模块
   ├─ M > 6：将模块平均分配，每个 agent 负责多个完整模块
   └─ 为每个 agent 分配 ID 段（每段 200 个）：
      - Agent 1: TC-001 ~ TC-200
      - Agent 2: TC-201 ~ TC-400
      - ...

3. 并行执行
   └─ 同时启动 N 个 Task agent，使用下方任务模板

4. 收集结果
   └─ 各 agent 输出到 cases/{module_name}.jsonl
```

**Task Agent 任务模板**：

```markdown
## 任务：测试用例生成

### 上下文
以下是规范化的需求文档（仅包含你负责的模块相关内容）：
{prd_module_section}

### 输入
- 负责模块：{module_names}
- 该模块的测试点：
{test_points_jsonl}
- ID 范围：TC-{start} ~ TC-{end}

### 要求
1. 为每个测试点生成 1-3 条测试用例
2. 用例名称使用主谓宾格式，以"验证"开头
3. 根据 priority-guide.md 判断优先级（P1-P5）
4. 根据 test-type-guide.md 选择测试类型
5. 反向用例（异常/边界场景）标记 is_negative: true
6. 每条用例包含 2-5 个步骤，每步骤有 action 和 expected
7. 步骤和预期结果要具体，避免"正常"、"成功"等模糊描述

### 输出格式
输出到 `cases/{module_name}.jsonl`，每行一条用例，严格遵循 TestCase Schema：
{"id":"TC-xxx","name":"...","module_name":"...","test_point_name":"...","priority":"Px","test_type":"...","is_negative":false,"preconditions":[...],"steps":[{"action":"...","expected":"..."}]}

### 注意
- ID 必须在分配范围内，顺序递增
- 每个模块单独一个文件，便于审查和追溯
- 只输出 JSONL 数据，不要输出解释
```

### Step 4: 质量审查

对各 agent 输出的模块文件进行审查（合并前）：

**4.1 格式验证**（使用脚本）

```bash
# 验证所有模块文件
python scripts/validate_jsonl.py cases/*.jsonl --strict
```

**4.2 AI 手动检查清单**

逐项检查并修复问题：

```markdown
## 质量检查清单

### 1. ID 重复检查（并发问题）
□ 检查是否有重复的 TC-xxx ID
□ 检查 ID 是否在各 agent 分配范围内
□ 修复方法：重新编号冲突的 ID

### 2. 测试点覆盖检查（遗漏问题）
□ 列出 test-points.jsonl 中所有 test_point_name
□ 检查 cases/*.jsonl 中每个 test_point_name 是否都有对应用例
□ 遗漏的测试点需补充用例
□ 输出：覆盖率 = 已覆盖测试点数 / 总测试点数

### 3. 格式规范检查
□ 用例名称是否以"验证"开头（主谓宾格式）
□ module_name 是否 ≤15 字符
□ steps 是否至少有 1 条，每条有 action 和 expected
□ preconditions 是否为数组格式

### 4. 业务逻辑检查
□ 优先级是否合理（P1 占比 10-20%）
□ 反向用例是否标记 is_negative: true
□ test_type 是否与场景匹配（安全场景→安全性测试）

### 5. 内容质量检查
□ 步骤描述是否具体可执行（避免"正确操作"等模糊描述）
□ 预期结果是否可验证（避免"正常"等模糊描述）
□ 前置条件是否完整
```

**检查结果报告**：

```markdown
## 质量审查报告

- 总用例数：{N}
- ID 重复：{N} 处（已修复 / 待修复）
- 测试点覆盖率：{X}%（{covered}/{total}）
- 遗漏测试点：{list}
- 格式问题：{N} 处
- 优先级分布：P1({x}%) P2({x}%) P3({x}%) P4({x}%) P5({x}%)

### 待修复问题
1. ...
2. ...
```

### Step 5: 合并与导出

**5.1 合并测试用例**

```bash
python scripts/merge_jsonl.py cases/*.jsonl -o cases.jsonl --sort-by module
```

**5.2 导出 XMind 思维导图**

```bash
python scripts/convert_to_xmind.py cases.jsonl -o cases.xmind --name "{需求名称}"
```

**5.3 生成统计报告**

```bash
python scripts/stats_report.py cases.jsonl --test-points test-points.jsonl -o stats-report.md
```

**5.4 输出确认**

```markdown
## 导出完成

已生成以下文件：
- cases/（{M} 个模块文件，中间态）
- cases.jsonl（{N} 条用例，合并后）
- cases.xmind（思维导图）
- stats-report.md（统计报告）

请查收。
```

## 工具脚本

### validate_jsonl.py

验证 JSONL 文件格式和内容。

```bash
python scripts/validate_jsonl.py test-points.jsonl
python scripts/validate_jsonl.py cases.jsonl --strict
```

### merge_jsonl.py

合并多个 JSONL 文件。

```bash
python scripts/merge_jsonl.py cases/*.jsonl -o cases.jsonl
```

### convert_to_xmind.py

将 JSONL 转换为 XMind 思维导图。

```bash
# 基本转换
python scripts/convert_to_xmind.py cases.jsonl -o cases.xmind

# 指定根节点名称
python scripts/convert_to_xmind.py cases.jsonl -o cases.xmind --name "用户管理"

# 扁平模式（跳过测试点层级）
python scripts/convert_to_xmind.py cases.jsonl -o cases.xmind --flat
```

**依赖**：`pip install xmind`

**思维导图结构**：
```
根节点
├── 模块 (module_name)
│   └── 测试点 (test_point_name)
│       └── 用例 [优先级图标]
│           ├── 测试项
│           ├── 前置条件
│           ├── 步骤 1
│           │   └── 预期结果 1
│           └── 备注
```

### stats_report.py

生成统计报告。

```bash
python scripts/stats_report.py cases.jsonl -o stats-report.md
```

## 用例名称规范

用例名称应按**主谓宾格式**表达：

| 正确示例 | 错误示例 |
|---------|---------|
| 验证用户成功登录系统 | 登录测试 |
| 验证密码错误时登录失败 | 密码错误 |
| 验证系统防止SQL注入 | SQL注入测试 |

## 成功标准

1. **文档完整性**：
   - prd.md（规范化需求）
   - test-points.jsonl（测试点）
   - cases/（各模块用例，中间态）
   - cases.jsonl（合并后用例）
   - cases.xmind（思维导图）
   - stats-report.md（统计报告）
2. **测试覆盖度**：所有测试点都有对应测试用例，覆盖率 100%
3. **用例质量**：步骤清晰、预期明确、无模糊描述
4. **格式规范**：通过 JSON Schema 验证，无 ID 重复

## 注意事项

1. 发现需求疑问时必须与用户确认，不可擅自修改
2. 用例 ID 必须全局唯一
3. 用例名称按主谓宾格式，不含 ID
4. 优先级按功能重要性和场景类型综合判断
5. 测试类型从 13 种中选择最匹配的一种
