#!/usr/bin/env python3
"""
解析模块 README.md 中的测试项规划表格

用法：
    python3 parse_readme.py <README.md路径>
"""

import re
import sys
import argparse
from pathlib import Path


def parse_readme(readme_path):
    """
    解析 README.md 中的测试项规划表格

    参数:
        readme_path: README.md 文件路径

    返回:
        list[dict]: 测试项列表，每项包含 test_item, function_level, expected_positive,
                    expected_negative, expected_total, actual_count, status
    """
    content = Path(readme_path).read_text(encoding='utf-8')

    # 提取模块名称（# 标题）
    module_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    module_name = module_match.group(1).strip() if module_match else "未知模块"

    # 查找测试项规划表格
    # 匹配 ## 测试项规划 后面的表格
    table_pattern = r'##\s+测试项规划\s*\n\s*\|.+\|.+\n\s*\|[-:\s|]+\|\s*\n((?:\|.+\|\s*\n)+)'
    table_match = re.search(table_pattern, content, re.MULTILINE)

    if not table_match:
        return {
            'module_name': module_name,
            'test_items': []
        }

    table_content = table_match.group(1)

    # 解析表格行
    test_items = []
    for line in table_content.strip().split('\n'):
        line = line.strip()
        if not line or not line.startswith('|'):
            continue

        # 分割单元格
        cells = [cell.strip() for cell in line.split('|')[1:-1]]

        if len(cells) < 7:
            continue

        test_item = {
            'test_item': cells[0],
            'function_level': cells[1],  # 核心功能/基本功能/不常用功能
            'expected_positive': int(cells[2]) if cells[2].isdigit() else 0,
            'expected_negative': int(cells[3]) if cells[3].isdigit() else 0,
            'expected_total': int(cells[4]) if cells[4].isdigit() else 0,
            'actual_count': int(cells[5]) if cells[5].isdigit() else 0,
            'status': cells[6]  # ⬜/✅
        }

        test_items.append(test_item)

    return {
        'module_name': module_name,
        'test_items': test_items
    }


def main():
    parser = argparse.ArgumentParser(description='解析模块 README.md 中的测试项规划表格')
    parser.add_argument('readme', type=Path, help='README.md 文件路径')
    parser.add_argument('--json', action='store_true', help='以 JSON 格式输出')

    args = parser.parse_args()

    if not args.readme.exists():
        print(f"❌ 文件不存在: {args.readme}")
        sys.exit(1)

    result = parse_readme(args.readme)

    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"模块名称: {result['module_name']}")
        print(f"测试项数量: {len(result['test_items'])}")
        print()

        if result['test_items']:
            print(f"{'测试项':<20} {'功能等级':<10} {'正向':<6} {'异常':<6} {'预估':<6} {'实际':<6} {'状态':<4}")
            print("-" * 70)
            for item in result['test_items']:
                print(f"{item['test_item']:<20} {item['function_level']:<10} "
                      f"{item['expected_positive']:<6} {item['expected_negative']:<6} "
                      f"{item['expected_total']:<6} {item['actual_count']:<6} {item['status']:<4}")
        else:
            print("⚠️  未找到测试项规划表格")


if __name__ == '__main__':
    main()
