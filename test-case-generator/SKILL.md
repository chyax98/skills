---
name: test-case-generator
description: 从需求文档生成结构化测试用例。按 test_item 逐个生成并即时校验，独立审查查漏补缺，输出 JSONL/Excel/XMind 格式。触发词：生成测试用例、需求转用例、测试用例生成。
---

# 测试用例生成器

**执行要求**：严格按 Step 1 → 2 → 3 → 4 顺序执行

## 输出结构

```
./                                    # 当前工作目录
└── {需求名称}/                        # 工作区（自动创建）
    ├── 相框创建/                      # 模块文件夹
    │   ├── 相框类型选择.jsonl         # test_item 文件（极简 Schema：6 字段）
    │   └── 自用相框创建.jsonl
    ├── 成员邀请/
    │   └── 邀请码生成.jsonl
    ├── 成员管理/
    │   └── 成员列表展示.jsonl
    ├── 相框创建.jsonl                 # Step 3: 模块合并（已添加 module_name, test_item）
    ├── 成员邀请.jsonl                 # Step 3: 模块合并
    ├── 成员管理.jsonl                 # Step 3: 模块合并
    ├── {需求名称}-测试用例.jsonl      # Step 4: 最终合并（8 字段完整版）
    ├── {需求名称}-测试用例.xlsx       # Step 4: Excel 导出
    ├── {需求名称}-测试用例.xmind      # Step 4: XMind 导出（可选）
    ├── review-report.md              # Step 3: 审查报告
    └── stats-report.md               # Step 4: 统计报告
```

**输入**：需求文档路径

**工作区命名**：从文档标题提取，如 `# Frame相框管理` → 工作区为 `./Frame相框管理/`

---

## Step 1: 需求理解与模块规划

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

4. **评估功能等级**（核心/基本/不常用）：

**判断标准**：
- **核心功能**：系统最关键业务流程，失败会导致系统核心价值丧失
  - 占比：10-15% 的 test_item
  - 示例：用户登录、相框创建成功、内容上传成功、支付完成
  - 判断方法：如果这个功能失败，用户是否无法完成核心任务？

- **基本功能**：常用辅助功能，失败会影响用户体验但不阻塞核心流程
  - 占比：60-70% 的 test_item
  - 示例：列表展示、排序、筛选、查看详情、通知、成员管理
  - 判断方法：这个功能每天都会用到吗？失败后用户能否绕过继续使用？

- **不常用功能**：低频扩展功能，失败影响极少数用户
  - 占比：15-25% 的 test_item
  - 示例：批量操作、高级搜索、管理统计、导出报表
  - 判断方法：这个功能一个月用几次？只有高级用户才用？

5. **预估用例数量**：为每个 test_item 预估正向和异常用例数

6. **创建目录结构**：
   ```bash
   mkdir -p {workspace}/{module_name}/
   ```

7. **内存规划格式**（不写文件）：
   ```python
   modules = [
       {
           "name": "相框创建",
           "test_items": [
               {"name": "相框类型选择", "function_level": "核心功能"},
               {"name": "自用相框创建", "function_level": "核心功能"},
               {"name": "礼物相框创建", "function_level": "核心功能"}
           ]
       },
       {
           "name": "成员邀请",
           "test_items": [
               {"name": "邀请码生成", "function_level": "核心功能"},
               {"name": "扫码加入", "function_level": "基本功能"}
           ]
       }
   ]
   ```

**Step 1 完成后**：
- 使用 TodoWrite 创建各模块的生成任务
- 规划保存在对话上下文中（AI 记忆）
- 创建模块文件夹（空文件夹，Step 2 填充）

---

## Step 2: 逐 test_item 生成用例

**执行者**：主 Agent（不可委托，保持全局上下文）

**前置准备**（强制执行）：

```python
# 1. 【必须】读取优先级指南
priority_guide = read_file("{skill_dir}/assets/priority-guide.md")

# 2. 读取用例格式示例
case_examples = read_file("{skill_dir}/assets/cases.jsonl")
```

**核心循环**：

