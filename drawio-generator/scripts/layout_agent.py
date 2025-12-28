#!/usr/bin/env python3
"""
Layout Agent - 布局计算工具

用法:
    python layout_agent.py --spec spec.json --output layout.json
    python layout_agent.py --spec spec.json --algorithm layered --spacing 150
    echo '{"nodes":[...], "edges":[...]}' | python layout_agent.py

输入: DiagramSpec JSON
输出: LayoutResult JSON
"""

import json
import math
import sys
import argparse
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# 尝试导入 Grandalf（可选依赖）
try:
    from grandalf.graphs import Vertex, Edge, Graph
    from grandalf.layouts import SugiyamaLayout
    HAS_GRANDALF = True
except ImportError:
    HAS_GRANDALF = False


@dataclass
class LayoutConfig:
    canvas_width: int = 800
    canvas_height: int = 600
    node_width: int = 120
    node_height: int = 60
    spacing: int = 120
    layer_spacing: int = 120
    margin: int = 40
    grid_size: int = 10
    algorithm: str = "auto"  # auto, layered, radial, grid, force


@dataclass
class NodePosition:
    id: str
    x: int
    y: int
    width: int
    height: int


@dataclass
class EdgePath:
    id: str
    source: str
    target: str
    exit_x: float
    exit_y: float
    entry_x: float
    entry_y: float
    waypoints: List[Tuple[int, int]]


