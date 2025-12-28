# Phase 5: XML 生成 (XML Generation)

## 一、阶段目标

将布局结果和样式库转换为标准的 DrawIO XML 文件（.drawio 格式）。

---

## 二、输入

### 2.1 LayoutResult (来自 Phase 4)

```typescript
interface LayoutResult {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  children?: LayoutResult[];
  edges?: LayoutEdge[];
}
```

### 2.2 StyleLibrary (来自 Phase 3)

```typescript
interface StyleLibrary {
  node_styles: { [nodeId: string]: NodeStyle };
  edge_styles: { [edgeType: string]: string };
  theme: ThemeColors;
}
```

### 2.3 GraphSpec (来自 Phase 2)

用于获取节点标签和边标签。

---

## 三、输出

### 3.1 DrawIO XML 结构

```xml
<mxfile host="DrawIO-Agent" modified="2025-01-XX" agent="DrawIO-Generator/1.0">
  <diagram name="Diagram" id="diagram-1">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" page="1" pageWidth="800" pageHeight="600">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- 节点 -->
        <mxCell id="2" value="Node Label" style="..." vertex="1" parent="1">
          <mxGeometry x="100" y="50" width="120" height="60" as="geometry"/>
        </mxCell>

        <!-- 嵌套节点 -->
        <mxCell id="3" value="Container" style="..." vertex="1" parent="1">
          <mxGeometry x="200" y="200" width="300" height="200" as="geometry"/>
        </mxCell>
        <mxCell id="4" value="Child" style="..." vertex="1" parent="3">
          <!-- 子节点坐标相对于父容器 -->
          <mxGeometry x="20" y="40" width="100" height="50" as="geometry"/>
        </mxCell>

        <!-- 连线 -->
        <mxCell id="5" value="" style="..." edge="1" parent="1" source="2" target="3">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="200" y="150"/>
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 3.2 关键规则

| 规则 | 说明 |
|------|------|
| `id="0"` 和 `id="1"` | 保留 ID，用户内容从 `id="2"` 开始 |
| `vertex="1"` | 节点必须包含此属性 |
| `edge="1"` | 连线必须包含此属性 |
| `parent` | 指定父节点 ID，嵌套时使用 |
| `as="geometry"` | mxGeometry 必须包含此属性 |
| `relative="1"` | 连线的 mxGeometry 必须包含此属性 |
| 坐标对齐 | 所有坐标应为 10 的倍数 |

---

## 四、处理逻辑

### 4.1 处理流程

```
LayoutResult + StyleLibrary + GraphSpec
    │
    ▼
┌─────────────────────────────────────┐
│  Step 1: 初始化                      │
│  • 创建 XML 文档头                   │
│  • 创建 root 元素（id=0, id=1）      │
│  • 初始化 ID 计数器 = 2              │
│  • 初始化节点 ID 映射表              │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 2: 递归生成节点                │
│  • render_node(node, parent_id)     │
│  • 分配 mxCell ID                   │
│  • 记录 ID 映射                     │
│  • 应用样式                         │
│  • 生成 mxGeometry                  │
│  • 递归处理 children                │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 3: 生成连线                    │
│  • 查找源/目标节点的 mxCell ID       │
│  • 应用边样式                        │
│  • 转换 bendPoints → mxPoint        │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Step 4: 组装文档                    │
│  • 添加 XML 头                       │
│  • 添加 mxfile 包装                  │
│  • 格式化输出                        │
└─────────────────────────────────────┘
    │
    ▼