```python
# 使用 Step 1 内存中的规划
for module in modules:  # modules 来自 Step 1
    module_name = module["name"]

    # 遍历该模块的每个 test_item
    for test_item in module["test_items"]:
        test_item_name = test_item["name"]
        function_level = test_item["function_level"]

        # 1. 检查是否已生成（断点恢复）
        file_path = f"{workspace}/{module_name}/{test_item_name}.jsonl"
        if os.path.exists(file_path):
            print(f"⏭️  跳过已生成：{module_name}/{test_item_name}")
            continue

        # 2. 更新 TodoWrite：标记当前 test_item 为 in_progress
        TodoWrite(...)

        # 3. 场景分析
        scenarios = analyze_scenarios(
            test_item=test_item_name,
            function_level=function_level,
            priority_guide=priority_guide
        )

        # 4. 生成用例（极简 Schema：6 字段）
        cases = []
        for scenario in scenarios:
            scenario_cases = generate_cases(
                test_item=test_item_name,
                scenario=scenario,
                function_level=function_level,
                priority_guide=priority_guide
            )
            cases.extend(scenario_cases)

        # 5. 写入文件
        write_jsonl(file_path, cases)

        # 6. 即时检验（编码+格式）
        bash(f"grep -n '�' {file_path}")  # 无输出 = 通过
        bash(f"python3 {{skill_dir}}/scripts/validate.py {file_path} --strict")

        # 7. 更新 TodoWrite：标记当前 test_item 为 completed
        TodoWrite(...)
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
- 核心功能（function_level=核心功能）：正向 + 边界 + 异常 + 性能/安全（如适用）
- 基本功能（function_level=基本功能）：正向 + 边界 + 异常
- 不常用功能（function_level=不常用功能）：正向 + 主要异常

---

### 优先级判定规则

**前置要求**（强制执行）：
1. **必须**读取 `{skill_dir}/assets/priority-guide.md` 完整指南
2. 理解功能等级与优先级的映射关系

**判定步骤**：
1. 从 README.md 读取 test_item 的 `功能等级`
2. 判断当前场景的类型（正向/反向）
3. 按以下规则映射优先级：

| 功能等级 | 场景类型 | 优先级 | 说明 |
|---------|---------|-------|------|
| **核心功能** | 正向场景 | **P1** | 冒烟测试必测 |
| **核心功能** | 反向场景 | **P3** | 核心健壮性验证 |
| **基本功能** | 正向场景 | **P2** | 日常回归测试 |
| **基本功能** | 反向场景 | **P4** | 完整回归测试 |
| **不常用功能** | 任意场景 | **P5** | 发布前测试 |

**快速口诀**（来自 priority-guide.md）：
- 核心正向必 P1
- 基本正向上 P2
- 核心反向是 P3
- 基本反向给 P4
- 不常用的都 P5

**优先级分布目标**：P1(10-15%) P2(25-35%) P3(20-30%) P4(15-25%) P5(5-10%)

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

### TestCase Schema（生成时 - 极简版）

```typescript
interface TestCase {
  name: string;                // 用例名称（唯一标识，以"验证"开头）
  priority: "P1" | "P2" | "P3" | "P4" | "P5";
  test_type: string;           // 功能测试、安全性测试等
  is_negative: boolean;        // 是否为反向用例
  preconditions: string[];     // 前置条件
  steps: Array<{
    action: string;            // 操作步骤
    expected?: string;         // 预期结果（可选）
  }>;
  notes?: string;              // 备注（可选）
}
```

**字段说明**：
- **只包含业务字段**，不包含元信息（module_name, test_item）
- **字段数**：6 个核心字段
- **唯一标识**：name 字段
- **无 id 字段**：完全不需要数字编号

---

### 用例生成规范

**用例名称**：主谓宾格式，以"验证"开头
```
✅ 验证用户成功创建自用相框
✅ 验证用户输入错误密码时登录失败并提示错误信息
✅ 验证系统拒绝超过20字符的用户名
❌ 登录测试
❌ 密码错误
```

### 可执行性原则

确保测试人员可执行，根据测试场景选择验证方式：

| 场景 | 步骤 | 预期验证 |
|-----|------|---------|
| 前端/UI 测试 | 界面操作 | 界面可见结果 |
| 服务端/接口测试 | 调用 API | 响应 + 数据库/日志 |
| 端到端测试 | 界面操作 | 界面结果 + 数据落库 |

**关键**：明确验证方式，避免模糊描述
- ✅ "检查订单表，status 字段为 'paid'"
- ✅ "查看日志，记录包含 'order created'"
- ❌ "数据正确入库"（模糊）
- ❌ "日志正常"（模糊）

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
✅ "用户已登录"
✅ "相框已绑定实体设备"
✅ "用户未达到相框数量上限"
❌ "系统正常"
❌ "用户登录"（缺少"已"字，不明确）
```

