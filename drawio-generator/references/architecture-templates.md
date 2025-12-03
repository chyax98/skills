# 架构图模板库

## 适用场景

- 云架构图（AWS/GCP/Azure/阿里云）
- 微服务架构图
- 分层架构图（三层/N层）
- 网络拓扑图
- 系统部署图
- C4 模型架构图

---

## 一、云架构图

### 1.1 AWS 风格配色

| 服务类型 | fillColor | strokeColor | 图标风格 |
|---------|-----------|-------------|----------|
| 计算 (EC2/Lambda) | #FF9900 | #FF6600 | 橙色 |
| 存储 (S3) | #3F8624 | #2E6B1A | 绿色 |
| 数据库 (RDS/DynamoDB) | #3B48CC | #2A36A3 | 蓝色 |
| 网络 (VPC/ELB) | #8C4FFF | #6B3ACC | 紫色 |
| 安全 (IAM) | #DD344C | #B32940 | 红色 |

### 1.2 VPC 边界

```xml
<!-- VPC 边界框 -->
<mxCell id="vpc" value="VPC (10.0.0.0/16)"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#8C4FFF;strokeWidth=2;dashed=1;dashPattern=5 5;verticalAlign=top;align=left;spacingLeft=10;spacingTop=5;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="700" height="500" as="geometry"/>
</mxCell>

<!-- 公有子网 -->
<mxCell id="public_subnet" value="Public Subnet"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;verticalAlign=top;align=left;spacingLeft=10;"
        vertex="1" parent="vpc">
  <mxGeometry x="20" y="40" width="300" height="200" as="geometry"/>
</mxCell>

<!-- 私有子网 -->
<mxCell id="private_subnet" value="Private Subnet"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#FF9800;verticalAlign=top;align=left;spacingLeft=10;"
        vertex="1" parent="vpc">
  <mxGeometry x="20" y="260" width="300" height="200" as="geometry"/>
</mxCell>
```

### 1.3 云服务节点

```xml
<!-- EC2 实例 -->
<mxCell id="ec2" value="EC2&#xa;Web Server"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF9900;strokeColor=#FF6600;fontColor=#ffffff;shadow=1;"
        vertex="1" parent="public_subnet">
  <mxGeometry x="30" y="50" width="100" height="60" as="geometry"/>
</mxCell>

<!-- RDS 数据库 -->
<mxCell id="rds" value="RDS&#xa;MySQL"
        style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#3B48CC;strokeColor=#2A36A3;fontColor=#ffffff;shadow=1;"
        vertex="1" parent="private_subnet">
  <mxGeometry x="30" y="50" width="80" height="80" as="geometry"/>
</mxCell>

<!-- S3 存储桶 -->
<mxCell id="s3" value="S3&#xa;Assets"
        style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#3F8624;strokeColor=#2E6B1A;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="800" y="200" width="80" height="80" as="geometry"/>
</mxCell>

<!-- Lambda 函数 -->
<mxCell id="lambda" value="Lambda&#xa;API Handler"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF9900;strokeColor=#FF6600;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="100" width="100" height="60" as="geometry"/>
</mxCell>

<!-- 负载均衡器 -->
<mxCell id="elb" value="ALB"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#8C4FFF;strokeColor=#6B3ACC;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="80" height="50" as="geometry"/>
</mxCell>
```

### 1.4 GCP 风格配色

| 服务类型 | fillColor | strokeColor |
|---------|-----------|-------------|
| Compute Engine | #4285F4 | #1967D2 |
| Cloud Storage | #4285F4 | #1967D2 |
| Cloud SQL | #4285F4 | #1967D2 |
| BigQuery | #669DF6 | #4285F4 |
| Pub/Sub | #AECBFA | #669DF6 |

### 1.5 Azure 风格配色

| 服务类型 | fillColor | strokeColor |
|---------|-----------|-------------|
| VM | #0078D4 | #005A9E |
| Storage | #0078D4 | #005A9E |
| SQL Database | #0078D4 | #005A9E |
| App Service | #50E6FF | #0078D4 |

---

## 二、微服务架构图

### 2.1 服务节点

