# Phase 4: ELK 布局计算 (ELK Layout Computation)

## 一、阶段目标

使用 ELK.js 引擎计算所有节点的精确坐标和连线路径。这是整个流程的核心计算阶段。

---

## 二、为什么选择 ELK？

### 2.1 方案对比

| 特性 | ELK.js | Python Grandalf | 自写布局算法 | mxGraph 内置 |
|------|--------|-----------------|-------------|-------------|
| **嵌套支持** | ⭐⭐⭐ 原生 | ⭐ 需要额外处理 | ❌ 极复杂 | ⭐⭐ 基础 |
| **正交路由** | ⭐⭐⭐ 内置 | ❌ 无 | ⭐ 需实现 A* | ⭐⭐ 有限 |
| **算法选择** | 6+ 种 | 1 种 (Sugiyama) | 自定义 | 5+ 种 |
| **维护成本** | 低 | 中 | 高 | 低 |
| **社区活跃** | 活跃 (Eclipse) | 低 | N/A | 停滞 |
| **2025 状态** | ⭐⭐⭐ 持续更新 | ⭐ 维护模式 | N/A | ⭐ 停止更新 |

### 2.2 ELK 核心能力

1. **原生嵌套支持**
   - `elk.hierarchyHandling: INCLUDE_CHILDREN`
   - 自动计算容器尺寸
   - 子节点使用相对坐标

2. **正交连线路由**
   - `elk.edgeRouting: ORTHOGONAL`
   - 自动避让障碍物
   - 生成直角拐点 (bendPoints)

3. **混合布局**
   - 根节点和子容器可以使用不同布局算法
   - 支持 layered, mrtree, radial, force 等

---

## 三、架构设计

### 3.1 桥接模式

```
┌─────────────────────────────────────────────────────────────────┐
│                        Python (主进程)                          │
│                                                                  │
│  ┌──────────────┐                        ┌──────────────────┐   │
│  │  GraphSpec   │  ──── subprocess ───→  │   LayoutResult   │   │
│  │    (JSON)    │       stdin/stdout     │     (JSON)       │   │
│  └──────────────┘                        └──────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Node.js (子进程)                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                       elk_runner.js                       │   │
│  │                                                           │   │
│  │   const ELK = require('elkjs');                          │   │
│  │   const elk = new ELK();                                 │   │
│  │                                                           │   │
│  │   // 读取 stdin                                          │   │
│  │   const graph = JSON.parse(input);                       │   │
│  │                                                           │   │
│  │   // 执行布局                                             │   │
│  │   const result = await elk.layout(graph);                │   │
│  │                                                           │   │
│  │   // 输出到 stdout                                        │   │
│  │   console.log(JSON.stringify(result));                   │   │
│  │                                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 数据流

```
GraphSpec (Phase 2)
    │
    ├─→ layoutOptions 添加默认值
    │
    ▼
ELK Input JSON
    │
    ├─→ subprocess: node elk_runner.js
    │
    ▼
ELK Output JSON
    │
    ├─→ 坐标校验 (范围检查)
    │
    ▼
LayoutResult
```

---

## 四、输入输出规范

### 4.1 输入 (GraphSpec)

```typescript
// 与 Phase 2 输出一致，ELK 原生格式
interface ELKInput {
  id: string;
  labels?: { text: string }[];
  width?: number;
  height?: number;
  children?: ELKInput[];
  edges?: {
    id: string;
    sources: string[];
    targets: string[];
  }[];
  layoutOptions?: {
    'elk.algorithm': string;
    'elk.direction': string;
    [key: string]: any;
  };
}
```

### 4.2 输出 (LayoutResult)

```typescript
interface LayoutResult {
  id: string;

  // ELK 计算的坐标（相对于父节点）
  x: number;
  y: number;

  // ELK 计算的尺寸（容器会自动扩展）
  width: number;
  height: number;

  // 子节点（递归）
  children?: LayoutResult[];

  // 边布局结果
  edges?: LayoutEdge[];
}

interface LayoutEdge {
  id: string;
  sources: string[];
  targets: string[];

