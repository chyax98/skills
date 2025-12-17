# DrawIO 图标库指南

## 概述

DrawIO 内置了丰富的图标库，包括 AWS、Azure、Kubernetes、GCP 等云服务图标，以及各种业务和技术图标。

## ⚠️ 重要提示

1. **图标库需要启用**：在生成的 .drawio 文件中使用云服务图标时，需要确保 DrawIO 编辑器已加载对应的图标库
2. **形状名称来源**：shape 名称来自 mxGraph 库，格式为 `shape=mxgraph.{库名}.{形状名}`
3. **兼容性**：部分旧版本的 DrawIO 可能不支持某些新图标
4. **建议**：在生成复杂图表前，先在 DrawIO 编辑器中测试图标是否可用

## AWS 图标库

### 启用 AWS 图标库

在 DrawIO 中通过 "More Shapes" → "Networking" → 选择 AWS 图标库。在 XML 中直接使用：

```xml
<!-- AWS Lambda 函数 -->
<mxCell id="aws_lambda" value="Lambda"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws3.lambda_function;fillColor=#F58534;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="80" height="80" as="geometry"/>
</mxCell>

<!-- AWS EC2 实例 -->
<mxCell id="aws_ec2" value="EC2"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws3.ec2_instance;fillColor=#FF9900;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="100" width="80" height="80" as="geometry"/>
</mxCell>

<!-- AWS S3 存储桶 -->
<mxCell id="aws_s3" value="S3"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws3.s3_bucket;fillColor=#569A31;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="300" y="100" width="80" height="80" as="geometry"/>
</mxCell>

<!-- AWS RDS 数据库 -->
<mxCell id="aws_rds" value="RDS"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws3.rds_instance;fillColor=#7AA116;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="400" y="100" width="80" height="80" as="geometry"/>
</mxCell>

<!-- AWS API Gateway -->
<mxCell id="aws_api_gateway" value="API GW"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.aws3.api_gateway;fillColor=#dd344c;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="500" y="100" width="80" height="80" as="geometry"/>
</mxCell>
```

### 常用 AWS 服务图标

| 服务 | Shape 名称 | 默认颜色 |
|------|------------|----------|
| Lambda | `mxgraph.aws3.lambda_function` | #F58534 |
| EC2 | `mxgraph.aws3.ec2_instance` | #FF9900 |
| S3 | `mxgraph.aws3.s3_bucket` | #569A31 |
| RDS | `mxgraph.aws3.rds_instance` | #7AA116 |
| DynamoDB | `mxgraph.aws3.dynamodb_table` | #4053A6 |
| CloudFront | `mxgraph.aws3.cloudfront` | #A1666F |
| VPC | `mxgraph.aws3.vpc` | #5A30B5 |
| Elastic Load Balancer | `mxgraph.aws3.elastic_load_balancer` | #8C4799 |
| SQS | `mxgraph.aws3.sqs_queue` | #FF5252 |
| SNS | `mxgraph.aws3.sns_topic` | #D86613 |
| CloudWatch | `mxgraph.aws3.cloudwatch_alarm` | #FF9900 |
| IAM | `mxgraph.aws3.iam_role` | #DD344C |

## Azure 图标库

```xml
<!-- Azure 虚拟机 -->
<mxCell id="azure_vm" value="VM"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.azure.vm_windows;fillColor=#0078D4;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Azure App Service -->
<mxCell id="azure_app" value="App Service"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.azure.app_service;fillColor=#0078D4;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="170" y="200" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Azure Storage -->
<mxCell id="azure_storage" value="Storage"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.azure.storage_account;fillColor=#0078D4;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="240" y="200" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Azure SQL Database -->
<mxCell id="azure_sql" value="SQL DB"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.azure.sql_database;fillColor=#0078D4;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="310" y="200" width="50" height="50" as="geometry"/>
</mxCell>
```

## Kubernetes 图标库

