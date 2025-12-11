# DrawIO 配色方案指南

## 概述

合理的配色方案能让图表更专业、更易读。以下是针对不同场景的配色方案。

## 企业商务配色

### 方案1：经典蓝灰

```xml
<!-- 主色：深蓝 -->
<mxCell id="primary" value=""
        style="rounded=1;fillColor=#1565C0;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 次要色：浅蓝 -->
<mxCell id="secondary" value=""
        style="rounded=1;fillColor=#E3F2FD;strokeColor=#1565C0;"
        vertex="1" parent="1">
  <mxGeometry x="220" y="50" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 强调色：橙色 -->
<mxCell id="accent" value=""
        style="rounded=1;fillColor=#FF9800;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="340" y="50" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 中性色：浅灰 -->
<mxCell id="neutral" value=""
        style="rounded=1;fillColor=#F5F5F5;strokeColor=#E0E0E0;"
        vertex="1" parent="1">
  <mxGeometry x="460" y="50" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 成功色：绿色 -->
<mxCell id="success" value=""
        style="rounded=1;fillColor=#4CAF50;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="110" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 警告色：琥珀色 -->
<mxCell id="warning" value=""
        style="rounded=1;fillColor=#FFA726;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="220" y="110" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 错误色：红色 -->
<mxCell id="error" value=""
        style="rounded=1;fillColor=#F44336;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="340" y="110" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 文字色：深灰 -->
<mxCell id="text" value="Text"
        style="text;html=1;strokeColor=none;fillColor=none;fontColor=#424242;fontSize=14;"
        vertex="1" parent="1">
  <mxGeometry x="460" y="115" width="100" height="30" as="geometry"/>
</mxCell>
```

**配色代码参考**：
- 主色：#1565C0 (深蓝)
- 次要色：#E3F2FD (浅蓝背景)
- 强调色：#FF9800 (橙色)
- 成功：#4CAF50 (绿色)
- 警告：#FFA726 (琥珀色)
- 错误：#F44336 (红色)
- 中性：#F5F5F5 (浅灰)
- 边框：#E0E0E0 (中灰)

### 方案2：现代简约

```xml
<!-- 深色主题 -->
<mxCell id="dark_primary" value=""
        style="rounded=1;fillColor=#263238;strokeColor=none;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 渐变效果 -->
<mxCell id="gradient_box" value=""
        style="rounded=1;fillColor=#2196F3;gradientColor=#64B5F6;gradientDirection=east;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="220" y="200" width="100" height="40" as="geometry"/>
</mxCell>
```

## AI/ML 主题配色

### 方案1：科技蓝紫

```xml
<!-- AI 主题容器 -->
<mxCell id="ai_theme" value="AI Pipeline"
        style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#1A237E;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="300" width="600" height="400" as="geometry"/>
</mxCell>

<!-- 数据输入层：深蓝 -->
<mxCell id="data_layer" value="数据层"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#283593;strokeColor=none;fontColor=white;"
        vertex="1" parent="ai_theme">
  <mxGeometry x="50" y="50" width="500" height="60" as="geometry"/>
</mxCell>

<!-- 处理层：紫色渐变 -->
<mxCell id="process_layer" value="处理层"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#4527A0;gradientColor=#7B1FA2;gradientDirection=south;strokeColor=none;fontColor=white;"
        vertex="1" parent="ai_theme">
  <mxGeometry x="50" y="130" width="500" height="60" as="geometry"/>
</mxCell>

<!-- AI模型层：特殊紫色 -->
<mxCell id="ai_model" value="AI 模型"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#6A1B9A;strokeColor=none;fontColor=white;shadow=1;"
        vertex="1" parent="ai_theme">
  <mxGeometry x="50" y="210" width="500" height="60" as="geometry"/>
</mxCell>

<!-- 输出层：靛蓝 -->
<mxCell id="output_layer" value="输出层"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#303F9F;strokeColor=none;fontColor=white;"
        vertex="1" parent="ai_theme">
  <mxGeometry x="50" y="290" width="500" height="60" as="geometry"/>
</mxCell>
```

**AI/ML 配色代码**：
- 背景：#1A237E (深靛蓝)
- 数据层：#283593 (深蓝)
- 处理层：#4527A0 → #7B1FA2 (紫色渐变)
- AI模型：#6A1B9A (神秘紫)
- 输出层：#303F9F (靛蓝)
- 强调：#00BCD4 (青色，用于特殊节点)

### 方案2：数据流配色

