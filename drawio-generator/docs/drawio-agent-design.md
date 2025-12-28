# DrawIO Agent 工作流设计文档

## 一、项目定位

构建一个专业的 DrawIO 图表生成 Agent，能够处理复杂图表，支持多 Agent 协作。

**核心原则**：
- 效果是唯一评判标准
- 不考虑 token 成本
- 精细化考虑 AI 的输出能力
- 复杂图表必须拆分任务

---

## 二、核心工具设计

### 2.1 知识检索工具

**定位**：上下文工程的核心，实现动态上下文注入

**为什么需要**：
- AI 不可能记住所有画图组件的语法
- 只能按需检索，按需提供模型所需的上下文

**功能需求**：
- 批量检索图标（AWS、Azure、GCP、K8s 等）
- 检索元素语法（mxGraph 元素表示）
- 支持语义搜索（如"我要用数据库图标"能找到 cylinder 形状）
- 返回可直接使用的 style 字符串

**输入**：
```json
{
  "queries": ["AWS Lambda", "数据库", "用户图标"],
  "category": "architecture",  // 可选，限定检索范围
  "limit": 5  // 每个 query 返回的结果数
}
```

**输出**：
```json
{
  "results": {
    "AWS Lambda": [
      {
        "name": "AWS Lambda",
        "shape": "mxgraph.aws4.lambda_function",
        "style": "shape=mxgraph.aws4.lambda_function;...",
        "size": {"width": 78, "height": 78},
        "source": "references/devops.md"
      }
    ],
    "数据库": [...],
    "用户图标": [...]
  }
}
```

### 2.2 布局计算工具

**定位**：解决 AI 无法精确计算坐标的核心难题

**为什么需要**：
- 单纯 AI 无法做好布局
- 布局算法做不好，图表必然丑陋
- 元素大小不确定，坐标难以计算
- 需要代码保证布局的确定性

**核心难点**：
1. **元素尺寸不确定**
   - 文字长度影响节点宽度
   - 不同图标有不同的推荐尺寸
   - 容器大小依赖内部元素

2. **坐标计算复杂**
   - 元素每个顶点的位置
   - 相对位置 vs 绝对位置
   - 连线锚点（exitX, exitY, entryX, entryY）

3. **对齐问题**
   - 元素容易对不齐
   - 连线穿过其他节点
   - 整体布局不美观

**解决方案**：
- 方案 A：纯代码布局（算法确定性高）
- 方案 B：固定零点坐标，所有后续坐标基于零点推算
- 方案 C：布局算法 + AI 微调（推荐）

**输入**：
```json
{
  "nodes": [
    {"id": "gw", "label": "API Gateway", "type": "gateway", "size_hint": "M"},
    {"id": "svc1", "label": "用户服务", "type": "service"}
  ],
  "edges": [
    {"source": "gw", "target": "svc1", "type": "arrow"}
  ],
  "layout_strategy": "layered",  // layered | horizontal | radial | grid
  "canvas": {"width": 800, "height": 600},
  "origin": {"x": 40, "y": 40}  // 零点坐标
}
```

**输出**：
```json
{
  "nodes": [
    {
      "id": "gw",
      "x": 340, "y": 40,
      "width": 120, "height": 60,
      "anchors": {
        "top": {"x": 400, "y": 40},
        "bottom": {"x": 400, "y": 100},
        "left": {"x": 340, "y": 70},
        "right": {"x": 460, "y": 70}
      }
    }
  ],
  "edges": [
    {
      "id": "gw_svc1",
      "source": "gw", "target": "svc1",
      "exit": {"x": 0.5, "y": 1.0},
      "entry": {"x": 0.5, "y": 0.0},
      "waypoints": []
    }
  ],
  "canvas": {"width": 800, "height": 600}
}
```

### 2.3 XML 生成工具（可选）

**功能**：将布局结果 + 样式转换为 DrawIO XML

**为什么可能需要**：
- XML 格式固定，适合模板化生成
- 减少 AI 生成 XML 的出错概率

---

## 三、工作流设计

