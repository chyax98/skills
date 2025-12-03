# 商业图表模板库

## 适用场景

- 组织结构图 (Org Chart)
- 思维导图 (Mind Map)
- 概念图 (Concept Map)
- 甘特图 (Gantt Chart)
- 时间线 (Timeline)
- 鱼骨图 / 因果图 (Ishikawa/Fishbone)
- SWOT 分析
- Kanban 看板

---

## 一、组织结构图 (Org Chart)

### 1.1 标准组织节点

```xml
<!-- 高管层（深色） -->
<mxCell id="ceo" value="张三&#xa;CEO"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1565C0;strokeColor=#0D47A1;fontColor=#ffffff;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="350" y="50" width="100" height="60" as="geometry"/>
</mxCell>

<!-- 管理层（中等色） -->
<mxCell id="cto" value="李四&#xa;CTO"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#42A5F5;strokeColor=#1976D2;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="150" y="150" width="100" height="60" as="geometry"/>
</mxCell>

<!-- 员工层（浅色） -->
<mxCell id="dev1" value="王五&#xa;高级工程师"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#90CAF9;strokeColor=#42A5F5;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="250" width="100" height="60" as="geometry"/>
</mxCell>
```

### 1.2 组织连线

```xml
<!-- 直接汇报（实线） -->
<mxCell id="report_line" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=none;strokeWidth=2;"
        edge="1" parent="1" source="ceo" target="cto">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 虚线汇报（虚线） -->
<mxCell id="dotted_line" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=none;dashed=1;strokeWidth=1;"
        edge="1" parent="1" source="pm" target="dev">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 1.3 部门分组

```xml
<mxCell id="dept_tech" value="技术部"
        style="swimlane;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;startSize=25;rounded=1;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="130" width="250" height="200" as="geometry"/>
</mxCell>
```

---

## 二、思维导图 (Mind Map)

### 2.1 中心节点

```xml
<mxCell id="center" value="核心主题"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#FF9800;strokeColor=#F57C00;fontColor=#ffffff;fontStyle=1;fontSize=16;"
        vertex="1" parent="1">
  <mxGeometry x="350" y="250" width="120" height="80" as="geometry"/>
</mxCell>
```

### 2.2 分支节点

```xml
<!-- 一级分支（较大） -->
<mxCell id="branch1" value="分支一"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=#388E3C;fontColor=#ffffff;fontSize=14;"
        vertex="1" parent="1">
  <mxGeometry x="550" y="150" width="100" height="50" as="geometry"/>
</mxCell>

<!-- 二级分支（中等） -->
<mxCell id="sub_branch1" value="子主题"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#81C784;strokeColor=#4CAF50;fontSize=12;"
        vertex="1" parent="1">
  <mxGeometry x="700" y="120" width="80" height="40" as="geometry"/>
</mxCell>

<!-- 三级分支（较小） -->
<mxCell id="leaf1" value="细节"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#81C784;fontSize=11;"
        vertex="1" parent="1">
  <mxGeometry x="820" y="100" width="60" height="30" as="geometry"/>
</mxCell>
```

### 2.3 思维导图连线

```xml
<!-- 曲线连接 -->
<mxCell id="mind_edge" style="edgeStyle=orthogonalEdgeStyle;curved=1;rounded=1;endArrow=none;strokeWidth=2;strokeColor=#4CAF50;"
        edge="1" parent="1" source="center" target="branch1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 2.4 思维导图配色（按分支）

| 分支 | fillColor | strokeColor |
|------|-----------|-------------|
| 中心 | #FF9800 | #F57C00 |
| 分支1 | #4CAF50 | #388E3C |
| 分支2 | #2196F3 | #1976D2 |
| 分支3 | #9C27B0 | #7B1FA2 |
| 分支4 | #F44336 | #D32F2F |
| 分支5 | #00BCD4 | #0097A7 |

---

## 三、甘特图 (Gantt Chart)

### 3.1 时间轴头部

```xml
<!-- 月份标题 -->
<mxCell id="month_jan" value="1月"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="50" width="120" height="30" as="geometry"/>
</mxCell>

<!-- 周标题 -->
<mxCell id="week1" value="W1"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#BBDEFB;strokeColor=#1976D2;fontSize=10;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="80" width="30" height="20" as="geometry"/>
</mxCell>
```

### 3.2 任务条