---

### 用例示例

**文件**：`相框创建/自用相框创建.jsonl`

```jsonl
{"name":"验证用户成功创建自用相框","priority":"P1","test_type":"功能测试","is_negative":false,"preconditions":["用户已登录","用户未达到相框数量上限"],"steps":[{"action":"进入创建相框页面"},{"action":"选择'为自己创建'类型"},{"action":"输入相框名称'家庭相框'"},{"action":"点击创建按钮","expected":"相框创建成功，跳转到相框页面，显示相框名称"}]}

{"name":"验证相框名称超长时提示错误","priority":"P3","test_type":"功能测试","is_negative":true,"preconditions":["用户已登录"],"steps":[{"action":"进入创建相框页面"},{"action":"选择'为自己创建'类型"},{"action":"输入超过50字符的相框名称"},{"action":"点击创建按钮","expected":"提示'相框名称不能超过50字符'"}]}
```

**注意**：
- 无 `id` 字段
- 无 `module_name` 字段（合并时从文件夹名添加）
- 无 `test_item` 字段（合并时从文件名添加）

---

### 即时检验（每个 test_item 必做）

```bash
# 1. 编码检查（必须无乱码）
grep -n '�' {module_dir}/{test_item}.jsonl
# 无输出 = 通过；有输出 = 显示行号，必须修复

# 2. 格式校验
python3 {skill_dir}/scripts/validate.py {module_dir}/{test_item}.jsonl --strict
```

### 断点恢复

```
如果中途中断：
1. 检查所有模块的 README.md
2. 找到第一个未完成的 test_item（状态为 ⬜）
3. 从该 test_item 继续生成
已生成的 .jsonl 文件不会丢失
```

**示例**：
```
相框创建/ → README.md → 所有 test_item 状态为 ✅
成员邀请/ → README.md → 所有 test_item 状态为 ✅
成员管理/ → README.md
  ✅ 成员列表展示
  ⬜ 移除成员  ← 从这里继续
  ⬜ 离开相框
```

---

## Step 3: 模块审查与全量审查

### 3.1 模块审查（每个 module 完成后）

```python
for module_dir in glob("{workspace}/*/"):
    module_name = os.path.basename(module_dir.rstrip("/"))

    # 检查是否所有 test_item 都完成了
    if not all_test_items_completed(module_dir):
        continue

    # 1. 合并 module 内所有 test_item
    merge_command = f"""
    python3 {skill_dir}/scripts/merge.py \\
        {module_dir}/*.jsonl \\
        -o {workspace}/{module_name}.jsonl
    """
    run_bash(merge_command)

    # 2. 模块级检查
    validate_command = f"""
    python3 {skill_dir}/scripts/validate.py \\
        {workspace}/{module_name}.jsonl \\
        --strict
    """
    run_bash(validate_command)

    # 3. 启动审查 Agent（轻量级）
    Task(
        subagent_type="general-purpose",
        model="haiku",
        prompt=f"""
        审查模块 {module_name} 的用例质量：

        输入文件：{workspace}/{module_name}.jsonl
        参考文件：{module_dir}/README.md

        检查项：
        1. 覆盖率：README.md 中规划的所有场景是否都覆盖了？
        2. 一致性：用例命名、步骤描述风格是否一致？
        3. 优先级：是否符合 priority-guide.md 规则？

        输出格式：
        ✅ 通过项：[列表]
        ⚠️ 建议修复项（可选）：[列表]
        ❌ 必须修复项：[列表]
        """
    )
```

### 3.2 全量审查（所有 module 完成后）

**执行者**：Task Agent（主 Agent 启动）

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
1. **脚本扫描**：`validate.py --strict` 输出待审查项
2. **Agent 裁决**：逐项判断是否需要修复
3. **输出报告**：`{workspace}/review-report.md`

---

## Step 4: 合并与导出

**执行者**：主 Agent + 脚本

