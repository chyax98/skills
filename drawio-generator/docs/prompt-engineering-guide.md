# DrawIO 图表生成系统 Prompt Engineering 指南

> **版本**: 1.0
> **日期**: 2025-12-29
> **作者**: Prompt Engineering Expert
> **基于**: Anthropic Prompt Engineering Best Practices (2025)

## 目录

- [核心设计原则](#核心设计原则)
- [阶段 1: 意图理解 (Intent Understanding)](#阶段-1-意图理解-intent-understanding)
- [阶段 2: 规划 (Planning)](#阶段-2-规划-planning)
- [阶段 3: 布局评审 (Layout Review)](#阶段-3-布局评审-layout-review)
- [阶段 4: XML 验证 (XML Validation)](#阶段-4-xml-验证-xml-validation)
- [Prompt 设计原则总结](#prompt-设计原则总结)
- [参考文献](#参考文献)

---

## 核心设计原则

基于 Anthropic 2025 年最新的 Prompt Engineering 指南，本文档遵循以下核心原则：

### 1. 明确性优于含糊性 (Explicit > Implicit)

**原则**: 直接告诉模型你要看到的内容，不要假设它能猜出你的意图。

- ✅ 使用直接的动词开头："提取"、"生成"、"分析"、"评审"
- ✅ 描述期望的最终结果
- ✅ 明确质量、深度、细节的期待
- ❌ 避免模糊指令如"处理这个需求"

### 2. 提供背景与动机 (Context & Motivation)

**原则**: 解释"为什么"某件事重要，帮助 AI 理解目标。

- ✅ 说明成果用于什么场景
- ✅ 阐明限制的原因
- ✅ 声明受众是谁
- ✅ 说明要解决的问题

### 3. 结构化输出控制 (Structured Output)

**原则**: 使用示例、模板、预填充来确保格式一致性。

- ✅ 提供输出格式的 JSON Schema 或模板
- ✅ 使用 Few-shot 示例展示期望格式
- ✅ 对于复杂格式，使用预填充技术
- ❌ 避免仅用文字描述复杂格式

### 4. Chain of Thought 策略选择

**原则**: 根据任务复杂度选择合适的 CoT 策略。

| 任务类型 | CoT 策略 | 何时使用 |
|---------|---------|---------|
| 简单提取 | 无需 CoT | 节点数 < 10，结构简单 |
| 中等复杂度 | 基础 CoT | 节点数 10-30，需要推理连接关系 |
| 高复杂度 | 结构化 CoT | 节点数 > 30，需要分层规划 |
| 评审任务 | 引导式 CoT | 需要多维度评估 |

### 5. 允许表达不确定性 (Uncertainty Handling)

**原则**: 明确允许模型在信息不足时表达"不确定"，减少幻觉。

- ✅ "如果用户描述不明确，请列出可能的解释并要求确认"
- ✅ "当节点类型无法确定时，使用 'default' 并注明理由"
- ❌ "必须推断出所有节点类型"（会导致幻觉）

---

## 阶段 1: 意图理解 (Intent Understanding)

### 任务描述

将用户的自然语言描述（可能模糊、不完整）转换为结构化的需求理解。

### 系统提示 (System Prompt)

```markdown
你是 DrawIO 图表生成系统的意图理解专家。你的任务是分析用户对图表的描述，
提取关键信息并输出结构化的需求理解。

**核心职责**:
1. 识别图表类型（flowchart、architecture、uml、er、network、mindmap）
2. 提取节点列表（实体、组件、步骤等）
3. 推断节点之间的连接关系
4. 识别布局偏好（水平、垂直、辐射、网格等）
5. 理解用户对样式的期待（专业、技术风格、简洁、多彩等）

**重要原则**:
- 当信息不明确时，基于图表类型使用合理默认值，但必须在输出中注明"推断依据"
- 如果用户描述存在歧义，列出可能的解释
- 优先保证节点连接的逻辑性，而非追求节点数量
```

### 任务指令 (Task Instruction)

```markdown
分析以下用户描述，输出结构化的需求理解。

**用户描述**:
{user_input}

**输出要求**:
1. 图表类型识别：从 flowchart、architecture、uml、er、network、mindmap 中选择
2. 节点列表：每个节点包含 id（唯一标识）、label（显示文字）、type（节点类型）
3. 连接关系：每条边包含 source、target、可选的 label
4. 布局偏好：horizontal、vertical、radial、grid 或 auto
5. 主题偏好：professional、tech、minimal、colorful、dark

**推理过程** (Chain of Thought):
在输出最终结果前，请先在 <thinking> 标签中分析：
- 用户描述的核心意图是什么？
- 哪些信息是明确的？哪些需要推断？
- 节点之间的连接关系是什么？
- 推荐什么样的布局和主题？

然后在 <output> 标签中给出最终的结构化输出。
```

### 输出格式

```json
{
  "diagram_type": "architecture",
  "title": "微服务架构图",
  "nodes": [
    {
      "id": "gateway",
      "label": "API Gateway",
      "type": "gateway",
      "inferred": false
    },
    {
      "id": "auth_service",
      "label": "认证服务",
      "type": "service",
      "inferred": true,
      "inference_reason": "用户提到'认证'，推断为独立服务"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "gateway",
      "target": "auth_service",
      "label": "验证请求",
      "type": "arrow"
    }
  ],
  "layout_hint": "vertical",
  "theme": "professional",
  "confidence": {
    "diagram_type": "high",
    "nodes": "medium",
    "edges": "high",
    "layout": "medium"
  },
  "clarifications_needed": [
    "认证服务是使用 OAuth2 还是 JWT？（不影响图表结构，但可能影响标注）"
  ]
}
```

### Few-shot 示例

#### 示例 1: 明确描述

**用户输入**:
```
画一个用户登录流程图：
1. 用户打开登录页
2. 输入账号密码
3. 系统验证
4. 如果成功跳转首页，失败显示错误
```

**输出**:
```json
{
  "diagram_type": "flowchart",
  "title": "用户登录流程",
  "nodes": [
    {"id": "start", "label": "开始", "type": "start", "inferred": false},
    {"id": "login_page", "label": "打开登录页", "type": "process", "inferred": false},
    {"id": "input", "label": "输入账号密码", "type": "process", "inferred": false},
    {"id": "verify", "label": "系统验证", "type": "decision", "inferred": false},
    {"id": "success", "label": "跳转首页", "type": "process", "inferred": false},
    {"id": "error", "label": "显示错误", "type": "process", "inferred": false},
    {"id": "end", "label": "结束", "type": "end", "inferred": false}
  ],
  "edges": [
    {"id": "e1", "source": "start", "target": "login_page", "type": "arrow"},
    {"id": "e2", "source": "login_page", "target": "input", "type": "arrow"},
    {"id": "e3", "source": "input", "target": "verify", "type": "arrow"},
    {"id": "e4", "source": "verify", "target": "success", "label": "成功", "type": "arrow"},
    {"id": "e5", "source": "verify", "target": "error", "label": "失败", "type": "arrow"}
  ],
  "layout_hint": "vertical",
  "theme": "professional",
  "confidence": {
    "diagram_type": "high",
    "nodes": "high",
    "edges": "high",
    "layout": "high"
  },
  "clarifications_needed": []
}
```

#### 示例 2: 模糊描述

**用户输入**:
```
我想画个系统架构，有前端、后端、数据库，还有个缓存
```

**输出**:
```json
{
  "diagram_type": "architecture",
  "title": "系统架构图",
  "nodes": [
    {"id": "frontend", "label": "前端", "type": "client", "inferred": false},
    {"id": "backend", "label": "后端服务", "type": "service", "inferred": false},
    {"id": "database", "label": "数据库", "type": "database", "inferred": false},
    {"id": "cache", "label": "缓存", "type": "cache", "inferred": false}
  ],
  "edges": [
    {
      "id": "e1",
      "source": "frontend",
      "target": "backend",
      "type": "arrow",
      "inferred": true,
      "inference_reason": "典型的前后端分离架构"
    },
    {
      "id": "e2",
      "source": "backend",
      "target": "cache",
      "type": "arrow",
      "inferred": true,
      "inference_reason": "后端通常先查缓存"
    },
    {
      "id": "e3",
      "source": "backend",
      "target": "database",
      "type": "arrow",
      "inferred": true,
      "inference_reason": "缓存未命中时访问数据库"
    }
  ],
  "layout_hint": "vertical",
  "theme": "tech",
  "confidence": {
    "diagram_type": "high",
    "nodes": "high",
    "edges": "medium",
    "layout": "medium"
  },
  "clarifications_needed": [
    "是否需要负载均衡器？",
    "数据库是否有主从复制？",
    "缓存类型是 Redis 还是 Memcached？"
  ]
}
```

---

## 阶段 2: 规划 (Planning)

### 任务描述

基于需求理解结果，生成完整的 DiagramSpec JSON，包含所有节点、边、布局提示、主题等信息。

### 系统提示 (System Prompt)

```markdown
你是 DrawIO 图表生成系统的规划专家。你的任务是将需求理解结果转换为完整的
DiagramSpec JSON，确保图表具有良好的可视化效果。

**核心职责**:
1. 验证并完善节点定义（确保 id 唯一、type 正确、label 清晰）
2. 规划节点连接关系（确保逻辑正确、避免循环、合理分组）
3. 选择最佳布局策略（基于图表类型和节点数量）
4. 确定节点类型到视觉样式的映射
5. 预判布局挑战（如节点重叠、连线交叉等）

**节点类型参考**:
- 架构图: gateway, service, microservice, api, database, cache, queue, loadbalancer, firewall
- 用户/客户端: user, client, browser, mobile, app
- 流程图: start, end, process, decision, condition, document, data
- 网络: server, router, switch, cloud

**布局策略**:
- horizontal: 适用于流程图、时间线（节点数 < 15）
- vertical/layered: 适用于架构图、依赖关系（节点数 10-50）
- radial: 适用于中心辐射型、网络拓扑（节点数 < 20）
- grid: 适用于分类展示、ER图（节点数较多且无明显层级）

**主题选择**:
- professional: 企业文档、正式报告
- tech: 技术分享、开发文档（带渐变、阴影）
- minimal: 简洁演示、教学材料
- colorful: 营销材料、信息图表
- dark: 深色模式、技术演示
```

### 任务指令 (Task Instruction)

```markdown
基于以下需求理解结果，生成完整的 DiagramSpec JSON。

**输入**:
{requirement_analysis}

**输出要求**:
1. 验证所有节点 id 唯一性
2. 补充任何缺失的节点（如 start/end 节点）
3. 优化节点 type，确保与形状库匹配
4. 检查边的连接关系，避免逻辑错误
5. 根据节点数量和类型选择最佳布局算法
6. 添加分组信息（如果适用）

**推理过程** (Structured CoT):
请按照以下步骤思考：

<step1_node_analysis>
分析节点列表：
- 总数: ?
- 是否需要补充节点（如 start/end）?
- 节点类型是否正确映射?
</step1_node_analysis>

<step2_edge_validation>
验证连接关系：
- 是否有孤立节点?
- 是否有循环依赖?
- 连接逻辑是否清晰?
</step2_edge_validation>

<step3_layout_selection>
选择布局策略：
- 图表类型: ?
- 节点数量: ?
- 是否有明显的层级关系?
- 推荐布局: ?
- 推荐理由: ?
</step3_layout_selection>

<step4_optimization>
优化建议：
- 是否需要分组?
- 预判的布局挑战: ?
- 建议的解决方案: ?
</step4_optimization>

<final_spec>
最终 DiagramSpec JSON
</final_spec>
```

### 输出格式

```json
{
  "diagram_type": "architecture",
  "title": "微服务架构图",
  "nodes": [
    {
      "id": "gateway",
      "label": "API Gateway",
      "type": "gateway",
      "group": null
    },
    {
      "id": "auth_service",
      "label": "认证服务",
      "type": "service",
      "group": "services"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "gateway",
      "target": "auth_service",
      "label": "验证请求",
      "type": "arrow"
    }
  ],
  "groups": [
    {
      "id": "services",
      "label": "微服务集群",
      "style": "dashed_container"
    }
  ],
  "layout_hint": "vertical",
  "layout_rationale": "架构图通常采用分层布局，从上到下展示请求流向",
  "theme": "professional",
  "custom_styles": {
    "gateway": {
      "fillColor": "#d5e8d4",
      "strokeColor": "#82b366"
    }
  },
  "metadata": {
    "node_count": 8,
    "edge_count": 12,
    "estimated_canvas": "1000x750",
    "complexity": "medium"
  }
}
```

### Few-shot 示例

#### 示例 1: 流程图规划

**输入** (需求理解结果):
```json
{
  "diagram_type": "flowchart",
  "nodes": [
    {"id": "input", "label": "输入数据", "type": "process"},
    {"id": "validate", "label": "验证", "type": "decision"},
    {"id": "save", "label": "保存", "type": "process"}
  ],
  "edges": [
    {"source": "input", "target": "validate"},
    {"source": "validate", "target": "save", "label": "有效"}
  ]
}
```

**输出**:
```json
{
  "diagram_type": "flowchart",
  "title": "数据验证流程",
  "nodes": [
    {"id": "start", "label": "开始", "type": "start"},
    {"id": "input", "label": "输入数据", "type": "process"},
    {"id": "validate", "label": "数据有效?", "type": "decision"},
    {"id": "save", "label": "保存数据", "type": "process"},
    {"id": "error", "label": "显示错误", "type": "process"},
    {"id": "end", "label": "结束", "type": "end"}
  ],
  "edges": [
    {"id": "e1", "source": "start", "target": "input", "type": "arrow"},
    {"id": "e2", "source": "input", "target": "validate", "type": "arrow"},
    {"id": "e3", "source": "validate", "target": "save", "label": "有效", "type": "arrow"},
    {"id": "e4", "source": "validate", "target": "error", "label": "无效", "type": "arrow"},
    {"id": "e5", "source": "save", "target": "end", "type": "arrow"},
    {"id": "e6", "source": "error", "target": "end", "type": "arrow"}
  ],
  "layout_hint": "vertical",
  "layout_rationale": "流程图从上到下展示流程步骤，decision 节点向两侧分支",
  "theme": "professional",
  "metadata": {
    "node_count": 6,
    "edge_count": 6,
    "estimated_canvas": "800x600",
    "complexity": "low",
    "补充说明": "添加了 start、end、error 节点使流程完整"
  }
}
```

---

## 阶段 3: 布局评审 (Layout Review)

### 任务描述

评审布局工具的输出，识别布局问题（重叠、交叉、间距不合理），并给出微调建议。

### 系统提示 (System Prompt)

```markdown
你是 DrawIO 图表生成系统的布局评审专家。你的任务是评估自动布局结果的质量，
识别潜在问题，并提供改进建议。

**评审维度**:
1. 节点间距：是否符合最小间距要求（120px）
2. 节点重叠：是否有节点位置重叠
3. 连线交叉：连线是否会穿过其他节点
4. 画布利用率：节点分布是否合理
5. 视觉平衡：布局是否美观、对称
6. 逻辑流向：连线方向是否符合阅读习惯

**评分标准**:
- A (90-100): 优秀，无需修改
- B (75-89): 良好，有小问题但可接受
- C (60-74): 一般，建议优化
- D (0-59): 较差，必须修正

**硬性约束**:
- 节点间距: >= 120px
- 画布边界: margin >= 40px
- 节点尺寸: 符合 S(80x40)、M(120x60)、L(160x80)
- 网格对齐: 所有坐标是 10 的倍数
```

### 任务指令 (Task Instruction)

```markdown
评审以下布局结果，给出评分和改进建议。

**输入**:
- DiagramSpec: {spec}
- LayoutResult: {layout}

**评审流程** (Guided CoT):

<dimension1_spacing>
检查节点间距：
- 计算相邻节点的最小距离
- 标记间距 < 120px 的节点对
- 评分: ?/100
</dimension1_spacing>

<dimension2_overlap>
检查节点重叠：
- 是否有节点边界框重叠?
- 列出重叠的节点对
- 评分: ?/100
</dimension2_overlap>

<dimension3_edge_crossing>
检查连线交叉：
- 哪些连线会穿过其他节点?
- 是否需要添加 waypoints?
- 评分: ?/100
</dimension3_edge_crossing>

<dimension4_canvas_usage>
检查画布利用率：
- 节点分布是否均匀?
- 是否有大片空白区域?
- 是否超出画布范围?
- 评分: ?/100
</dimension4_canvas_usage>

<dimension5_visual_balance>
检查视觉平衡：
- 布局是否对称?
- 是否符合图表类型的惯例?
- 评分: ?/100
</dimension5_visual_balance>

<dimension6_flow_logic>
检查逻辑流向：
- 连线方向是否符合阅读习惯（从左到右、从上到下）?
- 是否有反向连线造成困惑?
- 评分: ?/100
</dimension6_flow_logic>

<overall_assessment>
总体评估：
- 综合评分: ?/100 (等级: A/B/C/D)
- 主要问题: ?
- 是否需要重新布局: 是/否
</overall_assessment>

<recommendations>
改进建议（优先级排序）：
1. [高优先级] ...
2. [中优先级] ...
3. [低优先级] ...
</recommendations>
```

### 输出格式

```json
{
  "overall_score": 78,
  "grade": "B",
  "dimensions": {
    "spacing": {"score": 85, "issues": ["节点 'db1' 和 'db2' 间距仅 100px"]},
    "overlap": {"score": 100, "issues": []},
    "edge_crossing": {"score": 60, "issues": ["连线 e3 穿过节点 'cache'"]},
    "canvas_usage": {"score": 75, "issues": ["右侧有较大空白"]},
    "visual_balance": {"score": 80, "issues": ["底层节点分布不均"]},
    "flow_logic": {"score": 90, "issues": []}
  },
  "critical_issues": [
    {
      "type": "edge_crossing",
      "description": "连线 e3 (service1 -> db1) 穿过节点 'cache'",
      "severity": "high",
      "suggested_fix": "为连线 e3 添加 waypoint: [{x: 300, y: 200}]"
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "action": "增加节点 'db1' 和 'db2' 之间的水平间距至 140px",
      "rationale": "当前间距 100px 低于最小要求 120px",
      "affected_nodes": ["db1", "db2"]
    },
    {
      "priority": "medium",
      "action": "调整连线 e3 的路径，添加 waypoint 绕过 'cache' 节点",
      "rationale": "避免连线穿过节点，提高图表可读性",
      "affected_edges": ["e3"]
    }
  ],
  "needs_relayout": false,
  "estimated_fix_effort": "low"
}
```

### Few-shot 示例

#### 示例 1: 发现连线交叉问题

**输入**:
```json
{
  "spec": {
    "nodes": [
      {"id": "a", "label": "A"},
      {"id": "b", "label": "B"},
      {"id": "c", "label": "C"}
    ],
    "edges": [
      {"id": "e1", "source": "a", "target": "c"}
    ]
  },
  "layout": {
    "nodes": [
      {"id": "a", "x": 100, "y": 100, "width": 120, "height": 60},
      {"id": "b", "x": 300, "y": 100, "width": 120, "height": 60},
      {"id": "c", "x": 500, "y": 100, "width": 120, "height": 60}
    ],
    "edges": [
      {"id": "e1", "source": "a", "target": "c", "waypoints": []}
    ]
  }
}
```

**输出**:
```json
{
  "overall_score": 65,
  "grade": "C",
  "dimensions": {
    "spacing": {"score": 100, "issues": []},
    "overlap": {"score": 100, "issues": []},
    "edge_crossing": {
      "score": 0,
      "issues": ["连线 e1 (a -> c) 穿过节点 b，因为三个节点在同一水平线上"]
    },
    "canvas_usage": {"score": 90, "issues": []},
    "visual_balance": {"score": 95, "issues": []},
    "flow_logic": {"score": 100, "issues": []}
  },
  "critical_issues": [
    {
      "type": "edge_crossing",
      "description": "连线 e1 从 a(100,100) 到 c(500,100) 会穿过 b(300,100)",
      "severity": "high",
      "suggested_fix": "添加 waypoint: [{x: 300, y: 50}] 或 [{x: 300, y: 150}] 使连线绕过 b"
    }
  ],
  "recommendations": [
    {
      "priority": "high",
      "action": "为连线 e1 添加 waypoint: {x: 300, y: 50}",
      "rationale": "从上方绕过节点 b，保持水平方向的主要流向",
      "affected_edges": ["e1"],
      "estimated_improvement": "+35 分"
    }
  ],
  "needs_relayout": false,
  "estimated_fix_effort": "low"
}
```

---

## 阶段 4: XML 验证 (XML Validation)

### 任务描述

分析 XML 验证报告，决定如何修复错误：重新生成、局部修正、调整参数等。

### 系统提示 (System Prompt)

```markdown
你是 DrawIO 图表生成系统的 XML 验证专家。你的任务是分析 XML 验证错误，
判断错误类型和严重程度，并决定最佳修复策略。

**错误分类**:
1. 结构性错误：XML 格式不符合规范（缺少必需属性、标签嵌套错误等）
2. 几何错误：节点位置/尺寸超出画布、重叠等
3. 引用错误：连线引用不存在的节点 ID
4. 样式错误：样式字符串格式错误
5. 语义错误：逻辑上不合理但语法正确

**修复策略**:
- 轻微错误 (score > 80): 局部修正（修改单个属性）
- 中等错误 (score 60-80): 部分重生成（重新生成问题节点/连线）
- 严重错误 (score < 60): 完全重新生成
- 布局问题: 调用布局工具重新计算
- 样式问题: 调用样式匹配工具

**重试限制**:
- 最多 3 轮迭代
- 每轮必须有明确的改进方向
- 第 3 轮后如仍失败，降级到简化版本
```

### 任务指令 (Task Instruction)

```markdown
分析以下 XML 验证报告，制定修复计划。

**输入**:
- 验证报告: {validation_report}
- 生成参数: {generation_params}
- 当前迭代次数: {iteration_count}

**分析流程** (Structured CoT):

<step1_error_classification>
错误分类：
- 结构性错误: 列出所有
- 几何错误: 列出所有
- 引用错误: 列出所有
- 样式错误: 列出所有
- 语义错误: 列出所有
</step1_error_classification>

<step2_severity_assessment>
严重性评估：
- 致命错误（阻止渲染）: ?
- 严重错误（影响功能）: ?
- 一般错误（影响美观）: ?
- 轻微警告: ?
</step2_severity_assessment>

<step3_root_cause>
根因分析：
- 是布局算法的问题？
- 是样式生成的问题？
- 是 XML 生成逻辑的问题？
- 是输入数据的问题？
</step3_root_cause>

<step4_strategy_selection>
修复策略选择：
- 如果是布局问题 → 调整布局参数并重新布局
- 如果是样式问题 → 重新匹配样式
- 如果是结构问题 → 修正 XML 生成逻辑
- 如果是数据问题 → 返回规划阶段
</step4_strategy_selection>

<step5_fix_plan>
具体修复计划：
1. 修复动作: ?
2. 修复范围: 完全重生成 / 部分重生成 / 局部修正
3. 调整参数: ?
4. 预期改进: ?
</step5_fix_plan>

<step6_retry_decision>
重试决策：
- 是否重试: 是/否
- 重试策略: ?
- 如果第 3 轮仍失败: 降级方案
</step6_retry_decision>
```

### 输出格式

```json
{
  "error_summary": {
    "total_errors": 5,
    "total_warnings": 2,
    "critical_count": 1,
    "severity_distribution": {
      "critical": 1,
      "high": 2,
      "medium": 2,
      "low": 2
    }
  },
  "error_classification": {
    "structural": [
      {
        "type": "missing_attribute",
        "description": "mxCell id='5' 缺少 'as' 属性在 mxGeometry 标签中",
        "severity": "critical",
        "location": "line 45"
      }
    ],
    "geometric": [
      {
        "type": "node_overlap",
        "description": "节点 'db1' (x=300) 与 'cache' (x=310) 重叠",
        "severity": "high",
        "affected_elements": ["db1", "cache"]
      }
    ],
    "reference": [],
    "style": [
      {
        "type": "invalid_style_property",
        "description": "节点 'gateway' 的样式包含未知属性 'shadowColor'",
        "severity": "low",
        "affected_elements": ["gateway"]
      }
    ],
    "semantic": []
  },
  "root_cause_analysis": {
    "primary_cause": "layout_algorithm",
    "explanation": "布局算法未检测到节点重叠，间距计算有误",
    "contributing_factors": [
      "节点数量较多（35 个）",
      "使用了 grid 布局但图表更适合 layered 布局"
    ]
  },
  "fix_strategy": {
    "approach": "partial_regenerate",
    "scope": "layout_only",
    "steps": [
      {
        "step": 1,
        "action": "修正结构性错误（添加缺失的 'as' 属性）",
        "method": "direct_edit",
        "estimated_time": "immediate"
      },
      {
        "step": 2,
        "action": "重新运行布局算法",
        "method": "call_layout_agent",
        "parameters": {
          "algorithm": "layered",
          "spacing": 140,
          "force_no_overlap": true
        }
      },
      {
        "step": 3,
        "action": "移除无效的样式属性",
        "method": "style_cleanup",
        "affected_nodes": ["gateway"]
      }
    ]
  },
  "retry_decision": {
    "should_retry": true,
    "retry_count": 1,
    "max_retries": 3,
    "retry_strategy": "incremental_fix",
    "fallback_plan": "如果第 3 轮仍失败，简化图表：移除非关键节点，减少连线交叉",
    "estimated_success_rate": 0.85
  },
  "expected_improvement": {
    "before_score": 45,
    "after_score": 85,
    "improvement": "+40",
    "remaining_issues": "可能仍有轻微的样式警告，但不影响功能"
  }
}
```

### Few-shot 示例

#### 示例 1: 结构性错误修复

**输入**:
```json
{
  "validation_report": {
    "valid": false,
    "errors": [
      {
        "type": "missing_attribute",
        "message": "mxCell id='3' 的 mxGeometry 缺少 'as' 属性",
        "severity": "critical"
      },
      {
        "type": "invalid_attribute",
        "message": "mxCell id='5' 的 'relative' 属性值应为 '1' 而非 'true'",
        "severity": "high"
      }
    ],
    "warnings": []
  },
  "iteration_count": 1
}
```

**输出**:
```json
{
  "error_summary": {
    "total_errors": 2,
    "total_warnings": 0,
    "critical_count": 1,
    "severity_distribution": {"critical": 1, "high": 1}
  },
  "error_classification": {
    "structural": [
      {
        "type": "missing_attribute",
        "description": "mxGeometry 缺少必需的 'as=\"geometry\"' 属性",
        "severity": "critical",
        "location": "mxCell id='3'"
      },
      {
        "type": "invalid_attribute_value",
        "description": "relative 属性应为数值 '1' 而非布尔值 'true'",
        "severity": "high",
        "location": "mxCell id='5'"
      }
    ]
  },
  "root_cause_analysis": {
    "primary_cause": "xml_generation_logic",
    "explanation": "XML 生成器未正确处理属性值类型转换",
    "contributing_factors": ["Python 布尔值 True 未转换为字符串 '1'"]
  },
  "fix_strategy": {
    "approach": "direct_edit",
    "scope": "specific_attributes",
    "steps": [
      {
        "step": 1,
        "action": "为所有 mxGeometry 标签添加 'as=\"geometry\"' 属性",
        "method": "regex_replace",
        "pattern": "<mxGeometry(?! as=)",
        "replacement": "<mxGeometry as=\"geometry\""
      },
      {
        "step": 2,
        "action": "将所有 'relative=\"true\"' 替换为 'relative=\"1\"'",
        "method": "string_replace"
      }
    ]
  },
  "retry_decision": {
    "should_retry": true,
    "retry_count": 1,
    "max_retries": 3,
    "retry_strategy": "apply_fixes_and_revalidate",
    "estimated_success_rate": 0.95
  },
  "expected_improvement": {
    "before_score": 0,
    "after_score": 100,
    "improvement": "+100",
    "remaining_issues": "无"
  }
}
```

#### 示例 2: 布局问题需要重新规划

**输入**:
```json
{
  "validation_report": {
    "valid": true,
    "errors": [],
    "warnings": [
      {"type": "poor_layout", "message": "50% 的连线存在交叉"}
    ],
    "layout_quality_score": 35
  },
  "iteration_count": 2
}
```

**输出**:
```json
{
  "error_summary": {
    "total_errors": 0,
    "total_warnings": 1,
    "critical_count": 0,
    "severity_distribution": {"medium": 1}
  },
  "root_cause_analysis": {
    "primary_cause": "layout_algorithm_selection",
    "explanation": "当前使用的 'grid' 布局不适合有向图，导致大量连线交叉",
    "contributing_factors": [
      "图表类型为 'architecture'，应使用 'layered' 布局",
      "节点之间有明显的层级关系"
    ]
  },
  "fix_strategy": {
    "approach": "complete_regenerate",
    "scope": "layout_phase",
    "steps": [
      {
        "step": 1,
        "action": "返回规划阶段，修改 layout_hint 为 'layered'",
        "method": "update_spec",
        "changes": {"layout_hint": "layered"}
      },
      {
        "step": 2,
        "action": "使用 Grandalf Sugiyama 算法重新布局",
        "method": "call_layout_agent",
        "parameters": {"algorithm": "layered", "spacing": 150}
      },
      {
        "step": 3,
        "action": "重新生成 XML",
        "method": "call_generator_agent"
      }
    ]
  },
  "retry_decision": {
    "should_retry": true,
    "retry_count": 2,
    "max_retries": 3,
    "retry_strategy": "change_layout_algorithm",
    "fallback_plan": "如果 layered 布局仍不理想，使用 radial 布局并手动调整关键节点位置",
    "estimated_success_rate": 0.80
  },
  "expected_improvement": {
    "before_score": 35,
    "after_score": 75,
    "improvement": "+40",
    "remaining_issues": "可能仍有少量连线交叉，需人工微调"
  }
}
```

---

## Prompt 设计原则总结

### 1. 明确性原则

| 维度 | 实践 |
|------|------|
| 任务描述 | 使用动作动词："提取"、"生成"、"评审"、"修复" |
| 输出格式 | 提供 JSON Schema 或模板 |
| 质量标准 | 明确评分标准、可接受阈值 |
| 边界条件 | 说明何时允许"不确定"、何时必须推断 |

### 2. 上下文原则

| 维度 | 实践 |
|------|------|
| 背景信息 | 说明任务在整个系统中的位置 |
| 动机解释 | 解释为什么需要某个约束 |
| 受众说明 | 明确输出将被谁使用（下游工具、人类用户） |
| 场景描述 | 提供典型用例 |

### 3. 结构化输出原则

| 方法 | 适用场景 | 实现方式 |
|------|---------|---------|
| JSON Schema | 严格的数据结构 | 提供完整的 schema 定义 |
| Few-shot 示例 | 复杂格式、微妙的风格 | 提供 1-3 个完整示例 |
| 预填充 | 强制特定开头 | 在 assistant 消息中预填开头 |
| 标签分隔 | 多段输出 | 使用 `<thinking>` `<output>` 等 |

### 4. Chain of Thought 原则

| CoT 类型 | 适用任务 | 复杂度 |
|---------|---------|--------|
| 基础 CoT | 简单推理、单步分析 | 低 |
| 引导式 CoT | 多步骤、有固定流程 | 中 |
| 结构化 CoT | 复杂决策、需要审查推理 | 高 |
| Extended Thinking | 极复杂、开放式问题 | 极高 |

**选择建议**:
- 节点数 < 10: 无需 CoT
- 节点数 10-30: 基础 CoT
- 节点数 > 30: 结构化 CoT
- 评审任务: 引导式 CoT（分维度评估）

### 5. 错误处理原则

| 场景 | 策略 |
|------|------|
| 输入不完整 | 允许推断，但必须标记 `inferred: true` 和理由 |
| 输入歧义 | 列出可能解释，要求澄清 |
| 任务失败 | 提供降级方案、简化版本 |
| 迭代上限 | 明确告知用户，建议人工介入 |

### 6. 提示词优化清单

在发布 Prompt 前，检查以下各项：

- [ ] 是否明确指定了输出格式？
- [ ] 是否提供了 1-2 个 Few-shot 示例？
- [ ] 是否说明了任务的背景和动机？
- [ ] 是否允许模型表达不确定性？
- [ ] 是否使用了合适的 CoT 策略？
- [ ] 是否定义了评分标准（如果需要评估）？
- [ ] 是否处理了边界情况（空输入、极端值）？
- [ ] 是否避免了过时的技巧（过度的 XML 标签、角色扮演）？

---

## 参考文献

### 官方文档

1. **Anthropic Prompt Engineering Guide (2025)**
   - URL: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
   - 核心内容: Be explicit, Provide context, Use examples, Chain of thought
   - 关键更新: Extended thinking, Prefill 技术, Structured outputs

2. **Anthropic 中文实践指南 (2025-11)**
   - URL: https://datacanvas.csdn.net/692559772087ae0db79c9127.html
   - 核心内容: 提示词工程常见错误、技巧选择决策树
   - 关键要点: "从简单开始，逐步增加复杂度"

3. **OpenAI Prompt Engineering Best Practices**
   - URL: https://platform.openai.com/docs/guides/prompt-engineering
   - 核心内容: Write clear instructions, Provide reference text, Split complex tasks
   - 关键技巧: Few-shot prompting, System message design

### 学术论文

4. **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models**
   - 作者: Wei et al. (Google Research, 2022)
   - 核心发现: 在提示词中加入推理步骤可显著提升复杂任务表现
   - 应用: 本文档的结构化 CoT 设计

5. **Large Language Models are Zero-Shot Reasoners**
   - 作者: Kojima et al. (2022)
   - 核心发现: 简单添加"Let's think step by step"即可激活推理能力
   - 应用: 基础 CoT 的理论基础

### 技术博客

6. **Lilian Weng's Blog - Prompt Engineering**
   - URL: https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
   - 核心内容: Prompt engineering, adversarial attacks on LLMs
   - 关键技巧: Self-consistency, Tree of thoughts

7. **Brex's Prompt Engineering Guide**
   - URL: https://github.com/brexhq/prompt-engineering
   - 核心内容: 企业级 Prompt 工程实践
   - 关键要点: 测试驱动的 Prompt 开发、版本控制

### 工具与规范

8. **JSON Schema 规范**
   - URL: https://json-schema.org/
   - 用途: 定义结构化输出格式

9. **DrawIO mxGraph XML 规范**
   - URL: https://jgraph.github.io/mxgraph/docs/js-api/files/model/mxCell-js.html
   - 用途: 验证生成 XML 的正确性

### 实践案例

10. **LangChain Prompt Templates**
    - URL: https://python.langchain.com/docs/modules/model_io/prompts/
    - 核心内容: Prompt 模板设计模式
    - 关键模式: ChatPromptTemplate, FewShotPromptTemplate

11. **Guidance (Microsoft)**
    - URL: https://github.com/microsoft/guidance
    - 核心内容: 结构化 Prompt 控制
    - 关键技巧: 模板语法、输出约束

---

## 附录: Prompt 模板快速参考

### A. 意图理解模板（简化版）

```markdown
分析用户描述，输出 DiagramSpec JSON。

用户描述: {user_input}

输出格式: {"diagram_type": "...", "nodes": [...], "edges": [...]}

如果信息不明确，在 "clarifications_needed" 字段列出问题。
```

### B. 规划模板（简化版）

```markdown
基于以下需求，生成完整的 DiagramSpec:
{requirement}

验证:
1. 所有节点 id 唯一
2. 所有边引用的节点存在
3. 布局算法适合图表类型

输出完整的 JSON。
```

### C. 布局评审模板（简化版）

```markdown
评审布局质量，给出评分（0-100）和改进建议。

输入:
- Spec: {spec}
- Layout: {layout}

评审维度: 间距、重叠、连线交叉、画布利用、视觉平衡、逻辑流向

输出格式: {"overall_score": ?, "recommendations": [...]}
```

### D. 验证修复模板（简化版）

```markdown
分析验证报告，制定修复计划。

报告: {validation_report}
迭代次数: {iteration}

分析:
1. 错误分类
2. 根因分析
3. 修复策略（完全重生成/部分重生成/局部修正）

如果迭代次数 >= 3，提供降级方案。
```

---

## 结论

本文档为 DrawIO 图表生成系统的四个关键阶段设计了专业的 Prompt 模板，遵循 Anthropic 2025 年的最新最佳实践：

### 核心要点

1. **明确性 > 含糊性**: 所有 Prompt 都使用直接、清晰的指令，避免让模型猜测意图。

2. **提供充分背景**: 每个阶段的 Prompt 都说明了任务在整个系统中的位置和重要性。

3. **结构化输出**: 通过 JSON Schema、Few-shot 示例、预填充等技术确保输出格式一致。

4. **适度使用 CoT**:
   - 意图理解: 基础 CoT（简单推理）
   - 规划: 结构化 CoT（多步骤规划）
   - 布局评审: 引导式 CoT（分维度评估）
   - XML 验证: 结构化 CoT（复杂决策）

5. **错误处理**: 所有阶段都允许模型表达不确定性，并提供降级方案。

### 关键创新

- **推断标记**: 在意图理解阶段，所有推断的信息都标记 `inferred: true` 和理由
- **置信度评分**: 输出包含各维度的置信度，帮助下游决策
- **迭代控制**: 在验证阶段明确最多 3 轮迭代，避免无限循环
- **降级策略**: 当复杂方案失败时，提供简化版本

### 实施建议

1. **从简单开始**: 先使用简化版模板，验证基本功能
2. **逐步增强**: 根据实际问题逐步加入 CoT、Few-shot 示例
3. **持续测试**: 对每个 Prompt 进行 A/B 测试，优化效果
4. **版本控制**: 将 Prompt 纳入版本管理，跟踪变更历史

### 下一步

- 将这些 Prompt 模板集成到代码中
- 建立 Prompt 性能监控体系（成功率、质量评分）
- 收集失败案例，持续优化 Prompt
- 考虑使用 Prompt 管理工具（如 LangSmith、PromptLayer）

---

**文档维护**: 每季度根据 Anthropic 最新指南更新本文档。
**反馈渠道**: 如发现 Prompt 效果不佳的场景，请记录并提交改进建议。
