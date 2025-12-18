#!/usr/bin/env python3
"""
JSONL 格式验证与审查工具

功能：
1. 验证 JSONL 文件的 JSON 语法
2. 验证业务规则（ID 唯一性、格式规范）
3. 审查模式：发现待审查项（禁用词、可执行性、覆盖完整性）

用法：
    python validate.py cases.jsonl
    python validate.py cases.jsonl --strict
    python validate.py cases/*.jsonl --strict
    python validate.py cases/*.jsonl --audit --modules modules.jsonl
"""

import json
import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter, defaultdict


# 非黑盒关键词（可执行性检测）
NON_BLACKBOX_WORDS = [
    '数据库', 'SQL', 'API', '接口', '日志', 'log', '缓存', 'cache',
    '后台', '服务端', '响应码', '状态码', '返回值', '配置文件'
]


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


class AuditItem:
    """待审查项（需要 Agent 判断）"""
    def __init__(self, category: str, case_id: str, location: str, message: str, context: str = None):
        self.category = category  # 覆盖/禁用词/可执行
        self.case_id = case_id
        self.location = location  # 步骤/预期/名称
        self.message = message
        self.context = context  # 原文

    def __str__(self):
        ctx = f' "{self.context}"' if self.context else ""
        return f"[{self.category}] {self.case_id}:{self.location} - {self.message}{ctx}"


def load_jsonl(file_path: Path) -> Tuple[List[Tuple[int, Dict]], List[ValidationError]]:
    """加载 JSONL 文件"""
    objects = []
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
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
    """业务规则验证"""
    errors = []
    warnings = []

    # 规则 1：ID 唯一性
    ids = [obj.get('id') for _, obj in objects if 'id' in obj]
    id_counts = Counter(ids)
    for dup_id, count in id_counts.items():
        if count > 1:
            line_nums = [ln for ln, obj in objects if obj.get('id') == dup_id]
            errors.append(ValidationError(
                str(file_path), line_nums[0], "重复ID",
                f"ID '{dup_id}' 重复，出现在行 {', '.join(map(str, line_nums))}"
            ))

    # 规则 2：ID 格式检查
    case_id_pattern = re.compile(r'^M[0-9]{2}-[0-9]{3}$')
    module_id_pattern = re.compile(r'^M[0-9]{2}$')

    for line_num, obj in objects:
        case_id = obj.get('id', '')
        if 'test_item' in obj:  # 测试用例
            if not case_id_pattern.match(case_id):
                errors.append(ValidationError(
                    str(file_path), line_num, "ID格式",
                    f"用例 ID '{case_id}' 格式错误，应为 M01-001", case_id
                ))
        elif 'test_items' in obj:  # 模块
            module_id = obj.get('module_id', '')
            if not module_id_pattern.match(module_id):
                errors.append(ValidationError(
                    str(file_path), line_num, "ID格式",
                    f"module_id '{module_id}' 格式错误，应为 M01"
                ))

    # 规则 3：steps 必须有验证点
    for line_num, obj in objects:
        if 'steps' not in obj:
            continue
        steps = obj['steps']
        case_id = obj.get('id', '?')

        has_expected = False
        for i, step in enumerate(steps, 1):
            if not isinstance(step, dict):
                errors.append(ValidationError(
                    str(file_path), line_num, "格式错误",
                    f"步骤 {i} 应为对象", case_id
                ))
                continue
            if 'action' not in step:
                errors.append(ValidationError(
                    str(file_path), line_num, "格式错误",
                    f"步骤 {i} 缺少 action", case_id
                ))
            if step.get('expected'):
                has_expected = True

        if not has_expected:
            errors.append(ValidationError(
                str(file_path), line_num, "缺少验证点",
                f"至少一个步骤需要 expected", case_id
            ))

    # 规则 4：名称以"验证"开头
    for line_num, obj in objects:
        if 'name' in obj and 'steps' in obj:
            name = obj['name']
            if not name.startswith('验证'):
                warnings.append(ValidationError(
                    str(file_path), line_num, "名称格式",
                    f"建议以'验证'开头", obj.get('id')
                ))

    return errors, warnings


def audit_executable(objects: List[Tuple[int, Dict]]) -> List[AuditItem]:
    """可执行性检测（黑盒原则）"""
    items = []

    for _, obj in objects:
        if 'steps' not in obj:
            continue
        case_id = obj.get('id', '?')

        for i, step in enumerate(obj['steps'], 1):
            action = step.get('action', '')
            expected = step.get('expected', '')

            for word in NON_BLACKBOX_WORDS:
                if word.lower() in action.lower():
                    items.append(AuditItem(
                        "可执行", case_id, f"步骤{i}",
                        f"包含非黑盒词 '{word}'", action[:50]
                    ))
                if word.lower() in expected.lower():
                    items.append(AuditItem(
                        "可执行", case_id, f"预期{i}",
                        f"包含非黑盒词 '{word}'", expected[:50]
                    ))

    return items


