# AI/ML 流程图专用资源库

## 概述

本文档提供 AI/ML 流程图中常用的视觉元素，包括模型图标、数据流符号、装饰性元素等。

---

## 1. 模型卡片样式

### 1.1 Frozen 模型卡片（带雪花图标）

```xml
<!-- Frozen 模型 - 深蓝渐变 + 内嵌雪花 -->
<mxCell id="frozen_model" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1565C0;gradientColor=#0D47A1;gradientDirection=south;strokeColor=none;arcSize=25;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="55" as="geometry"/>
</mxCell>
<mxCell id="frozen_text" value="CLIP" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontColor=#FFFFFF;fontSize=14;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="55" as="geometry"/>
</mxCell>
<mxCell id="frozen_icon" value="❄" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontColor=#FFFFFF;fontSize=16;" vertex="1" parent="1">
  <mxGeometry x="195" y="100" width="30" height="55" as="geometry"/>
</mxCell>
```

### 1.2 Trainable 模型卡片（带火焰图标）

```xml
<!-- Trainable 模型 - 橙红渐变 + 火焰 -->
<mxCell id="trainable_model" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF5722;gradientColor=#E64A19;gradientDirection=south;strokeColor=none;arcSize=25;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="140" height="55" as="geometry"/>
</mxCell>
<mxCell id="trainable_text" value="GPT" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontColor=#FFFFFF;fontSize=14;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="100" height="55" as="geometry"/>
</mxCell>
<mxCell id="trainable_icon" value="🔥" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontColor=#FFFFFF;fontSize=16;" vertex="1" parent="1">
  <mxGeometry x="195" y="200" width="30" height="55" as="geometry"/>
</mxCell>
```

### 1.3 预设模型颜色方案

| 模型类型 | fillColor | gradientColor | 图标 |
|---------|-----------|---------------|------|
| Frozen | #1565C0 | #0D47A1 | ❄ |
| Trainable | #FF5722 | #E64A19 | 🔥 |
| Pretrained | #7B1FA2 | #4A148C | 🎓 |
| Fine-tuned | #00897B | #004D40 | 🎯 |
| Ensemble | #5D4037 | #3E2723 | 🔀 |

---

## 2. 数据/输出卡片样式

### 2.1 标准输出卡片

```xml
<!-- 橙色输出卡片 -->
<mxCell id="output_card" value="Semantic Label" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF7043;gradientColor=#E64A19;gradientDirection=south;strokeColor=none;fontColor=#FFFFFF;fontSize=13;fontStyle=1;arcSize=25;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="150" height="50" as="geometry"/>
</mxCell>
```

### 2.2 带图标的数据卡片

```xml
<!-- Semantic Score 带柱状图图标 -->
<mxCell id="score_card" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF7043;gradientColor=#E64A19;gradientDirection=south;strokeColor=none;arcSize=25;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="50" as="geometry"/>
</mxCell>
<mxCell id="score_text" value="Semantic Score" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontColor=#FFFFFF;fontSize=12;fontStyle=1;spacingLeft=10;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="50" as="geometry"/>
</mxCell>
<!-- 柱状图图标组合 -->
<mxCell id="bar1" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=none;opacity=80;" vertex="1" parent="1">
  <mxGeometry x="225" y="130" width="6" height="12" as="geometry"/>
</mxCell>
<mxCell id="bar2" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=none;opacity=80;" vertex="1" parent="1">
  <mxGeometry x="233" y="125" width="6" height="17" as="geometry"/>
</mxCell>
<mxCell id="bar3" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=none;opacity=80;" vertex="1" parent="1">
  <mxGeometry x="241" y="118" width="6" height="24" as="geometry"/>
</mxCell>
```

### 2.3 预设数据卡片颜色

| 数据类型 | fillColor | gradientColor |
|---------|-----------|---------------|
| 标准输出 | #FF7043 | #E64A19 |
| 高置信度 | #26A69A | #00897B |
| 低置信度 | #FFCA28 | #F9A825 |
| 错误/异常 | #EF5350 | #C62828 |
| 中间结果 | #AB47BC | #7B1FA2 |

---

## 3. 处理图标

### 3.1 漏斗图标（用于 one-hot、筛选等）

```xml
<!-- 漏斗 - 使用三角形组合 -->
<mxCell id="funnel_top" value="" style="shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fixedSize=1;fillColor=#EEEEEE;strokeColor=#666666;strokeWidth=2;size=15;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="50" height="25" as="geometry"/>
</mxCell>
<mxCell id="funnel_bottom" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#EEEEEE;strokeColor=#666666;strokeWidth=2;" vertex="1" parent="1">
  <mxGeometry x="117" y="125" width="16" height="20" as="geometry"/>
</mxCell>
<mxCell id="funnel_label" value="one-hot" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;fontColor=#666666;fontSize=11;" vertex="1" parent="1">
  <mxGeometry x="95" y="148" width="60" height="20" as="geometry"/>
</mxCell>
```

