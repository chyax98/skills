---
name: drawio-generator
description: This skill enables generation of professional DrawIO diagrams (.drawio XML format) directly from text descriptions. Claude Code reads the XML specification and generates diagrams without script dependencies. Supports flowcharts, architecture diagrams, UML, ER diagrams, and network topology with full mxGraph XML control.
license: Apache-2.0
---

# DrawIO 图表生成器

## 概述

根据用户描述**直接生成** DrawIO XML 文件。掌握完整的 mxGraph XML 规范，可生成任意复杂度的专业图表。

**核心能力**：
- 直接生成 XML，无脚本依赖
- 完整控制每个元素的位置、样式、连线
- 支持高级特性：容器、泳道、图层、分组
- 生成的文件可在 https://app.diagrams.net 打开编辑

**适用场景**：流程图、架构图、UML、ER图、网络拓扑、组织结构图、思维导图等

**触发短语**：
- "生成 drawio 图表"、"画架构图/流程图/UML图"、"创建 .drawio 文件"

---

## 一、XML 核心语法

### 1.1 文件结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Claude Code">
  <diagram name="图表名称" id="唯一ID">
    <mxGraphModel dx="1200" dy="800" grid="1" page="1" pageWidth="1200" pageHeight="800">
      <root>
        <mxCell id="0"/>                    <!-- 必须：根节点 -->
        <mxCell id="1" parent="0"/>         <!-- 必须：默认图层 -->
        <!-- 在此添加节点和连线 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 1.2 节点 (Vertex)

```xml
<mxCell id="唯一ID" value="显示文本" style="样式字符串" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>
```

### 1.3 连线 (Edge)

```xml
<mxCell id="唯一ID" value="标签" style="edgeStyle=orthogonalEdgeStyle;endArrow=classic;"
        edge="1" parent="1" source="源ID" target="目标ID">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 1.4 关键规则

| 规则 | 说明 |
|------|------|
| `as="geometry"` | **必须存在**，否则导入失败 |
| `id="0"` 和 `id="1"` | **保留 ID**，不可用于其他元素 |
| Style 末尾 | **必须有分号** |
| 颜色格式 | 小写十六进制 `#rrggbb` |
| 文本换行 | 使用 `&#xa;` |
| 特殊字符 | `<` → `&lt;`、`>` → `&gt;`、`&` → `&amp;` |

---

## 二、基础形状

### 2.1 常用形状

| 形状 | Style |
|------|-------|
| 矩形 | `whiteSpace=wrap;html=1;` |
| 圆角矩形 | `rounded=1;whiteSpace=wrap;html=1;` |
| 椭圆 | `ellipse;whiteSpace=wrap;html=1;` |
| 菱形 | `rhombus;whiteSpace=wrap;html=1;` |
| 圆柱(数据库) | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;` |
| 平行四边形 | `shape=parallelogram;whiteSpace=wrap;html=1;` |
| 六边形 | `shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;` |
| 云形 | `ellipse;shape=cloud;whiteSpace=wrap;html=1;` |
| 文档 | `shape=document;whiteSpace=wrap;html=1;boundedLbl=1;` |
| 人物(Actor) | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;` |
| 注释 | `shape=note;whiteSpace=wrap;html=1;` |
| 标注(Callout) | `shape=callout;whiteSpace=wrap;html=1;perimeter=calloutPerimeter;` |

### 2.2 标注形状 (Callout) 参数

Callout 用于添加指向性说明，箭头指向被解释的内容：

```xml
<mxCell style="shape=callout;whiteSpace=wrap;html=1;perimeter=calloutPerimeter;
               base=20;position=0.5;position2=0;size=10;" .../>
```

| 参数 | 说明 | 取值范围 |
|------|------|----------|
| `base` | 箭头底部宽度 | 数值，建议 15-30 |
| `position` | 箭头在底边的水平位置 | 0(左) ~ 1(右)，0.5 为中间 |
| `position2` | 箭头指向方向 | 0=向下, 0.5=水平, 1=向上 |
| `size` | 箭头长度 | 数值，建议 10-30 |

**常用组合**：
```xml
<!-- 箭头向下（指向下方内容） -->
position=0.5;position2=0;

<!-- 箭头向上（指向上方内容） -->
position=0.5;position2=1;

<!-- 箭头向右下（左侧标注指向右边内容） -->
position=0.9;position2=0;

<!-- 箭头向左下（右侧标注指向左边内容） -->
position=0.1;position2=0;
```

### 2.3 标准配色方案

