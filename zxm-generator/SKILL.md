---
name: zxm-generator
description: This skill should be used when generating ZhiXi mindmap files (.zxm format). It converts AI-friendly JSONL DSL into native ZhiXi files with support for priority, star ratings, progress bars, todos, notes, hyperlinks, marks, and expressions. Trigger phrases include "生成 zxm", "知犀格式", "导出思维导图".
license: MIT
---

# ZXM 思维导图生成器

将 JSONL DSL 转换为知犀思维导图原生文件（.zxm）。

---

## 环境要求

| 依赖 | 要求 | 说明 |
|------|------|------|
| Python | ≥ 3.9 | 使用了类型注解语法 `dict[str, Any]` |
| 知犀应用 | 已安装 | 用于打开 `.zxm` 文件 |
| 外部依赖 | 无 | 仅使用标准库 |

**常见问题**：
- **TypeError: 'type' object is not subscriptable** → Python 版本低于 3.9，请升级
- **文件打开失败** → 确认已安装知犀思维导图应用
- **编码错误** → 确保 JSONL 文件为 UTF-8 编码
- **文本乱码** → 脚本会自动检测并清理乱码字符（U+FFFD），控制台会输出警告

---

## 工作流程

### Step 1: 创建输出目录

在**当前工作区**根据需求名称创建文件夹：

```
./{需求名称}/
├── {需求名称}.jsonl    # DSL 源文件
└── {需求名称}.zxm      # 思维导图文件
```

示例：用户请求 "Python学习路线" → 创建 `./Python学习路线/` 目录

### Step 2: 生成 JSONL 文件

在目录中创建 `.jsonl` 文件，每行一个 JSON 对象：

```jsonl
{"id":"_config","theme":"ai-classical1","template":"right"}
{"id":0,"text":"Python学习路线","bg":"#4A90D9","fc":"#FFFFFF","bold":true}
{"id":1,"pid":0,"text":"分支一","priority":1,"mark":"flag"}
{"id":2,"pid":1,"text":"子节点","star":5}
```

### Step 3: 调用生成器

```python
import sys
sys.path.insert(0, '/path/to/zxm-generator')
from scripts.zxm_generator import generate_zxm_from_file

# 从 jsonl 文件生成 zxm（同目录下）
generate_zxm_from_file("./Python学习路线/Python学习路线.jsonl", "./Python学习路线/Python学习路线.zxm")
```

### Step 4: 打开文件

```bash
open "./Python学习路线/Python学习路线.zxm"
```

**重要**：
- **禁止修改** `scripts/zxm_generator.py`
- **只使用下方列出的有效图标值**，无效值会导致文件无法打开

**最佳实践**：
- **标签适度**：每个节点建议 1-2 个标签，最多不超过 3 个，过多会显得杂乱
- **按需使用**：根据场景选择合适的标签类型，不必每个节点都加标签
- **层级区分**：一级分支可加 priority，重点节点加 mark/star，普通节点保持简洁

---

## JSONL DSL 快速参考

每行一个 JSON 对象。详细规范见 `references/schema.md`。

### 核心字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 节点 ID（0 起始） |
| `pid` | int | 父节点 ID（根节点省略） |
| `text` | string | 节点文本 |

### 样式字段

| 字段 | 说明 | 示例 |
|------|------|------|
| `bg` | 背景色 | `"#4A90D9"` |
| `fc` | 字体颜色 | `"#FFFFFF"` |
| `fs` | 字体大小 | `18` |
| `bold` | 加粗 | `true` |

### 功能字段

| 字段 | 范围/类型 | 说明 |
|------|-----------|------|
| `priority` | 1-20 | 优先级 ①②③... |
| `star` | 1-10 | 星级评分 |
| `progress` | 1-9 | 进度条 |
| `todo` | `"done"` / `"undone"` | 待办 |
| `note` | string | 备注 |
| `link` | URL | 超链接 |
| `formula` | LaTeX | 数学公式 |

### 图标字段（只能使用以下有效值）

