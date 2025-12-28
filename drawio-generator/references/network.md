# 网络拓扑素材库

网络设备、安全组件、连接类型的图标和样式。

启用内置库：More Shapes → Networking → Cisco / Network

## 核心网络设备

### 路由器

```xml
<!-- 标准路由器 -->
<mxCell value="Router"
        style="shape=mxgraph.cisco.routers.router;html=1;pointerEvents=1;dashed=0;fillColor=#036897;strokeColor=#ffffff;strokeWidth=2;verticalLabelPosition=bottom;verticalAlign=top;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="78" height="53" as="geometry"/>
</mxCell>

<!-- 简化版路由器（圆形+箭头） -->
<mxCell value="🌐 Router"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#00ACC1;strokeColor=#00838F;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 核心路由器 -->
<mxCell value="Core Router"
        style="shape=mxgraph.cisco.routers.atm_router;html=1;fillColor=#29B6F6;strokeColor=#0277BD;"
        vertex="1" .../>
```

### 交换机

```xml
<!-- 二层交换机 -->
<mxCell value="L2 Switch"
        style="shape=mxgraph.cisco.switches.workgroup_switch;html=1;fillColor=#29B6F6;strokeColor=#01579B;verticalLabelPosition=bottom;verticalAlign=top;"
        vertex="1" .../>

<!-- 三层交换机 -->
<mxCell value="L3 Switch"
        style="shape=mxgraph.cisco.switches.multilayer_switch;html=1;fillColor=#26A69A;strokeColor=#00695C;verticalLabelPosition=bottom;verticalAlign=top;"
        vertex="1" .../>

<!-- 简化版交换机 -->
<mxCell value="Switch"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#29B6F6;strokeColor=#0277BD;fontColor=#FFFFFF;"
        vertex="1" .../>
```

### 防火墙

```xml
<!-- Cisco 风格防火墙 -->
<mxCell value="Firewall"
        style="shape=mxgraph.cisco.security.firewall;html=1;fillColor=#EF5350;strokeColor=#B71C1C;verticalLabelPosition=bottom;verticalAlign=top;"
        vertex="1" .../>

<!-- 简化版防火墙 -->
<mxCell value="🔥 Firewall"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#EF5350;strokeColor=#C62828;fontColor=#FFFFFF;arcSize=10;"
        vertex="1" .../>

<!-- 下一代防火墙 -->
<mxCell value="NGFW"
        style="shape=mxgraph.cisco.security.asa_5500;html=1;fillColor=#FF7043;strokeColor=#D84315;"
        vertex="1" .../>
```

### 负载均衡器

```xml
<!-- 负载均衡器 -->
<mxCell value="Load Balancer"
        style="shape=mxgraph.cisco.misc.load_balancer;html=1;fillColor=#AB47BC;strokeColor=#6A1B9A;verticalLabelPosition=bottom;verticalAlign=top;"
        vertex="1" .../>

<!-- 简化版 -->
<mxCell value="⚖️ LB"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#AB47BC;strokeColor=#6A1B9A;fontColor=#FFFFFF;"
        vertex="1" .../>
```

---

## 服务器与存储

### 服务器

```xml
<!-- 物理服务器 -->
<mxCell value="Server"
        style="shape=mxgraph.cisco.servers.standard_host;html=1;fillColor=#5C6BC0;strokeColor=#283593;verticalLabelPosition=bottom;verticalAlign=top;"
        vertex="1" .../>

<!-- 机架服务器 -->
<mxCell value="Rack Server"
        style="shape=mxgraph.cisco.servers.ucs_express;html=1;fillColor=#42A5F5;strokeColor=#1565C0;"
        vertex="1" .../>

<!-- 虚拟服务器 -->
<mxCell value="VM"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#90CAF9;strokeColor=#1976D2;fontColor=#333333;dashed=1;"
        vertex="1" .../>

<!-- 服务器集群 -->
<mxCell value="Server Cluster"
        style="shape=mxgraph.cisco.servers.generic_appliance;html=1;fillColor=#78909C;strokeColor=#455A64;"
        vertex="1" .../>
```

### 存储

