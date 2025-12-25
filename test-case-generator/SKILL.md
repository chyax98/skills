---
name: test-case-generator
description: 从需求文档生成结构化测试用例。按测试点逐个生成并即时校验，输出 JSONL/Excel/XMind 格式。触发词：生成测试用例、需求转用例、测试用例生成。
---

# 测试用例生成器

**流程**：Step 1（规划）→ Step 2（生成）→ Step 3（输出）

---

## 输出结构

```
./需求名称/
├── 模块A/
│   ├── 测试点1.jsonl
│   └── 测试点2.jsonl
├── 模块B/
│   └── 测试点3.jsonl
├── 需求名称-测试用例.jsonl   # 合并后
├── 需求名称-测试用例.xlsx    # Excel
├── 需求名称-测试用例.xmind   # XMind（可选）
├── review-report.md          # 审查报告
└── stats-report.md           # 统计报告
```

---

## Step 1: 规划

**输入**：需求文档

**处理**：

1. **读取需求文档**，理解完整业务

2. **划分模块**（≤8 个），按功能内聚原则

3. **识别测试点**：
   - 每个用户可执行的操作 = 1 个测试点
   - 每个系统自动行为 = 1 个测试点
   - 每个 CRUD 操作 = 各 1 个测试点
   - 每个关键业务规则 = 1 个测试点

4. **评估功能等级**：

   | 等级 | 定义 | 占比 | 示例 |
   |-----|------|-----|------|
   | 核心功能 | 失败导致系统核心价值丧失 | 10-15% | 登录、创建、支付 |
   | 基本功能 | 失败影响体验但不阻塞核心流程 | 60-70% | 列表、筛选、通知 |
   | 不常用功能 | 低频扩展功能 | 15-25% | 批量操作、高级搜索 |

5. **创建目录结构**：
   ```bash
   mkdir -p {workspace}/{module_name}/
   ```

6. **使用 TodoWrite** 创建生成任务清单

**输出**：目录结构 + TodoWrite 任务清单

---

## Step 2: 生成

**处理**：遍历每个模块的每个测试点

```python
for module in modules:
    for test_point in module["test_points"]:

        # 1. 断点恢复：已存在则跳过
        file_path = f"{workspace}/{module['name']}/{test_point['name']}.jsonl"
        if file_exists(file_path):
            continue

        # 2. 更新 TodoWrite 状态

        # 3. 分析场景 + 生成用例
        cases = generate_cases(test_point)

        # 4. 写入文件
        write_jsonl(file_path, cases)

        # 5. 即时校验
        run(f"python3 {skill_dir}/scripts/validate.py {file_path}")

        # 6. 标记完成
```

### 场景覆盖

| 功能等级 | 覆盖要求 |
|---------|---------|
| 核心功能 | 正向 + 边界 + 异常 + 性能/安全（如适用） |
| 基本功能 | 正向 + 边界 + 异常 |
| 不常用功能 | 正向 + 主要异常 |

### 优先级判定

| 功能等级 | 正向场景 | 反向场景 |
|---------|---------|---------|
| 核心功能 | **P1** | **P3** |
| 基本功能 | **P2** | **P4** |
| 不常用功能 | **P5** | **P5** |

**口诀**：核心正向必P1，基本正向上P2，核心反向是P3，基本反向给P4，不常用都P5

**目标分布**：P1(10-15%) P2(25-35%) P3(20-30%) P4(15-25%) P5(5-10%)

### 用例 Schema

```typescript
interface TestCase {
  name: string;                    // 以"验证"开头，唯一标识
  priority: "P1" | "P2" | "P3" | "P4" | "P5";
  test_type: string;               // 功能测试、安全性测试等
  is_negative: boolean;            // 是否反向用例
  preconditions: string[];         // 前置条件
  steps: Array<{
    action: string;                // 操作步骤
    expected?: string;             // 预期结果（验证点必填）
  }>;
  notes?: string;                  // 备注
}
```

### 用例示例

```jsonl
{"name":"验证用户成功创建自用相框","priority":"P1","test_type":"功能测试","is_negative":false,"preconditions":["用户已登录","用户未达到相框数量上限"],"steps":[{"action":"进入创建相框页面"},{"action":"选择'为自己创建'类型"},{"action":"输入相框名称'家庭相框'"},{"action":"点击创建按钮","expected":"相框创建成功，跳转到相框页面"}]}
{"name":"验证相框名称超长时提示错误","priority":"P3","test_type":"功能测试","is_negative":true,"preconditions":["用户已登录"],"steps":[{"action":"进入创建相框页面"},{"action":"输入超过50字符的相框名称"},{"action":"点击创建按钮","expected":"提示'相框名称不能超过50字符'"}]}
```

