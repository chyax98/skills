#!/usr/bin/env python3
"""
DrawIO XML 结构验证脚本
用法: python validate_drawio.py <file.drawio>
"""

import xml.etree.ElementTree as ET
import sys
import re
from pathlib import Path


class DrawIOValidator:
    """DrawIO XML 验证器"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.errors = []      # 严重错误，必须修复
        self.warnings = []    # 警告，建议修复
        self.tree = None
        self.root = None
        self.nodes = {}       # id -> node info
        self.edges = []       # edge list

    def validate(self) -> bool:
        """执行全部验证，返回是否通过"""
        print(f"🔍 验证文件: {self.filepath}\n")

        # 1. 解析 XML
        if not self._parse_xml():
            return False

        # 2. 结构验证
        self._validate_structure()

        # 3. 节点验证
        self._validate_nodes()

        # 4. 连线验证
        self._validate_edges()

        # 5. 样式验证
        self._validate_styles()

        # 输出结果
        self._print_results()

        return len(self.errors) == 0

    def _parse_xml(self) -> bool:
        """解析 XML 文件"""
        try:
            self.tree = ET.parse(self.filepath)
            self.root = self.tree.getroot()
            print("✅ XML 语法正确")
            return True
        except ET.ParseError as e:
            self.errors.append(f"XML 解析失败: {e}")
            return False
        except FileNotFoundError:
            self.errors.append(f"文件不存在: {self.filepath}")
            return False

    def _validate_structure(self):
        """验证基础结构"""
        # 检查根元素
        if self.root.tag != 'mxfile':
            self.errors.append("根元素必须是 <mxfile>")
            return

        # 检查 diagram
        diagram = self.root.find('diagram')
        if diagram is None:
            self.errors.append("缺少 <diagram> 元素")
            return

        # 检查 mxGraphModel
        model = diagram.find('mxGraphModel')
        if model is None:
            self.errors.append("缺少 <mxGraphModel> 元素")
            return

        # 检查 root
        root_elem = model.find('root')
        if root_elem is None:
            self.errors.append("缺少 <root> 元素")
            return

        # 检查必须的 id="0" 和 id="1"
        cells = root_elem.findall('mxCell')
        ids = [cell.get('id') for cell in cells]

        if '0' not in ids:
            self.errors.append("缺少 id='0' 的根节点")
        if '1' not in ids:
            self.errors.append("缺少 id='1' 的默认图层")

        print("✅ 基础结构完整")

    def _validate_nodes(self):
        """验证所有节点"""
        root_elem = self.root.find('.//root')
        if root_elem is None:
            return

        all_ids = set()
        canvas_width = int(self.root.find('.//mxGraphModel').get('dx', 800))
        canvas_height = int(self.root.find('.//mxGraphModel').get('dy', 600))

        for cell in root_elem.findall('mxCell'):
            cell_id = cell.get('id')

            # ID 唯一性检查
            if cell_id in all_ids:
                self.errors.append(f"重复的 ID: {cell_id}")
            all_ids.add(cell_id)

            # 跳过根节点
            if cell_id in ['0', '1']:
                continue

            # 节点 (vertex)
            if cell.get('vertex') == '1':
                geom = cell.find('mxGeometry')
                if geom is None:
                    self.errors.append(f"节点 {cell_id} 缺少 <mxGeometry>")
                    continue

                # 检查 as="geometry"
                if geom.get('as') != 'geometry':
                    self.errors.append(f"节点 {cell_id} 的 mxGeometry 缺少 as='geometry'")

                # 坐标检查
                x = float(geom.get('x', 0))
                y = float(geom.get('y', 0))
                w = float(geom.get('width', 0))
                h = float(geom.get('height', 0))

                # 存储节点信息
                self.nodes[cell_id] = {'x': x, 'y': y, 'width': w, 'height': h}

                # 边界检查（相对坐标的子节点跳过）
                parent = cell.get('parent')
                if parent == '1':  # 只检查顶层节点
                    if x < 0 or y < 0:
                        self.warnings.append(f"节点 {cell_id} 坐标为负: ({x}, {y})")
                    if x + w > canvas_width + 100:  # 允许一定误差
                        self.warnings.append(f"节点 {cell_id} 超出画布右边界: x={x+w}")
                    if y + h > canvas_height + 100:
                        self.warnings.append(f"节点 {cell_id} 超出画布下边界: y={y+h}")

            # 连线 (edge)
            elif cell.get('edge') == '1':
                source = cell.get('source')
                target = cell.get('target')
                self.edges.append({
                    'id': cell_id,
                    'source': source,
                    'target': target,
                    'style': cell.get('style', '')
                })

                # 检查 geometry
                geom = cell.find('mxGeometry')
                if geom is not None and geom.get('as') != 'geometry':
                    self.errors.append(f"连线 {cell_id} 的 mxGeometry 缺少 as='geometry'")

        print(f"✅ 发现 {len(self.nodes)} 个节点, {len(self.edges)} 条连线")

    def _validate_edges(self):
        """验证连线"""
        for edge in self.edges:
            source = edge['source']
            target = edge['target']

            # 检查 source/target 是否存在
            if source and source not in self.nodes and source not in ['0', '1']:
                self.errors.append(f"连线 {edge['id']} 的 source='{source}' 不存在")
            if target and target not in self.nodes and target not in ['0', '1']:
                self.errors.append(f"连线 {edge['id']} 的 target='{target}' 不存在")

    def _validate_styles(self):
        """验证样式格式"""
        root_elem = self.root.find('.//root')
        if root_elem is None:
            return

        color_pattern = re.compile(r'#[0-9a-fA-F]{6}')

        for cell in root_elem.findall('mxCell'):
            cell_id = cell.get('id')
            style = cell.get('style', '')

            if not style:
                continue

            # 检查样式末尾分号
            if style and not style.endswith(';'):
                self.warnings.append(f"元素 {cell_id} 的 style 末尾缺少分号")

            # 检查颜色格式（建议小写）
            colors = color_pattern.findall(style)
            for color in colors:
                if color != color.lower():
                    self.warnings.append(f"元素 {cell_id} 的颜色建议使用小写: {color}")

    def _check_overlapping(self):
        """检查节点重叠（简化版）"""
        node_list = list(self.nodes.items())
        for i, (id1, n1) in enumerate(node_list):
            for id2, n2 in node_list[i+1:]:
                # 简单矩形重叠检测
                if (n1['x'] < n2['x'] + n2['width'] and
                    n1['x'] + n1['width'] > n2['x'] and
                    n1['y'] < n2['y'] + n2['height'] and
                    n1['y'] + n1['height'] > n2['y']):
                    self.warnings.append(f"节点 {id1} 和 {id2} 可能重叠")

    def _print_results(self):
        """输出验证结果"""
        print("\n" + "="*50)

        if self.errors:
            print(f"\n❌ 错误 ({len(self.errors)} 个) - 必须修复:")
            for i, err in enumerate(self.errors, 1):
                print(f"   {i}. {err}")

        if self.warnings:
            print(f"\n⚠️  警告 ({len(self.warnings)} 个) - 建议修复:")
            for i, warn in enumerate(self.warnings, 1):
                print(f"   {i}. {warn}")

        print("\n" + "="*50)
        if not self.errors:
            print("✅ 验证通过！文件可以正常导入 DrawIO")
        else:
            print("❌ 验证失败，请修复以上错误")


def main():
    if len(sys.argv) < 2:
        print("用法: python validate_drawio.py <file.drawio>")
        print("示例: python validate_drawio.py my_diagram.drawio")
        sys.exit(1)

    filepath = sys.argv[1]
    validator = DrawIOValidator(filepath)
    success = validator.validate()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
