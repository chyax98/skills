---
name: drawio-generator
description: This skill enables generation of professional DrawIO diagrams (.drawio XML format) directly from text descriptions. Claude Code reads the XML specification and generates diagrams without script dependencies. Supports flowcharts, architecture diagrams, UML, ER diagrams, and network topology with full mxGraph XML control.
license: Apache-2.0
---

# DrawIO 图表生成器

根据用户描述直接生成 DrawIO XML 文件（.drawio）。

---

## 工作流程

1. **分析需求** → 确定图表类型和复杂度
2. **按需加载语法规则** → 读取 references/ 下对应文件
3. **生成 XML** → 按规则生成完整 XML
4. **验证** → 运行验证脚本
5. **保存** → 输出 .drawio 文件

---

## 语法规则索引

| 需求 | 读取文件 |
|------|---------|
| 形状、填充、边框、文字样式 | `references/shapes.md` |
| 连线、箭头、锚点、拐点 | `references/edges.md` |
| 容器、泳道、图层、分组 | `references/advanced.md` |

---

## XML 基础结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Claude Code">
  <diagram name="图表名称" id="唯一ID">
    <mxGraphModel dx="800" dy="600" grid="1" page="1" pageWidth="800" pageHeight="600">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 节点和连线 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 硬性规则

| 规则 | 说明 |
|------|------|
| `as="geometry"` | mxGeometry 必须包含此属性 |
| `id="0"` 和 `id="1"` | 保留 ID，不可用于其他元素 |
| Style 末尾分号 | `style="...;"` 必须以分号结尾 |
| 颜色格式 | 小写十六进制 `#rrggbb` |
| 文本换行 | 使用 `&#xa;` |
| 特殊字符转义 | `<` → `&lt;`、`>` → `&gt;`、`&` → `&amp;` |

---

## 验证

```bash
python scripts/validate_drawio.py <file.drawio>
```
