#!/usr/bin/env python3
"""
Git Commit Analysis Script

提取 Git 提交的 Java 代码变更,用于缺陷分析。

Usage:
    python analyze_commit.py <commit_hash>
    python analyze_commit.py HEAD
    python analyze_commit.py abc123..def456  # Compare commits
"""

import sys
import subprocess
import json
import re
from pathlib import Path
from typing import List, Dict, Optional


class CommitAnalyzer:
    """Git 提交分析器"""

    def __init__(self, commit_ref: str = "HEAD"):
        self.commit_ref = commit_ref
        self.java_file_pattern = re.compile(r'\.java$')

    def get_commit_info(self) -> Dict:
        """获取提交基本信息"""
        try:
            # 获取提交信息
            commit_info = subprocess.check_output(
                ["git", "show", "--no-patch", "--format=%H%n%an%n%ae%n%ad%n%s", self.commit_ref],
                stderr=subprocess.STDOUT
            ).decode('utf-8').strip().split('\n')

            return {
                "commit_hash": commit_info[0],
                "author": commit_info[1],
                "email": commit_info[2],
                "date": commit_info[3],
                "message": commit_info[4] if len(commit_info) > 4 else ""
            }
        except subprocess.CalledProcessError as e:
            print(f"Error: 无法获取提交信息: {e.output.decode('utf-8')}")
            sys.exit(1)

    def get_changed_files(self) -> List[str]:
        """获取变更的 Java 文件列表"""
        try:
            output = subprocess.check_output(
                ["git", "diff", "--name-only", f"{self.commit_ref}^", self.commit_ref],
                stderr=subprocess.STDOUT
            ).decode('utf-8')

            files = output.strip().split('\n')
            java_files = [f for f in files if self.java_file_pattern.search(f)]
            return java_files
        except subprocess.CalledProcessError as e:
            print(f"Error: 无法获取变更文件: {e.output.decode('utf-8')}")
            return []

    def get_file_diff(self, file_path: str) -> str:
        """获取文件的详细 diff"""
        try:
            output = subprocess.check_output(
                ["git", "diff", "-U5", f"{self.commit_ref}^", self.commit_ref, "--", file_path],
                stderr=subprocess.STDOUT
            ).decode('utf-8', errors='ignore')
            return output
        except subprocess.CalledProcessError:
            return ""

    def parse_method_changes(self, diff: str) -> List[Dict]:
        """解析方法级别的变更"""
        changes = []
        current_method = None
        method_pattern = re.compile(r'^\+.*(?:public|private|protected)\s+(?:\w+\s+)*(\w+)\s*\(')

        for line in diff.split('\n'):
            # 检测新增的方法
            if line.startswith('+') and not line.startswith('+++'):
                method_match = method_pattern.search(line)
                if method_match:
                    current_method = method_match.group(1)
                    changes.append({
                        "type": "method_added",
                        "method": current_method,
                        "line": line[1:].strip()
                    })

        return changes

    def get_stats(self) -> Dict:
        """获取统计信息"""
        try:
            output = subprocess.check_output(
                ["git", "diff", "--shortstat", f"{self.commit_ref}^", self.commit_ref],
                stderr=subprocess.STDOUT
            ).decode('utf-8')

            # 解析统计信息: "1 file changed, 10 insertions(+), 5 deletions(-)"
            stats = {"files_changed": 0, "insertions": 0, "deletions": 0}

            files_match = re.search(r'(\d+) files? changed', output)
            insertions_match = re.search(r'(\d+) insertions?', output)
            deletions_match = re.search(r'(\d+) deletions?', output)

            if files_match:
                stats["files_changed"] = int(files_match.group(1))
            if insertions_match:
                stats["insertions"] = int(insertions_match.group(1))
            if deletions_match:
                stats["deletions"] = int(deletions_match.group(1))

            return stats
        except subprocess.CalledProcessError:
            return {"files_changed": 0, "insertions": 0, "deletions": 0}

    def analyze(self) -> Dict:
        """执行完整分析"""
        commit_info = self.get_commit_info()
        java_files = self.get_changed_files()
        stats = self.get_stats()

        java_changes = []
        for file_path in java_files:
            diff = self.get_file_diff(file_path)
            method_changes = self.parse_method_changes(diff)

            java_changes.append({
                "file": file_path,
                "diff": diff,
                "methods": method_changes
            })

        return {
            "commit_info": commit_info,
            "stats": stats,
            "java_files": java_files,
            "java_changes": java_changes
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_commit.py <commit_hash>")
        print("Example: python analyze_commit.py HEAD")
        sys.exit(1)

    commit_ref = sys.argv[1]
    analyzer = CommitAnalyzer(commit_ref)
    result = analyzer.analyze()

    # 输出 JSON 格式结果
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
