# 流程图模板库

## 适用场景

- 泳道流程图（跨部门/角色协作）
- BPMN 业务流程图
- 复杂决策分支流程
- 审批流程、工作流

---

## 一、泳道流程图

### 1.1 水平泳道布局

```xml
<!-- 泳道容器 -->
<mxCell id="lane_user" value="用户"
        style="swimlane;horizontal=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;startSize=30;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="600" height="100" as="geometry"/>
</mxCell>

<mxCell id="lane_system" value="系统"
        style="swimlane;horizontal=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;startSize=30;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="150" width="600" height="100" as="geometry"/>
</mxCell>

<mxCell id="lane_db" value="数据库"
        style="swimlane;horizontal=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;startSize=30;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="250" width="600" height="100" as="geometry"/>
</mxCell>

<!-- 泳道内节点（坐标相对于泳道） -->
<mxCell id="step1" value="发起请求" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="lane_user">
  <mxGeometry x="40" y="35" width="100" height="40" as="geometry"/>
</mxCell>
```

### 1.2 垂直泳道布局

```xml
<mxCell id="vlane1" value="阶段一"
        style="swimlane;horizontal=0;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;startSize=30;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="150" height="400" as="geometry"/>
</mxCell>
```

### 1.3 泳道配色方案

| 角色 | fillColor | strokeColor |
|------|-----------|-------------|
| 用户/客户 | #fff2cc | #d6b656 |
| 系统/服务 | #dae8fc | #6c8ebf |
| 数据库/存储 | #e1d5e7 | #9673a6 |
| 外部系统 | #f5f5f5 | #666666 |
| 审批/管理 | #ffe6cc | #d79b00 |

---

## 二、BPMN 业务流程图

### 2.1 BPMN 事件

```xml
<!-- 开始事件（细边框圆形） -->
<mxCell id="start_event" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;strokeWidth=2;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="40" height="40" as="geometry"/>
</mxCell>

<!-- 结束事件（粗边框圆形） -->
<mxCell id="end_event" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;strokeWidth=4;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="100" width="40" height="40" as="geometry"/>
</mxCell>

<!-- 中间事件（双边框） -->
<mxCell id="intermediate" value=""
        style="ellipse;whiteSpace=wrap;html=1;strokeWidth=2;double=1;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="40" height="40" as="geometry"/>
</mxCell>
```

### 2.2 BPMN 网关

```xml
<!-- 排他网关 (XOR) - 只走一条路 -->
<mxCell id="xor_gateway" value="X"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="90" width="50" height="50" as="geometry"/>
</mxCell>

<!-- 并行网关 (AND) - 所有路都走 -->
<mxCell id="and_gateway" value="+"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="90" width="50" height="50" as="geometry"/>
</mxCell>

<!-- 包含网关 (OR) - 走一条或多条 -->
<mxCell id="or_gateway" value="O"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="400" y="90" width="50" height="50" as="geometry"/>
</mxCell>
```

### 2.3 BPMN 任务类型

```xml
<!-- 用户任务 -->
<mxCell id="user_task" value="审批申请"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>

<!-- 服务任务 -->
<mxCell id="service_task" value="调用API"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="120" height="60" as="geometry"/>
</mxCell>

<!-- 子流程（带边框容器） -->
<mxCell id="subprocess" value="子流程"
        style="swimlane;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;startSize=25;rounded=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="300" width="200" height="150" as="geometry"/>
</mxCell>
```

---

## 三、决策分支流程

### 3.1 二分支决策

```xml
<!-- 决策节点 -->
<mxCell id="decision" value="条件判断?"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="1">
  <mxGeometry x="190" y="150" width="120" height="80" as="geometry"/>
</mxCell>

<!-- 是分支（右出） -->
<mxCell id="yes_edge" value="是"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
        edge="1" parent="1" source="decision" target="yes_node">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 否分支（下出） -->
<mxCell id="no_edge" value="否"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"
        edge="1" parent="1" source="decision" target="no_node">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 3.2 多分支决策

```xml
<!-- 多分支从决策节点的不同方向出 -->
<!-- 上：exitX=0.5;exitY=0 -->
<!-- 右：exitX=1;exitY=0.5 -->
<!-- 下：exitX=0.5;exitY=1 -->
<!-- 左：exitX=0;exitY=0.5 -->

<mxCell id="branch_a" value="选项A"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;exitX=1;exitY=0.5;"
        edge="1" parent="1" source="decision" target="node_a">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<mxCell id="branch_b" value="选项B"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;exitX=0.5;exitY=1;"
        edge="1" parent="1" source="decision" target="node_b">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<mxCell id="branch_c" value="选项C"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;exitX=0;exitY=0.5;"
        edge="1" parent="1" source="decision" target="node_c">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 四、审批流程模板

### 4.1 串行审批

```xml
<!-- 申请 → 部门审批 → 财务审批 → 总经理审批 → 完成 -->
<mxCell id="apply" value="提交申请" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="50" as="geometry"/>
</mxCell>

<mxCell id="dept_approve" value="部门审批" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="250" y="100" width="100" height="50" as="geometry"/>
</mxCell>

<mxCell id="finance_approve" value="财务审批" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="400" y="100" width="100" height="50" as="geometry"/>
</mxCell>

<mxCell id="gm_approve" value="总经理审批" style="whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
  <mxGeometry x="550" y="100" width="100" height="50" as="geometry"/>
</mxCell>

<mxCell id="complete" value="完成" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
  <mxGeometry x="700" y="100" width="100" height="50" as="geometry"/>
</mxCell>
```