### 3.1 完整工作流

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              用户输入                                        │
│                   (文字描述 / 图片复刻 / 需求文档)                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Phase 1: 意图理解 (Intent Understanding)                                   │
│  ─────────────────────────────────────────                                  │
│  • 识别用户到底想干嘛                                                         │
│  • 要做什么类型的图表（架构图/流程图/UML/ER图/网络拓扑...）                      │
│  • 复刻场景：分析图片内容                                                      │
│  • 输出：意图识别结果 + 图表类型                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Phase 2: 深度规划 (Deep Planning)                                          │
│  ─────────────────────────────────────────                                  │
│  • 对用户需求进行深度理解                                                      │
│  • 规划图表结构：                                                             │
│    - 有哪些节点（谁、是什么类型）                                              │
│    - 连接关系（谁连谁、什么类型的线、是否有标签）                                │
│    - 分组/容器（哪些节点属于同一个组）                                          │
│    - 层级关系（嵌套结构）                                                      │
│  • 规划布局策略：                                                             │
│    - 上面放什么，下面放什么                                                    │
│    - 哪个节点和谁连在一起                                                      │
│    - 整体是垂直/水平/放射/网格布局                                             │
│  • 查询我们支持的所有元素类型                                                  │
│  • 输出：DiagramSpec（图表规格说明书）                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Phase 3: 知识检索 (Knowledge Retrieval)                                    │
│  ─────────────────────────────────────────                                  │
│  • 根据规划结果，批量检索所需元素                                              │
│  • 检索内容：                                                                │
│    - 图标语法（如 AWS Lambda 的 mxGraph 表示）                                │
│    - 形状样式（如 cylinder 数据库形状）                                        │
│    - 连线样式（箭头类型、虚线等）                                              │
│    - 配色方案                                                                │
│  • 判断哪些检索结果是有用的                                                    │
│  • 输出：ElementLibrary（元素库，包含所有需要的样式字符串）                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Phase 4: 布局计算 (Layout Computation)                                     │
│  ─────────────────────────────────────────                                  │
│  • 调用布局工具，计算节点位置                                                  │
│  • 布局算法处理：                                                             │
│    - 确定每个元素的大小（基于类型和文字长度）                                    │
│    - 计算绝对坐标（基于零点推算）                                              │
│    - 计算连线锚点和路径                                                       │
│    - 处理元素避让（连线不穿过节点）                                            │
│  • AI 微调：                                                                 │
│    - 纯布局算法不够，需要 AI 调整                                              │
│    - 处理算法无法覆盖的特殊情况                                                │
│    - 标注需要特殊处理的区域                                                    │
│  • 输出：LayoutResult（完整布局结果）                                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Phase 5: 分块生成 (Chunked Generation)                                     │
│  ─────────────────────────────────────────                                  │
│  【重要】不建议一次性生成全部 XML                                              │
│                                                                              │
│  • 分块策略：                                                                │
│    - 按区域分块（上半部分/下半部分）                                           │
│    - 按模块分块（用户模块/服务模块/数据模块）                                   │
│    - 按层级分块（先容器，再内部元素）                                          │
│  • 每块生成：                                                                │
│    - 生成该区域的节点 XML                                                     │
│    - 生成该区域的连线 XML                                                     │
│    - 验证该块的正确性                                                         │
│  • 复杂图表可能需要多个 Agent 协作：                                           │
│    - Agent A 负责左半部分                                                     │
│    - Agent B 负责右半部分                                                     │
│    - Coordinator 负责拼装和协调                                               │
│  • 输出：XML 片段列表                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Phase 6: 拼装与验证 (Assembly & Validation)                                │
│  ─────────────────────────────────────────                                  │
│  • 拼装所有 XML 片段                                                         │
│  • 确保全局一致性：                                                           │
│    - ID 不冲突                                                               │
│    - 跨块连线正确                                                             │
│    - 坐标系统统一                                                             │
│  • 验证 XML 结构：                                                            │
│    - mxCell 结构正确                                                         │
│    - 必要属性存在（vertex/edge, as="geometry"）                               │
│    - 连线锚点合理                                                             │
│  • 输出：完整的 .drawio 文件                                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Phase 7: 迭代修正 (Iterative Refinement)                                   │
│  ─────────────────────────────────────────                                  │
│  • 如果验证失败或质量不达标：                                                  │
│    - 结构错误 → 回到 Phase 5 重新生成该块                                      │
│    - 布局问题 → 回到 Phase 4 调整布局                                         │
│    - 元素缺失 → 回到 Phase 3 补充检索                                         │
│    - 规划错误 → 回到 Phase 2 重新规划                                         │
│  • 最多迭代 N 轮                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 复杂图表的多 Agent 协作

