# DrawIO 多 Agent 协作架构

## 系统概览

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Orchestrator (主控)                              │
│                    负责调度各 Agent，管理迭代循环                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│    Planner    │          │    Layout     │          │    Element    │
│     Agent     │          │     Agent     │          │     Agent     │
│  (需求规划)    │────────→│   (布局计算)   │────────→│  (元素匹配)    │
└───────────────┘          └───────────────┘          └───────────────┘
        │                           │                           │
        │                           │                           │
        │                           ▼                           │
        │                  ┌───────────────┐                    │
        │                  │   Generator   │◄───────────────────┘
        │                  │     Agent     │
        │                  │  (XML 生成)   │
        │                  └───────────────┘
        │                           │
        │                           ▼
        │                  ┌───────────────┐
        └─────────────────→│   Validator   │
                           │     Agent     │
                           │   (验证修正)   │
                           └───────────────┘
                                    │
                                    ▼
                           ┌───────────────┐
                           │   .drawio     │
                           │    输出文件    │
                           └───────────────┘
```

## Agent 定义

### 1. Planner Agent (需求规划)

**职责**: 理解用户意图，输出结构化的图表规格

**输入**:
```json
{
  "user_input": "画一个微服务架构图，包含网关、用户服务、订单服务、数据库",
  "image": null,  // 可选：base64 图片（复刻场景）
  "constraints": []  // 可选：额外约束
}
```

**输出** (DiagramSpec):
```json
{
  "diagram_type": "architecture",
  "title": "微服务架构图",
  "nodes": [
    {"id": "gw", "label": "API Gateway", "type": "gateway", "group": null},
    {"id": "user_svc", "label": "用户服务", "type": "service", "group": null},
    {"id": "order_svc", "label": "订单服务", "type": "service", "group": null},
    {"id": "db", "label": "MySQL", "type": "database", "group": null}
  ],
  "edges": [
    {"id": "e1", "source": "gw", "target": "user_svc", "label": null, "type": "arrow"},
    {"id": "e2", "source": "gw", "target": "order_svc", "label": null, "type": "arrow"},
    {"id": "e3", "source": "user_svc", "target": "db", "label": null, "type": "arrow"},
    {"id": "e4", "source": "order_svc", "target": "db", "label": null, "type": "arrow"}
  ],
  "groups": [],
  "layout_hint": "vertical",
  "theme": "professional"
}
```

**工具**: `scripts/planner.py` 或 Sub-Agent prompt

---

### 2. Layout Agent (布局计算)

**职责**: 计算每个节点的精确位置

**输入** (DiagramSpec + LayoutConfig):
```json
{
  "spec": { /* DiagramSpec from Planner */ },
  "config": {
    "canvas_width": 800,
    "canvas_height": 600,
    "node_width": 120,
    "node_height": 60,
    "spacing": 120,
    "margin": 40,
    "algorithm": "layered"  // layered | force | radial | grid
  }
}
```

**输出** (LayoutResult):
```json
{
  "nodes": [
    {"id": "gw", "x": 340, "y": 40, "width": 120, "height": 60},
    {"id": "user_svc", "x": 160, "y": 200, "width": 120, "height": 60},
    {"id": "order_svc", "x": 520, "y": 200, "width": 120, "height": 60},
    {"id": "db", "x": 340, "y": 360, "width": 120, "height": 60}
  ],
  "edges": [
    {
      "id": "e1", "source": "gw", "target": "user_svc",
      "exit": {"x": 0.3, "y": 1}, "entry": {"x": 0.5, "y": 0},
      "waypoints": []
    },
    {
      "id": "e2", "source": "gw", "target": "order_svc",
      "exit": {"x": 0.7, "y": 1}, "entry": {"x": 0.5, "y": 0},
      "waypoints": []
    }
    // ...
  ],
  "canvas": {"width": 800, "height": 600},
  "algorithm_used": "layered"
}
```

**工具**: `scripts/layout_agent.py`
- 内置简单布局算法
- 可选集成 ELK (通过 Node.js)

---

### 3. Element Agent (元素匹配)

**职责**: 为每个节点匹配 DrawIO 形状和样式

**输入** (DiagramSpec + Theme):
```json
{
  "nodes": [
    {"id": "gw", "label": "API Gateway", "type": "gateway"},
    {"id": "db", "label": "MySQL", "type": "database"}
  ],
  "theme": "professional",
  "custom_styles": {}  // 可选覆盖
}
```

**输出** (ElementStyles):
```json
{
  "node_styles": {
    "gw": {
      "shape": "rounded_rect",
      "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;shadow=1;arcSize=20;"
    },
    "db": {
      "shape": "cylinder",
      "style": "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#f5f5f5;strokeColor=#666666;"
    }
  },
  "edge_style": "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;strokeColor=#666666;",
  "theme_applied": "professional"
}
```

**工具**: `scripts/element_agent.py`
- 基于 references/shapes.md, icons.md, color_schemes.md
- 关键词匹配 + 规则映射

---

### 4. Generator Agent (XML 生成)

**职责**: 将布局和样式合成为 DrawIO XML

**输入** (LayoutResult + ElementStyles + DiagramSpec):
```json
{
  "layout": { /* LayoutResult */ },
  "styles": { /* ElementStyles */ },
  "spec": { /* DiagramSpec - for labels */ }
}
```

**输出** (DrawioXML):
```json
{
  "xml": "<?xml version=\"1.0\"?><mxfile>...</mxfile>",
  "stats": {
    "nodes": 4,
    "edges": 4,
    "groups": 0
  }
}
```

**工具**: `scripts/generator_agent.py`
- 严格遵循 XML 规范
- 模板化生成

---

### 5. Validator Agent (验证修正)

**职责**: 验证 XML 质量，提供修复建议

**输入** (DrawioXML + DiagramSpec):
```json
{
  "xml": "...",
  "spec": { /* DiagramSpec - for coverage check */ }
}
```

**输出** (ValidationResult):
```json
{
  "passed": true,
  "score": 95,
  "errors": [],
  "warnings": [
    {"code": "W001", "message": "节点 user_svc 与 order_svc 间距较小", "fix": "增加 spacing"}
  ],
  "coverage": {
    "nodes": {"expected": 4, "found": 4, "missing": []},
    "edges": {"expected": 4, "found": 4, "missing": []}
  }
}
```

**工具**: `scripts/validate_drawio.py` (已有，需增强)

---

## 执行流程

```
Phase 1: Planning
─────────────────
Orchestrator 调用 Planner Agent
├── 输入: user_input
├── 输出: DiagramSpec
└── 检查点: spec 是否完整（nodes, edges 非空）

