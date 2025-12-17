# ZXM DSL 规范

## 设计理念

**单文件内联装饰**：
- **Markdown** 定义树结构（最自然的方式）
- **`<<{...}>>`** 在行末添加装饰（JSON 格式）
- 无装饰的节点保持纯净

---

## Markdown 结构

### 格式规则

用 `#` 数量表示层级：

```markdown
# 根节点
## 一级分支1
### 二级节点
## 一级分支2
```

**要求**：
- 每行一个节点
- `#` 后必须有空格
- 空行会被忽略（不影响结构）

### 备选：列表风格

用缩进（2空格）表示层级：

```markdown
- 根节点
  - 一级分支1
    - 二级节点
  - 一级分支2
```

---

## 内联装饰语法

在节点行末添加 `<<{JSON}>>` 即可装饰该节点：

```markdown
# 主题名称 <<{"theme":"ai-classical1","bg":"#4A90D9","bold":true}>>
## 一级分支 <<{"priority":1,"mark":"flag"}>>
### 普通节点
### 重点节点 <<{"star":5}>>
```

**规则**：
- `<<` 和 `>>` 之间是标准 JSON
- JSON 必须是单行（不能换行）
- 无装饰的节点不需要添加 `<<>>`

---

## 全局配置

在**根节点**的装饰中设置全局配置：

```markdown
# 主题 <<{"theme":"ai-classical1","template":"right","bg":"#4A90D9"}>>
```

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `theme` | string | `classical2` | 主题风格 |
| `template` | string | `right` | 布局方向 |
| `rainbow` | bool | `true` | 彩虹分支色 |

**主题选项**：`ai-classical1`（推荐）, `classical`, `classical2`, `dark`

**布局选项**：
- `right` - 向右展开（默认，最常用）
- `left` - 向左展开
- `both` - 左右展开
- `tree` - 树状图
- `org` - 组织架构图

---

## 样式字段详解

### bg（背景色）

**作用**：设置节点背景颜色

**格式**：十六进制颜色 `"#RRGGBB"`

**示例**：
```markdown
# 主题 <<{"bg":"#4A90D9"}>>
## 警告 <<{"bg":"#FF6B6B"}>>
```

### fc（字体颜色）

**作用**：设置文字颜色

**格式**：十六进制颜色 `"#RRGGBB"`

**示例**：
```markdown
# 主题 <<{"bg":"#4A90D9","fc":"#FFFFFF"}>>
```

### fs（字体大小）

**作用**：设置文字大小（像素）

**格式**：整数（14-24 常用）

**示例**：
```markdown
# 大标题 <<{"fs":20}>>
```

### bold / italic（粗体/斜体）

**格式**：布尔值

**示例**：
```markdown
# 主题 <<{"bold":true}>>
### 术语 <<{"italic":true}>>
```

---

## 功能字段详解

### priority（优先级）

**作用**：显示数字编号 ①②③④⑤...

**范围**：1-20

**示例**：
```markdown
## 第一步 <<{"priority":1}>>
## 第二步 <<{"priority":2}>>
## 第三步 <<{"priority":3}>>
```

### star（星级评分）

**作用**：显示星星数量 ★★★★★

**范围**：1-10

**示例**：
```markdown
### 核心概念 <<{"star":5}>>
### 了解即可 <<{"star":2}>>
```

### progress（进度条）

**作用**：显示完成进度

**范围**：1-9（1=开始，9=完成）

**示例**：
```markdown
## 需求分析 <<{"progress":9}>>
## 开发中 <<{"progress":5}>>
## 待开始 <<{"progress":1}>>
```

### todo（待办状态）

**作用**：显示复选框

**值**：`"done"` / `"undone"`

**示例**：
```markdown
### 已完成任务 <<{"todo":"done"}>>
### 待办任务 <<{"todo":"undone"}>>
```

### note（备注）

**作用**：添加悬浮备注（支持多行，用 `\n` 换行）

**示例**：
```markdown
### 闭包 <<{"note":"def outer():\n  x = 1\n  def inner(): print(x)\n  return inner"}>>
```

### link（超链接）

**作用**：添加可点击链接

**示例**：
```markdown
### 官方文档 <<{"link":"https://docs.python.org/3/"}>>
```

