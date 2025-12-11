#!/usr/bin/env python3
"""
ZXM (知犀思维导图) 文件生成器 v2
- 输入：JSONL 格式的简化 DSL
- 输出：可被知犀打开的 .zxm 文件
"""
import json
import uuid
import zipfile
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field


def gen_id() -> str:
    """生成类似知犀的 ID 格式"""
    return str(uuid.uuid4()).replace('-', '')[:21]


# ============ 图标映射表 ============

# mark 图标：DSL 使用语义化名称，映射到知犀的 25-69 数值
MARK_MAP = {
    # 收藏/评价类
    "star": 25,           # ⭐ 黄色星星
    "medal": 26,          # 🏅 奖章
    "heart": 27,          # ❤️ 红心
    "heart-broken": 28,   # 💔 破碎的心
    "flag": 29,           # 🚩 红旗
    "star-orange": 30,    # ⭐ 橙色星星

    # 箭头方向类
    "arrow-up-left": 31,     # ↖ 左上箭头
    "arrow-up": 32,          # ↑ 上箭头
    "arrow-up-right": 33,    # ↗ 右上箭头
    "arrow-right": 34,       # → 右箭头
    "arrow-down-right": 35,  # ↘ 右下箭头
    "arrow-down": 36,        # ↓ 下箭头
    "arrow-down-left": 37,   # ↙ 左下箭头
    "arrow-left": 38,        # ← 左箭头

    # 状态类
    "circle": 39,         # ○ 空心圆
    "check-circle": 40,   # ✅ 绿色对勾圆
    "ban": 41,            # 🚫 禁止
    "check": 42,          # ✓ 绿色对勾
    "cross": 43,          # ✗ 红色叉
    "warning": 44,        # ⚠️ 红色感叹号
    "question": 45,       # ❓ 橙色问号

    # 时间/提醒类
    "calendar": 46,       # 📅 日历
    "clock": 47,          # ⏰ 时钟
    "bell": 48,           # 🔔 铃铛

    # 通讯/工具类
    "location": 49,       # 📍 定位
    "mail": 50,           # ✉️ 邮件
    "phone": 51,          # 📞 电话
    "chat": 52,           # 💬 聊天气泡
    "clipboard": 53,      # 📋 剪贴板
    "chart": 54,          # 📊 柱状图
    "target": 55,         # 🎯 靶心
    "thumbs-up": 56,      # 👍 点赞

    # 其他
    "trophy": 57,         # 🏆 奖杯
    "diamond": 58,        # 💎 钻石
    "money": 59,          # 💰 金币
    "woman": 60,          # 👩 女性头像
    "man": 61,            # 👨 男性头像
    "music": 62,          # 🎵 音乐
    "mic": 63,            # 🎤 麦克风
    "headset": 64,        # 🎧 耳机

    # 新增 (65-69)
    "lightbulb": 65,      # 💡 灯泡/想法
    "pencil": 66,         # ✏️ 铅笔/编辑
    "gift": 67,           # 🎁 礼物
    "alert": 68,          # ⚠️ 警告三角
    "fire": 69,           # 🔥 火焰/热门
}

# expression 表情图标：DSL 使用语义化名称 (1-8, 6 不存在)
EXPRESSION_MAP = {
    "cool": 1,      # 😎 墨镜酷
    "smile": 2,     # 🙂 微笑
    "happy": 3,     # 😃 开心
    "sad": 4,       # 😢 伤心
    "tongue": 5,    # 😛 吐舌头
    "cry": 7,       # 😭 大哭
    "awkward": 8,   # 😬 尴尬/紧张
}

# flag 旗帜图标：彩色旗帜 (1-10)
FLAG_MAP = {
    "flag-red": 1,        # 🚩 红色旗帜
    "flag-orange": 2,     # 🟠 橙色旗帜
    "flag-blue": 3,       # 🔵 蓝色旗帜
    "flag-green": 4,      # 🟢 绿色旗帜
    "flag-purple": 5,     # 🟣 紫色旗帜
    "flag-cyan": 6,       # 青色旗帜
    "flag-peach": 7,      # 桃红旗帜
    "flag-lime": 8,       # 黄绿旗帜
    "flag-teal": 9,       # 蓝绿旗帜
    "flag-light-blue": 10,  # 浅蓝旗帜
}

# star 五角星图标：彩色星星 (1-10)
STAR_ICON_MAP = {
    "star-coral": 1,      # 珊瑚红星星
    "star-orange": 2,     # 橙色星星
    "star-blue": 3,       # 蓝色星星
    "star-green": 4,      # 绿色星星
    "star-purple": 5,     # 紫色星星
    "star-cyan": 6,       # 青色星星
    "star-peach": 7,      # 桃色星星
    "star-lime": 8,       # 黄绿星星
    "star-turquoise": 9,  # 青绿星星
    "star-light-blue": 10,  # 浅蓝星星
}

