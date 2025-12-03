---
name: excalidraw-generator
description: This skill enables generation of Excalidraw diagrams (.excalidraw JSON format) directly from text descriptions. Claude Code reads the JSON specification and generates diagrams without script dependencies. Supports flowcharts, architecture diagrams, mind maps, and hand-drawn style sketches with full Excalidraw element control.
license: MIT
---

# Excalidraw 图表生成器

## 概述

根据用户描述**直接生成** Excalidraw JSON 文件。Claude Code 掌握完整的 Excalidraw v2 JSON 规范，可生成任意复杂度的手绘风格图表。

**核心能力**：
- 直接生成 JSON，无脚本依赖
- 完整控制每个元素的位置、样式、连线
- 支持分组、框架、弯曲箭头、正交箭头
- 生成的文件可在 https://excalidraw.com 打开编辑

## 适用场景

**触发短语**：
- "生成 excalidraw 图表"
- "创建手绘风格图"
- "画 .excalidraw 文件"

**适用**：手绘风格、白板草图、快速原型、教学演示、思维导图

**不适用**：专业正式图表 → drawio-generator | 简单示意 → mermaid

---

## JSON 核心规范

### 文件结构

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| type | string | 是 | 固定值 `"excalidraw"` |
| version | number | 是 | 固定值 `2` |
| source | string | 是 | 来源 URL |
| elements | array | 是 | 画布元素数组 |
| appState | object | 否 | 应用状态 |
| files | object | 否 | 图片数据 (base64) |

### 基础元素结构

```json
{
  "type": "rectangle",
  "id": "唯一ID",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 80,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": {"type": 3},
  "seed": 12345,
  "version": 1,
  "versionNonce": 67890,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

### 属性分类

| 分类 | 属性 | 说明 |
|------|------|------|
| **必需** | `type`, `id`, `x`, `y` | 元素类型、唯一标识、位置 |
| **推荐** | `width`, `height`, `strokeColor`, `backgroundColor` | 尺寸和颜色 |
| **有默认值** | `angle`(0), `opacity`(100), `roughness`(1), `strokeWidth`(1), `fillStyle`("hachure"), `strokeStyle`("solid") | 可省略 |
| **自动生成** | `seed`, `version`, `versionNonce`, `updated` | 随机数/时间戳 |
| **关系型** | `groupIds`, `frameId`, `boundElements` | 分组/框架/绑定 |

**⚠️ 注意**：为确保兼容性，建议提供完整属性。`seed` 和 `versionNonce` 使用随机整数。

---

## 元素类型

### 形状

| 类型 | type 值 | 说明 |
|------|---------|------|
| 矩形 | `rectangle` | 流程步骤，圆角用 `roundness: {type: 3}` |
| 椭圆 | `ellipse` | 开始/结束节点 |
| 菱形 | `diamond` | 决策/判断节点 |

### 线性元素

| 类型 | type 值 | 说明 |
|------|---------|------|
| 箭头 | `arrow` | 有 points 数组、startBinding、endBinding |
| 直线 | `line` | 仅有 points 数组 |

### 其他

| 类型 | type 值 | 说明 |
|------|---------|------|
| 文本 | `text` | 独立或绑定到容器 (containerId) |
| 框架 | `frame` | 容器，子元素用 frameId 关联 |
| 自由绘制 | `freedraw` | 手写笔迹 |
| 图片 | `image` | 需配合 files 字段 |

---

## 样式速查

### 配色方案

| 用途 | strokeColor | backgroundColor |
|------|-------------|-----------------|
| 蓝色/信息 | #1971c2 | #a5d8ff |
| 绿色/成功 | #2f9e44 | #b2f2bb |
| 黄色/警告 | #f08c00 | #ffe066 |
| 红色/错误 | #e03131 | #ffc9c9 |
| 紫色/标记 | #9c36b5 | #e599f7 |
| 灰色/辅助 | #495057 | #ced4da |

### 填充样式 (fillStyle)

| 值 | 效果 |
|----|------|
| `solid` | 实心填充 |
| `hachure` | 斜线填充 |
| `cross-hatch` | 交叉斜线 |
| `zigzag` | 锯齿填充 |

### 边框样式 (strokeStyle)

| 值 | 效果 |
|----|------|
| `solid` | 实线 |
| `dashed` | 虚线 |
| `dotted` | 点线 |

### 手绘度 (roughness)

| 值 | 效果 |
|----|------|
| 0 | 光滑精确 |
| 1 | 轻微手绘（默认）|
| 2 | 明显手绘 |

---

## 箭头与连线

### 基础箭头

```json
{
  "type": "arrow",
  "id": "arrow_1",
  "x": 175,
  "y": 180,
  "width": 0,
  "height": 70,
  "points": [[0, 0], [0, 70]],
  "startBinding": {
    "elementId": "rect_1",
    "focus": 0,
    "gap": 1
  },
  "endBinding": {
    "elementId": "rect_2",
    "focus": 0,
    "gap": 1
  },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "strokeColor": "#1e1e1e",
  "strokeWidth": 2,
  "roughness": 1,
  ...其他必需属性
}
```

### points 数组规范

- 第一个点必须是 `[0, 0]`（相对于元素 x, y）
- 最少两个点
- 多个点创建弯曲/折线效果

```json
// 直线箭头
"points": [[0, 0], [0, 100]]

