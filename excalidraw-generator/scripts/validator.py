#!/usr/bin/env python3
"""
Excalidraw JSON 验证工具

验证生成的 .excalidraw 文件是否符合规范
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


class ExcalidrawValidator:
    """Excalidraw 文件验证器"""

    REQUIRED_TOP_LEVEL = {"type", "version", "elements"}
    REQUIRED_ELEMENT_PROPS = {
        "type", "id", "x", "y", "width", "height", "angle",
        "strokeColor", "backgroundColor", "fillStyle", "strokeWidth",
        "strokeStyle", "roughness", "opacity", "groupIds", "frameId",
        "seed", "version", "versionNonce", "isDeleted", "boundElements",
        "updated", "link", "locked"
    }
    SHAPE_TYPES = {"rectangle", "ellipse", "diamond"}
    LINEAR_TYPES = {"arrow", "line"}
    VALID_TYPES = {"rectangle", "ellipse", "diamond", "arrow", "line", "text", "frame", "freedraw", "image"}
    VALID_FILL_STYLES = {"solid", "hachure", "cross-hatch", "zigzag"}
    VALID_STROKE_STYLES = {"solid", "dashed", "dotted"}
    VALID_ARROWHEADS = {None, "arrow", "triangle", "triangle_outline", "diamond", "diamond_outline", "dot", "circle", "circle_outline", "bar"}

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.data: dict[str, Any] | None = None

    def validate(self) -> bool:
        """执行所有验证，返回是否通过"""
        print(f"\n验证文件: {self.file_path}")
        print("=" * 50)

        # 1. 文件存在性
        if not self.file_path.exists():
            self.errors.append(f"文件不存在: {self.file_path}")
            return self._report()

        # 2. JSON 解析
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON 解析错误: {e}")
            return self._report()

        # 3. 顶层结构验证
        self._validate_top_level()

        if self.data is None or "elements" not in self.data:
            return self._report()

        # 4. 元素验证
        self._validate_elements()

        # 5. 引用验证
        self._validate_references()

        # 6. 框架顺序验证
        self._validate_frame_order()

        return self._report()

    def _validate_top_level(self) -> None:
        """验证顶层结构"""
        if self.data is None:
            return

        # 检查必需字段
        for field in self.REQUIRED_TOP_LEVEL:
            if field not in self.data:
                self.errors.append(f"缺少必需字段: {field}")

        # 检查 type
        if self.data.get("type") != "excalidraw":
            self.errors.append(f'type 应为 "excalidraw"，实际为: {self.data.get("type")}')

        # 检查 version
        if self.data.get("version") != 2:
            self.warnings.append(f'version 建议为 2，实际为: {self.data.get("version")}')

        # 检查 elements 是否为数组
        if "elements" in self.data and not isinstance(self.data["elements"], list):
            self.errors.append("elements 必须是数组")

    def _validate_elements(self) -> None:
        """验证所有元素"""
        if self.data is None:
            return

        elements = self.data.get("elements", [])
        seen_ids: set[str] = set()

        for i, elem in enumerate(elements):
            elem_id = elem.get("id", f"<index:{i}>")

            # 检查 ID 唯一性
            if "id" in elem:
                if elem["id"] in seen_ids:
                    self.errors.append(f"元素 {elem_id}: ID 重复")
                seen_ids.add(elem["id"])

            # 检查类型
            elem_type = elem.get("type")
            if elem_type not in self.VALID_TYPES:
                self.errors.append(f"元素 {elem_id}: 无效类型 '{elem_type}'")
                continue

            # 检查必需属性
            self._validate_element_props(elem, elem_id)

            # 类型特定验证
            if elem_type in self.LINEAR_TYPES:
                self._validate_linear_element(elem, elem_id)
            elif elem_type == "text":
                self._validate_text_element(elem, elem_id)
            elif elem_type == "frame":
                self._validate_frame_element(elem, elem_id)

    def _validate_element_props(self, elem: dict, elem_id: str) -> None:
        """验证元素必需属性"""
        elem_type = elem.get("type")
        required = self.REQUIRED_ELEMENT_PROPS.copy()

        # 文本元素有额外必需属性
        if elem_type == "text":
            required.update({"text", "fontSize", "fontFamily", "textAlign", "verticalAlign"})

        # 线性元素有额外必需属性
        if elem_type in self.LINEAR_TYPES:
            required.add("points")

        for prop in required:
            if prop not in elem:
                self.warnings.append(f"元素 {elem_id}: 缺少属性 '{prop}'")

        # 验证样式值
        fill_style = elem.get("fillStyle")
        if fill_style and fill_style not in self.VALID_FILL_STYLES:
            self.warnings.append(f"元素 {elem_id}: fillStyle '{fill_style}' 可能无效")

        stroke_style = elem.get("strokeStyle")
        if stroke_style and stroke_style not in self.VALID_STROKE_STYLES:
            self.warnings.append(f"元素 {elem_id}: strokeStyle '{stroke_style}' 可能无效")

        # 验证 seed 和 versionNonce 是数字
        for num_field in ["seed", "versionNonce"]:
            if num_field in elem and not isinstance(elem[num_field], (int, float)):
                self.errors.append(f"元素 {elem_id}: {num_field} 必须是数字")

    def _validate_linear_element(self, elem: dict, elem_id: str) -> None:
        """验证线性元素（箭头/直线）"""
        points = elem.get("points", [])

        # 检查 points 数组
        if not isinstance(points, list):
            self.errors.append(f"元素 {elem_id}: points 必须是数组")
            return

        if len(points) < 2:
            self.errors.append(f"元素 {elem_id}: points 至少需要 2 个点")
            return

        # 检查第一个点是否为 [0, 0]
        if len(points) > 0:
            first_point = points[0]
            if not isinstance(first_point, list) or len(first_point) < 2:
                self.errors.append(f"元素 {elem_id}: points[0] 格式错误")
            elif first_point[0] != 0 or first_point[1] != 0:
                self.errors.append(f"元素 {elem_id}: points[0] 必须是 [0, 0]，实际为 {first_point}")

        # 检查箭头头样式
        if elem.get("type") == "arrow":
            for arrowhead in ["startArrowhead", "endArrowhead"]:
                val = elem.get(arrowhead)
                if val not in self.VALID_ARROWHEADS:
                    self.warnings.append(f"元素 {elem_id}: {arrowhead} '{val}' 可能无效")

    def _validate_text_element(self, elem: dict, elem_id: str) -> None:
        """验证文本元素"""
        # 检查 fontFamily
        font_family = elem.get("fontFamily")
        if font_family is not None and font_family not in {1, 2, 3, 4}:
            self.warnings.append(f"元素 {elem_id}: fontFamily {font_family} 可能无效 (应为 1-4)")

        # 检查 textAlign
        text_align = elem.get("textAlign")
        if text_align and text_align not in {"left", "center", "right"}:
            self.warnings.append(f"元素 {elem_id}: textAlign '{text_align}' 可能无效")

        # 检查 verticalAlign
        vertical_align = elem.get("verticalAlign")
        if vertical_align and vertical_align not in {"top", "middle", "bottom"}:
            self.warnings.append(f"元素 {elem_id}: verticalAlign '{vertical_align}' 可能无效")

        # 注意: baseline 属性在 v0.18.0 已废弃，不再检查

    def _validate_frame_element(self, elem: dict, elem_id: str) -> None:
        """验证框架元素"""
        if "name" not in elem:
            self.warnings.append(f"元素 {elem_id}: 框架缺少 name 属性")

    def _validate_references(self) -> None:
        """验证引用关系"""
        if self.data is None:
            return

        elements = self.data.get("elements", [])
        element_ids = {e.get("id") for e in elements if "id" in e}

        for elem in elements:
            elem_id = elem.get("id", "<unknown>")

            # 验证 binding 引用
            for binding_key in ["startBinding", "endBinding"]:
                binding = elem.get(binding_key)
                if binding and isinstance(binding, dict):
                    ref_id = binding.get("elementId")
                    if ref_id and ref_id not in element_ids:
                        self.errors.append(f"元素 {elem_id}: {binding_key}.elementId '{ref_id}' 引用不存在")

            # 验证 containerId
            container_id = elem.get("containerId")
            if container_id and container_id not in element_ids:
                self.errors.append(f"元素 {elem_id}: containerId '{container_id}' 引用不存在")

            # 验证 frameId
            frame_id = elem.get("frameId")
            if frame_id and frame_id not in element_ids:
                self.errors.append(f"元素 {elem_id}: frameId '{frame_id}' 引用不存在")

            # 验证 boundElements 双向关系
            bound_elements = elem.get("boundElements", [])
            if isinstance(bound_elements, list):
                for be in bound_elements:
                    if isinstance(be, dict):
                        be_id = be.get("id")
                        be_type = be.get("type")
                        if be_id and be_id not in element_ids:
                            self.errors.append(f"元素 {elem_id}: boundElements 引用 '{be_id}' 不存在")
                        # 检查双向关系
                        if be_id and be_type == "text":
                            text_elem = next((e for e in elements if e.get("id") == be_id), None)
                            if text_elem and text_elem.get("containerId") != elem_id:
                                self.warnings.append(f"元素 {elem_id}: boundElements 包含文本 '{be_id}'，但文本的 containerId 不匹配")

    def _validate_frame_order(self) -> None:
        """验证框架出现在子元素之后"""
        if self.data is None:
            return

        elements = self.data.get("elements", [])
        frame_positions: dict[str, int] = {}
        child_positions: dict[str, list[int]] = {}

        for i, elem in enumerate(elements):
            elem_id = elem.get("id")
            if elem.get("type") == "frame" and elem_id:
                frame_positions[elem_id] = i
                child_positions[elem_id] = []

            frame_id = elem.get("frameId")
            if frame_id:
                if frame_id not in child_positions:
                    child_positions[frame_id] = []
                child_positions[frame_id].append(i)

        for frame_id, frame_pos in frame_positions.items():
            children = child_positions.get(frame_id, [])
            for child_pos in children:
                if child_pos > frame_pos:
                    self.warnings.append(f"框架 '{frame_id}' (位置 {frame_pos}) 应在其子元素之后 (子元素位置 {child_pos})")

    def _report(self) -> bool:
        """输出验证报告"""
        passed = len(self.errors) == 0

        if self.errors:
            print("\n错误:")
            for err in self.errors:
                print(f"  - {err}")

        if self.warnings:
            print("\n警告:")
            for warn in self.warnings:
                print(f"  - {warn}")

        if passed and not self.warnings:
            print("\n验证通过!")
        elif passed:
            print(f"\n验证通过 (有 {len(self.warnings)} 个警告)")
        else:
            print(f"\n验证失败: {len(self.errors)} 个错误, {len(self.warnings)} 个警告")

        print("=" * 50)
        return passed


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python validator.py <file.excalidraw> [file2.excalidraw ...]")
        print("\n示例:")
        print("  python validator.py output.excalidraw")
        print("  python validator.py ../assets/*.excalidraw")
        sys.exit(1)

    all_passed = True
    for file_path in sys.argv[1:]:
        validator = ExcalidrawValidator(file_path)
        if not validator.validate():
            all_passed = False

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
