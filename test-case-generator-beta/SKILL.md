---
name: test-case-generator
description: This skill generates structured test cases from requirement documents. Use when users ask to create test cases, convert requirements to test cases, or generate test suites. Outputs JSONL/Excel/XMind formats.
---

# 测试用例生成器

**核心理念**：测试点 = 用例名称。"验证用户成功登录" 本身就是测试点，是评审核心。

---

## 成功标准

1. 格式校验 0 错误
2. 无真正重复用例（相似度 ≥ 0.7 需人工判断，同场景同预期则删除）
3. 优先级分布：P1(10-15%) P2(25-35%) P3(20-30%) P4(15-25%) P5(5-10%)
4. 每个测试项 ≥1 正向 + ≥1 反向用例
5. 所有用例名称以"验证"开头，包含预期结果

---

## 用例 Schema

### 字段定义

| 字段 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | ✅ | 以"验证"开头，主谓宾结构，包含场景+预期结果 |
| priority | enum | ✅ | P1/P2/P3/P4/P5，按决策树判定 |
| is_negative | boolean | ✅ | true=反向用例，false=正向用例 |
| test_type | string | ✅ | 见测试类型列表，默认"功能测试" |
| preconditions | string[] | ✅ | 前置条件数组，无则填 [] |
| steps | Step[] | ✅ | 操作步骤数组，至少 1 个 |
| notes | string | ❌ | 备注，可选 |

### Step 结构

| 字段 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| action | string | ✅ | 具体操作，包含实际值 |
| expected | string | ❌ | 预期结果，验证点必填，过渡步骤省略 |

### TypeScript 定义

```typescript
interface TestCase {
  name: string;
  priority: "P1" | "P2" | "P3" | "P4" | "P5";
  is_negative: boolean;
  test_type: string;
  preconditions: string[];
  steps: Array<{ action: string; expected?: string }>;
  notes?: string;
}

// merge.py 自动添加的字段
interface MergedTestCase extends TestCase {
  module_name: string;  // 从父目录名推断
  test_item: string;    // 从文件名推断
}
```

### 完整示例

```jsonl
{"name":"验证用户输入正确账号密码时成功登录并跳转首页","priority":"P1","is_negative":false,"test_type":"功能测试","preconditions":["用户已注册","账号未被锁定"],"steps":[{"action":"打开登录页面"},{"action":"输入用户名 testuser"},{"action":"输入密码 Test@123"},{"action":"点击登录按钮","expected":"登录成功，跳转到首页"}]}
{"name":"验证用户输入错误密码时登录失败并提示密码错误","priority":"P3","is_negative":true,"test_type":"功能测试","preconditions":["用户已注册"],"steps":[{"action":"打开登录页"},{"action":"输入用户名 testuser"},{"action":"输入错误密码 wrong123"},{"action":"点击登录按钮","expected":"提示密码错误，保留在登录页"}]}
```

**CRITICAL**：用例名称 = 测试点，必须包含：场景 + 预期结果

---

## 优先级规范

### 判断决策树

**注意**：以下判断是针对**整个需求**的功能重要性。

```
是该需求的核心业务流程？
├─ 是 → 是正向场景？
│       ├─ 是 → P1
│       └─ 否 → P3
└─ 否 → 是该需求的基本功能？
        ├─ 是 → 是正向场景？
        │       ├─ 是 → P2
        │       └─ 否 → P4
        └─ 否 → P5（不常用功能）
```

**示例**（电商需求）：
- 核心：登录、下单、支付
- 基本：商品列表、订单查询、修改收货地址
- 不常用：高级搜索、批量导出、管理员后台

### 映射表

| 功能重要性 | 正向场景 | 反向场景 |
|-----------|---------|---------|
| 核心功能 | P1 | P3 |
| 基本功能 | P2 | P4 |
| 不常用功能 | P5 | P5 |

### 功能等级判定

| 等级 | 定义 | 示例 | 占比 |
|-----|------|-----|-----|
| 核心 | 失败导致系统核心价值丧失 | 登录/注册、订单/支付、核心数据保存 | 10-15% |
| 基本 | 失败影响体验但不阻塞核心 | 列表/查询、修改信息、消息通知 | 60-70% |
| 不常用 | 低频扩展功能 | 高级搜索、批量操作、管理员功能 | 15-25% |

### 特殊场景优先级