Phase 2: Layout
─────────────────
Orchestrator 调用 Layout Agent
├── 输入: DiagramSpec + LayoutConfig
├── 输出: LayoutResult
└── 检查点: 所有节点有位置，无重叠

Phase 3: Styling
─────────────────
Orchestrator 调用 Element Agent
├── 输入: DiagramSpec + Theme
├── 输出: ElementStyles
└── 检查点: 所有节点有样式

Phase 4: Generation
─────────────────
Orchestrator 调用 Generator Agent
├── 输入: LayoutResult + ElementStyles + DiagramSpec
├── 输出: DrawioXML
└── 检查点: XML 可解析

Phase 5: Validation
─────────────────
Orchestrator 调用 Validator Agent
├── 输入: DrawioXML + DiagramSpec
├── 输出: ValidationResult
├── 如果 passed=false 且 iteration < max:
│   └── 根据 errors 调整，返回 Phase 2 或 Phase 3
└── 如果 passed=true:
    └── 输出最终 .drawio 文件
```

## Agent 实现方式

### 方式 A: Python 脚本 (Agent as Tool)

每个 Agent 是一个独立的 Python 脚本：

```bash
# 调用 Planner
python scripts/planner.py --input request.json --output spec.json

# 调用 Layout
python scripts/layout_agent.py --spec spec.json --output layout.json

