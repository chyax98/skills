# DrawIO 连线语法规则

基于 mxGraph 官方规范。

## mxCell 连线结构

```xml
<mxCell id="唯一ID" value="标签文本" style="样式字符串" edge="1" parent="1" source="起点ID" target="终点ID">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

**必要属性**：
- `edge="1"` - 标识为连线（非节点）
- `parent="1"` - 父元素 ID
- `source` - 起点节点 ID（可选，无则为浮动起点）
- `target` - 终点节点 ID（可选，无则为浮动终点）
- `relative="1"` - 连线 mxGeometry 必须包含此属性

## 连线样式（edgeStyle）

| 样式 | style 值 | 说明 |
|------|----------|------|
| 直角折线 | `edgeStyle=orthogonalEdgeStyle;` | 只有水平/垂直线段 |
| 圆角直角 | `edgeStyle=orthogonalEdgeStyle;rounded=1;` | 折角处圆滑 |
| 曲线 | `edgeStyle=orthogonalEdgeStyle;curved=1;` | S 形曲线 |
| 直线 | `edgeStyle=none;` 或不设置 | 直接连接 |
| 肘形 | `edgeStyle=elbowEdgeStyle;` | 单折点 |
| 实体关系 | `edgeStyle=entityRelationEdgeStyle;` | ER 图专用 |
| 正交 | `edgeStyle=orthogonalEdgeStyle;orthogonal=1;` | 严格正交 |
| 环路 | `edgeStyle=loopEdgeStyle;` | 自连接（同一节点） |
| 段落 | `edgeStyle=segmentEdgeStyle;` | 多段线 |
| isometric | `edgeStyle=isometricEdgeStyle;` | 等轴测风格 |

## 箭头类型

### 箭头形状

| 类型 | 值 | 说明 |
|------|-----|------|
| 经典箭头 | `classic` | 标准三角箭头 |
| 细经典 | `classicThin` | 细长三角 |
| 实心块 | `block` | 实心三角块 |
| 细块 | `blockThin` | 细长实心块 |
| 开放箭头 | `open` | 开放式 V 形 |
| 细开放 | `openThin` | 细长开放式 |
| 椭圆 | `oval` | 圆形端点 |
| 菱形 | `diamond` | 菱形端点 |
| 细菱形 | `diamondThin` | 细长菱形 |
| 无箭头 | `none` | 无端点标记 |
| 异步 | `async` | 异步消息箭头 |
| 箭头连接器 | `arrow` | 箭头形连接器 |

### 箭头设置

```
endArrow=classic;     // 终点箭头类型
startArrow=none;      // 起点箭头类型
endFill=1;            // 终点箭头填充（1=实心, 0=空心）
startFill=0;          // 起点箭头填充
endSize=8;            // 终点箭头大小
startSize=8;          // 起点箭头大小
```

## 锚点控制

### 出发点（source 侧）

| 属性 | 值范围 | 说明 |
|------|--------|------|
| `exitX` | 0-1 | 出发点 X（0=左, 0.5=中, 1=右） |
| `exitY` | 0-1 | 出发点 Y（0=上, 0.5=中, 1=下） |
| `exitDx` | 像素值 | X 方向偏移 |
| `exitDy` | 像素值 | Y 方向偏移 |
| `exitPerimeter` | 0/1 | 1=从边界出发，0=从指定点出发 |

### 进入点（target 侧）

| 属性 | 值范围 | 说明 |
|------|--------|------|
| `entryX` | 0-1 | 进入点 X |
| `entryY` | 0-1 | 进入点 Y |
| `entryDx` | 像素值 | X 方向偏移 |
| `entryDy` | 像素值 | Y 方向偏移 |
| `entryPerimeter` | 0/1 | 1=从边界进入，0=从指定点进入 |

### 常用锚点组合

```
// 水平流程（右出左入）
exitX=1;exitY=0.5;entryX=0;entryY=0.5;

// 垂直流程（下出上入）
exitX=0.5;exitY=1;entryX=0.5;entryY=0;

// 对角连接（右下出左上入）
exitX=1;exitY=1;entryX=0;entryY=0;

// 四个基本锚点
顶部中心: x=0.5, y=0
底部中心: x=0.5, y=1
左侧中心: x=0, y=0.5
右侧中心: x=1, y=0.5
```

## 线条样式

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `strokeColor` | #rrggbb | 线条颜色 |
| `strokeWidth` | 数值 | 线条粗细，默认 1 |
| `strokeOpacity` | 0-100 | 线条不透明度 |
| `dashed` | 0/1 | 虚线 |
| `dashPattern` | 空格分隔数值 | 虚线模式，如 `8 8` |
| `opacity` | 0-100 | 整体不透明度 |
| `shadow` | 0/1 | 阴影 |

## 路由控制

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `jettySize` | auto/数值 | 连线起始段长度 |
| `sourceJettySize` | auto/数值 | 起点侧起始段长度 |
| `targetJettySize` | auto/数值 | 终点侧起始段长度 |
| `orthogonalLoop` | 0/1 | 自连接时使用正交路由 |
| `orthogonal` | 0/1 | 强制正交（仅水平/垂直） |

## 手动拐点

当自动路由不满足需求时，手动指定拐点：

```xml
<mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="A" target="B">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="100"/>
      <mxPoint x="300" y="200"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### 浮动连线（无连接节点）

```xml
<mxCell id="edge2" style="edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="100" y="100" as="sourcePoint"/>
    <mxPoint x="300" y="200" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

## 标签样式

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `labelBackgroundColor` | #rrggbb/none | 标签背景色 |
| `labelBorderColor` | #rrggbb/none | 标签边框色 |
| `labelPadding` | 数值 | 标签内边距 |
| `fontColor` | #rrggbb | 标签字体颜色 |
| `fontSize` | 数值 | 标签字号 |
| `align` | left/center/right | 标签水平对齐 |
| `verticalAlign` | top/middle/bottom | 标签垂直对齐 |

### 标签位置

连线标签位置由 mxGeometry 的相对坐标控制：

```xml
<mxGeometry x="0.5" y="0" relative="1" as="geometry">
  <mxPoint as="offset"/>
</mxGeometry>
```

- `x` (0-1): 沿连线位置，0=起点，1=终点，0.5=中点
- `y`: 垂直偏移量（像素）
- `offset`: 额外微调

## 交互属性

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `editable` | 0/1 | 可编辑标签 |
| `bendable` | 0/1 | 可添加/移动拐点 |
| `movable` | 0/1 | 可移动（整体） |
| `deletable` | 0/1 | 可删除 |
| `noEdgeStyle` | 0/1 | 1=忽略 edgeStyle，使用手动路由 |

## 完整示例

```xml
<!-- 带箭头的标准连线 -->
<mxCell id="edge1" value="数据流"
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;
               strokeColor=#6c8ebf;strokeWidth=2;endArrow=classic;endFill=1;"
        edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 虚线无箭头连线 -->
<mxCell id="edge2" value=""
        style="edgeStyle=orthogonalEdgeStyle;dashed=1;dashPattern=8 8;
               strokeColor=#999999;endArrow=none;"
        edge="1" parent="1" source="node3" target="node4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 双向箭头连线 -->
<mxCell id="edge3" value="双向"
        style="edgeStyle=orthogonalEdgeStyle;strokeWidth=2;
               startArrow=classic;startFill=1;endArrow=classic;endFill=1;"
        edge="1" parent="1" source="node5" target="node6">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```
