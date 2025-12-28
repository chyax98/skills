# Phase 6: 验证修正 (Validation & Refinement)

## 一、阶段目标

验证生成的 DrawIO XML 的正确性和质量，必要时进行迭代修正。

---

## 二、输入

来自 Phase 5 的 DrawIO XML 字符串或文件。

---

## 三、验证维度

### 3.1 结构验证

| 检查项 | 规则 | 严重程度 |
|--------|------|---------|
| XML 格式 | 符合 XML 1.0 规范 | 致命 |
| mxfile 结构 | 包含 `<mxfile><diagram><mxGraphModel><root>` | 致命 |
| 保留 ID | 存在 `id="0"` 和 `id="1"` 的 mxCell | 致命 |
| ID 唯一性 | 所有 mxCell 的 id 唯一 | 致命 |
| 节点属性 | 节点包含 `vertex="1"` | 错误 |
| 边属性 | 边包含 `edge="1"` | 错误 |
| 几何属性 | mxGeometry 包含 `as="geometry"` | 错误 |
| 边几何 | 边的 mxGeometry 包含 `relative="1"` | 警告 |
| 父节点引用 | parent 属性引用存在的 ID | 错误 |
| 边端点引用 | source/target 属性引用存在的 ID | 错误 |

### 3.2 布局验证

| 检查项 | 规则 | 严重程度 |
|--------|------|---------|
| 节点重叠 | 任意两节点间距 ≥ 20px | 警告 |
| 画布范围 | 节点在画布范围内 | 警告 |
| 坐标对齐 | 坐标是 10 的倍数 | 建议 |
| 尺寸合理 | width/height > 0 | 错误 |

### 3.3 质量验证

| 检查项 | 规则 | 严重程度 |
|--------|------|---------|
| 样式完整 | 每个节点有 style 属性 | 警告 |
| 标签存在 | 每个节点有 value 属性 | 建议 |
| 连线清晰 | 边有正交路由样式 | 建议 |

---

## 四、验证流程

```
DrawIO XML
    │
    ▼
┌─────────────────────────────────────┐
│  Step 1: XML 解析验证               │
│  • 使用 XML 解析器验证格式           │
│  • 检查基本结构                      │
└─────────────────────────────────────┘
    │ Pass / Fail
    ▼
┌─────────────────────────────────────┐
│  Step 2: 结构规则验证               │
│  • 检查必要元素                      │
│  • 检查 ID 唯一性和引用              │
└─────────────────────────────────────┘
    │ Pass / Warnings
    ▼
┌─────────────────────────────────────┐
│  Step 3: 布局质量验证               │
│  • 检测节点重叠                      │
│  • 检查画布范围                      │
└─────────────────────────────────────┘
    │ Pass / Warnings
    ▼
┌─────────────────────────────────────┐
│  Step 4: 汇总报告                    │
│  • 统计错误和警告                    │
│  • 生成修复建议                      │
└─────────────────────────────────────┘
    │
    ▼
ValidationResult
```

---

## 五、输出

### 5.1 ValidationResult 结构

```typescript
interface ValidationResult {
  // 是否通过验证
  passed: boolean;

  // 错误列表（致命和错误级别）
  errors: ValidationIssue[];

  // 警告列表
  warnings: ValidationIssue[];

  // 建议列表
  suggestions: ValidationIssue[];

  // 统计信息
  stats: {
    total_nodes: number;
    total_edges: number;
    overlapping_pairs: number;
    out_of_bounds_nodes: number;
  };

  // 修复建议
  fix_hints: FixHint[];
}

interface ValidationIssue {
  code: string;           // 错误代码
  message: string;        // 描述
  severity: 'fatal' | 'error' | 'warning' | 'suggestion';
  location?: {
    element_id?: string;
    line?: number;
  };
}

interface FixHint {
  issue_code: string;
  action: 'regenerate' | 'adjust_layout' | 'fix_style' | 'manual';
  description: string;
  target_phase?: number;  // 需要回退到哪个阶段
}
```

---

## 六、代码实现

### 6.1 validator.py