```xml
<!-- Kubernetes Pod -->
<mxCell id="k8s_pod" value="Pod"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.kubernetes.pod;fillColor=#326CE5;strokeColor=#326CE5;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="300" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Kubernetes Service -->
<mxCell id="k8s_service" value="Service"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.kubernetes.service;fillColor=#326CE5;strokeColor=#326CE5;"
        vertex="1" parent="1">
  <mxGeometry x="170" y="300" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Kubernetes Deployment -->
<mxCell id="k8s_deployment" value="Deployment"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.kubernetes.deployment;fillColor=#326CE5;strokeColor=#326CE5;"
        vertex="1" parent="1">
  <mxGeometry x="240" y="300" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Kubernetes Ingress -->
<mxCell id="k8s_ingress" value="Ingress"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.kubernetes.ingress;fillColor=#326CE5;strokeColor=#326CE5;"
        vertex="1" parent="1">
  <mxGeometry x="310" y="300" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Kubernetes Node -->
<mxCell id="k8s_node" value="Node"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.kubernetes.node;fillColor=#326CE5;strokeColor=#326CE5;"
        vertex="1" parent="1">
  <mxGeometry x="380" y="300" width="50" height="50" as="geometry"/>
</mxCell>

<!-- Kubernetes Cluster -->
<mxCell id="k8s_cluster" value="Cluster"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.kubernetes.cluster;fillColor=#326CE5;strokeColor=#326CE5;"
        vertex="1" parent="1">
  <mxGeometry x="450" y="300" width="50" height="50" as="geometry"/>
</mxCell>
```

## GCP 图标库

```xml
<!-- GCP Compute Engine -->
<mxCell id="gcp_compute" value="Compute"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.gcp2.compute_engine;fillColor=#4285F4;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="400" width="50" height="50" as="geometry"/>
</mxCell>

<!-- GCP Cloud Storage -->
<mxCell id="gcp_storage" value="Storage"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.gcp2.cloud_storage;fillColor=#0F9D58;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="170" y="400" width="50" height="50" as="geometry"/>
</mxCell>

<!-- GCP BigQuery -->
<mxCell id="gcp_bigquery" value="BigQuery"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.gcp2.bigquery;fillColor=#4285F4;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="240" y="400" width="50" height="50" as="geometry"/>
</mxCell>

<!-- GCP Cloud Functions -->
<mxCell id="gcp_functions" value="Functions"
        style="outlineConnect=0;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;shape=mxgraph.gcp2.cloud_functions;fillColor=#F4B400;gradientColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="310" y="400" width="50" height="50" as="geometry"/>
</mxCell>
```

## 业务图标

### 用户相关图标

```xml
<!-- 用户（Actor） -->
<mxCell id="user" value="用户"
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="500" width="30" height="60" as="geometry"/>
</mxCell>

<!-- 用户组 -->
<mxCell id="users" value="用户组"
        style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;"
        vertex="1" parent="1">
  <mxGeometry x="150" y="500" width="80" height="60" as="geometry"/>
</mxCell>
```

### 设备图标

```xml
<!-- 电脑 -->
<mxCell id="desktop" value=""
        style="shape=desktop;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="250" y="500" width="60" height="50" as="geometry"/>
</mxCell>

<!-- 笔记本 -->
<mxCell id="laptop" value=""
        style="shape=notebook;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="330" y="500" width="60" height="40" as="geometry"/>
</mxCell>

<!-- 手机 -->
<mxCell id="mobile" value=""
        style="shape=mobileDevice2;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="410" y="500" width="30" height="50" as="geometry"/>
</mxCell>

<!-- 平板 -->
<mxCell id="tablet" value=""
        style="shape=tablet2;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="460" y="500" width="50" height="40" as="geometry"/>
</mxCell>
```

### 网络图标

```xml
<!-- 云 -->
<mxCell id="cloud" value="云"
        style="shape=cloud;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="530" y="500" width="80" height="50" as="geometry"/>
</mxCell>

<!-- 服务器 -->
<mxCell id="server" value="服务器"
        style="shape=cube;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;"
        vertex="1" parent="1">
  <mxGeometry x="630" y="500" width="60" height="60" as="geometry"/>
</mxCell>

<!-- 数据库 -->
<mxCell id="database" value="数据库"
        style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;"
        vertex="1" parent="1">
  <mxGeometry x="710" y="500" width="60" height="60" as="geometry"/>
</mxCell>
```

### 业务图标

```xml
<!-- 购物车 -->
<mxCell id="cart" value="购物车"
        style="shape=document;whiteSpace=wrap;html=1;boundedLbl=1;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="600" width="80" height="60" as="geometry"/>
</mxCell>

<!-- 邮件 -->
<mxCell id="email" value="邮件"
        style="shape=mxgraph.basic.email;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="600" width="60" height="40" as="geometry"/>
</mxCell>

<!-- 设置/齿轮 -->
<mxCell id="settings" value="设置"
        style="shape=mxgraph.basic.gear;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="280" y="600" width="50" height="50" as="geometry"/>
</mxCell>

<!-- 锁 -->
<mxCell id="lock" value="安全"
        style="shape=mxgraph.basic.lock;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="350" y="600" width="40" height="50" as="geometry"/>
</mxCell>

<!-- 问号/帮助 -->
<mxCell id="help" value="帮助"
        style="shape=mxgraph.basic.question_mark;whiteSpace=wrap;html=1;"
        vertex="1" parent="1">
  <mxGeometry x="410" y="600" width="40" height="50" as="geometry"/>
</mxCell>
```