DrawIO XML 字符串
```

### 4.2 递归渲染算法

```python
def render_node(node: dict, parent_id: str, id_map: dict, id_counter: list) -> list:
    """
    递归渲染节点

    Args:
        node: 布局结果节点
        parent_id: 父节点的 mxCell ID
        id_map: 原始 ID → mxCell ID 映射
        id_counter: ID 计数器 [current_id]

    Returns:
        mxCell XML 字符串列表
    """
    cells = []

    # 跳过根节点（只处理其子节点）
    if node.get('id') == 'root':
        for child in node.get('children', []):
            cells.extend(render_node(child, '1', id_map, id_counter))
        return cells

    # 分配 mxCell ID
    cell_id = str(id_counter[0])
    id_counter[0] += 1

    # 记录映射
    orig_id = node.get('id')
    id_map[orig_id] = cell_id

    # 获取样式
    style = get_style(orig_id)

    # 获取标签
    label = get_label(orig_id)

    # 判断是否是容器
    is_container = bool(node.get('children'))

    # 生成 mxCell
    cell_xml = generate_cell_xml(
        cell_id=cell_id,
        label=label,
        style=style,
        x=node['x'],
        y=node['y'],
        width=node['width'],
        height=node['height'],
        parent=parent_id,
        is_vertex=True
    )
    cells.append(cell_xml)

    # 递归处理子节点
    for child in node.get('children', []):
        cells.extend(render_node(child, cell_id, id_map, id_counter))

    return cells
