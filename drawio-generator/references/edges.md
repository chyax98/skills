# DrawIO 连线语法规则

## 连线类型

| 类型 | style 参数 |
|------|-----------|
| 直角折线 | `edgeStyle=orthogonalEdgeStyle;rounded=0;` |
| 圆角折线 | `edgeStyle=orthogonalEdgeStyle;rounded=1;` |
| 曲线 | `edgeStyle=orthogonalEdgeStyle;curved=1;` |
| 直线 | `edgeStyle=none;` |
| 肘形 | `edgeStyle=elbowEdgeStyle;` |
| 实体关系 | `edgeStyle=entityRelationEdgeStyle;` |

## 箭头类型

| 类型 | endArrow/startArrow 值 |
|------|----------------------|
| 经典箭头 | `classic` |
| 实心块 | `block` |
| 开放箭头 | `open` |
| 菱形（空心） | `diamond` |
| 菱形（实心） | `diamondThin` |
| 椭圆 | `oval` |
| 无箭头 | `none` |
| 异步 | `async` |

设置方式：
```
endArrow=classic;endFill=1;    // 终点实心箭头
startArrow=diamond;startFill=0; // 起点空心菱形
```

## 锚点控制

| 属性 | 值范围 | 说明 |
|------|-------|------|
| `exitX` | 0-1 | 出发点 X（0=左, 0.5=中, 1=右） |
| `exitY` | 0-1 | 出发点 Y（0=上, 0.5=中, 1=下） |
| `entryX` | 0-1 | 进入点 X |
| `entryY` | 0-1 | 进入点 Y |

常用组合：
```
exitX=1;exitY=0.5;entryX=0;entryY=0.5;  // 右出左入（水平流程）
exitX=0.5;exitY=1;entryX=0.5;entryY=0;  // 下出上入（垂直流程）
```

## 线条样式

| 属性 | 值 | 说明 |
|------|---|------|
| `strokeColor` | #rrggbb | 线条颜色 |
| `strokeWidth` | 数值 | 线条粗细 |
| `dashed` | 0/1 | 虚线 |
| `dashPattern` | 数值序列 | 虚线样式 |
| `opacity` | 0-100 | 不透明度 |

## 拐点控制

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

## 标签

| 属性 | 值 | 说明 |
|------|---|------|
| `labelBackgroundColor` | #rrggbb/none | 标签背景 |
| `labelBorderColor` | #rrggbb/none | 标签边框 |