| 语义 | fillColor | strokeColor | 用途 |
|------|-----------|-------------|------|
| 绿色 | #d5e8d4 | #82b366 | 开始、成功、正向 |
| 蓝色 | #dae8fc | #6c8ebf | 处理、过程、一般 |
| 黄色 | #fff2cc | #d6b656 | 决策、警告、判断 |
| 红色 | #f8cecc | #b85450 | 结束、错误、危险 |
| 紫色 | #e1d5e7 | #9673a6 | 数据、存储、外部 |
| 橙色 | #ffe6cc | #d79b00 | 重要、高亮、注意 |
| 灰色 | #f5f5f5 | #666666 | 辅助、背景、禁用 |

---

## 三、连线样式

### 3.1 连线类型

| 类型 | Style |
|------|-------|
| 直角折线 | `edgeStyle=orthogonalEdgeStyle;rounded=0;` |
| 曲线 | `edgeStyle=orthogonalEdgeStyle;curved=1;` |
| 直线 | `edgeStyle=none;` |
| 虚线 | `dashed=1;` |

### 3.2 箭头类型

| 类型 | endArrow/startArrow |
|------|---------------------|
| 经典箭头 | `classic` |
| 实心块 | `block` |
| 开放箭头 | `open` |
| 菱形 | `diamond` |
| 椭圆 | `oval` |
| 无箭头 | `none` |

### 3.3 锚点控制

```xml
<mxCell style="...;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" .../>
```

| 位置 | X | Y |
|------|---|---|
| 左中 | 0 | 0.5 |
| 右中 | 1 | 0.5 |
| 上中 | 0.5 | 0 |
| 下中 | 0.5 | 1 |
| 中心 | 0.5 | 0.5 |

### 3.4 拐点控制

当自动路由不满足需求时，可手动指定连线拐点：

```xml
<mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
        edge="1" parent="1" source="node1" target="node2">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="200"/>  <!-- 第一个拐点 -->
      <mxPoint x="300" y="400"/>  <!-- 第二个拐点 -->
    </Array>
  </mxGeometry>
</mxCell>
```

**要点**：
- `<Array as="points">` 定义拐点序列，连线按顺序经过这些点
- 坐标为画布绝对坐标，不受 source/target 影响
- 适用于需要绕过障碍物或创建特定路径的连线
- 拐点越多，布局越精确，但维护成本也越高

---

## 四、布局结构

### 4.1 容器/分组

```xml
<!-- 容器（可折叠） -->
<mxCell id="container1" value="容器标题"
        style="swimlane;whiteSpace=wrap;html=1;startSize=30;collapsible=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry"/>
</mxCell>

<!-- 子元素：parent 指向容器，坐标相对于容器 -->
<mxCell id="child1" value="子节点" style="..." vertex="1" parent="container1">
  <mxGeometry x="20" y="50" width="100" height="40" as="geometry"/>
</mxCell>
```

### 4.2 泳道

```xml
<mxCell id="lane1" value="用户层"
        style="swimlane;horizontal=1;whiteSpace=wrap;html=1;startSize=30;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="500" height="120" as="geometry"/>
</mxCell>
```

| 属性 | 说明 |
|------|------|
| horizontal=1 | 水平泳道（标题在左） |
| horizontal=0 | 垂直泳道（标题在上） |
| startSize | 标题栏高度/宽度 |

### 4.3 图层

```xml
<!-- 新图层 -->
<mxCell id="layer2" value="背景层" style="locked=1;" parent="0"/>

<!-- 元素放到指定图层 -->
<mxCell id="bg_element" value="背景" style="..." vertex="1" parent="layer2">
  ...
</mxCell>
```

---

## 五、生成流程

### 5.1 标准工作流

```
1. 分析需求 → 2. 选择模板库 → 3. 规划布局 → 4. 生成 XML → 5. 自检验证 → 6. 保存交付
```

### 5.2 详细步骤

**Step 1: 分析需求**
- 识别图表类型（流程图/架构图/UML/ER/...）
- 提取节点和关系
- 确定布局方向（垂直/水平/自由）

**Step 2: 选择模板库**（见第七节索引）
- 简单流程图 → 仅需基础层
- 专业场景 → 加载对应模板库

**Step 3: 规划布局**
- 估算节点数量和层级
- 计算画布大小（pageWidth/pageHeight）
- 规划坐标间距（根据图表复杂度调整，参见 6.2 节）

**Step 4: 生成 XML**
- 按结构模板生成完整 XML
- 确保所有 `as="geometry"` 存在
- 文本正确编码

**Step 5: 自检验证**（见第六节评判标准）

**Step 6: 保存交付**
- 保存为 `.drawio` 文件
- 告知用户可用 `open xxx.drawio` 打开

---

## 六、评判标准

### 6.1 结构正确性（必须通过）