对于复杂图表，单个 Agent 难以一次生成正确，需要拆分任务：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Coordinator Agent                                  │
│                         (任务分解与结果整合)                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                    │                    │
         ┌──────────┴──────────┐         │         ┌──────────┴──────────┐
         ▼                     ▼         ▼         ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Planner Agent  │  │  Layout Agent   │  │ Generator Agent │  │ Validator Agent │
│   (需求规划)     │  │   (布局计算)     │  │   (XML 生成)     │  │   (质量验证)     │
└─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
         │                     │                    │                    │
         │                     │                    │                    │
         ▼                     ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             Tool Layer                                       │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐ │
│  │ 知识检索工具   │  │  布局计算工具  │  │ XML 生成工具   │  │  验证工具      │ │
│  └───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
         │                     │                    │                    │
         ▼                     ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Knowledge Layer                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  references/                                                            ││
│  │  ├── shapes.md, edges.md          # 基础元素语法                         ││
│  │  ├── icons.md                     # 图标库                              ││
│  │  ├── layout.md, layout_examples.md # 布局规则                           ││
│  │  ├── ai_ml_assets.md              # AI/ML 领域图标                      ││
│  │  ├── uml.md                       # UML 图形                            ││
│  │  ├── devops.md                    # DevOps/开源生态                      ││
│  │  ├── business.md                  # 业务流程图标                         ││
│  │  ├── network.md                   # 网络拓扑                            ││
│  │  └── color_schemes.md             # 配色方案                            ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.3 任务拆分策略

**按图表复杂度拆分**：

| 复杂度 | 节点数 | 策略 |
|--------|--------|------|
| 简单 | < 10 | 单 Agent 一次生成 |
| 中等 | 10-30 | 分 2-3 块生成 |
| 复杂 | 30-100 | 多 Agent 协作 |
| 超复杂 | > 100 | 分层次逐级生成 |

**按结构拆分**：

- 有容器/泳道：先生成容器，再生成内部元素
- 有分组：按组拆分
- 多层级：按层级拆分

---

## 四、mxGraph 技术要点

### 4.1 必须了解的核心概念

DrawIO 基于 mxGraph，生成正确的 XML 需要理解：

1. **mxCell 结构**
   - 所有元素都是 mxCell
   - 节点：`vertex="1"`
   - 连线：`edge="1"`
   - 必须是 `<root>` 的直接子元素，不能嵌套

2. **mxGeometry**
   - 节点：`x, y, width, height`
   - 连线：`relative="1"`，可选 `waypoints`

3. **Style 字符串**
   - 分号分隔的键值对
   - 如：`rounded=1;fillColor=#dae8fc;strokeColor=#6c8ebf;`

4. **连线锚点**
   - `exitX, exitY`：从源节点哪个点出发 (0-1)
   - `entryX, entryY`：进入目标节点哪个点 (0-1)
   - 必须显式指定，否则连线方向不可控

5. **ID 规则**
   - id="0" 和 id="1" 保留
   - 用户内容从 id="2" 开始
   - ID 必须唯一

### 4.2 常见错误

- mxCell 嵌套 → 图无法解析
- 缺少 `as="geometry"` → 几何信息丢失
- 连线缺少 `relative="1"` → 布局错乱
- 使用角落锚点 (1,1) → 连线不自然
- 坐标不是 10 的倍数 → 不对齐网格

---

## 五、布局算法设计

### 5.1 零点坐标方案

**核心思想**：固定一个零点坐标 (origin)，所有后续坐标基于零点推算

```
origin = (40, 40)  # 画布左上角留边距

node_1.x = origin.x
node_1.y = origin.y

node_2.x = node_1.x + node_1.width + spacing
node_2.y = node_1.y

...以此类推
```

**优点**：
- 坐标计算有明确的参考点
- 容易保证对齐
- 便于调试

### 5.2 元素尺寸确定

**尺寸规格**：

| 规格 | 宽度 | 高度 | 适用场景 |
|------|------|------|----------|
| XS | 60 | 40 | 小图标、简短文字 |
| S | 80 | 40 | 短标签 |
| M | 120 | 60 | 标准节点（默认） |
| L | 160 | 80 | 长文字、重要节点 |
| XL | 200 | 100 | 容器标题、大型组件 |

**动态计算**：
```
width = max(MIN_WIDTH, len(label) * CHAR_WIDTH + PADDING)
height = 固定值（根据规格）
```

### 5.3 连线路径计算

