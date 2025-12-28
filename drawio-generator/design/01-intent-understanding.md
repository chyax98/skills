# Phase 1: 意图理解 (Intent Understanding)

## 一、阶段目标

分析用户输入，识别图表类型和复杂度，为后续阶段提供决策依据。

---

## 二、输入

| 输入类型 | 说明 | 示例 |
|---------|------|------|
| 文字描述 | 自然语言描述图表需求 | "画一个微服务架构图，包含 API Gateway、用户服务、订单服务、MySQL 和 Redis" |
| 图片 | 需要复刻的现有图表 | 上传的 PNG/JPG 图片 |
| 需求文档 | 结构化的需求说明 | Markdown 或 JSON 格式 |

---

## 三、输出

### 3.1 IntentResult 数据结构

```typescript
interface IntentResult {
  // 图表类型
  diagram_type:
    | 'architecture'  // 架构图（微服务、系统设计）
    | 'flowchart'     // 流程图（业务流程、算法流程）
    | 'uml_class'     // UML 类图
    | 'uml_sequence'  // UML 时序图
    | 'er'            // ER 图（数据库设计）
    | 'network'       // 网络拓扑图
    | 'mindmap'       // 思维导图
    | 'transformer';  // Transformer/神经网络架构

  // 复杂度评估
  complexity: 'simple' | 'medium' | 'complex';

  // 预估节点数量
  estimated_nodes: number;

  // 是否包含嵌套结构
  has_nesting: boolean;

  // 嵌套深度（0 = 无嵌套）
  nesting_depth: number;

  // 预估连线数量
  estimated_edges: number;

  // 是否有循环依赖
  has_cycles: boolean;

  // 用户描述的结构化理解
  description: string;

  // 关键实体提取
  entities: string[];

  // 关系提取
  relationships: Array<{
    source: string;
    target: string;
    type: string;  // "connects" | "contains" | "extends" | "depends"
  }>;

  // 布局偏好（如果用户明确指定）
  layout_preference?: 'vertical' | 'horizontal' | 'radial' | 'auto';

  // 主题偏好
  theme_preference?: 'professional' | 'tech' | 'minimal' | 'colorful' | 'dark';
}
```

### 3.2 复杂度判断标准

| 复杂度 | 节点数 | 嵌套深度 | 连线密度 | 处理方式 |
|--------|--------|---------|---------|---------|
| simple | ≤ 10 | 0 | 低 | 可选：直接生成 |
| medium | 11-30 | 1 | 中 | 必须：使用工具链 |
| complex | 31+ | 2+ | 高 | 必须：使用工具链 + 分块 |

---

## 四、处理逻辑

### 4.1 Prompt 模板

```markdown
你是一个图表需求分析专家。请分析用户的图表需求，输出结构化的意图识别结果。

## 用户输入
{user_input}

## 分析任务

1. **识别图表类型**
   - architecture: 系统架构图、微服务架构、云架构
   - flowchart: 业务流程、算法流程、审批流程
   - uml_class: 类图、接口图
   - uml_sequence: 时序图、交互图
   - er: 数据库表关系图
   - network: 网络拓扑、部署图
   - mindmap: 思维导图、知识图谱
   - transformer: 神经网络架构、AI 模型结构

2. **提取关键实体**
   列出所有提到的节点/组件名称

3. **识别关系类型**
   - connects: A 连接到 B（普通连线）
   - contains: A 包含 B（嵌套/容器）
   - extends: A 继承 B（UML）
   - depends: A 依赖 B（依赖关系）

4. **评估复杂度**
   根据节点数、嵌套深度、连线密度判断

5. **识别布局偏好**
   如果用户提到"从上到下"、"水平"、"放射状"等词汇

## 输出格式
严格输出 JSON，无其他文字：
```json
{
  "diagram_type": "...",
  "complexity": "...",
  "estimated_nodes": 0,
  "has_nesting": false,
  "nesting_depth": 0,
  "estimated_edges": 0,
  "has_cycles": false,
  "description": "...",
  "entities": [],
  "relationships": [],
  "layout_preference": null,
  "theme_preference": null
}
```
```

### 4.2 处理流程

```
用户输入
    │
    ▼
┌─────────────────────────────────────┐
│  Step 1: 输入预处理                  │
│  • 清理输入文本                      │
│  • 如果是图片，调用视觉理解          │
│  • 如果是文档，提取关键信息          │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 2: LLM 意图识别               │
│  • 使用 Prompt 模板调用 Claude      │
│  • 解析 JSON 输出                   │
│  • 验证必填字段                     │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 3: 复杂度校准                  │
│  • 根据实体数量校准 estimated_nodes  │
│  • 检测嵌套关键词（"包含"、"内部"）   │
│  • 检测循环关键词（"回调"、"反馈"）   │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 4: 决策输出                    │
│  • 如果 complexity = simple 且       │
│    用户要求快速，可跳过工具链        │
│  • 否则进入 Phase 2                 │
└─────────────────────────────────────┘
```