```python
"""
Phase 6: 验证修正模块
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional
from enum import Enum


class Severity(str, Enum):
    FATAL = 'fatal'
    ERROR = 'error'
    WARNING = 'warning'
    SUGGESTION = 'suggestion'


@dataclass
class ValidationIssue:
    code: str
    message: str
    severity: Severity
    element_id: Optional[str] = None
    line: Optional[int] = None


@dataclass
class FixHint:
    issue_code: str
    action: str
    description: str
    target_phase: Optional[int] = None


@dataclass
class ValidationResult:
    passed: bool
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)
    suggestions: List[ValidationIssue] = field(default_factory=list)
    stats: Dict = field(default_factory=dict)
    fix_hints: List[FixHint] = field(default_factory=list)


class DrawioValidator:
    """DrawIO XML 验证器"""

    def validate(self, xml_content: str) -> ValidationResult:
        """
        验证 DrawIO XML

        Args:
            xml_content: XML 字符串

        Returns:
            ValidationResult
        """
        result = ValidationResult(passed=True)

        # Step 1: XML 解析验证
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            result.passed = False
            result.errors.append(ValidationIssue(
                code='XML_PARSE_ERROR',
                message=f'XML 解析失败: {e}',
                severity=Severity.FATAL
            ))
            return result

        # Step 2: 结构验证
        self._validate_structure(root, result)

        # Step 3: 布局验证
        self._validate_layout(root, result)

        # 判断是否通过
        result.passed = len(result.errors) == 0

        # 生成修复建议
        self._generate_fix_hints(result)

        return result

    def _validate_structure(self, root: ET.Element, result: ValidationResult):
        """验证结构"""
        # 检查 mxfile 结构
        if root.tag != 'mxfile':
            result.errors.append(ValidationIssue(
                code='MISSING_MXFILE',
                message='根元素应为 mxfile',
                severity=Severity.FATAL
            ))
            return

        # 检查 diagram
        diagram = root.find('diagram')
        if diagram is None:
            result.errors.append(ValidationIssue(
                code='MISSING_DIAGRAM',
                message='缺少 diagram 元素',
                severity=Severity.FATAL
            ))
            return

        # 检查 mxGraphModel
        model = diagram.find('mxGraphModel')
        if model is None:
            result.errors.append(ValidationIssue(
                code='MISSING_MODEL',
                message='缺少 mxGraphModel 元素',
                severity=Severity.FATAL
            ))
            return

        # 检查 root
        graph_root = model.find('root')
        if graph_root is None:
            result.errors.append(ValidationIssue(
                code='MISSING_ROOT',
                message='缺少 root 元素',
                severity=Severity.FATAL
            ))
            return

        # 检查所有 mxCell
        cells = graph_root.findall('mxCell')
        ids: Set[str] = set()
        has_id_0 = False
        has_id_1 = False

        for cell in cells:
            cell_id = cell.get('id')

            # ID 唯一性
            if cell_id in ids:
                result.errors.append(ValidationIssue(
                    code='DUPLICATE_ID',
                    message=f'重复的 ID: {cell_id}',
                    severity=Severity.ERROR,
                    element_id=cell_id
                ))
            ids.add(cell_id)

            # 检查保留 ID
            if cell_id == '0':
                has_id_0 = True
            elif cell_id == '1':
                has_id_1 = True
            else:
                # 检查节点/边属性
                is_vertex = cell.get('vertex') == '1'
                is_edge = cell.get('edge') == '1'

                if not is_vertex and not is_edge:
                    result.warnings.append(ValidationIssue(
                        code='MISSING_TYPE',
                        message=f'mxCell {cell_id} 缺少 vertex 或 edge 属性',
                        severity=Severity.WARNING,
                        element_id=cell_id
                    ))

                # 检查几何
                geometry = cell.find('mxGeometry')
                if geometry is not None:
                    if geometry.get('as') != 'geometry':
                        result.errors.append(ValidationIssue(
                            code='MISSING_AS_GEOMETRY',
                            message=f'mxGeometry 缺少 as="geometry"',
                            severity=Severity.ERROR,
                            element_id=cell_id
                        ))

                    if is_edge and geometry.get('relative') != '1':
                        result.warnings.append(ValidationIssue(
                            code='MISSING_RELATIVE',
                            message=f'边 {cell_id} 的 mxGeometry 缺少 relative="1"',
                            severity=Severity.WARNING,
                            element_id=cell_id
                        ))

                # 检查 parent 引用
                parent_id = cell.get('parent')
                if parent_id and parent_id not in ids and parent_id not in ['0', '1']:
                    result.errors.append(ValidationIssue(
                        code='INVALID_PARENT_REF',
                        message=f'mxCell {cell_id} 的 parent={parent_id} 不存在',
                        severity=Severity.ERROR,
                        element_id=cell_id
                    ))

                # 检查 source/target 引用
                if is_edge:
                    source_id = cell.get('source')
                    target_id = cell.get('target')

                    if source_id and source_id not in ids:
                        result.errors.append(ValidationIssue(
                            code='INVALID_SOURCE_REF',
                            message=f'边 {cell_id} 的 source={source_id} 不存在',
                            severity=Severity.ERROR,
                            element_id=cell_id
                        ))

                    if target_id and target_id not in ids:
                        result.errors.append(ValidationIssue(
                            code='INVALID_TARGET_REF',
                            message=f'边 {cell_id} 的 target={target_id} 不存在',
                            severity=Severity.ERROR,
                            element_id=cell_id
                        ))

        # 检查保留 ID
        if not has_id_0:
            result.errors.append(ValidationIssue(
                code='MISSING_ID_0',
                message='缺少 id="0" 的 mxCell',
                severity=Severity.ERROR
            ))
        if not has_id_1:
            result.errors.append(ValidationIssue(
                code='MISSING_ID_1',
                message='缺少 id="1" 的 mxCell',
                severity=Severity.ERROR
            ))

        # 统计
        result.stats['total_cells'] = len(cells)
        result.stats['total_nodes'] = sum(1 for c in cells if c.get('vertex') == '1')
        result.stats['total_edges'] = sum(1 for c in cells if c.get('edge') == '1')

    def _validate_layout(self, root: ET.Element, result: ValidationResult):
        """验证布局"""
        model = root.find('.//mxGraphModel')
        if model is None:
            return

        # 获取画布尺寸
        canvas_width = int(model.get('pageWidth', 800))
        canvas_height = int(model.get('pageHeight', 600))

        # 收集所有节点位置
        nodes: List[Dict] = []
        graph_root = model.find('root')

        for cell in graph_root.findall('mxCell'):
            if cell.get('vertex') == '1' and cell.get('id') not in ['0', '1']:
                geometry = cell.find('mxGeometry')
                if geometry is not None:
                    x = float(geometry.get('x', 0))
                    y = float(geometry.get('y', 0))
                    w = float(geometry.get('width', 100))
                    h = float(geometry.get('height', 60))

                    nodes.append({
                        'id': cell.get('id'),
                        'x': x,
                        'y': y,
                        'width': w,
                        'height': h
                    })

                    # 检查尺寸
                    if w <= 0 or h <= 0:
                        result.errors.append(ValidationIssue(
                            code='INVALID_SIZE',
                            message=f'节点 {cell.get("id")} 尺寸无效: {w}x{h}',
                            severity=Severity.ERROR,
                            element_id=cell.get('id')
                        ))

                    # 检查画布范围
                    if x < 0 or y < 0 or x + w > canvas_width or y + h > canvas_height:
                        result.warnings.append(ValidationIssue(
                            code='OUT_OF_BOUNDS',
                            message=f'节点 {cell.get("id")} 超出画布范围',
                            severity=Severity.WARNING,
                            element_id=cell.get('id')
                        ))

                    # 检查坐标对齐
                    if x % 10 != 0 or y % 10 != 0:
                        result.suggestions.append(ValidationIssue(
                            code='NOT_GRID_ALIGNED',
                            message=f'节点 {cell.get("id")} 坐标未对齐网格',
                            severity=Severity.SUGGESTION,
                            element_id=cell.get('id')
                        ))

        # 检查节点重叠
        overlapping = 0
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i+1:]:
                if self._check_overlap(n1, n2):
                    overlapping += 1
                    result.warnings.append(ValidationIssue(
                        code='NODES_OVERLAP',
                        message=f'节点 {n1["id"]} 和 {n2["id"]} 重叠',
                        severity=Severity.WARNING
                    ))

        result.stats['overlapping_pairs'] = overlapping
        result.stats['out_of_bounds_nodes'] = len([
            i for i in result.warnings if i.code == 'OUT_OF_BOUNDS'
        ])

    def _check_overlap(self, n1: Dict, n2: Dict, margin: float = 20) -> bool:
        """检查两个节点是否重叠"""
        return not (
            n1['x'] + n1['width'] + margin < n2['x'] or
            n2['x'] + n2['width'] + margin < n1['x'] or
            n1['y'] + n1['height'] + margin < n2['y'] or
            n2['y'] + n2['height'] + margin < n1['y']
        )

    def _generate_fix_hints(self, result: ValidationResult):
        """生成修复建议"""
        for issue in result.errors:
            if issue.code in ['XML_PARSE_ERROR', 'MISSING_MXFILE', 'MISSING_MODEL']:
                result.fix_hints.append(FixHint(
                    issue_code=issue.code,
                    action='regenerate',
                    description='重新生成 XML (Phase 5)',
                    target_phase=5
                ))
            elif issue.code in ['INVALID_SOURCE_REF', 'INVALID_TARGET_REF']:
                result.fix_hints.append(FixHint(
                    issue_code=issue.code,
                    action='regenerate',
                    description='检查节点 ID 映射，重新生成 (Phase 5)',
                    target_phase=5
                ))

        for issue in result.warnings:
            if issue.code == 'NODES_OVERLAP':
                result.fix_hints.append(FixHint(
                    issue_code=issue.code,
                    action='adjust_layout',
                    description='增加节点间距，重新布局 (Phase 4)',
                    target_phase=4
                ))


def validate_drawio(file_path: str) -> ValidationResult:
    """验证 DrawIO 文件的便捷函数"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return DrawioValidator().validate(content)
```

