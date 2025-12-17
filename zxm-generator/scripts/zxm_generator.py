#!/usr/bin/env python3
"""
ZXM Generator - Markdown + 内联装饰
- 输入：Markdown 文件（支持 <<{JSON}>> 内联装饰）
- 输出：知犀思维导图 .zxm 文件
"""
import json
import re
import uuid
import zipfile
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field


def gen_id() -> str:
    """生成知犀格式的 ID"""
    return str(uuid.uuid4()).replace('-', '')[:21]


# ============ 图标映射表（复用 v1）============

MARK_MAP = {
    "star": 25, "medal": 26, "heart": 27, "heart-broken": 28, "flag": 29, "star-orange": 30,
    "arrow-up-left": 31, "arrow-up": 32, "arrow-up-right": 33, "arrow-right": 34,
    "arrow-down-right": 35, "arrow-down": 36, "arrow-down-left": 37, "arrow-left": 38,
    "circle": 39, "check-circle": 40, "ban": 41, "check": 42, "cross": 43, "warning": 44, "question": 45,
    "calendar": 46, "clock": 47, "bell": 48,
    "location": 49, "mail": 50, "phone": 51, "chat": 52, "clipboard": 53, "chart": 54, "target": 55, "thumbs-up": 56,
    "trophy": 57, "diamond": 58, "money": 59, "woman": 60, "man": 61, "music": 62, "mic": 63, "headset": 64,
    "lightbulb": 65, "pencil": 66, "gift": 67, "alert": 68, "fire": 69,
}

EXPRESSION_MAP = {"cool": 1, "smile": 2, "happy": 3, "sad": 4, "tongue": 5, "cry": 7, "awkward": 8}

FLAG_MAP = {
    "flag-red": 1, "flag-orange": 2, "flag-blue": 3, "flag-green": 4, "flag-purple": 5,
    "flag-cyan": 6, "flag-peach": 7, "flag-lime": 8, "flag-teal": 9, "flag-light-blue": 10,
}

STAR_ICON_MAP = {
    "star-coral": 1, "star-orange": 2, "star-blue": 3, "star-green": 4, "star-purple": 5,
    "star-cyan": 6, "star-peach": 7, "star-lime": 8, "star-turquoise": 9, "star-light-blue": 10,
}

AVATAR_MAP = {
    "avatar-coral": 1, "avatar-orange": 2, "avatar-blue": 3, "avatar-green": 4, "avatar-purple": 5,
    "avatar-cyan": 6, "avatar-peach": 7, "avatar-lime": 8, "avatar-teal": 9, "avatar-slate-blue": 10,
}

MONTH_MAP = {
    "jan": 13, "feb": 14, "mar": 15, "apr": 16, "may": 17, "jun": 18,
    "jul": 19, "aug": 20, "sep": 21, "oct": 22, "nov": 23, "dec": 24,
    "jan-en": 1, "feb-en": 2, "mar-en": 3, "apr-en": 4, "may-en": 5, "jun-en": 6,
    "jul-en": 7, "aug-en": 8, "sep-en": 9, "oct-en": 10, "nov-en": 11, "dec-en": 12,
}

WEEK_MAP = {
    "mon": 8, "tue": 9, "wed": 10, "thu": 11, "fri": 12, "sat": 13, "sun": 14,
    "mon-en": 1, "tue-en": 2, "wed-en": 3, "thu-en": 4, "fri-en": 5, "sat-en": 6, "sun-en": 7,
}


# ============ 数据结构 ============

@dataclass
class MindMapConfig:
    theme: str = "classical2"
    template: str = "right"
    rainbow: bool = True
    rainbow_colors: list[str] = field(default_factory=lambda: [
        "#8CF0E7", "#4AD2FF", "#41A8F3", "#3180CD", "#BCE284", "#71D77B", "#78BF6D"
    ])

    def to_dict(self) -> dict:
        result = {"theme": self.theme, "template": self.template}
        if self.rainbow:
            result["rainbowColors"] = self.rainbow_colors
        return result