| 场景 | 优先级 |
|-----|-------|
| 核心功能性能测试 | P2 |
| 认证授权安全测试 | P1/P2 |
| 注入防护安全测试 | P3 |
| 主流环境兼容性 | P2 |
| 次要环境兼容性 | P4 |

### 常见错误

| 错误 | 正确 |
|-----|-----|
| 登录密码错误 → P2 | → P3（核心功能反向） |
| 修改个人信息 → P3 | → P2（基本功能正向） |
| 所有正向都设 P1 | 按功能等级判定 |

---

## 测试类型

### 选择决策树

```
涉及多个模块协作？ → 集成测试
关注长期运行稳定？ → 稳定性测试
关注故障恢复？ → 可靠性测试
关注安全防护？ → 安全性测试
关注性能指标？ → 性能测试
关注跨环境运行？ → 兼容性测试
关注用户体验？ → 易用性测试
关注数据埋点？ → 埋点测试
关注 AI 输出？ → AI效果测试
关注硬件交互？ → 硬件效果测试
默认 → 功能测试
```

### 类型列表

| 类型 | 说明 | 占比 |
|-----|------|-----|
| **功能测试** | 业务逻辑验证 | 50-60% |
| 安全性测试 | 认证授权、攻击防护 | 5-10% |
| 性能测试 | 响应时间、并发能力 | 5-10% |
| 易用性测试 | 用户体验、界面交互 | 5-10% |
| 兼容性测试 | 跨环境运行 | 5-10% |
| 稳定性测试 | 长期运行稳定性 | 3-5% |
| 集成测试 | 模块间协作 | 5-10% |
| 可靠性测试 | 故障恢复 | - |
| 可维护性测试 | 运维能力 | - |
| 可移植性测试 | 迁移能力 | - |
| 埋点测试 | 数据上报 | - |
| AI效果测试 | AI 输出质量 | - |
| 硬件效果测试 | 硬件交互 | - |

---

## 用例编写规范

### 命名规范

**格式**：验证 + [主体] + [动作/条件] + [预期结果]

```
✅ 验证用户成功创建订单
✅ 验证系统拒绝超过50字符的用户名
✅ 验证未登录用户访问个人中心时跳转登录页

❌ 登录测试（缺少"验证"）
❌ 验证密码错误（缺少预期结果）
❌ 测试用户注册功能（不是验证点格式）
```

### 前置条件规范

**原则**：明确具体状态，无废话

```
✅ 用户已登录
✅ 购物车中有商品
✅ 账号连续错误4次

❌ 系统正常（废话）
❌ 网络正常（默认条件）
❌ 无（应填空数组 []）
```

### 操作步骤规范

**原则**：具体可执行，包含实际值

```
✅ 输入用户名 testuser
✅ 输入21个字符的用户名 abcdefghijklmnopqrstu
✅ 点击"提交"按钮

❌ 输入正确的用户名（不具体）
❌ 输入用户名（缺少值）
❌ 操作系统（不可执行）
```

### 预期结果规范

**原则**：只在验证点写，明确可验证

```
✅ 步骤: "点击登录按钮"
   预期: "登录成功，跳转到首页"

✅ 步骤: "输入用户名 testuser"
   （无预期 - 过渡步骤）

❌ 步骤: "输入用户名 testuser"
   预期: "用户名输入框显示 testuser"（废话预期）
```

### 覆盖完整性

| 功能等级 | 覆盖要求 |
|---------|---------|
| 核心功能 | 正向 + 边界 + 异常 + 性能/安全 |
| 基本功能 | 正向 + 边界 + 异常 |
| 不常用功能 | 正向 + 主要异常 |

**CRITICAL**：每个测试项至少 1 正向 + 1 反向用例

---

## 流程概览

```
Phase 1: 理解需求 → Phase 2: 规划 → Phase 3: 逐模块生成 → Phase 4: 合并检测 → Phase 5: 评估修正 → Phase 6: 导出
```

---

## Phase 1: 理解需求

阅读需求文档，理解业务全貌。

---

## Phase 2: 规划

1. 划分模块（≤8 个）
2. 识别每个模块下的测试项
3. 使用 TodoWrite 建立任务清单
4. 创建目录结构

```bash
# 在当前工作目录下创建 workspace（不要在 skill 目录下创建）
workspace="${PWD}/需求名称"
mkdir -p "${workspace}/{模块名}/"
```

---

## Phase 3: 逐模块生成