```xml
<!-- 微服务（圆角矩形 + 渐变） -->
<mxCell id="user_service" value="User Service&#xa;:8080"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#4CAF50;gradientColor=#2E7D32;strokeColor=#1B5E20;fontColor=#ffffff;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="120" height="60" as="geometry"/>
</mxCell>

<mxCell id="order_service" value="Order Service&#xa;:8081"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#2196F3;gradientColor=#1565C0;strokeColor=#0D47A1;fontColor=#ffffff;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="200" width="120" height="60" as="geometry"/>
</mxCell>

<mxCell id="payment_service" value="Payment Service&#xa;:8082"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF9800;gradientColor=#EF6C00;strokeColor=#E65100;fontColor=#ffffff;shadow=1;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="200" width="120" height="60" as="geometry"/>
</mxCell>
```

### 2.2 API 网关

```xml
<mxCell id="api_gateway" value="API Gateway"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9C27B0;gradientColor=#6A1B9A;strokeColor=#4A148C;fontColor=#ffffff;shadow=1;strokeWidth=2;"
        vertex="1" parent="1">
  <mxGeometry x="250" y="50" width="200" height="50" as="geometry"/>
</mxCell>
```

### 2.3 消息队列

```xml
<!-- Kafka/RabbitMQ -->
<mxCell id="message_queue" value="Message Queue&#xa;(Kafka)"
        style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#FF6F00;strokeColor=#E65100;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="350" width="100" height="80" as="geometry"/>
</mxCell>
```

### 2.4 服务发现/注册中心

```xml
<mxCell id="service_registry" value="Service Registry&#xa;(Consul/Eureka)"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#607D8B;strokeColor=#455A64;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="550" y="50" width="120" height="60" as="geometry"/>
</mxCell>
```

### 2.5 微服务连线样式

```xml
<!-- 同步调用（实线） -->
<mxCell id="sync_call" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;strokeWidth=2;"
        edge="1" parent="1" source="user_service" target="order_service">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 异步消息（虚线） -->
<mxCell id="async_msg" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;dashed=1;strokeColor=#FF6F00;"
        edge="1" parent="1" source="order_service" target="message_queue">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 服务注册（点线） -->
<mxCell id="register" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=none;dashed=1;dashPattern=1 4;strokeColor=#607D8B;"
        edge="1" parent="1" source="user_service" target="service_registry">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 三、分层架构图

### 3.1 三层架构

```xml
<!-- 表示层 -->
<mxCell id="presentation" value="表示层 (Presentation)"
        style="swimlane;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;startSize=30;horizontal=0;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="700" height="120" as="geometry"/>
</mxCell>

<!-- 业务层 -->
<mxCell id="business" value="业务层 (Business)"
        style="swimlane;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#4CAF50;startSize=30;horizontal=0;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="170" width="700" height="120" as="geometry"/>
</mxCell>

<!-- 数据层 -->
<mxCell id="data" value="数据层 (Data)"
        style="swimlane;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#FF9800;startSize=30;horizontal=0;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="290" width="700" height="120" as="geometry"/>
</mxCell>

<!-- 层内组件 -->
<mxCell id="web_app" value="Web App" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="presentation">
  <mxGeometry x="50" y="40" width="100" height="50" as="geometry"/>
</mxCell>

<mxCell id="mobile_app" value="Mobile App" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="presentation">
  <mxGeometry x="180" y="40" width="100" height="50" as="geometry"/>
</mxCell>

<mxCell id="api_service" value="API Service" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="business">
  <mxGeometry x="50" y="40" width="100" height="50" as="geometry"/>
</mxCell>

<mxCell id="db" value="Database" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;" vertex="1" parent="data">
  <mxGeometry x="50" y="30" width="80" height="70" as="geometry"/>
</mxCell>
```

---

## 四、网络拓扑图

### 4.1 网络设备样式

```xml
<!-- 路由器 -->
<mxCell id="router" value="Router"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;strokeWidth=2;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="100" height="60" as="geometry"/>
</mxCell>

<!-- 交换机 -->
<mxCell id="switch" value="Switch"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;strokeWidth=2;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="200" width="100" height="40" as="geometry"/>
</mxCell>

<!-- 防火墙 -->
<mxCell id="firewall" value="Firewall"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFCDD2;strokeColor=#F44336;strokeWidth=2;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="50" width="100" height="30" as="geometry"/>
</mxCell>

