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
  "flag": "flag-red",         // 彩色旗帜图标
  "star_icon": "star-blue",   // 彩色星星图标
  "avatar": "avatar-green",   // 彩色头像图标
  "month": "jan",             // 月份图标
  "week": "mon",              // 星期图标

  // === 公式 ===
  "formula": "E=mc^2"         // LaTeX 公式
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

### 公式字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `formula` | string | LaTeX 公式（存在此字段时节点显示公式） |

**示例**：
```jsonl
{"id":2,"pid":1,"text":"质能方程","formula":"E=mc^2"}
{"id":3,"pid":1,"text":"求和公式","formula":"\\sum_{i=1}^{n}i=\\frac{n(n+1)}{2}"}
{"id":4,"pid":1,"text":"方程组","formula":"\\begin{cases}x+y=10\\\\x-y=2\\end{cases}"}
{"id":5,"pid":1,"text":"积分","formula":"\\int_{0}^{\\infty}e^{-x^2}dx=\\frac{\\sqrt{\\pi}}{2}"}
```

**注意**：
- 使用标准 LaTeX 语法
- JSON 中反斜杠需要转义（`\\` 表示 `\`）
- `text` 字段用于搜索和备用显示

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
- `lightbulb` 💡 | `pencil` ✏️ | `gift` 🎁 | `alert` ⚠️ | `fire` 🔥

### 表情图标 (expression)

- `cool` 😎 墨镜酷
- `smile` 🙂 微笑
- `happy` 😃 开心
- `sad` 😢 伤心
- `tongue` 😛 吐舌头
- `cry` 😭 大哭
- `awkward` 😬 尴尬/紧张

### 旗帜图标 (flag)

彩色旗帜，用于分类标记：
- `flag-red` 🚩 红色 | `flag-orange` 橙色 | `flag-blue` 蓝色
- `flag-green` 绿色 | `flag-purple` 紫色 | `flag-cyan` 青色
- `flag-peach` 桃红 | `flag-lime` 黄绿 | `flag-teal` 蓝绿 | `flag-light-blue` 浅蓝

### 彩色星星图标 (star_icon)

彩色五角星，用于重要性标记：
- `star-coral` 珊瑚红 | `star-orange` 橙色 | `star-blue` 蓝色
- `star-green` 绿色 | `star-purple` 紫色 | `star-cyan` 青色
- `star-peach` 桃色 | `star-lime` 黄绿 | `star-turquoise` 青绿 | `star-light-blue` 浅蓝

### 头像图标 (avatar)

彩色人物头像，用于人员标记：
- `avatar-coral` 珊瑚红 | `avatar-orange` 橙色 | `avatar-blue` 蓝色
- `avatar-green` 绿色 | `avatar-purple` 紫色 | `avatar-cyan` 青色
- `avatar-peach` 桃色 | `avatar-lime` 黄绿 | `avatar-teal` 蓝绿 | `avatar-slate-blue` 石蓝

### 月份图标 (month)

**中文（默认）**：`jan`, `feb`, `mar`, `apr`, `may`, `jun`, `jul`, `aug`, `sep`, `oct`, `nov`, `dec`

**英文**：`jan-en`, `feb-en`, `mar-en`, `apr-en`, `may-en`, `jun-en`, `jul-en`, `aug-en`, `sep-en`, `oct-en`, `nov-en`, `dec-en`

### 星期图标 (week)

**中文（默认）**：`mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`

**英文**：`mon-en`, `tue-en`, `wed-en`, `thu-en`, `fri-en`, `sat-en`, `sun-en`

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
{"id":5,"pid":0,"text":"面向对象","priority":2,"mark":"target"}
{"id":6,"pid":5,"text":"类与对象","todo":"done","mark":"check-circle"}
{"id":7,"pid":5,"text":"继承与多态","todo":"undone","mark":"clock"}
{"id":8,"pid":5,"text":"魔术方法","todo":"undone","note":"__init__, __str__, __repr__等","mark":"warning"}
{"id":9,"pid":0,"text":"进阶主题","priority":3,"mark":"trophy"}
{"id":10,"pid":9,"text":"异步编程","link":"https://docs.python.org/3/library/asyncio.html","mark":"chart"}
{"id":11,"pid":9,"text":"元编程","star":3,"expression":"cool"}
```

## 字段值映射（内部）

生成器自动处理以下映射，DSL 使用直觉值：

| DSL 字段 | DSL 值 | 知犀内部值 |
|---------|--------|-----------|
| `priority` | 1-20 | 11-30 (+10) |
| `star` | 1-10 | 1-10 (不变) |
| `progress` | 1-9 | 1-9 (不变) |
| `mark` | 语义化名称 | 25-69 (映射表) |
| `expression` | 语义化名称 | 1-8 (映射表) |
| `flag` | 语义化名称 | 1-10 (映射表) |
| `star_icon` | 语义化名称 | 1-10 (映射表) |
| `avatar` | 语义化名称 | 1-10 (映射表) |
| `month` | 语义化名称 | 1-24 (映射表) |
| `week` | 语义化名称 | 1-14 (映射表) |
| `formula` | LaTeX 字符串 | Quill Delta 格式 |
