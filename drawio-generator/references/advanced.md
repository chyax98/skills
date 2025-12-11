# DrawIO 高级图表规则

基于 mxGraph 官方规范。

## 文件结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Claude Code" version="1.0">
  <diagram name="图表名称" id="唯一ID">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1"
                  tooltips="1" connect="1" arrows="1" fold="1"
                  page="1" pageScale="1" pageWidth="800" pageHeight="600">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 节点和连线放在这里 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## mxGraphModel 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `dx`, `dy` | 数值 | 画布偏移量 |
| `grid` | 0/1 | 显示网格 |
| `gridSize` | 数值 | 网格大小（像素） |
| `guides` | 0/1 | 对齐辅助线 |
| `tooltips` | 0/1 | 显示工具提示 |
| `connect` | 0/1 | 允许连接 |
| `arrows` | 0/1 | 显示箭头 |
| `fold` | 0/1 | 允许折叠 |
| `page` | 0/1 | 显示页面边界 |
| `pageScale` | 数值 | 页面缩放比例 |
| `pageWidth`, `pageHeight` | 数值 | 页面尺寸 |
| `background` | #rrggbb/none | 背景色 |
| `math` | 0/1 | 启用 LaTeX 数学公式 |
| `shadow` | 0/1 | 全局阴影 |

## 容器（Container）

容器可包含子元素，子元素坐标相对于容器。

```xml
<!-- 容器 -->
<mxCell id="container1" value="容器标题"
        style="swimlane;whiteSpace=wrap;html=1;startSize=30;collapsible=1;fillColor=#f5f5f5;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry"/>
</mxCell>

<!-- 子元素：parent 指向容器，坐标相对于容器 -->
<mxCell id="child1" value="子节点"
        style="rounded=1;whiteSpace=wrap;html=1;"
        vertex="1" parent="container1">
  <mxGeometry x="20" y="50" width="100" height="40" as="geometry"/>
</mxCell>
```

### 容器样式属性

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `swimlane` | - | 容器形状标识 |
| `startSize` | 数值 | 标题栏高度 |
| `collapsible` | 0/1 | 可折叠 |
| `collapsed` | 0/1 | 默认折叠状态 |
| `container` | 0/1 | 强制作为容器 |
| `childLayout` | - | 子元素布局方式 |
| `swimlaneFillColor` | #rrggbb | 内容区填充色 |
| `swimlaneLine` | 0/1 | 显示泳道分隔线 |
| `horizontal` | 0/1 | 标题栏方向（1=水平，0=垂直） |

## 泳道（Swimlane）

多个泳道组合形成泳道图：

```xml
<!-- 水平泳道（标签在左侧） -->
<mxCell id="lane1" value="开发团队"
        style="swimlane;horizontal=1;whiteSpace=wrap;html=1;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="600" height="150" as="geometry"/>
</mxCell>

<!-- 垂直泳道（标签在顶部） -->
<mxCell id="lane2" value="测试团队"
        style="swimlane;horizontal=0;whiteSpace=wrap;html=1;startSize=30;fillColor=#d5e8d4;strokeColor=#82b366;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="200" width="600" height="150" as="geometry"/>
</mxCell>
```

### 嵌套泳道

```xml
<!-- 父泳道 -->
<mxCell id="parentLane" value="部门A"
        style="swimlane;horizontal=1;startSize=40;" vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="700" height="300" as="geometry"/>
</mxCell>

<!-- 子泳道 -->
<mxCell id="childLane1" value="小组1"
        style="swimlane;horizontal=1;startSize=25;" vertex="1" parent="parentLane">
  <mxGeometry x="10" y="50" width="680" height="100" as="geometry"/>
</mxCell>
```

## 分组（Group）

分组与容器的区别：分组不显示边框，仅用于组织。

```xml
<mxCell id="group1" value=""
        style="group;"
        vertex="1" connectable="0" parent="1">
  <mxGeometry x="100" y="100" width="200" height="150" as="geometry"/>
</mxCell>

<mxCell id="grouped1" value="节点1" style="..." vertex="1" parent="group1">
  <mxGeometry x="10" y="10" width="80" height="40" as="geometry"/>
</mxCell>
```

| 属性 | 值 | 说明 |
|------|-----|------|
| `group` | - | 分组标识 |
| `connectable` | 0/1 | 分组本身是否可连接 |

## 图层（Layer）

图层用于组织不同层次的内容：

```xml
<!-- 默认图层（id="1"） -->
<mxCell id="1" parent="0"/>

<!-- 自定义图层 -->
<mxCell id="layer_background" value="背景层" parent="0"/>
<mxCell id="layer_main" value="主内容层" parent="0"/>
<mxCell id="layer_annotation" value="标注层" parent="0"/>

<!-- 元素放到指定图层 -->
<mxCell id="bg_rect" value=""
        style="fillColor=#f0f0f0;strokeColor=none;"
        vertex="1" parent="layer_background">
  <mxGeometry x="0" y="0" width="800" height="600" as="geometry"/>
</mxCell>
```

