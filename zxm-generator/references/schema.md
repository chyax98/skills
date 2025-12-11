# ZXM JSONL DSL Schema

## 概述

使用 JSONL（每行一个 JSON）格式定义思维导图节点。DSL 设计原则：
- **直觉友好**：字段值符合直觉（如 priority 1-10，而非内部值 11-20）
- **语义化**：图标使用名称（如 `"flag"`）而非数字
- **脚本转换**：生成器自动处理内部格式映射

## 节点 Schema

```jsonc
{
  // === 必填字段 ===
  "id": 0,                    // 节点 ID（整数，从 0 开始）
  "text": "节点文本",          // 节点显示文本

  // === 结构字段 ===
  "pid": 0,                   // 父节点 ID（根节点省略此字段）

  // === 样式字段 ===
  "bg": "#4A90D9",            // 背景色（十六进制）
  "fc": "#FFFFFF",            // 字体颜色（十六进制）
  "fs": 18,                   // 字体大小（像素）
  "bold": true,               // 是否加粗
  "italic": false,            // 是否斜体

  // === 功能字段 ===
  "priority": 1,              // 优先级数字图标（1-10）→ 显示 ①②③...
  "star": 5,                  // 星级评分（1-10）
  "progress": 7,              // 进度条（1-9）
  "todo": "done",             // 待办状态："done" | "undone"
  "note": "备注内容",          // 备注
  "link": "https://...",      // 超链接 URL

  // === 图标字段 ===
  "mark": "flag",             // 标记图标（语义化名称）
  "expression": "happy",      // 表情图标（语义化名称）

  // === 代码块 ===
  "code": "print('hello')",   // 代码内容
  "lang": "python"            // 语言（默认 python）
}
```

## 字段详细说明

### 必填字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | int | 节点唯一标识，从 0 开始递增 |
| `text` | string | 节点显示文本 |

### 结构字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `pid` | int | 父节点 ID，**根节点省略此字段** |

### 样式字段

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `bg` | string | - | 背景色，如 `"#4A90D9"` |
| `fc` | string | - | 字体颜色，如 `"#FFFFFF"` |
| `fs` | int | - | 字体大小（像素） |
| `bold` | bool | false | 是否加粗 |
| `italic` | bool | false | 是否斜体 |

### 功能字段

| 字段 | 类型 | 范围 | 说明 |
|------|------|------|------|
| `priority` | int | 1-10 | 优先级数字图标，显示 ①②③④⑤⑥⑦⑧⑨⑩ |
| `star` | int | 1-10 | 星级评分 |
| `progress` | int | 1-9 | 进度条（1=开始, 9=完成） |
| `todo` | string | `"done"` / `"undone"` | 待办复选框 |
| `note` | string | - | 备注内容 |
| `link` | string | - | 超链接 URL |

### 代码块字段

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `code` | string | - | 代码内容（存在此字段时节点显示代码块） |
| `lang` | string | `"python"` | 编程语言 |

支持的语言：`python`, `javascript`, `typescript`, `java`, `c`, `cpp`, `go`, `rust`, `sql`, `bash`, `json`, `yaml`, `markdown`, `html`, `css` 等

**示例**：
```jsonl
{"id":5,"pid":1,"text":"快速排序","code":"def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[0]\n    return quicksort([x for x in arr[1:] if x < pivot]) + [pivot] + quicksort([x for x in arr[1:] if x >= pivot])","lang":"python"}
```

### 标记图标 (mark)

使用语义化名称，生成器自动转换为知犀内部值。

**收藏/评价类**：
- `star` ⭐ 黄色星星
- `medal` 🏅 奖章
- `heart` ❤️ 红心
- `heart-broken` 💔 破碎的心
- `flag` 🚩 红旗
- `star-orange` ⭐ 橙色星星

**状态类**：
- `circle` ○ 空心圆
- `check-circle` ✅ 绿色对勾圆
- `ban` 🚫 禁止
- `check` ✓ 绿色对勾
- `cross` ✗ 红色叉
- `warning` ⚠️ 红色感叹号
- `question` ❓ 橙色问号

