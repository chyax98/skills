# Phase 2: 深度规划 (Deep Planning)

## 一、阶段目标

将意图理解结果转换为 ELK 兼容的递归图规格（GraphSpec），这是整个流程的核心规划阶段。

---

## 二、输入

来自 Phase 1 的 `IntentResult`：

```typescript
interface IntentResult {
  diagram_type: string;
  complexity: string;
  estimated_nodes: number;
  has_nesting: boolean;
  nesting_depth: number;
  entities: string[];
  relationships: Relationship[];
  layout_preference?: string;
  theme_preference?: string;
}
```

---

## 三、输出

### 3.1 GraphSpec 数据结构（ELK 兼容）

```typescript
/**
 * 核心数据结构：递归式图规格
 * 与 ELK JSON 格式完全兼容
 */
interface GraphSpec {
  // 唯一标识
  id: string;

  // 标签（显示文本）
  labels?: Array<{ text: string }>;

  // 节点尺寸（可选，ELK 会自动计算）
  width?: number;
  height?: number;

  // 节点类型（用于样式匹配）
  nodeType?: string;  // gateway, service, database, container, etc.

  // 递归嵌套：子节点
  children?: GraphSpec[];

  // 连线定义（定义在父节点层级）
  edges?: EdgeSpec[];

  // ELK 布局选项
  layoutOptions?: {
    'elk.algorithm'?: 'layered' | 'mrtree' | 'radial' | 'force' | 'stress';
    'elk.direction'?: 'DOWN' | 'UP' | 'RIGHT' | 'LEFT';
    'elk.spacing.nodeNode'?: string;
    'elk.layered.spacing.nodeNodeBetweenLayers'?: string;
    'elk.hierarchyHandling'?: 'INCLUDE_CHILDREN' | 'SEPARATE_CHILDREN';
    'elk.edgeRouting'?: 'ORTHOGONAL' | 'POLYLINE' | 'SPLINES';
    [key: string]: any;
  };

  // 端口定义（可选，用于精确控制连接点）
  ports?: PortSpec[];
}

interface EdgeSpec {
  id: string;
  sources: string[];  // 源节点 ID 列表
  targets: string[];  // 目标节点 ID 列表
  labels?: Array<{ text: string }>;
  edgeType?: 'arrow' | 'dashed' | 'bidirectional' | 'none';
}

interface PortSpec {
  id: string;
  width?: number;
  height?: number;
  // 端口位置约束
  layoutOptions?: {
    'elk.port.side'?: 'NORTH' | 'SOUTH' | 'EAST' | 'WEST';
  };
}
```

### 3.2 为什么用递归结构？

```
扁平结构 vs 递归结构

❌ 扁平结构（旧方案）:
{
  "nodes": [
    {"id": "encoder", "type": "container"},
    {"id": "mha", "parent": "encoder"},      // parent 隐式关系
    {"id": "ffn", "parent": "encoder"}
  ],
  "edges": [...]
}

问题：
- parent 关系隐式，容易出错
- 难以表达多层嵌套
- 与 ELK 格式不兼容，需要转换

✅ 递归结构（新方案）:
{
  "id": "encoder",
  "children": [                              // children 显式嵌套
    {"id": "mha"},
    {"id": "ffn"}
  ],
  "edges": [...]
}

优势：
- 嵌套关系直观
- 天然支持无限层级
- 与 ELK JSON 格式一致，无需转换
```

---

## 四、处理逻辑

### 4.1 Prompt 模板

