#!/usr/bin/env python3
"""
测试用例相似度检测工具

功能：
1. 使用 Jaccard 相似度检测步骤相似的用例
2. 检测用例名称相似度（编辑距离）
3. 输出可疑重复对，供审查判断

用法：
    python detect_duplicates.py cases.jsonl
    python detect_duplicates.py cases.jsonl --threshold 0.7
    python detect_duplicates.py cases.jsonl --name-only
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict


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


def jaccard_similarity(set1: set, set2: set) -> float:
    """计算 Jaccard 相似度"""
    if not set1 and not set2:
        return 1.0
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union) if union else 0.0


def levenshtein_distance(s1: str, s2: str) -> int:
    """计算编辑距离"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # 插入、删除、替换的成本
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def name_similarity(name1: str, name2: str) -> float:
    """计算名称相似度（基于编辑距离）"""
    max_len = max(len(name1), len(name2))
    if max_len == 0:
        return 1.0
    distance = levenshtein_distance(name1, name2)
    return 1 - (distance / max_len)


def steps_similarity(steps1: List[Dict], steps2: List[Dict]) -> float:
    """计算步骤相似度（Jaccard）"""
    # 提取所有 action
    actions1 = set(step.get('action', '') for step in steps1 if step.get('action'))
    actions2 = set(step.get('action', '') for step in steps2 if step.get('action'))

    return jaccard_similarity(actions1, actions2)


def expected_similarity(steps1: List[Dict], steps2: List[Dict]) -> float:
    """计算预期结果相似度（Jaccard）"""
    # 提取所有 expected
    expected1 = set(step.get('expected', '') for step in steps1 if step.get('expected'))
    expected2 = set(step.get('expected', '') for step in steps2 if step.get('expected'))

    return jaccard_similarity(expected1, expected2)


def detect_duplicates(cases: List[Dict],
                     threshold: float = 0.7,
                     name_only: bool = False) -> List[Tuple[Dict, Dict, Dict]]:
    """
    检测重复或高度相似的测试用例

    Args:
        cases: 测试用例列表
        threshold: 相似度阈值（0-1）
        name_only: 只检查名称相似度

    Returns:
        List of (case1, case2, similarity_scores)
    """
    duplicates = []

    for i in range(len(cases)):
        for j in range(i + 1, len(cases)):
            case1 = cases[i]
            case2 = cases[j]

            name1 = case1.get('name', '')
            name2 = case2.get('name', '')

            # 计算名称相似度
            name_sim = name_similarity(name1, name2)

            if name_only:
                if name_sim >= threshold:
                    duplicates.append((case1, case2, {
                        'name_similarity': name_sim
                    }))
                continue

            # 计算步骤相似度
            steps1 = case1.get('steps', [])
            steps2 = case2.get('steps', [])

            steps_sim = steps_similarity(steps1, steps2)
            expected_sim = expected_similarity(steps1, steps2)

            # 综合相似度：名称 40% + 步骤 40% + 预期 20%
            overall_sim = (name_sim * 0.4 + steps_sim * 0.4 + expected_sim * 0.2)

            if overall_sim >= threshold:
                duplicates.append((case1, case2, {
                    'overall': overall_sim,
                    'name': name_sim,
                    'steps': steps_sim,
                    'expected': expected_sim
                }))

    return duplicates


def main():
    parser = argparse.ArgumentParser(
        description='测试用例相似度检测工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python detect_duplicates.py cases.jsonl
  python detect_duplicates.py cases.jsonl --threshold 0.8
  python detect_duplicates.py cases.jsonl --name-only
        """
    )
    parser.add_argument('file', type=Path, help='JSONL 文件')
    parser.add_argument('--threshold', type=float, default=0.7,
                       help='相似度阈值（0-1，默认 0.7）')
    parser.add_argument('--name-only', action='store_true',
                       help='仅检查名称相似度')

    args = parser.parse_args()

    if not args.file.exists():
        print(f"错误：文件不存在 {args.file}")
        sys.exit(1)

    # 加载用例
    cases = load_jsonl(args.file)

    if not cases:
        print("错误：文件为空或无有效用例")
        sys.exit(1)

    print(f"加载 {len(cases)} 条用例，开始检测...")
    print(f"相似度阈值：{args.threshold}")
    if args.name_only:
        print("模式：仅检查名称相似度")
    print()

    # 检测重复
    duplicates = detect_duplicates(cases, args.threshold, args.name_only)

    if not duplicates:
        print("✅ 未发现高度相似的用例")
        return

    # 输出结果
    print(f"⚠️  发现 {len(duplicates)} 对可疑相似用例：")
    print("="*80)

    for idx, (case1, case2, scores) in enumerate(duplicates, 1):
        print(f"\n【{idx}】可疑相似对")
        print(f"用例 1: {case1.get('name', '?')}")
        print(f"  - 模块: {case1.get('module_name', '?')}")
        print(f"  - 测试项: {case1.get('test_item', '?')}")
        print(f"  - 优先级: {case1.get('priority', '?')}")

        print(f"\n用例 2: {case2.get('name', '?')}")
        print(f"  - 模块: {case2.get('module_name', '?')}")
        print(f"  - 测试项: {case2.get('test_item', '?')}")
        print(f"  - 优先级: {case2.get('priority', '?')}")

        print(f"\n相似度：")
        if args.name_only:
            print(f"  - 名称: {scores['name_similarity']:.2%}")
        else:
            print(f"  - 综合: {scores['overall']:.2%}")
            print(f"  - 名称: {scores['name']:.2%}")
            print(f"  - 步骤: {scores['steps']:.2%}")
            print(f"  - 预期: {scores['expected']:.2%}")

        print("-"*80)

    print(f"\n汇总：")
    print(f"  - 总用例数: {len(cases)}")
    print(f"  - 可疑相似对: {len(duplicates)}")
    print(f"  - 相似度阈值: {args.threshold}")

    # 按模块分组统计
    module_counts = defaultdict(int)
    for case1, case2, _ in duplicates:
        module1 = case1.get('module_name', '?')
        module2 = case2.get('module_name', '?')
        if module1 == module2:
            module_counts[module1] += 1

    if module_counts:
        print(f"\n  - 同模块内相似对:")
        for module, count in sorted(module_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"    {module}: {count} 对")


if __name__ == '__main__':
    main()
