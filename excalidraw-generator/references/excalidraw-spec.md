# Excalidraw JSON 格式规范 (v2.0)

## 文件顶层结构

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {},
  "files": {}
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 是 | 固定值 "excalidraw" |
| version | number | 是 | Schema 版本号 (当前为 2) |
| source | string | 是 | 来源 URL |
| elements | array | 是 | 画布元素数组 |
| appState | object | 否 | 应用状态配置 |
| files | object | 否 | 图片文件数据 (base64) |

## 元素类型总览

| 元素类型 | type 值 | 说明 | 特有属性 |
|---------|--------|------|----------|
| 矩形 | `rectangle` | 基础形状 | roundness |
| 椭圆 | `ellipse` | 基础形状 | - |
| 菱形 | `diamond` | 基础形状 | roundness |
| 箭头 | `arrow` | 线性元素，可绑定 | points, startBinding, endBinding, elbowed |
| 直线 | `line` | 线性元素 | points |
| 文本 | `text` | 可独立或作为容器标签 | fontSize, fontFamily, containerId |
| 图片 | `image` | 需要 files 字段配合 | fileId |
| 自由绘制 | `freedraw` | 手写笔迹 | points, pressures, simulatePressure |
| 框架 | `frame` | 容器，用于分组 | name |
| AI框架 | `magicframe` | AI 生成区域 | name |

## 基础元素属性 (22个必需字段)

```typescript
type ExcalidrawElementBase = {
  id: string;                    // 唯一标识符
  type: string;                  // 元素类型
  x: number;                     // 左上角 X 坐标
  y: number;                     // 左上角 Y 坐标
  width: number;                 // 宽度 (默认 100)
  height: number;                // 高度 (默认 100)
  angle: number;                 // 旋转角度 (弧度)
  strokeColor: string;           // 边框颜色 (默认 "#1e1e1e")
  backgroundColor: string;       // 背景颜色 (默认 "transparent")
  fillStyle: FillStyle;          // 填充样式
  strokeWidth: number;           // 边框宽度 (默认 1)
  strokeStyle: StrokeStyle;      // 边框样式
  roughness: number;             // 手绘粗糙度 (0-2)
  opacity: number;               // 透明度 (0-100)
  groupIds: string[];            // 所属分组 ID 列表
  frameId: string | null;        // 所属框架 ID
  boundElements: BoundElement[]; // 绑定的元素
  locked: boolean;               // 是否锁定
  link: string | null;           // 超链接
  seed: number;                  // 随机种子 (roughjs)
  version: number;               // 版本号 (协作用)
  versionNonce: number;          // 版本随机数
  isDeleted: boolean;            // 是否已删除
  updated: number;               // 更新时间戳
};
```

## 样式属性可选值

### fillStyle (填充样式)

| 值 | 效果 | 使用场景 |
|----|------|----------|
| `"solid"` | 实心填充 | 正式图表 |
| `"hachure"` | 斜线填充 | 手绘风格 |
| `"cross-hatch"` | 交叉斜线 | 强调区域 |
| `"zigzag"` | 锯齿填充 | 特殊效果 |

### strokeStyle (边框样式)

| 值 | 效果 | 使用场景 |
|----|------|----------|
| `"solid"` | 实线 | 默认边框 |
| `"dashed"` | 虚线 | 虚拟/可选关系 |
| `"dotted"` | 点线 | 弱关联 |

### fontFamily (字体)

| 值 | 字体 | 风格 |
|----|------|------|
| 1 | Virgil | 手写体 (默认) |
| 2 | Helvetica | 无衬线 |
| 3 | Cascadia | 等宽代码字体 |
| 4 | Assistant | 专业字体 |

### roughness (手绘粗糙度)

| 值 | 效果 |
|----|------|
| 0 | 光滑精确 (专业风格) |
| 1 | 轻微手绘 (默认) |
| 2 | 明显手绘 (草图风格) |

## 文本元素属性

```json
{
  "type": "text",
  "id": "text-1",
  "x": 100,
  "y": 100,
  "text": "Hello World",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "#1e1e1e",
  "containerId": null,
  "autoResize": true,
  "lineHeight": 1.25
}
```

