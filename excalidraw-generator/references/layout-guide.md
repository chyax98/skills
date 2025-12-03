# Excalidraw 布局算法指南

## 自动布局算法

### 1. flowchart_layout (流程图布局)

**垂直布局** (默认):
- 节点从上到下排列
- 适用于流程图、决策树
- 连线方向：向下

**水平布局**:
- 节点从左到右排列
- 适用于时间线、管道图
- 连线方向：向右

**参数建议**:
```python
{
    "direction": "vertical",  # vertical | horizontal
    "spacing_x": 150,         # 水平间距
    "spacing_y": 100,         # 垂直间距
    "start_x": 100,           # 起始 X 坐标
    "start_y": 100            # 起始 Y 坐标
}
```

### 2. grid_layout (网格布局)

**说明**: 元素按网格排列，适用于卡片、图标集、矩阵结构

**参数建议**:
```python
{
    "columns": 3,             # 列数
    "spacing_x": 120,         # 列间距
    "spacing_y": 100,         # 行间距
    "start_x": 50,            # 起始 X
    "start_y": 50             # 起始 Y
}
```

### 3. hierarchy_layout (树形层次布局)

**说明**: 根节点在顶部，子节点逐层展开

**层级计算**:
- Level 0: 根节点
- Level 1: 第一层子节点
- Level 2: 第二层子节点
- ...

**参数建议**:
```python
{
    "level_spacing": 150,     # 层级间距
    "sibling_spacing": 120,   # 兄弟节点间距
    "start_x": 400,           # 根节点 X
    "start_y": 50             # 根节点 Y
}
```

### 4. circular_layout (环形布局)

**说明**: 节点沿圆形排列，中心可选

**参数建议**:
```python
{
    "radius": 200,            # 圆半径
    "center_x": 400,          # 圆心 X
    "center_y": 300,          # 圆心 Y
    "start_angle": 0,         # 起始角度 (度)
    "has_center": True        # 是否有中心节点
}
```

## 布局参数推荐

### 节点间距

| 布局类型 | 水平间距 | 垂直间距 | 说明 |
|---------|---------|---------|------|
| 流程图 | 150-200 | 100-150 | 预留箭头空间 |
| 网格 | 120-150 | 100-120 | 紧凑排列 |
| 树形 | 100-150 | 120-180 | 强调层级 |
| 环形 | - | - | 使用半径控制 |

### 画布边距

| 位置 | 推荐值 | 说明 |
|-----|--------|------|
| 左边距 | 50-100 | 避免贴边 |
| 上边距 | 50-100 | 标题空间 |
| 右边距 | 50 | 预留空间 |
| 下边距 | 50 | 预留空间 |

## 节点尺寸推荐

### 根据文本长度

| 文本长度 | 宽度 | 高度 | 字体大小 |
|---------|------|------|---------|
| 1-5 字符 | 80-100 | 60-80 | 16-20 |
| 6-10 字符 | 120-150 | 60-80 | 16-18 |
| 11-20 字符 | 160-200 | 70-90 | 14-16 |
| 21+ 字符 | 200-250 | 80-100 | 12-14 |

### 形状类型

| 形状 | 推荐宽度 | 推荐高度 | 用途 |
|-----|---------|---------|------|
| rectangle | 120-200 | 60-80 | 流程步骤 |
| ellipse | 100-150 | 100-150 | 开始/结束 |
| diamond | 140-180 | 100-120 | 决策点 |

## 常见布局模式

### 线性流程 (Vertical)

```
开始 (ellipse, 120x100)
  ↓ (spacing: 100)
步骤1 (rectangle, 150x70)
  ↓
步骤2 (rectangle, 150x70)
  ↓
结束 (ellipse, 120x100)
```

### 决策流程 (Branching)

```
       步骤
         ↓
      决策? (diamond)
      ↙    ↘
    是      否
     ↓       ↓
   处理A   处理B
     ↓       ↓
       合并
```

**参数**:
- 菱形宽度: 140-160
- 分支水平偏移: ±100-150
- 垂直间距: 120-150

### 并行流程 (Parallel)

```
开始
  ↓
 分发
↙ ↓ ↘
A  B  C
↘ ↓ ↙
 汇总
  ↓
结束
```

**参数**:
- 并行节点间距: 120-150
- 垂直层间距: 100-120

### 层次结构 (Tree)

```
        根
    ↙  ↓  ↘
   A   B   C
  ↙↘  ↓  ↙↘
 A1 A2 B1 C1 C2
```

**参数**:
- Level 0-1 间距: 150
- Level 1-2 间距: 120
- 兄弟节点间距: 100-120

## 动态尺寸计算

### 文本宽度估算

```python
def estimate_text_width(text: str, font_size: int) -> int:
    char_count = len(text)
    avg_char_width = font_size * 0.6
    padding = 40
    return int(char_count * avg_char_width + padding)
```

### 推荐尺寸

```python
def recommend_size(text: str, shape: str):
    text_len = len(text)

    if shape == "ellipse":
        size = max(100, text_len * 10)
        return (size, size)

    elif shape == "rectangle":
        width = max(120, text_len * 8 + 40)
        height = 70
        return (width, height)

    elif shape == "diamond":
        width = max(140, text_len * 10 + 40)
        height = max(100, width * 0.7)
        return (width, height)
```

## 箭头路径计算

### 直线箭头

```python
def straight_arrow(from_node, to_node):
    return {
        "points": [[0, 0], [to_node.x - from_node.x, to_node.y - from_node.y]]
    }
```

### 垂直/水平箭头

```python
def vertical_arrow(from_node, to_node):
    from_center_x = from_node.x + from_node.width / 2
    from_bottom_y = from_node.y + from_node.height

    to_center_x = to_node.x + to_node.width / 2
    to_top_y = to_node.y

    return {
        "x": from_center_x,
        "y": from_bottom_y,
        "width": abs(to_center_x - from_center_x),
        "height": abs(to_top_y - from_bottom_y)
    }
```

## 画布尺寸计算

```python
def calculate_canvas_bounds(elements):
    min_x = min(e.x for e in elements)
    min_y = min(e.y for e in elements)
    max_x = max(e.x + e.width for e in elements)
    max_y = max(e.y + e.height for e in elements)

    padding = 50

    return {
        "width": max_x - min_x + padding * 2,
        "height": max_y - min_y + padding * 2
    }
```
