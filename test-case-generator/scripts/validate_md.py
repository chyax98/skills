
"""
测试用例 Markdown 验证工具

验证 Markdown 格式的测试用例，输出统计报告。

使用方法：
    uv run validate_md.py test-cases.md
"""

import re
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from collections import defaultdict


@dataclass
class TestCase:
    """测试用例数据结构"""
    line_number: int = 0
    module: str = ""
    scenario: str = ""
    name: str = ""
    priority: str = ""
    test_type: str = ""
    is_negative: bool = False
    preconditions: str = ""
    steps: list = field(default_factory=list)
    notes: str = ""


@dataclass
class ValidationError:
    """验证错误"""
    line: int
    case_name: str
    message: str


VALID_PRIORITIES = {'P1', 'P2', 'P3', 'P4', 'P5'}

VALID_TEST_TYPES = {
    '功能', '功能测试', '兼容性', '兼容性测试', '易用性', '易用性测试',
    '性能', '性能测试', '稳定性', '稳定性测试', '安全性', '安全性测试',
    '可靠性', '可靠性测试', '效果', '效果测试', '效果（AI类）', 'AI效果测试',
    '效果（硬件类）', '硬件效果测试', '可维护性', '可维护性测试',
    '可移植性', '可移植性测试', '埋点', '埋点测试', '集成', '集成测试',
}

# 扩展模糊词汇列表（V4.0 增强）
VAGUE_WORDS = {
    # 原有模糊词
    '正确', '正常', '合适', '适当', '有效',
    # 新增模糊词
    '成功', '失败', '完成', '错误',  # 结果类模糊词
    '好', '对', '行', '可以',  # 简单判断词
    '应该', '可能', '大概',  # 不确定词
}

# 禁止的操作描述（V4.0 增强）
VAGUE_ACTIONS = {
    '正确操作', '正确输入', '正确填写',
    '按要求操作', '按要求输入', '按要求填写',
    '合理操作', '合理输入',
}

# 模块名称长度限制
MAX_MODULE_NAME_LENGTH = 15


def parse_metadata(line: str) -> tuple[str, str, bool]:
    """
    解析元数据行：P1|功能|反向
    返回：(priority, test_type, is_negative)
    """
    parts = [p.strip() for p in line.split('|')]
    priority = parts[0] if parts else ""
    test_type = parts[1] if len(parts) > 1 else ""
    is_negative = len(parts) > 2 and '反向' in parts[2]
    return priority, test_type, is_negative


def parse_steps(lines: list[str]) -> list[tuple[str, str]]:
    steps = []
    for line in lines:
        line = line.strip()
        match = re.match(r'^\d+\.\s*(.+)$', line)
        if match:
            content = match.group(1)
            # 使用 ➡️ 作为分隔符
            if '➡️' in content:
                parts = content.split('➡️', 1)
                steps.append((parts[0].strip(), parts[1].strip() if len(parts) > 1 else ""))
            else:
                steps.append((content.strip(), ""))
    return steps


def parse_markdown(content: str) -> list[TestCase]:
    cases = []
    lines = content.split('\n')
    current_module, current_scenario = "", ""
    current_case: Optional[TestCase] = None
    current_section, section_lines = None, []

    def save_section():
        nonlocal current_case, current_section, section_lines
        if current_case and current_section and section_lines:
            if current_section == 'preconditions':
                precond_list = [l.strip().lstrip('- ') for l in section_lines if l.strip()]
                current_case.preconditions = '；'.join(precond_list)
            elif current_section == 'steps':
                current_case.steps = parse_steps(section_lines)
            elif current_section == 'notes':
                current_case.notes = ' '.join(l.strip() for l in section_lines if l.strip())
        section_lines.clear()
        current_section = None

    def save_case():
        nonlocal current_case
        save_section()
        if current_case and current_case.name:
            cases.append(current_case)
        current_case = None

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped == '---':
            continue
        if line.startswith('# ') and not line.startswith('## '):
            save_case()
            current_module, current_scenario = line[2:].strip(), ""
        elif line.startswith('## '):
            save_case()
            current_scenario = line[3:].strip()
        elif line.startswith('### '):
            save_case()
            current_case = TestCase(line_number=line_num, module=current_module, scenario=current_scenario, name=line[4:].strip())
        elif current_case and re.match(r'^P[1-5]\|', stripped):
            save_section()
            current_case.priority, current_case.test_type, current_case.is_negative = parse_metadata(stripped)
        elif stripped.startswith('[前置]') and current_case:
            save_section()
            current_section = 'preconditions'
            if rest := stripped[4:].strip():
                section_lines.append(rest)
        elif stripped.startswith('[步骤]') and current_case:
            save_section()
            current_section = 'steps'
        elif stripped.startswith('[备注]') and current_case:
            save_section()
            current_section = 'notes'
            if rest := stripped[4:].strip():
                section_lines.append(rest)
        elif current_section and stripped:
            section_lines.append(stripped)

    save_case()
    return cases


