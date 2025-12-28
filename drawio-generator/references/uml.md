# UML 图形素材库

DrawIO 内置 UML 库使用指南。启用方式：More Shapes → Software → UML

## 类图 (Class Diagram)

### 类框结构

```xml
<!-- 标准类框：3个分区（类名、属性、方法） -->
<mxCell id="class1" value="&lt;b&gt;ClassName&lt;/b&gt;&lt;hr&gt;- field1: String&lt;br&gt;- field2: int&lt;hr&gt;+ method1()&lt;br&gt;+ method2(param): void"
        style="swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=26;fillColor=#dae8fc;strokeColor=#6c8ebf;collapsible=0;swimlaneFillColor=#ffffff;align=center;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="120" as="geometry"/>
</mxCell>
```

### 类关系

| 关系类型 | 箭头样式 | style 片段 |
|---------|---------|------------|
| 继承 (extends) | 空心三角 | `endArrow=block;endFill=0;` |
| 实现 (implements) | 空心三角+虚线 | `endArrow=block;endFill=0;dashed=1;` |
| 关联 (association) | 普通箭头 | `endArrow=open;` |
| 聚合 (aggregation) | 空心菱形 | `startArrow=diamond;startFill=0;endArrow=open;` |
| 组合 (composition) | 实心菱形 | `startArrow=diamond;startFill=1;endArrow=open;` |
| 依赖 (dependency) | 虚线箭头 | `dashed=1;endArrow=open;` |

### 访问修饰符

| 符号 | 含义 | HTML 表示 |
|------|------|-----------|
| + | public | `+ methodName()` |
| - | private | `- fieldName` |
| # | protected | `# fieldName` |
| ~ | package | `~ fieldName` |

### 接口和抽象类

```xml
<!-- 接口（斜体名称 + <<interface>> 标记） -->
<mxCell value="&lt;i&gt;&amp;lt;&amp;lt;interface&amp;gt;&amp;gt;&lt;/i&gt;&lt;br&gt;&lt;b&gt;Comparable&lt;/b&gt;&lt;hr&gt;+ compareTo(o): int"
        style="swimlane;fontStyle=0;align=center;fillColor=#fff2cc;strokeColor=#d6b656;" .../>

<!-- 抽象类（斜体类名） -->
<mxCell value="&lt;i&gt;AbstractClass&lt;/i&gt;&lt;hr&gt;- field&lt;hr&gt;&lt;i&gt;+ abstractMethod()&lt;/i&gt;"
        style="swimlane;fontStyle=2;align=center;fillColor=#e1d5e7;strokeColor=#9673a6;" .../>
```

---

## 序列图 (Sequence Diagram)

### 参与者 (Lifeline)

```xml
<!-- 参与者头部 -->
<mxCell id="actor1" value=":User"
        style="shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=0;collapsible=0;recursiveResize=0;outlineConnect=0;portConstraint=eastwest;participant=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="40" width="100" height="300" as="geometry"/>
</mxCell>

<!-- 激活框 -->
<mxCell id="activation1" value=""
        style="html=1;points=[];perimeter=orthogonalPerimeter;outlineConnect=0;targetShapes=umlLifeline;portConstraint=eastwest;dashed=0;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="145" y="80" width="10" height="60" as="geometry"/>
</mxCell>
```

### 消息类型

| 消息类型 | style 片段 | 用途 |
|---------|-----------|------|
| 同步调用 | `endArrow=block;endFill=1;` | 同步方法调用 |
| 异步调用 | `endArrow=async;` | 异步消息 |
| 返回消息 | `dashed=1;endArrow=open;` | 返回值 |
| 创建对象 | `endArrow=open;dashed=1;` + 指向头部 | new 操作 |
| 销毁对象 | 在生命线末端加 X | 对象销毁 |
| 自调用 | 弯曲箭头指向自己 | 递归/自调用 |

```xml
<!-- 同步消息 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;html=1;verticalAlign=bottom;endArrow=block;endFill=1;rounded=0;"
        edge="1" source="actor1" target="actor2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 返回消息 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;html=1;verticalAlign=bottom;endArrow=open;dashed=1;rounded=0;"
        edge="1" source="actor2" target="actor1">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 片段框 (Combined Fragment)

```xml
<!-- Alt/Loop/Opt 片段 -->
<mxCell value="alt"
        style="shape=umlFrame;whiteSpace=wrap;html=1;pointerEvents=0;fillColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="80" y="120" width="340" height="160" as="geometry"/>
</mxCell>
```

| 片段类型 | 标签 | 用途 |
|---------|------|------|
| alt | alt [condition] | 条件分支 |
| opt | opt [condition] | 可选执行 |
| loop | loop [condition] | 循环 |
| par | par | 并行执行 |
| critical | critical | 临界区 |
| break | break | 中断 |

---

## 状态图 (State Diagram)

### 状态节点

```xml
<!-- 普通状态 -->
<mxCell value="Idle"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;arcSize=40;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="50" as="geometry"/>
</mxCell>