```python
for 模块 in 所有模块:
    for 测试项 in 模块.测试项:
        生成完整用例 → ${workspace}/${模块}/${测试项}.jsonl
        python3 scripts/validate.py ${workspace}/${模块}/${测试项}.jsonl

    # 合并单模块（--deduplicate 防止重复运行时的重复条目）
    python3 scripts/merge.py ${workspace}/${模块}/*.jsonl \
        -o ${workspace}/${模块}/_merged.jsonl --deduplicate

    # 模块内重复检测
    python3 scripts/detect_duplicates.py ${workspace}/${模块}/_merged.jsonl

    # 执行模块自审检查清单
```

**CRITICAL - 用例名称规范**：
- 以"验证"开头，主谓宾结构
- 包含：验证 + [主体] + [动作/条件] + [预期结果]
- ✅ `验证用户输入超过20字符的用户名时系统提示长度错误`
- ❌ `验证用户名长度`（缺少预期结果）

---

## Phase 4: 合并 + 跨模块检测

```bash
python3 scripts/merge.py ${workspace}/*/_merged.jsonl \
    -o ${workspace}/${需求名称}-测试用例.jsonl --sort-by priority --deduplicate

# 跨模块重复检测
python3 scripts/detect_duplicates.py ${workspace}/${需求名称}-测试用例.jsonl

# 优先级分布统计
python3 scripts/stats.py ${workspace}/${需求名称}-测试用例.jsonl \
    -o ${workspace}/统计报告.md
```

**CRITICAL**：合并后必须运行重复检测和统计

---

## Phase 5: 评估 + 修正

根据 detect_duplicates.py 和 stats.py 的输出，逐项评估并修正。

**重复用例判断**：

detect_duplicates.py 会输出相似度 ≥ 0.7 的用例对（默认阈值，可用 --threshold 调整）。对于每一对，根据以下问题自主判断：

1. **是否测试同一场景？** 对比用例名称中的"条件"和"预期结果"
2. **是否覆盖不同边界？** 如"输入为空"vs"输入超长"是不同边界，保留两者
3. **是否正向/反向互补？** 正向和反向用例即使名称相似也应保留

**处理原则**：
- 测试同一场景且预期相同 → 删除其中一个
- 测试同一场景但预期不同 → 保留或合并
- 测试不同边界/条件 → 保留两者

**循环直到**：符合成功标准

---

## Phase 6: 导出

```bash
python3 scripts/to_excel.py ${workspace}/${需求名称}-测试用例.jsonl \
    -o ${workspace}/${需求名称}-测试用例.xlsx

python3 scripts/to_xmind.py ${workspace}/${需求名称}-测试用例.jsonl \
    -o ${workspace}/${需求名称}-测试用例.xmind
```

---

## 最终验收清单

| 检查项 | 失败时修正 |
|-------|-----------|
| 用例名称以"验证"开头 | 重写用例名称 |
| 用例名称包含预期结果 | 补充预期结果描述 |
| steps 非空且有 expected | 补充步骤和预期 |
| preconditions 为数组 | 修正格式 |
| 每测试项 ≥1正向+≥1反向 | 补充缺失用例 |
| 核心功能有 P1 用例 | 调整优先级 |
| 重复用例 0 个 | 删除或合并重复项 |
| 格式校验 0 错误 | 按错误提示修正 |
| 优先级分布在目标范围 | 批量调整优先级 |
| 重复检测无高相似度对 | 逐项处理重复用例 |

---

## 目录结构

```
${workspace}/
├── 模块A/
│   ├── 测试项1.jsonl
│   ├── 测试项2.jsonl
│   └── _merged.jsonl
├── ${需求名称}-测试用例.jsonl
├── ${需求名称}-测试用例.xlsx
├── ${需求名称}-测试用例.xmind
└── 统计报告.md
```

---

## 脚本

| 脚本 | 功能 | 状态 |
|-----|------|------|
| scripts/validate.py | 格式校验、必填字段、名称唯一性 | ✅ |
| scripts/merge.py | 合并 JSONL，推断 module_name/test_item | ✅ |
| scripts/detect_duplicates.py | 相似度检测（名称+步骤+预期） | ✅ |
| scripts/to_excel.py | 导出 Excel | ✅ |
| scripts/to_xmind.py | 导出 XMind | ✅ |
| scripts/stats.py | 优先级分布统计 | ✅ |