<!-- 服务器 -->
<mxCell id="server" value="Server"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#4CAF50;strokeWidth=2;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="300" width="80" height="100" as="geometry"/>
</mxCell>

<!-- 客户端/PC -->
<mxCell id="client" value="Client"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFF9C4;strokeColor=#FBC02D;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="300" width="60" height="50" as="geometry"/>
</mxCell>

<!-- 云/互联网 -->
<mxCell id="internet" value="Internet"
        style="ellipse;shape=cloud;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#9E9E9E;"
        vertex="1" parent="1">
  <mxGeometry x="250" y="0" width="200" height="80" as="geometry"/>
</mxCell>
```

### 4.2 网络连线

```xml
<!-- 物理连接 -->
<mxCell id="physical" style="endArrow=none;strokeWidth=2;strokeColor=#000000;"
        edge="1" parent="1" source="router" target="switch">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<!-- 虚拟连接 -->
<mxCell id="virtual" style="endArrow=none;strokeWidth=2;dashed=1;strokeColor=#2196F3;"
        edge="1" parent="1" source="vm1" target="vm2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

---

## 五、C4 模型

### 5.1 系统上下文图 (Level 1)

```xml
<!-- 人物 -->
<mxCell id="user" value="用户"
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="150" width="40" height="80" as="geometry"/>
</mxCell>

<!-- 核心系统（蓝色大框） -->
<mxCell id="system" value="电商系统&#xa;[Software System]&#xa;&#xa;处理用户订单和支付"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#438DD5;strokeColor=#3C7FC0;fontColor=#ffffff;align=center;verticalAlign=middle;"
        vertex="1" parent="1">
  <mxGeometry x="250" y="120" width="200" height="140" as="geometry"/>
</mxCell>

<!-- 外部系统（灰色） -->
<mxCell id="external" value="支付网关&#xa;[External System]"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#999999;strokeColor=#666666;fontColor=#ffffff;"
        vertex="1" parent="1">
  <mxGeometry x="550" y="150" width="150" height="80" as="geometry"/>
</mxCell>
```

### 5.2 容器图 (Level 2)

```xml
<!-- 系统边界 -->
<mxCell id="system_boundary" value="电商系统 [System]"
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#438DD5;strokeWidth=2;dashed=1;verticalAlign=top;align=left;spacingLeft=10;"
        vertex="1" parent="1">
  <mxGeometry x="50" y="50" width="600" height="400" as="geometry"/>
</mxCell>

<!-- Web 应用容器 -->
<mxCell id="web_container" value="Web Application&#xa;[Container: React]&#xa;&#xa;用户界面"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#438DD5;strokeColor=#3C7FC0;fontColor=#ffffff;"
        vertex="1" parent="system_boundary">
  <mxGeometry x="30" y="50" width="150" height="100" as="geometry"/>
</mxCell>

<!-- API 容器 -->
<mxCell id="api_container" value="API Application&#xa;[Container: Node.js]&#xa;&#xa;业务逻辑"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#438DD5;strokeColor=#3C7FC0;fontColor=#ffffff;"
        vertex="1" parent="system_boundary">
  <mxGeometry x="220" y="50" width="150" height="100" as="geometry"/>
</mxCell>

<!-- 数据库容器 -->
<mxCell id="db_container" value="Database&#xa;[Container: PostgreSQL]&#xa;&#xa;数据存储"
        style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#438DD5;strokeColor=#3C7FC0;fontColor=#ffffff;"
        vertex="1" parent="system_boundary">
  <mxGeometry x="220" y="200" width="150" height="120" as="geometry"/>
</mxCell>
```

---

