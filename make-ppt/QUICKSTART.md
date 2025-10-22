# Make-PPT 快速入门

5 分钟快速上手,生成专业 HTML 演示文稿。

## 安装依赖

```bash
npm install -g reveal-md
```

## 基础使用

### 方式 1: 直接生成

只需一句话:

```
使用 make-ppt 生成关于 [主题] 的 PPT
```

例如:
```
使用 make-ppt 生成关于 React Hooks 的 PPT
```

### 方式 2: 从 URL 生成

```
使用 make-ppt 从 https://example.com/article 生成 PPT
```

### 方式 3: 从本地文件生成

```
使用 make-ppt 从 /path/to/notes.md 生成 PPT
```

## 生成流程

1. **资料收集**: 自动搜索或提取内容
2. **内容生成**: 根据时长生成充实的 Markdown
3. **渲染输出**: 转换为可交互的 HTML 幻灯片

## 输出文件

生成的文件位于:
```
/Users/Apple/dev/skills/make-ppt/output/html/index.html
```

双击打开,使用以下快捷键导航:
- `←/→` 或 `空格`: 翻页
- `Esc`: 查看全局视图
- `F`: 全屏模式

## 自定义主题

可选主题:
- `black` (默认): 黑色背景
- `white`: 白色背景
- `league`: 灰色背景,蓝色标题
- `sky`: 蓝色背景
- `beige`: 米色背景

## 内容密度

生成的幻灯片数量基于:
```
时长(分钟) × 0.8 = 幻灯片数量
```

例如 60 分钟演讲 ≈ 48 张幻灯片

## 质量保证

每个核心概念包含:
- **定义**: 清晰的概念说明
- **解释**: 详细的原理阐述
- **示例**: 代码或实际案例

## 常见问题

**Q: 生成的内容太少?**
A: 指定时长,如 "生成 60 分钟的 PPT"

**Q: 如何修改样式?**
A: 编辑生成的 Markdown,重新渲染

**Q: 支持哪些编程语言代码高亮?**
A: 支持所有主流语言 (JavaScript, Python, Go, Rust, Java 等)

## 模板参考

查看 `templates/` 目录:
- `basic.md`: 基础模板
- `technical.md`: 技术演讲模板

## 示例

查看 `examples/` 目录查看完整示例。