```markdown
你是一个图表规划专家。请将意图分析结果转换为 ELK 兼容的递归图规格。

## 输入：意图分析结果
{intent_result_json}

## 规划任务

1. **构建递归节点树**
   - 根据 relationships 中的 "contains" 关系确定嵌套结构
   - 没有父节点的元素放在根层级
   - 支持多层嵌套

2. **规划连线**
   - 每条边在其源节点和目标节点的最近公共祖先层级定义
   - 边的 sources 和 targets 使用节点 ID

3. **设置布局选项**
   - 根据 diagram_type 选择默认算法：
     - architecture: layered + DOWN
     - flowchart: layered + DOWN
     - uml_sequence: layered + RIGHT
     - network: force
     - mindmap: mrtree
     - transformer: layered + DOWN
   - 根据 layout_preference 覆盖方向

4. **确定节点类型**
   根据实体名称推断类型，用于后续样式匹配：
   - 包含 "Gateway/API" → gateway
   - 包含 "Service/服务" → service
   - 包含 "MySQL/PostgreSQL/MongoDB/DB/数据库" → database
   - 包含 "Redis/Cache/缓存" → cache
   - 包含 "Queue/Kafka/RabbitMQ/消息" → queue
   - 包含 "User/用户/客户端" → user
   - 包含 "Block/Container/容器" → container
   - 其他 → default

5. **估算节点尺寸**
   - 普通节点：width 根据标签长度估算 (中文字符×14 + 英文字符×8 + 40)
   - 容器节点：由 ELK 自动计算

## 输出格式
严格输出 JSON：
```json
{
  "id": "root",
  "layoutOptions": {
    "elk.algorithm": "layered",
    "elk.direction": "DOWN",
    "elk.spacing.nodeNode": "40",
    "elk.hierarchyHandling": "INCLUDE_CHILDREN",
    "elk.edgeRouting": "ORTHOGONAL"
  },
  "children": [
    {
      "id": "node_id",
      "labels": [{"text": "显示文本"}],
      "nodeType": "service",
      "width": 120,
      "height": 60,
      "children": [],
      "edges": []
    }
  ],
  "edges": [
    {
      "id": "edge_id",
      "sources": ["source_node_id"],
      "targets": ["target_node_id"],
      "edgeType": "arrow"
    }
  ]
}
```
```

### 4.2 处理流程

```
IntentResult
    │
    ▼
┌─────────────────────────────────────┐
│  Step 1: 构建嵌套树                  │
│  • 遍历 relationships               │
│  • "contains" 关系 → 父子嵌套        │
│  • 其他关系 → 保留作为边              │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 2: 推断节点类型                │
│  • 根据实体名称关键词匹配             │
│  • 设置 nodeType 字段               │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 3: 估算节点尺寸                │
│  • 根据标签长度计算 width            │
│  • 容器节点不设尺寸（ELK 自动算）     │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 4: 选择布局算法                │
│  • 根据 diagram_type 设置默认值      │
│  • 应用 layout_preference 覆盖       │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 5: 组装 GraphSpec             │
│  • 构建递归 JSON 结构                │
│  • 验证 ID 唯一性                    │
│  • 验证边引用的节点存在               │
└─────────────────────────────────────┘
    │
    ▼
GraphSpec (ELK 兼容 JSON)
```

---

## 五、示例

### 示例 1: 微服务架构图

**输入 IntentResult**：
```json
{
  "diagram_type": "architecture",
  "entities": ["React", "Nginx", "API Gateway", "用户服务", "订单服务", "MySQL", "Redis"],
  "relationships": [
    {"source": "React", "target": "Nginx", "type": "connects"},
    {"source": "Nginx", "target": "API Gateway", "type": "connects"},
    {"source": "API Gateway", "target": "用户服务", "type": "connects"},
    {"source": "API Gateway", "target": "订单服务", "type": "connects"},
    {"source": "用户服务", "target": "MySQL", "type": "connects"},
    {"source": "订单服务", "target": "Redis", "type": "connects"}
  ],
  "layout_preference": "vertical"
}
```

