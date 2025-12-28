# DevOps 与开源生态素材库

CI/CD、容器化、监控、开源技术栈的图标和样式。

## CI/CD 流水线

### 阶段节点样式

```xml
<!-- 流水线阶段（圆角矩形 + 渐变） -->
<mxCell value="Build"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#1565C0;gradientColor=#0D47A1;fontColor=#FFFFFF;strokeColor=none;shadow=1;arcSize=20;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="50" as="geometry"/>
</mxCell>

<!-- 成功阶段 -->
<mxCell style="...;fillColor=#2E7D32;gradientColor=#1B5E20;..." .../>

<!-- 失败阶段 -->
<mxCell style="...;fillColor=#C62828;gradientColor=#B71C1C;..." .../>

<!-- 进行中阶段 -->
<mxCell style="...;fillColor=#F57C00;gradientColor=#E65100;..." .../>
```

### 流水线连线

```xml
<!-- 阶段间连线 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;strokeColor=#00ACC1;strokeWidth=2;"
        edge="1" .../>

<!-- 并行分支 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=classic;strokeColor=#00ACC1;dashed=1;"
        edge="1" .../>
```

### 典型 CI/CD 阶段

| 阶段 | 颜色 | Unicode 图标 |
|------|------|-------------|
| Source | #546E7A | 📥 |
| Build | #1565C0 | 🔨 |
| Test | #7B1FA2 | 🧪 |
| Security Scan | #C62828 | 🔒 |
| Deploy Staging | #F57C00 | 🚀 |
| Approval | #FFA000 | ✋ |
| Deploy Prod | #2E7D32 | ✅ |

---

## 容器与编排

### Docker

```xml
<!-- Docker 容器 -->
<mxCell value="🐳 Container"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#2196F3;strokeColor=#1565C0;fontColor=#FFFFFF;arcSize=15;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry"/>
</mxCell>

<!-- Docker 镜像 -->
<mxCell value="📦 Image:tag"
        style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;size=10;fillColor=#2196F3;strokeColor=#1565C0;fontColor=#FFFFFF;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="200" width="100" height="70" as="geometry"/>
</mxCell>

<!-- Docker Registry -->
<mxCell value="🏪 Registry"
        style="shape=cube;whiteSpace=wrap;html=1;boundedLbl=1;fillColor=#1976D2;strokeColor=#0D47A1;fontColor=#FFFFFF;"
        vertex="1" parent="1">
  <mxGeometry x="100" y="300" width="120" height="80" as="geometry"/>
</mxCell>
```

### Kubernetes 扩展

```xml
<!-- Pod（带状态指示） -->
<mxCell value="Pod ✅"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#326CE5;strokeColor=#1E3A8A;fontColor=#FFFFFF;arcSize=30;"
        vertex="1" .../>

<!-- Pod Pending -->
<mxCell value="Pod ⏳"
        style="...;fillColor=#FFA726;strokeColor=#E65100;..." .../>

<!-- Pod Failed -->
<mxCell value="Pod ❌"
        style="...;fillColor=#EF5350;strokeColor=#C62828;..." .../>

<!-- Deployment -->
<mxCell value="Deployment"
        style="shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fillColor=#326CE5;strokeColor=#1E3A8A;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- Service -->
<mxCell value="Service"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#7C4DFF;strokeColor=#4527A0;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- ConfigMap/Secret -->
<mxCell value="ConfigMap"
        style="shape=note;whiteSpace=wrap;html=1;fillColor=#FFE082;strokeColor=#FFA000;fontColor=#333333;"
        vertex="1" .../>

<!-- PersistentVolume -->
<mxCell value="PVC"
        style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#90CAF9;strokeColor=#1565C0;"
        vertex="1" .../>

<!-- Ingress -->
<mxCell value="Ingress"
        style="shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fillColor=#4DB6AC;strokeColor=#00897B;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- Namespace（容器框） -->
<mxCell value="namespace: production"
        style="swimlane;horizontal=1;startSize=30;fillColor=none;strokeColor=#326CE5;strokeWidth=2;dashed=1;"
        vertex="1" .../>
```

---

## 监控与可观测性

### Prometheus

```xml
<!-- Prometheus -->
<mxCell value="🔥 Prometheus"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E65100;strokeColor=#BF360C;fontColor=#FFFFFF;shadow=1;"
        vertex="1" .../>

<!-- Metrics -->
<mxCell value="📊 Metrics"
        style="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fillColor=#FFCC80;strokeColor=#E65100;"
        vertex="1" .../>

<!-- AlertManager -->
<mxCell value="🚨 AlertManager"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#D32F2F;strokeColor=#B71C1C;fontColor=#FFFFFF;"
        vertex="1" .../>
```

### Grafana

```xml
<!-- Grafana -->
<mxCell value="📈 Grafana"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F57C00;strokeColor=#E65100;fontColor=#FFFFFF;shadow=1;"
        vertex="1" .../>

<!-- Dashboard -->
<mxCell value="Dashboard"
        style="shape=document;whiteSpace=wrap;html=1;fillColor=#FFE0B2;strokeColor=#F57C00;"
        vertex="1" .../>
```

### ELK Stack

