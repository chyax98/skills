# UML 模板库

## 适用场景

- 类图 (Class Diagram)
- 时序图 (Sequence Diagram)
- 用例图 (Use Case Diagram)
- 活动图 (Activity Diagram)
- 状态图 (State Machine Diagram)
- 组件图 (Component Diagram)
- 部署图 (Deployment Diagram)

---

## 一、类图 (Class Diagram)

### 1.1 类节点

```xml
<!-- 标准类（三栏式） -->
<mxCell id="class_user" value="User&#xa;──────────────&#xa;-id: Long&#xa;-name: String&#xa;-email: String&#xa;──────────────&#xa;+getId(): Long&#xa;+setName(name)&#xa;+save(): void"
        style="whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=5;spacingTop=5;fontFamily=Courier New;fontSize=11;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="150" as="geometry"/>
</mxCell>

<!-- 简化类（单栏） -->
<mxCell id="class_simple" value="&lt;b&gt;UserService&lt;/b&gt;"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="120" height="50" as="geometry"/>
</mxCell>

<!-- 接口 -->
<mxCell id="interface_repo" value="&lt;&lt;interface&gt;&gt;&#xa;Repository&#xa;──────────────&#xa;+save(entity)&#xa;+findById(id)&#xa;+delete(id)"
        style="whiteSpace=wrap;html=1;align=left;verticalAlign=top;fontFamily=Courier New;fontSize=11;fontStyle=2;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="300" width="160" height="120" as="geometry"/>
</mxCell>

<!-- 抽象类 -->
<mxCell id="abstract_class" value="&lt;i&gt;AbstractEntity&lt;/i&gt;&#xa;──────────────&#xa;#id: Long&#xa;──────────────&#xa;+getId(): Long"
        style="whiteSpace=wrap;html=1;align=left;verticalAlign=top;fontFamily=Courier New;fontSize=11;fontStyle=2;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="300" width="160" height="100" as="geometry"/>
</mxCell>
```

### 1.2 类关系连线

```xml
<!-- 继承（实线 + 空心三角） -->
<mxCell id="extends" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=0;strokeWidth=2;"
        edge="1" parent="1" source="child_class" target="parent_class">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 实现（虚线 + 空心三角） -->
<mxCell id="implements" style="edgeStyle=orthogonalEdgeStyle;endArrow=block;endFill=0;dashed=1;strokeWidth=2;"
        edge="1" parent="1" source="impl_class" target="interface">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 组合（实线 + 实心菱形） - 强关联，生命周期一致 -->
<mxCell id="composition" style="edgeStyle=orthogonalEdgeStyle;endArrow=diamond;endFill=1;strokeWidth=2;"
        edge="1" parent="1" source="part" target="whole">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 聚合（实线 + 空心菱形） - 弱关联，可独立存在 -->
<mxCell id="aggregation" style="edgeStyle=orthogonalEdgeStyle;endArrow=diamond;endFill=0;strokeWidth=2;"
        edge="1" parent="1" source="member" target="container">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 关联（实线 + 箭头） -->
<mxCell id="association" style="edgeStyle=orthogonalEdgeStyle;endArrow=open;strokeWidth=2;"
        edge="1" parent="1" source="class_a" target="class_b">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 依赖（虚线 + 箭头） -->
<mxCell id="dependency" style="edgeStyle=orthogonalEdgeStyle;endArrow=open;dashed=1;strokeWidth=1;"
        edge="1" parent="1" source="client" target="supplier">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 1.3 多重性标注

```xml
<!-- 在连线上添加标签 -->
<mxCell id="assoc_label" value="1..*"
        style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;"
        vertex="1" connectable="0" parent="association">
  <mxGeometry x="0.5" relative="1" as="geometry"/>
</mxCell>
```

| 符号 | 含义 |
|------|------|
| 1 | 恰好一个 |
| 0..1 | 零或一个 |
| * | 零或多个 |
| 1..* | 一或多个 |
| n..m | n 到 m 个 |

---

## 二、时序图 (Sequence Diagram)

### 2.1 参与者

```xml
<!-- 用户（Actor） -->
<mxCell id="actor_user" value="用户"
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="40" height="80" as="geometry"/>
</mxCell>

<!-- 对象（矩形） -->
<mxCell id="object_service" value=":OrderService"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="250" y="50" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 生命线（虚线） -->
<mxCell id="lifeline_service"
        style="endArrow=none;dashed=1;dashPattern=3 3;strokeWidth=1;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="300" y="90" as="sourcePoint"/>
    <mxPoint x="300" y="400" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 激活框 -->
