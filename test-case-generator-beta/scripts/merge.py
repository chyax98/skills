#!/usr/bin/env python3
"""
JSONL 合并工具

功能：
1. 合并多个 JSONL 文件
2. 从文件路径推断 module_name 和 test_item
3. 支持按模块、优先级排序
4. 自动去重

用法：
    python merge.py 需求名称/**/cases.jsonl -o 需求名称-测试用例.jsonl
    python merge.py 需求名称/**/cases.jsonl -o 需求名称-测试用例.jsonl --sort-by module
    python merge.py 需求名称/**/cases.jsonl -o 需求名称-测试用例.jsonl --sort-by priority
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any


def load_jsonl(file_path: Path) -> List[Dict]:
    """
    加载 JSONL 文件，并从路径推断 module_name 和 test_item

    路径格式：{workspace}/{模块}/{测试项}/cases.jsonl
    - module_name = 父目录的父目录名（仅当用例中不存在时）
    - test_item = 父目录名（仅当用例中不存在时）

    如果用例中已有这两个字段，则不覆盖（支持多次合并）
    """
    objects = []

    # 从路径推断元信息（备用值）
    # 目录结构：{workspace}/{模块}/{测试项}.jsonl
    # - 文件名（不含扩展名）= 测试项
    # - 父目录名 = 模块
    test_item_from_path = file_path.stem  # 文件名（不含扩展名）= 测试项
    module_name_from_path = file_path.parent.name  # 父目录名 = 模块

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    obj = json.loads(line)

                    # 只在字段不存在时才添加（避免覆盖已有值）
                    if 'module_name' not in obj:
                        obj['module_name'] = module_name_from_path
                    if 'test_item' not in obj:
                        obj['test_item'] = test_item_from_path

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
        deduplicate: 是否去重（基于 name 字段）

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
        objects_without_name = []

        for obj in all_objects:
            name = obj.get('name')
            if name:
                if name in unique_map:
                    print(f"警告：发现重复用例名称 '{name}'，保留第一个", file=sys.stderr)
                else:
                    unique_map[name] = obj
            else:
                # 没有 name 的对象单独保存
                objects_without_name.append(obj)

        all_objects = list(unique_map.values()) + objects_without_name

    return all_objects


def sort_objects(objects: List[Dict], sort_by: str) -> List[Dict]:
    """
    排序对象列表

    Args:
        objects: 对象列表
        sort_by: 排序依据（module, priority）

    Returns:
        排序后的对象列表
    """
    if sort_by == 'module':
        # 按模块名称 + 测试项 + 用例名称排序
        objects.sort(key=lambda x: (
            x.get('module_name', ''),
            x.get('test_item', ''),
            x.get('name', '')
        ))
    elif sort_by == 'priority':
        # 按优先级 + 模块名称 + 测试项 + 用例名称排序
        priority_order = {'P1': 1, 'P2': 2, 'P3': 3, 'P4': 4, 'P5': 5}
        objects.sort(key=lambda x: (
            priority_order.get(x.get('priority', 'P5'), 99),
            x.get('module_name', ''),
            x.get('test_item', ''),
            x.get('name', '')
        ))
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
        description='JSONL 合并工具 - 自动从路径推断 module_name 和 test_item',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python merge.py Frame相框管理/*/*.jsonl -o Frame相框管理-测试用例.jsonl
  python merge.py Frame相框管理/*/*.jsonl -o Frame相框管理-测试用例.jsonl --sort-by module
  python merge.py Frame相框管理/*/*.jsonl -o Frame相框管理-测试用例.jsonl --sort-by priority
  python merge.py Frame相框管理/*/*.jsonl -o Frame相框管理-测试用例.jsonl --deduplicate

路径格式：
  需求名称/模块名/测试项.jsonl
  - module_name 从父目录名推断
  - test_item 从文件名推断
        """
    )
    parser.add_argument('files', nargs='+', help='要合并的 JSONL 文件（支持通配符）')
    parser.add_argument('-o', '--output', type=Path, required=True, help='输出文件路径')
    parser.add_argument('--sort-by', choices=['module', 'priority'], help='排序方式')
    parser.add_argument('--deduplicate', action='store_true', help='去重（基于 name 字段）')

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
