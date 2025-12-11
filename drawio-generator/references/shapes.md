# DrawIO 形状语法规则

## 基础形状

| 形状 | style 参数 |
|------|-----------|
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

## 特殊形状

| 形状 | style 参数 | 用途 |
|------|-----------|------|
| 文档 | `shape=document;whiteSpace=wrap;html=1;boundedLbl=1;` | 文档节点 |
| 注释 | `shape=note;whiteSpace=wrap;html=1;` | 注释/备注 |
| 卡片 | `shape=card;whiteSpace=wrap;html=1;` | 卡片样式 |
| 人物 | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;` | UML Actor |
| 数据库 | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;` | 数据存储 |
| 队列 | `shape=delay;whiteSpace=wrap;html=1;` | 消息队列 |

## 形状属性

| 属性 | 值 | 说明 |
|------|---|------|
| `rounded` | 0/1 | 圆角开关 |
| `arcSize` | 数值 | 圆角大小（rounded=1 时有效） |
| `aspect` | fixed | 保持宽高比 |
| `direction` | north/south/east/west | 形状方向 |
| `rotation` | 角度 | 旋转（需配合 `horizontal=1` 保持文字水平） |
| `flipH` | 0/1 | 水平翻转 |
| `flipV` | 0/1 | 垂直翻转 |

## 填充与边框

| 属性 | 值 | 说明 |
|------|---|------|
| `fillColor` | #rrggbb | 填充色 |
| `strokeColor` | #rrggbb | 边框色 |
| `strokeWidth` | 数值 | 边框粗细（默认 1） |
| `dashed` | 0/1 | 虚线边框 |
| `dashPattern` | 数值序列 | 虚线样式，如 `8 8` |
| `opacity` | 0-100 | 不透明度 |
| `gradientColor` | #rrggbb | 渐变色 |
| `gradientDirection` | north/south/east/west | 渐变方向 |
| `shadow` | 0/1 | 阴影 |

## 文字样式

| 属性 | 值 | 说明 |
|------|---|------|
| `fontSize` | 数值 | 字号 |
| `fontColor` | #rrggbb | 字色 |
| `fontStyle` | 0/1/2/3 | 0=正常, 1=粗体, 2=斜体, 3=粗斜体 |
| `fontFamily` | 字体名 | 字体 |
| `align` | left/center/right | 水平对齐 |
| `verticalAlign` | top/middle/bottom | 垂直对齐 |
| `labelPosition` | left/center/right | 标签水平位置 |
| `verticalLabelPosition` | top/middle/bottom | 标签垂直位置 |
