# DrawIO 信息图模板

## 概述

信息图是数据可视化的高级应用，通过图形化方式传达复杂信息。DrawIO 可以创建各种类型的信息图。

## 步骤流程图

### 垂直步骤流程

```xml
<!-- 步骤容器 -->
<mxCell id="steps_container" value="项目流程"
        style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#f5f5f5;strokeColor=#666666;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="200" height="500" as="geometry"/>
</mxCell>

<!-- 步骤1 -->
<mxCell id="step1" value="1.&lt;br&gt;&lt;b&gt;需求分析&lt;/b&gt;&lt;br&gt;收集用户需求"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=none;fontColor=white;align=center;verticalAlign=middle;spacing=5;"
        vertex="1" parent="steps_container">
  <mxGeometry x="50" y="50" width="100" height="80" as="geometry"/>
</mxCell>

<!-- 连接线1 -->
<mxCell id="arrow1" value=""
        style="edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=1;entryX=0.5;entryY=0;endArrow=classic;strokeColor=#4CAF50;strokeWidth=3;endFill=1;"
        edge="1" parent="steps_container" source="step1" target="step2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 步骤2 -->
<mxCell id="step2" value="2.&lt;br&gt;&lt;b&gt;设计&lt;/b&gt;&lt;br&gt;架构和UI设计"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=none;fontColor=white;align=center;verticalAlign=middle;spacing=5;"
        vertex="1" parent="steps_container">
  <mxGeometry x="50" y="150" width="100" height="80" as="geometry"/>
</mxCell>

<!-- 连接线2 -->
<mxCell id="arrow2" value=""
        style="edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=1;entryX=0.5;entryY=0;endArrow=classic;strokeColor=#2196F3;strokeWidth=3;endFill=1;"
        edge="1" parent="steps_container" source="step2" target="step3">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 步骤3 -->
<mxCell id="step3" value="3.&lt;br&gt;&lt;b&gt;开发&lt;/b&gt;&lt;br&gt;编码实现"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF9800;strokeColor=none;fontColor=white;align=center;verticalAlign=middle;spacing=5;"
        vertex="1" parent="steps_container">
  <mxGeometry x="50" y="250" width="100" height="80" as="geometry"/>
</mxCell>

<!-- 步骤4 -->
<mxCell id="step4" value="4.&lt;br&gt;&lt;b&gt;测试&lt;/b&gt;&lt;br&gt;质量保证"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9C27B0;strokeColor=none;fontColor=white;align=center;verticalAlign=middle;spacing=5;"
        vertex="1" parent="steps_container">
  <mxGeometry x="50" y="350" width="100" height="80" as="geometry"/>
</mxCell>
```

### 之字形步骤流程

```xml
<!-- 之字形布局 -->
<mxCell id="zigzag_container" value="创新流程"
        style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#fafafa;strokeColor=#e0e0e0;"
        vertex="1" parent="1">
  <mxGeometry x="350" y="50" width="600" height="500" as="geometry"/>
</mxCell>

<!-- 步骤1：左上 -->
<mxCell id="zz_step1" value="发现机会"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E91E63;strokeColor=none;fontColor=white;align=center;fontStyle=1;arcSize=50;"
        vertex="1" parent="zigzag_container">
  <mxGeometry x="50" y="50" width="120" height="80" as="geometry"/>
</mxCell>

<!-- 连接线1：右上到左下 -->
<mxCell id="zz_arrow1" value=""
        style="edgeStyle=orthogonalEdgeStyle;exitX=1;exitY=0.5;entryX=0;entryY=0.5;endArrow=classic;strokeColor=#E91E63;strokeWidth=2;endFill=1;curved=1;"
        edge="1" parent="zigzag_container" source="zz_step1" target="zz_step2">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="250" y="90"/>
      <mxPoint x="250" y="180"/>
    </Array>
  </mxGeometry>
</mxCell>

<!-- 步骤2：右上 -->
<mxCell id="zz_step2" value="市场调研"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9C27B0;strokeColor=none;fontColor=white;align=center;fontStyle=1;arcSize=50;"
        vertex="1" parent="zigzag_container">
  <mxGeometry x="430" y="140" width="120" height="80" as="geometry"/>
</mxCell>

<!-- 连接线2 -->
<mxCell id="zz_arrow2" value=""
        style="edgeStyle=orthogonalEdgeStyle;exitX=0;exitY=0.5;entryX=1;entryY=0.5;endArrow=classic;strokeColor=#9C27B0;strokeWidth=2;endFill=1;curved=1;"
        edge="1" parent="zigzag_container" source="zz_step2" target="zz_step3">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="350" y="220"/>
      <mxPoint x="350" y="270"/>
    </Array>
  </mxGeometry>
</mxCell>

<!-- 步骤3：左下 -->
<mxCell id="zz_step3" value="概念设计"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#673AB7;strokeColor=none;fontColor=white;align=center;fontStyle=1;arcSize=50;"
        vertex="1" parent="zigzag_container">
  <mxGeometry x="50" y="230" width="120" height="80" as="geometry"/>
</mxCell>
```

