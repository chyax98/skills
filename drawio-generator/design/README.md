# DrawIO 复杂图表生成器 - 最终设计方案

> 版本: 1.0.0 | 日期: 2025-01-XX | 状态: 最终定稿

## 一、项目定位

构建一个专业的 DrawIO 图表生成 Skill，专注于**复杂图表**（30-50+ 节点），如：
- Transformer 架构图
- 大型微服务架构图
- LLM 训练流程图
- 企业级系统设计图

**核心原则**：
- 效果是唯一评判标准
- 不考虑 token 成本
- AI 负责理解，算法负责计算
- 复杂图表必须用工具链

---

## 二、核心架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              用户输入                                        │
│                   (文字描述 / 图片复刻 / 需求文档)                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Phase 1: 意图理解                                    │
│                         (01-intent-understanding.md)                        │
│  • 识别图表类型（架构图/流程图/UML/ER图/网络拓扑）                              │
│  • 评估复杂度（节点数、嵌套深度、连线密度）                                      │
│  • 输出：IntentResult                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Phase 2: 深度规划                                    │
│                         (02-deep-planning.md)                               │
│  • 生成递归式图表规格（GraphSpec）                                            │
│  • 定义节点、连线、嵌套关系                                                    │
│  • 指定布局策略和约束                                                         │
│  • 输出：GraphSpec (ELK 兼容格式)                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Phase 3: 知识检索                                    │
│                         (03-knowledge-retrieval.md)                         │
│  • 批量检索图标样式（AWS/Azure/K8s 等）                                       │
│  • 检索形状语法（mxGraph style 字符串）                                       │
│  • 匹配主题配色                                                              │
│  • 输出：StyleLibrary                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Phase 4: ELK 布局计算                                │
│                         (04-elk-layout.md)                                  │
│  • Python 桥接 → Node.js ELK                                                │
│  • 计算所有节点的精确坐标                                                      │
│  • 计算连线路径（正交路由、自动避让）                                           │
│  • 支持嵌套容器布局                                                           │
│  • 输出：LayoutResult                                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Phase 5: XML 生成                                    │
│                         (05-xml-generation.md)                              │
│  • 递归遍历布局结果                                                           │
│  • 生成 mxCell 节点（含样式）                                                 │
│  • 生成连线（含 waypoints）                                                  │
│  • 处理嵌套 parent 关系                                                      │
│  • 输出：DrawIO XML                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Phase 6: 验证修正                                    │
│                         (06-validation.md)                                  │
│  • XML 结构验证                                                              │
│  • 布局质量检查（重叠、间距、连线穿透）                                         │
│  • 迭代修复（最多 3 轮）                                                      │
│  • 输出：最终 .drawio 文件                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

                              参考文献
                         (07-references.md)
```

---

## 三、技术选型

| 组件 | 选型 | 理由 |
|------|------|------|
| **布局引擎** | ELK.js (elkjs) | 原生嵌套支持、正交路由、工业级 |
| **桥接方式** | Python subprocess → Node.js | 简单可靠、无需常驻服务 |
| **数据格式** | 递归 JSON (children 模型) | 支持无限嵌套、ELK 原生格式 |
| **输出格式** | DrawIO XML (.drawio) | 行业标准、可视化编辑 |

### 为什么选 ELK.js？

| 特性 | ELK.js | Python Grandalf | 自写 A* |
|------|--------|-----------------|---------|
| 嵌套支持 | ⭐⭐⭐ 原生 | ⭐ 基础 | ❌ |
| 正交路由 | ⭐⭐⭐ 内置 | ❌ | 复杂 |
| 维护成本 | 低 | 中 | 高 |
| 性能 | 高 (C++/JS) | 中 | 低 |

---

## 四、目录结构

```
design/
├── README.md                    # 本文件 - 总体架构
├── 01-intent-understanding.md   # Phase 1: 意图理解
├── 02-deep-planning.md          # Phase 2: 深度规划
├── 03-knowledge-retrieval.md    # Phase 3: 知识检索
├── 04-elk-layout.md             # Phase 4: ELK 布局计算
├── 05-xml-generation.md         # Phase 5: XML 生成
├── 06-validation.md             # Phase 6: 验证修正
└── 07-references.md             # 参考文献汇总
```

---

## 五、数据流

```
IntentResult ──→ GraphSpec ──→ StyleLibrary ──→ LayoutResult ──→ DrawIO XML
    │               │              │                │               │
  Phase 1        Phase 2        Phase 3          Phase 4         Phase 5-6
