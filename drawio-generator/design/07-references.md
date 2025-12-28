# 07: 参考文献汇总 (References)

## 一、核心技术文档

### 1.1 ELK (Eclipse Layout Kernel)

| 资源 | 链接 | 说明 |
|------|------|------|
| **ELK 官方文档** | https://eclipse.dev/elk/ | 完整的布局算法文档 |
| **ELK JSON 格式** | https://eclipse.dev/elk/documentation/tooldevelopers/graphdatastructure/jsonformat.html | 输入输出 JSON 规范 |
| **ELK 布局选项** | https://eclipse.dev/elk/reference/options.html | 所有布局参数详解 |
| **elkjs GitHub** | https://github.com/kieler/elkjs | JavaScript 版本 |
| **elkjs npm** | https://www.npmjs.com/package/elkjs | npm 包 |
| **ELK Live Demo** | https://rtsys.informatik.uni-kiel.de/elklive/ | 在线调试工具 |

### 1.2 DrawIO / mxGraph

| 资源 | 链接 | 说明 |
|------|------|------|
| **DrawIO 官方文档** | https://www.drawio.com/doc/ | 官方文档入口 |
| **XML 格式说明** | https://www.drawio.com/doc/faq/diagram-source-edit | XML 源码编辑 |
| **mxGraph API** | https://jgraph.github.io/mxgraph/docs/js-api/ | mxGraph JavaScript API |
| **mxConstants** | https://jgraph.github.io/mxgraph/docs/js-api/files/util/mxConstants-js.html | 样式常量定义 |
| **mxGraphLayout** | https://jgraph.github.io/mxgraph/docs/js-api/files/layout/mxGraphLayout-js.html | 布局 API |
| **DrawIO GitHub** | https://github.com/jgraph/drawio | 源代码 |
| **形状库格式** | https://www.drawio.com/doc/faq/shape-libraries | 自定义形状库 |

### 1.3 图标资源

| 资源 | 链接 | 说明 |
|------|------|------|
| **AWS 图标** | https://aws.amazon.com/architecture/icons/ | AWS 架构图标 |
| **Azure 图标** | https://docs.microsoft.com/en-us/azure/architecture/icons/ | Azure 架构图标 |
| **GCP 图标** | https://cloud.google.com/icons | Google Cloud 图标 |
| **Kubernetes 图标** | https://github.com/kubernetes/community/tree/master/icons | K8s 官方图标 |

---

## 二、布局算法理论

### 2.1 Sugiyama 算法

| 资源 | 说明 |
|------|------|
| Sugiyama, K., Tagawa, S., & Toda, M. (1981). Methods for visual understanding of hierarchical system structures. IEEE Transactions on Systems, Man, and Cybernetics, 11(2), 109-125. | 原始论文 |
| https://en.wikipedia.org/wiki/Layered_graph_drawing | 维基百科解释 |

**核心步骤**：
1. 层次分配 (Layer Assignment)
2. 交叉最小化 (Crossing Minimization)
3. 坐标分配 (Coordinate Assignment)

### 2.2 力导向算法

| 资源 | 说明 |
|------|------|
| Fruchterman, T. M., & Reingold, E. M. (1991). Graph drawing by force-directed placement. Software: Practice and experience, 21(11), 1129-1164. | FR 算法 |
| https://en.wikipedia.org/wiki/Force-directed_graph_drawing | 维基百科 |

### 2.3 正交路由算法

| 资源 | 说明 |
|------|------|
| Wybrow, M., Marriott, K., & Stuckey, P. J. (2010). Orthogonal connector routing. In Proceedings of the 18th international conference on Graph Drawing. | 正交连线路由 |
| https://github.com/adaptagrams/adaptagrams | libavoid 库 |

---

## 三、Python 库

### 3.1 图布局