**mark** - 标记图标：
`star`, `medal`, `heart`, `heart-broken`, `flag`, `star-orange`, `arrow-up`, `arrow-down`, `arrow-left`, `arrow-right`, `arrow-up-left`, `arrow-up-right`, `arrow-down-left`, `arrow-down-right`, `circle`, `check-circle`, `ban`, `check`, `cross`, `warning`, `question`, `calendar`, `clock`, `bell`, `location`, `mail`, `phone`, `chat`, `clipboard`, `chart`, `target`, `thumbs-up`, `trophy`, `diamond`, `money`, `woman`, `man`, `music`, `mic`, `headset`, `lightbulb`, `pencil`, `gift`, `alert`, `fire`

**expression** - 表情：
`cool`, `smile`, `happy`, `sad`, `tongue`, `cry`, `awkward`

**flag** - 彩色旗帜：
`flag-red`, `flag-orange`, `flag-blue`, `flag-green`, `flag-purple`, `flag-cyan`, `flag-peach`, `flag-lime`, `flag-teal`, `flag-light-blue`

**star_icon** - 彩色星星：
`star-coral`, `star-orange`, `star-blue`, `star-green`, `star-purple`, `star-cyan`, `star-peach`, `star-lime`, `star-turquoise`, `star-light-blue`

**avatar** - 彩色头像：
`avatar-coral`, `avatar-orange`, `avatar-blue`, `avatar-green`, `avatar-purple`, `avatar-cyan`, `avatar-peach`, `avatar-lime`, `avatar-teal`, `avatar-slate-blue`

**month** - 月份（默认中文，加 `-en` 后缀为英文）：
`jan`, `feb`, `mar`, `apr`, `may`, `jun`, `jul`, `aug`, `sep`, `oct`, `nov`, `dec`

**week** - 星期（默认中文，加 `-en` 后缀为英文）：
`mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`

### 全局配置（可选首行）

```jsonl
{"id":"_config","theme":"ai-classical1","template":"right"}
```

---

## 完整示例

```python
import sys
sys.path.insert(0, '/path/to/zxm-generator')
from scripts.zxm_generator import generate_zxm_from_jsonl

jsonl = r'''
{"id":"_config","theme":"ai-classical1","template":"right"}
{"id":0,"text":"Python 学习路线","bg":"#4A90D9","fc":"#FFFFFF","fs":18,"bold":true}
{"id":1,"pid":0,"text":"基础语法","priority":1,"mark":"flag"}
{"id":2,"pid":1,"text":"变量与数据类型","star":5,"progress":9}
{"id":3,"pid":1,"text":"函数","note":"重点：闭包、装饰器","mark":"star"}
{"id":4,"pid":0,"text":"面向对象","priority":2,"mark":"target"}
{"id":5,"pid":4,"text":"类与对象","todo":"done","mark":"check-circle"}
{"id":6,"pid":4,"text":"继承多态","todo":"undone","mark":"clock"}
{"id":7,"pid":0,"text":"进阶主题","priority":3,"mark":"trophy"}
{"id":8,"pid":7,"text":"异步编程","link":"https://docs.python.org/3/library/asyncio.html"}
{"id":9,"pid":7,"text":"元编程","expression":"cool"}
{"id":10,"pid":0,"text":"数学基础","priority":4,"mark":"lightbulb"}
{"id":11,"pid":10,"text":"时间复杂度","formula":"O(n\\log n)"}
{"id":12,"pid":10,"text":"求和公式","formula":"\\sum_{i=1}^{n}i=\\frac{n(n+1)}{2}"}
'''

generate_zxm_from_jsonl(jsonl, "./python-learning.zxm")
```

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| 图标不显示 | 使用了无效的 mark 值 | 只使用上方列出的有效值 |
| 文件打不开 | JSON 格式错误 | 检查引号、逗号、转义 |
| 公式不显示 | `\` 未正确转义 | 使用 `r'''...'''` 或 `\\` |

---

## 参考

- 完整 DSL 规范：`references/schema.md`
- 生成器脚本：`scripts/zxm_generator.py`
