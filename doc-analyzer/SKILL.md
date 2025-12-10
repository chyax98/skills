---
name: doc-analyzer
description: This skill should be used when parsing PDF or Word documents and deeply understanding their content. It uses Docling for document parsing (extracting text, images, tables) and Claude's multimodal capabilities for image analysis. Suitable for requirement documents, PRD, prototypes, and technical proposals. Trigger phrases include "解析文档", "分析PDF", "读取Word", "文档转文字".
license: Apache-2.0
---

# 文档深度解析器

## 概述

将 PDF/Word 文档转换为结构化内容，结合多模态能力深度理解图文信息。

**支持格式**：
| 格式 | 说明 | 特点 |
|------|------|------|
| PDF | 便携文档格式 | 支持 OCR、复杂表格、图片提取 |
| DOCX | Word 2007+ | 快速解析，无需模型下载 |

**核心能力**：
- Docling 提取文本、图片、表格
- Claude 多模态分析图片内容
- 自动关联图片与文本上下文
- 多场景输出格式支持

**适用场景**：需求文档、PRD、原型图、技术方案、产品规格书

**触发短语**：
- "解析文档"、"分析 PDF"、"读取 Word"、"文档转文字"
- "提取需求"、"分析原型图"、"理解这份文档"

---

## 一、工作流程

### Step 1: 解析文档

使用 Docling 解析文档，提取文本和图片：

```bash
# 优先使用 conda dev 环境
conda run -n dev python /Users/Apple/tmp/pdfparser/doc_parser.py "<文档路径>" -o /tmp/doc_parsed

# 备选：直接运行
python /Users/Apple/tmp/pdfparser/doc_parser.py "<文档路径>" -o /tmp/doc_parsed
```

**支持的输入**：
- PDF 文件：`/path/to/document.pdf`
- Word 文件：`/path/to/document.docx`
- URL：`https://arxiv.org/pdf/2408.09869`

**解析产物**：
| 文件 | 说明 |
|------|------|
| `/tmp/doc_parsed/document.md` | Markdown 格式文本 |
| `/tmp/doc_parsed/images/*.png` | 提取的图片 |
| `/tmp/doc_parsed/result.json` | 解析元数据 |

**注意**：
- PDF 首次运行需下载模型（约 1-2GB），大文档可能需要几分钟
- DOCX 无需下载模型，解析速度快

### Step 2: 读取解析结果

1. 读取 Markdown 文件获取文本结构
2. 列出 images 目录下所有图片
3. 读取 result.json 获取元数据（页数、图片数、表格数）

```bash
cat /tmp/doc_parsed/result.json
ls /tmp/doc_parsed/images/
```

### Step 3: 多模态分析

**分析策略**：

1. **通读 Markdown**：了解文档整体结构和主要章节
2. **逐张分析图片**：使用 Read 工具读取每张图片
3. **图文关联**：将图片内容与对应文本段落关联
4. **综合理解**：生成完整的文档理解

**图片分析模板**（按类型）：

| 图片类型 | 分析角度 |
|---------|---------|
| 架构图/流程图 | 节点关系、数据流向、关键组件 |
| UI 截图/原型图 | 页面布局、交互元素、字段列表 |
| 数据图表 | 图表类型、数据维度、关键数值 |
| 代码截图 | 语言类型、核心逻辑、关键函数 |
| 表格截图 | 表头、行列数据、数据含义 |

### Step 4: 输出结果

根据用户需求选择输出格式。

---

## 二、输出格式

### 2.1 完整还原模式

用户说「还原」「转文字」「完整内容」时使用。

**输出结构**：
```markdown
# 文档标题

## 第一章节
文本内容...

[图片描述: 这是一张系统架构图，展示了三层结构：
- 表现层：Web界面、移动端
- 业务层：API网关、微服务集群
- 数据层：MySQL、Redis、ES
数据流从用户请求到数据库，经过负载均衡分发...]

更多文本内容...

## 第二章节
...
```

**关键原则**：
- 保留原始文档结构
- 图片用 `[图片描述: ...]` 详细描述
- 表格保留 Markdown 表格格式
- 代码块保留语法高亮

### 2.2 需求提取模式

用户说「提取需求」「分析功能」「需求清单」时使用。

**输出结构**：
```markdown
## 文档概述
- 文档类型：PRD / 需求规格 / 原型说明
- 产品名称：xxx
- 版本：v1.0
- 范围：xxx模块

## 功能模块

### 模块1：用户管理
**功能点**：
1. 用户注册
   - 描述：支持手机号/邮箱注册
   - 优先级：高
   - 验收标准：注册成功后自动登录

2. 用户登录
   - 描述：...
   - 优先级：高
   - 验收标准：...

### 模块2：xxx
...

## 界面设计
| 页面名称 | 入口 | 主要功能 | 关键字段 |
|---------|------|---------|---------|
| 登录页 | 首页 | 用户登录 | 手机号、密码、验证码 |
| ... | ... | ... | ... |

## 业务规则
1. 用户名长度限制：4-20字符
2. 密码复杂度要求：...
3. ...

## 待确认问题
1. [ ] 第三方登录是否支持？
2. [ ] 验证码有效期多长？
```

