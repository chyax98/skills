---
name: test-case-generator
description: This skill generates structured test cases from requirement documents. Use when users ask to create test cases, convert requirements to test cases, or generate test suites. Outputs JSONL/Excel/XMind formats.
---

# 测试用例生成器

**核心理念**：测试点 = 用例名称。"验证用户成功登录" 本身就是测试点，是评审核心。

---

## 成功标准

1. 格式校验 0 错误
2. 重复用例 0 个（相似度 ≥ 0.75 视为重复）
3. 优先级分布：P1(10-15%) P2(25-35%) P3(20-30%) P4(15-25%) P5(5-10%)
4. 每个测试项 ≥1 正向 + ≥1 反向用例
5. 所有用例名称以"验证"开头，包含预期结果

---

## 用例 Schema

```typescript
interface TestCase {
  name: string;           // "验证" 开头，唯一
  priority: "P1"|"P2"|"P3"|"P4"|"P5";
  is_negative: boolean;
  test_type: string;
  preconditions: string[];
  steps: Array<{ action: string; expected?: string }>;
  notes?: string;
}
```

**完整示例**：
```jsonl
{"name":"验证用户输入正确账号密码时成功登录并跳转首页","priority":"P1","is_negative":false,"test_type":"功能测试","preconditions":["用户已注册"],"steps":[{"action":"打开登录页"},{"action":"输入用户名 testuser"},{"action":"输入密码 Test@123"},{"action":"点击登录按钮","expected":"登录成功，跳转至首页"}]}
{"name":"验证用户输入错误密码时登录失败并提示密码错误","priority":"P3","is_negative":true,"test_type":"功能测试","preconditions":["用户已注册"],"steps":[{"action":"打开登录页"},{"action":"输入用户名 testuser"},{"action":"输入错误密码 wrong123"},{"action":"点击登录按钮","expected":"提示密码错误，保留在登录页"}]}
```

**CRITICAL**：用例名称 = 测试点，必须包含：场景 + 预期结果

---

## 优先级规范

| 功能重要性 | 正向场景 | 反向场景 |
|-----------|---------|---------|
| 核心功能 | P1 | P3 |
| 基本功能 | P2 | P4 |
| 不常用功能 | P5 | P5 |

**口诀**：核心正向必P1，基本正向上P2，核心反向是P3，基本反向给P4，不常用都P5

**功能等级**：
- **核心**：登录/注册、订单/支付、核心数据保存
- **基本**：列表/查询、修改信息、消息通知
- **不常用**：高级搜索、批量操作、管理员功能

---

## 测试类型

**默认**：功能测试（业务逻辑验证）

**特殊场景**：
- 涉及多模块协作 → 集成测试
- 关注认证授权/注入防护 → 安全性测试
- 关注响应时间/并发 → 性能测试
- 关注界面/操作流程 → 易用性测试
- 关注浏览器/设备兼容 → 兼容性测试

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
        python3 scripts/validate.py ${测试项}.jsonl

    # 合并单模块
    python3 scripts/merge.py ${workspace}/${模块}/*.jsonl \
        -o ${workspace}/${模块}/_merged.jsonl

    # 模块内重复检测
    python3 scripts/check.py ${workspace}/${模块}/_merged.jsonl --module-level

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
    -o ${workspace}/${需求名称}-测试用例.jsonl --sort-by priority

python3 scripts/check.py ${workspace}/${需求名称}-测试用例.jsonl \
    -o ${workspace}/check-report.md
```

**CRITICAL**：合并后必须运行 check.py 进行跨模块重复检测

---

## Phase 5: 评估 + 修正

阅读 check-report.md，逐项评估并修正。

**重复用例判断**：

check.py 会输出相似度 ≥ 0.75 的用例对。对于每一对，根据以下问题自主判断：

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
python3 scripts/export.py ${需求名称}-测试用例.jsonl \
    -o ${需求名称}-测试用例
# 输出 .xlsx 和 .xmind
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
| check-report 无严重问题 | 逐项处理报告问题 |

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
└── check-report.md
```

---

## 脚本 

| 脚本 | 功能 |
|-----|------|
| scripts/validate.py | 单文件格式校验 |
| scripts/merge.py | 合并 JSONL，自动推断 module_name/test_item |
| scripts/check.py | 综合检测（优先级、重复、乱码、覆盖） |
| scripts/export.py | 导出 Excel + XMind |