```xml
<!-- 网络存储 (NAS) -->
<mxCell value="NAS"
        style="shape=mxgraph.cisco.storage.network_attached_storage;html=1;fillColor=#8D6E63;strokeColor=#4E342E;verticalLabelPosition=bottom;verticalAlign=top;"
        vertex="1" .../>

<!-- SAN 存储 -->
<mxCell value="SAN"
        style="shape=mxgraph.cisco.storage.storage;html=1;fillColor=#A1887F;strokeColor=#5D4037;"
        vertex="1" .../>

<!-- 磁盘阵列 -->
<mxCell value="RAID"
        style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#BCAAA4;strokeColor=#6D4C41;fontColor=#333333;"
        vertex="1" .../>
```

---

## 安全设备

### 入侵检测/防御

```xml
<!-- IDS/IPS -->
<mxCell value="IDS/IPS"
        style="shape=mxgraph.cisco.security.ids_ips;html=1;fillColor=#FF8A65;strokeColor=#E64A19;verticalLabelPosition=bottom;verticalAlign=top;"
        vertex="1" .../>

<!-- WAF -->
<mxCell value="WAF"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFAB91;strokeColor=#E64A19;fontColor=#333333;"
        vertex="1" .../>
```

### VPN

```xml
<!-- VPN 网关 -->
<mxCell value="VPN Gateway"
        style="shape=mxgraph.cisco.security.vpn_gateway;html=1;fillColor=#4DB6AC;strokeColor=#00695C;"
        vertex="1" .../>

<!-- VPN 隧道（虚线） -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;dashed=1;dashPattern=8 8;strokeWidth=2;strokeColor=#00897B;endArrow=none;"
        edge="1" .../>
```

### 认证

```xml
<!-- AAA 服务器 -->
<mxCell value="AAA"
        style="shape=mxgraph.cisco.security.aaa_server;html=1;fillColor=#7986CB;strokeColor=#303F9F;"
        vertex="1" .../>

<!-- 证书服务器 -->
<mxCell value="🔐 CA"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9575CD;strokeColor=#512DA8;fontColor=#FFFFFF;"
        vertex="1" .../>
```

---

## 网络连接类型

### 物理连接

```xml
<!-- 以太网（实线） -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#1976D2;endArrow=none;"
        edge="1" .../>

<!-- 光纤（粗实线） -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4;strokeColor=#FF9800;endArrow=none;"
        edge="1" .../>

<!-- 串行连接 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#607D8B;endArrow=none;dashed=1;dashPattern=2 2;"
        edge="1" .../>
```

### 逻辑连接

```xml
<!-- VLAN Trunk -->
<mxCell value="Trunk"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=3;strokeColor=#4CAF50;endArrow=none;"
        edge="1" .../>

<!-- 链路聚合 (LAG) -->
<mxCell value="LAG"
        style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=4;strokeColor=#2196F3;endArrow=none;startArrow=none;"
        edge="1" .../>

<!-- BGP/OSPF 路由 -->
<mxCell value="BGP"
        style="edgeStyle=orthogonalEdgeStyle;curved=1;html=1;strokeWidth=2;strokeColor=#9C27B0;dashed=1;endArrow=classic;"
        edge="1" .../>
```

### 无线连接

```xml
<!-- WiFi -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeWidth=2;strokeColor=#00BCD4;dashed=1;dashPattern=4 4;endArrow=none;"
        edge="1" .../>

<!-- 无线接入点 -->
<mxCell value="📶 AP"
        style="shape=mxgraph.cisco.wireless.wireless_access_point;html=1;fillColor=#00ACC1;strokeColor=#00838F;"
        vertex="1" .../>
```

---

## 网络区域

### 安全区域

```xml
<!-- DMZ -->
<mxCell value="DMZ"
        style="swimlane;horizontal=1;startSize=30;fillColor=#FFECB3;strokeColor=#FF8F00;strokeWidth=2;dashed=1;"
        vertex="1" .../>

<!-- 内网 -->
<mxCell value="Internal Network"
        style="swimlane;horizontal=1;startSize=30;fillColor=#C8E6C9;strokeColor=#43A047;strokeWidth=2;"
        vertex="1" .../>

<!-- 外网 -->
<mxCell value="Internet / External"
        style="swimlane;horizontal=1;startSize=30;fillColor=#FFCDD2;strokeColor=#E53935;strokeWidth=2;"
        vertex="1" .../>
```