  // 连线路径
  sections: Array<{
    startPoint: Point;
    endPoint: Point;
    bendPoints?: Point[];  // 正交路由的拐点
  }>;

  // 边标签位置
  labels?: Array<{
    text: string;
    x: number;
    y: number;
    width: number;
    height: number;
  }>;
}

interface Point {
  x: number;
  y: number;
}
```

---

## 五、实现代码

### 5.1 elk_runner.js (Node.js)

```javascript
#!/usr/bin/env node
/**
 * ELK Layout Runner
 *
 * 用法:
 *   echo '{"id":"root",...}' | node elk_runner.js
 *   node elk_runner.js --file input.json
 */

const ELK = require('elkjs');

// 默认布局选项
const DEFAULT_OPTIONS = {
    'elk.algorithm': 'layered',
    'elk.direction': 'DOWN',
    'elk.edgeRouting': 'ORTHOGONAL',
    'elk.hierarchyHandling': 'INCLUDE_CHILDREN',
    'elk.spacing.nodeNode': '40',
    'elk.layered.spacing.nodeNodeBetweenLayers': '60',
    'elk.layered.crossingMinimization.strategy': 'LAYER_SWEEP',
    'elk.layered.nodePlacement.strategy': 'NETWORK_SIMPLEX',
    'elk.padding': '[top=20,left=20,bottom=20,right=20]',
};

async function main() {
    const elk = new ELK();

    // 读取输入
    let input = '';

    if (process.argv.includes('--file')) {
        const fs = require('fs');
        const fileIndex = process.argv.indexOf('--file') + 1;
        const filePath = process.argv[fileIndex];
        input = fs.readFileSync(filePath, 'utf-8');
    } else {
        // 从 stdin 读取
        input = await readStdin();
    }

    try {
        const graph = JSON.parse(input);

        // 应用默认选项
        graph.layoutOptions = {
            ...DEFAULT_OPTIONS,
            ...(graph.layoutOptions || {})
        };

        // 递归应用默认选项到子节点
        applyDefaultsRecursive(graph);

        // 执行布局
        const result = await elk.layout(graph);

        // 输出结果
        console.log(JSON.stringify(result, null, 2));

    } catch (error) {
        console.error(JSON.stringify({
            error: true,
            message: error.message,
            stack: error.stack
        }));
        process.exit(1);
    }
}

function applyDefaultsRecursive(node) {
    // 确保容器有嵌套处理选项
    if (node.children && node.children.length > 0) {
        node.layoutOptions = node.layoutOptions || {};
        node.layoutOptions['elk.hierarchyHandling'] = 'INCLUDE_CHILDREN';

        // 容器内边距
        if (!node.layoutOptions['elk.padding']) {
            node.layoutOptions['elk.padding'] = '[top=40,left=20,bottom=20,right=20]';
        }

        // 递归处理子节点
        for (const child of node.children) {
            applyDefaultsRecursive(child);
        }
    }
}

function readStdin() {
    return new Promise((resolve) => {
        let data = '';
        process.stdin.setEncoding('utf8');
        process.stdin.on('data', chunk => data += chunk);
        process.stdin.on('end', () => resolve(data));
    });
}

