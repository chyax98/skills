# 工程图模板库

## 适用场景

- 电路图 (Circuit Diagram)
- 逻辑门图 (Logic Gate Diagram)
- 机架图 (Rack Diagram)
- 网络拓扑图 (Network Topology)
- 平面图 (Floor Plan)
- P&ID 工艺流程图

---

## 一、电路图 (Circuit Diagram)

### 1.1 基本元件

```xml
<!-- 电阻 -->
<mxCell id="resistor" value="R1&#xa;10kΩ"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="60" height="20" as="geometry"/>
</mxCell>

<!-- 电容 -->
<mxCell id="capacitor" value="C1&#xa;100μF"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="150" width="10" height="30" as="geometry"/>
</mxCell>

<!-- 电感 -->
<mxCell id="inductor" value="L1"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;arcSize=50;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="60" height="15" as="geometry"/>
</mxCell>

<!-- 二极管 -->
<mxCell id="diode" value="D1"
        style="triangle;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;direction=east;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="250" width="30" height="20" as="geometry"/>
</mxCell>

<!-- 接地符号 -->
<mxCell id="ground" value=""
        style="triangle;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;direction=south;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="300" width="20" height="15" as="geometry"/>
</mxCell>

<!-- 电源 -->
<mxCell id="vcc" value="VCC&#xa;+5V"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#FF0000;strokeColor=#CC0000;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="50" width="40" height="40" as="geometry"/>
</mxCell>
```

### 1.2 连接点

```xml
<!-- 节点（连接点） -->
<mxCell id="junction" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="250" y="145" width="10" height="10" as="geometry"/>
</mxCell>

<!-- 不连接（跳线） -->
<mxCell id="crossing" style="endArrow=none;jumpStyle=arc;strokeWidth=1;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="200" y="200" as="sourcePoint"/>
    <mxPoint x="300" y="200" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

### 1.3 电路连线

```xml
<!-- 导线 -->
<mxCell id="wire" style="endArrow=none;strokeWidth=2;strokeColor=#000000;"
        edge="1" parent="1" source="resistor" target="capacitor">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 直角导线 -->
<mxCell id="wire_ortho" style="edgeStyle=orthogonalEdgeStyle;endArrow=none;strokeWidth=2;strokeColor=#000000;rounded=0;"
        edge="1" parent="1" source="vcc" target="resistor">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 二、逻辑门图 (Logic Gate)

### 2.1 基本逻辑门

```xml
<!-- AND 门 -->
<mxCell id="and_gate" value="AND"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="60" height="40" as="geometry"/>
</mxCell>

<!-- OR 门 -->
<mxCell id="or_gate" value="OR"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;arcSize=50;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="160" width="60" height="40" as="geometry"/>
</mxCell>

<!-- NOT 门（三角形 + 小圆） -->
<mxCell id="not_gate" value=""
        style="triangle;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;direction=east;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="220" width="40" height="30" as="geometry"/>
</mxCell>

<mxCell id="not_bubble" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="240" y="230" width="10" height="10" as="geometry"/>
</mxCell>

<!-- XOR 门 -->
<mxCell id="xor_gate" value="XOR"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;arcSize=50;double=1;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="280" width="60" height="40" as="geometry"/>
</mxCell>

<!-- NAND 门 -->
<mxCell id="nand_gate" value="NAND"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="60" height="40" as="geometry"/>
</mxCell>

<mxCell id="nand_bubble" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"
        vertex="1" parent="1">
  <mxGeometry x="360" y="115" width="10" height="10" as="geometry"/>
</mxCell>
```

### 2.2 输入输出

```xml
<!-- 输入 -->
<mxCell id="input_a" value="A"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="40" height="20" as="geometry"/>
</mxCell>

<!-- 输出 -->
<mxCell id="output_y" value="Y"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#4CAF50;"
        vertex="1" parent="1">
  <mxGeometry x="400" y="110" width="40" height="20" as="geometry"/>
</mxCell>

<!-- 时钟信号 -->
<mxCell id="clock" value="CLK"
        style="triangle;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#FF9800;direction=east;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="20" height="20" as="geometry"/>
</mxCell>
```

---

## 三、机架图 (Rack Diagram)

### 3.1 机架框架

