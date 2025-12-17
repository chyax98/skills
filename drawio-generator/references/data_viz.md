# DrawIO 数据可视化组件

## 概述

DrawIO 虽然不是专门的图表工具，但可以通过组合基础形状实现丰富的数据可视化效果。

## 进度条 (Progress Bar)

### 水平进度条

```xml
<!-- 背景条 -->
<mxCell id="progress_bg" value=""
        style="rounded=1;fillColor=#f0f0f0;strokeColor=#cccccc;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="20" as="geometry"/>
</mxCell>

<!-- 进度条 (75%) -->
<mxCell id="progress_bar" value=""
        style="rounded=1;fillColor=#4CAF50;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="150" height="20" as="geometry"/>
</mxCell>

<!-- 百分比标签 -->
<mxCell id="progress_label" value="75%"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="20" as="geometry"/>
</mxCell>
```

### 渐变进度条

```xml
<mxCell id="progress_gradient" value=""
        style="rounded=1;fillColor=#4CAF50;gradientColor=#81C784;strokeColor=none;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="150" width="160" height="20" as="geometry"/>
</mxCell>
```

### 环形进度条

**注意**：DrawIO 不支持真正的弧形进度条。以下是可行的替代方案：

#### 方案1：双圆环叠加（简易）

```xml
<!-- 外圈背景 -->
<mxCell id="ring_bg" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#e0e0e0;strokeWidth=10;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="80" height="80" as="geometry"/>
</mxCell>

<!-- 中心文字 -->
<mxCell id="ring_text" value="&lt;b style=&quot;font-size:18px;color:#2196F3&quot;&gt;60%&lt;/b&gt;"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="80" height="80" as="geometry"/>
</mxCell>
```

#### 方案2：半环形展示（推荐）

```xml
<!-- 左半圆（已完成部分） -->
<mxCell id="half_progress" value=""
        style="shape=partialRectangle;top=0;bottom=0;right=1;fillColor=#2196F3;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="40" height="80" as="geometry"/>
</mxCell>

<!-- 右半圆（未完成部分） -->
<mxCell id="half_remaining" value=""
        style="shape=partialRectangle;top=0;bottom=0;left=1;fillColor=#e0e0e0;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="140" y="200" width="40" height="80" as="geometry"/>
</mxCell>
```

#### 方案3：使用仪表盘数字显示（最佳实践）

```xml
<!-- 圆形背景 -->
<mxCell id="gauge_bg" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#2196F3;strokeWidth=3;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="100" height="100" as="geometry"/>
</mxCell>

<!-- 数值 -->
<mxCell id="gauge_value" value="&lt;span style=&quot;font-size:24px;font-weight:bold;color:#1565C0&quot;&gt;75&lt;/span&gt;&lt;span style=&quot;font-size:12px;color:#666&quot;&gt;%&lt;/span&gt;"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="100" height="100" as="geometry"/>
</mxCell>
```

## KPI 卡片

### 基础 KPI 卡片

```xml
<!-- 卡片背景 -->
<mxCell id="kpi_bg" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="300" width="180" height="100" as="geometry"/>
</mxCell>

<!-- 标题 -->
<mxCell id="kpi_title" value="月度用户增长"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=12;fontColor=#666666;"
        vertex="1" parent="1">
  <mxGeometry x="110" y="310" width="160" height="20" as="geometry"/>
</mxCell>

<!-- 主要数值 -->
<mxCell id="kpi_value" value="+24.5%"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=24;fontStyle=1;fontColor=#4CAF50;"
        vertex="1" parent="1">
  <mxGeometry x="110" y="335" width="160" height="30" as="geometry"/>
</mxCell>

<!-- 趋势箭头 -->
<mxCell id="kpi_trend" value=""
        style="shape=flexArrow;endArrow=classic;endFill=1;strokeColor=#4CAF50;strokeWidth=2;fillColor=none;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="240" y="350" as="sourcePoint"/>
    <mxPoint x="240" y="335" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

### 带图标的 KPI 卡片

```xml
<!-- 图标背景圆 -->
<mxCell id="icon_bg" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="110" y="460" width="40" height="40" as="geometry"/>
</mxCell>

<!-- 简化用户图标 -->
<mxCell id="user_icon" value=""
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;strokeColor=#2196F3;strokeWidth=2;fillColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="120" y="470" width="20" height="20" as="geometry"/>
</mxCell>

