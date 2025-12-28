# DrawIO Generator Asset Knowledge Base

## 概述

本目录包含 DrawIO 图表生成器的完整素材知识库，采用 JSON 格式，支持语义检索。

## 文件结构

```
assets/
├── index.json          # 统一索引，包含快速查找表和预设样式
├── cloud_icons.json    # 云服务图标 (AWS, Azure, GCP, K8s)
├── basic_shapes.json   # 基础形状和样式
├── domain_assets.json  # 领域专用素材 (AI/ML, DevOps, 网络等)
└── README.md           # 本文档
```

## 使用方式

### 1. 按用例查找

`index.json` 中的 `quick_lookup.by_use_case` 提供常见场景的推荐组件：

```python
# 示例：获取微服务架构推荐组件
use_case = index["quick_lookup"]["by_use_case"]["microservice_architecture"]
recommended_icons = use_case["recommended"]
container_type = use_case["container"]
edge_style = use_case["edge_style"]
```

支持的用例：
- `microservice_architecture` - 微服务架构
- `ai_ml_pipeline` - AI/ML 流水线
- `network_topology` - 网络拓扑
- `cicd_pipeline` - CI/CD 流水线
- `cloud_architecture` - 云架构
- `transformer_model` - Transformer 模型
- `data_lake` - 数据湖
- `kubernetes_deployment` - K8s 部署

### 2. 按关键词查找

`index.json` 中的 `quick_lookup.by_keyword` 提供关键词到图标的映射：

```python
# 示例：查找数据库相关图标
db_icons = index["quick_lookup"]["by_keyword"]["database"]
# 返回: ["aws_rds", "aws_dynamodb", "azure_sql", ...]
```

支持的关键词：
- `database`, `serverless`, `container`, `storage`
- `messaging`, `api`, `load_balancer`, `security`
- `monitoring`, `ai_ml`

### 3. 获取具体图标样式

从具体的 JSON 文件中获取完整样式：

```python
import json

# 加载云图标库
with open("cloud_icons.json") as f:
    cloud_icons = json.load(f)

# 获取 AWS Lambda 图标
for icon in cloud_icons["categories"]["aws"]["icons"]["compute"]:
    if icon["id"] == "aws_lambda":
        shape = icon["shape"]        # mxgraph.aws3.lambda_function
        fill = icon["fillColor"]     # #F58534
        size = icon["size"]          # {"width": 80, "height": 80}
        tags = icon["tags"]          # ["serverless", "function", ...]
```

### 4. 使用预设样式

`index.json` 中的 `style_presets` 提供常用样式预设：

```python
# 获取冻结模型样式
frozen_style = index["style_presets"]["frozen_model"]["style"]
frozen_icon = index["style_presets"]["frozen_model"]["icon"]  # ❄
```

### 5. 配色方案

`index.json` 中的 `color_schemes` 提供标准配色：

```python
# 获取 Kubernetes 配色
k8s_colors = index["color_schemes"]["kubernetes"]
primary = k8s_colors["primary"]    # #326CE5
light = k8s_colors["light"]        # #E8EAF6
```

## 数据结构

### 图标定义

```json
{
  "id": "aws_lambda",
  "name": "Lambda",
  "name_cn": "Lambda 函数",
  "shape": "mxgraph.aws3.lambda_function",
  "fillColor": "#F58534",
  "size": {"width": 80, "height": 80},
  "tags": ["serverless", "function", "compute", "无服务器", "函数计算"]
}
```

### 形状定义

```json
{
  "id": "rounded_rectangle",
  "name": "Rounded Rectangle",
  "name_cn": "圆角矩形",
  "style": "rounded=1;whiteSpace=wrap;html=1;",
  "tags": ["basic", "rounded", "card", "圆角", "卡片"]
}
```

### 领域组件

```json
{
  "id": "frozen_model",
  "name": "Frozen Model",
  "name_cn": "冻结模型",
  "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#1565C0;...",
  "icon": "❄",
  "tags": ["model", "frozen", "pretrained", "冻结", "预训练"]
}
```

## 与语义检索集成

本知识库设计为与 `asset_search.py` 语义检索工具配合使用：

1. **构建索引**：解析 JSON 文件，提取 tags 和 name_cn
2. **语义匹配**：使用 sentence-transformers 进行向量匹配
3. **返回结果**：返回最相关的组件及其完整样式

## 扩展指南

### 添加新图标

1. 在对应 JSON 文件中添加图标定义
2. 确保包含 `id`, `name`, `name_cn`, `style/shape`, `tags`
3. 更新 `index.json` 中的 `quick_lookup` 映射

### 添加新领域

1. 在 `domain_assets.json` 中添加新领域
2. 定义 `components` 分类
3. 在 `index.json` 中添加对应的用例和关键词

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2025-01 | 初始版本，包含 300+ 组件 |

## 参考资源

- [DrawIO 官方文档](https://www.drawio.com/doc/)
- [mxGraph API](https://jgraph.github.io/mxgraph/docs/js-api/)
- [AWS 架构图标](https://aws.amazon.com/architecture/icons/)
- [Azure 图标](https://docs.microsoft.com/en-us/azure/architecture/icons/)
- [GCP 图标](https://cloud.google.com/icons)
- [Kubernetes 图标](https://github.com/kubernetes/community/tree/master/icons)