## 时间线设计

### 水平时间线

```xml
<!-- 时间线标题 -->
<mxCell id="timeline_title" value="产品发展历程"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=20;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="800" height="40" as="geometry"/>
</mxCell>

<!-- 时间线主线 -->
<mxCell id="timeline_main" value=""
        style="edgeStyle=orthogonalEdgeStyle;strokeWidth=4;strokeColor=#2196F3;endArrow=none;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="150" y="250" as="sourcePoint"/>
    <mxPoint x="850" y="250" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 2019 -->
<mxCell id="milestone_2019" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=white;strokeWidth=3;fontSize=14;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="225" width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="year_2019" value="2019"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;fontColor=white;"
        vertex="1" parent="1" parent="milestone_2019">
  <mxGeometry width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="event_2019" value="公司成立&lt;br&gt;初始团队 5 人"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#4CAF50;align=center;verticalAlign=middle;"
        vertex="1" parent="1">
  <mxGeometry x="170" y="300" width="110" height="60" as="geometry"/>
</mxCell>

<!-- 连接线2019到事件 -->
<mxCell id="connect_2019" value=""
        style="edgeStyle=orthogonalEdgeStyle;strokeWidth=1;strokeColor=#4CAF50;endArrow=none;"
        edge="1" parent="1" source="milestone_2019" target="event_2019">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 2020 -->
<mxCell id="milestone_2020" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=white;strokeWidth=3;"
        vertex="1" parent="1">
  <mxGeometry x="350" y="225" width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="year_2020" value="2020"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;fontColor=white;"
        vertex="1" parent="1" parent="milestone_2020">
  <mxGeometry width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="event_2020" value="产品 V1 发布&lt;br&gt;获得天使投资"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#2196F3;align=center;verticalAlign=middle;"
        vertex="1" parent="1">
  <mxGeometry x="320" y="150" width="110" height="60" as="geometry"/>
</mxCell>

<!-- 2021 -->
<mxCell id="milestone_2021" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#FF9800;strokeColor=white;strokeWidth=3;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="225" width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="year_2021" value="2021"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;fontColor=white;"
        vertex="1" parent="1" parent="milestone_2021">
  <mxGeometry width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="event_2021" value="用户突破 10 万&lt;br&gt;团队扩张到 50 人"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#FF9800;align=center;verticalAlign=middle;"
        vertex="1" parent="1">
  <mxGeometry x="470" y="300" width="110" height="60" as="geometry"/>
</mxCell>

<!-- 2022 -->
<mxCell id="milestone_2022" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#9C27B0;strokeColor=white;strokeWidth=3;"
        vertex="1" parent="1">
  <mxGeometry x="650" y="225" width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="year_2022" value="2022"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;fontColor=white;"
        vertex="1" parent="1" parent="milestone_2022">
  <mxGeometry width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="event_2022" value="国际化扩张&lt;br&gt;进入 5 个新市场"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F3E5F5;strokeColor=#9C27B0;align=center;verticalAlign=middle;"
        vertex="1" parent="1">
  <mxGeometry x="620" y="150" width="110" height="60" as="geometry"/>
</mxCell>
```

### 垂直时间线