class LayoutEngine:
    """布局引擎"""

    def __init__(self, config: LayoutConfig):
        self.config = config

    def layout(self, spec: dict) -> dict:
        """执行布局计算"""
        nodes = spec.get('nodes', [])
        edges = spec.get('edges', [])
        layout_hint = spec.get('layout_hint', 'auto')
        diagram_type = spec.get('diagram_type', 'flowchart')

        # 选择算法
        algorithm = self._select_algorithm(layout_hint, diagram_type)

        # 调整画布大小
        self._adjust_canvas(len(nodes))

        # 执行布局
        if algorithm == 'layered':
            node_positions = self._layered_layout(nodes, edges)
        elif algorithm == 'radial':
            node_positions = self._radial_layout(nodes, edges)
        elif algorithm == 'grid':
            node_positions = self._grid_layout(nodes)
        elif algorithm == 'horizontal':
            node_positions = self._horizontal_layout(nodes)
        else:
            node_positions = self._layered_layout(nodes, edges)

        # 计算边路径
        edge_paths = self._compute_edges(node_positions, edges, algorithm)

        return {
            'nodes': [asdict(n) for n in node_positions],
            'edges': [asdict(e) for e in edge_paths],
            'canvas': {
                'width': self.config.canvas_width,
                'height': self.config.canvas_height
            },
            'algorithm_used': algorithm
        }

    def _select_algorithm(self, hint: str, diagram_type: str) -> str:
        """选择布局算法"""
        if self.config.algorithm != 'auto':
            return self.config.algorithm

        if hint == 'horizontal':
            return 'horizontal'
        elif hint == 'vertical':
            return 'layered'
        elif hint == 'radial':
            return 'radial'
        elif hint == 'grid':
            return 'grid'

        # 根据图表类型推断
        type_map = {
            'flowchart': 'horizontal',
            'architecture': 'layered',
            'network': 'radial',
            'uml': 'layered',
            'er': 'grid',
            'mindmap': 'radial'
        }
        return type_map.get(diagram_type, 'layered')

    def _adjust_canvas(self, node_count: int):
        """根据节点数量调整画布"""
        if node_count > 20:
            self.config.canvas_width = 1200
            self.config.canvas_height = 900
        elif node_count > 10:
            self.config.canvas_width = 1000
            self.config.canvas_height = 750

    def _snap_to_grid(self, value: float) -> int:
        """对齐到网格"""
        return round(value / self.config.grid_size) * self.config.grid_size

    def _horizontal_layout(self, nodes: List[dict]) -> List[NodePosition]:
        """水平流程布局"""
        positions = []
        n = len(nodes)
        if n == 0:
            return positions

        total_width = n * self.config.node_width + (n - 1) * self.config.spacing
        start_x = max(self.config.margin, (self.config.canvas_width - total_width) // 2)
        y = (self.config.canvas_height - self.config.node_height) // 2

        for i, node in enumerate(nodes):
            x = start_x + i * (self.config.node_width + self.config.spacing)
            positions.append(NodePosition(
                id=node['id'],
                x=self._snap_to_grid(x),
                y=self._snap_to_grid(y),
                width=self.config.node_width,
                height=self.config.node_height
            ))

        return positions

    def _layered_layout(self, nodes: List[dict], edges: List[dict]) -> List[NodePosition]:
        """层级布局（垂直）- 优先使用 Grandalf Sugiyama 算法"""
        if HAS_GRANDALF and len(nodes) > 0:
            try:
                return self._grandalf_sugiyama(nodes, edges)
            except Exception as e:
                print(f"⚠️  Grandalf 布局失败，回退到简单布局: {e}", file=sys.stderr)

        # 回退到简单拓扑分层
        return self._simple_layered_layout(nodes, edges)

    def _grandalf_sugiyama(self, nodes: List[dict], edges: List[dict]) -> List[NodePosition]:
        """使用 Grandalf 的 Sugiyama 算法（边交叉最小化）"""
        # 创建顶点映射
        vertices = {}
        for node in nodes:
            v = Vertex(node)
            vertices[node['id']] = v

        V = list(vertices.values())

        # 创建边（只添加两端都存在的边）
        E = []
        for edge in edges:
            src_id, tgt_id = edge['source'], edge['target']
            if src_id in vertices and tgt_id in vertices:
                E.append(Edge(vertices[src_id], vertices[tgt_id]))

        if not E:
            # 没有边，使用网格布局
            return self._grid_layout(nodes)

        # 创建图
        g = Graph(V, E)

        # 设置节点尺寸视图
        class NodeView:
            def __init__(self, w, h):
                self.w = w
                self.h = h
                self.xy = (0, 0)

        for v in V:
            v.view = NodeView(self.config.node_width, self.config.node_height)

        # 执行 Sugiyama 布局
        sug = SugiyamaLayout(g.C[0])
        sug.init_all()
        sug.draw()

        # 收集坐标并计算边界
        raw_positions = []
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        for v in g.C[0].sV:
            x, y = v.view.xy
            raw_positions.append((v.data['id'], x, y))
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + self.config.node_width)
            max_y = max(max_y, y + self.config.node_height)

        # 计算偏移量，使图居中
        graph_width = max_x - min_x
        graph_height = max_y - min_y
        offset_x = (self.config.canvas_width - graph_width) / 2 - min_x
        offset_y = self.config.margin - min_y

        # 生成最终位置
        positions = []
        for node_id, x, y in raw_positions:
            final_x = self._snap_to_grid(x + offset_x)
            final_y = self._snap_to_grid(y + offset_y)
            positions.append(NodePosition(
                id=node_id,
                x=final_x,
                y=final_y,
                width=self.config.node_width,
                height=self.config.node_height
            ))

        return positions

    def _simple_layered_layout(self, nodes: List[dict], edges: List[dict]) -> List[NodePosition]:
        """简单拓扑分层布局（回退方案）"""
        # 拓扑分层
        levels = self._topological_levels(nodes, edges)

        positions = []
        y = self.config.margin

        for level_ids in levels:
            level_nodes = [n for n in nodes if n['id'] in level_ids]
            n = len(level_nodes)

            total_width = n * self.config.node_width + (n - 1) * self.config.spacing
            start_x = max(self.config.margin, (self.config.canvas_width - total_width) // 2)

            for i, node in enumerate(level_nodes):
                x = start_x + i * (self.config.node_width + self.config.spacing)
                positions.append(NodePosition(
                    id=node['id'],
                    x=self._snap_to_grid(x),
                    y=self._snap_to_grid(y),
                    width=self.config.node_width,
                    height=self.config.node_height
                ))

            y += self.config.node_height + self.config.layer_spacing

        return positions

    def _radial_layout(self, nodes: List[dict], edges: List[dict]) -> List[NodePosition]:
        """中心辐射布局"""
        positions = []
        n = len(nodes)
        if n == 0:
            return positions

        center_x = self.config.canvas_width // 2
        center_y = self.config.canvas_height // 2

        # 第一个节点放中心
        positions.append(NodePosition(
            id=nodes[0]['id'],
            x=self._snap_to_grid(center_x - self.config.node_width // 2),
            y=self._snap_to_grid(center_y - self.config.node_height // 2),
            width=self.config.node_width,
            height=self.config.node_height
        ))

        # 其余节点围绕中心
        if n > 1:
            radius = min(center_x, center_y) - self.config.margin - self.config.node_width
            for i, node in enumerate(nodes[1:], 1):
                angle = 2 * math.pi * (i - 1) / (n - 1) - math.pi / 2
                x = center_x + radius * math.cos(angle) - self.config.node_width // 2
                y = center_y + radius * math.sin(angle) - self.config.node_height // 2

                positions.append(NodePosition(
                    id=node['id'],
                    x=self._snap_to_grid(x),
                    y=self._snap_to_grid(y),
                    width=self.config.node_width,
                    height=self.config.node_height
                ))

        return positions

    def _grid_layout(self, nodes: List[dict]) -> List[NodePosition]:
        """网格布局"""
        positions = []
        n = len(nodes)
        if n == 0:
            return positions

        cols = math.ceil(math.sqrt(n))
        rows = math.ceil(n / cols)

        cell_w = self.config.node_width + self.config.spacing
        cell_h = self.config.node_height + self.config.spacing

        total_w = cols * cell_w - self.config.spacing
        total_h = rows * cell_h - self.config.spacing
        start_x = max(self.config.margin, (self.config.canvas_width - total_w) // 2)
        start_y = max(self.config.margin, (self.config.canvas_height - total_h) // 2)

        for i, node in enumerate(nodes):
            row = i // cols
            col = i % cols
            x = start_x + col * cell_w
            y = start_y + row * cell_h

            positions.append(NodePosition(
                id=node['id'],
                x=self._snap_to_grid(x),
                y=self._snap_to_grid(y),
                width=self.config.node_width,
                height=self.config.node_height
            ))

        return positions

    def _topological_levels(self, nodes: List[dict], edges: List[dict]) -> List[List[str]]:
        """拓扑排序分层"""
        node_ids = {n['id'] for n in nodes}
        adj = {n['id']: [] for n in nodes}
        in_degree = {n['id']: 0 for n in nodes}

        for e in edges:
            src, tgt = e['source'], e['target']
            if src in adj and tgt in node_ids:
                adj[src].append(tgt)
                in_degree[tgt] += 1

        levels = []
        queue = [n for n, d in in_degree.items() if d == 0]
        visited = set()

        while queue:
            levels.append(queue)
            visited.update(queue)
            next_queue = []

            for node in queue:
                for neighbor in adj[node]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0 and neighbor not in visited:
                        next_queue.append(neighbor)

            queue = next_queue

        # 处理未访问的节点
        remaining = [n['id'] for n in nodes if n['id'] not in visited]
        if remaining:
            levels.append(remaining)

        return levels

    def _compute_edges(
        self,
        positions: List[NodePosition],
        edges: List[dict],
        algorithm: str
    ) -> List[EdgePath]:
        """计算边的连接路径"""
        pos_map = {p.id: p for p in positions}
        paths = []

        for e in edges:
            src = pos_map.get(e['source'])
            tgt = pos_map.get(e['target'])

            if not src or not tgt:
                continue

            exit_x, exit_y, entry_x, entry_y = self._compute_anchors(src, tgt, algorithm)
            waypoints = self._compute_waypoints(src, tgt, positions, pos_map)

            paths.append(EdgePath(
                id=e.get('id', f"{e['source']}_{e['target']}"),
                source=e['source'],
                target=e['target'],
                exit_x=exit_x,
                exit_y=exit_y,
                entry_x=entry_x,
                entry_y=entry_y,
                waypoints=waypoints
            ))

        return paths

    def _compute_anchors(
        self,
        src: NodePosition,
        tgt: NodePosition,
        algorithm: str
    ) -> Tuple[float, float, float, float]:
        """计算锚点"""
        src_cx = src.x + src.width / 2
        src_cy = src.y + src.height / 2
        tgt_cx = tgt.x + tgt.width / 2
        tgt_cy = tgt.y + tgt.height / 2

        dx = tgt_cx - src_cx
        dy = tgt_cy - src_cy

        if algorithm == 'horizontal':
            return (1.0, 0.5, 0.0, 0.5) if dx >= 0 else (0.0, 0.5, 1.0, 0.5)
        elif algorithm == 'layered':
            return (0.5, 1.0, 0.5, 0.0) if dy >= 0 else (0.5, 0.0, 0.5, 1.0)
        else:
            # 自动判断
            if abs(dx) > abs(dy):
                return (1.0 if dx > 0 else 0.0), 0.5, (0.0 if dx > 0 else 1.0), 0.5
            else:
                return 0.5, (1.0 if dy > 0 else 0.0), 0.5, (0.0 if dy > 0 else 1.0)

    def _compute_waypoints(
        self,
        src: NodePosition,
        tgt: NodePosition,
        all_positions: List[NodePosition],
        pos_map: Dict[str, NodePosition]
    ) -> List[Tuple[int, int]]:
        """计算绕行点"""
        # 简化实现：检查直线是否穿过其他节点
        src_cx = src.x + src.width / 2
        src_cy = src.y + src.height / 2
        tgt_cx = tgt.x + tgt.width / 2
        tgt_cy = tgt.y + tgt.height / 2

        for pos in all_positions:
            if pos.id == src.id or pos.id == tgt.id:
                continue

            if self._line_intersects_rect(
                src_cx, src_cy, tgt_cx, tgt_cy,
                pos.x, pos.y, pos.width, pos.height
            ):
                # 需要绕行
                if abs(tgt_cx - src_cx) > abs(tgt_cy - src_cy):
                    # 主要水平移动，上下绕行
                    wp_y = pos.y - 30 if src_cy < pos.y + pos.height / 2 else pos.y + pos.height + 30
                    return [(int(src_cx), int(wp_y)), (int(tgt_cx), int(wp_y))]
                else:
                    # 主要垂直移动，左右绕行
                    wp_x = pos.x - 30 if src_cx < pos.x + pos.width / 2 else pos.x + pos.width + 30
                    return [(int(wp_x), int(src_cy)), (int(wp_x), int(tgt_cy))]

        return []

    def _line_intersects_rect(
        self,
        x1: float, y1: float, x2: float, y2: float,
        rx: float, ry: float, rw: float, rh: float
    ) -> bool:
        """检查线段是否与矩形相交"""
        # 简化：检查线段中点是否在矩形内
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        return rx < mid_x < rx + rw and ry < mid_y < ry + rh


def main():
    parser = argparse.ArgumentParser(description='Layout Agent - 布局计算')
    parser.add_argument('--spec', '-s', help='DiagramSpec JSON 文件路径')
    parser.add_argument('--output', '-o', help='输出 LayoutResult JSON 文件路径')
    parser.add_argument('--algorithm', '-a', default='auto',
                        choices=['auto', 'layered', 'horizontal', 'radial', 'grid'],
                        help='布局算法')
    parser.add_argument('--spacing', type=int, default=120, help='节点间距')
    parser.add_argument('--width', type=int, default=800, help='画布宽度')
    parser.add_argument('--height', type=int, default=600, help='画布高度')

    args = parser.parse_args()

    # 读取输入
    if args.spec:
        with open(args.spec, 'r', encoding='utf-8') as f:
            spec = json.load(f)
    else:
        spec = json.load(sys.stdin)

    # 配置
    config = LayoutConfig(
        canvas_width=args.width,
        canvas_height=args.height,
        spacing=args.spacing,
        algorithm=args.algorithm
    )

    # 执行布局
    engine = LayoutEngine(config)
    result = engine.layout(spec)

    # 输出
    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ Layout saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