```xml
<!-- 42U 机架 -->
<mxCell id="rack" value="机架 A-01"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#37474F;strokeColor=#263238;fontColor=#ffffff;verticalAlign=top;align=center;fontSize=14;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="300" height="700" as="geometry"/>
</mxCell>

<!-- U 位标尺 -->
<mxCell id="u_scale" value="42U&#xa;41U&#xa;40U&#xa;...&#xa;2U&#xa;1U"
        style="text;html=1;align=right;verticalAlign=top;fontSize=8;fontColor=#90A4AE;"
        vertex="1" parent="1">
  <mxGeometry x="60" y="80" width="30" height="650" as="geometry"/>
</mxCell>
```

### 3.2 机架设备

```xml
<!-- 1U 服务器 -->
<mxCell id="server_1u" value="Server 01"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#1976D2;strokeColor=#0D47A1;fontColor=#ffffff;fontSize=10;"
        vertex="1" parent="rack">
  <mxGeometry x="10" y="40" width="280" height="15" as="geometry"/>
</mxCell>

<!-- 2U 服务器 -->
<mxCell id="server_2u" value="Database Server"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#388E3C;strokeColor=#1B5E20;fontColor=#ffffff;fontSize=10;"
        vertex="1" parent="rack">
  <mxGeometry x="10" y="60" width="280" height="30" as="geometry"/>
</mxCell>

<!-- 交换机 -->
<mxCell id="switch_rack" value="Switch 48-Port"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FF9800;strokeColor=#F57C00;fontColor=#ffffff;fontSize=10;"
        vertex="1" parent="rack">
  <mxGeometry x="10" y="100" width="280" height="15" as="geometry"/>
</mxCell>

<!-- 存储阵列 (4U) -->
<mxCell id="storage" value="Storage Array&#xa;100TB"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#7B1FA2;strokeColor=#4A148C;fontColor=#ffffff;fontSize=10;"
        vertex="1" parent="rack">
  <mxGeometry x="10" y="120" width="280" height="60" as="geometry"/>
</mxCell>

<!-- 空位 -->
<mxCell id="empty_slot" value=""
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#263238;strokeColor=#37474F;strokeWidth=1;dashed=1;"
        vertex="1" parent="rack">
  <mxGeometry x="10" y="190" width="280" height="15" as="geometry"/>
</mxCell>

<!-- PDU 电源 -->
<mxCell id="pdu" value="PDU"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F44336;strokeColor=#C62828;fontColor=#ffffff;fontSize=10;"
        vertex="1" parent="rack">
  <mxGeometry x="10" y="650" width="280" height="30" as="geometry"/>
</mxCell>
```

### 3.3 设备高度参考

| 高度 | 像素 (建议) |
|------|-------------|
| 1U | 15px |
| 2U | 30px |
| 3U | 45px |
| 4U | 60px |

---

## 四、网络拓扑图

### 4.1 网络设备

```xml
<!-- 核心路由器 -->
<mxCell id="core_router" value="Core Router"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1565C0;strokeColor=#0D47A1;fontColor=#ffffff;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="350" y="50" width="100" height="50" as="geometry"/>
</mxCell>

<!-- 防火墙 -->
<mxCell id="firewall_net" value="Firewall"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F44336;strokeColor=#C62828;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="350" y="130" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 核心交换机 -->
<mxCell id="core_switch" value="Core Switch"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FF9800;strokeColor=#F57C00;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="350" y="200" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 接入交换机 -->
<mxCell id="access_switch" value="Access SW"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFC107;strokeColor=#FFA000;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="280" width="80" height="30" as="geometry"/>
</mxCell>

<!-- 服务器 -->
<mxCell id="server_net" value="Server"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=#388E3C;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="350" width="80" height="60" as="geometry"/>
</mxCell>

<!-- 客户端/工作站 -->
<mxCell id="workstation" value="PC"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ECEFF1;strokeColor=#90A4AE;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="350" width="60" height="40" as="geometry"/>
</mxCell>

<!-- 云/互联网 -->
<mxCell id="cloud" value="Internet"
        style="ellipse;shape=cloud;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;"
        vertex="1" parent="1">
  <mxGeometry x="320" y="0" width="160" height="80" as="geometry"/>
</mxCell>

<!-- 无线AP -->
<mxCell id="ap" value="AP"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#9C27B0;strokeColor=#7B1FA2;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="280" width="50" height="50" as="geometry"/>
</mxCell>
```

### 4.2 网络区域