```xml
<!-- 垂直时间线容器 -->
<mxCell id="vertical_timeline" value="项目里程碑"
        style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#f5f5f5;strokeColor=#bdbdbd;horizontal=0;"
        vertex="1" parent="1">
  <mxGeometry x="1000" y="50" width="300" height="600" as="geometry"/>
</mxCell>

<!-- 时间线中心线 -->
<mxCell id="v_timeline" value=""
        style="edgeStyle=orthogonalEdgeStyle;strokeWidth=4;strokeColor=#FF5722;endArrow=none;"
        edge="1" parent="vertical_timeline">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="150" y="100" as="sourcePoint"/>
    <mxPoint x="150" y="550" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- Q1 -->
<mxCell id="q1_marker" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#FF5722;strokeColor=white;strokeWidth=3;"
        vertex="1" parent="vertical_timeline">
  <mxGeometry x="125" y="120" width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="q1_label" value="Q1"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;fontColor=white;"
        vertex="1" parent="vertical_timeline" parent="q1_marker">
  <mxGeometry width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="q1_content" value="&lt;b&gt;启动阶段&lt;/b&gt;&lt;br&gt;• 团队组建&lt;br&gt;• 需求调研&lt;br&gt;• 原型设计"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FBE9E7;strokeColor=#FF5722;align=left;verticalAlign=top;spacingLeft=10;"
        vertex="1" parent="vertical_timeline">
  <mxGeometry x="190" y="110" width="100" height="70" as="geometry"/>
</mxCell>

<!-- Q2 -->
<mxCell id="q2_marker" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=white;strokeWidth=3;"
        vertex="1" parent="vertical_timeline">
  <mxGeometry x="125" y="230" width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="q2_label" value="Q2"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;fontColor=white;"
        vertex="1" parent="vertical_timeline" parent="q2_marker">
  <mxGeometry width="50" height="50" as="geometry"/>
</mxCell>

<mxCell id="q2_content" value="&lt;b&gt;开发阶段&lt;/b&gt;&lt;br&gt;• 前端开发&lt;br&gt;• 后端开发&lt;br&gt;• 接口对接"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#4CAF50;align=left;verticalAlign=top;spacingLeft=10;"
        vertex="1" parent="vertical_timeline">
  <mxGeometry x="30" y="220" width="100" height="70" as="geometry"/>
</mxCell>
```

## 对比布局

### 左右对比

```xml
<!-- 对比容器 -->
<mxCell id="compare_container" value="方案对比"
        style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#f8f9fa;strokeColor=#dee2e6;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="650" width="900" height="400" as="geometry"/>
</mxCell>

<!-- VS 分隔线 -->
<mxCell id="vs_divider" value="VS"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#FF5722;strokeColor=white;fontColor=white;fontSize=20;fontStyle=1;arcSize=50;"
        vertex="1" parent="compare_container">
  <mxGeometry x="400" y="180" width="100" height="100" as="geometry"/>
</mxCell>

<!-- 左侧方案A -->
<mxCell id="plan_a" value="方案 A"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#2196F3;fontSize=16;fontStyle=1;align=center;"
        vertex="1" parent="compare_container">
  <mxGeometry x="50" y="60" width="300" height="40" as="geometry"/>
</mxCell>

<!-- 特点列表A -->
<mxCell id="feature_a1" value="✓ 快速实施"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;"
        vertex="1" parent="compare_container">
  <mxGeometry x="60" y="120" width="280" height="25" as="geometry"/>
</mxCell>

<mxCell id="feature_a2" value="✓ 成本较低"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;"
        vertex="1" parent="compare_container">
  <mxGeometry x="60" y="150" width="280" height="25" as="geometry"/>
</mxCell>

<mxCell id="feature_a3" value="✗ 可扩展性差"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;color=#F44336;"
        vertex="1" parent="compare_container">
  <mxGeometry x="60" y="180" width="280" height="25" as="geometry"/>
</mxCell>

<!-- 右侧方案B -->
<mxCell id="plan_b" value="方案 B"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#4CAF50;fontSize=16;fontStyle=1;align=center;"
        vertex="1" parent="compare_container">
  <mxGeometry x="550" y="60" width="300" height="40" as="geometry"/>
</mxCell>

<!-- 特点列表B -->
<mxCell id="feature_b1" value="✓ 高度可扩展"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;"
        vertex="1" parent="compare_container">
  <mxGeometry x="560" y="120" width="280" height="25" as="geometry"/>
</mxCell>

<mxCell id="feature_b2" value="✓ 性能优越"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;"
        vertex="1" parent="compare_container">
  <mxGeometry x="560" y="150" width="280" height="25" as="geometry"/>
</mxCell>

<mxCell id="feature_b3" value="✗ 开发周期长"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;color=#F44336;"
        vertex="1" parent="compare_container">
  <mxGeometry x="560" y="180" width="280" height="25" as="geometry"/>
</mxCell>

<!-- 评分部分 -->
<mxCell id="rating_label" value="综合评分"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;fontStyle=1;"
        vertex="1" parent="compare_container">
  <mxGeometry x="50" y="300" width="800" height="30" as="geometry"/>
</mxCell>

<!-- 方案A评分 -->
<mxCell id="score_a_bg" value=""
        style="rounded=1;fillColor=#e0e0e0;strokeColor=none;"
        vertex="1" parent="compare_container">
  <mxGeometry x="100" y="340" width="200" height="30" as="geometry"/>
</mxCell>

<mxCell id="score_a" value=""
        style="rounded=1;fillColor=#2196F3;strokeColor=none;"
        vertex="1" parent="compare_container">
  <mxGeometry x="100" y="340" width="140" height="30" as="geometry"/>
</mxCell>

<mxCell id="score_a_text" value="7.0/10"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;fontColor=white;fontStyle=1;"
        vertex="1" parent="compare_container" parent="score_a">
  <mxGeometry width="200" height="30" as="geometry"/>
</mxCell>

<!-- 方案B评分 -->
<mxCell id="score_b_bg" value=""
        style="rounded=1;fillColor=#e0e0e0;strokeColor=none;"
        vertex="1" parent="compare_container">
  <mxGeometry x="600" y="340" width="200" height="30" as="geometry"/>
</mxCell>

<mxCell id="score_b" value=""
        style="rounded=1;fillColor=#4CAF50;strokeColor=none;"
        vertex="1" parent="compare_container">
  <mxGeometry x="600" y="340" width="170" height="30" as="geometry"/>
</mxCell>

<mxCell id="score_b_text" value="8.5/10"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;fontColor=white;fontStyle=1;"
        vertex="1" parent="compare_container" parent="score_b">
  <mxGeometry width="200" height="30" as="geometry"/>
</mxCell>
```