# avatar 头像图标：彩色头像 (1-10)
AVATAR_MAP = {
    "avatar-coral": 1,       # 珊瑚红头像
    "avatar-orange": 2,      # 橙色头像
    "avatar-blue": 3,        # 蓝色头像
    "avatar-green": 4,       # 绿色头像
    "avatar-purple": 5,      # 紫色头像
    "avatar-cyan": 6,        # 青色头像
    "avatar-peach": 7,       # 桃色头像
    "avatar-lime": 8,        # 黄绿头像
    "avatar-teal": 9,        # 蓝绿头像
    "avatar-slate-blue": 10,  # 石蓝头像
}

# month 月份图标 (1-24)
MONTH_MAP = {
    # 中文月份（默认）→ 知犀 13-24
    "jan": 13, "feb": 14, "mar": 15, "apr": 16,
    "may": 17, "jun": 18, "jul": 19, "aug": 20,
    "sep": 21, "oct": 22, "nov": 23, "dec": 24,
    # 英文月份 → 知犀 1-12
    "jan-en": 1, "feb-en": 2, "mar-en": 3, "apr-en": 4,
    "may-en": 5, "jun-en": 6, "jul-en": 7, "aug-en": 8,
    "sep-en": 9, "oct-en": 10, "nov-en": 11, "dec-en": 12,
}

# week 星期图标 (1-14)
WEEK_MAP = {
    # 中文星期（默认）→ 知犀 8-14
    "mon": 8, "tue": 9, "wed": 10, "thu": 11,
    "fri": 12, "sat": 13, "sun": 14,
    # 英文星期 → 知犀 1-7
    "mon-en": 1, "tue-en": 2, "wed-en": 3, "thu-en": 4,
    "fri-en": 5, "sat-en": 6, "sun-en": 7,
}


# ============ 数据类 ============

@dataclass
class NodeStyle:
    background: Optional[str] = None
    font_color: Optional[str] = None
    font_size: Optional[int] = None
    bold: bool = False
    italic: bool = False


@dataclass
class NodeContent:
    text: str
    note: Optional[str] = None           # 备注
    link: Optional[str] = None           # 超链接
    priority: Optional[int] = None       # 优先级图标 (1-20)
    star: Optional[int] = None           # 星级评分 (1-10)
    progress: Optional[int] = None       # 进度条 (1-9)
    todo: Optional[str] = None           # 待办状态 ("done" / "undone")
    mark: Optional[str] = None           # 标记图标 (语义化名称，见 MARK_MAP)
    expression: Optional[str] = None     # 表情图标 (语义化名称，见 EXPRESSION_MAP)
    # 图标类型
    flag: Optional[str] = None           # 旗帜图标 (语义化名称，见 FLAG_MAP)
    star_icon: Optional[str] = None      # 彩色星星图标 (语义化名称，见 STAR_ICON_MAP)
    avatar: Optional[str] = None         # 头像图标 (语义化名称，见 AVATAR_MAP)
    month: Optional[str] = None          # 月份图标 (语义化名称，见 MONTH_MAP)
    week: Optional[str] = None           # 星期图标 (语义化名称，见 WEEK_MAP)
    # 公式
    formula: Optional[str] = None        # LaTeX 公式


