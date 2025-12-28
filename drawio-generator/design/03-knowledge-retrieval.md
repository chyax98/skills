# Phase 3: 知识检索 (Knowledge Retrieval)

## 一、阶段目标

根据规划结果，批量检索所需的样式信息，包括图标、形状、配色，输出可直接使用的 mxGraph style 字符串。

---

## 二、输入

来自 Phase 2 的 `GraphSpec`：

```typescript
interface GraphSpec {
  id: string;
  children?: GraphSpec[];
  edges?: EdgeSpec[];
  // 每个节点的 nodeType 用于样式匹配
}
```

---

## 三、输出

### 3.1 StyleLibrary 数据结构

```typescript
interface StyleLibrary {
  // 节点样式映射：nodeId → mxGraph style 字符串
  node_styles: {
    [nodeId: string]: {
      shape: string;           // 形状名称
      style: string;           // 完整的 mxGraph style 字符串
      width: number;           // 推荐宽度
      height: number;          // 推荐高度
      icon?: string;           // 图标路径（如果有）
    }
  };

  // 边样式
  edge_styles: {
    arrow: string;
    dashed: string;
    bidirectional: string;
    none: string;
  };

  // 主题配色
  theme: {
    name: string;
    primary: ThemeColor;
    secondary: ThemeColor;
    accent: ThemeColor;
    neutral: ThemeColor;
    danger: ThemeColor;
  };
}

interface ThemeColor {
  fill: string;      // 填充色
  stroke: string;    // 边框色
  font: string;      // 文字色
  gradient?: string; // 渐变色（可选）
}
```

---

## 四、知识库结构

### 4.1 现有知识文件

```
references/
├── shapes.md          # 基础形状语法
├── edges.md           # 连线语法
├── icons.md           # 图标库指南
├── color_schemes.md   # 配色方案
├── ai_ml_assets.md    # AI/ML 专用素材
├── uml.md             # UML 图形
├── devops.md          # DevOps/云服务图标
├── business.md        # 业务流程图标
└── network.md         # 网络拓扑图标
```

### 4.2 形状库（内置）

```python
SHAPE_LIBRARY = {
    # 基础形状
    'rect': 'rounded=0;whiteSpace=wrap;html=1;',
    'rounded_rect': 'rounded=1;whiteSpace=wrap;html=1;arcSize=20;',
    'ellipse': 'ellipse;whiteSpace=wrap;html=1;',
    'diamond': 'rhombus;whiteSpace=wrap;html=1;',
    'cylinder': 'shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;size=10;',
    'hexagon': 'shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;',
    'parallelogram': 'shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;',
    'document': 'shape=document;whiteSpace=wrap;html=1;',
    'cloud': 'ellipse;shape=cloud;whiteSpace=wrap;html=1;',
    'actor': 'shape=actor;whiteSpace=wrap;html=1;',

    # 容器
    'container': 'rounded=1;whiteSpace=wrap;html=1;container=1;collapsible=0;',
    'swimlane': 'swimlane;whiteSpace=wrap;html=1;',

    # 特殊形状
    'database': 'shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;',
    'queue': 'shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;',
    'cache': 'rounded=1;whiteSpace=wrap;html=1;arcSize=40;',
}

# 节点类型 → 形状映射
TYPE_TO_SHAPE = {
    'gateway': 'rounded_rect',
    'service': 'rounded_rect',
    'database': 'cylinder',
    'cache': 'rounded_rect',
    'queue': 'parallelogram',
    'user': 'ellipse',
    'client': 'rounded_rect',
    'container': 'container',
    'process': 'rounded_rect',
    'decision': 'diamond',
    'default': 'rounded_rect',
}
```

### 4.3 主题配色

