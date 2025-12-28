#!/usr/bin/env python3
"""
Asset Lookup - JSON 知识库快速查询工具

用法:
    # 按用例查找
    python asset_lookup.py --use-case microservice_architecture

    # 按关键词查找
    python asset_lookup.py --keyword database

    # 按 ID 查找
    python asset_lookup.py --id aws_lambda

    # 获取样式预设
    python asset_lookup.py --preset frozen_model

    # 获取配色方案
    python asset_lookup.py --color kubernetes

输入: 用例/关键词/ID
输出: 完整的组件定义 (JSON)
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any


class AssetKnowledgeBase:
    """JSON 知识库"""

    def __init__(self, assets_dir: Optional[Path] = None):
        """初始化知识库"""
        if assets_dir is None:
            script_dir = Path(__file__).parent
            assets_dir = script_dir.parent / 'references' / 'assets'

        self.assets_dir = assets_dir
        self.index: Dict = {}
        self.cloud_icons: Dict = {}
        self.basic_shapes: Dict = {}
        self.domain_assets: Dict = {}
        self._loaded = False

    def load(self) -> bool:
        """加载所有 JSON 文件"""
        if self._loaded:
            return True

        try:
            # 加载索引
            index_path = self.assets_dir / 'index.json'
            if index_path.exists():
                with open(index_path, 'r', encoding='utf-8') as f:
                    self.index = json.load(f)

            # 加载云图标
            cloud_path = self.assets_dir / 'cloud_icons.json'
            if cloud_path.exists():
                with open(cloud_path, 'r', encoding='utf-8') as f:
                    self.cloud_icons = json.load(f)

            # 加载基础形状
            shapes_path = self.assets_dir / 'basic_shapes.json'
            if shapes_path.exists():
                with open(shapes_path, 'r', encoding='utf-8') as f:
                    self.basic_shapes = json.load(f)

            # 加载领域素材
            domain_path = self.assets_dir / 'domain_assets.json'
            if domain_path.exists():
                with open(domain_path, 'r', encoding='utf-8') as f:
                    self.domain_assets = json.load(f)

            self._loaded = True
            return True

        except Exception as e:
            print(f"❌ 加载知识库失败: {e}", file=sys.stderr)
            return False

    def get_by_use_case(self, use_case: str) -> Optional[Dict]:
        """按用例获取推荐组件"""
        self.load()

        use_cases = self.index.get('quick_lookup', {}).get('by_use_case', {})
        if use_case not in use_cases:
            return None

        use_case_def = use_cases[use_case]
        recommended_ids = use_case_def.get('recommended', [])

        # 查找每个推荐组件的完整定义
        components = []
        for comp_id in recommended_ids:
            comp = self.get_by_id(comp_id)
            if comp:
                components.append(comp)

        return {
            'use_case': use_case,
            'recommended_container': use_case_def.get('container'),
            'edge_style': use_case_def.get('edge_style'),
            'components': components
        }

    def get_by_keyword(self, keyword: str) -> List[Dict]:
        """按关键词获取组件列表"""
        self.load()

        keywords = self.index.get('quick_lookup', {}).get('by_keyword', {})
        if keyword not in keywords:
            # 尝试模糊匹配
            matched = []
            for kw, ids in keywords.items():
                if keyword.lower() in kw.lower():
                    matched.extend(ids)
            if not matched:
                return []
            component_ids = list(set(matched))
        else:
            component_ids = keywords[keyword]

        components = []
        for comp_id in component_ids:
            comp = self.get_by_id(comp_id)
            if comp:
                components.append(comp)

        return components

    def get_by_id(self, component_id: str) -> Optional[Dict]:
        """按 ID 获取组件完整定义"""
        self.load()

        # 搜索云图标
        for vendor, vendor_data in self.cloud_icons.get('categories', {}).items():
            for category, icons in vendor_data.get('icons', {}).items():
                for icon in icons:
                    if icon.get('id') == component_id:
                        return {
                            **icon,
                            'vendor': vendor,
                            'category': category,
                            'source': 'cloud_icons'
                        }

        # 搜索基础形状
        for category, shapes in self.basic_shapes.get('shapes', {}).items():
            for shape in shapes:
                if shape.get('id') == component_id:
                    return {
                        **shape,
                        'category': category,
                        'source': 'basic_shapes'
                    }

        # 搜索边
        for category, edges in self.basic_shapes.get('edges', {}).items():
            for edge in edges:
                if edge.get('id') == component_id:
                    return {
                        **edge,
                        'category': category,
                        'source': 'basic_shapes',
                        'type': 'edge'
                    }

        # 搜索领域素材
        for domain, domain_data in self.domain_assets.get('domains', {}).items():
            for category, components in domain_data.get('components', {}).items():
                for comp in components:
                    if comp.get('id') == component_id:
                        return {
                            **comp,
                            'domain': domain,
                            'category': category,
                            'source': 'domain_assets'
                        }

        return None

    def get_preset(self, preset_name: str) -> Optional[Dict]:
        """获取样式预设"""
        self.load()

        presets = self.index.get('style_presets', {})
        return presets.get(preset_name)

    def get_color_scheme(self, scheme_name: str) -> Optional[Dict]:
        """获取配色方案"""
        self.load()

        schemes = self.index.get('color_schemes', {})
        return schemes.get(scheme_name)

    def search_by_tags(self, query: str, limit: int = 10) -> List[Dict]:
        """按标签搜索（简单关键词匹配）"""
        self.load()

        query_lower = query.lower()
        results = []

        # 搜索所有来源
        sources = [
            ('cloud_icons', self.cloud_icons.get('categories', {})),
            ('basic_shapes', self.basic_shapes.get('shapes', {})),
            ('domain_assets', self.domain_assets.get('domains', {})),
        ]

        for source_name, source_data in sources:
            self._search_recursive(source_data, query_lower, results, source_name)

        # 按匹配度排序
        results.sort(key=lambda x: x.get('match_score', 0), reverse=True)

        return results[:limit]

    def _search_recursive(self, data: Any, query: str, results: List, source: str):
        """递归搜索"""
        if isinstance(data, dict):
            # 检查是否是组件定义
            if 'id' in data and 'tags' in data:
                tags = data.get('tags', [])
                name = data.get('name', '').lower()
                name_cn = data.get('name_cn', '').lower()

                match_score = 0
                for tag in tags:
                    if query in tag.lower():
                        match_score += 1
                if query in name:
                    match_score += 2
                if query in name_cn:
                    match_score += 2

                if match_score > 0:
                    results.append({
                        **data,
                        'source': source,
                        'match_score': match_score
                    })
            else:
                # 继续搜索嵌套结构
                for value in data.values():
                    self._search_recursive(value, query, results, source)
        elif isinstance(data, list):
            for item in data:
                self._search_recursive(item, query, results, source)

    def list_use_cases(self) -> List[str]:
        """列出所有用例"""
        self.load()
        return list(self.index.get('quick_lookup', {}).get('by_use_case', {}).keys())

    def list_keywords(self) -> List[str]:
        """列出所有关键词"""
        self.load()
        return list(self.index.get('quick_lookup', {}).get('by_keyword', {}).keys())

    def list_presets(self) -> List[str]:
        """列出所有预设"""
        self.load()
        return list(self.index.get('style_presets', {}).keys())

    def list_color_schemes(self) -> List[str]:
        """列出所有配色方案"""
        self.load()
        return list(self.index.get('color_schemes', {}).keys())


def main():
    parser = argparse.ArgumentParser(description='Asset Lookup - JSON 知识库快速查询')
    parser.add_argument('--use-case', '-u', help='按用例查找')
    parser.add_argument('--keyword', '-k', help='按关键词查找')
    parser.add_argument('--id', '-i', help='按 ID 查找')
    parser.add_argument('--preset', '-p', help='获取样式预设')
    parser.add_argument('--color', '-c', help='获取配色方案')
    parser.add_argument('--search', '-s', help='按标签搜索')
    parser.add_argument('--list', '-l', choices=['use-cases', 'keywords', 'presets', 'colors'], help='列出可用选项')
    parser.add_argument('--limit', type=int, default=10, help='搜索结果数量限制')

    args = parser.parse_args()

    kb = AssetKnowledgeBase()

    if args.use_case:
        result = kb.get_by_use_case(args.use_case)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 未找到用例: {args.use_case}", file=sys.stderr)
            print(f"可用用例: {', '.join(kb.list_use_cases())}", file=sys.stderr)
            sys.exit(1)

    elif args.keyword:
        results = kb.get_by_keyword(args.keyword)
        if results:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 未找到关键词: {args.keyword}", file=sys.stderr)
            print(f"可用关键词: {', '.join(kb.list_keywords())}", file=sys.stderr)
            sys.exit(1)

    elif args.id:
        result = kb.get_by_id(args.id)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 未找到组件: {args.id}", file=sys.stderr)
            sys.exit(1)

    elif args.preset:
        result = kb.get_preset(args.preset)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 未找到预设: {args.preset}", file=sys.stderr)
            print(f"可用预设: {', '.join(kb.list_presets())}", file=sys.stderr)
            sys.exit(1)

    elif args.color:
        result = kb.get_color_scheme(args.color)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 未找到配色方案: {args.color}", file=sys.stderr)
            print(f"可用方案: {', '.join(kb.list_color_schemes())}", file=sys.stderr)
            sys.exit(1)

    elif args.search:
        results = kb.search_by_tags(args.search, limit=args.limit)
        if results:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 未找到匹配: {args.search}", file=sys.stderr)
            sys.exit(1)

    elif args.list:
        if args.list == 'use-cases':
            for uc in kb.list_use_cases():
                print(f"  • {uc}")
        elif args.list == 'keywords':
            for kw in kb.list_keywords():
                print(f"  • {kw}")
        elif args.list == 'presets':
            for p in kb.list_presets():
                print(f"  • {p}")
        elif args.list == 'colors':
            for c in kb.list_color_schemes():
                print(f"  • {c}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
