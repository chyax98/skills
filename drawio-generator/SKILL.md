---
name: drawio-generator
description: This skill enables generation of professional DrawIO diagrams (.drawio XML format) directly from text descriptions. Claude Code reads the XML specification and generates diagrams without script dependencies. Supports flowcharts, architecture diagrams, UML, ER diagrams, and network topology with full mxGraph XML control.
license: Apache-2.0
---

# DrawIO 图表生成器

根据用户描述生成 DrawIO XML 文件（.drawio），采用多 Agent 协作架构。

## 多 Agent 工作流程

```
用户需求 → Planner → Layout → Element → Generator → Validator → .drawio
              ↑                                          │
              └──────── 迭代修复 (最多 3 轮) ─────────────┘
```

### Phase 1: 需求规划 (Planner Agent)

**触发**: 用户描述图表需求

**任务**: 使用 Task tool 调用 sub-agent 分析需求，输出 DiagramSpec JSON

**Prompt 模板**:
```
分析用户的图表需求，输出结构化的 DiagramSpec JSON。

用户需求: {user_input}

输出格式:
{
  "diagram_type": "flowchart|architecture|uml|er|network|mindmap",
  "title": "图表标题",
  "nodes": [
    {"id": "唯一ID", "label": "显示文字", "type": "节点类型", "group": null}
  ],
  "edges": [
    {"id": "边ID", "source": "源节点ID", "target": "目标节点ID", "label": null, "type": "arrow|dashed|bidirectional"}
  ],
  "groups": [],
  "layout_hint": "horizontal|vertical|radial|grid|auto",
  "theme": "professional|tech|minimal|colorful|dark"
}

节点类型参考: gateway, service, database, user, client, decision, process, start, end, cache, queue, loadbalancer, firewall, server, cloud
```

### Phase 2: 布局计算 (Layout Agent)

**工具**: `scripts/layout_agent.py`

```bash
# 将 DiagramSpec 保存为 spec.json 后执行
python scripts/layout_agent.py --spec spec.json --output layout.json

# 可选参数
--algorithm auto|layered|horizontal|radial|grid  # 布局算法
--spacing 120                                      # 节点间距
--width 800 --height 600                          # 画布尺寸
```

**输出**: LayoutResult JSON (节点位置 + 边路径 + 锚点)

### Phase 3: 样式匹配 (Element Agent)

**工具**: `scripts/element_agent.py`

```bash
python scripts/element_agent.py --spec spec.json --theme professional --output styles.json

# 查看可用主题和节点类型
python scripts/element_agent.py --list-themes
python scripts/element_agent.py --list-types
```

**输出**: ElementStyles JSON (每个节点的形状和样式字符串)

### Phase 4: XML 生成 (Generator Agent)

**工具**: `scripts/generator_agent.py`

```bash
# 分离输入
python scripts/generator_agent.py --layout layout.json --styles styles.json --spec spec.json --output diagram.drawio

# 或合并输入
python scripts/generator_agent.py --all-in-one combined.json --output diagram.drawio
```

**输出**: 完整的 .drawio XML 文件

### Phase 5: 验证修正 (Validator Agent)

**工具**: `scripts/validate_drawio.py`

```bash
python scripts/validate_drawio.py diagram.drawio
```

**迭代策略** (最多 3 轮):
- 结构错误 → 重新生成 (Phase 4)
- 布局问题 (重叠/间距) → 调整布局 (Phase 2)
- 覆盖不全 → 重新规划 (Phase 1)

---

## 简化模式

对于简单图表，可跳过工具直接生成 XML：

1. **分析需求** → 确定图表类型、节点数量、连接关系
2. **规划布局** → 先规划节点位置，预判连线路径，避免交叉
3. **读取语法规则** → 按需加载 references/ 下对应文件
4. **生成 XML** → 按规则生成完整 XML，遵守硬性规则
5. **验证** → 运行验证脚本检查 XML 格式
6. **保存** → 输出 .drawio 文件

## 数据接口规范

### DiagramSpec (Planner 输出)

```json
{
  "diagram_type": "architecture",
  "title": "微服务架构图",
  "nodes": [
    {"id": "gw", "label": "API Gateway", "type": "gateway"},
    {"id": "db", "label": "MySQL", "type": "database"}
  ],
  "edges": [
    {"id": "e1", "source": "gw", "target": "db", "type": "arrow"}
  ],
  "layout_hint": "vertical",
  "theme": "professional"
}
```

### LayoutResult (Layout Agent 输出)

```json
{
  "nodes": [
    {"id": "gw", "x": 340, "y": 40, "width": 120, "height": 60}
  ],
  "edges": [
    {"id": "e1", "source": "gw", "target": "db",
     "exit_x": 0.5, "exit_y": 1, "entry_x": 0.5, "entry_y": 0,
     "waypoints": []}
  ],
  "canvas": {"width": 800, "height": 600}
}
```

### ElementStyles (Element Agent 输出)

```json
{
  "node_styles": {
    "gw": {"shape": "rounded_rect", "style": "rounded=1;fillColor=#d5e8d4;..."},
    "db": {"shape": "cylinder", "style": "shape=cylinder3;fillColor=#f5f5f5;..."}
  },
  "edge_style": "edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=classic;strokeColor=#666666;"
}
```

---

## 语法规则索引