<!-- 分隔线 -->
<mxCell id="separator" value=""
        style="endArrow=none;html=1;strokeColor=#e0e0e0;strokeWidth=1;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="160" y="480" as="sourcePoint"/>
    <mxPoint x="260" y="480" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

## 饼图

**注意**：DrawIO 不支持原生饼图形状。可以使用以下替代方案：

### 方案1：使用 mxGraph 的 pie 形状

```xml
<!-- 饼图使用 shape=pie（需要 libs=infographic） -->
<mxCell id="pie_chart" value=""
        style="shape=mxgraph.infographic.shadedRing;dx=0.1;fillColor=#dae8fc;strokeColor=#6c8ebf;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="580" width="120" height="120" as="geometry"/>
</mxCell>
```

### 方案2：使用分段圆环（推荐）

```xml
<!-- 外环背景 -->
<mxCell id="ring_outer" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#e0e0e0;strokeWidth=20;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="580" width="120" height="120" as="geometry"/>
</mxCell>

<!-- 用多个彩色弧线近似表示饼图（需要手动调整） -->
<!-- 实际效果有限，建议使用柱状图或堆叠条形图代替 -->
```

### 方案3：使用柱状图代替（推荐）

由于 DrawIO 不支持真正的饼图，建议使用水平堆叠条形图来展示比例：

```xml
<!-- 堆叠条形图 -->
<mxCell id="stack1" value="40%"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=none;fontColor=white;align=center;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="580" width="120" height="30" as="geometry"/>
</mxCell>

<mxCell id="stack2" value="30%"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=none;fontColor=white;align=center;"
        vertex="1" parent="1">
  <mxGeometry x="220" y="580" width="90" height="30" as="geometry"/>
</mxCell>

<mxCell id="stack3" value="20%"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFC107;strokeColor=none;fontColor=white;align=center;"
        vertex="1" parent="1">
  <mxGeometry x="310" y="580" width="60" height="30" as="geometry"/>
</mxCell>

<mxCell id="stack4" value="10%"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F44336;strokeColor=none;fontColor=white;align=center;"
        vertex="1" parent="1">
  <mxGeometry x="370" y="580" width="30" height="30" as="geometry"/>
</mxCell>
```

### 图例

```xml
<!-- 图例容器 -->
<mxCell id="legend_box" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fafafa;strokeColor=#e0e0e0;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="630" width="300" height="100" as="geometry"/>
</mxCell>

<!-- 图例项1 -->
<mxCell id="legend1_color" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="110" y="645" width="12" height="12" as="geometry"/>
</mxCell>

<mxCell id="legend1_text" value="产品A - 40%"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;"
        vertex="1" parent="1">
  <mxGeometry x="130" y="640" width="100" height="20" as="geometry"/>
</mxCell>

<!-- 图例项2 -->
<mxCell id="legend2_color" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="110" y="670" width="12" height="12" as="geometry"/>
</mxCell>

<mxCell id="legend2_text" value="产品B - 30%"
        style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;"
        vertex="1" parent="1">
  <mxGeometry x="130" y="665" width="100" height="20" as="geometry"/>
</mxCell>
```

## 柱状图

```xml
<!-- Y轴 -->
<mxCell id="y_axis" value=""
        style="endArrow=none;html=1;strokeColor=#333333;strokeWidth=2;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="400" y="800" as="sourcePoint"/>
    <mxPoint x="400" y="650" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- X轴 -->
<mxCell id="x_axis" value=""
        style="endArrow=none;html=1;strokeColor=#333333;strokeWidth=2;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="400" y="800" as="sourcePoint"/>
    <mxPoint x="600" y="800" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 柱子1 -->
<mxCell id="bar1" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="420" y="720" width="40" height="80" as="geometry"/>
</mxCell>

<!-- 柱子2 -->
<mxCell id="bar2" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="480" y="690" width="40" height="110" as="geometry"/>
</mxCell>

<!-- 柱子3 -->
<mxCell id="bar3" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFC107;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="540" y="740" width="40" height="60" as="geometry"/>
</mxCell>

<!-- 数值标签 -->
<mxCell id="bar1_label" value="80"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="420" y="700" width="40" height="20" as="geometry"/>
</mxCell>
```

## 时间线

