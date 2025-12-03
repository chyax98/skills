#!/usr/bin/env python3
"""
JSONL 合并工具

功能：
1. 合并多个 JSONL 文件
2. 支持按模块、优先级、ID 排序
3. 自动去重

用法：
    python merge_jsonl.py cases/*.jsonl -o cases.jsonl
    python merge_jsonl.py cases/*.jsonl -o cases.jsonl --sort-by module
    python merge_jsonl.py cases/*.jsonl -o cases.jsonl --sort-by priority
    python merge_jsonl.py cases/*.jsonl -o cases.jsonl --deduplicate
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any


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

    return objects


def merge_jsonl_files(file_paths: List[Path], deduplicate: bool = False) -> List[Dict]:
    """
    合并多个 JSONL 文件

    Args:
        file_paths: JSONL 文件路径列表
        deduplicate: 是否去重（基于 ID）

    Returns:
        合并后的对象列表
    """
    all_objects = []

    for file_path in file_paths:
        objects = load_jsonl(file_path)
        all_objects.extend(objects)

    # 去重
    if deduplicate:
        unique_map = {}
        objects_without_id = []

        for obj in all_objects:
            obj_id = obj.get('id')
            if obj_id:
                if obj_id in unique_map:
                    print(f"警告：发现重复 ID '{obj_id}'，保留第一个", file=sys.stderr)
                else:
                    unique_map[obj_id] = obj
            else:
                # 没有 ID 的对象单独保存
                objects_without_id.append(obj)

        all_objects = list(unique_map.values()) + objects_without_id

    return all_objects


def sort_objects(objects: List[Dict], sort_by: str) -> List[Dict]:
    """
    排序对象列表

    Args:
        objects: 对象列表
        sort_by: 排序依据（module, priority, id）

    Returns:
        排序后的对象列表
    """
    if sort_by == 'module':
        # 按模块名称 + 对象 ID 排序
        objects.sort(key=lambda x: (
            x.get('module_name', ''),
            x.get('id', '')
        ))
    elif sort_by == 'priority':
        # 按优先级 + 模块名称 + 对象 ID 排序
        priority_order = {'P1': 1, 'P2': 2, 'P3': 3, 'P4': 4, 'P5': 5}
        objects.sort(key=lambda x: (
            priority_order.get(x.get('priority', 'P5'), 99),
            x.get('module_name', ''),
            x.get('id', '')
        ))
    elif sort_by == 'id':
        # 按对象 ID 排序
        objects.sort(key=lambda x: x.get('id', ''))
    else:
        print(f"警告：未知的排序方式 '{sort_by}'，跳过排序", file=sys.stderr)

    return objects


def write_jsonl(file_path: Path, objects: List[Dict]):
    """写入 JSONL 文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for obj in objects:
                line = json.dumps(obj, ensure_ascii=False)
                f.write(line + '\n')
        print(f"✅ 已写入 {len(objects)} 条记录到 {file_path}")
    except Exception as e:
        print(f"错误：无法写入文件 {file_path}：{e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='JSONL 合并工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python merge_jsonl.py cases/*.jsonl -o cases.jsonl
  python merge_jsonl.py cases/*.jsonl -o cases.jsonl --sort-by module
  python merge_jsonl.py cases/*.jsonl -o cases.jsonl --sort-by priority
  python merge_jsonl.py cases/*.jsonl -o cases.jsonl --deduplicate
        """
    )
    parser.add_argument('files', nargs='+', help='要合并的 JSONL 文件（支持通配符）')
    parser.add_argument('-o', '--output', type=Path, required=True, help='输出文件路径')
    parser.add_argument('--sort-by', choices=['module', 'priority', 'id'], help='排序方式')
    parser.add_argument('--deduplicate', action='store_true', help='去重（基于 ID）')

    args = parser.parse_args()

    # 收集所有文件
    all_files = []
    for file_pattern in args.files:
        file_path = Path(file_pattern)
        if file_path.is_file():
            all_files.append(file_path)
        else:
            # 处理通配符
            parent = file_path.parent if file_path.parent.exists() else Path('.')
            pattern = file_path.name
            matched = list(parent.glob(pattern))
            all_files.extend(matched)

    if not all_files:
        print("错误：未找到任何文件")
        sys.exit(1)

    print(f"合并 {len(all_files)} 个文件：")
    for file_path in all_files:
        print(f"  - {file_path}")

    # 合并文件
    all_objects = merge_jsonl_files(all_files, args.deduplicate)

    # 排序
    if args.sort_by:
        all_objects = sort_objects(all_objects, args.sort_by)
        print(f"✅ 已按 '{args.sort_by}' 排序")

    # 写入输出文件
    write_jsonl(args.output, all_objects)

    # 统计报告
    print("\n" + "="*60)
    print("合并报告：")
    print("="*60)
    print(f"输入文件数：{len(all_files)}")
    print(f"总记录数：{len(all_objects)}")
    if args.deduplicate:
        print("去重：已启用")
    if args.sort_by:
        print(f"排序方式：{args.sort_by}")
    print(f"输出文件：{args.output}")


if __name__ == '__main__':
    main()