1. 根据节点相对位置确定锚点
2. 检查直线是否穿过其他节点
3. 如果穿过，计算 waypoints 绕行
4. 多条连线共享路径时，微调锚点避免重叠

---

## 六、数据结构定义

### 6.1 DiagramSpec（规划输出）

```typescript
interface DiagramSpec {
  diagram_type: 'flowchart' | 'architecture' | 'uml' | 'er' | 'network' | 'mindmap' | 'sequence';
  title: string;
  description: string;  // 图表描述，用于理解上下文

  nodes: NodeSpec[];
  edges: EdgeSpec[];
  groups: GroupSpec[];
  containers: ContainerSpec[];  // 泳道、容器

  layout: {
    strategy: 'layered' | 'horizontal' | 'radial' | 'grid' | 'custom';
    direction: 'TB' | 'BT' | 'LR' | 'RL';  // Top-Bottom, Left-Right...
    spacing: number;
    layer_spacing: number;
  };

  theme: 'professional' | 'tech' | 'minimal' | 'colorful' | 'dark';
}

interface NodeSpec {
  id: string;
  label: string;
  type: string;  // gateway, service, database, user, decision, process...
  size_hint: 'XS' | 'S' | 'M' | 'L' | 'XL';
  group?: string;
  container?: string;
  icon?: string;  // 指定使用的图标
  style_override?: object;  // 样式覆盖
}

interface EdgeSpec {
  id: string;
  source: string;
  target: string;
  label?: string;
  type: 'arrow' | 'dashed' | 'bidirectional' | 'none';
  style_override?: object;
}

interface GroupSpec {
  id: string;
  label: string;
  members: string[];  // 包含的节点 ID
  style?: object;
}

interface ContainerSpec {
  id: string;
  label: string;
  type: 'swimlane' | 'group' | 'region';
  children: string[];  // 可以是节点或其他容器
  position_hint?: 'left' | 'right' | 'top' | 'bottom';
}
```

### 6.2 ElementLibrary（检索结果）

```typescript
interface ElementLibrary {
  nodes: {
    [node_id: string]: {
      shape: string;
      style: string;  // 完整的 DrawIO style 字符串
      size: { width: number; height: number };
    }
  };
  edge_styles: {
    [edge_type: string]: string;  // edge type -> style string
  };
  theme_colors: {
    primary: string;
    secondary: string;
    accent: string;
    // ...
  };
}
```

### 6.3 LayoutResult（布局结果）

```typescript
interface LayoutResult {
  canvas: {
    width: number;
    height: number;
    origin: { x: number; y: number };
  };

  nodes: {
    id: string;
    x: number;
    y: number;
    width: number;
    height: number;
    z_index?: number;  // 层级
  }[];

  edges: {
    id: string;
    source: string;
    target: string;
    exit: { x: number; y: number };   // 0-1
    entry: { x: number; y: number };  // 0-1
    waypoints: { x: number; y: number }[];
  }[];

  containers: {
    id: string;
    x: number;
    y: number;
    width: number;
    height: number;
    children_layout: LayoutResult;  // 递归结构
  }[];
}
```

---

## 七、待解决问题

1. **元素尺寸动态计算**
   - 如何准确估算文字渲染后的宽度？
   - 不同字体、字号的影响？

2. **复杂容器布局**
   - 嵌套容器如何计算内部布局？
   - 容器大小如何自适应内容？

3. **跨块连线**
   - 分块生成时，跨块的连线如何处理？
   - 如何保证锚点计算正确？

4. **全局一致性**
   - 分块生成后，整体风格如何保持一致？
   - 配色、间距如何统一？

5. **错误恢复**
   - 某一块生成失败，如何定位问题？
   - 如何最小化重新生成的范围？

---

## 八、专家评审结论

### 8.1 双路径设计（评审推荐）

**核心发现**：不是所有图表都需要完整工具链

```
用户输入
    ↓
需求分析 → DiagramSpec → 评估复杂度
    ↓
[Simple ≤ 5 节点] ──→ Claude 直接生成（读 references，手工计算）
    ↓
[Complex > 5 节点] ──→ 工具链路径（Layout → Element → Generator → Validator）
```

**复杂度判断标准**：
- **Simple**：节点数 ≤ 5，无分组，连线无交叉
- **Complex**：其他所有情况

**Simple 模式优势**：
- 速度快（< 5 秒）
- 无工具调用开销
- 适合快速草图

### 8.2 布局难点深入分析