## 分类展示

### 卡片网格

```xml
<!-- 分类容器 -->
<mxCell id="category_container" value="服务分类"
        style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#f5f5f5;strokeColor=#e0e0e0;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="1100" width="900" height="500" as="geometry"/>
</mxCell>

<!-- 卡片1：基础设施 -->
<mxCell id="card1" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;arcSize=10;"
        vertex="1" parent="category_container">
  <mxGeometry x="50" y="60" width="250" height="180" as="geometry"/>
</mxCell>

<mxCell id="card1_icon" value="⚙"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=40;color=#607D8B;"
        vertex="1" parent="card1">
  <mxGeometry y="20" width="250" height="50" as="geometry"/>
</mxCell>

<mxCell id="card1_title" value="基础设施"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;"
        vertex="1" parent="card1">
  <mxGeometry y="80" width="250" height="25" as="geometry"/>
</mxCell>

<mxCell id="card1_desc" value="• 服务器管理&lt;br&gt;• 网络配置&lt;br&gt;• 存储方案&lt;br&gt;• 容器编排"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;spacingLeft=20;"
        vertex="1" parent="card1">
  <mxGeometry y="110" width="250" height="70" as="geometry"/>
</mxCell>

<!-- 卡片2：数据服务 -->
<mxCell id="card2" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;arcSize=10;"
        vertex="1" parent="category_container">
  <mxGeometry x="325" y="60" width="250" height="180" as="geometry"/>
</mxCell>

<mxCell id="card2_icon" value="📊"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=40;color=#4CAF50;"
        vertex="1" parent="card2">
  <mxGeometry y="20" width="250" height="50" as="geometry"/>
</mxCell>

<mxCell id="card2_title" value="数据服务"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;"
        vertex="1" parent="card2">
  <mxGeometry y="80" width="250" height="25" as="geometry"/>
</mxCell>

<mxCell id="card2_desc" value="• 数据库管理&lt;br&gt;• 数据分析&lt;br&gt;• 报表生成&lt;br&gt;• 数据同步"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;spacingLeft=20;"
        vertex="1" parent="card2">
  <mxGeometry y="110" width="250" height="70" as="geometry"/>
</mxCell>

<!-- 卡片3：应用服务 -->
<mxCell id="card3" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;arcSize=10;"
        vertex="1" parent="category_container">
  <mxGeometry x="600" y="60" width="250" height="180" as="geometry"/>
</mxCell>

<mxCell id="card3_icon" value="🚀"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=40;color=#FF9800;"
        vertex="1" parent="card3">
  <mxGeometry y="20" width="250" height="50" as="geometry"/>
</mxCell>

<mxCell id="card3_title" value="应用服务"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;"
        vertex="1" parent="card3">
  <mxGeometry y="80" width="250" height="25" as="geometry"/>
</mxCell>

<mxCell id="card3_desc" value="• API 网关&lt;br&gt;• 微服务&lt;br&gt;• 函数计算&lt;br&gt;• 消息队列"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;spacingLeft=20;"
        vertex="1" parent="card3">
  <mxGeometry y="110" width="250" height="70" as="geometry"/>
</mxCell>

<!-- 第二行卡片 -->
<!-- 卡片4：安全服务 -->
<mxCell id="card4" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;arcSize=10;"
        vertex="1" parent="category_container">
  <mxGeometry x="50" y="260" width="250" height="180" as="geometry"/>
</mxCell>

<mxCell id="card4_icon" value="🔒"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=40;color=#F44336;"
        vertex="1" parent="card4">
  <mxGeometry y="20" width="250" height="50" as="geometry"/>
</mxCell>

<mxCell id="card4_title" value="安全服务"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=16;fontStyle=1;"
        vertex="1" parent="card4">
  <mxGeometry y="80" width="250" height="25" as="geometry"/>
</mxCell>

<mxCell id="card4_desc" value="• 身份认证&lt;br&gt;• 访问控制&lt;br&gt;• 加密服务&lt;br&gt;• 安全审计"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=14;spacingLeft=20;"
        vertex="1" parent="card4">
  <mxGeometry y="110" width="250" height="70" as="geometry"/>
</mxCell>
```

