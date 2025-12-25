# Schema 定义

## 测试点 Schema（points.jsonl）

Phase 2 输出，仅包含核心信息：

```typescript
interface TestPoint {
  name: string;      // 以"验证"开头，主谓宾结构
  priority: "P1" | "P2" | "P3" | "P4" | "P5";
  is_negative: boolean;
}
```

示例：
```jsonl
{"name":"验证用户成功登录","priority":"P1","is_negative":false}
{"name":"验证密码错误时登录失败","priority":"P3","is_negative":true}
```

---

## 完整用例 Schema（cases.jsonl）

Phase 3 输出：

```typescript
interface TestCase {
  name: string;                    // 以"验证"开头
  priority: "P1" | "P2" | "P3" | "P4" | "P5";
  is_negative: boolean;
  test_type: string;               // 见测试类型列表
  preconditions: string[];         // 前置条件
  steps: Array<{
    action: string;                // 操作步骤
    expected?: string;             // 预期结果（验证点必填）
  }>;
  notes?: string;                  // 备注（可选）
}
```

示例：
```jsonl
{"name":"验证用户成功登录","priority":"P1","is_negative":false,"test_type":"功能测试","preconditions":["用户已注册","账号未被锁定"],"steps":[{"action":"打开登录页面"},{"action":"输入用户名 testuser"},{"action":"输入密码 Test@123"},{"action":"点击登录按钮","expected":"登录成功，跳转到首页"}]}
```

---

## 合并后 Schema

merge.py 自动添加路径推断字段：

```typescript
interface MergedTestCase extends TestCase {
  module_name: string;  // 从目录路径推断
  test_item: string;    // 从目录路径推断
}
```

路径推断规则：
```
{workspace}/{模块}/{测试项}/cases.jsonl
              ↑        ↑
        module_name  test_item
```

---

## 字段映射

### Excel 映射

| Schema 字段 | Excel 列 |
|------------|---------|
| module_name | 一级模块 |
| (序号) | 编号 |
| test_item | 测试项 |
| priority | 优先级 |
| name | 用例标题 |
| steps[].action | 操作步骤 |
| steps[].expected | 预期结果 |
| is_negative | 是否反向用例 |
| test_type | 测试类型 |
| (固定"是") | AI生成 |
| notes | 备注 |

### XMind 映射

```
根节点（需求名称）
├── 模块节点（module_name）
│   └── 测试项节点（test_item）
│       └── 用例节点（name + priority图标）
│           ├── 测试项: {test_type}
│           ├── 前置条件: {preconditions}
│           ├── 步骤: 1 {action}
│           │   └── 预期结果: 1 {expected}
│           └── 备注: {notes}
```

---

## 测试类型列表

| 类型 | 说明 |
|-----|-----|
| 功能测试 | 业务逻辑验证（主体，50-60%） |
| 安全性测试 | 认证授权、攻击防护 |
| 性能测试 | 响应时间、并发能力 |
| 易用性测试 | 用户体验、界面交互 |
| 兼容性测试 | 跨环境运行 |
| 稳定性测试 | 长期运行稳定性 |
| 集成测试 | 模块间协作 |
| 可靠性测试 | 故障恢复 |
| 可维护性测试 | 运维能力 |
| 可移植性测试 | 迁移能力 |
| 埋点测试 | 数据上报 |
| AI效果测试 | AI 输出质量 |
| 硬件效果测试 | 硬件交互 |