## 图标使用技巧

### 1. 自定义图标颜色

```xml
<!-- 修改 AWS Lambda 颜色 -->
<style="shape=mxgraph.aws3.lambda_function;fillColor=#2196F3;strokeColor=#1976D2;"
```

### 2. 添加阴影效果

```xml
<style="shape=mxgraph.aws3.ec2_instance;fillColor=#FF9900;shadow=1;"
```

### 3. 组合图标和文本

```xml
<!-- 图标和文字分离布局 -->
<mxCell id="icon" value=""
        style="shape=mxgraph.aws3.lambda_function;fillColor=#F58534;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="60" height="60" as="geometry"/>
</mxCell>

<mxCell id="label" value="处理函数"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="170" width="60" height="20" as="geometry"/>
</mxCell>
```

### 4. 使用图标作为连接点

```xml
<!-- 为图标添加自定义连接点 -->
<mxCell id="icon_with_points" value="处理"
        style="shape=mxgraph.aws3.lambda_function;points=[[0,0.5],[1,0.5],[0.5,0],[0.5,1]];fillColor=#F58534;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="60" height="60" as="geometry"/>
</mxCell>
```

### 5. 图标大小标准化

| 用途 | 推荐尺寸 |
|------|----------|
| 小图标（列表中） | 32×32 |
| 标准图标 | 48×48 或 60×60 |
| 大图标（展示） | 80×80 或 100×100 |

### 6. 图标对齐网格

```xml
<!-- 保持图标对齐 10px 网格 -->
<mxGeometry x="100" y="100" width="80" height="80" as="geometry"/>
```

## 完整示例：微服务架构

```xml
<!-- API Gateway -->
<mxCell id="api_gateway" value=""
        style="shape=mxgraph.aws3.api_gateway;fillColor="#dd344c";outlineConnect=0;"
        vertex="1" parent="1">
  <mxGeometry x="360" y="50" width="80" height="80" as="geometry"/>
</mxCell>

<!-- 服务1：用户服务 -->
<mxCell id="user_service" value=""
        style="shape=mxgraph.kubernetes.pod;fillColor=#326CE5;outlineConnect=0;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="50" height="50" as="geometry"/>
</mxCell>
<mxCell id="user_label" value="用户服务"
        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;"
        vertex="1" parent="1">
  <mxGeometry x="200" y="260" width="50" height="20" as="geometry"/>
</mxCell>

<!-- 服务2：订单服务 -->
<mxCell id="order_service" value=""
        style="shape=mxgraph.kubernetes.pod;fillColor=#326CE5;outlineConnect=0;"
        vertex="1" parent="1">
  <mxGeometry x="375" y="200" width="50" height="50" as="geometry"/>
</mxCell>

<!-- 服务3：支付服务 -->
<mxCell id="payment_service" value=""
        style="shape=mxgraph.kubernetes.pod;fillColor=#326CE5;outlineConnect=0;"
        vertex="1" parent="1">
  <mxGeometry x="550" y="200" width="50" height="50" as="geometry"/>
</mxCell>

<!-- 数据库层 -->
<mxCell id="database" value=""
        style="shape=mxgraph.aws3.rds_instance;fillColor=#7AA116;outlineConnect=0;"
        vertex="1" parent="1">
  <mxGeometry x="375" y="350" width="80" height="80" as="geometry"/>
</mxCell>

<!-- 连接线 -->
<mxCell id="edge1" style="edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=1;entryX=0.5;entryY=0;endArrow=classic;strokeColor=#666666;" edge="1" parent="1" source="api_gateway" target="user_service">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>

<mxCell id="edge2" style="edgeStyle=orthogonalEdgeStyle;exitX=0.5;exitY=1;entryX=0.5;entryY=0;endArrow=classic;strokeColor=#666666;" edge="1" parent="1" source="api_gateway" target="order_service">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## 注意事项

1. **版本兼容性**：不同 DrawIO 版本的图标库可能有差异
2. **离线使用**：保存图表时图标会嵌入 XML 中，无需额外文件
3. **自定义图标**：可以通过 `shape=image` 使用自定义 SVG/PNG 图标
4. **性能考虑**：过多复杂图标可能影响性能，适当使用
5. **品牌规范**：使用云服务图标时遵守相应的品牌使用规范