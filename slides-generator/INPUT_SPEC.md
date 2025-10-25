# md2ppt 输入规范

**版本**: 1.0.0
**用途**: 约束 AI/人类输入,确保生成有效 Slidev 幻灯片

---

## Markdown 输入要求

### 必须项
- **文件编码**: UTF-8
- **换行符**: LF (`\n`)
- **标题语法**: ATX 风格 (`# 标题`)
- **标题层级**: 1-6 级,递进关系清晰

### 标题规范
```markdown
# H1 仅用于文档总标题
## H2 章节标题
### H3 页面标题
#### H4 页面内子标题
```

**约束**:
- 标题层级不跳跃 (H1 → H3 ❌)
- 同级标题 >1 个才视为章节层级
- 章节层级必须 ≥2 级 (H2/H3/H4...)

### 代码块规范
````markdown
```语言标识
代码内容
```
````

**约束**:
- 必须指定语言 (```js, ```python)
- 无语言标识视为纯文本
- 代码块内反引号需转义

### 内容元素
**允许**:
- 标题 (H1-H6)
- 代码块 (fenced code)
- 列表 (有序/无序)
- 引用块 (`>`)
- 图片 (`![alt](url)`)
- 链接 (`[text](url)`)
- 粗体/斜体

**禁止**:
- HTML 标签 (除 Slidev 指令)
- 内联样式
- 表格跨度语法
- 脚注
- TOC 指令

---

## Frontmatter 规范

### 位置要求
- 必须在文件开头
- 前后用 `---` 包裹
- 与内容间空一行

### 允许字段
```yaml
---
theme: default          # Slidev 主题
background: url         # 背景图/色
class: text-center      # CSS 类
highlighter: shiki      # 代码高亮
lineNumbers: false      # 行号
drawings:
  persist: false
transition: slide-left  # 过渡动画
title: 标题             # 演示标题
---
```

**约束**:
- 仅接受 Slidev 官方字段
- 自定义字段 → 警告
- YAML 语法错误 → 拒绝

---

## 分页逻辑输入要求

### 自动分页条件
1. **章节层级识别**:
   - 扫描 H2-H6
   - 找第一个出现 >1 次的标题级别
   - 该级别 = 章节标题

2. **页面层级识别**:
   - 从章节层级+1 开始扫描
   - 找第一个出现 >0 次的标题级别
   - 该级别 = 页面分隔符

**示例**:
```markdown
# 文档标题
## 章节 1        ← H2 出现 >1 次 → 章节层级
### 页面 1.1    ← H3 为 H2+1 且出现 >0 次 → 页面层级
### 页面 1.2
## 章节 2        ← 新页面 (章节层级)
### 页面 2.1    ← 新页面 (页面层级)
```

**无法自动分页场景**:
- 仅有 H1
- 所有标题仅出现 1 次
- 层级跳跃

---

## CLI 参数输入规范

### 必填参数
```bash
md2ppt <input>          # Markdown 文件路径
```

**约束**:
- 必须是 `.md` 文件
- 文件必须存在
- 路径支持相对/绝对

### 可选参数
```bash
-o, --output <path>     # 输出目录 (默认: ./slides)
-t, --theme <name>      # 主题 (默认: default)
--open                  # 生成后自动打开
-p, --port <number>     # 端口 (默认: 30301, 范围: 1024-65535)
-c, --config <path>     # 配置文件路径
```

**约束**:
- `output`: 目录路径,自动创建
- `theme`: Slidev 主题名
- `port`: 1024-65535 整数
- `config`: 文件存在且可读

---

## 配置文件输入规范

### 支持格式
- `.md2pptrc` (JSON)
- `.md2pptrc.json`
- `.md2pptrc.yaml`
- `.md2pptrc.yml`
- `package.json` 中 `md2ppt` 字段

### 配置结构
```json
{
  "theme": "default",
  "output": "./slides",
  "port": 30301,
  "autoOpen": false,
  "slidev": {
    "highlighter": "shiki",
    "lineNumbers": false
  }
}
```

**约束**:
- 字段类型严格校验
- 未知字段 → 警告
- `slidev` 对象仅接受 Slidev 配置

---

## 错误处理要求

### 必须拒绝
- 空文件
- 无标题文件
- 编码非 UTF-8
- YAML 语法错误
- 端口超范围

### 必须警告
- 标题层级跳跃
- 自定义 frontmatter 字段
- 无法自动分页
- 配置文件未知字段

### 降级处理
- 无 frontmatter → 使用默认配置
- 无章节层级 → 整体作为单页
- 无语言标识代码块 → 视为纯文本

---

## 输出保证

### 生成文件
```
<output>/
├── slides.md           # Slidev 主文件
└── package.json        # Slidev 依赖声明
```

### slides.md 结构
```markdown
---
[frontmatter]
---

# 标题页

---

# 章节/页面 1
内容

---

# 结束页
```

**约束**:
- 每页用 `---` 分隔
- 标题页单独一页
- 结束页可选
- 代码块语言标识保留

---

## 验证清单

输入前检查:
- [ ] 文件编码 UTF-8
- [ ] 标题层级连续
- [ ] 代码块有语言标识
- [ ] Frontmatter YAML 合法
- [ ] CLI 参数类型正确
- [ ] 配置文件格式正确

输出前检查:
- [ ] 分页符 `---` 正确
- [ ] Frontmatter 合并正确
- [ ] 代码块未损坏
- [ ] 特殊字符转义
- [ ] 文件可被 Slidev 解析

---

**最后更新**: 2025-10-26