### 用例规范

**名称**：主谓宾格式，以"验证"开头
```
✅ 验证用户成功创建自用相框
✅ 验证系统拒绝超过20字符的用户名
❌ 登录测试
❌ 密码错误
```

**步骤**：具体可执行
```
✅ 输入用户名 testuser
✅ 输入21个字符的用户名 abcdefghijklmnopqrstu
❌ 输入正确的用户名
```

**预期**：只在验证点写，过渡步骤省略
```
✅ action: "点击登录按钮"
   expected: "登录成功，跳转到首页"

✅ action: "输入用户名 testuser"
   （无预期 - 过渡步骤）

❌ action: "输入用户名 testuser"
   expected: "用户名输入框显示 testuser"  // 废话
```

**前置条件**：明确状态
```
✅ 用户已登录
✅ 相框已绑定实体设备
❌ 系统正常
```

### 即时校验

```bash
# 每个测试点生成后立即执行
python3 {skill_dir}/scripts/validate.py {file_path}
```

---

## Step 3: 输出

### 3.1 合并

```bash
python3 {skill_dir}/scripts/merge.py \
    {workspace}/*/*.jsonl \
    -o {workspace}/{需求名称}-测试用例.jsonl \
    --sort-by priority
```

### 3.2 审查（独立 Agent）

启动审查 Agent：

```python
Task(
    subagent_type="general-purpose",
    prompt=read_file("{skill_dir}/assets/review-prompt.md")
           .replace("{workspace}", workspace_path)
           .replace("{skill_dir}", skill_dir_path)
           .replace("{requirement_doc}", requirement_doc_path)
           .replace("{需求名称}", requirement_name)
)
```

审查 Agent 执行：
1. 格式校验（validate.py）
2. 重复检测 + 裁决（detect_duplicates.py）
3. 覆盖性检查（对照需求文档）
4. 优先级分布检查
5. 输出 `review-report.md`

### 3.3 导出

```bash
# Excel
python3 {skill_dir}/scripts/to_excel.py \
    {workspace}/{需求名称}-测试用例.jsonl \
    -o {workspace}/{需求名称}-测试用例.xlsx

# XMind（可选）
python3 {skill_dir}/scripts/to_xmind.py \
    {workspace}/{需求名称}-测试用例.jsonl \
    -o {workspace}/{需求名称}-测试用例.xmind \
    --name "{需求名称}"

# 统计报告
python3 {skill_dir}/scripts/stats.py \
    {workspace}/{需求名称}-测试用例.jsonl \
    -o {workspace}/stats-report.md
```

**输出确认**：

```markdown
## ✅ 测试用例生成完成

| 文件 | 说明 |
|------|------|
| {需求名称}-测试用例.jsonl | 合并用例（N 条） |
| {需求名称}-测试用例.xlsx | Excel 格式 |
| {需求名称}-测试用例.xmind | XMind 思维导图 |
| review-report.md | 审查报告 |
| stats-report.md | 统计报告 |
```

---

## 测试类型

| 类型 | 适用场景 |
|-----|---------|
| **功能测试** | 业务逻辑验证（主体，50-60%） |
| 安全性测试 | 认证授权、攻击防护 |
| 性能测试 | 响应时间、并发能力 |
| 易用性测试 | 用户体验、界面交互 |
| 兼容性测试 | 跨环境运行 |
| 稳定性测试 | 长期运行稳定性 |
| 集成测试 | 模块间协作 |

> 详细说明见 `{skill_dir}/assets/test-type-guide.md`

---

## 质量标准

| 指标 | 目标 |
|------|-----|
| 测试点覆盖率 | 100% |
| 场景覆盖 | 每个测试点至少 1 正向 + 1 异常/边界 |
| 格式校验 | 0 错误 |
| 优先级分布 | P1(10-15%) P2(25-35%) P3(20-30%) P4(15-25%) P5(5-10%) |

---

## 工具脚本

| 脚本 | 功能 |
|-----|------|
| validate.py | 格式校验 |
| merge.py | 合并 JSONL，从路径推断 module_name 和 test_item |
| detect_duplicates.py | 相似度检测 |
| to_excel.py | 导出 Excel |
| to_xmind.py | 导出 XMind |
| stats.py | 生成统计报告 |

---

## 参考文档

| 文档 | 用途 |
|------|-----|
| `assets/priority-guide.md` | 优先级判定详细指南 |
| `assets/test-type-guide.md` | 测试类型详细说明 |
| `assets/cases.jsonl` | 用例格式示例 |
| `assets/review-prompt.md` | 审查 Agent 提示词 |