| 检查项 | 说明 |
|--------|------|
| XML 可解析 | 无语法错误 |
| 根节点完整 | 存在 `id="0"` 和 `id="1"` |
| geometry 属性 | 所有 `<mxGeometry>` 包含 `as="geometry"` |
| ID 有效性 | ID 唯一，edge 的 source/target 存在 |
| Style 格式 | 末尾有分号，颜色小写十六进制 |

### 6.2 视觉质量（应当满足）

| 检查项 | 标准 |
|--------|------|
| 节点无重叠 | 任意两节点不相交 |
| 间距合理 | 根据复杂度调整，见下表 |
| 对齐整齐 | 网格对齐或中心线对齐 |
| 连线清晰 | 避免不必要交叉 |
| 配色一致 | 同类节点相同颜色，符合语义 |

**间距参考**（非强制，根据实际内容调整）：

| 图表复杂度 | 节点数 | 垂直间距 | 水平间距 | 画布建议 |
|-----------|--------|---------|---------|---------|
| 简单 | <10 | 60-80px | 120-150px | 800×600 |
| 中等 | 10-30 | 80-120px | 150-200px | 1200×900 |
| 复杂 | >30 | 120-180px | 200-300px | 1600×1200+ |

**原则**：
- 内容越多，间距越大，确保阅读舒适
- 有标注/说明时，为其预留空间
- 边缘留白至少 50-80px

### 6.3 语义正确性（用户验收）

| 检查项 | 说明 |
|--------|------|
| 需求完整 | 所有用户要求的元素都已包含 |
| 逻辑正确 | 节点关系、流程方向正确 |
| 标注清晰 | 关键节点有明确标注 |
| 领域规范 | 符合 UML/BPMN/ER 等领域惯例 |

---

## 七、模板库索引

根据图表类型，按需加载对应模板库：

| 场景 | 模板库 | 何时加载 |
|------|--------|----------|
| **流程图** | `flowchart-templates.md` | 泳道流程、BPMN、复杂决策分支 |
| **架构图** | `architecture-templates.md` | AWS/GCP/Azure、微服务、分层架构、网络拓扑 |
| **UML** | `uml-templates.md` | 类图、时序图、用例图、状态图、活动图 |
| **ER图** | `er-templates.md` | 数据库设计、实体关系 |
| **商业图表** | `business-templates.md` | 组织结构图、思维导图、甘特图、鱼骨图、SWOT |
| **工程图** | `engineering-templates.md` | 电路图、逻辑图、机架图、平面图 |
| **样式预设** | `style-presets.md` | 需要特定配色方案或高级样式效果 |

**加载方式**：读取 `references/{模板库文件名}`

**简单场景无需加载**：基础流程图、简单架构示意图等，本文档已足够。

---

## 八、输出配置

**路径优先级**：
1. 用户指定路径 → 使用用户路径
2. 未指定 → `./drawio-output/`（当前工作目录下，自动创建）

**文件命名**：`{主题}-{类型}-{日期}.drawio`
- 示例：`user-service-architecture-20251203.drawio`

---

## 九、快速示例

### 简单流程图

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Claude Code">
  <diagram name="简单流程" id="flow1">
    <mxGraphModel dx="800" dy="600" grid="1" page="1" pageWidth="800" pageHeight="600">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- 开始 -->
        <mxCell id="start" value="开始"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
                vertex="1" parent="1">
          <mxGeometry x="340" y="50" width="120" height="50" as="geometry"/>
        </mxCell>

        <!-- 处理 -->
        <mxCell id="process" value="处理数据"
                style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
                vertex="1" parent="1">
          <mxGeometry x="340" y="150" width="120" height="50" as="geometry"/>
        </mxCell>

        <!-- 结束 -->
        <mxCell id="end" value="结束"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
                vertex="1" parent="1">
          <mxGeometry x="340" y="250" width="120" height="50" as="geometry"/>
        </mxCell>

        <!-- 连线 -->
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="start" target="process">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="process" target="end">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 参考资源

### references/（模板库）
- `flowchart-templates.md` - 流程图模板（泳道、BPMN、决策）
- `architecture-templates.md` - 架构图模板（云、微服务、网络）
- `uml-templates.md` - UML 模板（类图、时序图、用例图等）
- `er-templates.md` - ER 图模板（数据库设计）
- `business-templates.md` - 商业图表（组织图、思维导图、甘特图）
- `engineering-templates.md` - 工程图（电路、机架、平面图）
- `style-presets.md` - 样式预设库（配色、渐变、阴影）

### assets/（示例文件）
- 可上传到 https://app.diagrams.net 查看
- 复杂示例：`transformer-architecture.drawio`、`microservices-architecture.drawio`、`aws-architecture.drawio`