@dataclass
class NodeData:
    """从 Markdown 解析的节点"""
    line: int           # 行号（1-based）
    level: int          # 层级（1-based）
    text: str           # 节点文本
    decorations: dict = field(default_factory=dict)  # 装饰数据


@dataclass
class TreeNode:
    """树结构节点"""
    id: str
    data: NodeData
    children: list['TreeNode'] = field(default_factory=list)

    def to_zxm_dict(self) -> dict:
        """转换为知犀格式"""
        d = self.data.decorations
        text = self.data.text

        # 构建 richText
        text_attrs = {}
        if d.get('bold'):
            text_attrs["bold"] = True
        if d.get('italic'):
            text_attrs["italic"] = True
        if d.get('fc'):
            text_attrs["color"] = d['fc']
        if d.get('fs'):
            text_attrs["size"] = f"{d['fs']}px"

        rich_text = {
            "ops": [
                {"attributes": text_attrs, "insert": text},
                {"insert": "\n", "attributes": {}}
            ]
        }

        data: dict[str, Any] = {"text": text, "richText": rich_text}

        # 背景色
        if d.get('bg'):
            data["background"] = d['bg']

        # 备注
        if d.get('note'):
            data["note"] = d['note']

        # 超链接
        if d.get('link'):
            data["hyperlink"] = {"href": d['link'], "title": d['link']}

        # 优先级 (1-20 → 11-30)
        if d.get('priority') is not None:
            data["priority"] = d['priority'] + 10

        # 星级 (1-10)
        if d.get('star') is not None:
            data["star"] = d['star']

        # 进度条 (1-9)
        if d.get('progress') is not None:
            data["progress"] = d['progress']

        # 待办
        if d.get('todo'):
            data["todo"] = {"status": d['todo']}

        # 图标映射
        if d.get('mark') and d['mark'] in MARK_MAP:
            data["mark"] = MARK_MAP[d['mark']]
        if d.get('expression') and d['expression'] in EXPRESSION_MAP:
            data["expression"] = EXPRESSION_MAP[d['expression']]
        if d.get('flag') and d['flag'] in FLAG_MAP:
            data["flag"] = FLAG_MAP[d['flag']]
        if d.get('star_icon') and d['star_icon'] in STAR_ICON_MAP:
            data["starIcon"] = STAR_ICON_MAP[d['star_icon']]
        if d.get('avatar') and d['avatar'] in AVATAR_MAP:
            data["avatar"] = AVATAR_MAP[d['avatar']]
        if d.get('month') and d['month'] in MONTH_MAP:
            data["month"] = MONTH_MAP[d['month']]
        if d.get('week') and d['week'] in WEEK_MAP:
            data["week"] = WEEK_MAP[d['week']]

        # 公式
        if d.get('formula'):
            data["text"] = "\n"
            data["richText"] = {
                "ops": [
                    {"insert": {"formula": d['formula']}},
                    {"insert": "\n"}
                ]
            }

        result = {"id": self.id, "data": data}
        if self.children:
            result["children"] = {"normal": [c.to_zxm_dict() for c in self.children]}
        return result


# ============ Markdown 解析 ============

# 内联装饰正则：匹配 <<{...}>>
INLINE_DECORATION_PATTERN = re.compile(r'<<(\{.*?\})>>\s*$')


def parse_inline_decoration(text: str) -> tuple[str, dict]:
    """从文本中提取内联装饰，返回 (纯文本, 装饰dict)"""
    match = INLINE_DECORATION_PATTERN.search(text)
    if match:
        try:
            decoration = json.loads(match.group(1))
            clean_text = text[:match.start()].strip()
            return clean_text, decoration
        except json.JSONDecodeError:
            pass
    return text, {}


