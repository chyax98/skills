#!/usr/bin/env python3
"""
测试用例统计报告工具

功能：
1. 生成测试用例统计报告
2. 分析覆盖率、优先级分布、模块分布
3. 生成质量指标

用法：
    python stats_report.py cases.jsonl -o stats-report.md
    python stats_report.py cases.jsonl --test-points test-points.jsonl -o stats-report.md
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
from collections import defaultdict, Counter


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


def generate_stats_report(test_cases: List[Dict], test_points: List[Dict] = None) -> str:
    """
    生成统计报告

    Args:
        test_cases: 测试用例列表
        test_points: 测试点列表（可选）

    Returns:
        Markdown 格式的统计报告
    """
    lines = []

    # 标题
    lines.append("# 测试用例统计报告")
    lines.append("")

    # 总体统计
    lines.append("## 总体统计")
    lines.append("")

    total_cases = len(test_cases)
    lines.append(f"- 测试用例总数：{total_cases}")

    if test_points:
        total_points = len(test_points)
        lines.append(f"- 测试点总数：{total_points}")
        lines.append(f"- 平均每测试点用例数：{total_cases / total_points:.2f}")

    lines.append("")

    # 模块分布
    lines.append("## 模块分布")
    lines.append("")

    modules = defaultdict(list)
    for case in test_cases:
        module_name = case.get('module_name', '未分类')
        modules[module_name].append(case)

    lines.append("| 模块 | 测试用例 | 占比 |")
    lines.append("|------|---------|------|")

    for module_name, cases in sorted(modules.items(), key=lambda x: len(x[1]), reverse=True):
        count = len(cases)
        percentage = (count / total_cases) * 100 if total_cases > 0 else 0
        lines.append(f"| {module_name} | {count} | {percentage:.1f}% |")

    lines.append("")

    # 优先级分布
    lines.append("## 优先级分布")
    lines.append("")

    priorities = Counter([case.get('priority', 'P4') for case in test_cases])
    lines.append("| 优先级 | 数量 | 占比 |")
    lines.append("|--------|------|------|")

    for priority in ['P1', 'P2', 'P3', 'P4']:
        count = priorities.get(priority, 0)
        percentage = (count / total_cases) * 100 if total_cases > 0 else 0
        lines.append(f"| {priority} | {count} | {percentage:.1f}% |")

    lines.append("")

    # 测试类型分布
    lines.append("## 测试类型分布")
    lines.append("")

    test_types = Counter([case.get('test_type', '未知') for case in test_cases])
    lines.append("| 测试类型 | 数量 | 占比 |")
    lines.append("|---------|------|------|")

    for test_type, count in test_types.most_common():
        percentage = (count / total_cases) * 100 if total_cases > 0 else 0
        lines.append(f"| {test_type} | {count} | {percentage:.1f}% |")

    lines.append("")

    # 正向/反向用例分布
    lines.append("## 正向/反向用例分布")
    lines.append("")

    positive_count = sum(1 for case in test_cases if not case.get('is_negative', False))
    negative_count = total_cases - positive_count

    lines.append("| 类型 | 数量 | 占比 |")
    lines.append("|------|------|------|")
    lines.append(f"| 正向用例 | {positive_count} | {(positive_count / total_cases) * 100:.1f}% |")
    lines.append(f"| 反向用例 | {negative_count} | {(negative_count / total_cases) * 100:.1f}% |")
    lines.append("")

    # 建议
    lines.append("## 建议")
    lines.append("")

    # 建议 1：P1 用例覆盖
    p1_count = priorities.get('P1', 0)
    p1_percentage = (p1_count / total_cases) * 100 if total_cases > 0 else 0
    if 10 <= p1_percentage <= 20:
        lines.append(f"1. ✅ P1 用例占比合理（{p1_percentage:.1f}%）")
    elif p1_percentage < 10:
        lines.append(f"1. ⚠️  P1 用例占比偏低（{p1_percentage:.1f}%），建议补充核心功能正向用例")
    else:
        lines.append(f"1. ⚠️  P1 用例占比偏高（{p1_percentage:.1f}%），建议检查是否有误标")

    # 建议 2：反向用例覆盖
    negative_percentage = (negative_count / total_cases) * 100 if total_cases > 0 else 0
    if negative_percentage >= 15:
        lines.append(f"2. ✅ 反向用例覆盖率良好（{negative_percentage:.1f}%）")
    else:
        lines.append(f"2. ⚠️  反向用例覆盖率偏低（{negative_percentage:.1f}%），建议补充异常场景和边界条件测试")

    # 建议 3：测试类型多样性
    test_type_count = len(test_types)
    if test_type_count >= 3:
        lines.append(f"3. ✅ 测试类型多样（{test_type_count} 种），覆盖全面")
    else:
        lines.append(f"3. ⚠️  测试类型较少（{test_type_count} 种），建议补充性能、安全、兼容性等测试")

    lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='测试用例统计报告工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python stats_report.py cases.jsonl -o stats-report.md
  python stats_report.py cases.jsonl --test-points test-points.jsonl -o stats-report.md
        """
    )
    parser.add_argument('cases', type=Path, help='测试用例 JSONL 文件')
    parser.add_argument('-o', '--output', type=Path, required=True, help='输出报告文件路径')
    parser.add_argument('--test-points', type=Path, help='测试点 JSONL 文件（可选）')

    args = parser.parse_args()

    # 加载测试用例
    test_cases = load_jsonl(args.cases)

    if not test_cases:
        print("错误：测试用例文件为空")
        sys.exit(1)

    # 加载测试点（可选）
    test_points = None
    if args.test_points and args.test_points.exists():
        test_points = load_jsonl(args.test_points)

    # 生成报告
    report = generate_stats_report(test_cases, test_points)

    # 写入文件
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding='utf-8')

    print(f"✅ 已生成统计报告：{args.output}")

    # 控制台输出摘要
    print("\n" + "="*60)
    print("统计摘要：")
    print("="*60)
    print(f"测试用例总数：{len(test_cases)}")
    if test_points:
        print(f"测试点总数：{len(test_points)}")


if __name__ == '__main__':
    main()
