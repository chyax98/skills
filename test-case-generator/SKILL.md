---
name: test-case-generator
description: 基于规范化需求文档（prd.md）生成完整测试用例体系。采用轻量级测试项识别 + 重量级并发用例生成的策略，支持场景分析、模块组织、质量审查和多格式导出。适用于已规范化的需求文档（建议先使用 requirement-tester 预处理）。
license: Proprietary
---

# 测试用例生成器

## 概述

根据规范化的需求文档（prd.md）自动生成结构化的测试用例体系（JSONL 格式），包含测试项识别、场景分析、用例生成、质量审查和多格式导出。

**核心设计**：
- **轻量级测试项识别**：快速提取需要测试的功能项，作为并发分配基准
- **重量级用例生成**：并发执行场景分析（正向/边界/异常/性能/安全）和用例生成
- **单一职责**：专注于用例生成，不处理需求质量问题

## 执行流程（必读）

**你（主 Agent）必须自己执行以下步骤，不可整体委托给 Task Agent**

```
Step 1: 你自己执行测试项识别 → 输出 test-items.jsonl
    ↓
Step 2: 你启动多个 Task Agent 并行生成用例 → 输出 cases/*.jsonl
    ↓
Step 3: 你自己执行质量审查 → 验证格式和内容
    ↓
Step 4: 你自己执行合并与导出 → 输出 cases.jsonl + stats-report.md
```

