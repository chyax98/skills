---
name: zxm-generator
description: This skill should be used when generating ZhiXi mindmap files (.zxm format). It converts AI-friendly JSONL DSL into native ZhiXi files with support for priority, star ratings, progress bars, todos, notes, hyperlinks, marks, and expressions. Trigger phrases include "生成 zxm", "知犀格式", "导出思维导图".
license: MIT
---

# ZXM 思维导图生成器

将 JSONL DSL 转换为知犀思维导图原生文件（.zxm）。

**适用场景**：知识梳理、学习笔记、项目规划

**触发短语**："生成 zxm"、"知犀格式"、"导出思维导图"

---

## JSONL DSL 快速参考

每行一个 JSON 对象，表示一个节点。详细规范见 `references/schema.md`。

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

| 字段 | 范围 | 说明 |
|------|------|------|
| `priority` | 1-10 | 优先级数字 ①②③... |
| `star` | 1-10 | 星级评分 |
| `progress` | 1-9 | 进度条 |
| `todo` | `"done"` / `"undone"` | 待办状态 |
| `note` | string | 备注 |
| `link` | URL | 超链接 |
| `mark` | 语义名称 | 标记图标（见 schema.md） |
| `expression` | 语义名称 | 表情图标（见 schema.md） |
| `code` | string | 代码内容 |
| `lang` | string | 代码语言（默认 python） |

### 常用 mark 图标

- **状态**: `flag`, `check`, `cross`, `warning`, `question`
- **评价**: `star`, `heart`, `trophy`, `medal`
- **工具**: `target`, `chart`, `clock`, `calendar`

### 全局配置（可选首行）

```jsonl
{"id":"_config","theme":"ai-classical1","template":"right"}
```

---

## 工作流程

### Step 1: 分析需求

确定：主题、分支结构（3-7 个）、是否需要进度/待办

### Step 2: 生成 JSONL

```jsonl
{"id":"_config","theme":"ai-classical1","template":"right"}
{"id":0,"text":"主题","bg":"#4A90D9","fc":"#FFFFFF","bold":true}
{"id":1,"pid":0,"text":"分支一","priority":1,"mark":"flag"}
{"id":2,"pid":1,"text":"子节点","star":5,"progress":7}
{"id":3,"pid":1,"text":"待办项","todo":"undone","mark":"clock"}
{"id":4,"pid":1,"text":"代码示例","code":"print('Hello')","lang":"python"}
```

**原则**：
- 根节点：设置背景色和加粗
- 主分支：用 `priority` 标记顺序
- 重要项：用 `star` 标记
- 进度项：用 `progress` 标记
- 待办项：用 `todo` 标记
- 代码示例：用 `code` + `lang` 添加代码块

### Step 3: 生成 ZXM

```python
from scripts.zxm_generator import generate_zxm_from_jsonl

generate_zxm_from_jsonl(jsonl_content, "./output.zxm")
```

---

## 完整示例

**请求**：生成「Python 学习路线」思维导图

```jsonl
{"id":"_config","theme":"ai-classical1","template":"right"}
{"id":0,"text":"Python 学习路线","bg":"#4A90D9","fc":"#FFFFFF","fs":18,"bold":true}
{"id":1,"pid":0,"text":"基础语法","priority":1,"mark":"flag"}
{"id":2,"pid":1,"text":"变量与数据类型","star":5,"progress":9}
{"id":3,"pid":1,"text":"函数","note":"重点：闭包、装饰器","mark":"star"}
{"id":4,"pid":1,"text":"装饰器示例","code":"@decorator\ndef func():\n    pass","lang":"python"}
{"id":5,"pid":0,"text":"面向对象","priority":2,"mark":"target"}
{"id":6,"pid":5,"text":"类与对象","todo":"done","mark":"check-circle"}
{"id":7,"pid":5,"text":"继承多态","todo":"undone","mark":"clock"}
{"id":8,"pid":0,"text":"进阶主题","priority":3,"mark":"trophy"}
{"id":9,"pid":8,"text":"异步编程","link":"https://docs.python.org/3/library/asyncio.html"}
{"id":10,"pid":8,"text":"元编程","expression":"cool"}
```

---

## 参考

- 完整 DSL 规范：`references/schema.md`
- 生成器脚本：`scripts/zxm_generator.py`