```xml
<!-- 时间线主线 -->
<mxCell id="timeline" value=""
        style="endArrow=none;html=1;strokeColor=#2196F3;strokeWidth=3;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="100" y="900" as="sourcePoint"/>
    <mxPoint x="700" y="900" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 里程碑1 -->
<mxCell id="milestone1" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="175" y="885" width="30" height="30" as="geometry"/>
</mxCell>

<!-- 里程碑标签 -->
<mxCell id="milestone1_label" value="2024 Q1&lt;br&gt;项目启动"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=top;whiteSpace=wrap;rounded=0;fontSize=12;"
        vertex="1" parent="1">
  <mxGeometry x="150" y="925" width="80" height="40" as="geometry"/>
</mxCell>

<!-- 里程碑2 -->
<mxCell id="milestone2" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="335" y="885" width="30" height="30" as="geometry"/>
</mxCell>

<!-- 里程碑3 -->
<mxCell id="milestone3" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFC107;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="495" y="885" width="30" height="30" as="geometry"/>
</mxCell>

<!-- 里程碑4 -->
<mxCell id="milestone4" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#F44336;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="655" y="885" width="30" height="30" as="geometry"/>
</mxCell>
```

## 仪表盘布局示例

```xml
<!-- 仪表盘容器 -->
<mxCell id="dashboard" value="系统监控仪表盘"
        style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#f8f9fa;strokeColor=#dee2e6;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="900" height="600" as="geometry"/>
</mxCell>

<!-- KPI 卡片1 -->
<mxCell id="kpi_card1" value="CPU 使用率"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;"
        vertex="1" parent="dashboard">
  <mxGeometry x="70" y="70" width="180" height="100" as="geometry"/>
</mxCell>

<!-- KPI 卡片2 -->
<mxCell id="kpi_card2" value="内存使用"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;"
        vertex="1" parent="dashboard">
  <mxGeometry x="270" y="70" width="180" height="100" as="geometry"/>
</mxCell>

<!-- KPI 卡片3 -->
<mxCell id="kpi_card3" value="网络流量"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;"
        vertex="1" parent="dashboard">
  <mxGeometry x="470" y="70" width="180" height="100" as="geometry"/>
</mxCell>

<!-- KPI 卡片4 -->
<mxCell id="kpi_card4" value="磁盘空间"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;"
        vertex="1" parent="dashboard">
  <mxGeometry x="670" y="70" width="180" height="100" as="geometry"/>
</mxCell>

<!-- 图表区域1 -->
<mxCell id="chart_area1" value="性能趋势"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;"
        vertex="1" parent="dashboard">
  <mxGeometry x="70" y="190" width="380" height="250" as="geometry"/>
</mxCell>

<!-- 图表区域2 -->
<mxCell id="chart_area2" value="错误统计"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;"
        vertex="1" parent="dashboard">
  <mxGeometry x="470" y="190" width="380" height="250" as="geometry"/>
</mxCell>

<!-- 日志区域 -->
<mxCell id="log_area" value="系统日志"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;strokeColor=#e0e0e0;shadow=1;"
        vertex="1" parent="dashboard">
  <mxGeometry x="70" y="460" width="780" height="150" as="geometry"/>
</mxCell>
```

## 高级技巧

### 1. 使用渐变

```xml
<style="fillColor=#4CAF50;gradientColor=#81C784;gradientDirection=north;shadow=1;"
```

### 2. 玻璃态效果（近似）

```xml
<style="rounded=1;fillColor=#ffffff;fillOpacity=30;strokeColor=#e0e0e0;strokeWidth=1;shadow=1;"
```

### 3. 分组技巧

将多个形状组合为一个组件时，可以使用 group 样式：

```xml
<mxCell id="chart_group" value=""
        style="group;collapsible=0;container=1;"
        vertex="1" connectable="0" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry"/>
</mxCell>

<!-- 子元素 parent 指向组ID -->
<mxCell id="child1" value="子元素"
        style="rounded=1;whiteSpace=wrap;html=1;"
        vertex="1" parent="chart_group">
  <mxGeometry x="10" y="10" width="100" height="40" as="geometry"/>
</mxCell>
```

## 最佳实践

1. **颜色一致性**：使用统一的配色方案
2. **尺寸规范**：保持相同类型组件的尺寸一致
3. **间距统一**：使用 10/20/40 像素的间距倍数
4. **对齐原则**：使用网格对齐，所有坐标是 10 的倍数
5. **分组逻辑**：相关元素用容器或分组组织