---

## 五、示例

### 示例 1: 微服务架构图

**用户输入**：
```
画一个微服务架构图。前端是 React，通过 Nginx 代理访问 API Gateway。
Gateway 后面有用户服务、订单服务、支付服务三个微服务。
用户服务连 MySQL，订单服务连 PostgreSQL，支付服务连 Redis 缓存。
所有服务都注册到 Eureka。
```

**输出**：
```json
{
  "diagram_type": "architecture",
  "complexity": "medium",
  "estimated_nodes": 11,
  "has_nesting": false,
  "nesting_depth": 0,
  "estimated_edges": 10,
  "has_cycles": false,
  "description": "微服务架构图，包含前端、网关、3个微服务、3个数据库和服务注册中心",
  "entities": [
    "React", "Nginx", "API Gateway",
    "用户服务", "订单服务", "支付服务",
    "MySQL", "PostgreSQL", "Redis", "Eureka"
  ],
  "relationships": [
    {"source": "React", "target": "Nginx", "type": "connects"},
    {"source": "Nginx", "target": "API Gateway", "type": "connects"},
    {"source": "API Gateway", "target": "用户服务", "type": "connects"},
    {"source": "API Gateway", "target": "订单服务", "type": "connects"},
    {"source": "API Gateway", "target": "支付服务", "type": "connects"},
    {"source": "用户服务", "target": "MySQL", "type": "connects"},
    {"source": "订单服务", "target": "PostgreSQL", "type": "connects"},
    {"source": "支付服务", "target": "Redis", "type": "connects"},
    {"source": "用户服务", "target": "Eureka", "type": "connects"},
    {"source": "订单服务", "target": "Eureka", "type": "connects"},
    {"source": "支付服务", "target": "Eureka", "type": "connects"}
  ],
  "layout_preference": "vertical",
  "theme_preference": "professional"
}
```

### 示例 2: Transformer Encoder

**用户输入**：
```
画一个 Transformer Encoder Block 的内部结构。
包含 Multi-Head Attention 和 Feed Forward Network 两个子模块。
每个子模块都有 Add & Norm 层。
输入先进入 Multi-Head Attention，输出和输入做残差连接，然后 Layer Norm。
再进入 FFN，同样做残差和 Norm。
```

**输出**：
```json
{
  "diagram_type": "transformer",
  "complexity": "medium",
  "estimated_nodes": 8,
  "has_nesting": true,
  "nesting_depth": 2,
  "estimated_edges": 8,
  "has_cycles": false,
  "description": "Transformer Encoder Block 内部结构，包含 MHA 和 FFN 两个子模块，每个带残差连接和 Layer Norm",
  "entities": [
    "Encoder Block",
    "Multi-Head Attention", "Add & Norm 1",
    "Feed Forward Network", "Add & Norm 2",
    "Input", "Output"
  ],
  "relationships": [
    {"source": "Encoder Block", "target": "Multi-Head Attention", "type": "contains"},
    {"source": "Encoder Block", "target": "Add & Norm 1", "type": "contains"},
    {"source": "Encoder Block", "target": "Feed Forward Network", "type": "contains"},
    {"source": "Encoder Block", "target": "Add & Norm 2", "type": "contains"},
    {"source": "Input", "target": "Multi-Head Attention", "type": "connects"},
    {"source": "Multi-Head Attention", "target": "Add & Norm 1", "type": "connects"},
    {"source": "Add & Norm 1", "target": "Feed Forward Network", "type": "connects"},
    {"source": "Feed Forward Network", "target": "Add & Norm 2", "type": "connects"},
    {"source": "Add & Norm 2", "target": "Output", "type": "connects"}
  ],
  "layout_preference": "vertical",
  "theme_preference": "tech"
}
```

---

## 六、边界情况处理

### 6.1 模糊输入

**输入**："帮我画个图"

**处理**：
1. 识别为不完整输入
2. 返回澄清问题：
   - "请问您想画什么类型的图表？"
   - "请描述图表中需要包含哪些元素？"

### 6.2 图片复刻

**输入**：用户上传图片

**处理**：
1. 调用视觉模型理解图片内容
2. 提取图片中的节点和连线
3. 生成等效的 IntentResult
4. 在 description 中标注"复刻自用户上传图片"