#### 8.2.1 边路径规划（最难问题）

**三层难度**：

1. **锚点选择**
   - 问题：多条边连接同一对节点会重叠
   - 方案：智能锚点分配（0.5 → 0.3 → 0.7 → 0.2 → 0.8）

```python
def select_smart_anchors(src, tgt, existing_edges):
    """智能锚点选择，避免边重叠"""
    same_pair_count = count_edges_between(src, tgt, existing_edges)
    offset_positions = [0.5, 0.3, 0.7, 0.2, 0.8]
    offset = offset_positions[min(same_pair_count, 4)]

    if is_horizontal(src, tgt):
        return (1.0, offset), (0.0, offset)
    else:
        return (offset, 1.0), (offset, 0.0)
```

2. **障碍物检测**
   - 问题：当前只检查线段中点，不准确
   - 方案：线段-矩形精确相交检测（Liang-Barsky 算法）

3. **Waypoint 生成**
   - 问题：复杂路径需要多个拐点
   - 方案：A* 路径规划算法

```python
def compute_path_astar(src, tgt, obstacles, grid_size=20):
    """A* 算法计算最优绕行路径"""
    # 1. 构建可行路径网格
    # 2. 障碍物膨胀（留出边距）
    # 3. A* 搜索最短路径
    # 4. 简化路径（移除共线点）
    pass
```

#### 8.2.2 节点尺寸动态计算

**问题**：当前所有节点固定 120×60，不合理

**方案**：

```python
def estimate_node_size(node: dict) -> Tuple[int, int]:
    """动态估算节点尺寸"""
    node_type = node.get('type', 'default')
    label = node.get('label', '')

    # 1. 形状基础尺寸
    BASE_SIZES = {
        'cylinder': (120, 80),      # 圆柱体需要高一些
        'diamond': (100, 100),      # 菱形要方
        'ellipse': (100, 60),       # 椭圆
        'default': (120, 60),
    }
    base_w, base_h = BASE_SIZES.get(TYPE_SHAPE_MAP.get(node_type), (120, 60))

    # 2. 根据标签长度调整宽度
    # 中文字符 ≈ 12px，英文字符 ≈ 7px
    label_width = sum(12 if ord(c) > 127 else 7 for c in label) + 24
    width = max(base_w, label_width)

    # 3. 对齐到网格
    width = round(width / 10) * 10

    return width, base_h
```

### 8.3 零点坐标方案评审

**三种方案对比**：

| 方案 | 零点位置 | 优点 | 缺点 |
|------|---------|------|------|
| A | 画布左上角 (40, 40) | 简单直观 | 扩展时需整体重算 |
| B | 图表中心 | 便于对称布局、增量扩展 | 坐标计算复杂 |
| C | 根节点位置 | 符合直觉 | 不适合网状图 |

**评审推荐：方案 B（以图表中心为零点）**

```python
class CenterBasedLayout:
    def __init__(self, canvas_width=800, canvas_height=600):
        self.origin_x = canvas_width // 2
        self.origin_y = canvas_height // 2

    def place_node(self, relative_x, relative_y, width, height):
        """相对原点放置节点"""
        absolute_x = self.origin_x + relative_x - width // 2
        absolute_y = self.origin_y + relative_y - height // 2
        return self._snap_to_grid(absolute_x), self._snap_to_grid(absolute_y)
```

**优势**：
- 便于增量添加节点（新节点相对已有节点定位）
- 自然支持对称布局
- 便于实现"固定某些节点，调整其他节点"

### 8.4 分块生成评审结论

**结论：大多数情况不需要分块**

**理由**：
- 500 节点的 XML 文件也就几百 KB
- Claude 的上下文窗口完全够
- 分块反而增加复杂度和出错概率
- 全局 ID 管理更简单

**何时需要分块**：
- 超大图表（1000+ 节点）
- 需要多人协作编辑
- 需要增量更新

**如果必须分块**：
```python
class StreamingDrawioGenerator:
    def __init__(self):
        self.id_counter = 2
        self.node_id_map = {}  # 维护全局 ID 映射

    def generate_nodes_batch(self, nodes_batch):
        """先生成所有节点，建立 ID 映射"""
        for node in nodes_batch:
            cell_id = str(self._next_id())
            self.node_id_map[node['id']] = cell_id
        ...

    def generate_edges_batch(self, edges_batch):
        """后生成边，必须在所有节点生成后"""
        for edge in edges_batch:
            src_id = self.node_id_map[edge['source']]  # 查找 ID
            tgt_id = self.node_id_map[edge['target']]
        ...
```

