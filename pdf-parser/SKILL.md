---
name: pdf-parser
description: 解析需求文档 PDF（PRD、原型、功能说明）。使用 Docling 提取结构化 Markdown + 图片，Agent 通过多模态能力描述图片内容（原型图、流程图、表格截图等），输出完整的文档理解。触发词：解析需求文档、分析 PRD、理解这个 PDF。
---

# 需求文档解析器

将需求文档 PDF 解析为 Markdown + 图片，配合多模态能力生成完整理解。

需求文档通常包含：文本描述、原型图、流程图、表格、截图等图文混排内容。

## 工作流程

```
PDF 文件 → Docling 解析 → Markdown + 图片 → 多模态读取图片 → 整合输出
```

### Step 1: 执行解析

```bash
uv run ~/.claude/skills/pdf-parser/scripts/parse_pdf.py /path/to/需求文档.pdf -o ./output

# 非扫描件可加速（禁用 OCR）
uv run ~/.claude/skills/pdf-parser/scripts/parse_pdf.py /path/to/需求文档.pdf -o ./output --no-ocr
```

输出 JSON：
```json
{
  "markdown_path": "output/document.md",
  "image_paths": ["output/images/image_0.png", ...],
  "page_count": 10,
  "table_count": 3
}
```

### Step 2: 读取 Markdown

读取 `document.md`，理解：
- 文档结构和章节
- 文本内容（已 NFKC 规范化，无乱码）
- 表格数据（Markdown 格式）
- 图片引用（`![](image_xxx.png)` 格式）

### Step 3: 多模态图片描述

Markdown 中已包含图片引用，对每张图片使用 Read 工具读取，生成描述：

```markdown
### 图片 N: [标题]

**类型**: [原型图/流程图/表格/截图/图表]

**内容**: [2-3句描述]

**关键元素**:
- [元素]: [说明]

**上下文**: [与文档的关联]
```

#### 图片类型描述要点

| 类型 | 重点描述 |
|------|----------|
| 原型图 | 页面名称、功能区域、表单字段、按钮、交互流程 |
| 流程图 | 节点、分支条件、流向、起止点 |
| 表格截图 | 列名、关键数据、统计汇总 |
| 架构图 | 组件、连接关系、数据流向 |

### Step 4: 整合输出

根据需求输出：
- **文档概述**: 产品/功能总结
- **功能列表**: 模块、功能点、验收标准
- **界面设计**: 原型图描述整理
- **待确认问题**: 文档中的歧义或缺失

## 输出结构

```
output/
├── document.md      # Markdown（含图片引用 ![](xxx.png)）
├── result.json      # 元数据
└── *.png            # 图片文件（与 md 同目录）
```

## 检查清单

- [ ] Markdown 结构完整
- [ ] 图片全部提取
- [ ] 每张图片有描述
- [ ] 描述与上下文关联
- [ ] 输出符合用户需求

## 故障排除

| 问题 | 解决 |
|------|------|
| 脚本路径错误 | 使用 `~/.claude/skills/pdf-parser/scripts/parse_pdf.py` |
| 依赖安装失败 | 检查网络，uv 自动安装 docling/docling-core |
| 图片为空 | PDF 无嵌入图片，正常现象 |
| 解析慢 | 扫描件 OCR 耗时，非扫描件用 `--no-ocr` |
| 表格识别错误 | 复杂表格结合图片多模态补充识别 |