```bash
# 1. 最终格式检验
python3 {skill_dir}/scripts/validate.py {workspace}/*.jsonl --strict

# 2. 合并所有模块（按需求命名）
python3 {skill_dir}/scripts/merge.py \\
    {workspace}/*.jsonl \\
    -o {workspace}/{需求名称}-测试用例.jsonl \\
    --sort-by priority

# 3. 导出 Excel（按需求命名）
python3 {skill_dir}/scripts/to_excel.py \\
    {workspace}/{需求名称}-测试用例.jsonl \\
    -o {workspace}/{需求名称}-测试用例.xlsx

# 4. 导出 XMind（可选，按需求命名）
python3 {skill_dir}/scripts/to_xmind.py \\
    {workspace}/{需求名称}-测试用例.jsonl \\
    -o {workspace}/{需求名称}-测试用例.xmind \\
    --name "{需求名称}"

# 5. 生成统计报告
python3 {skill_dir}/scripts/stats.py \\
    {workspace}/{需求名称}-测试用例.jsonl \\
    -o {workspace}/stats-report.md
```

**输出确认**：

```markdown
## ✅ 测试用例生成完成

| 文件 | 说明 |
|------|------|
| 相框创建/ | 模块文件夹（含 README.md 和 test_item JSONL） |
| 相框创建.jsonl | 模块合并用例 |
| {需求名称}-测试用例.jsonl | 最终合并用例（N 条） |
| {需求名称}-测试用例.xlsx | Excel 格式 |
| {需求名称}-测试用例.xmind | XMind 思维导图 |
| review-report.md | 审查报告 |
| stats-report.md | 统计报告 |
```

---

## 质量检查清单

### 完整性
- [ ] 每个 test_item 至少 1 正向 + 1 异常/边界
- [ ] 核心功能（function_level=核心功能）覆盖更多场景

### 格式规范
- [ ] 用例名称以"验证"开头
- [ ] priority 为 P1-P5
- [ ] test_type 为 13 种之一
- [ ] steps 至少 1 条，至少 1 条有 expected
- [ ] `grep -n '�' {module}/*.jsonl` 无乱码

### 内容质量
- [ ] 步骤具体可执行，预期可验证
- [ ] 验证方式明确（界面/数据库/日志），避免模糊描述
- [ ] 反向用例标记 is_negative: true

---

## 成功标准

| 指标 | 目标值 |
|------|-------|
| 测试项覆盖率 | 100% |
| 场景覆盖 | 每个测试项至少 1 正向 + 1 异常/边界 |
| 格式校验 | 0 错误 |
| 编码检查 | 0 乱码 |
| 优先级分布 | P1(10-15%) P2(25-35%) P3(20-30%) P4(15-25%) P5(5-10%) |

---

## 工具脚本

**环境**：Python 3.9+，依赖 `jsonschema`、`xmind`、`openpyxl`

**路径**：脚本在 `{skill_dir}/scripts/`，使用绝对路径调用

| 脚本 | 功能 |
|-----|------|
| validate.py | 验证格式 + 编码检查（极简 Schema） |
| merge.py | 合并 JSONL 文件，从路径推断 module_name 和 test_item（支持多次合并） |
| detect_duplicates.py | 检测相似/重复用例（Jaccard 相似度 + 编辑距离） |
| to_excel.py | 转换为 Excel（11 列格式） |
| to_xmind.py | 转换为 XMind 思维导图 |
| stats.py | 生成统计报告 |

---

## 按需读取的参考文档

以下文档在特定场景下读取，不要一开始就全部加载：

| 文档 | 读取时机 | 内容 |
|------|---------|------|
| `assets/priority-guide.md` | **Step 2 开始前必读** | 优先级判定完整指南 |
| `assets/test-type-guide.md` | 选择测试类型时需要更多指导 | 各测试类型详细说明和更多示例 |
| `assets/cases.jsonl` | Step 2 首次生成前 | 完整的用例格式示例 |
| `assets/review-prompt.md` | Step 3 启动审查 Agent 时 | 审查 Agent 的完整提示词 |

---

## 注意事项

1. **主 Agent 执行 Step 1、2、4**，只有 Step 3 使用 Task Agent
2. **生成时不写 id, module_name, test_item**，合并时从路径推断并添加
3. **每个 test_item 生成后立即检验**，不要等到最后
4. **保持全局上下文**，生成时参考前面模块的风格
5. **断点可恢复**，已生成的文件不会丢失
6. **按需读取参考文档**，不要一开始就加载所有 assets
7. **强制读取 priority-guide.md**，不要依赖简化表格
8. **文件命名使用需求名称**，不使用通用名称
9. **完全不需要数字编号的 id 字段**，用 name 作为唯一标识