def audit_coverage(cases: List[Dict], modules: List[Dict]) -> List[AuditItem]:
    """覆盖完整性检测"""
    items = []

    # 构建 test_item -> cases 映射
    item_cases = defaultdict(list)
    for case in cases:
        item = case.get('test_item', '')
        item_cases[item].append(case)

    # 检查每个模块的测试项
    for module in modules:
        module_id = module.get('module_id', '?')
        module_name = module.get('module_name', '?')
        test_items = module.get('test_items', [])

        for ti in test_items:
            item_name = ti.get('item', '')
            biz_value = ti.get('business_value', '中')
            cases_for_item = item_cases.get(item_name, [])

            if not cases_for_item:
                items.append(AuditItem(
                    "覆盖", f"{module_id}", item_name,
                    f"无用例（business_value={biz_value}）"
                ))
                continue

            # 检查正向/反向覆盖
            positive = [c for c in cases_for_item if not c.get('is_negative', False)]
            negative = [c for c in cases_for_item if c.get('is_negative', False)]

            if not positive:
                items.append(AuditItem(
                    "覆盖", f"{module_id}", item_name,
                    f"缺少正向用例（共 {len(cases_for_item)} 条）"
                ))

            if not negative:
                items.append(AuditItem(
                    "覆盖", f"{module_id}", item_name,
                    f"缺少异常/边界用例（共 {len(cases_for_item)} 条）"
                ))

    return items


def validate_files(file_paths: List[Path], strict: bool = False) -> Tuple[int, List[ValidationError], List[ValidationError]]:
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

        if strict:
            errors, warnings = validate_business_rules(objects, file_path)
            all_errors.extend(errors)
            all_warnings.extend(warnings)

    return total_objects, all_errors, all_warnings


def audit_files(case_files: List[Path], modules_path: Path = None) -> List[AuditItem]:
    """审查模式"""
    all_items = []
    all_cases = []

    # 加载所有用例
    for file_path in case_files:
        objects, _ = load_jsonl(file_path)
        all_cases.extend([obj for _, obj in objects])

    # 可执行性检测
    for file_path in case_files:
        objects, _ = load_jsonl(file_path)
        all_items.extend(audit_executable(objects))

    # 覆盖完整性检测
    if modules_path and modules_path.exists():
        modules_objects, _ = load_jsonl(modules_path)
        modules = [obj for _, obj in modules_objects]
        all_items.extend(audit_coverage(all_cases, modules))

    return all_items


def main():
    parser = argparse.ArgumentParser(
        description='JSONL 验证与审查工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python validate.py cases.jsonl --strict
  python validate.py cases/*.jsonl --audit --modules modules.jsonl
        """
    )
    parser.add_argument('files', nargs='+', help='JSONL 文件（支持通配符）')
    parser.add_argument('--strict', action='store_true', help='严格模式（业务规则验证）')
    parser.add_argument('--audit', action='store_true', help='审查模式（输出待审查项）')
    parser.add_argument('--modules', type=Path, help='模块文件（用于覆盖检查）')

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
    total, errors, warnings = validate_files(all_files, args.strict)

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

    # 审查模式
    if args.audit:
        audit_items = audit_files(all_files, args.modules)

        if audit_items:
            print(f"\n{'='*60}\n待审查项（共 {len(audit_items)} 项，需 Agent 判断）：\n{'='*60}")

            # 按类别分组
            by_category = defaultdict(list)
            for item in audit_items:
                by_category[item.category].append(item)

            for cat in ['覆盖', '可执行']:
                if cat in by_category:
                    print(f"\n[{cat}]")
                    for item in by_category[cat]:
                        print(f"  {item.case_id}:{item.location} - {item.message}")
                        if item.context:
                            print(f"    原文: {item.context}")
        else:
            print(f"\n✅ 审查完成，无待审查项")

    # 汇总
    print(f"\n{'='*60}\n汇总：\n{'='*60}")
    print(f"文件数：{len(all_files)}")
    print(f"用例数：{total}")
    print(f"错误：{len(errors)}")
    print(f"警告：{len(warnings)}")
    if args.audit:
        print(f"待审查：{len(audit_items) if args.audit else 0}")

    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