```xml
<!-- 数据流配色示例 -->
<mxCell id="data_source" value="数据源"
        style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;fillColor=#00838F;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="750" width="80" height="80" as="geometry"/>
</mxCell>

<!-- ETL过程 -->
<mxCell id="etl_process" value="ETL"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#00695C;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="220" y="760" width="80" height="60" as="geometry"/>
</mxCell>

<!-- 特征工程 -->
<mxCell id="feature_eng" value="特征工程"
        style="shape=process;whiteSpace=wrap;html=1;fillColor=#2E7D32;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="340" y="760" width="80" height="60" as="geometry"/>
</mxCell>

<!-- 模型训练 -->
<mxCell id="model_train" value="训练"
        style="shape=cloud;whiteSpace=wrap;html=1;fillColor=#558B2F;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="460" y="750" width="80" height="80" as="geometry"/>
</mxCell>

<!-- 预测结果 -->
<mxCell id="prediction" value="预测"
        style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fillColor=#F57F17;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="580" y="760" width="80" height="60" as="geometry"/>
</mxCell>
```

## 暗色模式配色

### 方案1：深空黑

```xml
<!-- 暗色模式容器 -->
<mxCell id="dark_mode" value="Dark Mode Dashboard"
        style="swimlane;whiteSpace=wrap;html=1;startSize=30;fillColor=#121212;strokeColor=#333333;fontColor=#FFFFFF;"
        vertex="1" parent="1">
  <mxGeometry x="750" y="50" width="500" height="600" as="geometry"/>
</mxCell>

<!-- 卡片背景 -->
<mxCell id="dark_card" value=""
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E1E1E;strokeColor=#333333;shadow=1;"
        vertex="1" parent="dark_mode">
  <mxGeometry x="50" y="50" width="400" height="100" as="geometry"/>
</mxCell>

<!-- 主要按钮 -->
<mxCell id="dark_button" value="Primary Action"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#3700B3;strokeColor=none;fontColor=white;shadow=1;"
        vertex="1" parent="dark_mode">
  <mxGeometry x="50" y="170" width="150" height="40" as="geometry"/>
</mxCell>

<!-- 次要按钮 -->
<mxCell id="dark_secondary" value="Secondary"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#2D2D2D;strokeColor=#666666;fontColor=white;"
        vertex="1" parent="dark_mode">
  <mxGeometry x="220" y="170" width="150" height="40" as="geometry"/>
</mxCell>

<!-- 强调色：霓虹蓝 -->
<mxCell id="neon_highlight" value="Highlight"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#00BCD4;strokeColor=none;fontColor=#000000;fontStyle=1;shadow=1;"
        vertex="1" parent="dark_mode">
  <mxGeometry x="50" y="230" width="150" height="40" as="geometry"/>
</mxCell>

<!-- 成功状态 -->
<mxCell id="dark_success" value="Success"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#00E676;strokeColor=none;fontColor=#000000;fontStyle=1;"
        vertex="1" parent="dark_mode">
  <mxGeometry x="220" y="230" width="150" height="40" as="geometry"/>
</mxCell>
```

**暗色模式配色代码**：
- 背景：#121212 (深黑)
- 卡片：#1E1E1E (深灰)
- 边框：#333333 (中灰)
- 主色：#3700B3 (深紫)
- 强调：#00BCD4 (霓虹青)
- 成功：#00E676 (霓虹绿)
- 警告：#FFD600 (霓虹黄)
- 错误：#FF5252 (霓虹红)
- 文字：#FFFFFF (白) / #AAAAAA (灰)

## 渐变配色方案

### 方案1：蓝紫渐变

```xml
<!-- 渐变示例 -->
<mxCell id="grad1" value="渐变1"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1E88E5;gradientColor=#7B1FA2;gradientDirection=east;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="900" width="150" height="50" as="geometry"/>
</mxCell>

<!-- 垂直渐变 -->
<mxCell id="grad2" value="渐变2"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#43A047;gradientColor=#FDD835;gradientDirection=south;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="220" y="900" width="150" height="50" as="geometry"/>
</mxCell>

<!-- 径向渐变（近似） -->
<mxCell id="grad3" value="径向效果"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#E91E63;gradientColor=#FFC107;gradientDirection=north;strokeColor=none;fontColor=white;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="390" y="890" width="80" height="70" as="geometry"/>
</mxCell>
```

### 方案2：彩虹渐变

```xml
<!-- 彩虹色卡片 -->
<mxCell id="rainbow1" value="阶段1"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF5252;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="980" width="100" height="40" as="geometry"/>
</mxCell>

<mxCell id="rainbow2" value="阶段2"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF9800;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="170" y="980" width="100" height="40" as="geometry"/>
</mxCell>

<mxCell id="rainbow3" value="阶段3"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFEB3B;strokeColor=none;fontColor=#333333;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="290" y="980" width="100" height="40" as="geometry"/>
</mxCell>

<mxCell id="rainbow4" value="阶段4"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="410" y="980" width="100" height="40" as="geometry"/>
</mxCell>

<mxCell id="rainbow5" value="阶段5"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="530" y="980" width="100" height="40" as="geometry"/>
</mxCell>

<mxCell id="rainbow6" value="阶段6"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9C27B0;strokeColor=none;fontColor=white;"
        vertex="1" parent="1">
  <mxGeometry x="650" y="980" width="100" height="40" as="geometry"/>
</mxCell>
```