| 属性 | 类型 | 可选值 | 说明 |
|------|------|--------|------|
| text | string | - | 文本内容（支持 \n 换行） |
| fontSize | number | - | 字体大小 |
| fontFamily | number | 1-4 | 字体族 |
| textAlign | string | left/center/right | 水平对齐 |
| verticalAlign | string | top/middle/bottom | 垂直对齐 |
| containerId | string/null | - | 容器 ID (文本在容器内时) |
| autoResize | boolean | - | true=自动宽度 |
| lineHeight | number | - | 行高 (默认 1.25) |

## 箭头/线条元素属性

### 基础箭头

```json
{
  "type": "arrow",
  "id": "arrow-1",
  "x": 100,
  "y": 200,
  "width": 200,
  "height": 50,
  "points": [[0, 0], [200, 50]],
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "startBinding": {
    "elementId": "rect-1",
    "focus": 0,
    "gap": 1
  },
  "endBinding": {
    "elementId": "rect-2",
    "focus": 0,
    "gap": 1
  }
}
```

### 正交箭头 (Elbowed)

```json
{
  "type": "arrow",
  "elbowed": true,
  "points": [
    [0, 0],
    [100, 0],
    [100, 50],
    [200, 50]
  ]
}
```

### 多点弯曲箭头

```json
{
  "type": "arrow",
  "points": [
    [0, 0],
    [50, 25],
    [100, 0],
    [150, 50]
  ]
}
```

## Arrowhead 类型表

| 值 | 效果 | 使用场景 |
|----|------|----------|
| `null` | 无箭头 | 普通连接线 |
| `"arrow"` | 普通箭头 | 默认箭头 |
| `"bar"` | 横杠 | 终止符号 |
| `"dot"` | 实心点 | 聚合关系 |
| `"circle"` | 实心圆 | 组合关系 |
| `"circle_outline"` | 空心圆 | 关联关系 |
| `"triangle"` | 实心三角 | 继承关系 |
| `"triangle_outline"` | 空心三角 | 实现关系 |
| `"diamond"` | 实心菱形 | UML组合 |
| `"diamond_outline"` | 空心菱形 | UML聚合 |

## Binding (绑定) 详解

绑定用于将箭头连接到形状元素，使箭头随形状移动。

```json
{
  "startBinding": {
    "elementId": "target-element-id",
    "focus": 0,
    "gap": 1,
    "fixedPoint": null
  }
}
```

| 属性 | 类型 | 范围 | 说明 |
|------|------|------|------|
| elementId | string | - | 被绑定元素的 ID |
| focus | number | -1 到 1 | 绑定点在边界上的位置 |
| gap | number | ≥0 | 箭头端点与元素的间距 |
| fixedPoint | [number, number] / null | [0-1, 0-1] | 固定绑定点（相对坐标）|

### focus 值含义

- `-1`: 左边/上边
- `0`: 中间 (默认)
- `1`: 右边/下边

### fixedPoint 使用

当需要精确控制箭头连接点位置时使用：

```json
{
  "fixedPoint": [0.5, 1]  // 元素底部中心
}
```

- `[0, 0]`: 左上角
- `[1, 0]`: 右上角
- `[0, 1]`: 左下角
- `[1, 1]`: 右下角
- `[0.5, 0]`: 顶部中心
- `[0.5, 1]`: 底部中心

## Points 数组规范

线性元素（arrow、line）的 points 数组包含相对坐标：

```json
{
  "x": 100,
  "y": 50,
  "points": [
    [0, 0],        // 第一个点必须在原点 (相对于 x, y)
    [100, 50],     // 第二个点
    [200, 0]       // 第三个点
  ]
}
```

**关键约束**:
- 第一个点总是 `[0, 0]`
- 所有点相对于元素的 `(x, y)` 位置
- 最少两个点
- 添加中间点可创建弯曲/折线效果

## 分组 (Group) 机制

### groupIds 工作原理

元素通过 `groupIds` 数组属于一个或多个分组：

```json
{
  "type": "rectangle",
  "id": "elem-1",
  "groupIds": ["group-1"]
},
{
  "type": "ellipse",
  "id": "elem-2",
  "groupIds": ["group-1"]
}
```

### 嵌套分组

```json
{
  "type": "rectangle",
  "id": "elem-1",
  "groupIds": ["inner-group", "outer-group"]
}
```

## 框架 (Frame) 使用

框架是容器元素，子元素通过 `frameId` 关联：

