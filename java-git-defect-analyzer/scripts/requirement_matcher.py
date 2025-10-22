#!/usr/bin/env python3
"""
Requirement Matching Script

对比需求文档与代码实现,识别功能缺陷和实现偏差。

Usage:
    python requirement_matcher.py --requirement req.md --commit HEAD
"""

import argparse
import json
import re
from pathlib import Path
from typing import List, Dict, Set


class RequirementMatcher:
    """需求匹配分析器"""

    def __init__(self, requirement_doc: str, code_changes: Dict):
        self.requirement_doc = requirement_doc
        self.code_changes = code_changes
        self.requirement_features = []
        self.implementation_features = []

    def extract_requirement_features(self) -> List[Dict]:
        """从需求文档中提取功能点"""
        features = []

        # 识别需求关键词模式
        patterns = [
            r'需要|应该|必须|要求',
            r'用户.*(?:能够|可以)',
            r'系统.*(?:应|需|须)',
            r'功能[:：]',
            r'\d+[\.、].*'  # 编号列表
        ]

        lines = self.requirement_doc.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # 检查是否匹配需求模式
            for pattern in patterns:
                if re.search(pattern, line):
                    features.append({
                        "line_number": i + 1,
                        "text": line,
                        "keywords": self._extract_keywords(line),
                        "type": self._classify_requirement(line)
                    })
                    break

        self.requirement_features = features
        return features

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 移除常见词汇
        stop_words = {'需要', '应该', '必须', '要求', '能够', '可以', '系统', '用户'}

        # 简单分词 (可以用 jieba 替代)
        words = re.findall(r'[\u4e00-\u9fa5]+', text)
        keywords = [w for w in words if len(w) > 1 and w not in stop_words]
        return keywords[:5]  # 取前5个关键词

    def _classify_requirement(self, text: str) -> str:
        """分类需求类型"""
        if re.search(r'登录|注册|认证|授权', text):
            return "authentication"
        elif re.search(r'数据|存储|保存|查询', text):
            return "data_operation"
        elif re.search(r'通知|邮件|短信|消息', text):
            return "notification"
        elif re.search(r'日志|记录|审计', text):
            return "logging"
        elif re.search(r'验证|校验|检查', text):
            return "validation"
        else:
            return "general"

    def extract_implementation_features(self) -> List[Dict]:
        """从代码变更中提取实现功能"""
        features = []

        for change in self.code_changes.get('java_changes', []):
            file_path = change.get('file', '')
            methods = change.get('methods', [])

            for method in methods:
                method_name = method.get('method', '')
                features.append({
                    "file": file_path,
                    "method": method_name,
                    "type": method.get('type', 'unknown'),
                    "keywords": self._extract_code_keywords(method_name)
                })

        self.implementation_features = features
        return features

    def _extract_code_keywords(self, method_name: str) -> List[str]:
        """从方法名提取关键词"""
        # 驼峰命名拆分
        words = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', method_name)).split()
        return [w.lower() for w in words if len(w) > 2]

    def match_features(self) -> List[Dict]:
        """匹配需求与实现"""
        matches = []

        for req_feature in self.requirement_features:
            req_keywords = set(req_feature['keywords'])
            matched = False
            matched_implementations = []

            for impl_feature in self.implementation_features:
                impl_keywords = set(impl_feature['keywords'])

                # 计算关键词重叠度
                overlap = req_keywords & impl_keywords
                if overlap:
                    matched = True
                    matched_implementations.append({
                        "file": impl_feature['file'],
                        "method": impl_feature['method'],
                        "overlap": list(overlap)
                    })

            status = "implemented" if matched else "missing"
            matches.append({
                "requirement": req_feature['text'],
                "status": status,
                "matched_code": matched_implementations,
                "severity": "CRITICAL" if status == "missing" else "LOW"
            })

        return matches

    def analyze(self) -> Dict:
        """执行完整匹配分析"""
        self.extract_requirement_features()
        self.extract_implementation_features()
        matches = self.match_features()

        # 统计
        total = len(matches)
        missing = len([m for m in matches if m['status'] == 'missing'])
        implemented = total - missing

        return {
            "summary": {
                "total_requirements": total,
                "implemented": implemented,
                "missing": missing,
                "coverage_score": round((implemented / total * 10) if total > 0 else 0, 1)
            },
            "matches": matches,
            "requirement_features": self.requirement_features,
            "implementation_features": self.implementation_features
        }


def main():
    parser = argparse.ArgumentParser(description='需求匹配分析')
    parser.add_argument('--requirement', required=True, help='需求文档路径')
    parser.add_argument('--commit', default='HEAD', help='Git commit reference')
    args = parser.parse_args()

    # 读取需求文档
    req_path = Path(args.requirement)
    if not req_path.exists():
        # 如果不是文件路径,可能是直接输入的文本
        requirement_text = args.requirement
    else:
        requirement_text = req_path.read_text(encoding='utf-8')

    # 读取代码变更 (从 analyze_commit.py 的输出)
    import subprocess
    script_dir = Path(__file__).parent
    analyze_script = script_dir / "analyze_commit.py"

    result = subprocess.run(
        ["python3", str(analyze_script), args.commit],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error: 无法分析提交: {result.stderr}")
        return

    code_changes = json.loads(result.stdout)

    # 执行匹配分析
    matcher = RequirementMatcher(requirement_text, code_changes)
    analysis = matcher.analyze()

    # 输出结果
    print(json.dumps(analysis, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
