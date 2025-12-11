#!/usr/bin/env python3
"""
DrawIO XML 验证脚本
用法: python validate_drawio.py <file.drawio>

验证内容:
1. XML 语法正确性
2. 基础结构完整性 (mxfile/diagram/mxGraphModel/root)
3. 必要属性检查 (vertex/edge, as="geometry", relative)
4. ID 唯一性和引用完整性
5. 样式格式规范
6. 节点重叠检测
"""

import xml.etree.ElementTree as ET
import sys
import re
from typing import Dict, List, Set, Optional, Tuple


class DrawIOValidator:
    """DrawIO XML 验证器"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.errors: List[Tuple[str, str, Optional[str]]] = []   # (message, fix_hint, element_id)
        self.warnings: List[Tuple[str, str, Optional[str]]] = []
        self.tree: Optional[ET.ElementTree] = None
        self.root: Optional[ET.Element] = None
        self.all_ids: Set[str] = set()
        self.nodes: Dict[str, dict] = {}
        self.edges: List[dict] = []
        self.page_count: int = 0

    def _error(self, msg: str, fix: str, elem_id: str = None):
        self.errors.append((msg, fix, elem_id))

    def _warn(self, msg: str, fix: str, elem_id: str = None):
        self.warnings.append((msg, fix, elem_id))

    def validate(self) -> bool:
        """执行验证，返回是否通过"""
        print(f"🔍 验证: {self.filepath}\n")

        if not self._parse_xml():
            self._print_results()
            return False

        self._validate_structure()
        self._collect_elements()
        self._validate_nodes()
        self._validate_edges()
        self._validate_styles()
        self._check_overlapping()
        self._print_results()

        return len(self.errors) == 0

    def _parse_xml(self) -> bool:
        try:
            self.tree = ET.parse(self.filepath)
            self.root = self.tree.getroot()
            return True
        except ET.ParseError as e:
            self._error(f"XML 解析失败: {e}", "检查标签闭合和特殊字符转义")
            return False
        except FileNotFoundError:
            self._error(f"文件不存在", "检查文件路径")
            return False

    def _validate_structure(self):
        if self.root.tag != 'mxfile':
            self._error("根元素必须是 <mxfile>", "修改根元素标签")
            return

        diagrams = self.root.findall('diagram')
        if not diagrams:
            self._error("缺少 <diagram>", "添加 <diagram name='...' id='...'>")
            return

        self.page_count = len(diagrams)

        for i, diagram in enumerate(diagrams):
            diagram_id = diagram.get('id', f'diagram_{i}')

            if not diagram.get('name'):
                self._warn("<diagram> 缺少 name", "添加 name='页面名称'", diagram_id)
            if not diagram.get('id'):
                self._warn("<diagram> 缺少 id", "添加 id='唯一标识'")

            model = diagram.find('mxGraphModel')
            if model is None:
                self._error("缺少 <mxGraphModel>", "在 <diagram> 内添加 <mxGraphModel>", diagram_id)
                continue

            root_elem = model.find('root')
            if root_elem is None:
                self._error("缺少 <root>", "在 <mxGraphModel> 内添加 <root>", diagram_id)
                continue

            ids = [c.get('id') for c in root_elem.findall('mxCell')]
            if '0' not in ids:
                self._error("缺少 id='0' 根节点", "添加 <mxCell id='0'/>")
            if '1' not in ids:
                self._error("缺少 id='1' 默认图层", "添加 <mxCell id='1' parent='0'/>")

    def _collect_elements(self):
        for cell in self.root.findall('.//mxCell'):
            cell_id = cell.get('id')
            if cell_id:
                self.all_ids.add(cell_id)

    def _validate_nodes(self):
        for cell in self.root.findall('.//mxCell'):
            cell_id = cell.get('id')
            if cell_id in ['0', '1'] or cell.get('parent') == '0':
                continue

            is_vertex = cell.get('vertex') == '1'
            is_edge = cell.get('edge') == '1'
            has_style = cell.get('style') is not None

            if has_style and not is_vertex and not is_edge:
                if cell.get('parent') != '0':
                    self._warn("有 style 但缺少 vertex/edge 属性", "添加 vertex='1' 或 edge='1'", cell_id)

            if is_vertex:
                self._validate_vertex(cell, cell_id)
            elif is_edge:
                self._validate_edge_cell(cell, cell_id)

    def _validate_vertex(self, cell: ET.Element, cell_id: str):
        geom = cell.find('mxGeometry')
        if geom is None:
            self._error("节点缺少 <mxGeometry>", "添加 <mxGeometry x='' y='' width='' height='' as='geometry'/>", cell_id)
            return

        if geom.get('as') != 'geometry':
            self._error("mxGeometry 缺少 as='geometry'", "添加 as='geometry'", cell_id)

        parent = cell.get('parent')
        if parent and parent not in self.all_ids:
            self._error(f"parent='{parent}' 不存在", f"改为 '1' 或创建 id='{parent}'", cell_id)

        x, y = float(geom.get('x', 0)), float(geom.get('y', 0))
        w, h = float(geom.get('width', 0)), float(geom.get('height', 0))
        self.nodes[cell_id] = {'x': x, 'y': y, 'width': w, 'height': h, 'parent': parent}

        if w <= 0 or h <= 0:
            self._warn(f"尺寸无效: {w}x{h}", "设置正数 width/height", cell_id)

    def _validate_edge_cell(self, cell: ET.Element, cell_id: str):
        self.edges.append({
            'id': cell_id,
            'source': cell.get('source'),
            'target': cell.get('target')
        })

        geom = cell.find('mxGeometry')
        if geom is not None:
            if geom.get('as') != 'geometry':
                self._error("连线 mxGeometry 缺少 as='geometry'", "添加 as='geometry'", cell_id)
            if geom.get('relative') != '1':
                self._error("连线 mxGeometry 缺少 relative='1'", "添加 relative='1'", cell_id)

        parent = cell.get('parent')
        if parent and parent not in self.all_ids:
            self._error(f"parent='{parent}' 不存在", "改为 '1'", cell_id)

    def _validate_edges(self):
        for edge in self.edges:
            eid, src, tgt = edge['id'], edge['source'], edge['target']
            if src and src not in self.all_ids:
                self._error(f"source='{src}' 不存在", f"修改 source 或创建 id='{src}'", eid)
            if tgt and tgt not in self.all_ids:
                self._error(f"target='{tgt}' 不存在", f"修改 target 或创建 id='{tgt}'", eid)

    def _validate_styles(self):
        for cell in self.root.findall('.//mxCell'):
            cell_id = cell.get('id')
            style = cell.get('style', '')
            if not style or cell_id in ['0', '1']:
                continue
            if not style.endswith(';'):
                self._warn("style 末尾缺少分号", "添加 ';'", cell_id)

    def _check_overlapping(self):
        by_parent: Dict[str, List[Tuple[str, dict]]] = {}
        for nid, info in self.nodes.items():
            p = info.get('parent', '1')
            by_parent.setdefault(p, []).append((nid, info))

        for nodes in by_parent.values():
            for i, (id1, n1) in enumerate(nodes):
                for id2, n2 in nodes[i+1:]:
                    if (n1['x'] < n2['x'] + n2['width'] and
                        n1['x'] + n1['width'] > n2['x'] and
                        n1['y'] < n2['y'] + n2['height'] and
                        n1['y'] + n1['height'] > n2['y']):
                        self._warn(f"与 {id2} 重叠", f"调整 {id1} 或 {id2} 位置", id1)

    def _print_results(self):
        if self.nodes or self.edges:
            print(f"✅ {len(self.nodes)} 节点, {len(self.edges)} 连线, {self.page_count} 页面")

        print("\n" + "="*50)

        if self.errors:
            print(f"\n❌ 错误 ({len(self.errors)}):")
            for msg, fix, eid in self.errors:
                e = f" [{eid}]" if eid else ""
                print(f"  • {msg}{e}")
                print(f"    → {fix}")

        if self.warnings:
            print(f"\n⚠️  警告 ({len(self.warnings)}):")
            for msg, fix, eid in self.warnings[:10]:
                e = f" [{eid}]" if eid else ""
                print(f"  • {msg}{e}")
                print(f"    → {fix}")
            if len(self.warnings) > 10:
                print(f"  ... 还有 {len(self.warnings) - 10} 个")

        print("\n" + "="*50)
        print("✅ 通过" if not self.errors else "❌ 失败，请修复错误后重新验证")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    validator = DrawIOValidator(sys.argv[1])
    sys.exit(0 if validator.validate() else 1)


if __name__ == '__main__':
    main()