def parse_markdown(content: str) -> list[NodeData]:
    """解析 Markdown，返回节点列表（支持内联装饰 <<{...}>>）"""
    nodes = []
    lines = content.split('\n')

    # 检测格式：标题风格 or 列表风格
    first_content_line = next((l for l in lines if l.strip()), "")
    is_heading_style = first_content_line.strip().startswith('#')

    node_index = 0
    for line_num, line in enumerate(lines, start=1):
        stripped = line.rstrip()
        if not stripped:
            continue

        if is_heading_style:
            # 标题风格：# 数量 = 层级
            match = re.match(r'^(#+)\s+(.+)$', stripped)
            if match:
                level = len(match.group(1))
                raw_text = match.group(2).strip()
                text, decoration = parse_inline_decoration(raw_text)
                node_index += 1
                nodes.append(NodeData(line=node_index, level=level, text=text, decorations=decoration))
        else:
            # 列表风格：缩进 / 2 + 1 = 层级
            match = re.match(r'^(\s*)[-*+]\s+(.+)$', stripped)
            if match:
                indent = len(match.group(1))
                level = indent // 2 + 1
                raw_text = match.group(2).strip()
                text, decoration = parse_inline_decoration(raw_text)
                node_index += 1
                nodes.append(NodeData(line=node_index, level=level, text=text, decorations=decoration))

    return nodes


def build_tree(nodes: list[NodeData]) -> TreeNode:
    """从节点列表构建树结构"""
    if not nodes:
        raise ValueError("No nodes found in Markdown")

    # 创建根节点
    root_data = nodes[0]
    root = TreeNode(id=gen_id(), data=root_data)

    # 用栈维护父节点链
    stack: list[TreeNode] = [root]

    for node_data in nodes[1:]:
        tree_node = TreeNode(id=gen_id(), data=node_data)

        # 找到合适的父节点
        while len(stack) > 1 and stack[-1].data.level >= node_data.level:
            stack.pop()

        # 添加为子节点
        stack[-1].children.append(tree_node)
        stack.append(tree_node)

    return root


# ============ 配置提取 ============

def extract_config_from_root(root: TreeNode) -> MindMapConfig:
    """从根节点装饰中提取全局配置"""
    config = MindMapConfig()
    d = root.data.decorations

    if 'theme' in d:
        config.theme = d.pop('theme')
    if 'template' in d:
        config.template = d.pop('template')
    if 'rainbow' in d:
        config.rainbow = d.pop('rainbow')

    return config


# ============ ZXM 生成 ============

class ZXMGenerator:
    def __init__(self, root: TreeNode, config: MindMapConfig):
        self.root = root
        self.config = config
        self.content_id = gen_id()

    def _generate_content_json(self) -> dict:
        return {
            "ver": 2,
            "contents": [{
                "id": self.content_id,
                "title": "",
                "type": "mind",
                "root": self.root.to_zxm_dict(),
                "config": self.config.to_dict()
            }]
        }

    def _generate_metadata_json(self) -> dict:
        return {"type": "mindmap", "template": self.config.template, "creator": "ai-generator"}

    def save(self, output_path: str) -> Path:
        output_path = Path(output_path)
        if not output_path.suffix:
            output_path = output_path.with_suffix('.zxm')

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('content.json', json.dumps(self._generate_content_json(), ensure_ascii=False))
            zf.writestr('metadata.json', json.dumps(self._generate_metadata_json(), ensure_ascii=False))
            zf.writestr('manifest.json', '{}')
            zf.writestr('resources/.keep', '')

        print(f"✅ 已生成: {output_path}")
        return output_path


# ============ 主接口 ============

