#!/usr/bin/env python3
"""
JSONL 转 XMind 思维导图工具

功能：
1. 将 JSONL 格式的测试用例转换为 XMind 思维导图
2. 支持按模块和测试点分层展示
3. 支持优先级图标标记
4. 步骤与预期结果形成父子结构

用法：
    python convert_to_xmind.py cases.jsonl -o output.xmind
    python convert_to_xmind.py cases.jsonl -o output.xmind --name "用户管理"
    python convert_to_xmind.py cases.jsonl -o output.xmind --flat

依赖：
    pip install xmind
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict
from collections import defaultdict

try:
    import xmind
    from xmind.core.workbook import WorkbookDocument
except ImportError:
    print("错误：需要安装 xmind 库")
    print("执行：pip install xmind")
    sys.exit(1)


# 优先级映射：P1-P5 对应 XMind 的 priority-1 到 priority-5
PRIORITY_MAP = {
    "P1": "priority-1",
    "P2": "priority-2",
    "P3": "priority-3",
    "P4": "priority-4",
    "P5": "priority-5"
}


def load_jsonl(file_path: Path) -> List[Dict]:
    """加载 JSONL 文件"""
    objects = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    obj = json.loads(line)
                    objects.append(obj)
                except json.JSONDecodeError as e:
                    print(f"警告：{file_path}:{line_num} JSON 解析失败：{e}", file=sys.stderr)
                    continue
    except Exception as e:
        print(f"错误：无法读取文件 {file_path}：{e}", file=sys.stderr)
        sys.exit(1)

    return objects


def group_by_module(test_cases: List[Dict]) -> Dict[str, Dict[str, List[Dict]]]:
    """
    按模块和测试点分组

    返回结构：{module_name: {test_point_name: [cases]}}
    """
    structure = defaultdict(lambda: defaultdict(list))
    for case in test_cases:
        module = case.get('module_name', '未命名模块')
        point = case.get('test_point_name', '默认测试点')
        structure[module][point].append(case)
    return structure


def build_case_node(parent_topic, case: Dict):
    """
    构建单个用例节点

    结构：
    用例节点（带优先级图标）
    ├── 测试项
    ├── 前置条件
    ├── 步骤1
    │   └── 预期结果1
    ├── 步骤2
    │   └── 预期结果2
    └── 备注
    """
    # 用例节点
    case_id = case.get('id', '')
    name = case.get('name', '')
    title = f"{case_id} {name}".strip()

    case_topic = parent_topic.addSubTopic()
    case_topic.setTitle(title)

    # 优先级图标
    priority = case.get('priority')
    if priority in PRIORITY_MAP:
        case_topic.addMarker(PRIORITY_MAP[priority])

    # 反向用例标记
    if case.get('is_negative'):
        case_topic.addMarker('symbol-wrong')

    # 测试项
    test_type = case.get('test_type')
    if test_type:
        node = case_topic.addSubTopic()
        node.setTitle(f"测试项： {test_type}")

    # 前置条件
    preconditions = case.get('preconditions', [])
    if preconditions:
        content = " ".join(preconditions)
        node = case_topic.addSubTopic()
        node.setTitle(f"前置条件： {content}")

    # 步骤与预期结果（父子结构）
    steps = case.get('steps', [])
    for i, step in enumerate(steps, 1):
        action = step.get('action', '')
        expected = step.get('expected', '')

        # 步骤节点
        step_topic = case_topic.addSubTopic()
        step_topic.setTitle(f"步骤： {i} {action}")

        # 预期结果节点（挂在步骤下）
        if expected:
            exp_topic = step_topic.addSubTopic()
            exp_topic.setTitle(f"预期结果： {i} {expected}")

    # 备注
    notes = case.get('notes')
    if notes:
        node = case_topic.addSubTopic()
        node.setTitle(f"备注： {notes}")


def convert_to_xmind(
    test_cases: List[Dict],
    output_path: Path,
    root_name: str = "测试用例",
    flat_mode: bool = False
):
    """
    转换测试用例为 XMind 思维导图

    Args:
        test_cases: 测试用例列表
        output_path: 输出文件路径
        root_name: 根节点名称
        flat_mode: 扁平模式（跳过测试点层级）
    """
    # 创建工作簿
    workbook = xmind.load(str(output_path))
    sheet = workbook.getPrimarySheet()
    sheet.setTitle("测试用例")

    # 根节点
    root = sheet.getRootTopic()
    root.setTitle(root_name)

    # 按模块分组
    grouped = group_by_module(test_cases)

    for module_name in sorted(grouped.keys()):
        points = grouped[module_name]

        # 模块节点
        mod_topic = root.addSubTopic()
        mod_topic.setTitle(module_name)

        for point_name in sorted(points.keys()):
            cases = points[point_name]

            # 判断是否需要测试点层级
            # 条件：flat 模式、测试点名与模块名相同、或为默认测试点
            skip_point_level = (
                flat_mode or
                point_name == module_name or
                point_name == "默认测试点"
            )

            if skip_point_level:
                parent_for_case = mod_topic
            else:
                point_topic = mod_topic.addSubTopic()
                point_topic.setTitle(point_name)
                parent_for_case = point_topic

            # 用例节点
            for case in cases:
                build_case_node(parent_for_case, case)

    # 保存
    xmind.save(workbook, str(output_path))


def print_stats(test_cases: List[Dict], output_path: Path):
    """打印统计信息"""
    # 按优先级统计
    priority_count = defaultdict(int)
    for case in test_cases:
        priority_count[case.get('priority', 'N/A')] += 1

    # 按模块统计
    module_count = defaultdict(int)
    for case in test_cases:
        module_count[case.get('module_name', '未分类')] += 1

    print("\n" + "=" * 60)
    print("转换报告：")
    print("=" * 60)
    print(f"用例总数：{len(test_cases)}")
    print(f"输出文件：{output_path}")
    print()
    print("按优先级：")
    for p in ['P1', 'P2', 'P3', 'P4', 'P5']:
        if priority_count[p] > 0:
            print(f"  {p}: {priority_count[p]} 条")
    print()
    print("按模块：")
    for module, count in sorted(module_count.items()):
        print(f"  {module}: {count} 条")


def main():
    parser = argparse.ArgumentParser(
        description='JSONL 转 XMind 思维导图工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python convert_to_xmind.py cases.jsonl -o output.xmind
  python convert_to_xmind.py cases.jsonl -o output.xmind --name "用户管理"
  python convert_to_xmind.py cases.jsonl -o output.xmind --flat
        """
    )
    parser.add_argument('input', type=Path, help='输入 JSONL 文件')
    parser.add_argument('-o', '--output', type=Path, required=True, help='输出 XMind 文件路径')
    parser.add_argument('--name', default='测试用例', help='根节点名称（默认：测试用例）')
    parser.add_argument('--flat', action='store_true', help='扁平模式：跳过测试点层级，用例直接挂在模块下')

    args = parser.parse_args()

    # 检查输入文件
    if not args.input.exists():
        print(f"错误：文件不存在 {args.input}")
        sys.exit(1)

    # 加载数据
    test_cases = load_jsonl(args.input)

    if not test_cases:
        print("错误：JSONL 文件为空")
        sys.exit(1)

    # 确保输出目录存在
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # 转换
    convert_to_xmind(
        test_cases,
        args.output,
        root_name=args.name,
        flat_mode=args.flat
    )

    print(f"转换完成：{args.output}")
    print_stats(test_cases, args.output)


if __name__ == '__main__':
    main()