<!-- 初始状态（实心圆） -->
<mxCell value=""
        style="ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="40" y="115" width="20" height="20" as="geometry"/>
</mxCell>

<!-- 终止状态（圆环+实心圆） -->
<mxCell value=""
        style="ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="115" width="20" height="20" as="geometry"/>
</mxCell>
```

### 复合状态

```xml
<!-- 复合状态（包含子状态） -->
<mxCell value="Processing"
        style="swimlane;horizontal=1;startSize=20;fillColor=#d5e8d4;strokeColor=#82b366;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="80" width="200" height="150" as="geometry"/>
</mxCell>
<!-- 子状态放在复合状态内，parent 指向复合状态 ID -->
```

### 转换

```xml
<!-- 状态转换（带事件/条件/动作） -->
<mxCell value="event [guard] / action"
        style="edgeStyle=orthogonalEdgeStyle;html=1;endArrow=open;rounded=0;"
        edge="1" source="state1" target="state2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 用例图 (Use Case Diagram)

### 元素

```xml
<!-- Actor -->
<mxCell value="User"
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="40" y="100" width="30" height="60" as="geometry"/>
</mxCell>

<!-- 用例（椭圆） -->
<mxCell value="Login"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="1">
  <mxGeometry x="150" y="100" width="100" height="50" as="geometry"/>
</mxCell>

<!-- 系统边界 -->
<mxCell value="System"
        style="shape=umlFrame;whiteSpace=wrap;html=1;pointerEvents=0;"
        vertex="1" parent="1">
  <mxGeometry x="120" y="40" width="300" height="200" as="geometry"/>
</mxCell>
```

### 用例关系

| 关系 | style 片段 | 说明 |
|------|-----------|------|
| 关联 | `endArrow=none;` | Actor 与用例连线 |
| 包含 | `dashed=1;endArrow=open;` + `<<include>>` 标签 | 必须执行 |
| 扩展 | `dashed=1;endArrow=open;` + `<<extend>>` 标签 | 可选执行 |
| 泛化 | `endArrow=block;endFill=0;` | 继承 |

---

## 活动图 (Activity Diagram)

### 节点类型

```xml
<!-- 开始节点 -->
<mxCell style="ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#000000;"
        vertex="1" .../>

<!-- 结束节点 -->
<mxCell style="ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;"
        vertex="1" .../>

<!-- 活动节点 -->
<mxCell value="Process Order"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;arcSize=40;"
        vertex="1" .../>

<!-- 判断节点（菱形） -->
<mxCell value=""
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" .../>

<!-- 分叉/合并条（同步条） -->
<mxCell value=""
        style="line;strokeWidth=4;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;"
        vertex="1" .../>
```

### 泳道

```xml
<!-- 水平泳道 -->
<mxCell value="Department A"
        style="swimlane;horizontal=1;startSize=30;fillColor=#e1d5e7;strokeColor=#9673a6;"
        vertex="1" parent="1">
  <mxGeometry x="0" y="0" width="800" height="200" as="geometry"/>
</mxCell>
```

---

## 组件图 (Component Diagram)

```xml
<!-- 组件 -->
<mxCell value="&lt;b&gt;WebServer&lt;/b&gt;"
        style="shape=component;align=left;spacingLeft=36;rounded=0;shadow=0;comic=0;labelBackgroundColor=none;strokeWidth=1;fontFamily=Verdana;fontSize=12;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>

<!-- 接口（棒棒糖） -->
<mxCell value="IService"
        style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="230" y="115" width="30" height="30" as="geometry"/>
</mxCell>
```

---

## 部署图 (Deployment Diagram)

```xml
<!-- 节点（3D 立方体） -->
<mxCell value="&lt;b&gt;Web Server&lt;/b&gt;&lt;br&gt;&amp;lt;&amp;lt;device&amp;gt;&amp;gt;"
        style="shape=cube;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;darkOpacity=0.05;darkOpacity2=0.1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="140" height="100" as="geometry"/>
</mxCell>

<!-- 制品 -->
<mxCell value="&amp;lt;&amp;lt;artifact&amp;gt;&amp;gt;&lt;br&gt;&lt;b&gt;app.war&lt;/b&gt;"
        style="shape=note;whiteSpace=wrap;html=1;size=14;verticalAlign=top;align=left;spacingTop=-6;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="1">
  <mxGeometry x="280" y="120" width="100" height="60" as="geometry"/>
</mxCell>
```

---

## 配色建议

| UML 图类型 | 推荐配色 | 说明 |
|-----------|---------|------|
| 类图 | 蓝色系 (#dae8fc/#6c8ebf) | 标准、专业 |
| 接口 | 黄色系 (#fff2cc/#d6b656) | 区分于类 |
| 抽象类 | 紫色系 (#e1d5e7/#9673a6) | 区分于具体类 |
| 序列图 | 蓝色系 + 灰色生命线 | 清晰的消息流 |
| 状态图 | 绿色系 (#d5e8d4/#82b366) | 状态转换 |
| 用例 | 黄色系椭圆 | 突出用例 |
| 组件 | 蓝色系立体 | 系统架构 |
