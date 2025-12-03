---
name: slides-generator
description: This skill should be used when generating Slidev presentations from any input (text, files, URLs, or topics). It intelligently converts content into presentation-ready Markdown slides with proper formatting, supports multiple scenarios (teaching, research, algorithms, project analysis), and automatically validates against Slidev specifications. Trigger phrases include "生成幻灯片", "制作PPT", "根据XXX做PPT", "XXX的教程", "讲解XXX".
license: Apache-2.0
---

# Slides Generator

将任意输入智能转换为 Slidev 幻灯片的通用生成器。

## 设计理念

```
用户需求 → Slidev Markdown → 原生 Slidev 渲染
```

**职责分离**:
- 生成符合 Slidev 规范的 Markdown
- 使用原生 Slidev 工具渲染

## 多角色协作框架 (DEPTH: D)

Generate high-quality slides through expert role collaboration:

**Content Architect**:
- Analyze content structure and narrative flow
- Design slide organization and progression
- Balance information density across slides
- Ensure logical coherence

**Domain Researcher**:
- Gather comprehensive topic information
- Use SearXNG MCP for web research when needed
- Extract key concepts, examples, and code samples
- Identify knowledge gaps

**Visual Designer**:
- Select appropriate Slidev layouts for content types
- Balance text, code, and visual elements
- Ensure readability and visual hierarchy
- Optimize for presentation context

**Quality Reviewer**:
- Validate against Slidev specifications
- Check content completeness and accuracy
- Run validation scripts
- Verify code examples and technical accuracy

## 工作流程

### 步骤 0: 背景信息收集 (DEPTH: P)

Before generating slides, collect essential context:

**Required Information**:
1. **Content Domain**: Identify the field (Technology/Business/Science/Arts)
2. **Target Audience**: Determine viewer level (Beginner/Intermediate/Expert)
3. **Presentation Purpose**: Clarify the goal
   - Teaching: Introduce new concepts
   - Research: Present findings or analysis
   - Algorithm: Explain problem-solving approach
   - Project: Demonstrate architecture or implementation
4. **Depth Requirement**: Overview/Detailed/Expert-level
5. **Time Constraint**: Presentation duration (affects slide count)
6. **Special Requirements**: Code examples, diagrams, specific topics to emphasize

**Information Gathering**:
- When context is provided: Use directly
- When context is unclear: Ask clarifying questions
- When researching topic: Use SearXNG MCP to gather domain knowledge

### 步骤 1: 素材获取

**Domain Researcher Role**:

根据输入类型选择工具获取素材:

**Research Process**:
1. Identify core concepts and key information
2. Extract code examples and technical details
3. Gather visual aids or diagrams if needed
4. Search additional context if needed (SearXNG MCP)

**详细流程**: @references/workflows/material-collection.md

### 步骤 2: 场景识别

**Content Architect Role**:

识别内容类型并加载对应模板。

| 场景 | 触发特征 | 模板 |
|------|---------|------|
| 教学 | 库名/框架 + "教程"/"学习" | @templates/teaching.md |
| 调研 | "调研"/"分析"/"对比" | @templates/research.md |
| 算法 | "LeetCode"/"算法题" | @templates/algorithm.md |
| 项目 | "源码"/"架构"/"解析" | @templates/project-analysis.md |

### 步骤 3: 内容生成 (DEPTH: T)

**Content Architect & Visual Designer Roles**:

按模板策略生成 Slidev Markdown:

**Task Breakdown**:
1. **Frontmatter Configuration**: Set theme, title, fonts, layout defaults
2. **Opening Slides**: Title, agenda, learning objectives
3. **Content Slides**: Core concepts, explanations, examples
4. **Code Slides**: Syntax highlighting, line highlighting, code annotations
5. **Visual Slides**: Diagrams, charts, architecture illustrations
6. **Closing Slides**: Summary, Q&A, references

**Content Density Management**:
- Balance information per slide (3-7 key points)
- Use progressive disclosure for complex topics
- Split dense content across multiple slides
- Leverage Slidev click animations for step-by-step reveals

**生成策略**: @references/workflows/content-generation.md

**必须符合**: @references/specs/slidev-core-rules.md

### 步骤 4: 规范检查 (DEPTH: E)

**Quality Reviewer Role**:

验证生成的 Markdown 是否符合 Slidev 规范:

**Success Criteria**:
1. **Technical Compliance**:
   - UTF-8 encoding
   - Proper frontmatter format
   - Correct slide separator usage (---)
   - Valid code block syntax
   - Proper Mermaid diagram configuration

2. **Content Quality**:
   - Each slide has clear purpose
   - Information density appropriate (not overcrowded)
   - Code examples are correct and runnable
   - Terminology accurate for target audience
   - Logical flow between slides

3. **Visual Quality**:
   - Appropriate layout selection
   - Readable font sizes
   - Proper use of emphasis (bold, italic, color)
   - Balanced text and visual elements
   - No content overflow