### 云/虚拟化

```xml
<!-- 云区域 -->
<mxCell value="☁️ Cloud"
        style="ellipse;shape=cloud;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;"
        vertex="1" .../>

<!-- VPC/虚拟网络 -->
<mxCell value="VPC"
        style="swimlane;horizontal=1;startSize=30;fillColor=#E8EAF6;strokeColor=#3F51B5;strokeWidth=2;dashed=1;"
        vertex="1" .../>

<!-- 子网 -->
<mxCell value="Subnet 10.0.1.0/24"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#C5CAE9;strokeColor=#3F51B5;dashed=1;"
        vertex="1" .../>
```

---

## 终端设备

### 用户设备

```xml
<!-- 台式电脑 -->
<mxCell value="PC"
        style="shape=mxgraph.cisco.computers_and_peripherals.pc;html=1;fillColor=#90A4AE;strokeColor=#546E7A;verticalLabelPosition=bottom;verticalAlign=top;"
        vertex="1" .../>

<!-- 笔记本 -->
<mxCell value="💻 Laptop"
        style="shape=mxgraph.cisco.computers_and_peripherals.laptop;html=1;fillColor=#78909C;strokeColor=#455A64;"
        vertex="1" .../>

<!-- 手机 -->
<mxCell value="📱 Mobile"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#546E7A;strokeColor=#37474F;fontColor=#FFFFFF;arcSize=30;"
        vertex="1" .../>

<!-- 打印机 -->
<mxCell value="🖨️ Printer"
        style="shape=mxgraph.cisco.computers_and_peripherals.printer;html=1;fillColor=#BDBDBD;strokeColor=#757575;"
        vertex="1" .../>
```

### IoT 设备

```xml
<!-- 传感器 -->
<mxCell value="📡 Sensor"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#4DB6AC;strokeColor=#00897B;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- 摄像头 -->
<mxCell value="📷 Camera"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#78909C;strokeColor=#455A64;fontColor=#FFFFFF;"
        vertex="1" .../>
```

---

## 网络拓扑模板

### 三层架构

```
[Internet Cloud]
      ↓
[Edge Router] ← 边界层
      ↓
[Firewall]
      ↓
[Core Switch] ← 核心层
   ↙    ↘
[Dist SW] [Dist SW] ← 汇聚层
  ↓   ↓     ↓   ↓
[Access SW] [Access SW] ← 接入层
  ↓   ↓       ↓   ↓
[PCs...]   [Servers...]
```

### 数据中心网络

```
[Spine Switch] [Spine Switch]  ← Spine 层
    ↓     ↘   ↙     ↓
[Leaf SW] [Leaf SW] [Leaf SW]  ← Leaf 层
    ↓         ↓         ↓
 [Rack 1]  [Rack 2]  [Rack 3]  ← 服务器机架
```

### 混合云架构

```
[On-Premise DC] ←─ VPN ─→ [AWS VPC]
       ↓                       ↓
  [Core Network]          [Transit GW]
       ↓                       ↓
  [DMZ] [Internal]    [Public] [Private]
```

---

## 配色方案

### Cisco 风格

```
路由器:   #036897
交换机:   #29B6F6
防火墙:   #EF5350
服务器:   #5C6BC0
存储:     #8D6E63
无线:     #00ACC1
安全:     #FF8A65
```

### 现代扁平风格

```
网络设备: #1976D2 (蓝色)
安全设备: #E53935 (红色)
服务器:   #5C6BC0 (靛蓝)
存储:     #795548 (棕色)
云服务:   #00BCD4 (青色)
用户设备: #78909C (蓝灰)
```

### 区域颜色

```
Internet:  #FFCDD2 (粉红 - 不可信)
DMZ:       #FFF9C4 (黄色 - 半信任)
Internal:  #C8E6C9 (绿色 - 可信)
Management: #E1BEE7 (紫色 - 管理)
```