### 图层属性

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `locked` | 0/1 | 锁定图层（不可编辑） |
| `visible` | 0/1 | 图层可见性 |

## 自定义连接点

为形状定义固定连接点：

```xml
<mxCell id="node1" value="节点"
        style="points=[[0,0.5],[1,0.5],[0.5,0],[0.5,1]];shape=rectangle;..."
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="60" as="geometry"/>
</mxCell>
```

`points` 格式：`[[x1,y1],[x2,y2],...]`
- 值范围 0-1，相对于形状边界
- `[0,0.5]` = 左侧中心
- `[1,0.5]` = 右侧中心
- `[0.5,0]` = 顶部中心
- `[0.5,1]` = 底部中心

## 多页图表

```xml
<mxfile host="Claude Code">
  <diagram name="页面1" id="page1">
    <mxGraphModel ...>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 页面1内容 -->
      </root>
    </mxGraphModel>
  </diagram>
  <diagram name="页面2" id="page2">
    <mxGraphModel ...>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 页面2内容 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## HTML 标签支持

当 `html=1` 时，value 中可使用 HTML：

```xml
<mxCell id="node1"
        value="&lt;b&gt;粗体&lt;/b&gt;&lt;br&gt;&lt;i&gt;斜体&lt;/i&gt;"
        style="whiteSpace=wrap;html=1;" .../>
```

### 转义规则

| 字符 | 转义 |
|------|------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |
| 换行 | `&#xa;` 或 `<br>` |

### 常用 HTML 格式

```
粗体: &lt;b&gt;文本&lt;/b&gt;
斜体: &lt;i&gt;文本&lt;/i&gt;
下划线: &lt;u&gt;文本&lt;/u&gt;
字体: &lt;font color="#ff0000" size="14"&gt;文本&lt;/font&gt;
换行: &lt;br&gt;
```

## 表格形状

```xml
<mxCell id="table1" value=""
        style="shape=table;startSize=0;container=1;collapsible=0;childLayout=tableLayout;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="120" as="geometry"/>
</mxCell>

<!-- 表格行 -->
<mxCell id="row1" value="" style="shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;strokeColor=inherit;top=0;left=0;bottom=0;right=0;collapsible=0;dropTarget=0;fillColor=none;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;" vertex="1" parent="table1">
  <mxGeometry y="0" width="300" height="40" as="geometry"/>
</mxCell>

<!-- 表格单元格 -->
<mxCell id="cell1" value="单元格1" style="shape=partialRectangle;html=1;whiteSpace=wrap;connectable=0;strokeColor=inherit;overflow=hidden;fillColor=none;top=0;left=0;bottom=0;right=0;pointerEvents=1;" vertex="1" parent="row1">
  <mxGeometry width="100" height="40" as="geometry"/>
</mxCell>
```

## 链接与动作

```xml
<!-- 外部链接 -->
<mxCell id="link1" value="点击打开"
        style="whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="40" as="geometry"/>
  <Object label="点击打开" link="https://example.com" as="UserObject"/>
</mxCell>

<!-- 内部跳转（页面间） -->
<mxCell ... style="..;link=data:page/id,page2;"/>
```

## ID 命名规范

- `id="0"` - 保留：根节点
- `id="1"` - 保留：默认图层
- 自定义 ID 建议使用有意义的前缀：
  - `node_xxx` - 节点
  - `edge_xxx` - 连线
  - `container_xxx` - 容器
  - `layer_xxx` - 图层
  - `group_xxx` - 分组

## 完整容器示例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Claude Code">
  <diagram name="架构图" id="arch1">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" page="1" pageWidth="800" pageHeight="600">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- 容器：前端层 -->
        <mxCell id="container_frontend" value="前端层"
                style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;"
                vertex="1" parent="1">
          <mxGeometry x="50" y="50" width="700" height="120" as="geometry"/>
        </mxCell>

        <!-- 容器内节点 -->
        <mxCell id="node_web" value="Web App"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;"
                vertex="1" parent="container_frontend">
          <mxGeometry x="50" y="40" width="100" height="50" as="geometry"/>
        </mxCell>

        <mxCell id="node_mobile" value="Mobile App"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;"
                vertex="1" parent="container_frontend">
          <mxGeometry x="200" y="40" width="100" height="50" as="geometry"/>
        </mxCell>

        <!-- 容器：后端层 -->
        <mxCell id="container_backend" value="后端层"
                style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#d5e8d4;strokeColor=#82b366;"
                vertex="1" parent="1">
          <mxGeometry x="50" y="200" width="700" height="120" as="geometry"/>
        </mxCell>

        <mxCell id="node_api" value="API Server"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;"
                vertex="1" parent="container_backend">
          <mxGeometry x="125" y="40" width="100" height="50" as="geometry"/>
        </mxCell>

        <!-- 跨容器连线 -->
        <mxCell id="edge_web_api"
                style="edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=classic;"
                edge="1" parent="1" source="node_web" target="node_api">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```
