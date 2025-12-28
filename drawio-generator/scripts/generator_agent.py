#!/usr/bin/env python3
"""
Generator Agent - XML 生成工具

用法:
    python generator_agent.py --layout layout.json --styles styles.json --spec spec.json --output diagram.drawio
    python generator_agent.py --all-in-one combined.json --output diagram.drawio

输入: LayoutResult + ElementStyles + DiagramSpec
输出: DrawIO XML 文件
"""

import json
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional
from xml.sax.saxutils import escape


class DrawioGenerator:
    """DrawIO XML 生成器"""

    def __init__(self):
        self.id_counter = 2  # 0 和 1 保留

    def generate(
        self,
        layout: dict,
        styles: dict,
        spec: dict
    ) -> str:
        """生成完整的 DrawIO XML"""
        self.id_counter = 2

        # 构建映射
        node_map = {n['id']: n for n in spec.get('nodes', [])}
        edge_map = {e['id']: e for e in spec.get('edges', [])}
        style_map = styles.get('node_styles', {})
        edge_style = styles.get('edge_style', '')

        # 生成 XML
        xml_parts = []
        xml_parts.append(self._header(layout.get('canvas', {}), spec.get('title', 'Diagram')))

        # 生成节点 ID 映射
        node_id_map = {}  # 原始 ID → mxCell ID
        for node_pos in layout.get('nodes', []):
            orig_id = node_pos['id']
            cell_id = str(self._next_id())
            node_id_map[orig_id] = cell_id

            node_info = node_map.get(orig_id, {})
            style_info = style_map.get(orig_id, {})

            xml_parts.append(self._node(
                cell_id=cell_id,
                label=node_info.get('label', orig_id),
                style=style_info.get('style', 'rounded=1;whiteSpace=wrap;html=1;'),
                x=node_pos['x'],
                y=node_pos['y'],
                width=node_pos['width'],
                height=node_pos['height']
            ))

        # 生成连线
        for edge_path in layout.get('edges', []):
            orig_id = edge_path['id']
            source_id = node_id_map.get(edge_path['source'])
            target_id = node_id_map.get(edge_path['target'])

            if not source_id or not target_id:
                continue

            edge_info = edge_map.get(orig_id, {})
            cell_id = str(self._next_id())

            # 构建边样式
            full_edge_style = self._build_edge_style(
                edge_style,
                edge_path,
                edge_info.get('type', 'arrow')
            )

            xml_parts.append(self._edge(
                cell_id=cell_id,
                source=source_id,
                target=target_id,
                style=full_edge_style,
                label=edge_info.get('label'),
                waypoints=edge_path.get('waypoints', [])
            ))

        xml_parts.append(self._footer())

        return '\n'.join(xml_parts)

    def _next_id(self) -> int:
        current = self.id_counter
        self.id_counter += 1
        return current

    def _header(self, canvas: dict, title: str) -> str:
        width = canvas.get('width', 800)
        height = canvas.get('height', 600)
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        title_escaped = escape(title)

        return f'''<mxfile host="DrawIO-Agent" modified="{timestamp}" agent="DrawIO-Generator/1.0" version="1.0">
  <diagram name="{title_escaped}" id="diagram-1">
    <mxGraphModel dx="{width}" dy="{height}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>'''

    def _footer(self) -> str:
        return '''      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

    def _node(
        self,
        cell_id: str,
        label: str,
        style: str,
        x: int,
        y: int,
        width: int,
        height: int,
        parent: str = '1'
    ) -> str:
        label_escaped = escape(label)
        return f'''        <mxCell id="{cell_id}" value="{label_escaped}" style="{style}" vertex="1" parent="{parent}">
          <mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/>
        </mxCell>'''

    def _edge(
        self,
        cell_id: str,
        source: str,
        target: str,
        style: str,
        label: Optional[str] = None,
        waypoints: List[List[int]] = None,
        parent: str = '1'
    ) -> str:
        label_attr = f'value="{escape(label)}"' if label else 'value=""'
        geometry = self._edge_geometry(waypoints)

        return f'''        <mxCell id="{cell_id}" {label_attr} style="{style}" edge="1" parent="{parent}" source="{source}" target="{target}">
{geometry}
        </mxCell>'''

    def _edge_geometry(self, waypoints: List[List[int]] = None) -> str:
        if waypoints:
            points = '\n'.join([
                f'            <mxPoint x="{int(wp[0])}" y="{int(wp[1])}"/>'
                for wp in waypoints
            ])
            return f'''          <mxGeometry relative="1" as="geometry">
            <Array as="points">
{points}
            </Array>
          </mxGeometry>'''
        else:
            return '          <mxGeometry relative="1" as="geometry"/>'

    def _build_edge_style(
        self,
        base_style: str,
        edge_path: dict,
        edge_type: str
    ) -> str:
        parts = base_style.rstrip(';').split(';')

        # 添加锚点
        parts.append(f"exitX={edge_path.get('exit_x', 0.5)}")
        parts.append(f"exitY={edge_path.get('exit_y', 1)}")
        parts.append(f"entryX={edge_path.get('entry_x', 0.5)}")
        parts.append(f"entryY={edge_path.get('entry_y', 0)}")

        # 处理边类型
        if edge_type == 'dashed':
            parts.append('dashed=1')
        elif edge_type == 'bidirectional':
            parts.append('startArrow=classic')

        return ';'.join(parts) + ';'


def main():
    parser = argparse.ArgumentParser(description='Generator Agent - XML 生成')
    parser.add_argument('--layout', '-l', help='LayoutResult JSON 文件路径')
    parser.add_argument('--styles', '-s', help='ElementStyles JSON 文件路径')
    parser.add_argument('--spec', help='DiagramSpec JSON 文件路径')
    parser.add_argument('--all-in-one', '-a', help='合并的输入 JSON (包含 layout, styles, spec)')
    parser.add_argument('--output', '-o', required=True, help='输出 .drawio 文件路径')

    args = parser.parse_args()

    # 读取输入
    if args.all_in_one:
        with open(args.all_in_one, 'r', encoding='utf-8') as f:
            data = json.load(f)
        layout = data.get('layout', {})
        styles = data.get('styles', {})
        spec = data.get('spec', {})
    else:
        if not args.layout or not args.styles or not args.spec:
            print("错误: 需要 --layout, --styles, --spec，或使用 --all-in-one", file=sys.stderr)
            sys.exit(1)

        with open(args.layout, 'r', encoding='utf-8') as f:
            layout = json.load(f)
        with open(args.styles, 'r', encoding='utf-8') as f:
            styles = json.load(f)
        with open(args.spec, 'r', encoding='utf-8') as f:
            spec = json.load(f)

    # 生成
    generator = DrawioGenerator()
    xml = generator.generate(layout, styles, spec)

    # 输出
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(xml)

    # 统计
    node_count = len(layout.get('nodes', []))
    edge_count = len(layout.get('edges', []))
    print(f"✅ Generated: {args.output}", file=sys.stderr)
    print(f"   Nodes: {node_count}, Edges: {edge_count}", file=sys.stderr)


if __name__ == '__main__':
    main()