---

## 七、迭代修复策略

### 7.1 修复流程

```
ValidationResult
    │
    ├─ passed = True → 完成 ✓
    │
    └─ passed = False
        │
        ▼
    ┌─────────────────────────────────────┐
    │  分析错误类型                        │
    │  • 结构错误 → 回退 Phase 5           │
    │  • 布局问题 → 回退 Phase 4           │
    │  • 样式问题 → 回退 Phase 3           │
    │  • 规划问题 → 回退 Phase 2           │
    └─────────────────────────────────────┘
        │
        ▼
    ┌─────────────────────────────────────┐
    │  执行修复                            │
    │  • 调整参数（如增加间距）             │
    │  • 重新执行目标阶段                  │
    └─────────────────────────────────────┘
        │
        ▼
    ┌─────────────────────────────────────┐
    │  重新验证                            │
    │  • 迭代次数 < 最大次数？             │
    │  • 是 → 重新验证                    │
    │  • 否 → 输出最佳结果 + 警告          │
    └─────────────────────────────────────┘
```

### 7.2 迭代控制

```python
def generate_with_validation(
    intent_result: dict,
    max_iterations: int = 3
) -> Tuple[str, ValidationResult]:
    """
    带验证的图表生成

    Args:
        intent_result: Phase 1 输出
        max_iterations: 最大迭代次数

    Returns:
        (XML 字符串, 验证结果)
    """
    for iteration in range(max_iterations):
        # Phase 2-5
        graph_spec = deep_planner.plan(intent_result)
        style_library = knowledge_retriever.retrieve(graph_spec)
        layout_result = layout_bridge.layout(graph_spec)
        xml = generator.generate(layout_result, style_library, graph_spec)

        # Phase 6
        validation = validator.validate(xml)

        if validation.passed:
            return xml, validation

        # 根据错误类型调整
        for hint in validation.fix_hints:
            if hint.target_phase == 4:
                # 调整布局参数
                increase_spacing(graph_spec)

        print(f"迭代 {iteration + 1}: {len(validation.errors)} 错误, 重试...")

    return xml, validation
```

---

## 八、与最终输出的关系

Phase 6 是最后一个阶段，验证通过后：

1. **保存文件** - 将 XML 写入 .drawio 文件
2. **返回结果** - 返回文件路径和验证报告
3. **用户反馈** - 如有警告，提示用户

---

## 九、参考

- [DrawIO XML Validation](https://www.drawio.com/doc/faq/diagram-source-edit)
- [XML Schema Validation](https://docs.python.org/3/library/xml.etree.elementtree.html)