```python
THEMES = {
    'professional': {
        'name': 'Professional',
        'primary': {'fill': '#dae8fc', 'stroke': '#6c8ebf', 'font': '#333333'},
        'secondary': {'fill': '#d5e8d4', 'stroke': '#82b366', 'font': '#333333'},
        'accent': {'fill': '#fff2cc', 'stroke': '#d6b656', 'font': '#333333'},
        'neutral': {'fill': '#f5f5f5', 'stroke': '#666666', 'font': '#333333'},
        'danger': {'fill': '#f8cecc', 'stroke': '#b85450', 'font': '#333333'},
    },
    'tech': {
        'name': 'Tech',
        'primary': {'fill': '#1565C0', 'stroke': 'none', 'font': '#FFFFFF', 'gradient': '#0D47A1'},
        'secondary': {'fill': '#26A69A', 'stroke': 'none', 'font': '#FFFFFF', 'gradient': '#00897B'},
        'accent': {'fill': '#FF7043', 'stroke': 'none', 'font': '#FFFFFF', 'gradient': '#E64A19'},
        'neutral': {'fill': '#37474F', 'stroke': 'none', 'font': '#FFFFFF', 'gradient': '#263238'},
        'danger': {'fill': '#E53935', 'stroke': 'none', 'font': '#FFFFFF', 'gradient': '#C62828'},
    },
    'minimal': {
        'name': 'Minimal',
        'primary': {'fill': '#FFFFFF', 'stroke': '#333333', 'font': '#333333'},
        'secondary': {'fill': '#FAFAFA', 'stroke': '#666666', 'font': '#333333'},
        'accent': {'fill': '#E3F2FD', 'stroke': '#1976D2', 'font': '#333333'},
        'neutral': {'fill': '#FFFFFF', 'stroke': '#9E9E9E', 'font': '#666666'},
        'danger': {'fill': '#FFEBEE', 'stroke': '#C62828', 'font': '#333333'},
    },
    'dark': {
        'name': 'Dark',
        'primary': {'fill': '#1E1E1E', 'stroke': '#3C3C3C', 'font': '#FFFFFF'},
        'secondary': {'fill': '#252526', 'stroke': '#3C3C3C', 'font': '#FFFFFF'},
        'accent': {'fill': '#0E639C', 'stroke': '#1177BB', 'font': '#FFFFFF'},
        'neutral': {'fill': '#2D2D2D', 'stroke': '#3C3C3C', 'font': '#CCCCCC'},
        'danger': {'fill': '#5A1D1D', 'stroke': '#8B2B2B', 'font': '#FFFFFF'},
    },
}

# 节点类型 → 颜色角色映射
TYPE_TO_COLOR = {
    'gateway': 'secondary',
    'service': 'primary',
    'database': 'neutral',
    'cache': 'accent',
    'queue': 'secondary',
    'user': 'neutral',
    'client': 'primary',
    'container': 'neutral',
    'process': 'primary',
    'decision': 'accent',
    'default': 'primary',
}
```

---

## 五、处理逻辑

### 5.1 处理流程

```
GraphSpec
    │
    ▼
┌─────────────────────────────────────┐
│  Step 1: 提取所有节点类型            │
│  • 递归遍历 children                 │
│  • 收集所有 nodeType                │
│  • 去重                             │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 2: 形状匹配                    │
│  • nodeType → shape 映射            │
│  • 获取基础 style 字符串             │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 3: 主题应用                    │
│  • 获取主题配色                      │
│  • nodeType → color role 映射       │
│  • 组合成完整 style                  │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 4: 高级检索（可选）            │
│  • 检索云服务图标（AWS/Azure/GCP）   │
│  • 检索专业图标（K8s/Docker）        │
│  • 使用语义搜索匹配                  │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 5: 边样式生成                  │
│  • 根据主题生成边颜色                │
│  • 生成各类型边的 style              │
└─────────────────────────────────────┘
    │
    ▼
StyleLibrary
```

### 5.2 Style 字符串组装

```python
def build_style(shape: str, colors: dict, is_container: bool = False) -> str:
    """
    组装完整的 mxGraph style 字符串

    Args:
        shape: 形状基础样式
        colors: 颜色配置 {fill, stroke, font, gradient?}
        is_container: 是否是容器节点

    Returns:
        完整的 style 字符串
    """
    parts = [SHAPE_LIBRARY[shape].rstrip(';')]

    # 填充色
    if colors.get('fill'):
        parts.append(f"fillColor={colors['fill']}")

    # 渐变色
    if colors.get('gradient'):
        parts.append(f"gradientColor={colors['gradient']}")
        parts.append("gradientDirection=south")

    # 边框色
    if colors.get('stroke'):
        if colors['stroke'] == 'none':
            parts.append("strokeColor=none")
        else:
            parts.append(f"strokeColor={colors['stroke']}")

    # 文字色
    if colors.get('font'):
        parts.append(f"fontColor={colors['font']}")

    # 容器特殊属性
    if is_container:
        parts.append("container=1")
        parts.append("collapsible=0")

    return ';'.join(parts) + ';'
```

---

## 六、云服务图标支持

### 6.1 AWS 图标