**严格禁止**：
- ❌ **禁止把整个工作流（Step 1-4）委托给一个 Task Agent**
- ❌ **禁止跳过 Step 1 直接生成 cases/*.jsonl**

**你的职责**：
- ✅ **Step 0**：用需求文档名称（去掉 .md）创建输出目录
- ✅ **Step 1**：你必须自己读取 prd.md，自己识别测试项，自己写 `{需求名称}/test-items.jsonl`
- ✅ **Step 2**：你读取 test-items.jsonl，计算并发数，启动多个 Task Agent（每个负责 2-3 个模块）
- ✅ **Step 3**：你自己执行质量审查
- ✅ **Step 4**：你自己执行合并导出

**只有 Step 2 才使用 Task Agent**，其他步骤你必须自己完成。

## 适用场景

当用户提供**已规范化的需求文档（prd.md）**并需要：
- 生成系统化的测试用例
- 按模块组织测试用例
- 导出为 JSONL/XMind 格式
- 进行测试覆盖度分析

### 前置条件
- **必需输入**：prd.md（已规范化，推荐使用 requirement-tester 预处理）
- **输入质量要求**：
  - 功能模块清晰可识别
  - 业务规则描述完整
  - 异常处理有说明（如已通过 requirement-tester 处理）

### 配置选项
- 范围与规模：预估测试项和用例数量
- 质量目标：优先级分布（P1 10–20%、反向≥15%）
- 导出需求：是否生成 XMind/统计报告
- 并发策略：是否启用并行（测试项 > 5 时建议启用）

## 输出结构

**第一步：用需求名称创建目录**

假设需求文档是 `/path/to/Polaris 差旅报销中台.md`，你必须先创建目录 `/path/to/Polaris 差旅报销中台/`

然后所有产物放在这个目录下：

```
/path/to/
├── Polaris 差旅报销中台.md      # 需求文档（输入）
└── Polaris 差旅报销中台/         # 创建的输出目录
    ├── test-items.jsonl          # 测试项文件（轻量级）
    ├── cases/                    # [中间态] 各模块用例
    │   ├── 报销单创建.jsonl
    │   ├── 费用审批.jsonl
    │   └── ...
    ├── cases.jsonl               # 合并后的测试用例
    ├── cases.xmind               # XMind 思维导图（可选）
    └── stats-report.md           # 统计报告
```

**关键**：
- ✅ 用需求文档名称（去掉 .md）创建目录
- ✅ 所有产物放在这个目录下
- ❌ 不要直接在需求文档所在目录生成文件（会混乱）

## Schema 定义

### 测试项 Schema（轻量级）

```typescript
interface ModuleTestItems {
  module_id: string;           // 模块ID，格式：M01, M02, M03...（用于用例ID前缀）
  module_name: string;         // 功能模块，≤15字符
  test_items: Array<{
    item: string;              // 测试项名称
    business_value: "高" | "中" | "低";
  }>;
  prd: string;                 // 该模块的需求详情
}
```

**说明**：
- **按模块分组**：test-items.jsonl 每行代表一个模块
- **module_id**：自动生成（M01-M99），用于用例 ID 前缀（如 M01-001）
- **test_items**：该模块包含的所有测试项
- **prd**：该模块的完整需求内容（供 Sub Agent 理解业务）
- 场景分析（正向/边界/异常/性能/安全）在 Step 2 并发执行

**示例**：
```jsonl
{"module_id":"M01","module_name":"用户注册","test_items":[{"item":"用户注册流程","business_value":"高"},{"item":"手机号验证","business_value":"高"}],"prd":"## 用户注册\n用户可以通过手机号或邮箱注册账号..."}
{"module_id":"M02","module_name":"用户登录","test_items":[{"item":"用户登录流程","business_value":"高"},{"item":"密码找回","business_value":"中"}],"prd":"## 用户登录\n支持用户名、手机号、邮箱三种方式登录..."}
```

### 测试用例 Schema

```typescript
interface TestCase {
  id: string;                  // 格式："{module_id}-{seq:03d}"，如 M01-001
  name: string;                // 用例名称（主谓宾格式）
  module_name: string;         // 测试项（被测对象），≤15字符
  test_item: string;           // 所属测试项（对应 TestItem.item）
  scenario_type: string;       // 场景类型（正向/边界/异常/性能/安全）
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

**ID 编号规则**：
- 格式：`{module_id}-{seq:03d}`
- 每个模块独立编号（M01-001, M01-002... M02-001, M02-002...）
- 天然无冲突，无需预分配 ID 段

**示例**：
```jsonl
{"id":"M01-001","name":"验证用户成功登录系统","module_name":"用户登录","test_item":"用户登录流程","scenario_type":"正向场景","priority":"P1","test_type":"功能测试","is_negative":false,"preconditions":["系统已部署","存在有效账号"],"steps":[{"action":"打开登录页面","expected":"页面正常显示"},{"action":"输入正确的用户名密码","expected":"输入成功"},{"action":"点击登录按钮","expected":"登录成功，跳转主页"}],"notes":"核心功能正向用例"}
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

### 角色分工
- **测试项识别者**：从 prd.md 提取功能清单，评估业务价值
- **用例设计者**：场景分析、用例生成（含并发协调）
- **QA 复核者**：运行校验脚本、执行质量清单、触发修正动作

### Step 1: 测试项识别（轻量级，单线程）

**目标**：快速提取"需要测试的功能清单"，作为并发分配基准

**执行流程**：

1. **读取 prd.md**，提取功能模块和业务规则
2. **识别测试项**（每个独立的功能点/业务规则）：
   ```
   识别规则：
   - 每个用户可执行的操作 = 1 个测试项
   - 每个系统自动触发的行为 = 1 个测试项
   - 每个数据实体的 CRUD 操作 = 各 1 个测试项
   - 每个关键业务规则 = 1 个测试项
   ```

3. **评估业务价值**：
   - 高：核心业务流程（登录、支付、下单）
   - 中：辅助功能（修改信息、查询记录）
   - 低：边缘功能（高级设置、管理员报表）

4. **提取需求内容**：提取该模块的相关 prd 章节内容

5. **分配 module_id**：按顺序递增（M01, M02, M03...）

6. **输出 test-items.jsonl**（按模块分组）：
   ```jsonl
   {"module_id":"M01","module_name":"用户注册","test_items":[{"item":"用户注册流程","business_value":"高"},{"item":"手机号验证","business_value":"高"}],"prd":"## 用户注册\n..."}
   {"module_id":"M02","module_name":"用户登录","test_items":[{"item":"用户登录流程","business_value":"高"}],"prd":"## 用户登录\n..."}
   ```

**关键原则**：
- ⚡ **快速识别**：只列清单，不做场景分析（场景分析在 Step 2）
- 📋 **粒度适中**：每个测试项预估生成 3-8 条用例
- 🎯 **面向并发**：按模块分组，便于并发分配
- 🔢 **module_id**：自动递增（M01-M99），用于用例 ID 前缀

**输出**：test-items.jsonl

---

### Step 2: 场景分析 + 用例生成（重量级，并发）

**目标**：并发执行场景分析并直接生成测试用例

**并发策略（简化）**：

1. **计算 Agent 数量**：
   ```
   模块数 = M（来自 test-items.jsonl）
   Agent 数 = ceil(M / 2.5)  # 每个 agent 负责 2-3 个模块

   示例：
   - 5 个模块 → 2 个 agent（每个 2-3 个模块）
   - 10 个模块 → 4 个 agent（每个 2-3 个模块）
   ```

2. **模块分配**：
   - 按顺序将模块分配给各 agent（顺序分配，不做负载均衡）
   - 示例：10 个模块 → Agent1(M01-M03), Agent2(M04-M06), Agent3(M07-M08), Agent4(M09-M10)

3. **并行执行**：
   - 同时启动 N 个 Task agent
   - 每个 agent 读取 `assets/agent-prompt.md` 模板作为提示词
   - 传递给 agent：工作区路径、分配的模块列表（module_id）
   - Agent 自行读取 prd.md、test-items.jsonl、参考文档

4. **收集结果**：
   - 各 agent 输出到 `cases/{module_name}.jsonl`
   - 用例 ID 格式：`{module_id}-{seq:03d}`（如 M01-001, M01-002）
   - 模块内 ID 独立编号，天然无冲突

**Sub Agent 提示词模板位置**：

```
assets/agent-prompt.md
```

模板包含以下占位符：
- `{workspace}`：工作区根路径（需求输出目录的绝对路径）
- `{skill_dir}`：test-case-generator skill 目录的绝对路径
- `{assigned_modules}`：分配的模块列表（JSON 数组）

**重要**：启动 Sub Agent 时，必须替换 agent-prompt.md 中的占位符为实际的绝对路径。

**输出**：cases/{module_name}.jsonl（多个文件）

---

### Step 3: 质量审查

对各 agent 输出的模块文件进行审查（合并前）：

**3.1 编码检查**（优先执行）

```bash
# 检查所有模块文件是否有乱码字符
grep -n '�' cases/*.jsonl
```

- **无输出** = 无乱码，继续下一步
- **有输出** = 显示 `文件名:行号:内容`，必须先修复再继续

**3.2 格式验证**（使用脚本）

```bash
# 验证所有模块文件的格式和业务规则
python scripts/validate_jsonl.py cases/*.jsonl --strict
```

**3.2 AI 手动检查清单**

逐项检查并修复问题：

```markdown
## 质量检查清单

### 1. 测试项覆盖检查（遗漏问题）
□ 列出 test-items.jsonl 中所有测试项
□ 检查 cases/*.jsonl 中每个测试项是否都有对应用例
□ 遗漏的测试项需补充用例
□ 输出：覆盖率 = 已覆盖测试项数 / 总测试项数

### 2. 场景覆盖检查
□ 每个测试项是否至少有 1 个正向场景
□ 每个测试项是否至少有 1 个异常/边界场景
□ 核心功能（business_value=高）是否覆盖更多场景类型

### 3. 格式规范检查
□ 用例名称是否以"验证"开头（主谓宾格式）
□ module_name 是否 ≤15 字符
□ test_item 是否与 test-items.jsonl 中的 item 匹配
□ scenario_type 是否为有效值（正向/边界/异常/性能/安全）
□ steps 是否至少有 1 条，每条有 action 和 expected
□ preconditions 是否为数组格式

### 4. 业务逻辑检查
□ 优先级是否合理（P1 占比 10-20%）
□ 反向用例是否标记 is_negative: true
□ test_type 是否与 scenario_type 匹配（安全场景→安全性测试）

### 5. 内容质量检查
□ 步骤描述是否具体可执行（避免"正确操作"等模糊描述）
□ 预期结果是否可验证（避免"正常"等模糊描述）
□ 前置条件是否完整
```

**检查结果报告**：

```markdown
## 质量审查报告

- 总用例数：{N}
- 测试项覆盖率：{X}%（{covered}/{total}）
- 遗漏测试项：{list}
- 场景覆盖：正向场景 {N} 个，异常场景 {N} 个，边界场景 {N} 个
- 格式问题：{N} 处
- 优先级分布：P1({x}%) P2({x}%) P3({x}%) P4({x}%) P5({x}%)

### 待修复问题
1. ...
2. ...
```

---

### Step 4: 合并与导出

**4.1 合并测试用例**

```bash
python scripts/merge_jsonl.py cases/*.jsonl -o cases.jsonl --sort-by module
```

> 若发现 ID 溢出/冲突：按模块排序后整体重排 ID（TC-001 起），或调整分段后重新生成并合并。

**4.2 导出 XMind 思维导图**（可选）

```bash
python scripts/convert_to_xmind.py cases.jsonl -o cases.xmind --name "{需求名称}"
```

**4.3 生成统计报告**

```bash
python scripts/stats_report.py cases.jsonl --test-items test-items.jsonl -o stats-report.md
```

**4.4 输出确认**

```markdown
## 导出完成

已生成以下文件：
- test-items.jsonl（{N} 个测试项）
- cases/（{M} 个模块文件，中间态）
- cases.jsonl（{N} 条用例，合并后）
- cases.xmind（思维导图，可选）
- stats-report.md（统计报告）

请查收。
```

## 工具脚本

### 环境与依赖
- Python 3.9+
- `jsonschema`（Schema 验证）：`pip install jsonschema`
- `xmind`（生成 XMind）：`pip install xmind`

### 路径说明

**执行脚本时**，所有脚本路径都是相对于 test-case-generator skill 目录的相对路径：
- 脚本位置：`scripts/validate_jsonl.py`、`scripts/merge_jsonl.py` 等
- 这些脚本需要从 skill 目录执行，或使用绝对路径

**在工作流中调用脚本的正确方式**：
```bash
# 方式 1：使用绝对路径（推荐）
python /path/to/test-case-generator/scripts/validate_jsonl.py {workspace}/cases/*.jsonl --strict

# 方式 2：先 cd 到 skill 目录
cd /path/to/test-case-generator
python scripts/validate_jsonl.py {workspace}/cases/*.jsonl --strict
```

### 可用脚本

| 脚本 | 功能 | 详细用法 |
|-----|------|---------|
| `validate_jsonl.py` | 验证 JSONL 格式、Schema、业务规则 | `--help` |
| `merge_jsonl.py` | 合并多个 JSONL 文件 | `--help` |
| `convert_to_xmind.py` | 转换为 XMind 思维导图 | `--help` |
| `stats_report.py` | 生成统计报告 | `--help` |

**使用方法**：所有脚本都支持 `--help` 查看详细参数说明。

**常用命令**：参见 workflow 中各步骤的脚本调用示例。

## 用例名称规范

用例名称应按**主谓宾格式**表达：

| 正确示例 | 错误示例 |
|---------|---------|
| 验证用户成功登录系统 | 登录测试 |
| 验证密码错误时登录失败 | 密码错误 |
| 验证系统防止SQL注入 | SQL注入测试 |

## 成功标准
1. **文档完整性**：test-items.jsonl / cases/ / cases.jsonl / stats-report.md；有网且依赖满足时附 cases.xmind。
2. **覆盖率**：测试项覆盖 100%，缺失=0。
3. **场景覆盖**：每个测试项至少有 1 个正向场景 + 1 个异常/边界场景；核心功能（business_value=高）覆盖更多场景类型。
4. **质量阈值**：模糊描述=0；每步含 expected；module_name ≤15；用例名以"验证"开头；scenario_type 为有效值。
5. **优先级分布**：P1 10–20%，P2 25–35%，P3 20–30%，P4 15–25%，P5 5–10%；反向用例占比 ≥15%。
6. **格式校验**：`validate_jsonl.py --strict` 0 错误；ID 冲突=0；Schema 校验通过。
7. **并发安全**：无 ID 溢出/越界；如调整分段需在合并后重排 ID。

## 注意事项

1. **本 skill 专注于用例生成**，不处理需求质量问题（如需求模糊、缺失信息等，请先使用 requirement-tester）
2. 用例 ID 必须全局唯一
3. 用例名称按主谓宾格式，不含 ID
4. 优先级按 business_value 和 scenario_type 综合判断
5. 测试类型从 13 种中选择最匹配的一种
6. scenario_type 必须为：正向场景、边界场景、异常场景、性能场景、安全场景 之一

## 按需加载提示
- references（priority/test-type guide）仅在判定优先级/类型时读取，避免整篇加载。
- assets 模板用于快速起稿，完成后可删除未用文件。
- scripts 执行输出即可，不把脚本内容拉入上下文。