// 弯曲箭头 (3个点)
"points": [[0, 0], [50, 50], [100, 0]]

// 正交箭头 (4个点，90度转折)
"points": [[0, 0], [50, 0], [50, 100], [100, 100]]
```

### Binding (绑定)

```json
{
  "startBinding": {
    "elementId": "目标元素ID",
    "focus": 0,
    "gap": 1
  }
}
```

| 属性 | 范围 | 说明 |
|------|------|------|
| elementId | string | 绑定目标 ID |
| focus | -1 到 1 | 连接点位置 (0=中间) |
| gap | ≥0 | 与目标的间距 |

### Arrowhead 类型

| 值 | 效果 |
|----|------|
| `null` | 无箭头 |
| `"arrow"` | 普通箭头 |
| `"triangle"` | 实心三角 |
| `"triangle_outline"` | 空心三角 |
| `"diamond"` | 实心菱形 |
| `"diamond_outline"` | 空心菱形 |
| `"dot"` | 实心点 |
| `"circle"` | 实心圆 |
| `"circle_outline"` | 空心圆 |
| `"bar"` | 横杠 |

---

## 文本与容器

### 独立文本

```json
{
  "type": "text",
  "id": "text_1",
  "x": 100,
  "y": 100,
  "text": "Hello World",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "Hello World",
  "lineHeight": 1.25,
  ...其他基础属性
}
```

**文本特有属性：**

| 属性 | 必需 | 说明 |
|------|------|------|
| `text` | 是 | 显示内容 |
| `fontSize` | 是 | 字号 (默认 20) |
| `fontFamily` | 是 | 字体 (1-4) |
| `textAlign` | 否 | 水平对齐 (left/center/right) |
| `verticalAlign` | 否 | 垂直对齐 (top/middle/bottom) |
| `containerId` | 否 | 容器 ID (null 表示独立文本) |
| `originalText` | 否 | 原始文本 |
| `lineHeight` | 否 | 行高 (默认 1.25) |

> **注意**: `baseline` 属性在 v0.18.0 已废弃，不再需要。旧文件中的 `baseline` 会被忽略。

### 容器内文本

```json
// 容器
{
  "type": "rectangle",
  "id": "container_1",
  "boundElements": [{"id": "text_in_1", "type": "text"}],
  ...
}

// 容器内的文本
{
  "type": "text",
  "id": "text_in_1",
  "containerId": "container_1",
  "text": "容器标签",
  ...
}
```

### 字体 (fontFamily)

| 值 | 字体 |
|----|------|
| 1 | Virgil (手写体，默认) |
| 2 | Helvetica |
| 3 | Cascadia (等宽) |
| 4 | Assistant |

---

## 分组与框架

### 分组 (groupIds)

```json
// 同一分组的元素共享 groupIds
{"id": "elem_1", "groupIds": ["group_1"], ...}
{"id": "elem_2", "groupIds": ["group_1"], ...}

// 嵌套分组
{"id": "elem_3", "groupIds": ["inner_group", "outer_group"], ...}
```

### 框架 (Frame)

```json
// 框架容器
{
  "type": "frame",
  "id": "frame_1",
  "name": "框架名称",
  "x": 50,
  "y": 50,
  "width": 400,
  "height": 300,
  ...
}