```python
AWS_ICONS = {
    'lambda': {
        'shape': 'mxgraph.aws4.lambda_function',
        'style': 'outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;',
        'size': (78, 78)
    },
    's3': {
        'shape': 'mxgraph.aws4.s3',
        'style': 'outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.s3;',
        'size': (78, 78)
    },
    'ec2': {
        'shape': 'mxgraph.aws4.ec2',
        'style': 'outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2;',
        'size': (78, 78)
    },
    'rds': {
        'shape': 'mxgraph.aws4.rds',
        'style': 'outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.rds;',
        'size': (78, 78)
    },
    'api_gateway': {
        'shape': 'mxgraph.aws4.api_gateway',
        'style': 'outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;',
        'size': (78, 78)
    },
    'dynamodb': {
        'shape': 'mxgraph.aws4.dynamodb',
        'style': 'outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;',
        'size': (78, 78)
    },
    'sqs': {
        'shape': 'mxgraph.aws4.sqs',
        'style': 'outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sqs;',
        'size': (78, 78)
    },
    'sns': {
        'shape': 'mxgraph.aws4.sns',
        'style': 'outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sns;',
        'size': (78, 78)
    },
}
```

### 6.2 Kubernetes 图标

```python
K8S_ICONS = {
    'pod': {
        'shape': 'mxgraph.kubernetes.pod',
        'style': 'shape=mxgraph.kubernetes.pod;prIcon=pod;',
        'size': (50, 50)
    },
    'service': {
        'shape': 'mxgraph.kubernetes.service',
        'style': 'shape=mxgraph.kubernetes.service;prIcon=svc;',
        'size': (50, 50)
    },
    'deployment': {
        'shape': 'mxgraph.kubernetes.deployment',
        'style': 'shape=mxgraph.kubernetes.deployment;prIcon=deploy;',
        'size': (50, 50)
    },
    'ingress': {
        'shape': 'mxgraph.kubernetes.ingress',
        'style': 'shape=mxgraph.kubernetes.ingress;prIcon=ing;',
        'size': (50, 50)
    },
}
```

### 6.3 语义检索

对于用户描述的元素名称，使用关键词匹配或语义搜索：

```python
def search_icon(query: str) -> Optional[dict]:
    """
    根据查询词搜索最匹配的图标

    Args:
        query: 用户描述，如 "AWS Lambda 函数"

    Returns:
        匹配的图标信息，或 None
    """
    query_lower = query.lower()

    # 1. 精确匹配
    if 'lambda' in query_lower and 'aws' in query_lower:
        return AWS_ICONS['lambda']

    # 2. 关键词匹配
    keyword_map = {
        ('s3', 'bucket', '存储桶'): AWS_ICONS['s3'],
        ('ec2', '实例', 'instance'): AWS_ICONS['ec2'],
        ('rds', '数据库', 'database'): AWS_ICONS['rds'],
        ('pod', '容器组'): K8S_ICONS['pod'],
        ('deployment', '部署'): K8S_ICONS['deployment'],
    }

    for keywords, icon in keyword_map.items():
        if any(kw in query_lower for kw in keywords):
            return icon

    # 3. 使用 sentence-transformers 语义搜索（可选）
    # return semantic_search(query)

    return None
```

---

## 七、代码实现

### 7.1 knowledge_retriever.py