### 4.2 并行审批（会签）

```xml
<!-- 使用并行网关分叉和汇合 -->
<mxCell id="fork" value="+"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="125" width="40" height="40" as="geometry"/>
</mxCell>

<mxCell id="join" value="+"
        style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="125" width="40" height="40" as="geometry"/>
</mxCell>

<!-- 并行分支 -->
<mxCell id="approver1" value="审批人A" style="..." vertex="1" parent="1">
  <mxGeometry x="300" y="50" width="100" height="50" as="geometry"/>
</mxCell>

<mxCell id="approver2" value="审批人B" style="..." vertex="1" parent="1">
  <mxGeometry x="300" y="150" width="100" height="50" as="geometry"/>
</mxCell>

<mxCell id="approver3" value="审批人C" style="..." vertex="1" parent="1">
  <mxGeometry x="300" y="250" width="100" height="50" as="geometry"/>
</mxCell>
```

---

## 五、连线路径控制

### 5.1 自定义路径点

```xml
<mxCell id="custom_edge" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
        edge="1" parent="1" source="nodeA" target="nodeB">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="200" y="150"/>
      <mxPoint x="200" y="300"/>
      <mxPoint x="400" y="300"/>
    </Array>
  </mxGeometry>
</mxCell>
```

### 5.2 回路/循环

```xml
<!-- 从下方出，绕回上方入 -->
<mxCell id="loop_edge" value="重试"
        style="edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=classic;exitX=0.5;exitY=1;entryX=0;entryY=0.5;"
        edge="1" parent="1" source="process" target="process">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="160" y="250"/>
      <mxPoint x="50" y="250"/>
      <mxPoint x="50" y="175"/>
    </Array>
  </mxGeometry>
</mxCell>
```

---

## 六、完整示例：订单处理流程

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Claude Code">
  <diagram name="订单处理流程" id="order_flow">
    <mxGraphModel dx="1000" dy="800" grid="1" page="1" pageWidth="1000" pageHeight="800">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- 泳道 -->
        <mxCell id="lane_customer" value="客户"
                style="swimlane;horizontal=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;startSize=30;"
                vertex="1" parent="1">
          <mxGeometry x="50" y="50" width="900" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="lane_system" value="订单系统"
                style="swimlane;horizontal=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;startSize=30;"
                vertex="1" parent="1">
          <mxGeometry x="50" y="150" width="900" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="lane_warehouse" value="仓库"
                style="swimlane;horizontal=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;startSize=30;"
                vertex="1" parent="1">
          <mxGeometry x="50" y="250" width="900" height="100" as="geometry"/>
        </mxCell>

        <!-- 客户层节点 -->
        <mxCell id="place_order" value="下单"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;"
                vertex="1" parent="lane_customer">
          <mxGeometry x="40" y="35" width="80" height="40" as="geometry"/>
        </mxCell>

        <mxCell id="receive" value="收货"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;"
                vertex="1" parent="lane_customer">
          <mxGeometry x="780" y="35" width="80" height="40" as="geometry"/>
        </mxCell>

        <!-- 系统层节点 -->
        <mxCell id="validate" value="验证订单"
                style="whiteSpace=wrap;html=1;fillColor=#ffffff;"
                vertex="1" parent="lane_system">
          <mxGeometry x="150" y="30" width="100" height="50" as="geometry"/>
        </mxCell>

        <mxCell id="check_stock" value="库存?"
                style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
                vertex="1" parent="lane_system">
          <mxGeometry x="300" y="20" width="80" height="60" as="geometry"/>
        </mxCell>

        <mxCell id="confirm" value="确认订单"
                style="whiteSpace=wrap;html=1;fillColor=#ffffff;"
                vertex="1" parent="lane_system">
          <mxGeometry x="430" y="30" width="100" height="50" as="geometry"/>
        </mxCell>

        <mxCell id="notify" value="通知发货"
                style="whiteSpace=wrap;html=1;fillColor=#ffffff;"
                vertex="1" parent="lane_system">
          <mxGeometry x="580" y="30" width="100" height="50" as="geometry"/>
        </mxCell>

        <!-- 仓库层节点 -->
        <mxCell id="pack" value="打包"
                style="whiteSpace=wrap;html=1;fillColor=#ffffff;"
                vertex="1" parent="lane_warehouse">
          <mxGeometry x="580" y="30" width="80" height="50" as="geometry"/>
        </mxCell>

        <mxCell id="ship" value="发货"
                style="whiteSpace=wrap;html=1;fillColor=#ffffff;"
                vertex="1" parent="lane_warehouse">
          <mxGeometry x="700" y="30" width="80" height="50" as="geometry"/>
        </mxCell>

        <!-- 连线 -->
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="place_order" target="validate">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="validate" target="check_stock">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e3" value="有"
                style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="check_stock" target="confirm">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="confirm" target="notify">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="notify" target="pack">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="pack" target="ship">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e7" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="ship" target="receive">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```