```

### 核心数据结构概览

```typescript
// Phase 1 输出
interface IntentResult {
  diagram_type: 'architecture' | 'flowchart' | 'uml' | 'sequence' | 'network';
  complexity: 'simple' | 'medium' | 'complex';
  estimated_nodes: number;
  has_nesting: boolean;
  description: string;
}

// Phase 2 输出 (ELK 兼容)
interface GraphSpec {
  id: string;
  labels: { text: string }[];
  children?: GraphSpec[];          // 递归嵌套
  edges?: EdgeSpec[];
  layoutOptions?: ELKLayoutOptions;
}

// Phase 3 输出
interface StyleLibrary {
  node_styles: { [nodeId: string]: string };  // mxGraph style 字符串
  edge_style: string;
  theme: ThemeColors;
}

// Phase 4 输出
interface LayoutResult {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  children?: LayoutResult[];
  edges?: LayoutEdge[];
}

// Phase 5 输出
// DrawIO XML 字符串
```

---

## 六、关键设计决策

### 决策 1: AI vs 算法的职责边界

| 职责 | 负责方 | 说明 |
|------|--------|------|
| 理解用户意图 | AI (Claude) | 自然语言理解 |
| 规划图表结构 | AI (Claude) | 决定有哪些节点、怎么连接 |
| 选择布局策略 | AI (Claude) | 决定用 layered/radial/tree |
| 计算精确坐标 | ELK 引擎 | 数学计算，AI 做不好 |
| 计算连线路径 | ELK 引擎 | 正交路由、避让 |
| 生成 XML | 代码模板 | 固定格式，无需 AI |

### 决策 2: 递归数据结构

**为什么用 `children[]` 而不是扁平 `nodes[]`？**

```json
// ❌ 扁平结构 - 无法表达嵌套
{
  "nodes": [
    {"id": "encoder", "type": "container"},
    {"id": "attn", "parent": "encoder"},
    {"id": "ffn", "parent": "encoder"}
  ]
}

// ✅ 递归结构 - 自然表达嵌套
{
  "id": "encoder",
  "children": [
    {"id": "attn"},
    {"id": "ffn"}
  ]
}
```

### 决策 3: Python-Node.js 桥接

```python
# layout_bridge.py
import subprocess
import json

def elk_layout(graph_spec: dict) -> dict:
    """调用 Node.js ELK 计算布局"""
    input_json = json.dumps(graph_spec)
    result = subprocess.run(
        ['node', 'elk_runner.js'],
        input=input_json,
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)
```

---

## 七、实施路线

| 阶段 | 任务 | 产出 |
|------|------|------|
| **Week 1** | 搭建 ELK 桥接 | elk_runner.js + layout_bridge.py |
| **Week 2** | 实现递归生成器 | generator_v2.py |
| **Week 3** | 集成知识检索 | knowledge_tool.py |
| **Week 4** | 端到端测试 | 10 个复杂图表用例 |
| **Week 5** | 优化迭代 | 验证器 + 修复逻辑 |

---

## 八、验收标准

| 指标 | 标准 | 检测方法 |
|------|------|---------|
| 节点不重叠 | 间距 ≥ 40px | 碰撞检测 |
| 连线不穿节点 | 使用正交路由 | ELK 保证 |
| 嵌套正确 | parent 关系正确 | XML 解析验证 |
| XML 有效 | DrawIO 可打开 | 实际打开测试 |
| 美观性 | 对齐、对称 | 人工审核 |

---

## 九、详细设计文档

请按顺序阅读：

1. [01-intent-understanding.md](./01-intent-understanding.md) - 意图理解
2. [02-deep-planning.md](./02-deep-planning.md) - 深度规划
3. [03-knowledge-retrieval.md](./03-knowledge-retrieval.md) - 知识检索
4. [04-elk-layout.md](./04-elk-layout.md) - ELK 布局计算
5. [05-xml-generation.md](./05-xml-generation.md) - XML 生成
6. [06-validation.md](./06-validation.md) - 验证修正
7. [07-references.md](./07-references.md) - 参考文献

---

## 十、快速开始

```bash
# 1. 安装依赖
npm install elkjs
pip install grandalf  # 备用

# 2. 测试 ELK 布局
echo '{"id":"root","children":[{"id":"n1","width":100,"height":50},{"id":"n2","width":100,"height":50}],"edges":[{"id":"e1","sources":["n1"],"targets":["n2"]}]}' | node scripts/elk_runner.js

# 3. 生成图表
python scripts/generate_diagram.py --input spec.json --output diagram.drawio
```