<mxCell id="activation" value=""
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="295" y="120" width="10" height="100" as="geometry"/>
</mxCell>
```

### 2.2 消息类型

```xml
<!-- 同步消息（实线 + 实心箭头） -->
<mxCell id="sync_msg" value="createOrder()"
        style="endArrow=block;endFill=1;strokeWidth=1;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="120" y="150" as="sourcePoint"/>
    <mxPoint x="295" y="150" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 异步消息（实线 + 开放箭头） -->
<mxCell id="async_msg" value="notify()"
        style="endArrow=open;strokeWidth=1;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="300" y="200" as="sourcePoint"/>
    <mxPoint x="450" y="200" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 返回消息（虚线 + 开放箭头） -->
<mxCell id="return_msg" value="orderId"
        style="endArrow=open;dashed=1;strokeWidth=1;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="295" y="250" as="sourcePoint"/>
    <mxPoint x="120" y="250" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 自调用 -->
<mxCell id="self_call" value="validate()"
        style="endArrow=block;endFill=1;strokeWidth=1;exitX=1;exitY=0;entryX=1;entryY=1;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="305" y="160" as="sourcePoint"/>
    <mxPoint x="305" y="180" as="targetPoint"/>
    <Array as="points">
      <mxPoint x="340" y="160"/>
      <mxPoint x="340" y="180"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### 2.3 组合片段

```xml
<!-- 循环框 (loop) -->
<mxCell id="loop_frame" value="loop [items.hasNext()]"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#666666;dashed=1;verticalAlign=top;align=left;spacingLeft=5;"
        vertex="1" parent="1">
  <mxGeometry x="80" y="280" width="400" height="100" as="geometry"/>
</mxCell>

<!-- 条件框 (alt) -->
<mxCell id="alt_frame" value="alt [condition]"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#666666;dashed=1;verticalAlign=top;align=left;spacingLeft=5;"
        vertex="1" parent="1">
  <mxGeometry x="80" y="400" width="400" height="150" as="geometry"/>
</mxCell>

<!-- alt 分隔线 -->
<mxCell id="alt_divider"
        style="endArrow=none;dashed=1;strokeColor=#666666;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="80" y="475" as="sourcePoint"/>
    <mxPoint x="480" y="475" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<mxCell id="else_label" value="[else]"
        style="text;html=1;align=left;verticalAlign=middle;"
        vertex="1" parent="1">
  <mxGeometry x="90" y="480" width="50" height="20" as="geometry"/>
</mxCell>
```

---

## 三、用例图 (Use Case Diagram)

### 3.1 元素

```xml
<!-- Actor -->
<mxCell id="actor" value="用户"
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="150" width="40" height="80" as="geometry"/>
</mxCell>

<!-- 用例（椭圆） -->
<mxCell id="usecase" value="登录系统"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="250" y="150" width="140" height="60" as="geometry"/>
</mxCell>

<!-- 系统边界 -->
<mxCell id="system_boundary" value="电商系统"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;verticalAlign=top;align=left;spacingLeft=10;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="50" width="400" height="400" as="geometry"/>
</mxCell>
```

### 3.2 关系

```xml
<!-- 关联（Actor 到 UseCase） -->
<mxCell id="assoc" style="endArrow=none;strokeWidth=1;"
        edge="1" parent="1" source="actor" target="usecase">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 包含 (include) -->
<mxCell id="include" value="&lt;&lt;include&gt;&gt;"
        style="endArrow=open;dashed=1;strokeWidth=1;"
        edge="1" parent="1" source="base_usecase" target="included_usecase">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 扩展 (extend) -->
<mxCell id="extend" value="&lt;&lt;extend&gt;&gt;"
        style="endArrow=open;dashed=1;strokeWidth=1;"
        edge="1" parent="1" source="extension_usecase" target="base_usecase">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 泛化 -->
<mxCell id="generalize" style="endArrow=block;endFill=0;strokeWidth=1;"
        edge="1" parent="1" source="child_actor" target="parent_actor">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 四、状态图 (State Machine Diagram)

### 4.1 状态元素

```xml
<!-- 初始状态（实心圆） -->
<mxCell id="initial" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="20" height="20" as="geometry"/>
</mxCell>

<!-- 最终状态（圆圈 + 实心圆） -->
<mxCell id="final" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;strokeWidth=3;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="100" width="30" height="30" as="geometry"/>
</mxCell>

