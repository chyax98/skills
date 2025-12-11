# DrawIO 高级图表规则

## 容器/分组

```xml
<mxCell id="container1" value="容器标题"
        style="swimlane;whiteSpace=wrap;html=1;startSize=30;collapsible=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry"/>
</mxCell>

<!-- 子元素：parent 指向容器，坐标相对于容器 -->
<mxCell id="child1" value="子节点" style="..." vertex="1" parent="container1">
  <mxGeometry x="20" y="50" width="100" height="40" as="geometry"/>
</mxCell>
```

| 属性 | 值 | 说明 |
|------|---|------|
| `swimlane` | - | 容器形状 |
| `startSize` | 数值 | 标题栏高度 |
| `collapsible` | 0/1 | 可折叠 |
| `collapsed` | 0/1 | 默认折叠状态 |

## 泳道

```xml
<mxCell id="lane1" value="泳道1"
        style="swimlane;horizontal=1;whiteSpace=wrap;html=1;startSize=30;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="500" height="120" as="geometry"/>
</mxCell>
```

| 属性 | 值 | 说明 |
|------|---|------|
| `horizontal` | 0/1 | 0=垂直泳道, 1=水平泳道 |
| `swimlaneFillColor` | #rrggbb | 泳道填充色 |
| `swimlaneLine` | 0/1 | 泳道分隔线 |

## 图层

```xml
<!-- 新建图层 -->
<mxCell id="layer2" value="背景层" style="locked=1;" parent="0"/>

<!-- 元素放到指定图层 -->
<mxCell id="bg" value="背景" style="..." vertex="1" parent="layer2">
  <mxGeometry ... as="geometry"/>
</mxCell>
```

| 属性 | 值 | 说明 |
|------|---|------|
| `locked` | 0/1 | 锁定图层 |
| `visible` | 0/1 | 图层可见性 |

## mxGraphModel 属性

```xml
<mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1"
              tooltips="1" connect="1" arrows="1" fold="1"
              page="1" pageScale="1" pageWidth="800" pageHeight="600"
              background="none" math="0" shadow="0">
```

| 属性 | 说明 |
|------|------|
| `dx`, `dy` | 画布偏移 |
| `grid` | 显示网格 |
| `gridSize` | 网格大小 |
| `guides` | 对齐辅助线 |
| `page` | 显示页面边界 |
| `pageWidth`, `pageHeight` | 页面尺寸 |
| `background` | 背景色/none |
| `shadow` | 全局阴影 |

## mxGeometry 属性

```xml
<mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
<mxGeometry relative="1" as="geometry"/>  <!-- 连线使用 -->
```

| 属性 | 说明 |
|------|------|
| `x`, `y` | 位置（绝对或相对于父容器） |
| `width`, `height` | 尺寸 |
| `relative` | 1=相对坐标（连线使用） |
| `as="geometry"` | **必须存在** |

## 连接点

自定义形状连接点：

```xml
<mxCell id="node1" value="节点" style="points=[[0,0.5],[1,0.5],[0.5,0],[0.5,1]];..." .../>
```

`points` 格式：`[[x1,y1],[x2,y2],...]`，值范围 0-1