```json
{
  "type": "frame",
  "id": "frame-1",
  "x": 50,
  "y": 50,
  "width": 400,
  "height": 300,
  "name": "My Frame"
}
```

子元素关联:
```json
{
  "type": "rectangle",
  "frameId": "frame-1"
}
```

**重要**: 框架元素必须在其子元素之后出现在 elements 数组中。

## Roundness 属性详解

| Type | 名称 | 用途 |
|------|------|------|
| null | 无圆角 | 尖锐边角 |
| 1 | LEGACY | 向后兼容 |
| 2 | PROPORTIONAL | 线性元素圆角 |
| 3 | ADAPTIVE | 形状元素圆角 |

```json
{
  "roundness": {
    "type": 3,
    "value": 32
  }
}
```

## 图片 (Image) 元素

### Image 元素结构

```json
{
  "type": "image",
  "id": "image-1",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 150,
  "fileId": "abc123hash"
}
```

### Files 对象格式

```json
{
  "files": {
    "abc123hash": {
      "mimeType": "image/png",
      "id": "abc123hash",
      "dataURL": "data:image/png;base64,iVBORw0KGgo...",
      "created": 1690295874454,
      "lastRetrieved": 1690295874454
    }
  }
}
```

支持的 MIME 类型:
- `image/png`
- `image/jpeg`
- `image/webp`
- `image/svg+xml`

## 自由绘制 (Freedraw) 元素

```json
{
  "type": "freedraw",
  "id": "freedraw-1",
  "x": 100,
  "y": 100,
  "points": [[0, 0], [10, 5], [20, 15]],
  "pressures": [0.5, 0.6, 0.7],
  "simulatePressure": true
}
```

| 属性 | 类型 | 说明 |
|------|------|------|
| points | array | 绘制路径点（相对坐标）|
| pressures | array | 每个点的压力值 (0-1) |
| simulatePressure | boolean | 是否模拟压力变化 |

## boundElements 属性

追踪绑定到该元素的其他元素：

```json
{
  "type": "rectangle",
  "boundElements": [
    {"id": "text-1", "type": "text"},
    {"id": "arrow-1", "type": "arrow"}
  ]
}
```

## appState 配置

```json
{
  "appState": {
    "gridSize": 20,
    "gridMode": false,
    "viewBackgroundColor": "#ffffff",
    "zoom": {"value": 1},
    "scrollX": 0,
    "scrollY": 0,
    "currentItemRoundness": "round",
    "currentItemStrokeWidth": 2,
    "currentItemStrokeStyle": "solid",
    "currentItemFillStyle": "solid"
  }
}
```

## 完整示例

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "type": "rectangle",
      "id": "rect-1",
      "x": 100,
      "y": 100,
      "width": 150,
      "height": 80,
      "strokeColor": "#1971c2",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "frameId": null,
      "roundness": {"type": 3},
      "seed": 123456,
      "version": 1,
      "versionNonce": 789012,
      "isDeleted": false,
      "boundElements": [
        {"id": "text-1", "type": "text"},
        {"id": "arrow-1", "type": "arrow"}
      ],
      "updated": 1690295874454,
      "link": null,
      "locked": false
    },
    {
      "type": "text",
      "id": "text-1",
      "x": 175,
      "y": 140,
      "text": "开始",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "rect-1",
      "strokeColor": "#1971c2",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 0,
      "opacity": 100,
      "angle": 0,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 234567,
      "version": 1,
      "versionNonce": 890123,
      "isDeleted": false,
      "boundElements": [],
      "updated": 1690295874454,
      "link": null,
      "locked": false,
      "lineHeight": 1.25,
      "originalText": "开始"
    }
  ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## 常见错误与解决

| 错误 | 原因 | 解决 |
|-----|------|------|
| 元素不显示 | 缺少必需属性 | 检查所有必需字段 |
| 绑定失效 | elementId 不存在 | 确保先创建目标元素 |
| 箭头不连接 | boundElements 未更新 | 添加箭头后更新目标元素的 boundElements |
| 文本不在容器内 | containerId 错误 | 检查 containerId 和容器 boundElements |
| 框架不包含子元素 | frameId 未设置 | 设置子元素的 frameId |
| 图片不显示 | fileId 未匹配 | 确保 files 中有对应数据 |