**输出 GraphSpec**：
```json
{
  "id": "root",
  "layoutOptions": {
    "elk.algorithm": "layered",
    "elk.direction": "DOWN",
    "elk.spacing.nodeNode": "50",
    "elk.layered.spacing.nodeNodeBetweenLayers": "80",
    "elk.hierarchyHandling": "INCLUDE_CHILDREN",
    "elk.edgeRouting": "ORTHOGONAL"
  },
  "children": [
    {
      "id": "react",
      "labels": [{"text": "React"}],
      "nodeType": "client",
      "width": 100,
      "height": 50
    },
    {
      "id": "nginx",
      "labels": [{"text": "Nginx"}],
      "nodeType": "gateway",
      "width": 100,
      "height": 50
    },
    {
      "id": "api_gateway",
      "labels": [{"text": "API Gateway"}],
      "nodeType": "gateway",
      "width": 140,
      "height": 50
    },
    {
      "id": "user_service",
      "labels": [{"text": "用户服务"}],
      "nodeType": "service",
      "width": 120,
      "height": 60
    },
    {
      "id": "order_service",
      "labels": [{"text": "订单服务"}],
      "nodeType": "service",
      "width": 120,
      "height": 60
    },
    {
      "id": "mysql",
      "labels": [{"text": "MySQL"}],
      "nodeType": "database",
      "width": 100,
      "height": 70
    },
    {
      "id": "redis",
      "labels": [{"text": "Redis"}],
      "nodeType": "cache",
      "width": 100,
      "height": 50
    }
  ],
  "edges": [
    {"id": "e1", "sources": ["react"], "targets": ["nginx"], "edgeType": "arrow"},
    {"id": "e2", "sources": ["nginx"], "targets": ["api_gateway"], "edgeType": "arrow"},
    {"id": "e3", "sources": ["api_gateway"], "targets": ["user_service"], "edgeType": "arrow"},
    {"id": "e4", "sources": ["api_gateway"], "targets": ["order_service"], "edgeType": "arrow"},
    {"id": "e5", "sources": ["user_service"], "targets": ["mysql"], "edgeType": "arrow"},
    {"id": "e6", "sources": ["order_service"], "targets": ["redis"], "edgeType": "arrow"}
  ]
}
```

### 示例 2: Transformer Encoder（嵌套结构）

**输入 IntentResult**：
```json
{
  "diagram_type": "transformer",
  "has_nesting": true,
  "nesting_depth": 2,
  "entities": ["Encoder Block", "Multi-Head Attention", "Add & Norm 1", "FFN", "Add & Norm 2"],
  "relationships": [
    {"source": "Encoder Block", "target": "Multi-Head Attention", "type": "contains"},
    {"source": "Encoder Block", "target": "Add & Norm 1", "type": "contains"},
    {"source": "Encoder Block", "target": "FFN", "type": "contains"},
    {"source": "Encoder Block", "target": "Add & Norm 2", "type": "contains"},
    {"source": "Multi-Head Attention", "target": "Add & Norm 1", "type": "connects"},
    {"source": "Add & Norm 1", "target": "FFN", "type": "connects"},
    {"source": "FFN", "target": "Add & Norm 2", "type": "connects"}
  ]
}
```

**输出 GraphSpec**：
```json
{
  "id": "root",
  "layoutOptions": {
    "elk.algorithm": "layered",
    "elk.direction": "DOWN",
    "elk.hierarchyHandling": "INCLUDE_CHILDREN",
    "elk.edgeRouting": "ORTHOGONAL"
  },
  "children": [
    {
      "id": "encoder_block",
      "labels": [{"text": "Encoder Block"}],
      "nodeType": "container",
      "layoutOptions": {
        "elk.algorithm": "layered",
        "elk.direction": "DOWN",
        "elk.padding": "[top=40,left=20,bottom=20,right=20]"
      },
      "children": [
        {
          "id": "mha",
          "labels": [{"text": "Multi-Head Attention"}],
          "nodeType": "process",
          "width": 180,
          "height": 50
        },
        {
          "id": "add_norm_1",
          "labels": [{"text": "Add & Norm"}],
          "nodeType": "process",
          "width": 120,
          "height": 40
        },
        {
          "id": "ffn",
          "labels": [{"text": "Feed Forward Network"}],
          "nodeType": "process",
          "width": 180,
          "height": 50
        },
        {
          "id": "add_norm_2",
          "labels": [{"text": "Add & Norm"}],
          "nodeType": "process",
          "width": 120,
          "height": 40
        }
      ],
      "edges": [
        {"id": "e1", "sources": ["mha"], "targets": ["add_norm_1"], "edgeType": "arrow"},
        {"id": "e2", "sources": ["add_norm_1"], "targets": ["ffn"], "edgeType": "arrow"},
        {"id": "e3", "sources": ["ffn"], "targets": ["add_norm_2"], "edgeType": "arrow"}
      ]
    }
  ],
  "edges": []
}
```