# 调用 Element
python scripts/element_agent.py --spec spec.json --theme professional --output styles.json

# 调用 Generator
python scripts/generator_agent.py --layout layout.json --styles styles.json --spec spec.json --output diagram.drawio

# 调用 Validator
python scripts/validate_drawio.py diagram.drawio --spec spec.json
```

**优点**: 确定性强，可独立测试
**缺点**: Planner 需要 LLM，纯脚本难以实现

### 方式 B: Sub-Agent (Claude Task)

在 SKILL.md 中定义，由 Claude 使用 Task tool 调用：

```markdown
## Agent 调用

### 调用 Planner Agent
使用 Task tool，subagent_type=general-purpose:
- prompt: "分析用户需求，输出 DiagramSpec JSON..."
- 返回: DiagramSpec

### 调用 Layout Agent
使用 Bash 执行:
- `python scripts/layout_agent.py --spec spec.json`
- 返回: LayoutResult
```

**优点**: Planner 可用 LLM，灵活
**缺点**: 上下文消耗大

### 方式 C: 混合模式 (推荐)

- **Planner**: Sub-Agent (需要 LLM 理解语义)
- **Layout**: Python 脚本 (确定性算法)
- **Element**: Python 脚本 (规则匹配)
- **Generator**: Python 脚本 (模板生成)
- **Validator**: Python 脚本 (规则检查)

---

## 数据格式规范

### DiagramSpec (规划输出)

```typescript
interface DiagramSpec {
  diagram_type: 'flowchart' | 'architecture' | 'uml' | 'er' | 'network' | 'mindmap';
  title: string;
  nodes: NodeSpec[];
  edges: EdgeSpec[];
  groups: GroupSpec[];
  layout_hint: 'horizontal' | 'vertical' | 'radial' | 'grid' | 'auto';
  theme: 'professional' | 'tech' | 'minimal' | 'colorful' | 'dark';
}

interface NodeSpec {
  id: string;
  label: string;
  type: string;  // gateway, service, database, user, decision, process, ...
  group?: string;
  icon?: string;
}

interface EdgeSpec {
  id: string;
  source: string;
  target: string;
  label?: string;
  type: 'arrow' | 'dashed' | 'bidirectional';
}

interface GroupSpec {
  id: string;
  label: string;
  members: string[];
}
```

### LayoutResult (布局输出)

```typescript
interface LayoutResult {
  nodes: NodePosition[];
  edges: EdgePath[];
  canvas: { width: number; height: number };
  algorithm_used: string;
}

interface NodePosition {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

interface EdgePath {
  id: string;
  source: string;
  target: string;
  exit: { x: number; y: number };  // 0-1
  entry: { x: number; y: number }; // 0-1
  waypoints: { x: number; y: number }[];
}
```

### ElementStyles (样式输出)

```typescript
interface ElementStyles {
  node_styles: { [id: string]: NodeStyle };
  edge_style: string;
  theme_applied: string;
}

interface NodeStyle {
  shape: string;
  style: string;  // DrawIO style string
}
```

---

## 迭代策略

```
最大迭代次数: 3

迭代触发条件:
├── 验证失败 (passed=false)
│   ├── 结构错误 → 重新生成 (Phase 4)
│   ├── 布局问题 → 调整布局 (Phase 2)
│   └── 覆盖不全 → 重新规划 (Phase 1)
│
└── 分数过低 (score < 80)
    └── 根据 warnings 微调

反馈传递:
├── Validator → Layout: 增加间距、调整位置
├── Validator → Element: 更换样式
└── Validator → Planner: 补充缺失节点
```