### formula（公式）

**作用**：显示 LaTeX 数学公式

**注意**：公式会覆盖节点文本

**示例**：
```markdown
### 复杂度 <<{"formula":"O(n\\log n)"}>>
```

---

## 图标字段详解

### mark（标记图标）

**常用值**：

| 值 | 图标 | 场景 |
|----|------|------|
| `flag` | 🚩 | 重要、里程碑 |
| `star` | ⭐ | 收藏、重点 |
| `check` | ✓ | 已确认 |
| `check-circle` | ✅ | 完成 |
| `cross` | ✗ | 失败、禁止 |
| `warning` | ⚠️ | 警告、注意 |
| `question` | ❓ | 疑问 |
| `target` | 🎯 | 目标 |
| `trophy` | 🏆 | 成就 |
| `lightbulb` | 💡 | 想法 |
| `fire` | 🔥 | 紧急 |
| `clock` | ⏰ | 时间相关 |

**完整列表**：
`star`, `medal`, `heart`, `heart-broken`, `flag`, `star-orange`,
`arrow-up`, `arrow-down`, `arrow-left`, `arrow-right`,
`circle`, `check-circle`, `ban`, `check`, `cross`, `warning`, `question`,
`calendar`, `clock`, `bell`, `location`, `mail`, `phone`, `chat`,
`clipboard`, `chart`, `target`, `thumbs-up`, `trophy`, `diamond`, `money`,
`woman`, `man`, `music`, `mic`, `headset`, `lightbulb`, `pencil`, `gift`, `alert`, `fire`

**示例**：
```markdown
## 核心功能 <<{"mark":"flag"}>>
### 待确认 <<{"mark":"question"}>>
### 高风险 <<{"mark":"warning"}>>
```

### expression（表情）

| 值 | 表情 |
|----|------|
| `cool` | 😎 |
| `smile` | 🙂 |
| `happy` | 😃 |
| `sad` | 😢 |
| `tongue` | 😛 |
| `cry` | 😭 |
| `awkward` | 😬 |

### flag（彩色旗帜）

用于分类标记：`flag-red`, `flag-orange`, `flag-blue`, `flag-green`, `flag-purple`, `flag-cyan`

### avatar（头像）

用于负责人标记：`avatar-coral`, `avatar-orange`, `avatar-blue`, `avatar-green`, `avatar-purple`

### month / week

月份：`jan`, `feb`, ... `dec`（中文）；`jan-en`, `feb-en`, ... `dec-en`（英文）

星期：`mon`, `tue`, ... `sun`（中文）；`mon-en`, `tue-en`, ... `sun-en`（英文）

---

## 装饰最佳实践

### 适度原则

- 每个节点 0-2 个装饰字段
- 不是每个节点都需要装饰
- 过多装饰会显得杂乱

### 层级装饰建议

| 层级 | 推荐装饰 |
|------|----------|
| 根节点 | `theme` + `bg` + `fc` + `bold` |
| 一级分支 | `priority` + 可选 `mark` |
| 重点节点 | `mark` 或 `star` |
| 普通节点 | 无装饰或仅 `link`/`note` |

### 完整示例

```markdown
# Python 装饰器 <<{"theme":"ai-classical1","bg":"#4A90D9","fc":"#FFF","bold":true}>>
## 基础概念 <<{"priority":1,"mark":"lightbulb"}>>
### 函数是一等公民
### 闭包 <<{"note":"内函数引用外函数变量"}>>
### 装饰器本质 <<{"star":5}>>
## 语法形式 <<{"priority":2}>>
### @语法糖
### 带参装饰器
## 常用场景 <<{"priority":3,"mark":"target"}>>
### 日志记录
### 性能计时 <<{"link":"https://docs.python.org/3/library/time.html"}>>
### 权限验证 <<{"mark":"warning","note":"注意安全"}>>
## 进阶技巧 <<{"priority":4,"mark":"trophy"}>>
### functools.wraps
### 装饰器堆叠
```

---

## CLI 使用

```bash
# 生成 ZXM
uv run zxm_generator.py input.md -o output.zxm

# 仅验证格式
uv run zxm_generator.py input.md --validate

# 预览节点结构
uv run zxm_generator.py input.md --preview
```