```python
"""
Phase 3: 知识检索模块
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class NodeStyle:
    shape: str
    style: str
    width: int
    height: int
    icon: Optional[str] = None


@dataclass
class StyleLibrary:
    node_styles: Dict[str, NodeStyle]
    edge_styles: Dict[str, str]
    theme: Dict[str, Any]

    def to_dict(self) -> dict:
        return {
            'node_styles': {
                k: {
                    'shape': v.shape,
                    'style': v.style,
                    'width': v.width,
                    'height': v.height,
                    'icon': v.icon
                }
                for k, v in self.node_styles.items()
            },
            'edge_styles': self.edge_styles,
            'theme': self.theme
        }


class KnowledgeRetriever:
    """知识检索器"""

    def __init__(self, theme: str = 'professional'):
        self.theme_name = theme
        self.theme = THEMES.get(theme, THEMES['professional'])

    def retrieve(self, graph_spec: dict) -> StyleLibrary:
        """
        根据图规格检索样式

        Args:
            graph_spec: Phase 2 的输出

        Returns:
            StyleLibrary
        """
        node_styles = {}

        # 递归遍历所有节点
        self._collect_styles(graph_spec, node_styles)

        # 生成边样式
        edge_color = self._get_edge_color()
        edge_styles = {
            'arrow': f'edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;strokeColor={edge_color};',
            'dashed': f'edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;dashed=1;strokeColor={edge_color};',
            'bidirectional': f'edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;startArrow=classic;strokeColor={edge_color};',
            'none': f'edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=none;strokeColor={edge_color};',
        }

        return StyleLibrary(
            node_styles=node_styles,
            edge_styles=edge_styles,
            theme={'name': self.theme_name, **self.theme}
        )

    def _collect_styles(self, node: dict, styles: Dict[str, NodeStyle]):
        """递归收集节点样式"""
        node_id = node.get('id')
        node_type = node.get('nodeType', 'default')

        if node_id and node_id != 'root':
            # 获取形状
            shape = TYPE_TO_SHAPE.get(node_type, 'rounded_rect')
            base_style = SHAPE_LIBRARY.get(shape, SHAPE_LIBRARY['rounded_rect'])

            # 获取颜色
            color_role = TYPE_TO_COLOR.get(node_type, 'primary')
            colors = self.theme.get(color_role, self.theme.get('primary'))

            # 检查是否是容器
            is_container = bool(node.get('children'))

            # 组装样式
            full_style = self._build_style(base_style, colors, is_container)

            # 尝试匹配专业图标
            labels = node.get('labels', [])
            label_text = labels[0].get('text', '') if labels else ''
            icon_info = search_icon(label_text)

            if icon_info:
                full_style = icon_info['style']
                width, height = icon_info['size']
            else:
                width = node.get('width', 120)
                height = node.get('height', 60)

            styles[node_id] = NodeStyle(
                shape=shape,
                style=full_style,
                width=width,
                height=height,
                icon=icon_info.get('shape') if icon_info else None
            )

        # 递归处理子节点
        for child in node.get('children', []):
            self._collect_styles(child, styles)

    def _build_style(self, base_style: str, colors: dict, is_container: bool) -> str:
        """组装完整样式字符串"""
        parts = [base_style.rstrip(';')]

        if colors.get('fill'):
            parts.append(f"fillColor={colors['fill']}")
        if colors.get('gradient'):
            parts.append(f"gradientColor={colors['gradient']}")
            parts.append("gradientDirection=south")
        if colors.get('stroke'):
            if colors['stroke'] == 'none':
                parts.append("strokeColor=none")
            else:
                parts.append(f"strokeColor={colors['stroke']}")
        if colors.get('font'):
            parts.append(f"fontColor={colors['font']}")

        if is_container:
            parts.append("container=1")
            parts.append("collapsible=0")

        # tech 主题添加阴影
        if self.theme_name == 'tech':
            parts.append("shadow=1")

        return ';'.join(parts) + ';'

    def _get_edge_color(self) -> str:
        """获取边颜色"""
        if self.theme_name == 'tech':
            return '#00ACC1'
        elif self.theme_name == 'dark':
            return '#888888'
        else:
            return '#666666'
```

---

## 八、高级功能：语义搜索

### 8.1 使用 sentence-transformers

```python
"""
可选：使用 sentence-transformers 进行语义搜索
需要安装：pip install sentence-transformers
"""

from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticSearch:
    def __init__(self, index_path: str = '.asset_index.pkl'):
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.index = self._load_or_build_index(index_path)

    def search(self, query: str, top_k: int = 5) -> List[dict]:
        """语义搜索素材"""
        query_embedding = self.model.encode(query)

        # 计算余弦相似度
        similarities = []
        for item in self.index:
            sim = np.dot(query_embedding, item['embedding']) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(item['embedding'])
            )
            similarities.append((sim, item))

        # 排序返回
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in similarities[:top_k]]
```

---

## 九、与下一阶段的衔接

Phase 3 输出的 `StyleLibrary` 将传递给 Phase 5（XML 生成），用于：

1. **节点渲染**
   - 使用 `node_styles[nodeId].style` 作为 mxCell 的 style 属性
   - 使用 `width` 和 `height` 作为 mxGeometry 尺寸

2. **边渲染**
   - 根据 `edgeType` 选择对应的 `edge_styles`

---

## 十、参考

- [mxGraph Styles](https://jgraph.github.io/mxgraph/docs/js-api/files/util/mxConstants-js.html)
- [DrawIO Shape Libraries](https://www.drawio.com/doc/faq/shape-libraries)
- [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/)
- [Kubernetes Icons](https://github.com/kubernetes/community/tree/master/icons)
