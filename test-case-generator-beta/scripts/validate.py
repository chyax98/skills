#!/usr/bin/env python3
"""
JSONL 格式验证工具（极简 Schema）

功能：
1. 验证 JSONL 文件的 JSON 语法
2. 验证必填字段（name, priority, test_type, is_negative, preconditions, steps）
3. 验证字段格式（优先级 P1-P5、测试类型 13 种、步骤结构）
4. 检测重复用例名称

用法：
    python validate.py cases.jsonl
    python validate.py 需求名称/*/*.jsonl
"""

import json
import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter, defaultdict


class ValidationError:
    """验证错误（必须修复）"""
    def __init__(self, file_path: str, line_num: int, error_type: str, message: str, case_id: str = None):
        self.file_path = file_path
        self.line_num = line_num
        self.error_type = error_type
        self.message = message
        self.case_id = case_id

    def __str__(self):
        id_str = f" {self.case_id}" if self.case_id else ""
        return f"{self.file_path}:{self.line_num}{id_str} [{self.error_type}] {self.message}"


def load_jsonl(file_path: Path) -> Tuple[List[Tuple[int, Dict]], List[ValidationError]]:
    """加载 JSONL 文件"""
    objects = []
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate[str](f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                try:
                    obj = json.loads(line)
                    objects.append((line_num, obj))
                except json.JSONDecodeError as e:
                    errors.append(ValidationError(
                        str(file_path), line_num, "语法错误",
                        f"JSON 解析失败：{e}"
                    ))
    except Exception as e:
        errors.append(ValidationError(
            str(file_path), 0, "文件错误",
            f"无法读取文件：{e}"
        ))

    return objects, errors


def validate_business_rules(objects: List[Tuple[int, Dict]], file_path: Path) -> Tuple[List[ValidationError], List[ValidationError]]:
    """业务规则验证（极简 Schema）"""
    errors = []
    warnings = []

    # 必填字段
    required_fields = ['name', 'priority', 'test_type', 'is_negative', 'preconditions', 'steps']

    # 规则 1：用例名称唯一性
    names = [obj.get('name') for _, obj in objects if 'name' in obj]
    name_counts = Counter(names)
    for dup_name, count in name_counts.items():
        if count > 1:
            line_nums = [ln for ln, obj in objects if obj.get('name') == dup_name]
            errors.append(ValidationError(
                str(file_path), line_nums[0], "重复名称",
                f"用例名称 '{dup_name}' 重复，出现在行 {', '.join(map(str, line_nums))}"
            ))

    # 规则 2：必填字段验证
    for line_num, obj in objects:
        case_name = obj.get('name', '?')

        for field in required_fields:
            if field not in obj:
                errors.append(ValidationError(
                    str(file_path), line_num, "缺少字段",
                    f"缺少必填字段 '{field}'", case_name
                ))

    # 规则 3：优先级格式
    valid_priorities = {'P1', 'P2', 'P3', 'P4', 'P5'}
    for line_num, obj in objects:
        priority = obj.get('priority', '')
        case_name = obj.get('name', '?')
        if priority and priority not in valid_priorities:
            errors.append(ValidationError(
                str(file_path), line_num, "优先级格式",
                f"优先级 '{priority}' 无效，应为 P1-P5", case_name
            ))

    # 规则 4：is_negative 类型
    for line_num, obj in objects:
        is_negative = obj.get('is_negative')
        case_name = obj.get('name', '?')
        if is_negative is not None and not isinstance(is_negative, bool):
            errors.append(ValidationError(
                str(file_path), line_num, "类型错误",
                f"is_negative 应为布尔值，实际为 {type(is_negative).__name__}", case_name
            ))

    # 规则 4.5：test_type 有效性
    valid_test_types = {
        '功能测试', '安全性测试', '性能测试', '易用性测试',
        '兼容性测试', '稳定性测试', '集成测试', '可靠性测试',
        '可维护性测试', '可移植性测试', '埋点测试',
        'AI效果测试', '硬件效果测试'
    }
    for line_num, obj in objects:
        test_type = obj.get('test_type', '')
        case_name = obj.get('name', '?')
        if test_type and test_type not in valid_test_types:
            errors.append(ValidationError(
                str(file_path), line_num, "测试类型",
                f"test_type '{test_type}' 无效", case_name
            ))

    # 规则 5：preconditions 类型
    for line_num, obj in objects:
        preconditions = obj.get('preconditions')
        case_name = obj.get('name', '?')
        if preconditions is not None and not isinstance(preconditions, list):
            errors.append(ValidationError(
                str(file_path), line_num, "类型错误",
                f"preconditions 应为数组", case_name
            ))

    # 规则 6：steps 结构和验证点
    for line_num, obj in objects:
        if 'steps' not in obj:
            continue
        steps = obj['steps']
        case_name = obj.get('name', '?')

        if not isinstance(steps, list):
            errors.append(ValidationError(
                str(file_path), line_num, "类型错误",
                f"steps 应为数组", case_name
            ))
            continue

        if not steps:
            errors.append(ValidationError(
                str(file_path), line_num, "缺少步骤",
                f"steps 不能为空", case_name
            ))
            continue

        has_expected = False
        for i, step in enumerate(steps, 1):
            if not isinstance(step, dict):
                errors.append(ValidationError(
                    str(file_path), line_num, "格式错误",
                    f"步骤 {i} 应为对象", case_name
                ))
                continue
            if 'action' not in step:
                errors.append(ValidationError(
                    str(file_path), line_num, "格式错误",
                    f"步骤 {i} 缺少 action", case_name
                ))
            if step.get('expected'):
                has_expected = True

        if not has_expected:
            errors.append(ValidationError(
                str(file_path), line_num, "缺少验证点",
                f"至少一个步骤需要 expected", case_name
            ))

    # 规则 7：名称以"验证"开头（警告）
    for line_num, obj in objects:
        if 'name' in obj:
            name = obj['name']
            if not name.startswith('验证'):
                warnings.append(ValidationError(
                    str(file_path), line_num, "名称格式",
                    f"建议以'验证'开头：{name}"
                ))

    return errors, warnings


def validate_files(file_paths: List[Path]) -> Tuple[int, List[ValidationError], List[ValidationError]]:
    """验证多个文件"""
    total_objects = 0
    all_errors = []
    all_warnings = []

    for file_path in file_paths:
        objects, syntax_errors = load_jsonl(file_path)
        all_errors.extend(syntax_errors)

        if syntax_errors:
            continue

        total_objects += len(objects)

        errors, warnings = validate_business_rules(objects, file_path)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    return total_objects, all_errors, all_warnings


def main():
    parser = argparse.ArgumentParser(
        description='JSONL 验证工具（极简 Schema）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python validate.py 需求名称/*/*.jsonl
  python validate.py 需求名称/模块1/测试点1.jsonl
        """
    )
    parser.add_argument('files', nargs='+', help='JSONL 文件（支持通配符）')

    args = parser.parse_args()

    # 收集文件
    all_files = []
    for pattern in args.files:
        p = Path(pattern)
        if p.is_file():
            all_files.append(p)
        else:
            parent = p.parent if p.parent.exists() else Path('.')
            all_files.extend(parent.glob(p.name))

    if not all_files:
        print("错误：未找到文件")
        sys.exit(1)

    # 验证
    total, errors, warnings = validate_files(all_files)

    # 输出验证结果
    for f in all_files:
        objs, errs = load_jsonl(f)
        if errs:
            print(f"❌ {f}: 语法错误")
        elif errors:
            print(f"⚠️  {f}: {len(objs)} 条")
        else:
            print(f"✅ {f}: {len(objs)} 条")

    if errors:
        print(f"\n{'='*60}\n错误（必须修复）：\n{'='*60}")
        for e in errors:
            print(f"  {e}")

    if warnings:
        print(f"\n{'='*60}\n警告：\n{'='*60}")
        for w in warnings:
            print(f"  {w}")

    # 汇总
    print(f"\n{'='*60}\n汇总：\n{'='*60}")
    print(f"文件数：{len(all_files)}")
    print(f"用例数：{total}")
    print(f"错误：{len(errors)}")
    print(f"警告：{len(warnings)}")

    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