### 8.5 效果评估标准

**验收标准**：

| 指标 | 标准 | 检测方法 |
|------|------|---------|
| 节点不重叠 | 间距 ≥ 120px | 碰撞检测算法 |
| 连线不穿过节点 | 无相交或使用 waypoint | 相交检测 |
| 相同类型节点一致 | 样式、尺寸一致 | 样式对比 |
| XML 格式正确 | 符合 DrawIO 规范 | validate_drawio.py |
| 美观性 | 对齐、对称、紧凑 | 人工审核 / 规则检查 |

**性能目标**：
- Simple 模式：< 5 秒
- Complex 模式：< 30 秒（含迭代）

### 8.6 改进优先级

| 优先级 | 改进项 | 当前状态 | 收益 |
|--------|--------|---------|------|
| ⭐⭐⭐ | 动态节点尺寸 | 固定 120×60 | 布局更准确 |
| ⭐⭐⭐ | A* 路径规划 | 简单中点检测 | 复杂连线正确 |
| ⭐⭐⭐ | Simple/Complex 双路径 | 无 | 简单图表快速生成 |
| ⭐⭐ | 智能锚点选择 | 固定锚点 | 避免边重叠 |
| ⭐⭐ | 容器/分组支持 | 无 | 支持复杂结构 |
| ⭐ | 图标集成 | 无 | 支持云服务图标 |
| ⭐ | 全局布局优化 | 无 | 更美观 |

---

## 九、下一步行动

### Phase 1：必须完成（高优先级）

1. **实现 Simple/Complex 双路径**
   - 在 SKILL.md 中定义复杂度判断标准
   - Simple 模式：Claude 直接读 references 生成
   - Complex 模式：调用工具链

2. **改进 Layout 工具**
   - 动态节点尺寸计算（根据类型 + 标签长度）
   - A* 路径规划替代简单中点检测
   - 智能锚点选择（避免边重叠）

3. **更新 SKILL.md**
   - 修正 "Agent" 术语为 "阶段/工具"
   - 添加决策树和复杂度判断标准
   - 明确 Claude 在每个阶段应该做什么

### Phase 2：推荐完成（中优先级）

4. **增强 Validator 工具**
   - 添加布局质量检查（重叠、间距）
   - 输出具体的修复建议
   - 支持增量验证

5. **优化知识检索工具**
   - 集成到主工作流
   - 支持批量检索 API
   - 缓存常用元素

6. **支持容器和分组**
   - 在 DiagramSpec 中添加 containers 字段
   - Layout 工具支持嵌套布局
   - Generator 工具生成容器 XML

### Phase 3：可选完成（低优先级）

7. **全局布局优化**
   - 对齐同类节点
   - 紧凑化（移除空白）
   - 对称性优化

8. **图标库集成**
   - 解析 references/*.md 中的图标定义
   - 生成可用图标索引
   - 在 Element 工具中自动匹配

9. **多页支持**
   - 支持生成多个 `<diagram>` 标签
   - 页面间引用

---

## 十、附录

### A. 工具命令速查

```bash
# 布局计算
python scripts/layout_agent.py --spec spec.json --output layout.json

# 样式匹配
python scripts/element_agent.py --spec spec.json --theme professional --output styles.json

# XML 生成
python scripts/generator_agent.py --layout layout.json --styles styles.json --spec spec.json --output diagram.drawio

# 验证
python scripts/validate_drawio.py diagram.drawio

# 素材检索
python scripts/asset_search.py --query "AWS Lambda" --json
```

### B. 参考文档索引

| 需求 | 文件 |
|------|------|
| 基础形状 | `references/shapes.md` |
| 连线规则 | `references/edges.md` |
| 布局约束 | `references/layout.md` |
| 布局示例 | `references/layout_examples.md` |
| 图标库 | `references/icons.md` |
| 配色方案 | `references/color_schemes.md` |
| AI/ML 图标 | `references/ai_ml_assets.md` |
| UML 图形 | `references/uml.md` |
| DevOps 图标 | `references/devops.md` |
| 业务流程 | `references/business.md` |
| 网络拓扑 | `references/network.md` |

### C. 文档版本

- 创建日期：2025-01-XX
- 最后更新：2025-01-XX
- 评审状态：已完成 5 轮深度评审