```

---

## 五、代码实现

### 5.1 xml_generator.py

```python
"""
Phase 5: XML 生成模块
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
from xml.sax.saxutils import escape
import json


class DrawioGenerator:
    """DrawIO XML 生成器"""

    def __init__(self):
        self.id_counter = 2  # 0 和 1 保留
        self.id_map: Dict[str, str] = {}  # 原始 ID → mxCell ID
        self.cells: List[str] = []

    def generate(
        self,
        layout_result: dict,
        style_library: dict,
        graph_spec: dict
    ) -> str:
        """
        生成完整的 DrawIO XML

        Args:
            layout_result: Phase 4 输出
            style_library: Phase 3 输出
            graph_spec: Phase 2 输出

        Returns:
            DrawIO XML 字符串
        """
        # 重置状态
        self.id_counter = 2
        self.id_map = {}
        self.cells = []

        # 存储样式库
        self.styles = style_library.get('node_styles', {})
        self.edge_styles = style_library.get('edge_styles', {})

        # 存储图规格（用于获取标签）
        self.spec = graph_spec
        self.spec_map = self._build_spec_map(graph_spec)

        # 计算画布尺寸
        canvas = self._calculate_canvas(layout_result)

        # 生成节点
        self._render_node(layout_result, '1')

        # 生成边
        self._render_edges(layout_result)

        # 组装 XML
        return self._assemble_xml(canvas)

    def _build_spec_map(self, spec: dict) -> Dict[str, dict]:
        """构建 ID → 规格映射"""
        result = {}

        def traverse(node):
            if node.get('id'):
                result[node['id']] = node
            for child in node.get('children', []):
                traverse(child)

        traverse(spec)
        return result

    def _calculate_canvas(self, layout: dict) -> dict:
        """计算画布尺寸"""
        max_x = 0
        max_y = 0

        def traverse(node, offset_x=0, offset_y=0):
            nonlocal max_x, max_y
            x = node.get('x', 0) + offset_x
            y = node.get('y', 0) + offset_y
            w = node.get('width', 100)
            h = node.get('height', 60)

            max_x = max(max_x, x + w)
            max_y = max(max_y, y + h)

            for child in node.get('children', []):
                traverse(child, x, y)

        traverse(layout)

        # 添加边距
        return {
            'width': max(800, max_x + 100),
            'height': max(600, max_y + 100)
        }

    def _render_node(self, node: dict, parent_id: str):
        """递归渲染节点"""
        orig_id = node.get('id')

        # 跳过根节点
        if orig_id == 'root':
            for child in node.get('children', []):
                self._render_node(child, '1')
            return

        # 分配 ID
        cell_id = str(self.id_counter)
        self.id_counter += 1
        self.id_map[orig_id] = cell_id

        # 获取样式
        style_info = self.styles.get(orig_id, {})
        style = style_info.get('style', 'rounded=1;whiteSpace=wrap;html=1;')

        # 获取标签
        spec_node = self.spec_map.get(orig_id, {})
        labels = spec_node.get('labels', [])
        label = labels[0].get('text', orig_id) if labels else orig_id

        # 坐标对齐
        x = self._snap_to_grid(node.get('x', 0))
        y = self._snap_to_grid(node.get('y', 0))
        width = self._snap_to_grid(node.get('width', 100))
        height = self._snap_to_grid(node.get('height', 60))

        # 生成 XML
        cell_xml = self._cell_xml(
            cell_id=cell_id,
            value=label,
            style=style,
            x=x,
            y=y,
            width=width,
            height=height,
            parent=parent_id,
            vertex=True
        )
        self.cells.append(cell_xml)

        # 递归子节点
        for child in node.get('children', []):
            self._render_node(child, cell_id)

    def _render_edges(self, node: dict):
        """递归渲染边"""
        for edge in node.get('edges', []):
            self._render_edge(edge, node.get('id', 'root'))

        for child in node.get('children', []):
            self._render_edges(child)

    def _render_edge(self, edge: dict, parent_context: str):
        """渲染单条边"""
        edge_id = edge.get('id')
        sources = edge.get('sources', [])
        targets = edge.get('targets', [])

        if not sources or not targets:
            return

        source_id = self.id_map.get(sources[0])
        target_id = self.id_map.get(targets[0])

        if not source_id or not target_id:
            return

        # 分配 ID
        cell_id = str(self.id_counter)
        self.id_counter += 1

        # 获取边类型
        spec_edge = self._find_edge_spec(edge_id)
        edge_type = spec_edge.get('edgeType', 'arrow') if spec_edge else 'arrow'

        # 获取样式
        style = self.edge_styles.get(edge_type, self.edge_styles.get('arrow', ''))

        # 获取标签
        labels = edge.get('labels', [])
        label = labels[0].get('text', '') if labels else ''

        # 获取路径点
        waypoints = self._extract_waypoints(edge)

        # 确定父节点
        parent_id = '1'
        if parent_context != 'root':
            parent_id = self.id_map.get(parent_context, '1')

        # 生成 XML
        cell_xml = self._edge_xml(
            cell_id=cell_id,
            value=label,
            style=style,
            source=source_id,
            target=target_id,
            parent=parent_id,
            waypoints=waypoints
        )
        self.cells.append(cell_xml)

    def _find_edge_spec(self, edge_id: str) -> Optional[dict]:
        """查找边规格"""
        def search(node):
            for edge in node.get('edges', []):
                if edge.get('id') == edge_id:
                    return edge
            for child in node.get('children', []):
                result = search(child)
                if result:
                    return result
            return None

        return search(self.spec)

    def _extract_waypoints(self, edge: dict) -> List[Tuple[int, int]]:
        """从 ELK 边提取路径点"""
        waypoints = []
        for section in edge.get('sections', []):
            for point in section.get('bendPoints', []):
                x = self._snap_to_grid(point.get('x', 0))
                y = self._snap_to_grid(point.get('y', 0))
                waypoints.append((x, y))
        return waypoints

    def _snap_to_grid(self, value: float) -> int:
        """对齐到网格"""
        return round(value / 10) * 10

    def _cell_xml(
        self,
        cell_id: str,
        value: str,
        style: str,
        x: int,
        y: int,
        width: int,
        height: int,
        parent: str,
        vertex: bool = False,
        edge: bool = False
    ) -> str:
        """生成 mxCell XML"""
        value_escaped = escape(value)
        attrs = [f'id="{cell_id}"', f'value="{value_escaped}"', f'style="{style}"']

        if vertex:
            attrs.append('vertex="1"')
        if edge:
            attrs.append('edge="1"')

        attrs.append(f'parent="{parent}"')

        return f'''        <mxCell {' '.join(attrs)}>
          <mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/>
        </mxCell>'''

    def _edge_xml(
        self,
        cell_id: str,
        value: str,
        style: str,
        source: str,
        target: str,
        parent: str,
        waypoints: List[Tuple[int, int]]
    ) -> str:
        """生成边 mxCell XML"""
        value_escaped = escape(value) if value else ''

        geometry = self._edge_geometry_xml(waypoints)

        return f'''        <mxCell id="{cell_id}" value="{value_escaped}" style="{style}" edge="1" parent="{parent}" source="{source}" target="{target}">
{geometry}
        </mxCell>'''

    def _edge_geometry_xml(self, waypoints: List[Tuple[int, int]]) -> str:
        """生成边的几何 XML"""
        if waypoints:
            points_xml = '\n'.join([
                f'            <mxPoint x="{x}" y="{y}"/>'
                for x, y in waypoints
            ])
            return f'''          <mxGeometry relative="1" as="geometry">
            <Array as="points">
{points_xml}
            </Array>
          </mxGeometry>'''
        else:
            return '          <mxGeometry relative="1" as="geometry"/>'

    def _assemble_xml(self, canvas: dict) -> str:
        """组装完整 XML"""
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        width = canvas['width']
        height = canvas['height']

        cells_xml = '\n'.join(self.cells)

        return f'''<mxfile host="DrawIO-Agent" modified="{timestamp}" agent="DrawIO-Generator/1.0" version="1.0">
  <diagram name="Diagram" id="diagram-1">
    <mxGraphModel dx="{width}" dy="{height}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{cells_xml}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''


def generate_drawio(
    layout_result: dict,
    style_library: dict,
    graph_spec: dict,
    output_path: str
) -> str:
    """
    生成 DrawIO 文件的便捷函数

    Args:
        layout_result: Phase 4 输出
        style_library: Phase 3 输出
        graph_spec: Phase 2 输出
        output_path: 输出文件路径

    Returns:
        生成的 XML 字符串
    """
    generator = DrawioGenerator()
    xml = generator.generate(layout_result, style_library, graph_spec)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml)

    return xml
```

---

## 六、示例

### 6.1 输入

**layout_result**:
```json
{
  "id": "root",
  "width": 300,
  "height": 200,
  "children": [
    {"id": "client", "x": 100, "y": 20, "width": 100, "height": 50},
    {"id": "server", "x": 100, "y": 120, "width": 100, "height": 50}
  ],
  "edges": [
    {
      "id": "e1",
      "sources": ["client"],
      "targets": ["server"],
      "sections": [{"startPoint": {"x": 150, "y": 70}, "endPoint": {"x": 150, "y": 120}}]
    }
  ]
}
```

**style_library**:
```json
{
  "node_styles": {
    "client": {"style": "rounded=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"},
    "server": {"style": "rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;"}
  },
  "edge_styles": {
    "arrow": "edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=classic;strokeColor=#666666;"
  }
}
```

### 6.2 输出

```xml
<mxfile host="DrawIO-Agent" modified="2025-01-XX" agent="DrawIO-Generator/1.0" version="1.0">
  <diagram name="Diagram" id="diagram-1">
    <mxGraphModel dx="400" dy="300" grid="1" gridSize="10">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="Client" style="rounded=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="100" y="20" width="100" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="3" value="Server" style="rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
          <mxGeometry x="100" y="120" width="100" height="50" as="geometry"/>
        </mxCell>
        <mxCell id="4" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=classic;strokeColor=#666666;" edge="1" parent="1" source="2" target="3">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 七、与下一阶段的衔接

Phase 5 输出的 DrawIO XML 将传递给 Phase 6（验证修正），用于：

1. **XML 结构验证**
2. **布局质量检查**
3. **迭代修复**

---

## 八、参考

- [DrawIO XML Format](https://www.drawio.com/doc/faq/diagram-source-edit)
- [mxGraph mxCell API](https://jgraph.github.io/mxgraph/docs/js-api/files/model/mxCell-js.html)