```xml
<!-- Elasticsearch -->
<mxCell value="🔍 Elasticsearch"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#00BCD4;strokeColor=#0097A7;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- Logstash -->
<mxCell value="📝 Logstash"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFC107;strokeColor=#FFA000;fontColor=#333333;"
        vertex="1" .../>

<!-- Kibana -->
<mxCell value="📊 Kibana"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E91E63;strokeColor=#C2185B;fontColor=#FFFFFF;"
        vertex="1" .../>
```

### Jaeger/Tracing

```xml
<!-- Jaeger -->
<mxCell value="🔗 Jaeger"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#00BFA5;strokeColor=#00897B;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- Trace -->
<mxCell value="Trace"
        style="shape=process;whiteSpace=wrap;html=1;fillColor=#B2DFDB;strokeColor=#00897B;"
        vertex="1" .../>
```

---

## 版本控制与协作

### Git 工作流

```xml
<!-- 分支节点 -->
<mxCell value="main"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#2E7D32;strokeColor=#1B5E20;fontColor=#FFFFFF;"
        vertex="1" .../>

<mxCell value="develop"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#1565C0;strokeColor=#0D47A1;fontColor=#FFFFFF;"
        vertex="1" .../>

<mxCell value="feature/*"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#7B1FA2;strokeColor=#4A148C;fontColor=#FFFFFF;"
        vertex="1" .../>

<mxCell value="hotfix/*"
        style="ellipse;whiteSpace=wrap;html=1;fillColor=#C62828;strokeColor=#B71C1C;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- Commit -->
<mxCell value="●"
        style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#333333;strokeColor=#333333;"
        vertex="1" .../>

<!-- Merge 箭头 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=1;dashed=1;endArrow=classic;strokeColor=#666666;"
        edge="1" .../>
```

### GitHub/GitLab

```xml
<!-- Pull Request / Merge Request -->
<mxCell value="PR #123"
        style="shape=callout;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1976D2;perimeter=calloutPerimeter;"
        vertex="1" .../>

<!-- Issue -->
<mxCell value="Issue #456"
        style="shape=note;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#F57C00;"
        vertex="1" .../>

<!-- Action/Pipeline -->
<mxCell value="▶ CI Pipeline"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#4CAF50;strokeColor=#2E7D32;fontColor=#FFFFFF;"
        vertex="1" .../>
```

---

## 常用开源技术栈

### 数据库

| 技术 | 颜色 | 图标 |
|------|------|------|
| PostgreSQL | #336791 | 🐘 |
| MySQL | #4479A1 | 🐬 |
| MongoDB | #47A248 | 🍃 |
| Redis | #DC382D | ⚡ |
| Cassandra | #1287B1 | 👁 |
| InfluxDB | #22ADF6 | 📈 |

```xml
<!-- PostgreSQL -->
<mxCell value="🐘 PostgreSQL"
        style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#336791;strokeColor=#1E3A5F;fontColor=#FFFFFF;boundedLbl=1;"
        vertex="1" .../>
```

### 消息队列

| 技术 | 颜色 | 图标 |
|------|------|------|
| Kafka | #231F20 | 📨 |
| RabbitMQ | #FF6600 | 🐰 |
| NATS | #27AAE1 | 📮 |
| Pulsar | #188FFF | 🌟 |

```xml
<!-- Kafka -->
<mxCell value="📨 Kafka"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#231F20;strokeColor=#000000;fontColor=#FFFFFF;arcSize=10;"
        vertex="1" .../>
```

### Web 框架

| 技术 | 颜色 |
|------|------|
| Nginx | #009639 |
| Apache | #D22128 |
| Node.js | #339933 |
| Spring | #6DB33F |
| Django | #092E20 |
| FastAPI | #009688 |

### 服务网格

```xml
<!-- Istio -->
<mxCell value="Istio"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#466BB0;strokeColor=#2C4A7F;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- Envoy -->
<mxCell value="Envoy"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#AC6199;strokeColor=#8B4F7A;fontColor=#FFFFFF;"
        vertex="1" .../>

<!-- Linkerd -->
<mxCell value="Linkerd"
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#2BEDA7;strokeColor=#1FA77A;fontColor=#333333;"
        vertex="1" .../>
```

---

## DevOps 架构模板

### 微服务 + K8s 架构

```
[Ingress] → [Service] → [Deployment]
                              ↓
                          [Pod] [Pod] [Pod]
                              ↓
         [ConfigMap] [Secret] [PVC]
```

### CI/CD 流水线

```
[Git Push] → [Build] → [Test] → [Scan] → [Stage] → [Approval] → [Prod]
                ↓          ↓        ↓
            [Docker]  [Sonar]  [Trivy]
```

### 监控堆栈

```
[App] → [Prometheus] → [Grafana]
  ↓           ↓
[Logs]    [AlertManager]
  ↓           ↓
[Fluentd] → [Elasticsearch] → [Kibana]
  ↓
[Jaeger]
```

---

## 配色方案

### DevOps 蓝绿配色

```
主色:     #1565C0 (蓝色 - 构建/部署)
成功:     #2E7D32 (绿色)
警告:     #F57C00 (橙色)
错误:     #C62828 (红色)
中性:     #546E7A (灰色)
Kubernetes: #326CE5 (K8s 蓝)
Docker:   #2196F3 (Docker 蓝)
```

### 开源技术配色

```
PostgreSQL: #336791
MongoDB:    #47A248
Redis:      #DC382D
Kafka:      #231F20
RabbitMQ:   #FF6600
Nginx:      #009639
Spring:     #6DB33F
```