**箭头方向类**：
- `arrow-up` ↑ | `arrow-down` ↓ | `arrow-left` ← | `arrow-right` →
- `arrow-up-left` ↖ | `arrow-up-right` ↗ | `arrow-down-left` ↙ | `arrow-down-right` ↘

**时间/提醒类**：
- `calendar` 📅 日历
- `clock` ⏰ 时钟
- `bell` 🔔 铃铛

**通讯/工具类**：
- `location` 📍 | `mail` ✉️ | `phone` 📞 | `chat` 💬
- `clipboard` 📋 | `chart` 📊 | `target` 🎯 | `thumbs-up` 👍

**其他**：
- `trophy` 🏆 | `diamond` 💎 | `money` 💰
- `woman` 👩 | `man` 👨 | `music` 🎵 | `mic` 🎤 | `headset` 🎧

### 表情图标 (expression)

- `cool` 😎 墨镜酷
- `smile` 🙂 微笑
- `happy` 😃 开心
- `sad` 😢 伤心
- `tongue` 😛 吐舌头
- `cry` 😭 大哭

## 全局配置

第一行可以是全局配置（id 为 `"_config"`）：

```jsonl
{"id":"_config","theme":"ai-classical1","template":"right","rainbow":true}
```

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `theme` | string | `"classical2"` | 主题：`ai-classical1`, `classical`, `classical2`, `dark` |
| `template` | string | `"right"` | 布局：`default`, `right`, `left`, `both`, `tree`, `org` |
| `rainbow` | bool | true | 是否启用彩虹分支色 |

## 完整示例

```jsonl
{"id":"_config","theme":"ai-classical1","template":"right"}
{"id":0,"text":"Python 学习路线","bg":"#4A90D9","fc":"#FFFFFF","fs":18,"bold":true}
{"id":1,"pid":0,"text":"基础语法","priority":1,"mark":"flag"}
{"id":2,"pid":1,"text":"变量与数据类型","star":5,"progress":9,"expression":"happy"}
{"id":3,"pid":1,"text":"控制流程","star":4,"progress":7,"mark":"check"}
{"id":4,"pid":1,"text":"函数","star":5,"progress":5,"note":"重点掌握闭包和装饰器","mark":"star"}
{"id":5,"pid":1,"text":"装饰器示例","code":"def timer(func):\n    def wrapper(*args):\n        import time\n        start = time.time()\n        result = func(*args)\n        print(f'{func.__name__} took {time.time()-start:.2f}s')\n        return result\n    return wrapper","lang":"python"}
{"id":6,"pid":0,"text":"面向对象","priority":2,"mark":"target"}
{"id":7,"pid":6,"text":"类与对象","todo":"done","mark":"check-circle"}
{"id":8,"pid":6,"text":"继承与多态","todo":"undone","mark":"clock"}
{"id":9,"pid":6,"text":"魔术方法","todo":"undone","note":"__init__, __str__, __repr__等","mark":"warning"}
{"id":10,"pid":0,"text":"进阶主题","priority":3,"mark":"trophy"}
{"id":11,"pid":10,"text":"异步编程","link":"https://docs.python.org/3/library/asyncio.html","mark":"chart"}
{"id":12,"pid":10,"text":"async 示例","code":"import asyncio\n\nasync def fetch_data():\n    await asyncio.sleep(1)\n    return 'data'\n\nasyncio.run(fetch_data())","lang":"python"}
{"id":13,"pid":10,"text":"元编程","star":3,"expression":"cool"}
```

## 字段值映射（内部）

生成器自动处理以下映射，DSL 使用直觉值：

| DSL 字段 | DSL 值 | 知犀内部值 |
|---------|--------|-----------|
| `priority` | 1-10 | 11-20 (+10) |
| `star` | 1-10 | 1-10 (不变) |
| `progress` | 1-9 | 1-9 (不变) |
| `mark` | 语义化名称 | 25-64 (映射表) |
| `expression` | 语义化名称 | 1-7 (映射表) |