---

## 六、ELK 布局选项详解

### 6.1 常用布局算法

| 算法 | 适用场景 | 说明 |
|------|---------|------|
| `layered` | 架构图、流程图、DAG | 分层布局，节点按层排列 |
| `mrtree` | 树形结构、思维导图 | 树形布局 |
| `radial` | 网络图、关系图 | 放射状布局 |
| `force` | 社交网络、无向图 | 力导向布局 |
| `stress` | 复杂网络 | 应力布局 |
| `rectpacking` | 容器内部布局 | 矩形打包 |

### 6.2 关键布局选项

```json
{
  // 布局算法
  "elk.algorithm": "layered",

  // 布局方向
  "elk.direction": "DOWN",  // DOWN, UP, RIGHT, LEFT

  // 节点间距
  "elk.spacing.nodeNode": "40",

  // 层间距
  "elk.layered.spacing.nodeNodeBetweenLayers": "80",

  // 嵌套处理方式
  "elk.hierarchyHandling": "INCLUDE_CHILDREN",  // INCLUDE_CHILDREN, SEPARATE_CHILDREN

  // 连线路由
  "elk.edgeRouting": "ORTHOGONAL",  // ORTHOGONAL, POLYLINE, SPLINES

  // 容器内边距
  "elk.padding": "[top=40,left=20,bottom=20,right=20]",

  // 端口约束
  "elk.portConstraints": "FIXED_SIDE",  // FREE, FIXED_SIDE, FIXED_ORDER, FIXED_POS

  // 节点对齐
  "elk.alignment": "CENTER"  // CENTER, TOP, BOTTOM
}
```

### 6.3 嵌套容器的特殊处理

```json
{
  "id": "container",
  "labels": [{"text": "容器标题"}],
  "layoutOptions": {
    // 容器内部使用独立的布局算法
    "elk.algorithm": "layered",
    "elk.direction": "DOWN",
    // 标题高度预留空间
    "elk.padding": "[top=50,left=20,bottom=20,right=20]"
  },
  "children": [
    // 子节点
  ],
  "edges": [
    // 容器内部的边
  ]
}
```

---

## 七、代码实现

### 7.1 deep_planner.py