| 需求 | 读取文件 |
|------|---------|
| 形状、填充、边框、文字样式 | `references/shapes.md` |
| 连线、箭头、锚点、拐点 | `references/edges.md` |
| 容器、泳道、图层、分组、多页 | `references/advanced.md` |
| **布局约束与连线规则** | `references/layout.md` |
| **布局示例与计算** | `references/layout_examples.md` |
| **图标库使用指南** | `references/icons.md` |
| **数据可视化组件** | `references/data_viz.md` |
| **信息图模板** | `references/infographic.md` |
| **配色方案** | `references/color_schemes.md` |
| **🧠 AI/ML 专用资源** | `references/ai_ml_assets.md` |
| **📐 UML 图形（类图/序列图/状态图）** | `references/uml.md` |
| **🔧 DevOps/开源生态** | `references/devops.md` |
| **💼 业务流程（金融/电商/HR）** | `references/business.md` |
| **🌐 网络拓扑** | `references/network.md` |
| **🤖 多 Agent 架构详解** | `docs/agent-architecture.md` |

## XML 基础结构

```xml
<mxGraphModel dx="800" dy="600" grid="1" gridSize="10" page="1" pageWidth="800" pageHeight="600">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- 所有节点和连线作为兄弟元素放在这里 -->
  </root>
</mxGraphModel>
```

**关键**：所有 mxCell 必须是 `<root>` 的直接子元素，不能嵌套！

## 硬性规则

| 规则 | 说明 |
|------|------|
| 不嵌套 mxCell | 所有 mxCell 是 `<root>` 的直接子元素 |
| `as="geometry"` | mxGeometry 必须包含此属性 |
| `id="0"` 和 `id="1"` | 保留 ID，用户内容从 id="2" 开始 |
| `relative="1"` | 连线的 mxGeometry 必须包含此属性 |
| 节点属性 | 必须包含 `vertex="1"` |
| 连线属性 | 必须包含 `edge="1"` |

## 连线规则（核心！）

**每条连线必须显式指定锚点**：

```xml
style="edgeStyle=orthogonalEdgeStyle;exitX=1;exitY=0.5;entryX=0;entryY=0.5;endArrow=classic;"
```

| 方向 | exitX;exitY | entryX;entryY |
|------|-------------|---------------|
| 右→左 | 1;0.5 | 0;0.5 |
| 下→上 | 0.5;1 | 0.5;0 |
| 左→右 | 0;0.5 | 1;0.5 |
| 上→下 | 0.5;0 | 0.5;1 |

**❌ 禁止角落连接**: exitX=1;exitY=1 这种角落点会导致连线不自然

**障碍物避让**：如果连线会穿过其他节点，必须用 waypoints 绕行：

```xml
<mxGeometry relative="1" as="geometry">
  <Array as="points">
    <mxPoint x="300" y="150"/>
  </Array>
</mxGeometry>
```

## 布局约束

- **画布范围**: x ∈ [40, 760], y ∈ [40, 560]
- **节点尺寸**: S(80×40), M(120×60), L(160×80)
- **节点间距**: 至少 120px（留出连线通道）
- **网格对齐**: 所有坐标是 10 的倍数

## 生成前检查

1. ❓ 节点间距够大吗？（至少 120px）
2. ❓ 每条连线会穿过其他节点吗？→ 加 waypoints
3. ❓ 有连线共享路径吗？→ 调整 exitY/entryY
4. ❓ 用了角落连接点吗？→ 改用边缘中点

## 验证

```bash
python scripts/validate_drawio.py <file.drawio>
```

## 高级功能

### 🎨 数据可视化
- **进度条**：水平、垂直、环形进度条
- **KPI 卡片**：带数值、趋势、图标的指标卡
- **图表**：饼图、柱状图、折线图（组合实现）
- **仪表盘**：多指标组合布局

### 📊 信息图
- **步骤流程**：垂直、之字形、网格式步骤展示
- **时间线**：水平、垂直时间轴设计
- **对比布局**：左右对比、优劣分析
- **分类展示**：卡片网格、图标分类

### 🎯 专业图标
- **云服务图标**：AWS、Azure、GCP、Kubernetes
- **业务图标**：用户、设备、网络、安全等
- **自定义图标**：支持 SVG/PNG 图标导入

### 🌈 配色方案
- **企业配色**：蓝灰、商务绿等专业���色
- **AI/ML 主题**：科技感配色方案
- **暗色模式**：深色主题配色
- **渐变效果**：多方向渐变、彩虹色

### 💫 视觉效果
- **阴影效果**：多层次阴影营造深度
- **玻璃态**：透明模糊效果
- **新拟态**：柔和凸凹效果
- **动画提示**：通过颜色变化暗示流程

## 素材检索

使用语义检索从素材库查找相关样式、形状、配色：

```bash
# 构建索引（首次使用）
python scripts/asset_search.py --build

# 语义搜索
python scripts/asset_search.py --query "数据库圆柱形状"
python scripts/asset_search.py --query "蓝色渐变配色" --top 5

# JSON 格式输出（供工具链使用）
python scripts/asset_search.py --query "箭头连线" --json
```

---

## 依赖安装

```bash
# 核心依赖（布局算法）
pip install grandalf

# 可选依赖（素材检索）
pip install sentence-transformers
```

| 依赖 | 用途 | 必需 |
|------|------|------|
| grandalf | Sugiyama 层级布局算法 | 推荐 |
| sentence-transformers | 素材语义检索 | 可选 |

无依赖时自动回退到简单实现。

---

## 参考来源

- [mxGraph API](https://jgraph.github.io/mxgraph/docs/js-api/files/util/mxConstants-js.html)
- [Draw.io 文档](https://www.drawio.com/doc/faq/shape-complex-create-edit)
- [AWS 图标库](https://aws.amazon.com/architecture/icons/)
- [Azure 图标](https://docs.microsoft.com/en-us/azure/architecture/icons/)
- [Kubernetes 图标](https://github.com/kubernetes/community/tree/master/icons)