### 3.2 Multi-frame 图标（叠加文档）

```xml
<!-- 多帧叠加效果 -->
<mxCell id="frame3" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0E0E0;strokeColor=#9E9E9E;strokeWidth=1;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="108" y="100" width="40" height="50" as="geometry"/>
</mxCell>
<mxCell id="frame2" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EEEEEE;strokeColor=#9E9E9E;strokeWidth=1;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="104" y="105" width="40" height="50" as="geometry"/>
</mxCell>
<mxCell id="frame1" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#9E9E9E;strokeWidth=1;arcSize=10;" vertex="1" parent="1">
  <mxGeometry x="100" y="110" width="40" height="50" as="geometry"/>
</mxCell>
<!-- 播放三角形 -->
<mxCell id="play_icon" value="" style="shape=triangle;direction=east;fillColor=#666666;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="112" y="125" width="15" height="20" as="geometry"/>
</mxCell>
<mxCell id="multi_label" value="multi-frame voting" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;fontColor=#666666;fontSize=10;" vertex="1" parent="1">
  <mxGeometry x="85" y="165" width="90" height="20" as="geometry"/>
</mxCell>
```

### 3.3 神经网络图标

```xml
<!-- 简化的神经网络图标 -->
<mxCell id="nn_input1" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="15" height="15" as="geometry"/>
</mxCell>
<mxCell id="nn_input2" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="100" y="120" width="15" height="15" as="geometry"/>
</mxCell>
<mxCell id="nn_input3" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="100" y="140" width="15" height="15" as="geometry"/>
</mxCell>
<mxCell id="nn_hidden1" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#9C27B0;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="135" y="110" width="15" height="15" as="geometry"/>
</mxCell>
<mxCell id="nn_hidden2" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#9C27B0;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="135" y="130" width="15" height="15" as="geometry"/>
</mxCell>
<mxCell id="nn_output" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="170" y="120" width="15" height="15" as="geometry"/>
</mxCell>
<!-- 连接线需单独添加 -->
```

### 3.4 齿轮/处理图标

```xml
<!-- 齿轮图标 -->
<mxCell id="gear" value="" style="shape=mxgraph.signs.tech.gear;html=1;pointerEvents=1;fillColor=#666666;strokeColor=none;verticalLabelPosition=bottom;verticalAlign=top;align=center;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="40" height="40" as="geometry"/>
</mxCell>
```

---

## 4. 状态指示器

### 4.1 进度/置信度条

```xml
<!-- 水平进度条 -->
<mxCell id="progress_bg" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0E0E0;strokeColor=none;arcSize=50;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="10" as="geometry"/>
</mxCell>
<mxCell id="progress_fill" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=none;arcSize=50;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="75" height="10" as="geometry"/>
</mxCell>
<mxCell id="progress_label" value="75%" style="text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;fontColor=#666666;fontSize=10;" vertex="1" parent="1">
  <mxGeometry x="205" y="95" width="30" height="20" as="geometry"/>
</mxCell>
```

### 4.2 状态徽章

```xml
<!-- 成功徽章 -->
<mxCell id="badge_success" value="✓" style="ellipse;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=none;fontColor=#FFFFFF;fontSize=12;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="24" height="24" as="geometry"/>
</mxCell>

<!-- 警告徽章 -->
<mxCell id="badge_warning" value="!" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FF9800;strokeColor=none;fontColor=#FFFFFF;fontSize=12;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="130" y="100" width="24" height="24" as="geometry"/>
</mxCell>

<!-- 错误徽章 -->
<mxCell id="badge_error" value="✕" style="ellipse;whiteSpace=wrap;html=1;fillColor=#F44336;strokeColor=none;fontColor=#FFFFFF;fontSize=12;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="160" y="100" width="24" height="24" as="geometry"/>
</mxCell>
```

---

## 5. 连接线样式

### 5.1 数据流箭头

```xml
<!-- 标准数据流 - 青蓝色 -->
<mxCell id="dataflow" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;strokeColor=#00BCD4;strokeWidth=2;endArrow=classic;endFill=1;" edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 反向传播 - 红色虚线 -->
<mxCell id="backprop" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;strokeColor=#F44336;strokeWidth=2;dashed=1;dashPattern=8 4;endArrow=classic;endFill=1;" edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 可选路径 - 灰色虚线 -->
<mxCell id="optional" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;strokeColor=#9E9E9E;strokeWidth=1;dashed=1;endArrow=classic;endFill=0;" edge="1" parent="1" source="a" target="b">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 5.2 分支连接

```xml
<!-- 从一个节点分出多条线 -->
<!-- 上分支 exitY=0.3 -->
<mxCell id="branch_up" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#00BCD4;strokeWidth=2;endArrow=classic;exitX=1;exitY=0.3;entryX=0;entryY=0.5;" edge="1" parent="1" source="main" target="branch1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
<!-- 下分支 exitY=0.7 -->
<mxCell id="branch_down" style="edgeStyle=orthogonalEdgeStyle;rounded=1;strokeColor=#00BCD4;strokeWidth=2;endArrow=classic;exitX=1;exitY=0.7;entryX=0;entryY=0.5;" edge="1" parent="1" source="main" target="branch2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 6. 装饰性元素