```python
"""
Phase 2: 深度规划模块
"""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


class NodeType(str, Enum):
    GATEWAY = "gateway"
    SERVICE = "service"
    DATABASE = "database"
    CACHE = "cache"
    QUEUE = "queue"
    USER = "user"
    CLIENT = "client"
    CONTAINER = "container"
    PROCESS = "process"
    DECISION = "decision"
    DEFAULT = "default"


@dataclass
class GraphNode:
    id: str
    labels: List[Dict[str, str]]
    node_type: NodeType = NodeType.DEFAULT
    width: Optional[int] = None
    height: Optional[int] = None
    children: List['GraphNode'] = field(default_factory=list)
    edges: List['GraphEdge'] = field(default_factory=list)
    layout_options: Dict[str, Any] = field(default_factory=dict)
    ports: List[Dict] = field(default_factory=list)

    def to_elk_json(self) -> dict:
        """转换为 ELK JSON 格式"""
        result = {
            "id": self.id,
            "labels": self.labels,
            "nodeType": self.node_type.value
        }

        if self.width:
            result["width"] = self.width
        if self.height:
            result["height"] = self.height
        if self.children:
            result["children"] = [c.to_elk_json() for c in self.children]
        if self.edges:
            result["edges"] = [e.to_elk_json() for e in self.edges]
        if self.layout_options:
            result["layoutOptions"] = self.layout_options
        if self.ports:
            result["ports"] = self.ports

        return result


@dataclass
class GraphEdge:
    id: str
    sources: List[str]
    targets: List[str]
    edge_type: str = "arrow"
    labels: List[Dict[str, str]] = field(default_factory=list)

    def to_elk_json(self) -> dict:
        result = {
            "id": self.id,
            "sources": self.sources,
            "targets": self.targets,
            "edgeType": self.edge_type
        }
        if self.labels:
            result["labels"] = self.labels
        return result


class DeepPlanner:
    """深度规划器"""

    # 节点类型关键词映射
    TYPE_KEYWORDS = {
        NodeType.GATEWAY: ['gateway', 'api', 'nginx', 'kong', '网关'],
        NodeType.SERVICE: ['service', '服务', 'microservice', '微服务'],
        NodeType.DATABASE: ['mysql', 'postgresql', 'mongodb', 'database', 'db', '数据库'],
        NodeType.CACHE: ['redis', 'memcached', 'cache', '缓存'],
        NodeType.QUEUE: ['kafka', 'rabbitmq', 'queue', 'mq', '消息', '队列'],
        NodeType.USER: ['user', '用户', 'client', '客户端'],
        NodeType.CONTAINER: ['block', 'container', '容器', 'group', '组'],
        NodeType.PROCESS: ['process', '处理', 'handler', 'layer', '层'],
        NodeType.DECISION: ['decision', '判断', '条件', 'if', 'switch'],
    }

    # 图表类型 → 默认布局选项
    DIAGRAM_LAYOUTS = {
        'architecture': {
            'elk.algorithm': 'layered',
            'elk.direction': 'DOWN',
            'elk.spacing.nodeNode': '50',
            'elk.layered.spacing.nodeNodeBetweenLayers': '80',
        },
        'flowchart': {
            'elk.algorithm': 'layered',
            'elk.direction': 'DOWN',
            'elk.spacing.nodeNode': '40',
        },
        'uml_sequence': {
            'elk.algorithm': 'layered',
            'elk.direction': 'RIGHT',
            'elk.spacing.nodeNode': '60',
        },
        'network': {
            'elk.algorithm': 'force',
            'elk.spacing.nodeNode': '80',
        },
        'mindmap': {
            'elk.algorithm': 'mrtree',
            'elk.direction': 'RIGHT',
        },
        'transformer': {
            'elk.algorithm': 'layered',
            'elk.direction': 'DOWN',
            'elk.spacing.nodeNode': '30',
            'elk.layered.spacing.nodeNodeBetweenLayers': '60',
        },
    }

    def plan(self, intent_result: dict) -> dict:
        """
        将意图结果转换为 GraphSpec

        Args:
            intent_result: Phase 1 的输出

        Returns:
            ELK 兼容的 GraphSpec JSON
        """
        # 1. 构建节点映射
        entities = intent_result.get('entities', [])
        relationships = intent_result.get('relationships', [])

        nodes = {}
        for entity in entities:
            node_id = self._normalize_id(entity)
            nodes[entity] = GraphNode(
                id=node_id,
                labels=[{"text": entity}],
                node_type=self._infer_node_type(entity),
                width=self._estimate_width(entity),
                height=self._estimate_height(self._infer_node_type(entity))
            )

        # 2. 处理嵌套关系
        root_children = []
        for entity, node in nodes.items():
            is_child = False
            for rel in relationships:
                if rel['type'] == 'contains' and rel['target'] == entity:
                    # 这个节点是某个容器的子节点
                    parent = nodes.get(rel['source'])
                    if parent:
                        parent.children.append(node)
                        is_child = True
                        break
            if not is_child:
                root_children.append(node)

        # 3. 处理连线
        edges = []
        for i, rel in enumerate(relationships):
            if rel['type'] != 'contains':  # 非嵌套关系 = 连线
                src_node = nodes.get(rel['source'])
                tgt_node = nodes.get(rel['target'])
                if src_node and tgt_node:
                    edge = GraphEdge(
                        id=f"e{i}",
                        sources=[src_node.id],
                        targets=[tgt_node.id],
                        edge_type=self._infer_edge_type(rel)
                    )
                    edges.append(edge)

        # 4. 设置布局选项
        diagram_type = intent_result.get('diagram_type', 'architecture')
        layout_options = self.DIAGRAM_LAYOUTS.get(diagram_type, self.DIAGRAM_LAYOUTS['architecture']).copy()

        # 应用用户布局偏好
        layout_pref = intent_result.get('layout_preference')
        if layout_pref:
            direction_map = {
                'vertical': 'DOWN',
                'horizontal': 'RIGHT',
                'radial': 'radial'  # 需要切换算法
            }
            if layout_pref in direction_map:
                if layout_pref == 'radial':
                    layout_options['elk.algorithm'] = 'radial'
                else:
                    layout_options['elk.direction'] = direction_map[layout_pref]

        # 始终启用正交路由和嵌套支持
        layout_options['elk.hierarchyHandling'] = 'INCLUDE_CHILDREN'
        layout_options['elk.edgeRouting'] = 'ORTHOGONAL'

        # 5. 构建根节点
        root = GraphNode(
            id="root",
            labels=[{"text": intent_result.get('description', 'Diagram')}],
            children=root_children,
            edges=edges,
            layout_options=layout_options
        )

        return root.to_elk_json()

    def _normalize_id(self, name: str) -> str:
        """将名称转换为合法 ID"""
        import re
        # 移除特殊字符，空格转下划线
        id_str = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fff]', '_', name)
        id_str = id_str.strip('_').lower()
        return id_str or 'node'

    def _infer_node_type(self, name: str) -> NodeType:
        """根据名称推断节点类型"""
        name_lower = name.lower()
        for node_type, keywords in self.TYPE_KEYWORDS.items():
            if any(kw in name_lower for kw in keywords):
                return node_type
        return NodeType.DEFAULT

    def _estimate_width(self, label: str) -> int:
        """估算节点宽度"""
        # 中文字符 ≈ 14px，英文字符 ≈ 8px
        width = sum(14 if ord(c) > 127 else 8 for c in label)
        width += 40  # padding
        # 对齐到 10 的倍数
        width = ((width + 9) // 10) * 10
        return max(80, min(width, 300))

    def _estimate_height(self, node_type: NodeType) -> int:
        """估算节点高度"""
        heights = {
            NodeType.DATABASE: 70,
            NodeType.CONTAINER: None,  # 容器由 ELK 计算
            NodeType.DECISION: 60,
            NodeType.DEFAULT: 50,
        }
        return heights.get(node_type, 50)

    def _infer_edge_type(self, relationship: dict) -> str:
        """推断连线类型"""
        rel_type = relationship.get('type', 'connects')
        if rel_type == 'depends':
            return 'dashed'
        elif rel_type == 'extends':
            return 'arrow'
        else:
            return 'arrow'
```

---

## 八、与下一阶段的衔接

Phase 2 输出的 `GraphSpec` 将传递给：

1. **Phase 3（知识检索）**
   - 使用 `nodeType` 字段批量检索样式
   - 使用 `labels` 匹配图标

2. **Phase 4（ELK 布局）**
   - 直接传入 ELK 引擎计算坐标
   - `layoutOptions` 控制布局行为

---

## 九、参考

- [ELK JSON Format](https://eclipse.dev/elk/documentation/tooldevelopers/graphdatastructure/jsonformat.html)
- [ELK Layout Options](https://eclipse.dev/elk/reference/options.html)
- [elkjs GitHub](https://github.com/kieler/elkjs)
