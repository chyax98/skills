---
name: drawio-generator
description: This skill enables generation of professional DrawIO diagrams (.drawio XML format) directly from text descriptions. Claude Code reads the XML specification and generates diagrams without script dependencies. Supports flowcharts, architecture diagrams, UML, ER diagrams, and network topology with full mxGraph XML control.
license: Apache-2.0
---

# DrawIO 图表生成器

根据用户描述直接生成 DrawIO XML 文件（.drawio）。

## 工作流程

1. **分析需求** → 确定图表类型、节点数量、连接关系
2. **规划布局** → 先规划节点位置，预判连线路径，避免交叉
3. **读取语法规则** → 按需加载 references/ 下对应文件
4. **生成 XML** → 按规则生成完整 XML，遵守硬性规则
5. **验证** → 运行验证脚本检查 XML 格式
6. **保存** → 输出 .drawio 文件

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

## 参考来源

- [mxGraph API](https://jgraph.github.io/mxgraph/docs/js-api/files/util/mxConstants-js.html)
- [Draw.io 文档](https://www.drawio.com/doc/faq/shape-complex-create-edit)
- [AWS 图标库](https://aws.amazon.com/architecture/icons/)
- [Azure 图标](https://docs.microsoft.com/en-us/azure/architecture/icons/)
- [Kubernetes 图标](https://github.com/kubernetes/community/tree/master/icons)