def validate_cases(cases: list[TestCase]) -> list[ValidationError]:
    errors = []
    for case in cases:
        # 用例名称检查
        if not case.name:
            errors.append(ValidationError(case.line_number, "(未命名)", "用例名称为空"))
        elif not case.name.startswith('验证'):
            errors.append(ValidationError(case.line_number, case.name, "用例名称未以'验证'开头"))

        # 模块名称长度检查
        if case.module and len(case.module) > MAX_MODULE_NAME_LENGTH:
            errors.append(ValidationError(case.line_number, case.name, f"模块名称过长({len(case.module)}字符)，建议≤{MAX_MODULE_NAME_LENGTH}字符"))

        # 优先级检查
        if not case.priority:
            errors.append(ValidationError(case.line_number, case.name, "缺少优先级"))
        elif case.priority not in VALID_PRIORITIES:
            errors.append(ValidationError(case.line_number, case.name, f"无效优先级 '{case.priority}'"))

        # 测试类型检查
        if not case.test_type:
            errors.append(ValidationError(case.line_number, case.name, "缺少测试类型"))
        elif case.test_type not in VALID_TEST_TYPES:
            errors.append(ValidationError(case.line_number, case.name, f"未知测试类型 '{case.test_type}'"))

        # 测试步骤检查
        if not case.steps:
            errors.append(ValidationError(case.line_number, case.name, "缺少测试步骤"))
        else:
            # 检查步骤描述质量
            for i, (action, expected) in enumerate(case.steps, 1):
                if not action.strip():
                    errors.append(ValidationError(case.line_number, case.name, f"步骤{i}操作为空"))

                # 检查模糊动作词
                for vague_action in VAGUE_ACTIONS:
                    if vague_action in action:
                        errors.append(ValidationError(case.line_number, case.name, f"步骤{i}操作含模糊描述'{vague_action}'"))

                # 检查模糊词汇（操作）
                for word in VAGUE_WORDS:
                    if word in action:
                        errors.append(ValidationError(case.line_number, case.name, f"步骤{i}操作描述模糊，含'{word}'"))

                # 检查模糊词汇（预期结果）
                if expected:
                    for word in VAGUE_WORDS:
                        if word in expected:
                            errors.append(ValidationError(case.line_number, case.name, f"步骤{i}预期结果模糊，含'{word}'"))

                    # 检查预期结果是否过于简单
                    if len(expected.strip()) < 3:
                        errors.append(ValidationError(case.line_number, case.name, f"步骤{i}预期结果过于简单"))

    return errors


def generate_report(cases: list[TestCase], errors: list[ValidationError]) -> str:
    total = len(cases)
    modules = defaultdict(lambda: {'count': 0})
    priorities = defaultdict(int)
    test_types = defaultdict(int)
    negative_count = 0

    for case in cases:
        modules[case.module or '(未分组)']['count'] += 1
        if case.priority:
            priorities[case.priority] += 1
        if case.test_type:
            test_types[case.test_type.replace('测试', '')] += 1
        if case.is_negative:
            negative_count += 1

    lines = ["# 测试用例统计报告\n", "## 概览\n", "| 指标 | 数值 |", "|------|------|"]
    lines.append(f"| 总用例数 | {total} |")
    lines.append(f"| 模块数 | {len(modules)} |")
    lines.append(f"| 验证问题 | {len(errors)} |")
    lines.append("")

    lines.extend(["## 优先级分布\n", "| 优先级 | 数量 | 占比 |", "|-------|------|------|"])
    for p in ['P1', 'P2', 'P3', 'P4', 'P5']:
        c = priorities.get(p, 0)
        lines.append(f"| {p} | {c} | {c*100//total if total else 0}% |")
    lines.append("")

    lines.extend(["## 测试类型分布\n", "| 测试类型 | 数量 | 占比 |", "|---------|------|------|"])
    for t, c in sorted(test_types.items(), key=lambda x: -x[1]):
        lines.append(f"| {t} | {c} | {c*100//total if total else 0}% |")
    lines.append("")

    lines.extend(["## 正向/反向分布\n", "| 类型 | 数量 | 占比 |", "|------|------|------|"])
    pos = total - negative_count
    lines.append(f"| 正向用例 | {pos} | {pos*100//total if total else 0}% |")
    lines.append(f"| 反向用例 | {negative_count} | {negative_count*100//total if total else 0}% |")
    lines.append("")

    if total > 0:
        ratio = negative_count / total
        if ratio < 0.15:
            lines.append(f"> ⚠️ 反向用例占比 {ratio*100:.0f}%，低于建议值 15%\n")
        else:
            lines.append(f"> ✅ 反向用例占比 {ratio*100:.0f}%，符合建议\n")

    lines.extend(["## 模块明细\n", "| 模块 | 用例数 | P1 | P2 | P3 | P4 | P5 |", "|------|-------|----|----|----|----|-----|"])
    for module, data in modules.items():
        mc = [c for c in cases if (c.module or '(未分组)') == module]
        pc = {f'P{i}': sum(1 for c in mc if c.priority == f'P{i}') for i in range(1, 6)}
        lines.append(f"| {module} | {data['count']} | {pc['P1']} | {pc['P2']} | {pc['P3']} | {pc['P4']} | {pc['P5']} |")
    lines.append("")

    if errors:
        lines.extend(["## 验证问题\n"])
        for e in errors:
            lines.append(f"- **行{e.line}** [{e.case_name}]: {e.message}")
        lines.append("")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='验证测试用例并生成统计报告')
    parser.add_argument('input', help='Markdown 文件路径')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误：文件不存在 {input_path}")
        return 1

    cases = parse_markdown(input_path.read_text(encoding='utf-8'))
    if not cases:
        print("未解析到任何测试用例")
        return 1

    errors = validate_cases(cases)
    report = generate_report(cases, errors)

    output_path = input_path.parent / 'stats-report.md'
    output_path.write_text(report, encoding='utf-8')

    print(f"共 {len(cases)} 条用例，{len(errors)} 个问题")
    if errors:
        print("\n问题列表：")
        for e in errors:
            print(f"  行{e.line} [{e.case_name}]: {e.message}")
    print(f"\n报告已生成：{output_path}")

    return 1 if errors else 0


if __name__ == '__main__':
    exit(main())