@dataclass
class MindNode:
    id: str
    content: NodeContent
    style: NodeStyle = field(default_factory=NodeStyle)
    children: list['MindNode'] = field(default_factory=list)

    def to_zxm_dict(self) -> dict:
        """转换为知犀 content.json 格式"""
        # 构建 richText (Quill Delta 格式)
        text_attrs = {}
        if self.style.bold:
            text_attrs["bold"] = True
        if self.style.italic:
            text_attrs["italic"] = True
        if self.style.font_color:
            text_attrs["color"] = self.style.font_color
        if self.style.font_size:
            text_attrs["size"] = f"{self.style.font_size}px"

        rich_text = {
            "ops": [
                {"attributes": text_attrs, "insert": self.content.text},
                {"insert": "\n", "attributes": {}}
            ]
        }

        # 基础数据
        data: dict[str, Any] = {
            "text": self.content.text,
            "richText": rich_text,
        }

        # 背景色
        if self.style.background:
            data["background"] = self.style.background

        # 备注
        if self.content.note:
            data["note"] = self.content.note

        # 超链接 (知犀用 hyperlink，不是 hyperLink)
        if self.content.link:
            data["hyperlink"] = {
                "href": self.content.link,
                "title": self.content.link
            }

        # 优先级图标 (DSL: 1-10 → 知犀: 11-20)
        if self.content.priority is not None:
            data["priority"] = self.content.priority + 10

        # 星级评分 (1-10)
        if self.content.star is not None:
            data["star"] = self.content.star

        # 进度条 (1-9)
        if self.content.progress is not None:
            data["progress"] = self.content.progress

        # 待办事项
        if self.content.todo is not None:
            data["todo"] = {"status": self.content.todo}

        # 标记图标 (DSL 语义化名称 → 知犀数值)
        if self.content.mark is not None:
            mark_value = MARK_MAP.get(self.content.mark)
            if mark_value:
                data["mark"] = mark_value

        # 表情图标 (DSL 语义化名称 → 知犀数值)
        if self.content.expression is not None:
            expr_value = EXPRESSION_MAP.get(self.content.expression)
            if expr_value:
                data["expression"] = expr_value

        # 旗帜图标 (DSL 语义化名称 → 知犀数值)
        if self.content.flag is not None:
            flag_value = FLAG_MAP.get(self.content.flag)
            if flag_value:
                data["flag"] = flag_value

        # 彩色星星图标 (DSL 语义化名称 → 知犀数值)
        if self.content.star_icon is not None:
            star_icon_value = STAR_ICON_MAP.get(self.content.star_icon)
            if star_icon_value:
                data["starIcon"] = star_icon_value

        # 头像图标 (DSL 语义化名称 → 知犀数值)
        if self.content.avatar is not None:
            avatar_value = AVATAR_MAP.get(self.content.avatar)
            if avatar_value:
                data["avatar"] = avatar_value

        # 月份图标 (DSL 语义化名称 → 知犀数值)
        if self.content.month is not None:
            month_value = MONTH_MAP.get(self.content.month)
            if month_value:
                data["month"] = month_value

        # 星期图标 (DSL 语义化名称 → 知犀数值)
        if self.content.week is not None:
            week_value = WEEK_MAP.get(self.content.week)
            if week_value:
                data["week"] = week_value

        # 公式 (LaTeX)：修改 richText 以嵌入公式
        if self.content.formula is not None:
            # 知犀公式节点的 text 必须是 "\n"
            data["text"] = "\n"
            data["richText"] = {
                "ops": [
                    {"insert": {"formula": self.content.formula}},
                    {"insert": "\n"}
                ]
            }

        # 构建节点
        result = {
            "id": self.id,
            "data": data,
        }

        # 子节点
        if self.children:
            result["children"] = {
                "normal": [child.to_zxm_dict() for child in self.children]
            }

        return result


@dataclass
class MindMapConfig:
    theme: str = "classical2"
    template: str = "right"
    rainbow: bool = True
    rainbow_colors: list[str] = field(default_factory=lambda: [
        "#8CF0E7", "#4AD2FF", "#41A8F3", "#3180CD",
        "#BCE284", "#71D77B", "#78BF6D"
    ])

    def to_dict(self) -> dict:
        result = {
            "theme": self.theme,
            "template": self.template,
        }
        if self.rainbow:
            result["rainbowColors"] = self.rainbow_colors
        return result


# ============ 文本校验 ============

def validate_text(text: str, field_name: str = "text") -> str:
    """校验文本，检测并清理乱码字符"""
    if not text:
        return text

    # 检测常见乱码模式（Unicode 替换字符）
    if '\ufffd' in text:
        print(f"⚠️ 警告: {field_name} 字段包含乱码字符 (U+FFFD)，已清理")
        text = text.replace('\ufffd', '')

    # 检测其他可能的乱码模式
    # 连续的高位 Unicode 私用区字符可能是乱码
    cleaned = []
    prev_was_invalid = False
    for char in text:
        code = ord(char)
        # 跳过私用区字符 (U+E000-U+F8FF) 和无效字符
        if 0xE000 <= code <= 0xF8FF:
            if not prev_was_invalid:
                print(f"⚠️ 警告: {field_name} 字段包含私用区字符，已清理")
            prev_was_invalid = True
            continue
        prev_was_invalid = False
        cleaned.append(char)

    return ''.join(cleaned)


# ============ JSONL 解析器 ============