## 信息图设计技巧

### 1. 使用图标增强视觉效果

```xml
<!-- 使用 Unicode 图标 -->
<mxCell id="check_icon" value="✓"
        style="text;html=1;strokeColor=none;fillColor=none;fontSize=20;fontColor=#4CAF50;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="20" height="20" as="geometry"/>
</mxCell>

<!-- 使用 emoji 图标 -->
<mxCell id="emoji_icon" value="📈"
        style="text;html=1;strokeColor=none;fillColor=none;fontSize=30;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="130" width="30" height="30" as="geometry"/>
</mxCell>
```

### 2. 创建视觉层次

```xml
<!-- 使用不同大小创建层次 -->
<mxCell id="title" value="主标题"
        style="text;html=1;fontSize=24;fontStyle=1;fillColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="200" height="30" as="geometry"/>
</mxCell>

<mxCell id="subtitle" value="副标题"
        style="text;html=1;fontSize=16;fontStyle=2;fillColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="85" width="200" height="25" as="geometry"/>
</mxCell>

<mxCell id="content" value="内容文本"
        style="text;html=1;fontSize=12;fillColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="115" width="200" height="20" as="geometry"/>
</mxCell>
```

### 3. 使用分组和容器

```xml
<!-- 创建信息组 -->
<mxCell id="info_group" value=""
        style="group;collapsible=0;"
        vertex="1" connectable="0" parent="1">
  <mxGeometry x="100" y="200" width="300" height="150" as="geometry"/>
</mxCell>

<!-- 组内元素 -->
<mxCell id="group_title" value="信息组标题"
        style="text;html=1;fontSize=14;fontStyle=1;"
        vertex="1" parent="info_group">
  <mxGeometry width="300" height="25" as="geometry"/>
</mxCell>
```

### 4. 颜色编码

```xml
<!-- 使用颜色表示不同状态或类别 -->
<mxCell id="status_success" value="成功"
        style="rounded=1;fillColor=#C8E6C9;strokeColor=#4CAF50;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="300" width="80" height="30" as="geometry"/>
</mxCell>

<mxCell id="status_warning" value="警告"
        style="rounded=1;fillColor=#FFE0B2;strokeColor=#FF9800;"
        vertex="1" parent="1">
  <mxGeometry x="190" y="300" width="80" height="30" as="geometry"/>
</mxCell>

<mxCell id="status_error" value="错误"
        style="rounded=1;fillColor=#FFCDD2;strokeColor=#F44336;"
        vertex="1" parent="1">
  <mxGeometry x="280" y="300" width="80" height="30" as="geometry"/>
</mxCell>
```

### 5. 数据可视化结合

```xml
<!-- 结合进度条和数据 -->
<mxCell id="data_progress" value="完成度：75%"
        style="text;html=1;fontSize=12;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="350" width="100" height="20" as="geometry"/>
</mxCell>

<mxCell id="progress_bar" value=""
        style="rounded=1;fillColor=#4CAF50;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="350" width="150" height="20" as="geometry"/>
</mxCell>
```

## 最佳实践

1. **保持简洁**：信息图应该传达核心信息，避免过多细节
2. **视觉一致性**：使用统一的颜色方案、字体和图标风格
3. **留白空间**：合理使用空白区域，提高可读性
4. **引导视线**：使用箭头、连线等引导读者视线流向
5. **数据准确**：确保所有数据和比例准确无误
6. **响应式设计**：考虑不同尺寸显示时的效果