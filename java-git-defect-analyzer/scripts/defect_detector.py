#!/usr/bin/env python3
"""
Java Defect Detection Script

检测 Java 代码中的常见缺陷模式 (NPE、资源泄漏、安全漏洞等)。

Usage:
    python defect_detector.py <commit_hash>
"""

import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple


class DefectDetector:
    """Java 缺陷检测器"""

    def __init__(self, code_changes: Dict):
        self.code_changes = code_changes
        self.defects = []

    def detect_npe_risks(self, code: str, file_path: str) -> List[Dict]:
        """检测 NPE 风险"""
        issues = []

        # 模式 1: 方法调用前未检查 null
        pattern = re.compile(
            r'(\w+)\s*=\s*\w+\.(?:find|get|query)\w*\([^)]*\);?\s*\n\s*.*?\1\.(\w+)\(',
            re.MULTILINE
        )

        for match in pattern.finditer(code):
            var_name = match.group(1)
            method_call = match.group(2)
            issues.append({
                "type": "NPE_RISK",
                "severity": "HIGH",
                "file": file_path,
                "variable": var_name,
                "description": f"变量 '{var_name}' 可能为 null, 直接调用 '{method_call}()' 存在 NPE 风险",
                "pattern": "unchecked_null_before_method_call",
                "line": code[:match.start()].count('\n') + 1
            })

        # 模式 2: Optional 未检查直接 get()
        optional_pattern = re.compile(r'\.findById\([^)]+\)\.get\(\)')
        for match in optional_pattern.finditer(code):
            issues.append({
                "type": "NPE_RISK",
                "severity": "HIGH",
                "file": file_path,
                "description": "Optional.get() 未检查 isPresent(), 可能抛出 NoSuchElementException",
                "pattern": "optional_get_without_check",
                "line": code[:match.start()].count('\n') + 1
            })

        return issues

    def detect_resource_leaks(self, code: str, file_path: str) -> List[Dict]:
        """检测资源泄漏"""
        issues = []

        # 检测未关闭的资源
        resource_types = [
            'Connection', 'Statement', 'PreparedStatement', 'ResultSet',
            'InputStream', 'OutputStream', 'Reader', 'Writer',
            'FileInputStream', 'FileOutputStream', 'Socket'
        ]

        for resource_type in resource_types:
            # 模式: 创建资源但未使用 try-with-resources
            pattern = re.compile(
                rf'{resource_type}\s+\w+\s*=\s*(?:new\s+{resource_type}|.*\.get{resource_type})',
                re.IGNORECASE
            )

            for match in pattern.finditer(code):
                # 检查是否在 try-with-resources 中
                start_pos = match.start()
                context = code[max(0, start_pos - 100):start_pos + 200]

                if 'try (' not in context and 'try-with-resources' not in context:
                    if '.close()' not in context:
                        issues.append({
                            "type": "RESOURCE_LEAK",
                            "severity": "HIGH",
                            "file": file_path,
                            "resource_type": resource_type,
                            "description": f"{resource_type} 可能未正确关闭, 建议使用 try-with-resources",
                            "pattern": "resource_not_closed",
                            "line": code[:match.start()].count('\n') + 1
                        })

        return issues

    def detect_sql_injection(self, code: str, file_path: str) -> List[Dict]:
        """检测 SQL 注入风险"""
        issues = []

        # 模式: 字符串拼接构造 SQL
        sql_concat_patterns = [
            re.compile(r'(?:SELECT|INSERT|UPDATE|DELETE).*?\+\s*\w+', re.IGNORECASE),
            re.compile(r'String\s+sql\s*=.*?".*?\+.*?"', re.IGNORECASE),
            re.compile(r'executeQuery\([^)]*\+[^)]*\)', re.IGNORECASE)
        ]

        for pattern in sql_concat_patterns:
            for match in pattern.finditer(code):
                issues.append({
                    "type": "SQL_INJECTION",
                    "severity": "CRITICAL",
                    "file": file_path,
                    "description": "使用字符串拼接构造 SQL 查询, 存在 SQL 注入风险",
                    "pattern": "sql_string_concatenation",
                    "line": code[:match.start()].count('\n') + 1,
                    "suggestion": "使用 PreparedStatement 和参数绑定"
                })

        return issues

    def detect_hardcoded_secrets(self, code: str, file_path: str) -> List[Dict]:
        """检测硬编码密钥"""
        issues = []

        # 敏感关键词
        sensitive_patterns = [
            (r'password\s*=\s*["\'](?!.*\$\{)(.+?)["\']', 'PASSWORD'),
            (r'apiKey\s*=\s*["\'](.+?)["\']', 'API_KEY'),
            (r'secret\s*=\s*["\'](.+?)["\']', 'SECRET'),
            (r'token\s*=\s*["\'](?!.*\$\{)(.+?)["\']', 'TOKEN'),
            (r'jdbc:.*://.*:(.+?)@', 'DB_PASSWORD')
        ]

        for pattern, secret_type in sensitive_patterns:
            for match in re.finditer(pattern, code, re.IGNORECASE):
                # 排除明显的占位符
                value = match.group(1)
                if len(value) < 3 or value in ['xxx', 'test', 'example', '***']:
                    continue

                issues.append({
                    "type": "HARDCODED_SECRET",
                    "severity": "CRITICAL",
                    "file": file_path,
                    "secret_type": secret_type,
                    "description": f"硬编码 {secret_type}, 存在安全风险",
                    "pattern": "hardcoded_credential",
                    "line": code[:match.start()].count('\n') + 1,
                    "suggestion": "使用环境变量或配置文件管理敏感信息"
                })

        return issues

    def detect_concurrency_issues(self, code: str, file_path: str) -> List[Dict]:
        """检测并发问题"""
        issues = []

        # 模式: 双重检查锁定错误
        dcl_pattern = re.compile(
            r'if\s*\(\s*\w+\s*==\s*null\s*\)\s*\{[^}]*synchronized.*?if\s*\(\s*\w+\s*==\s*null\s*\)',
            re.DOTALL
        )

        for match in dcl_pattern.finditer(code):
            if 'volatile' not in code[max(0, match.start() - 200):match.start()]:
                issues.append({
                    "type": "CONCURRENCY_ISSUE",
                    "severity": "MEDIUM",
                    "file": file_path,
                    "description": "双重检查锁定模式未使用 volatile, 可能导致线程安全问题",
                    "pattern": "double_checked_locking_without_volatile",
                    "line": code[:match.start()].count('\n') + 1
                })

        return issues

    def detect_performance_issues(self, code: str, file_path: str) -> List[Dict]:
        """检测性能问题"""
        issues = []

        # 模式 1: 循环中字符串拼接
        string_concat_pattern = re.compile(
            r'for\s*\([^)]+\)\s*\{[^}]*\w+\s*\+=\s*["\']',
            re.DOTALL
        )

        for match in string_concat_pattern.finditer(code):
            if 'StringBuilder' not in code[match.start():match.end() + 100]:
                issues.append({
                    "type": "PERFORMANCE_ISSUE",
                    "severity": "MEDIUM",
                    "file": file_path,
                    "description": "循环中使用 += 拼接字符串, 建议使用 StringBuilder",
                    "pattern": "string_concatenation_in_loop",
                    "line": code[:match.start()].count('\n') + 1
                })

        # 模式 2: 不必要的对象创建
        unnecessary_object_pattern = re.compile(r'new String\(')
        for match in unnecessary_object_pattern.finditer(code):
            issues.append({
                "type": "PERFORMANCE_ISSUE",
                "severity": "LOW",
                "file": file_path,
                "description": "不必要的 String 对象创建, 直接使用字符串字面量即可",
                "pattern": "unnecessary_string_object",
                "line": code[:match.start()].count('\n') + 1
            })

        return issues

    def detect_all(self) -> List[Dict]:
        """执行所有检测"""
        all_defects = []

        for change in self.code_changes.get('java_changes', []):
            file_path = change.get('file', '')
            diff = change.get('diff', '')

            # 只分析新增的代码 (+ 开头的行)
            added_lines = [line[1:] for line in diff.split('\n') if line.startswith('+') and not line.startswith('+++')]
            code = '\n'.join(added_lines)

            if not code.strip():
                continue

            # 执行各类检测
            all_defects.extend(self.detect_npe_risks(code, file_path))
            all_defects.extend(self.detect_resource_leaks(code, file_path))
            all_defects.extend(self.detect_sql_injection(code, file_path))
            all_defects.extend(self.detect_hardcoded_secrets(code, file_path))
            all_defects.extend(self.detect_concurrency_issues(code, file_path))
            all_defects.extend(self.detect_performance_issues(code, file_path))

        return all_defects

    def analyze(self) -> Dict:
        """执行完整缺陷检测"""
        defects = self.detect_all()

        # 按严重程度分类
        by_severity = {
            "CRITICAL": [],
            "HIGH": [],
            "MEDIUM": [],
            "LOW": []
        }

        for defect in defects:
            severity = defect.get('severity', 'LOW')
            by_severity[severity].append(defect)

        return {
            "summary": {
                "total_defects": len(defects),
                "critical": len(by_severity["CRITICAL"]),
                "high": len(by_severity["HIGH"]),
                "medium": len(by_severity["MEDIUM"]),
                "low": len(by_severity["LOW"])
            },
            "defects_by_severity": by_severity,
            "all_defects": defects
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python defect_detector.py <commit_hash>")
        sys.exit(1)

    commit_ref = sys.argv[1]

    # 读取代码变更 (从 analyze_commit.py 的输出)
    import subprocess
    script_dir = Path(__file__).parent
    analyze_script = script_dir / "analyze_commit.py"

    result = subprocess.run(
        ["python3", str(analyze_script), commit_ref],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error: 无法分析提交: {result.stderr}")
        sys.exit(1)

    code_changes = json.loads(result.stdout)

    # 执行缺陷检测
    detector = DefectDetector(code_changes)
    analysis = detector.analyze()

    # 输出结果
    print(json.dumps(analysis, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