main();
```

### 5.2 layout_bridge.py (Python)

```python
"""
Phase 4: ELK 布局桥接器
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class LayoutConfig:
    """布局配置"""
    node_js_path: str = 'node'
    elk_runner_path: str = 'scripts/elk_runner.js'
    timeout: int = 30  # 秒


class ELKLayoutError(Exception):
    """ELK 布局错误"""
    pass


class LayoutBridge:
    """ELK 布局桥接器"""

    def __init__(self, config: Optional[LayoutConfig] = None):
        self.config = config or LayoutConfig()
        self._validate_environment()

    def _validate_environment(self):
        """验证 Node.js 环境"""
        try:
            result = subprocess.run(
                [self.config.node_js_path, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                raise ELKLayoutError("Node.js 未安装或不可用")
        except FileNotFoundError:
            raise ELKLayoutError("找不到 Node.js，请确保已安装")

    def layout(self, graph_spec: dict) -> dict:
        """
        调用 ELK 计算布局

        Args:
            graph_spec: Phase 2 输出的 GraphSpec

        Returns:
            带有坐标的 LayoutResult

        Raises:
            ELKLayoutError: ELK 计算失败
        """
        # 准备输入
        input_json = json.dumps(graph_spec, ensure_ascii=False)

        # 获取 elk_runner.js 的绝对路径
        script_dir = Path(__file__).parent
        elk_runner = script_dir / self.config.elk_runner_path

        if not elk_runner.exists():
            raise ELKLayoutError(f"找不到 elk_runner.js: {elk_runner}")

        try:
            # 调用 Node.js
            result = subprocess.run(
                [self.config.node_js_path, str(elk_runner)],
                input=input_json,
                capture_output=True,
                text=True,
                timeout=self.config.timeout
            )

            if result.returncode != 0:
                error_info = result.stderr or result.stdout
                raise ELKLayoutError(f"ELK 布局失败: {error_info}")

            # 解析输出
            layout_result = json.loads(result.stdout)

            # 验证结果
            self._validate_result(layout_result)

            return layout_result

        except subprocess.TimeoutExpired:
            raise ELKLayoutError(f"ELK 布局超时 ({self.config.timeout}s)")
        except json.JSONDecodeError as e:
            raise ELKLayoutError(f"ELK 输出解析失败: {e}")

    def _validate_result(self, result: dict):
        """验证布局结果"""
        # 检查根节点是否有坐标
        if 'x' not in result or 'y' not in result:
            # 根节点可能没有坐标，这是正常的
            pass

        # 检查子节点
        for child in result.get('children', []):
            if 'x' not in child or 'y' not in child:
                raise ELKLayoutError(f"节点 {child.get('id')} 缺少坐标")
            if 'width' not in child or 'height' not in child:
                raise ELKLayoutError(f"节点 {child.get('id')} 缺少尺寸")

            # 递归验证
            self._validate_result(child)

    def layout_with_retry(self, graph_spec: dict, max_retries: int = 3) -> dict:
        """
        带重试的布局计算

        如果首次布局失败，尝试调整参数重新计算
        """
        last_error = None

        for attempt in range(max_retries):
            try:
                return self.layout(graph_spec)
            except ELKLayoutError as e:
                last_error = e

                # 尝试调整参数
                if 'crossing' in str(e).lower():
                    # 交叉问题：增加间距
                    self._increase_spacing(graph_spec)
                elif 'overlap' in str(e).lower():
                    # 重叠问题：增加节点间距
                    self._increase_node_spacing(graph_spec)

        raise ELKLayoutError(f"布局失败，已重试 {max_retries} 次: {last_error}")

    def _increase_spacing(self, graph_spec: dict):
        """增加层间距"""
        opts = graph_spec.setdefault('layoutOptions', {})
        current = int(opts.get('elk.layered.spacing.nodeNodeBetweenLayers', '60'))
        opts['elk.layered.spacing.nodeNodeBetweenLayers'] = str(current + 20)

    def _increase_node_spacing(self, graph_spec: dict):
        """增加节点间距"""
        opts = graph_spec.setdefault('layoutOptions', {})
        current = int(opts.get('elk.spacing.nodeNode', '40'))
        opts['elk.spacing.nodeNode'] = str(current + 20)


# 便捷函数
def compute_layout(graph_spec: dict) -> dict:
    """计算布局的便捷函数"""
    bridge = LayoutBridge()
    return bridge.layout(graph_spec)
```

### 5.3 package.json (Node.js 依赖)

```json
{
  "name": "drawio-elk-layout",
  "version": "1.0.0",
  "description": "ELK layout engine for DrawIO generator",
  "main": "elk_runner.js",
  "scripts": {
    "layout": "node elk_runner.js",
    "test": "node test_elk.js"
  },
  "dependencies": {
    "elkjs": "^0.9.3"
  },
  "engines": {
    "node": ">=16.0.0"
  }
}
```

---

## 六、ELK 布局选项详解

### 6.1 核心选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `elk.algorithm` | enum | layered | 布局算法 |
| `elk.direction` | enum | DOWN | 布局方向 |
| `elk.edgeRouting` | enum | ORTHOGONAL | 连线路由 |
| `elk.hierarchyHandling` | enum | SEPARATE_CHILDREN | 嵌套处理 |
| `elk.spacing.nodeNode` | number | 20 | 节点间距 |

### 6.2 算法选择

```javascript
// layered - 分层布局（适合 DAG、流程图）
{ 'elk.algorithm': 'layered' }

// mrtree - 树形布局（适合树、思维导图）
{ 'elk.algorithm': 'mrtree' }

// radial - 放射布局（适合网络图）
{ 'elk.algorithm': 'radial' }

// force - 力导向（适合复杂网络）
{ 'elk.algorithm': 'force' }

// stress - 应力布局
{ 'elk.algorithm': 'stress' }

// rectpacking - 矩形打包（容器内部）
{ 'elk.algorithm': 'rectpacking' }
```

### 6.3 嵌套容器配置

```javascript
{
  "id": "container",
  "labels": [{"text": "Container Title"}],
  "layoutOptions": {
    "elk.algorithm": "layered",
    "elk.direction": "DOWN",
    // 关键：启用子节点布局
    "elk.hierarchyHandling": "INCLUDE_CHILDREN",
    // 标题高度预留
    "elk.padding": "[top=50,left=20,bottom=20,right=20]"
  },
  "children": [
    // 子节点
  ]
}
```

### 6.4 连线路由选项

```javascript
// 正交路由（直角）
{ 'elk.edgeRouting': 'ORTHOGONAL' }

// 折线
{ 'elk.edgeRouting': 'POLYLINE' }

// 曲线
{ 'elk.edgeRouting': 'SPLINES' }
```

---

## 七、示例

### 7.1 简单架构图

**输入**:
```json
{
  "id": "root",
  "layoutOptions": {
    "elk.algorithm": "layered",
    "elk.direction": "DOWN"
  },
  "children": [
    {"id": "client", "width": 100, "height": 50, "labels": [{"text": "Client"}]},
    {"id": "server", "width": 100, "height": 50, "labels": [{"text": "Server"}]},
    {"id": "db", "width": 100, "height": 60, "labels": [{"text": "Database"}]}
  ],
  "edges": [
    {"id": "e1", "sources": ["client"], "targets": ["server"]},
    {"id": "e2", "sources": ["server"], "targets": ["db"]}
  ]
}
```

**输出**:
```json
{
  "id": "root",
  "x": 0,
  "y": 0,
  "width": 140,
  "height": 250,
  "children": [
    {"id": "client", "x": 20, "y": 20, "width": 100, "height": 50},
    {"id": "server", "x": 20, "y": 110, "width": 100, "height": 50},
    {"id": "db", "x": 20, "y": 200, "width": 100, "height": 60}
  ],
  "edges": [
    {
      "id": "e1",
      "sources": ["client"],
      "targets": ["server"],
      "sections": [{
        "startPoint": {"x": 70, "y": 70},
        "endPoint": {"x": 70, "y": 110}
      }]
    },
    {
      "id": "e2",
      "sources": ["server"],
      "targets": ["db"],
      "sections": [{
        "startPoint": {"x": 70, "y": 160},
        "endPoint": {"x": 70, "y": 200}
      }]
    }
  ]
}
```

### 7.2 嵌套 Transformer Block

**输入**:
```json
{
  "id": "root",
  "layoutOptions": {
    "elk.algorithm": "layered",
    "elk.direction": "DOWN",
    "elk.hierarchyHandling": "INCLUDE_CHILDREN"
  },
  "children": [
    {
      "id": "encoder",
      "labels": [{"text": "Encoder Block"}],
      "layoutOptions": {
        "elk.algorithm": "layered",
        "elk.direction": "DOWN",
        "elk.padding": "[top=40,left=20,bottom=20,right=20]"
      },
      "children": [
        {"id": "mha", "width": 150, "height": 40, "labels": [{"text": "Multi-Head Attention"}]},
        {"id": "norm1", "width": 100, "height": 30, "labels": [{"text": "Add & Norm"}]},
        {"id": "ffn", "width": 150, "height": 40, "labels": [{"text": "Feed Forward"}]},
        {"id": "norm2", "width": 100, "height": 30, "labels": [{"text": "Add & Norm"}]}
      ],
      "edges": [
        {"id": "e1", "sources": ["mha"], "targets": ["norm1"]},
        {"id": "e2", "sources": ["norm1"], "targets": ["ffn"]},
        {"id": "e3", "sources": ["ffn"], "targets": ["norm2"]}
      ]
    }
  ]
}
```

**输出**:
```json
{
  "id": "root",
  "width": 230,
  "height": 340,
  "children": [
    {
      "id": "encoder",
      "x": 20,
      "y": 20,
      "width": 190,
      "height": 300,
      "children": [
        {"id": "mha", "x": 20, "y": 40, "width": 150, "height": 40},
        {"id": "norm1", "x": 45, "y": 120, "width": 100, "height": 30},
        {"id": "ffn", "x": 20, "y": 190, "width": 150, "height": 40},
        {"id": "norm2", "x": 45, "y": 270, "width": 100, "height": 30}
      ],
      "edges": [
        {
          "id": "e1",
          "sections": [{
            "startPoint": {"x": 95, "y": 80},
            "endPoint": {"x": 95, "y": 120}
          }]
        },
        {
          "id": "e2",
          "sections": [{
            "startPoint": {"x": 95, "y": 150},
            "endPoint": {"x": 95, "y": 190}
          }]
        },
        {
          "id": "e3",
          "sections": [{
            "startPoint": {"x": 95, "y": 230},
            "endPoint": {"x": 95, "y": 270}
          }]
        }
      ]
    }
  ]
}
```

---

## 八、错误处理

### 8.1 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `Node not found` | 边引用了不存在的节点 | 验证节点 ID |
| `Cycle detected` | 存在循环依赖 | ELK 自动处理，或调整图结构 |
| `Timeout` | 图太复杂 | 增加超时时间，或简化图 |
| `Overlapping nodes` | 间距不足 | 增加 `elk.spacing.nodeNode` |

### 8.2 降级策略

```python
def layout_with_fallback(graph_spec: dict) -> dict:
    """带降级的布局计算"""
    try:
        # 尝试 ELK 布局
        return LayoutBridge().layout(graph_spec)
    except ELKLayoutError:
        # 降级到简单布局
        return simple_grid_layout(graph_spec)


def simple_grid_layout(graph_spec: dict) -> dict:
    """简单网格布局（备用）"""
    nodes = graph_spec.get('children', [])
    cols = min(4, len(nodes))
    spacing = 150

    for i, node in enumerate(nodes):
        row = i // cols
        col = i % cols
        node['x'] = 50 + col * spacing
        node['y'] = 50 + row * spacing
        node['width'] = node.get('width', 120)
        node['height'] = node.get('height', 60)

    return graph_spec
```

---

## 九、与下一阶段的衔接

Phase 4 输出的 `LayoutResult` 将传递给 Phase 5（XML 生成），用于：

1. **节点定位**
   - 使用 `x`, `y`, `width`, `height` 生成 mxGeometry

2. **连线路径**
   - 使用 `sections[].bendPoints` 生成 waypoints

3. **嵌套关系**
   - 使用 `children` 结构确定 `parent` 属性

---

## 十、参考

- [ELK Official Documentation](https://eclipse.dev/elk/)
- [ELK JSON Format](https://eclipse.dev/elk/documentation/tooldevelopers/graphdatastructure/jsonformat.html)
- [ELK Layout Options Reference](https://eclipse.dev/elk/reference/options.html)
- [elkjs GitHub](https://github.com/kieler/elkjs)
- [elkjs npm](https://www.npmjs.com/package/elkjs)