### 6.1 分组框/容器

```xml
<!-- 虚线分组框 -->
<mxCell id="group_box" value="Feature Extraction" style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#9E9E9E;strokeWidth=2;dashed=1;dashPattern=8 8;verticalAlign=top;fontColor=#666666;fontSize=12;fontStyle=1;spacingTop=5;" vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="300" height="200" as="geometry"/>
</mxCell>
```

### 6.2 标题栏

```xml
<!-- 带颜色条的标题 -->
<mxCell id="title_bar" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1565C0;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="5" as="geometry"/>
</mxCell>
<mxCell id="title_text" value="Stage 1: Preprocessing" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontColor=#333333;fontSize=14;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="110" width="200" height="25" as="geometry"/>
</mxCell>
```

### 6.3 注释/标签

```xml
<!-- 浮动注释 -->
<mxCell id="annotation" value="Loss: 0.023" style="shape=callout;whiteSpace=wrap;html=1;perimeter=calloutPerimeter;fillColor=#FFF9C4;strokeColor=#F9A825;fontSize=11;position2=0.5;size=10;position=0.5;base=20;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="40" as="geometry"/>
</mxCell>
```

---

## 7. 常用 Unicode 图标

在 value 中直接使用：

| 图标 | 代码 | 用途 |
|------|------|------|
| ❄ | `&#10052;` | Frozen 模型 |
| 🔥 | `&#128293;` | Trainable |
| ⚡ | `&#9889;` | 快速/GPU |
| 🎯 | `&#127919;` | 目标/精确 |
| 📊 | `&#128202;` | 图表/统计 |
| 🔄 | `&#128260;` | 循环/迭代 |
| ✓ | `&#10003;` | 完成 |
| ✕ | `&#10005;` | 错误 |
| ⚙ | `&#9881;` | 设置/处理 |
| 📥 | `&#128229;` | 输入 |
| 📤 | `&#128228;` | 输出 |
| 🧠 | `&#129504;` | AI/大脑 |
| 🔗 | `&#128279;` | 链接 |
| ➡ | `&#10145;` | 箭头 |
| ⬇ | `&#11015;` | 下箭头 |

---

## 8. 完整示例：AI Pipeline 卡片

```xml
<!-- 完整的 AI 模型卡片示例 -->
<!-- 背景卡片 -->
<mxCell id="card_bg" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1565C0;gradientColor=#0D47A1;gradientDirection=south;strokeColor=none;arcSize=20;shadow=1;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="60" as="geometry"/>
</mxCell>
<!-- 模型名称 -->
<mxCell id="card_name" value="GroundingDINO" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontColor=#FFFFFF;fontSize=13;fontStyle=1;spacingLeft=12;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="130" height="60" as="geometry"/>
</mxCell>
<!-- Frozen 图标 -->
<mxCell id="card_icon" value="❄" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontColor=#FFFFFF;fontSize=18;" vertex="1" parent="1">
  <mxGeometry x="220" y="100" width="30" height="60" as="geometry"/>
</mxCell>
```

---

## 9. AI/ML 专用图标（mxGraph 扩展）

部分 DrawIO 版本支持的扩展图标：

```xml
<!-- 神经网络节点 -->
<mxCell id="nn_node" value="" style="shape=mxgraph.cisco.misc.asr_1000_series_content_services_gateway;fillColor=#1565C0;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="50" height="50" as="geometry"/>
</mxCell>

<!-- 数据立方体 -->
<mxCell id="data_cube" value="Data" style="shape=cube;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;darkOpacity=0.05;darkOpacity2=0.1;fillColor=#E3F2FD;strokeColor=#1565C0;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="60" height="60" as="geometry"/>
</mxCell>

<!-- 流程箭头形状 -->
<mxCell id="flow_arrow" value="" style="shape=flexArrow;endArrow=classic;startArrow=none;html=1;fillColor=#00BCD4;strokeColor=none;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="30" as="geometry"/>
</mxCell>
```

---

## 10. 颜色快速参考

### AI/ML 语义颜色

| 语义 | 主色 | 渐变色 | 用途 |
|------|------|--------|------|
| 模型蓝 | #1565C0 | #0D47A1 | Frozen 模型、预训练 |
| 输出橙 | #FF7043 | #E64A19 | 输出、结果、预测 |
| 分布青 | #26A69A | #00897B | 概率分布、置信度 |
| 处理紫 | #7B1FA2 | #4A148C | 处理、转换 |
| 数据绿 | #43A047 | #2E7D32 | 数据、GT |
| 损失红 | #E53935 | #C62828 | 损失、错误 |
| 连线青 | #00BCD4 | - | 数据流箭头 |
| 文字灰 | #424242 | - | 标签文字 |
