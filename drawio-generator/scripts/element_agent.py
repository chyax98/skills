#!/usr/bin/env python3
"""
Element Agent - 元素匹配工具

用法:
    python element_agent.py --spec spec.json --theme professional --output styles.json
    echo '{"nodes":[...]}' | python element_agent.py --theme tech

输入: DiagramSpec JSON (只需 nodes 和 theme)
输出: ElementStyles JSON
"""

import json
import sys
import argparse
from typing import Dict, List, Optional


# ============ 形状库 ============

SHAPE_LIBRARY = {
    # 基础形状
    'rect': 'rounded=0;whiteSpace=wrap;html=1;',
    'rounded_rect': 'rounded=1;whiteSpace=wrap;html=1;arcSize=20;',
    'ellipse': 'ellipse;whiteSpace=wrap;html=1;',
    'diamond': 'rhombus;whiteSpace=wrap;html=1;',
    'cylinder': 'shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;',
    'hexagon': 'shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;',
    'parallelogram': 'shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;',
    'document': 'shape=document;whiteSpace=wrap;html=1;boundedLbl=1;',
    'terminator': 'rounded=1;whiteSpace=wrap;html=1;arcSize=50;',
    'cloud': 'ellipse;shape=cloud;whiteSpace=wrap;html=1;',
    'actor': 'shape=actor;whiteSpace=wrap;html=1;',
}

# ============ 节点类型到形状映射 ============

TYPE_SHAPE_MAP = {
    # 架构图
    'gateway': 'rounded_rect',
    'service': 'rounded_rect',
    'microservice': 'rounded_rect',
    'api': 'rounded_rect',
    'database': 'cylinder',
    'db': 'cylinder',
    'mysql': 'cylinder',
    'postgresql': 'cylinder',
    'mongodb': 'cylinder',
    'redis': 'rounded_rect',
    'cache': 'rounded_rect',
    'queue': 'rect',
    'mq': 'rect',
    'kafka': 'rect',
    'rabbitmq': 'rect',
    'loadbalancer': 'rounded_rect',
    'lb': 'rounded_rect',
    'firewall': 'rect',

    # 用户/客户端
    'user': 'ellipse',
    'client': 'rounded_rect',
    'browser': 'rounded_rect',
    'mobile': 'rounded_rect',
    'app': 'rounded_rect',

    # 流程图
    'start': 'terminator',
    'end': 'terminator',
    'process': 'rounded_rect',
    'decision': 'diamond',
    'condition': 'diamond',
    'document': 'document',
    'data': 'parallelogram',

    # 网络
    'server': 'rounded_rect',
    'router': 'rounded_rect',
    'switch': 'rounded_rect',
    'cloud': 'cloud',

    # 默认
    'default': 'rounded_rect',
}

# ============ 主题颜色 ============

THEMES = {
    'professional': {
        'primary': {'fill': '#dae8fc', 'stroke': '#6c8ebf', 'font': '#333333'},
        'secondary': {'fill': '#d5e8d4', 'stroke': '#82b366', 'font': '#333333'},
        'accent': {'fill': '#fff2cc', 'stroke': '#d6b656', 'font': '#333333'},
        'danger': {'fill': '#f8cecc', 'stroke': '#b85450', 'font': '#333333'},
        'neutral': {'fill': '#f5f5f5', 'stroke': '#666666', 'font': '#333333'},
        'edge': '#666666',
    },
    'tech': {
        'primary': {'fill': '#1565C0', 'stroke': 'none', 'font': '#FFFFFF', 'gradient': '#0D47A1'},
        'secondary': {'fill': '#26A69A', 'stroke': 'none', 'font': '#FFFFFF', 'gradient': '#00897B'},
        'accent': {'fill': '#FF7043', 'stroke': 'none', 'font': '#FFFFFF', 'gradient': '#E64A19'},
        'danger': {'fill': '#E53935', 'stroke': 'none', 'font': '#FFFFFF', 'gradient': '#C62828'},
        'neutral': {'fill': '#37474F', 'stroke': 'none', 'font': '#FFFFFF', 'gradient': '#263238'},
        'edge': '#00ACC1',
    },
    'minimal': {
        'primary': {'fill': '#FFFFFF', 'stroke': '#333333', 'font': '#333333'},
        'secondary': {'fill': '#FAFAFA', 'stroke': '#666666', 'font': '#333333'},
        'accent': {'fill': '#E3F2FD', 'stroke': '#1976D2', 'font': '#333333'},
        'neutral': {'fill': '#FFFFFF', 'stroke': '#9E9E9E', 'font': '#666666'},
        'edge': '#333333',
    },
    'colorful': {
        'primary': {'fill': '#E3F2FD', 'stroke': '#1565C0', 'font': '#333333'},
        'secondary': {'fill': '#E8F5E9', 'stroke': '#2E7D32', 'font': '#333333'},
        'accent': {'fill': '#FFF3E0', 'stroke': '#E65100', 'font': '#333333'},
        'danger': {'fill': '#FFEBEE', 'stroke': '#C62828', 'font': '#333333'},
        'purple': {'fill': '#F3E5F5', 'stroke': '#7B1FA2', 'font': '#333333'},
        'teal': {'fill': '#E0F2F1', 'stroke': '#00695C', 'font': '#333333'},
        'neutral': {'fill': '#F5F5F5', 'stroke': '#616161', 'font': '#333333'},
        'edge': '#616161',
    },
    'dark': {
        'primary': {'fill': '#1E1E1E', 'stroke': '#3C3C3C', 'font': '#FFFFFF'},
        'secondary': {'fill': '#252526', 'stroke': '#3C3C3C', 'font': '#FFFFFF'},
        'accent': {'fill': '#0E639C', 'stroke': '#1177BB', 'font': '#FFFFFF'},
        'neutral': {'fill': '#2D2D2D', 'stroke': '#3C3C3C', 'font': '#CCCCCC'},
        'edge': '#888888',
    },
}