// 框架内的子元素
{
  "type": "rectangle",
  "id": "child_1",
  "frameId": "frame_1",
  ...
}
```

**⚠️ 注意**：框架元素必须在其子元素之后出现在 elements 数组中

---

## 输出配置

**路径优先级**:
1. 用户指定路径 → 使用用户路径
2. 未指定 → `./excalidraw-generator/`（项目根目录下，自动创建）

**文件命名**: `{主题}-{类型}-{日期}.excalidraw`
- 示例: `login-flow-20251202.excalidraw`

**注意**: 输出基于当前工作目录 `$PWD`，非 skill 安装目录

---

## 生成流程

### 1. 分析需求
- 识别图表类型（流程图/架构图/思维导图）
- 提取节点和关系
- 确定布局方向

### 2. 规划布局
- 估算画布大小
- 规划节点坐标（建议间距：100-150px）
- 使用有意义的 ID 命名

### 3. 生成 JSON
- 按模板生成完整 JSON
- 确保所有元素包含必需属性
- 文本换行使用 `\n`
- 箭头的 source/target 引用有效 ID
- boundElements 双向关联正确

### 4. 保存验证
- 保存为 `.excalidraw` 文件
- 用 `open xxx.excalidraw` 或上传 excalidraw.com 验证

---

## 验证清单

生成后自检：

- [ ] 顶层结构完整：type, version, elements, appState
- [ ] 每个元素包含所有必需属性
- [ ] ID 唯一且有意义
- [ ] 箭头 points 第一个点是 `[0, 0]`
- [ ] Binding 的 elementId 引用存在的元素
- [ ] 容器的 boundElements 和文本的 containerId 双向关联
- [ ] 框架在子元素之后
- [ ] seed 和 versionNonce 是有效数字

---

## 参考资源

### references/
- `excalidraw-spec.md` - 完整 JSON 规范
- `layout-guide.md` - 布局参数指南

### assets/
- 生成的图表存放目录
- 复杂示例可用于参考学习

### scripts/（可选）
- `validator.py` - JSON 格式验证工具

---

## 示例：简单流程图

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "type": "ellipse",
      "id": "start",
      "x": 100,
      "y": 50,
      "width": 120,
      "height": 60,
      "angle": 0,
      "strokeColor": "#2f9e44",
      "backgroundColor": "#b2f2bb",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 123456,
      "version": 1,
      "versionNonce": 789012,
      "isDeleted": false,
      "boundElements": [
        {"id": "text_start", "type": "text"},
        {"id": "arrow_1", "type": "arrow"}
      ],
      "updated": 1700000000000,
      "link": null,
      "locked": false
    },
    {
      "type": "text",
      "id": "text_start",
      "x": 160,
      "y": 80,
      "width": 40,
      "height": 25,
      "angle": 0,
      "strokeColor": "#2f9e44",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 0,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 234567,
      "version": 1,
      "versionNonce": 890123,
      "isDeleted": false,
      "boundElements": [],
      "updated": 1700000000000,
      "link": null,
      "locked": false,
      "text": "开始",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "start",
      "originalText": "开始",
      "lineHeight": 1.25
    },
    {
      "type": "rectangle",
      "id": "process",
      "x": 100,
      "y": 180,
      "width": 120,
      "height": 60,
      "angle": 0,
      "strokeColor": "#1971c2",
      "backgroundColor": "#a5d8ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": {"type": 3},
      "seed": 345678,
      "version": 1,
      "versionNonce": 901234,
      "isDeleted": false,
      "boundElements": [
        {"id": "text_process", "type": "text"},
        {"id": "arrow_1", "type": "arrow"},
        {"id": "arrow_2", "type": "arrow"}
      ],
      "updated": 1700000000000,
      "link": null,
      "locked": false
    },
    {
      "type": "text",
      "id": "text_process",
      "x": 160,
      "y": 210,
      "width": 40,
      "height": 25,
      "angle": 0,
      "strokeColor": "#1971c2",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 0,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 456789,
      "version": 1,
      "versionNonce": 123456,
      "isDeleted": false,
      "boundElements": [],
      "updated": 1700000000000,
      "link": null,
      "locked": false,
      "text": "处理",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "process",
      "originalText": "处理",
      "lineHeight": 1.25
    },
    {
      "type": "ellipse",
      "id": "end",
      "x": 100,
      "y": 310,
      "width": 120,
      "height": 60,
      "angle": 0,
      "strokeColor": "#e03131",
      "backgroundColor": "#ffc9c9",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 567890,
      "version": 1,
      "versionNonce": 234567,
      "isDeleted": false,
      "boundElements": [
        {"id": "text_end", "type": "text"},
        {"id": "arrow_2", "type": "arrow"}
      ],
      "updated": 1700000000000,
      "link": null,
      "locked": false
    },
    {
      "type": "text",
      "id": "text_end",
      "x": 160,
      "y": 340,
      "width": 40,
      "height": 25,
      "angle": 0,
      "strokeColor": "#e03131",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 0,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 678901,
      "version": 1,
      "versionNonce": 345678,
      "isDeleted": false,
      "boundElements": [],
      "updated": 1700000000000,
      "link": null,
      "locked": false,
      "text": "结束",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "end",
      "originalText": "结束",
      "lineHeight": 1.25
    },
    {
      "type": "arrow",
      "id": "arrow_1",
      "x": 160,
      "y": 110,
      "width": 0,
      "height": 70,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": {"type": 2},
      "seed": 789012,
      "version": 1,
      "versionNonce": 456789,
      "isDeleted": false,
      "boundElements": [],
      "updated": 1700000000000,
      "link": null,
      "locked": false,
      "points": [[0, 0], [0, 70]],
      "startBinding": {
        "elementId": "start",
        "focus": 0,
        "gap": 1
      },
      "endBinding": {
        "elementId": "process",
        "focus": 0,
        "gap": 1
      },
      "startArrowhead": null,
      "endArrowhead": "arrow",
      "lastCommittedPoint": null
    },
    {
      "type": "arrow",
      "id": "arrow_2",
      "x": 160,
      "y": 240,
      "width": 0,
      "height": 70,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": {"type": 2},
      "seed": 890123,
      "version": 1,
      "versionNonce": 567890,
      "isDeleted": false,
      "boundElements": [],
      "updated": 1700000000000,
      "link": null,
      "locked": false,
      "points": [[0, 0], [0, 70]],
      "startBinding": {
        "elementId": "process",
        "focus": 0,
        "gap": 1
      },
      "endBinding": {
        "elementId": "end",
        "focus": 0,
        "gap": 1
      },
      "startArrowhead": null,
      "endArrowhead": "arrow",
      "lastCommittedPoint": null
    }
  ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```
