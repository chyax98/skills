#!/usr/bin/env python3
"""
JSONL 格式验证工具

功能：
1. 验证 JSONL 文件的 JSON 语法
2. 验证是否符合 JSON Schema
3. 验证业务规则（ID 唯一性、格式规范、内容质量）

用法：
    python validate_jsonl.py test-items.jsonl
    python validate_jsonl.py cases.jsonl
    python validate_jsonl.py cases.jsonl --strict
    python validate_jsonl.py cases/*.jsonl --strict
    python validate_jsonl.py cases.jsonl --schema test-case.schema.json
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import Counter

try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    print("警告：jsonschema 未安装，将跳过 Schema 验证")
    print("安装方法：pip install jsonschema")


class ValidationError:
    """验证错误"""
    def __init__(self, file_path: str, line_num: int, error_type: str, message: str):
        self.file_path = file_path
        self.line_num = line_num
        self.error_type = error_type
        self.message = message

    def __str__(self):
        return f"{self.file_path}:{self.line_num} [{self.error_type}] {self.message}"


class ValidationWarning:
    """验证警告"""
    def __init__(self, file_path: str, line_num: int, warning_type: str, message: str):
        self.file_path = file_path
        self.line_num = line_num
        self.warning_type = warning_type
        self.message = message

    def __str__(self):
        return f"{self.file_path}:{self.line_num} [{self.warning_type}] {self.message}"


def validate_json_syntax(file_path: Path) -> Tuple[List[Dict], List[ValidationError]]:
    """
    第 1 层：JSON 语法验证

    Returns:
        (objects, errors)
    """
    objects = []
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    obj = json.loads(line)
                    objects.append((line_num, obj))
                except json.JSONDecodeError as e:
                    errors.append(ValidationError(
                        str(file_path),
                        line_num,
                        "语法错误",
                        f"JSON 解析失败：{e}"
                    ))
    except Exception as e:
        errors.append(ValidationError(
            str(file_path),
            0,
            "文件错误",
            f"无法读取文件：{e}"
        ))

    return objects, errors


def validate_schema(objects: List[Tuple[int, Dict]], file_path: Path, schema_path: Path = None) -> List[ValidationError]:
    """
    第 2 层：Schema 验证

    Args:
        objects: [(line_num, obj), ...]
        file_path: JSONL 文件路径
        schema_path: JSON Schema 文件路径

    Returns:
        errors
    """
    if not JSONSCHEMA_AVAILABLE:
        return []

    errors = []

    # 自动推断 Schema 文件
    if schema_path is None:
        script_dir = Path(__file__).parent

        # 检查文件名判断类型
        file_name = file_path.name.lower()
        if 'test-item' in file_name or 'testitem' in file_name:
            schema_path = script_dir / 'test-item.schema.json'
        elif 'case' in file_name:
            schema_path = script_dir / 'test-case.schema.json'
        else:
            # 尝试从第一个对象推断
            if objects:
                _, first_obj = objects[0]
                if 'module_id' in first_obj and 'test_items' in first_obj:
                    schema_path = script_dir / 'test-item.schema.json'
                elif 'test_item' in first_obj and 'scenario_type' in first_obj:
                    schema_path = script_dir / 'test-case.schema.json'

    if schema_path is None or not schema_path.exists():
        errors.append(ValidationError(
            str(file_path),
            0,
            "Schema 错误",
            f"无法找到 Schema 文件：{schema_path}"
        ))
        return errors

    # 加载 Schema
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except Exception as e:
        errors.append(ValidationError(
            str(file_path),
            0,
            "Schema 错误",
            f"无法加载 Schema 文件：{e}"
        ))
        return errors

    # 验证每个对象
    for line_num, obj in objects:
        try:
            jsonschema.validate(obj, schema)
        except jsonschema.ValidationError as e:
            # 提取关键错误信息
            error_path = ' -> '.join(str(p) for p in e.path) if e.path else '根对象'
            errors.append(ValidationError(
                str(file_path),
                line_num,
                "Schema 错误",
                f"{error_path}: {e.message}"
            ))

    return errors


def validate_business_rules(objects: List[Tuple[int, Dict]], file_path: Path) -> Tuple[List[ValidationError], List[ValidationWarning]]:
    """
    第 3 层：业务规则验证

    Args:
        objects: [(line_num, obj), ...]
        file_path: JSONL 文件路径

    Returns:
        (errors, warnings)
    """
    errors = []
    warnings = []

    # 提取所有对象（不含行号）
    objs = [obj for _, obj in objects]

    # 规则 1：ID 唯一性检查
    ids = [obj.get('id') for obj in objs if 'id' in obj]
    id_counts = Counter(ids)
    duplicates = [id for id, count in id_counts.items() if count > 1]

    if duplicates:
        # 找出重复 ID 的行号
        for dup_id in duplicates:
            line_nums = [line_num for line_num, obj in objects if obj.get('id') == dup_id]
            errors.append(ValidationError(
                str(file_path),
                line_nums[0],
                "业务规则",
                f"重复 ID '{dup_id}'，出现在行 {', '.join(map(str, line_nums))}"
            ))

    # 规则 2：前置条件检查（测试用例）
    for line_num, obj in objects:
        if 'preconditions' in obj:
            preconditions = obj['preconditions']
            if not preconditions:
                warnings.append(ValidationWarning(
                    str(file_path),
                    line_num,
                    "空前置条件",
                    f"前置条件为空（用例：{obj.get('name', obj.get('id'))}）"
                ))

    # 规则 3：steps 格式检查（测试用例）
    for line_num, obj in objects:
        if 'steps' in obj:
            steps = obj['steps']
            for i, step in enumerate(steps, 1):
                if not isinstance(step, dict):
                    errors.append(ValidationError(
                        str(file_path),
                        line_num,
                        "业务规则",
                        f"步骤 {i} 格式错误：应为对象，包含 action 和 expected 字段"
                    ))
                    continue

                if 'action' not in step:
                    errors.append(ValidationError(
                        str(file_path),
                        line_num,
                        "业务规则",
                        f"步骤 {i} 缺少 action 字段"
                    ))

                if 'expected' not in step:
                    errors.append(ValidationError(
                        str(file_path),
                        line_num,
                        "业务规则",
                        f"步骤 {i} 缺少 expected 字段"
                    ))

    # 规则 4：module_name 长度检查
    for line_num, obj in objects:
        if 'module_name' in obj:
            module_name = obj['module_name']
            if len(module_name) > 15:
                warnings.append(ValidationWarning(
                    str(file_path),
                    line_num,
                    "测试项过长",
                    f"测试项 '{module_name}' 超过 15 字符，建议简化"
                ))

    # 规则 5：用例名称主谓宾格式检查
    for line_num, obj in objects:
        if 'name' in obj and 'steps' in obj:  # 只检查测试用例
            name = obj['name']
            if not name.startswith('验证'):
                warnings.append(ValidationWarning(
                    str(file_path),
                    line_num,
                    "名称格式",
                    f"用例名称 '{name}' 建议以'验证'开头（主谓宾格式）"
                ))

    # 规则 6：ID 格式检查（新格式 M01-001）
    import re
    module_id_pattern = re.compile(r'^M[0-9]{2}-[0-9]{3}$')
    for line_num, obj in objects:
        if 'id' in obj and 'scenario_type' in obj:  # 测试用例
            case_id = obj['id']
            if not module_id_pattern.match(case_id):
                errors.append(ValidationError(
                    str(file_path),
                    line_num,
                    "ID 格式错误",
                    f"用例 ID '{case_id}' 格式错误，应为 {{module_id}}-{{seq:03d}}（如 M01-001）"
                ))

    # 规则 7：scenario_type 有效值检查
    valid_scenarios = ['正向场景', '边界场景', '异常场景', '性能场景', '安全场景']
    for line_num, obj in objects:
        if 'scenario_type' in obj:
            scenario = obj['scenario_type']
            if scenario not in valid_scenarios:
                errors.append(ValidationError(
                    str(file_path),
                    line_num,
                    "场景类型错误",
                    f"scenario_type '{scenario}' 无效，应为：{', '.join(valid_scenarios)}"
                ))

    # 规则 8：module_id 格式检查（测试项文件）
    module_id_pattern_item = re.compile(r'^M[0-9]{2}$')
    for line_num, obj in objects:
        if 'module_id' in obj and 'test_items' in obj:  # 测试项
            module_id = obj['module_id']
            if not module_id_pattern_item.match(module_id):
                errors.append(ValidationError(
                    str(file_path),
                    line_num,
                    "module_id 格式错误",
                    f"module_id '{module_id}' 格式错误，应为 M01-M99"
                ))

    return errors, warnings


def validate_file(file_path: Path, schema_path: Path = None, strict: bool = False) -> Tuple[int, List[ValidationError], List[ValidationWarning]]:
    """
    验证单个 JSONL 文件

    Args:
        file_path: JSONL 文件路径
        schema_path: JSON Schema 文件路径（可选）
        strict: 是否启用严格模式（业务规则验证）

    Returns:
        (object_count, errors, warnings)
    """
    all_errors = []
    all_warnings = []

    # 第 1 层：JSON 语法验证
    objects, syntax_errors = validate_json_syntax(file_path)
    all_errors.extend(syntax_errors)

    if syntax_errors:
        # 如果语法错误，后续验证无意义
        return 0, all_errors, all_warnings

    # 第 2 层：Schema 验证
    schema_errors = validate_schema(objects, file_path, schema_path)
    all_errors.extend(schema_errors)

    # 第 3 层：业务规则验证（strict 模式）
    if strict:
        business_errors, business_warnings = validate_business_rules(objects, file_path)
        all_errors.extend(business_errors)
        all_warnings.extend(business_warnings)

    return len(objects), all_errors, all_warnings


def main():
    parser = argparse.ArgumentParser(
        description='JSONL 格式验证工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python validate_jsonl.py test-items.jsonl
  python validate_jsonl.py cases.jsonl
  python validate_jsonl.py cases.jsonl --strict
  python validate_jsonl.py cases/*.jsonl --strict
  python validate_jsonl.py cases.jsonl --schema test-case.schema.json
        """
    )
    parser.add_argument('files', nargs='+', help='要验证的 JSONL 文件（支持通配符）')
    parser.add_argument('--schema', type=Path, help='JSON Schema 文件路径（可选，自动推断）')
    parser.add_argument('--strict', action='store_true', help='启用严格模式（业务规则验证）')

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

    # 验证所有文件
    total_objects = 0
    total_errors = []
    total_warnings = []

    for file_path in all_files:
        object_count, errors, warnings = validate_file(file_path, args.schema, args.strict)
        total_objects += object_count
        total_errors.extend(errors)
        total_warnings.extend(warnings)

        # 单文件报告
        if errors:
            print(f"❌ {file_path}: {object_count} 条记录，{len(errors)} 个错误")
        elif warnings:
            print(f"⚠️  {file_path}: {object_count} 条记录，{len(warnings)} 个警告")
        else:
            print(f"✅ {file_path}: {object_count} 条记录，无错误")

    # 输出详细错误和警告
    if total_errors:
        print("\n" + "="*60)
        print("错误详情：")
        print("="*60)
        for error in total_errors:
            print(f"  {error}")

    if total_warnings:
        print("\n" + "="*60)
        print("警告详情：")
        print("="*60)
        for warning in total_warnings:
            print(f"  {warning}")

    # 汇总报告
    print("\n" + "="*60)
    print("汇总报告：")
    print("="*60)
    print(f"总文件数：{len(all_files)}")
    print(f"总记录数：{total_objects}")
    print(f"错误数：{len(total_errors)}")
    print(f"警告数：{len(total_warnings)}")

    if total_errors:
        print("\n❌ 验证失败")
        sys.exit(1)
    elif total_warnings:
        print("\n⚠️  验证通过（有警告）")
        sys.exit(0)
    else:
        print("\n✅ 验证通过")
        sys.exit(0)


if __name__ == '__main__':
    main()