```xml
<!-- DMZ 区域 -->
<mxCell id="dmz" value="DMZ"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#F44336;strokeWidth=2;dashed=1;verticalAlign=top;align=left;spacingLeft=10;"
        vertex="1" parent="1">
  <mxGeometry x="450" y="180" width="200" height="150" as="geometry"/>
</mxCell>

<!-- 内网区域 -->
<mxCell id="internal" value="Internal Network"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#4CAF50;strokeWidth=2;dashed=1;verticalAlign=top;align=left;spacingLeft=10;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="250" width="300" height="200" as="geometry"/>
</mxCell>
```

### 4.3 网络连线

```xml
<!-- 高速链路 -->
<mxCell id="high_speed" value="10Gbps"
        style="endArrow=none;strokeWidth=3;strokeColor=#1976D2;"
        edge="1" parent="1" source="core_router" target="core_switch">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 普通链路 -->
<mxCell id="normal_link" value="1Gbps"
        style="endArrow=none;strokeWidth=2;strokeColor=#4CAF50;"
        edge="1" parent="1" source="core_switch" target="access_switch">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 冗余链路 -->
<mxCell id="redundant" style="endArrow=none;strokeWidth=2;dashed=1;strokeColor=#FF9800;"
        edge="1" parent="1" source="switch_a" target="switch_b">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 五、平面图 (Floor Plan)

### 5.1 墙体和门窗

```xml
<!-- 外墙 -->
<mxCell id="outer_wall" value=""
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;strokeWidth=4;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="500" height="400" as="geometry"/>
</mxCell>

<!-- 内墙 -->
<mxCell id="inner_wall" style="endArrow=none;strokeWidth=2;strokeColor=#000000;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="250" y="50" as="sourcePoint"/>
    <mxPoint x="250" y="300" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 门 -->
<mxCell id="door" value=""
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1;"
        vertex="1" parent="1">
  <mxGeometry x="240" y="300" width="20" height="5" as="geometry"/>
</mxCell>

<!-- 门弧线 -->
<mxCell id="door_arc" style="curved=1;endArrow=none;strokeColor=#999999;"
        edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="260" y="300" as="sourcePoint"/>
    <mxPoint x="260" y="260" as="targetPoint"/>
    <Array as="points">
      <mxPoint x="290" y="280"/>
    </Array>
  </mxGeometry>
</mxCell>

<!-- 窗户 -->
<mxCell id="window" value=""
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;strokeWidth=2;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="50" width="60" height="5" as="geometry"/>
</mxCell>
```

### 5.2 家具/设备

```xml
<!-- 桌子 -->
<mxCell id="desk" value="办公桌"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#8D6E63;strokeColor=#5D4037;fontColor=#ffffff;fontSize=10;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="40" as="geometry"/>
</mxCell>

<!-- 椅子 -->
<mxCell id="chair" value=""
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#BCAAA4;strokeColor=#8D6E63;"
        vertex="1" parent="1">
  <mxGeometry x="125" y="150" width="30" height="30" as="geometry"/>
</mxCell>

<!-- 服务器机柜 -->
<mxCell id="server_cabinet" value="机柜"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#37474F;strokeColor=#263238;fontColor=#ffffff;fontSize=10;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="40" height="60" as="geometry"/>
</mxCell>
```

### 5.3 房间标注

```xml
<!-- 房间名称 -->
<mxCell id="room_name" value="会议室 A"
        style="text;html=1;align=center;verticalAlign=middle;fontSize=14;fontStyle=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="100" height="30" as="geometry"/>
</mxCell>

<!-- 面积标注 -->
<mxCell id="area" value="25m²"
        style="text;html=1;align=center;verticalAlign=middle;fontSize=10;fontColor=#666666;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="230" width="100" height="20" as="geometry"/>
</mxCell>
```

---

## 六、工程图配色总结

| 类型 | 元素 | fillColor | strokeColor |
|------|------|-----------|-------------|
| **电路** | 元件 | #ffffff | #000000 |
| **逻辑门** | 门 | #ffffff | #000000 |
| **机架** | 框架 | #37474F | #263238 |
| **机架** | 服务器 | #1976D2 | #0D47A1 |
| **机架** | 交换机 | #FF9800 | #F57C00 |
| **机架** | 存储 | #7B1FA2 | #4A148C |
| **网络** | 路由器 | #1565C0 | #0D47A1 |
| **网络** | 防火墙 | #F44336 | #C62828 |
| **网络** | 交换机 | #FF9800 | #F57C00 |
| **平面图** | 墙体 | none | #000000 |
| **平面图** | 窗户 | #E3F2FD | #1976D2 |