| 库 | 链接 | 说明 |
|------|------|------|
| **grandalf** | https://github.com/bdcht/grandalf | Python 图布局，Sugiyama 算法 |
| **NetworkX** | https://networkx.org/ | 图论库（布局功能有限） |
| **pygraphviz** | https://pygraphviz.github.io/ | Graphviz 的 Python 绑定 |

### 3.2 XML 处理

| 库 | 链接 | 说明 |
|------|------|------|
| **xml.etree.ElementTree** | https://docs.python.org/3/library/xml.etree.elementtree.html | Python 标准库 |
| **lxml** | https://lxml.de/ | 高性能 XML 处理 |

### 3.3 语义搜索

| 库 | 链接 | 说明 |
|------|------|------|
| **sentence-transformers** | https://www.sbert.net/ | 文本嵌入模型 |
| **faiss** | https://github.com/facebookresearch/faiss | 向量搜索 |

---

## 四、Node.js 库

| 库 | 链接 | 说明 |
|------|------|------|
| **elkjs** | https://www.npmjs.com/package/elkjs | ELK JavaScript 版 |
| **dagre** | https://www.npmjs.com/package/dagre | 另一个布局库 |
| **cytoscape** | https://js.cytoscape.org/ | 图可视化库 |

---

## 五、相关工具

### 5.1 图表生成工具

| 工具 | 链接 | 说明 |
|------|------|------|
| **Mermaid** | https://mermaid.js.org/ | Markdown 风格图表 |
| **PlantUML** | https://plantuml.com/ | 文本转 UML |
| **Structurizr** | https://structurizr.com/ | C4 架构图 |
| **Diagrams (Python)** | https://diagrams.mingrammer.com/ | Python 代码生成架构图 |

### 5.2 在线工具

| 工具 | 链接 | 说明 |
|------|------|------|
| **DrawIO Online** | https://app.diagrams.net/ | 在线绘图 |
| **Excalidraw** | https://excalidraw.com/ | 手绘风格 |
| **Lucidchart** | https://www.lucidchart.com/ | 商业工具 |

---

## 六、AI 与图表生成

### 6.1 LLM 提示工程

| 资源 | 链接 | 说明 |
|------|------|------|
| **Anthropic Prompt Engineering** | https://docs.anthropic.com/claude/docs/prompt-engineering | Claude 提示工程 |
| **Chain-of-Thought** | https://arxiv.org/abs/2201.11903 | CoT 论文 |

### 6.2 相关项目

| 项目 | 说明 |
|------|------|
| GPT-4 Vision + Diagram | 使用视觉模型理解图表 |
| Claude Code Skills | 本项目所属的 Skill 框架 |

---

## 七、设计参考

### 7.1 本项目参考的方案

| 来源 | 关键洞察 |
|------|---------|
| **Gemini ELK 方案** | 递归 children 结构、Python-Node.js 桥接模式 |
| **之前的专家评审** | A* 路径规划、智能锚点选择、动态节点尺寸 |
| **DrawIO 官方** | mxGraph 布局 API、XML 格式规范 |

### 7.2 核心设计决策来源

| 决策 | 来源 |
|------|------|
| 选择 ELK.js | 工业级嵌套支持、正交路由内置 |
| 递归数据结构 | ELK JSON 格式、支持无限嵌套 |
| Python 桥接 Node.js | 简单可靠、无需常驻服务 |
| 分阶段工作流 | 职责分离、便于调试和迭代 |

---

## 八、版本要求

| 组件 | 最低版本 | 推荐版本 |
|------|---------|---------|
| Node.js | 16.0.0 | 20.x LTS |
| Python | 3.9 | 3.11+ |
| elkjs | 0.8.0 | 0.9.3 |
| grandalf | 0.7 | 0.8 |

---

## 九、更新日志

| 日期 | 更新内容 |
|------|---------|
| 2025-01 | 初始版本，基于 ELK.js 的完整方案 |

---

## 十、贡献者

- 设计文档由 Claude Code 生成
- 参考了 Gemini 的 ELK 方案设计
- 整合了多轮专家评审的结论