<!-- 普通状态（圆角矩形） -->
<mxCell id="state_idle" value="Idle"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="90" width="100" height="50" as="geometry"/>
</mxCell>

<!-- 复合状态（包含子状态） -->
<mxCell id="composite_state" value="Processing"
        style="swimlane;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;startSize=25;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="250" height="150" as="geometry"/>
</mxCell>

<!-- 子状态 -->
<mxCell id="sub_state1" value="Validating"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;"
        vertex="1" parent="composite_state">
  <mxGeometry x="20" y="50" width="80" height="40" as="geometry"/>
</mxCell>
```

### 4.2 转换

```xml
<!-- 状态转换 -->
<mxCell id="transition" value="event [guard] / action"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;strokeWidth=1;"
        edge="1" parent="1" source="state_a" target="state_b">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 五、活动图 (Activity Diagram)

### 5.1 节点

```xml
<!-- 初始节点 -->
<mxCell id="initial_node" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="20" height="20" as="geometry"/>
</mxCell>

<!-- 活动终点 -->
<mxCell id="final_node" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#000000;strokeWidth=3;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="500" width="30" height="30" as="geometry"/>
</mxCell>

<!-- 活动节点（圆角矩形） -->
<mxCell id="activity" value="处理订单"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="70" y="100" width="100" height="50" as="geometry"/>
</mxCell>

<!-- 决策节点（菱形） -->
<mxCell id="decision" value=""
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="1">
  <mxGeometry x="95" y="200" width="50" height="50" as="geometry"/>
</mxCell>

<!-- 分叉/汇合节点（粗线） -->
<mxCell id="fork" value=""
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="300" width="150" height="5" as="geometry"/>
</mxCell>
```

---

## 六、组件图 (Component Diagram)

```xml
<!-- 组件 -->
<mxCell id="component" value="&lt;&lt;component&gt;&gt;&#xa;OrderService"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="140" height="80" as="geometry"/>
</mxCell>

<!-- 提供接口（棒棒糖） -->
<mxCell id="provided_interface" value="IOrderAPI"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="150" y="125" width="20" height="20" as="geometry"/>
</mxCell>

<mxCell id="interface_line" style="endArrow=none;strokeWidth=1;"
        edge="1" parent="1" source="provided_interface" target="component">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 需求接口（半圆） -->
<mxCell id="required_interface" value="IPaymentAPI"
        style="curved=1;endArrow=none;html=1;rounded=0;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="340" y="155" as="sourcePoint"/>
    <mxPoint x="380" y="135" as="targetPoint"/>
    <Array as="points">
      <mxPoint x="360" y="145"/>
    </Array>
  </mxGeometry>
</mxCell>
```

---

## 七、部署图 (Deployment Diagram)

```xml
<!-- 节点（3D 盒子效果） -->
<mxCell id="server_node" value="&lt;&lt;device&gt;&gt;&#xa;Web Server"
        style="shape=cube;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;size=10;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="180" height="120" as="geometry"/>
</mxCell>

<!-- 执行环境 -->
<mxCell id="exec_env" value="&lt;&lt;executionEnvironment&gt;&gt;&#xa;Docker Container"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;verticalAlign=top;"
        vertex="1" parent="server_node">
  <mxGeometry x="10" y="40" width="160" height="70" as="geometry"/>
</mxCell>

<!-- 制品 -->
<mxCell id="artifact" value="&lt;&lt;artifact&gt;&gt;&#xa;app.jar"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="exec_env">
  <mxGeometry x="10" y="25" width="80" height="40" as="geometry"/>
</mxCell>

<!-- 通信路径 -->
<mxCell id="comm_path" value="&lt;&lt;HTTPS&gt;&gt;"
        style="endArrow=none;strokeWidth=2;"
        edge="1" parent="1" source="server_node" target="db_node">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 八、UML 配色方案

| 元素类型 | fillColor | strokeColor |
|----------|-----------|-------------|
| 类/组件 | #dae8fc | #6c8ebf |
| 接口 | #ffffff | #000000 |
| 抽象类 | #f5f5f5 | #666666 |
| Actor | #dae8fc | #6c8ebf |
| 用例 | #dae8fc | #6c8ebf |
| 状态 | #dae8fc | #6c8ebf |
| 活动 | #dae8fc | #6c8ebf |
| 初始/终止 | #000000 | #000000 |
| 决策 | #fff2cc | #d6b656 |
| 节点/设备 | #dae8fc | #6c8ebf |