```xml
<!-- 任务名称 -->
<mxCell id="task1_name" value="需求分析"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#E0E0E0;align=left;spacingLeft=10;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="110" width="140" height="30" as="geometry"/>
</mxCell>

<!-- 任务进度条 -->
<mxCell id="task1_bar" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=#388E3C;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="115" width="90" height="20" as="geometry"/>
</mxCell>

<!-- 里程碑（菱形） -->
<mxCell id="milestone1" value=""
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#FF9800;strokeColor=#F57C00;"
        vertex="1" parent="1">
  <mxGeometry x="295" y="110" width="20" height="20" as="geometry"/>
</mxCell>
```

### 3.3 任务状态颜色

| 状态 | fillColor | strokeColor |
|------|-----------|-------------|
| 已完成 | #4CAF50 | #388E3C |
| 进行中 | #2196F3 | #1976D2 |
| 待开始 | #BDBDBD | #9E9E9E |
| 延期 | #F44336 | #D32F2F |
| 里程碑 | #FF9800 | #F57C00 |

---

## 四、时间线 (Timeline)

### 4.1 水平时间线

```xml
<!-- 时间轴主线 -->
<mxCell id="timeline_axis" style="endArrow=classic;strokeWidth=3;strokeColor=#1976D2;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="50" y="200" as="sourcePoint"/>
    <mxPoint x="750" y="200" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 时间点标记 -->
<mxCell id="point1" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#1976D2;strokeColor=#0D47A1;"
        vertex="1" parent="1">
  <mxGeometry x="145" y="192" width="16" height="16" as="geometry"/>
</mxCell>

<!-- 时间标签 -->
<mxCell id="date1" value="2024-01"
        style="text;html=1;align=center;verticalAlign=middle;fontSize=10;"
        vertex="1" parent="1">
  <mxGeometry x="120" y="215" width="60" height="20" as="geometry"/>
</mxCell>

<!-- 事件卡片（上方） -->
<mxCell id="event1" value="项目启动"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="120" width="100" height="50" as="geometry"/>
</mxCell>

<!-- 连接线 -->
<mxCell id="connect1" style="endArrow=none;strokeColor=#1976D2;"
        edge="1" parent="1" source="event1" target="point1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 4.2 垂直时间线

```xml
<!-- 垂直轴 -->
<mxCell id="v_timeline" style="endArrow=classic;strokeWidth=3;strokeColor=#1976D2;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="200" y="50" as="sourcePoint"/>
    <mxPoint x="200" y="500" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 左侧事件 -->
<mxCell id="left_event" value="事件A"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#4CAF50;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="80" width="120" height="50" as="geometry"/>
</mxCell>

<!-- 右侧事件 -->
<mxCell id="right_event" value="事件B"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#FF9800;"
        vertex="1" parent="1">
  <mxGeometry x="230" y="160" width="120" height="50" as="geometry"/>
</mxCell>
```

---

## 五、鱼骨图 / 因果图 (Ishikawa)

### 5.1 鱼骨主干

```xml
<!-- 问题（鱼头） -->
<mxCell id="problem" value="问题/效果"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F44336;strokeColor=#D32F2F;fontColor=#ffffff;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="700" y="175" width="100" height="50" as="geometry"/>
</mxCell>

<!-- 主干线 -->
<mxCell id="spine" style="endArrow=classic;strokeWidth=3;strokeColor=#333333;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="100" y="200" as="sourcePoint"/>
    <mxPoint x="700" y="200" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

### 5.2 主因分支（6M）

```xml
<!-- 上方分支：人、机、料 -->
<mxCell id="man" value="人 (Man)"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=#388E3C;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="150" y="50" width="80" height="30" as="geometry"/>
</mxCell>

<mxCell id="man_line" style="endArrow=none;strokeWidth=2;strokeColor=#4CAF50;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="190" y="80" as="sourcePoint"/>
    <mxPoint x="250" y="200" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 下方分支：法、环、测 -->
<mxCell id="method" value="法 (Method)"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=#1976D2;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="150" y="320" width="80" height="30" as="geometry"/>
</mxCell>

<mxCell id="method_line" style="endArrow=none;strokeWidth=2;strokeColor=#2196F3;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="190" y="320" as="sourcePoint"/>
    <mxPoint x="250" y="200" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

### 5.3 次因（小骨）

```xml
<mxCell id="sub_cause1" value="培训不足"
        style="text;html=1;align=left;fontSize=10;"
        vertex="1" parent="1">
  <mxGeometry x="160" y="100" width="60" height="20" as="geometry"/>
</mxCell>