4. **Presentation Effectiveness**:
   - Clear narrative structure
   - Smooth transitions between topics
   - Effective use of animations
   - Engaging opening and strong closing

**检查清单**: @references/specs/validation-checklist.md

### 步骤 5: 输出保存

**路径优先级**:
1. 用户指定路径 → 使用用户路径
2. 未指定 → `./slides/`（项目根目录下，自动创建）

**文件命名**: `{主题}-{场景}-{日期}.md`
- 示例: `fastapi-teaching-20251202.md`

**注意**: 输出基于当前工作目录 `$PWD`，非 skill 安装目录

### 步骤 6: 规范验证

使用验证脚本检查生成的幻灯片是否符合 Slidev 规范。

**验证命令**: `./scripts/validate-slides.sh ./slides/文件名.md`

**验证项目**:
- 文件格式 (UTF-8 编码、换行符)
- Frontmatter 配置 (theme, title, fonts)
- 分页规则 (---前后空行)
- 代码块规范 (语言标识)
- Mermaid 图表 (scale 参数)
- 内容溢出防止 (滚动/缩放)
- 内容质量 (空白页、标题)

**处理结果**:
- ❌ 失败: 根据提示修复后重新验证
- ⚠️ 警告: 记录改进建议,可选择性修复
- ✅ 通过: 进入下一步

### 步骤 7: 自动打开预览

生成完成后自动使用 Slidev 打开预览。

**命令**: `cd ./slides && slidev 文件名.md --open`

**说明**:
- `--open` 参数会自动在默认浏览器中打开幻灯片
- Slidev 会启动开发服务器 (通常在 http://localhost:3030)
- 支持热更新，修改文件会实时刷新

**CLI 参考**: @slidev-docs/builtin/cli.md

### 步骤 8: 自我评估 (DEPTH: H)

**Quality Reviewer Role**:

Before finalizing the slides, perform self-evaluation to ensure quality:

**Content Structure Assessment**:
- Does the narrative flow logically from introduction to conclusion?
- Are learning objectives clearly stated and met?
- Is information density balanced across slides?
- Are transitions between topics smooth and natural?
- Does each slide have a clear, singular focus?

**Technical Accuracy Check**:
- Are all code examples correct and runnable?
- Are technical terms used accurately?
- Are diagrams and visualizations accurate?
- Are references and sources properly cited?

**Visual Design Evaluation**:
- Is text readable at presentation size?
- Are layouts appropriate for content types?
- Is color usage consistent and accessible?
- Are animations purposeful, not distracting?
- Is the overall design professional and polished?

**Audience Appropriateness**:
- Is terminology suitable for target audience level?
- Are explanations sufficiently detailed for beginners/experts?
- Are examples relevant and relatable?
- Is pacing appropriate for presentation duration?

**Slidev Compliance Check**:
- Frontmatter properly configured?
- Slide separators (---) correctly placed?
- Code blocks with language identifiers?
- Mermaid diagrams with proper scale settings?
- No content overflow issues?

**Common Issues Avoidance**:
- No slides overcrowded with text?
- No missing code language identifiers?
- No improperly formatted Mermaid diagrams?
- No inconsistent layout usage?
- No unclear or ambiguous explanations?

**Action on Assessment**:
- If critical issues found: Return to relevant step and revise
- If warnings: Consider improvements before finalizing
- If passed: Slides ready for presentation

## Slidev 规范

### 快速参考

**核心语法**: @references/guides/slidev-quickref.md

**配置参数**: @references/guides/slidev-config.md

**核心规则**: @references/specs/slidev-core-rules.md

### 完整文档

**官方文档**: @slidev-docs/

**文档索引**: @references/guides/slidev-index.md

**快速查找**:
- 语法: @slidev-docs/guide/syntax.md
- 布局: @slidev-docs/builtin/layouts.md
- 动画: @slidev-docs/guide/animations.md
- 代码: @slidev-docs/features/line-highlighting.md

## 场景模板

- 教学: @templates/teaching.md
- 调研: @templates/research.md
- 算法: @templates/algorithm.md
- 项目: @templates/project-analysis.md

## 质量标准

生成的幻灯片必须满足:

1. **规范性**: 符合 @references/specs/slidev-core-rules.md
2. **完整性**: 内容完整，逻辑清晰
3. **实用性**: 代码可运行，概念准确
4. **美观性**: 布局合理，视觉清晰

**详细标准**: @references/workflows/content-generation.md

## 资源引用

### 工作流程

- 素材获取: @references/workflows/material-collection.md
- 内容生成: @references/workflows/content-generation.md

### 规范文档

- 核心规则: @references/specs/slidev-core-rules.md
- 检查清单: @references/specs/validation-checklist.md

### 快速参考

- Slidev 语法: @references/guides/slidev-quickref.md
- 配置参数: @references/guides/slidev-config.md
- 文档索引: @references/guides/slidev-index.md

### 官方文档

- 完整文档: @slidev-docs/
- 在线文档: https://cn.sli.dev

---

**版本**: 1.0.0
**更新**: 2025-10-26