def generate_zxm(md_path: str, output_path: str) -> str:
    """从 Markdown 文件生成 ZXM

    Args:
        md_path: Markdown 文件路径（支持内联装饰 <<{...}>>）
        output_path: 输出 .zxm 路径

    Returns:
        生成的文件路径
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    return generate_zxm_from_content(md_content, output_path)


def generate_zxm_from_content(md_content: str, output_path: str) -> str:
    """从 Markdown 内容生成 ZXM"""
    nodes = parse_markdown(md_content)
    root = build_tree(nodes)
    config = extract_config_from_root(root)

    generator = ZXMGenerator(root, config)
    return str(generator.save(output_path))


def preview_nodes(md_content: str) -> str:
    """预览 Markdown 节点结构（显示节点索引和装饰）"""
    nodes = parse_markdown(md_content)
    lines = []
    for node in nodes:
        indent = "  " * (node.level - 1)
        deco_str = f" <<{json.dumps(node.decorations, ensure_ascii=False)}>>" if node.decorations else ""
        lines.append(f"[{node.line:2d}] {indent}{node.text}{deco_str}")
    return "\n".join(lines)


# 保留旧名称，向后兼容
preview_lines = preview_nodes


def validate_markdown(md_content: str) -> list[str]:
    """验证 Markdown 格式，返回错误列表"""
    errors = []
    nodes = parse_markdown(md_content)

    if not nodes:
        errors.append("错误: Markdown 中没有找到任何节点")
        return errors

    # 检查根节点
    if nodes[0].level != 1:
        errors.append(f"警告: 根节点层级为 {nodes[0].level}，建议从 # 开始")

    # 检查层级跳跃
    for i in range(1, len(nodes)):
        prev_level = nodes[i-1].level
        curr_level = nodes[i].level
        if curr_level > prev_level + 1:
            errors.append(f"警告: 节点 [{nodes[i].line}] '{nodes[i].text}' 层级跳跃（从 {prev_level} 到 {curr_level}）")

    # 检查主分支数量 (Miller's Law)
    root_children = sum(1 for n in nodes if n.level == 2)
    if root_children > 7:
        errors.append(f"建议: 一级分支有 {root_children} 个，超过 7 个可能增加认知负荷")

    # 检查内联装饰 JSON 格式
    lines = md_content.split('\n')
    for line_num, line in enumerate(lines, start=1):
        match = re.search(r'<<(\{.*?\})>>', line)
        if match:
            try:
                json.loads(match.group(1))
            except json.JSONDecodeError as e:
                errors.append(f"错误: 第 {line_num} 行内联装饰 JSON 格式错误: {e}")

    return errors


# ============ CLI ============

def main():
    import argparse
    parser = argparse.ArgumentParser(description='ZXM Generator - Markdown to 知犀思维导图')
    parser.add_argument('input', nargs='?', help='输入 Markdown 文件路径')
    parser.add_argument('-o', '--output', help='输出 .zxm 文件路径')
    parser.add_argument('--validate', action='store_true', help='仅验证，不生成文件')
    parser.add_argument('--preview', action='store_true', help='预览节点结构')
    parser.add_argument('--test', action='store_true', help='运行内置测试')

    args = parser.parse_args()

    if args.test:
        run_test()
        return

    if not args.input:
        parser.print_help()
        return

    with open(args.input, 'r', encoding='utf-8') as f:
        content = f.read()

    if args.validate:
        errors = validate_markdown(content)
        if errors:
            print("验证结果:")
            for e in errors:
                print(f"  - {e}")
        else:
            print("✅ 验证通过")
        return

    if args.preview:
        print(preview_nodes(content))
        return

    output = args.output or args.input.rsplit('.', 1)[0] + '.zxm'
    generate_zxm(args.input, output)


def run_test():
    """运行内置测试（使用内联装饰）"""
    test_md = """# Python学习路线 <<{"theme":"ai-classical1","bg":"#4A90D9","fc":"#FFFFFF","bold":true}>>
## 基础语法 <<{"priority":1,"mark":"flag"}>>
### 变量与数据类型
### 函数
## 面向对象 <<{"priority":2,"mark":"target"}>>
### 类与对象
### 继承多态
## 进阶主题 <<{"priority":3,"mark":"trophy"}>>
### 异步编程 <<{"link":"https://docs.python.org/3/library/asyncio.html"}>>
### 元编程
"""

    print("=== 内联装饰示例 ===")
    print(test_md)
    print("\n=== 节点预览 ===")
    print(preview_nodes(test_md))
    print("\n=== 验证结果 ===")
    errors = validate_markdown(test_md)
    if errors:
        for e in errors:
            print(f"  - {e}")
    else:
        print("✅ 验证通过")

    output = generate_zxm_from_content(test_md, "/tmp/test_zxm.zxm")
    print(f"\n✅ 测试文件: {output}")


if __name__ == "__main__":
    main()