## 六、完整示例：微服务电商架构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Claude Code">
  <diagram name="电商微服务架构" id="ecommerce">
    <mxGraphModel dx="1200" dy="800" grid="1" page="1" pageWidth="1200" pageHeight="800">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- 客户端 -->
        <mxCell id="client" value="客户端&#xa;(Web/Mobile)"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;"
                vertex="1" parent="1">
          <mxGeometry x="500" y="30" width="120" height="50" as="geometry"/>
        </mxCell>

        <!-- API Gateway -->
        <mxCell id="gateway" value="API Gateway&#xa;(Kong/Nginx)"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9C27B0;strokeColor=#6A1B9A;fontColor=#ffffff;shadow=1;"
                vertex="1" parent="1">
          <mxGeometry x="480" y="120" width="160" height="50" as="geometry"/>
        </mxCell>

        <!-- 服务层边界 -->
        <mxCell id="services_boundary" value="Services"
                style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#9E9E9E;strokeWidth=1;dashed=1;verticalAlign=top;align=left;"
                vertex="1" parent="1">
          <mxGeometry x="100" y="200" width="920" height="180" as="geometry"/>
        </mxCell>

        <!-- 微服务 -->
        <mxCell id="user_svc" value="User Service&#xa;:8080"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=#2E7D32;fontColor=#ffffff;shadow=1;"
                vertex="1" parent="1">
          <mxGeometry x="130" y="250" width="120" height="60" as="geometry"/>
        </mxCell>

        <mxCell id="product_svc" value="Product Service&#xa;:8081"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=#1565C0;fontColor=#ffffff;shadow=1;"
                vertex="1" parent="1">
          <mxGeometry x="300" y="250" width="120" height="60" as="geometry"/>
        </mxCell>

        <mxCell id="order_svc" value="Order Service&#xa;:8082"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FF9800;strokeColor=#EF6C00;fontColor=#ffffff;shadow=1;"
                vertex="1" parent="1">
          <mxGeometry x="500" y="250" width="120" height="60" as="geometry"/>
        </mxCell>

        <mxCell id="payment_svc" value="Payment Service&#xa;:8083"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F44336;strokeColor=#C62828;fontColor=#ffffff;shadow=1;"
                vertex="1" parent="1">
          <mxGeometry x="700" y="250" width="120" height="60" as="geometry"/>
        </mxCell>

        <mxCell id="notification_svc" value="Notification&#xa;:8084"
                style="rounded=1;whiteSpace=wrap;html=1;fillColor=#9C27B0;strokeColor=#6A1B9A;fontColor=#ffffff;shadow=1;"
                vertex="1" parent="1">
          <mxGeometry x="870" y="250" width="120" height="60" as="geometry"/>
        </mxCell>

        <!-- 数据层 -->
        <mxCell id="user_db" value="User DB"
                style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#4CAF50;strokeColor=#2E7D32;fontColor=#ffffff;"
                vertex="1" parent="1">
          <mxGeometry x="145" y="450" width="70" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="product_db" value="Product DB"
                style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#2196F3;strokeColor=#1565C0;fontColor=#ffffff;"
                vertex="1" parent="1">
          <mxGeometry x="320" y="450" width="70" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="order_db" value="Order DB"
                style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#FF9800;strokeColor=#EF6C00;fontColor=#ffffff;"
                vertex="1" parent="1">
          <mxGeometry x="520" y="450" width="70" height="70" as="geometry"/>
        </mxCell>

        <!-- 消息队列 -->
        <mxCell id="kafka" value="Kafka"
                style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#607D8B;strokeColor=#455A64;fontColor=#ffffff;"
                vertex="1" parent="1">
          <mxGeometry x="720" y="450" width="80" height="70" as="geometry"/>
        </mxCell>

        <!-- Redis 缓存 -->
        <mxCell id="redis" value="Redis"
                style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#F44336;strokeColor=#C62828;fontColor=#ffffff;"
                vertex="1" parent="1">
          <mxGeometry x="900" y="450" width="70" height="70" as="geometry"/>
        </mxCell>

        <!-- 连线 -->
        <mxCell id="e1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="client" target="gateway">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="gateway" target="user_svc">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="gateway" target="product_svc">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="gateway" target="order_svc">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="gateway" target="payment_svc">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- 服务到数据库 -->
        <mxCell id="e6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="user_svc" target="user_db">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e7" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="product_svc" target="product_db">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e8" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;"
                edge="1" parent="1" source="order_svc" target="order_db">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- 异步消息 -->
        <mxCell id="e9" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;dashed=1;strokeColor=#607D8B;"
                edge="1" parent="1" source="order_svc" target="kafka">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="e10" style="edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=classic;dashed=1;strokeColor=#607D8B;"
                edge="1" parent="1" source="kafka" target="notification_svc">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```