## 特殊效果配色

### 玻璃态效果（Glass Morphism）

```xml
<!-- 玻璃态容器 -->
<mxCell id="glass_container" value="Glass Morphism"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=white;fillOpacity=20;strokeColor=white;strokeOpacity=30;strokeWidth=1;shadow=1;fontColor=#333333;"
        vertex="1" parent="1">
  <mxGeometry x="750" y="720" width="300" height="200" as="geometry"/>
</mxCell>

<!-- 毛玻璃卡片 -->
<mxCell id="glass_card" value="模糊背景"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0E0E0;fillOpacity=50;strokeColor=white;strokeOpacity=80;strokeWidth=2;fontColor=#333333;"
        vertex="1" parent="1">
  <mxGeometry x="770" y="760" width="120" height="120" as="geometry"/>
</mxCell>

<!-- 背景模糊层 -->
<mxCell id="glass_bg" value=""
        style="rounded=1;fillColor=#F5F5F5;strokeColor=none;opacity=80;"
        vertex="1" parent="1">
  <mxGeometry x="900" y="760" width="120" height="120" as="geometry"/>
</mxCell>
```

### 新拟态（Neumorphism）

```xml
<!-- 新拟态按钮 -->
<mxCell id="neu_button" value="Neumorphic"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0E0E0;strokeColor=none;shadow=1;fontColor=#333333;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="1080" width="150" height="50" as="geometry"/>
</mxCell>

<!-- 凹陷效果 -->
<mxCell id="neu_inset" value="Inset"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EEEEEE;strokeColor=#CCCCCC;strokeWidth=1;fontColor=#666666;"
        vertex="1" parent="1">
  <mxGeometry x="220" y="1080" width="150" height="50" as="geometry"/>
</mxCell>
```

## 配色应用原则

### 1. 60-30-10 法则

```xml
<!-- 60% 主色（背景） -->
<mxCell id="main_bg" value=""
        style="rounded=1;fillColor=#F5F5F5;strokeColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="1180" width="400" height="200" as="geometry"/>
</mxCell>

<!-- 30% 次要色（内容区） -->
<mxCell id="secondary_bg" value=""
        style="rounded=1;fillColor=white;strokeColor=#E0E0E0;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="70" y="1200" width="360" height="160" as="geometry"/>
</mxCell>

<!-- 10% 强调色（按钮/重点） -->
<mxCell id="accent_element" value="CTA"
        style="rounded=1;fillColor=#2196F3;strokeColor=none;fontColor=white;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="1260" width="100" height="40" as="geometry"/>
</mxCell>
```

### 2. 对比度考虑

```xml
<!-- 深色文字配浅色背景 -->
<mxCell id="high_contrast1" value="High Contrast"
        style="text;html=1;fontColor=#000000;fontSize=16;fillColor=#FFFFFF;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="1200" width="150" height="30" as="geometry"/>
</mxCell>

<!-- 避免低对比度 -->
<mxCell id="low_contrast" value="Low Contrast ❌"
        style="text;html=1;fontColor=#CCCCCC;fontSize=16;fillColor=#FFFFFF;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="1240" width="150" height="30" as="geometry"/>
</mxCell>
```

### 3. 一致性原则

```xml
<!-- 保持同类元素颜色一致 -->
<mxCell id="header_style" value="Header"
        style="text;html=1;fontColor=#1565C0;fontSize=18;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="700" y="1200" width="100" height="30" as="geometry"/>
</mxCell>

<mxCell id="another_header" value="Another Header"
        style="text;html=1;fontColor=#1565C0;fontSize=18;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="700" y="1240" width="150" height="30" as="geometry"/>
</mxCell>
```

## 预设配色方案快速参考

| 方案名称 | 主色 | 辅助色 | 强调色 | 适用场景 |
|---------|------|--------|--------|----------|
| 经典蓝灰 | #1565C0 | #E3F2FD | #FF9800 | 企业文档、技术架构 |
| AI科技 | #1A237E | #4527A0 | #00BCD4 | AI/ML、数据科学 |
| 暗色模式 | #121212 | #1E1E1E | #3700B3 | 仪表盘、监控 |
| 彩虹渐变 | #FF5252 | #FFEB3B | #4CAF50 | 流程阶段、进度 |
| 玻璃态 | white(20%) | #E0E0E0(50%) | #2196F3 | 现代UI、产品展示 |
| 自然绿 | #2E7D32 | #A5D6A7 | #FF6F00 | 环保、可持续发展 |

## 使用建议

1. **保持简单**：不要使用超过 5-6 种颜色
2. **考虑可访问性**：确保对比度满足 WCAG 标准
3. **测试打印效果**：某些配色在黑白打印时可能不清晰
4. **品牌一致**：使用品牌色系
5. **情境适配**：根据受众和使用场景选择合适的配色