<mxCell id="sub_line1" style="endArrow=none;strokeWidth=1;strokeColor=#4CAF50;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="190" y="110" as="sourcePoint"/>
    <mxPoint x="210" y="130" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

### 5.4 6M 配色

| 类别 | 中文 | fillColor | strokeColor |
|------|------|-----------|-------------|
| Man | 人 | #4CAF50 | #388E3C |
| Machine | 机 | #FF9800 | #F57C00 |
| Material | 料 | #9C27B0 | #7B1FA2 |
| Method | 法 | #2196F3 | #1976D2 |
| Measurement | 测 | #00BCD4 | #0097A7 |
| Environment | 环 | #795548 | #5D4037 |

---

## 六、SWOT 分析

### 6.1 四象限布局

```xml
<!-- 标题 -->
<mxCell id="swot_title" value="SWOT 分析"
        style="text;html=1;align=center;verticalAlign=middle;fontStyle=1;fontSize=18;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="20" width="200" height="30" as="geometry"/>
</mxCell>

<!-- S - 优势 (左上，绿色) -->
<mxCell id="strengths" value="S - 优势&#xa;Strengths"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#4CAF50;verticalAlign=top;align=center;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="70" width="200" height="150" as="geometry"/>
</mxCell>

<!-- W - 劣势 (右上，红色) -->
<mxCell id="weaknesses" value="W - 劣势&#xa;Weaknesses"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFCDD2;strokeColor=#F44336;verticalAlign=top;align=center;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="70" width="200" height="150" as="geometry"/>
</mxCell>

<!-- O - 机会 (左下，蓝色) -->
<mxCell id="opportunities" value="O - 机会&#xa;Opportunities"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#BBDEFB;strokeColor=#2196F3;verticalAlign=top;align=center;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="220" width="200" height="150" as="geometry"/>
</mxCell>

<!-- T - 威胁 (右下，橙色) -->
<mxCell id="threats" value="T - 威胁&#xa;Threats"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFE0B2;strokeColor=#FF9800;verticalAlign=top;align=center;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="220" width="200" height="150" as="geometry"/>
</mxCell>
```

---

## 七、Kanban 看板

### 7.1 列布局

```xml
<!-- 待办列 -->
<mxCell id="col_todo" value="待办 (To Do)"
        style="swimlane;whiteSpace=wrap;html=1;fillColor=#ECEFF1;strokeColor=#90A4AE;startSize=30;horizontal=0;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="200" height="400" as="geometry"/>
</mxCell>

<!-- 进行中列 -->
<mxCell id="col_doing" value="进行中 (Doing)"
        style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#FF9800;startSize=30;horizontal=0;"
        vertex="1" parent="1">
  <mxGeometry x="260" y="50" width="200" height="400" as="geometry"/>
</mxCell>

<!-- 已完成列 -->
<mxCell id="col_done" value="已完成 (Done)"
        style="swimlane;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#4CAF50;startSize=30;horizontal=0;"
        vertex="1" parent="1">
  <mxGeometry x="470" y="50" width="200" height="400" as="geometry"/>
</mxCell>
```

### 7.2 任务卡片

```xml
<!-- 任务卡片 -->
<mxCell id="card1" value="用户登录功能&#xa;───────&#xa;优先级: 高&#xa;负责人: 张三"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#BDBDBD;align=left;verticalAlign=top;spacingLeft=5;spacingTop=5;shadow=1;"
        vertex="1" parent="col_todo">
  <mxGeometry x="10" y="40" width="180" height="80" as="geometry"/>
</mxCell>

<!-- 带标签的卡片 -->
<mxCell id="card_tagged" value="&lt;span style='background:#F44336;color:white;padding:2px 5px;border-radius:3px;font-size:10px'&gt;BUG&lt;/span&gt;&#xa;&#xa;修复登录异常"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#F44336;align=left;verticalAlign=top;spacingLeft=5;spacingTop=5;"
        vertex="1" parent="col_doing">
  <mxGeometry x="10" y="40" width="180" height="70" as="geometry"/>
</mxCell>
```

### 7.3 WIP 限制标识

```xml
<!-- WIP 限制 -->
<mxCell id="wip_limit" value="WIP: 3"
        style="text;html=1;align=right;verticalAlign=middle;fontSize=10;fontColor=#FF9800;"
        vertex="1" parent="1">
  <mxGeometry x="370" y="55" width="80" height="20" as="geometry"/>
</mxCell>
```
