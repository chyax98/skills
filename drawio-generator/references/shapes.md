# DrawIO 形状语法规则

基于 mxGraph 官方规范。

## mxCell 节点结构

```xml
<mxCell id="唯一ID" value="显示文本" style="样式字符串" vertex="1" parent="父ID">
  <mxGeometry x="X坐标" y="Y坐标" width="宽度" height="高度" as="geometry"/>
</mxCell>
```

**必要属性**：
- `id` - 唯一标识符（"0" 和 "1" 为保留 ID）
- `vertex="1"` - 标识为节点（非连线）
- `parent` - 父元素 ID（顶层节点使用 "1"）
- `as="geometry"` - mxGeometry 必须包含此属性

## 基础形状

| 形状 | style 值 |
|------|----------|
| 矩形 | `whiteSpace=wrap;html=1;` |
| 圆角矩形 | `rounded=1;whiteSpace=wrap;html=1;` |
| 椭圆 | `ellipse;whiteSpace=wrap;html=1;` |
| 圆形 | `ellipse;whiteSpace=wrap;html=1;aspect=fixed;` |
| 菱形 | `rhombus;whiteSpace=wrap;html=1;` |
| 三角形 | `triangle;whiteSpace=wrap;html=1;` |
| 六边形 | `shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;` |
| 平行四边形 | `shape=parallelogram;whiteSpace=wrap;html=1;` |
| 梯形 | `shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;` |
| 圆柱 | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;` |
| 云形 | `ellipse;shape=cloud;whiteSpace=wrap;html=1;` |
| 双椭圆 | `doubleEllipse;whiteSpace=wrap;html=1;` |
| 线条 | `line;strokeWidth=2;html=1;` |

## 特殊形状

| 形状 | style 值 | 典型用途 |
|------|----------|----------|
| 文档 | `shape=document;whiteSpace=wrap;html=1;boundedLbl=1;` | 文档节点 |
| 注释 | `shape=note;whiteSpace=wrap;html=1;` | 注释/备注 |
| 卡片 | `shape=card;whiteSpace=wrap;html=1;` | 卡片样式 |
| 人物 | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;` | UML Actor |
| 数据库 | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;` | 数据存储 |
| 队列 | `shape=delay;whiteSpace=wrap;html=1;` | 消息队列 |
| 立方体 | `shape=cube;whiteSpace=wrap;html=1;boundedLbl=1;` | 3D 效果 |
| 折线箭头 | `shape=flexArrow;endArrow=classic;html=1;` | 流程指示 |
| 标注框 | `shape=callout;whiteSpace=wrap;html=1;perimeter=calloutPerimeter;` | Callout |
| 进程 | `shape=process;whiteSpace=wrap;html=1;` | 流程图进程 |
| 数据 | `shape=parallelogram;whiteSpace=wrap;html=1;` | 流程图数据 |

## 形状几何属性

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `rounded` | 0/1 | 圆角开关 |
| `arcSize` | 数值 | 圆角大小（rounded=1 时生效），默认由 RECTANGLE_ROUNDING_FACTOR 控制 |
| `absoluteArcSize` | 0/1 | 1=arcSize 为绝对像素值，0=百分比 |
| `aspect` | fixed/variable | fixed=保持宽高比 |
| `direction` | north/south/east/west | 形状朝向（三角形等方向性形状） |
| `rotation` | 0-360 | 旋转角度 |
| `flipH` | 0/1 | 水平翻转 |
| `flipV` | 0/1 | 垂直翻转 |

## 填充样式

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `fillColor` | #rrggbb / none | 填充色，支持 `inherit`/`swimlane` 继承 |
| `fillOpacity` | 0-100 | 填充不透明度 |
| `gradientColor` | #rrggbb | 渐变终止色 |
| `gradientDirection` | north/south/east/west | 渐变方向，默认 south |
| `opacity` | 0-100 | 整体不透明度（影响填充和边框） |
| `glass` | 0/1 | 玻璃效果 |

## 边框样式

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `strokeColor` | #rrggbb / none | 边框色，支持 `inherit`/`swimlane` 继承 |
| `strokeWidth` | 数值 | 边框粗细，默认 1 |
| `strokeOpacity` | 0-100 | 边框不透明度 |
| `dashed` | 0/1 | 虚线边框 |
| `dashPattern` | 空格分隔数值 | 虚线模式，如 `8 8` 或 `5 3 2 6` |
| `fixDash` | 0/1 | 1=虚线模式不随缩放变化 |
| `shadow` | 0/1 | 阴影效果 |

## 文字样式

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `fontColor` | #rrggbb | 字体颜色 |
| `fontSize` | 数值 | 字号（像素） |
| `fontFamily` | 字体名 | 字体系列 |
| `fontStyle` | 0/1/2/4 | 位运算：1=粗体, 2=斜体, 4=下划线（可组合，如 3=粗斜体, 5=粗体+下划线） |
| `align` | left/center/right | 水平对齐 |
| `verticalAlign` | top/middle/bottom | 垂直对齐 |
| `labelPosition` | left/center/right | 标签水平位置（相对于形状） |
| `verticalLabelPosition` | top/middle/bottom | 标签垂直位置（相对于形状） |
| `whiteSpace` | wrap | 启用文字换行（必须配合 html=1） |
| `html` | 0/1 | 1=启用 HTML 标签支持 |
| `overflow` | visible/hidden/fill/width | 文字溢出处理 |
| `spacing` | 数值 | 文字内边距（全方向） |
| `spacingTop/Left/Bottom/Right` | 数值 | 单方向内边距 |
| `horizontal` | 0/1 | 0=垂直文字，1=水平文字（配合 rotation 使用） |
| `textOpacity` | 0-100 | 文字不透明度 |

## 交互属性

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `resizable` | 0/1 | 可调整大小 |
| `rotatable` | 0/1 | 可旋转 |
| `movable` | 0/1 | 可移动 |
| `editable` | 0/1 | 可编辑文字 |
| `deletable` | 0/1 | 可删除 |
| `bendable` | 0/1 | 连接点可拖拽 |
| `cloneable` | 0/1 | 可复制 |
| `foldable` | 0/1 | 可折叠（容器） |
| `pointerEvents` | 0/1 | 是否响应鼠标事件（透明背景时） |

## 图片形状

```xml
<mxCell style="shape=image;image=URL或DataURI;imageAspect=0;aspect=fixed;" .../>
```

| 属性 | 值类型 | 说明 |
|------|--------|------|
| `image` | URL/DataURI | 图片路径 |
| `imageWidth` | 数值 | 图片宽度 |
| `imageHeight` | 数值 | 图片高度 |
| `imageAspect` | 0/1 | 1=保持图片宽高比 |
| `imageAlign` | left/center/right | 图片水平对齐 |
| `imageVerticalAlign` | top/middle/bottom | 图片垂直对齐 |
| `imageBackground` | #rrggbb | 图片背景色 |
| `imageBorder` | #rrggbb | 图片边框色 |

## 常用颜色

标准调色板：
```
蓝色系: #dae8fc (浅) #6c8ebf (边框) #1ba1e2 (强调)
绿色系: #d5e8d4 (浅) #82b366 (边框) #00a300 (强调)
黄色系: #fff2cc (浅) #d6b656 (边框) #f0a30a (强调)
橙色系: #ffe6cc (浅) #d79b00 (边框) #fa6800 (强调)
红色系: #f8cecc (浅) #b85450 (边框) #e51400 (强调)
紫色系: #e1d5e7 (浅) #9673a6 (边框) #aa00ff (强调)
灰色系: #f5f5f5 (浅) #666666 (边框) #333333 (深)
```

## 完整示例

```xml
<mxCell id="node1" value="处理数据"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=14;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```