### 2.3 技术分析模式

用户说「技术方案」「架构分析」「技术栈」时使用。

**输出结构**：
```markdown
## 技术概述
- 项目类型：Web应用 / 服务端 / SDK
- 主要语言：Python / Java / ...
- 框架：FastAPI / Spring Boot / ...

## 系统架构
[基于架构图描述整体设计]

### 核心组件
| 组件 | 职责 | 技术选型 |
|------|------|---------|
| API网关 | 请求路由、鉴权 | Kong |
| ... | ... | ... |

### 数据流
1. 用户请求 → API网关
2. 网关鉴权 → 转发至服务
3. 服务处理 → 数据库操作
4. 返回响应

## 关键代码
### 认证模块
```python
# 代码片段
```

## 部署架构
- 环境：Docker / K8s
- 配置：...
```

---

## 三、处理策略

### 3.1 大文档处理

图片超过 20 张时：
1. 优先分析前 10 张（通常是核心内容）
2. 根据 Markdown 上下文判断关键图片
3. 询问用户是否需要分析更多

### 3.2 敏感信息处理

识别并脱敏：
- 用户名、密码、API Key
- 手机号、身份证号
- 内部 URL、IP 地址

### 3.3 解析失败处理

如果 Docling 解析失败：
1. 检查文档路径是否正确
2. PDF：尝试禁用 OCR `--no-ocr`
3. DOCX：检查文件是否损坏
4. 建议用户直接让 Claude 读取文档（原生支持）

---

## 四、完整示例

**用户输入**：
```
解析这个文档：/path/to/需求文档.docx
```

**执行流程**：

```bash
# 1. 解析文档
conda run -n dev python /Users/Apple/tmp/pdfparser/doc_parser.py /path/to/需求文档.docx -o /tmp/doc_parsed

# 2. 查看解析结果
cat /tmp/doc_parsed/result.json
# 输出: {"format": "DOCX", "page_count": "N/A", "image_count": 5, "table_count": 3}
```

```
# 3. 读取 Markdown
Read /tmp/doc_parsed/document.md

# 4. 读取图片（逐张）
Read /tmp/doc_parsed/images/image_0.png
Read /tmp/doc_parsed/images/image_1.png
...

# 5. 综合分析并输出
```

---

## 五、配置说明

### 5.1 输出目录

| 优先级 | 路径 |
|--------|------|
| 1 | 用户指定路径 |
| 2 | `/tmp/doc_parsed`（默认） |

### 5.2 解析参数

| 参数 | 说明 | 默认值 | 适用格式 |
|------|------|--------|----------|
| `-o` | 输出目录 | `./parsed_output` | 全部 |
| `--no-ocr` | 禁用 OCR（加速） | 启用 | PDF |
| `--lang` | OCR 语言 | `ch_sim en` | PDF |
| `--scale` | 图片缩放比例 | 2.0 | PDF |

### 5.3 依赖要求

```bash
# 安装依赖
pip install docling pillow

# 或使用 conda
conda install -n dev docling pillow
```

---

## 六、格式对比

| 特性 | PDF | DOCX |
|------|-----|------|
| 模型下载 | 需要（首次 1-2GB） | 不需要 |
| 解析速度 | 较慢（含 AI 处理） | 快速 |
| OCR 支持 | 支持 | 不需要 |
| 表格识别 | AI 识别 | 原生解析 |
| 图片提取 | 支持 | 支持 |
| 复杂布局 | 支持 | 支持 |

---

## 七、常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| PDF 解析很慢 | 首次下载模型/大文档 | 等待或使用 `--no-ocr` |
| PDF 图片提取失败 | PDF 加密或损坏 | 尝试其他工具转换 |
| DOCX 图片显示异常 | WMF 格式（非 Windows） | 仅 Windows 支持 WMF |
| 中文乱码 | OCR 语言未配置 | 使用 `--lang ch_sim en` |
| 表格识别不准 | 复杂表格 | 结合图片人工校对 |

---

## 参考资源

### 脚本
- 解析脚本：`/Users/Apple/tmp/pdfparser/doc_parser.py`
- 旧版 PDF 脚本：`/Users/Apple/tmp/pdfparser/pdf_parser.py`

### 输出示例
- 完整还原示例：`references/full-restore-example.md`
- 需求提取示例：`references/requirement-extract-example.md`