# ============ 节点类型到颜色角色映射 ============

TYPE_COLOR_MAP = {
    'gateway': 'secondary',
    'api': 'secondary',
    'service': 'primary',
    'microservice': 'primary',
    'database': 'neutral',
    'db': 'neutral',
    'cache': 'accent',
    'redis': 'accent',
    'queue': 'secondary',
    'mq': 'secondary',
    'kafka': 'secondary',
    'loadbalancer': 'accent',
    'lb': 'accent',
    'firewall': 'danger',
    'client': 'primary',
    'user': 'neutral',
    'start': 'secondary',
    'end': 'danger',
    'decision': 'accent',
    'condition': 'accent',
    'default': 'primary',
}


class ElementMatcher:
    """元素匹配器"""

    def __init__(self, theme: str = 'professional'):
        self.theme_name = theme
        self.theme = THEMES.get(theme, THEMES['professional'])

    def match(self, spec: dict) -> dict:
        """匹配元素样式"""
        nodes = spec.get('nodes', [])
        custom_styles = spec.get('custom_styles', {})

        node_styles = {}
        for node in nodes:
            node_id = node['id']
            node_type = node.get('type', 'default').lower()

            # 获取形状
            shape_key = TYPE_SHAPE_MAP.get(node_type, 'rounded_rect')
            base_style = SHAPE_LIBRARY.get(shape_key, SHAPE_LIBRARY['rounded_rect'])

            # 获取颜色
            color_role = TYPE_COLOR_MAP.get(node_type, 'primary')
            colors = self.theme.get(color_role, self.theme.get('primary'))

            # 组合样式
            style = self._build_style(base_style, colors)

            # 应用自定义覆盖
            if node_id in custom_styles:
                style = self._apply_custom(style, custom_styles[node_id])

            node_styles[node_id] = {
                'shape': shape_key,
                'style': style
            }

        # 边样式
        edge_color = self.theme.get('edge', '#666666')
        edge_style = f'edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;strokeColor={edge_color};'

        return {
            'node_styles': node_styles,
            'edge_style': edge_style,
            'theme_applied': self.theme_name
        }

    def _build_style(self, base_style: str, colors: dict) -> str:
        """构建完整样式"""
        parts = [base_style.rstrip(';')]

        # 填充色
        if colors.get('fill'):
            parts.append(f"fillColor={colors['fill']}")

        # 渐变
        if colors.get('gradient'):
            parts.append(f"gradientColor={colors['gradient']}")
            parts.append("gradientDirection=south")

        # 边框
        if colors.get('stroke'):
            if colors['stroke'] == 'none':
                parts.append("strokeColor=none")
            else:
                parts.append(f"strokeColor={colors['stroke']}")

        # 文字颜色
        if colors.get('font'):
            parts.append(f"fontColor={colors['font']}")

        # 阴影 (tech 主题)
        if self.theme_name == 'tech':
            parts.append("shadow=1")

        return ';'.join(parts) + ';'

    def _apply_custom(self, style: str, custom: dict) -> str:
        """应用自定义样式"""
        parts = style.rstrip(';').split(';')

        for key, value in custom.items():
            # 移除旧值
            parts = [p for p in parts if not p.startswith(f'{key}=')]
            parts.append(f'{key}={value}')

        return ';'.join(parts) + ';'


def main():
    parser = argparse.ArgumentParser(description='Element Agent - 元素匹配')
    parser.add_argument('--spec', '-s', help='DiagramSpec JSON 文件路径')
    parser.add_argument('--output', '-o', help='输出 ElementStyles JSON 文件路径')
    parser.add_argument('--theme', '-t', default='professional',
                        choices=['professional', 'tech', 'minimal', 'colorful', 'dark'],
                        help='颜色主题')
    parser.add_argument('--list-themes', action='store_true', help='列出所有主题')
    parser.add_argument('--list-types', action='store_true', help='列出所有节点类型')

    args = parser.parse_args()

    if args.list_themes:
        print("可用主题:")
        for name in THEMES:
            print(f"  - {name}")
        return

    if args.list_types:
        print("节点类型 → 形状映射:")
        for t, s in sorted(TYPE_SHAPE_MAP.items()):
            print(f"  {t:15} → {s}")
        return

    # 读取输入
    if args.spec:
        with open(args.spec, 'r', encoding='utf-8') as f:
            spec = json.load(f)
    else:
        spec = json.load(sys.stdin)

    # 覆盖主题
    theme = spec.get('theme', args.theme)

    # 匹配
    matcher = ElementMatcher(theme)
    result = matcher.match(spec)

    # 输出
    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"✅ Styles saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