def parse_jsonl(jsonl_content: str) -> tuple[MindMapConfig, MindNode]:
    """解析 JSONL 格式的 DSL，返回配置和根节点"""
    lines = [line.strip() for line in jsonl_content.strip().split('\n') if line.strip()]

    config = MindMapConfig()
    nodes_data: list[dict] = []

    for line in lines:
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        # 检查是否是配置行
        if obj.get('id') == '_config' or obj.get('id') == -1:
            if 'theme' in obj:
                config.theme = obj['theme']
            if 'template' in obj:
                config.template = obj['template']
            if 'rainbow' in obj:
                config.rainbow = obj['rainbow']
        else:
            nodes_data.append(obj)

    # 构建节点字典
    nodes: dict[int, MindNode] = {}

    for data in nodes_data:
        node_id = data['id']

        # 解析内容（校验文本字段）
        raw_text = data.get('text', '')
        raw_note = data.get('note')

        content = NodeContent(
            text=validate_text(raw_text, f"节点{node_id}.text"),
            note=validate_text(raw_note, f"节点{node_id}.note") if raw_note else None,
            link=data.get('link'),
            priority=data.get('priority'),
            star=data.get('star'),
            progress=data.get('progress'),
            todo=data.get('todo'),
            mark=data.get('mark'),
            expression=data.get('expression'),
            # 图标类型
            flag=data.get('flag'),
            star_icon=data.get('star_icon'),
            avatar=data.get('avatar'),
            month=data.get('month'),
            week=data.get('week'),
            # 公式
            formula=data.get('formula'),
        )

        # 解析样式
        style = NodeStyle(
            background=data.get('bg'),
            font_color=data.get('fc'),
            font_size=data.get('fs'),
            bold=data.get('bold', False),
            italic=data.get('italic', False),
        )

        # 创建节点
        node = MindNode(
            id=gen_id(),
            content=content,
            style=style,
        )

        nodes[node_id] = node

    # 构建树结构
    root = None
    for data in nodes_data:
        node_id = data['id']
        parent_id = data.get('pid')

        node = nodes[node_id]

        if parent_id is None:
            root = node
        elif parent_id in nodes:
            nodes[parent_id].children.append(node)

    if root is None:
        raise ValueError("No root node found (node without pid)")

    return config, root


# ============ ZXM 生成器 ============

class ZXMGenerator:
    """ZXM 文件生成器"""

    def __init__(self, root: MindNode, config: Optional[MindMapConfig] = None):
        self.root = root
        self.config = config or MindMapConfig()
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
        return {
            "type": "mindmap",
            "template": self.config.template,
            "creator": "ai-generator-2.0"
        }

    def _generate_manifest_json(self) -> dict:
        return {}

    def save(self, output_path: str) -> Path:
        """保存为 .zxm 文件"""
        output_path = Path(output_path)
        if not output_path.suffix:
            output_path = output_path.with_suffix('.zxm')

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            content = json.dumps(self._generate_content_json(), ensure_ascii=False)
            zf.writestr('content.json', content)

            metadata = json.dumps(self._generate_metadata_json(), ensure_ascii=False)
            zf.writestr('metadata.json', metadata)

            manifest = json.dumps(self._generate_manifest_json(), ensure_ascii=False)
            zf.writestr('manifest.json', manifest)

            zf.writestr('resources/.keep', '')

        print(f"✅ 已生成: {output_path}")
        return output_path


# ============ 主接口 ============

def generate_zxm_from_jsonl(jsonl_content: str, output_path: str) -> str:
    """从 JSONL 内容生成 .zxm 文件

    Args:
        jsonl_content: JSONL 格式的思维导图 DSL
        output_path: 输出文件路径

    Returns:
        生成的文件路径
    """
    config, root = parse_jsonl(jsonl_content)
    generator = ZXMGenerator(root, config)
    return str(generator.save(output_path))


def generate_zxm_from_file(jsonl_file: str, output_path: str) -> str:
    """从 JSONL 文件生成 .zxm 文件"""
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        content = f.read()
    return generate_zxm_from_jsonl(content, output_path)


# ============ 测试 ============

if __name__ == "__main__":
    # 测试 JSONL 解析和生成
    test_jsonl = '''
{"id":"_config","theme":"ai-classical1","template":"right"}
{"id":0,"text":"Python 学习路线","bg":"#4A90D9","fc":"#FFFFFF","fs":18,"bold":true}
{"id":1,"pid":0,"text":"基础语法","priority":1,"mark":"flag"}
{"id":2,"pid":1,"text":"变量与数据类型","star":5,"progress":9}
{"id":3,"pid":1,"text":"函数","note":"重点：闭包、装饰器","mark":"star"}
{"id":4,"pid":0,"text":"面向对象","priority":2,"mark":"target"}
{"id":5,"pid":4,"text":"类与对象","todo":"done","mark":"check-circle"}
{"id":6,"pid":4,"text":"继承多态","todo":"undone","mark":"clock"}
{"id":7,"pid":0,"text":"数学基础","priority":3,"mark":"lightbulb"}
{"id":8,"pid":7,"text":"时间复杂度","formula":"O(n\\\\log n)"}
{"id":9,"pid":7,"text":"求和公式","formula":"\\\\sum_{i=1}^{n}i=\\\\frac{n(n+1)}{2}"}
'''

    output = generate_zxm_from_jsonl(
        test_jsonl,
        "/tmp/test_zxm.zxm"
    )
    print(f"\n测试文件已生成: {output}")