### 6.3 超复杂输入

**输入**：描述了 100+ 节点的复杂系统

**处理**：
1. 设置 complexity = "complex"
2. 在后续阶段启用分块处理
3. 可能需要用户确认分组/分层策略

---

## 七、代码实现

### 7.1 intent_analyzer.py

```python
"""
Phase 1: 意图理解模块
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Optional
from enum import Enum


class DiagramType(str, Enum):
    ARCHITECTURE = "architecture"
    FLOWCHART = "flowchart"
    UML_CLASS = "uml_class"
    UML_SEQUENCE = "uml_sequence"
    ER = "er"
    NETWORK = "network"
    MINDMAP = "mindmap"
    TRANSFORMER = "transformer"


class Complexity(str, Enum):
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


@dataclass
class Relationship:
    source: str
    target: str
    type: str  # connects, contains, extends, depends


@dataclass
class IntentResult:
    diagram_type: DiagramType
    complexity: Complexity
    estimated_nodes: int
    has_nesting: bool
    nesting_depth: int
    estimated_edges: int
    has_cycles: bool
    description: str
    entities: List[str]
    relationships: List[Relationship]
    layout_preference: Optional[str] = None
    theme_preference: Optional[str] = None

    def to_dict(self) -> dict:
        result = asdict(self)
        result['diagram_type'] = self.diagram_type.value
        result['complexity'] = self.complexity.value
        return result


class IntentAnalyzer:
    """意图分析器"""

    PROMPT_TEMPLATE = '''你是一个图表需求分析专家。请分析用户的图表需求。

## 用户输入
{user_input}

## 输出格式
严格输出 JSON：
```json
{{
  "diagram_type": "architecture|flowchart|uml_class|uml_sequence|er|network|mindmap|transformer",
  "complexity": "simple|medium|complex",
  "estimated_nodes": <数字>,
  "has_nesting": <true|false>,
  "nesting_depth": <数字>,
  "estimated_edges": <数字>,
  "has_cycles": <true|false>,
  "description": "<描述>",
  "entities": ["<实体1>", "<实体2>"],
  "relationships": [
    {{"source": "<源>", "target": "<目标>", "type": "connects|contains|extends|depends"}}
  ],
  "layout_preference": "vertical|horizontal|radial|null",
  "theme_preference": "professional|tech|minimal|colorful|dark|null"
}}
```'''

    def analyze(self, user_input: str) -> IntentResult:
        """
        分析用户输入，返回意图结果

        在实际实现中，这里会调用 Claude API
        """
        prompt = self.PROMPT_TEMPLATE.format(user_input=user_input)

        # TODO: 调用 Claude API
        # response = claude.complete(prompt)
        # result_json = extract_json(response)

        # 解析并返回
        # return self._parse_result(result_json)
        pass

    def _parse_result(self, result_json: dict) -> IntentResult:
        """解析 JSON 结果为 IntentResult"""
        relationships = [
            Relationship(**r) for r in result_json.get('relationships', [])
        ]

        return IntentResult(
            diagram_type=DiagramType(result_json['diagram_type']),
            complexity=Complexity(result_json['complexity']),
            estimated_nodes=result_json['estimated_nodes'],
            has_nesting=result_json['has_nesting'],
            nesting_depth=result_json['nesting_depth'],
            estimated_edges=result_json['estimated_edges'],
            has_cycles=result_json['has_cycles'],
            description=result_json['description'],
            entities=result_json['entities'],
            relationships=relationships,
            layout_preference=result_json.get('layout_preference'),
            theme_preference=result_json.get('theme_preference')
        )

    def _calibrate_complexity(self, result: IntentResult) -> IntentResult:
        """根据实体数量校准复杂度"""
        node_count = len(result.entities)

        if node_count <= 10 and result.nesting_depth == 0:
            result.complexity = Complexity.SIMPLE
        elif node_count <= 30 and result.nesting_depth <= 1:
            result.complexity = Complexity.MEDIUM
        else:
            result.complexity = Complexity.COMPLEX

        result.estimated_nodes = node_count
        return result
```

---

## 八、与下一阶段的衔接

Phase 1 输出的 `IntentResult` 将传递给 Phase 2（深度规划），用于：

1. **决定规划策略**
   - 根据 `diagram_type` 选择适合的规划模板
   - 根据 `complexity` 决定是否分块处理

2. **初始化节点列表**
   - `entities` 作为初始节点候选
   - `relationships` 作为连线候选

3. **设置布局参数**
   - `layout_preference` 传递给 ELK
   - `theme_preference` 传递给样式匹配

---

## 九、参考

- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Anthropic Claude Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
