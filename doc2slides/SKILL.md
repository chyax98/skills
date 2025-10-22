---
name: doc2slides
description: This skill should be used when the user wants to convert documents (primarily Markdown files) into educational presentation slides using reveal.js. Use this skill for tasks like "convert README.md to slides", "turn my tutorial into a PPT", or "make presentation slides from this document". The skill handles incremental generation to avoid failures, applies strict layout rules to prevent content overflow, and ensures readable typography for teaching purposes.
license: Apache-2.0
---

# Doc2Slides

将文档转换为美观、教学友好的reveal.js幻灯片，专注于可靠性和可读性。

## Overview

Doc2slides is a universal document-to-PPT converter that transforms Markdown files into clean, professional reveal.js presentation slides. The skill emphasizes reliability through incremental generation, strict layout constraints to prevent content overflow, and conservative styling optimized for educational use.

**Core principles:**
- 增量生成：逐段转换避免失败，支持断点续传
- 布局约束：严格防止横向溢出，字体固定在18-20px
- 保守样式：基础底色，非必要不调整，保持简洁专业

## When to Use This Skill

Use this skill when:
- Converting Markdown documents to presentation slides
- Need reliable generation for long documents (50-200 slides)
- Require教学-friendly formatting with proper typography
- Want to avoid layout issues like content overflow or unreadable fonts

**Input formats** (priority order):
1. **Markdown (.md)** - Primary format, processed directly
2. Other formats (PDF, DOCX, URL) - Convert to Markdown first using appropriate tools

## Workflow

This skill follows a structured 7-step workflow for reliable slide generation.

### Step 0: Input Validation and Preprocessing

**Purpose:** Verify input format and prepare for processing.

**Actions:**
1. Check if input is a file path or direct Markdown content
2. Verify file readability (if file path)
3. Detect file format:
   ```python
   if file_ext == '.md':
       # Process directly (90% of cases)
       markdown_content = read_file(file_path)
   elif file_ext in ['.pdf', '.docx', '.txt', '.html']:
       # Notify user: non-Markdown format detected
       # Suggest: "This is a {file_ext} file. Convert to Markdown first using appropriate tools."
       # Wait for user confirmation or converted Markdown
   elif is_url(input):
       # Suggest: "URL detected. Use Tavily Extract or similar to get content first."
   else:
       # Error: unsupported format
   ```

**Output:** Validated Markdown content ready for processing

**Constraints:**
- ❌ **FORBIDDEN**: Attempt to process unsupported formats without conversion
- ✅ **REQUIRED**: Always validate input before proceeding

---

### Step 1: Document Structure Analysis

**Purpose:** Understand document organization and content density.

**Actions:**
1. Parse Markdown structure using heading levels:
   ```python
   structure = {
       'h1_sections': [],  # Chapter-level (##)
       'h2_sections': [],  # Concept-level (###)
       'h3_sections': [],  # Sub-concept level
       'total_words': 0,
       'code_blocks': [],
       'tables': [],
       'images': []
   }
   ```

2. Calculate content density metrics:
   - Total章节数 (H1 count)
   - Total概念数 (H2 count)
   - Average words per section
   - Code block density (code_blocks / total_words)
   - Presence of tables and images

3. Generate structure analysis report:
   ```yaml
   analysis:
     chapters: 8
     sections: 23
     total_words: 12500
     avg_words_per_chapter: 1562
     code_density: 0.008  # 0.8%
     has_tables: true
     has_images: false
   ```

**Output:** Structure analysis report used for segmentation strategy

**Constraints:**
- ❌ **FORBIDDEN**: Skip structure analysis (may cause poor segmentation)
- ✅ **REQUIRED**: Parse all heading levels (H1-H3 minimum)

---

### Step 2: Segmentation Strategy Decision

**Purpose:** Determine optimal chunking strategy using adaptive algorithm.

**Adaptive segmentation logic:**
```python
def determine_strategy(analysis):
    chapters = analysis['chapters']
    sections = analysis['sections']
    avg_words = analysis['avg_words_per_chapter']

    # Decision tree
    if chapters > 5:
        strategy = 'fine_grain'  # by H2 (concept level)
        segments = sections
        reason = f"多章节 ({chapters} > 5)，使用细粒度分段"

    elif chapters <= 5 and avg_words > 2000:
        strategy = 'fine_grain'  # by H2
        segments = sections
        reason = f"章节少但内容密集 ({avg_words}字/章)，使用细粒度"

    elif chapters <= 5 and avg_words <= 2000:
        strategy = 'coarse_grain'  # by H1 (chapter level)
        segments = chapters
        reason = f"简单文档 ({chapters}章 × {avg_words}字)，使用粗粒度"

    else:
        strategy = 'whole'  # no segmentation
        segments = 1
        reason = "极简文档，整体生成"

    # Estimate total slides
    estimated_slides = estimate_slide_count(analysis, strategy)

    return {
        'strategy': strategy,
        'segments': segments,
        'estimated_slides': estimated_slides,
        'reason': reason
    }
```

**Slide count estimation:**
- Title slide: 1 per segment
- Text content: 1 slide per 500 words
- Code blocks: 1 slide per block
- Tables: 1 slide per table
- Images: 1 slide per image

**Output:** Segmentation plan with TodoWrite task list

**Actions after decision:**
1. Display strategy to user:
   ```
   📊 分段策略: {strategy}
   📦 分段数: {segments}
   📄 预估幻灯片: {estimated_slides}张
   💡 原因: {reason}
   ```

2. Create TodoWrite task list:
   ```python
   todos = [
       {"content": f"转换 {seg.title}", "status": "pending", "activeForm": f"转换 {seg.title}"}
       for seg in segments
   ]
   TodoWrite(todos)
   ```

**Constraints:**
- ❌ **FORBIDDEN**: Use hard-coded segmentation without analysis
- ✅ **REQUIRED**: Always explain the chosen strategy to user

---

### Step 3: Incremental Content Conversion

**Purpose:** Convert each segment to PPT format incrementally with state persistence.

**Actions:**

1. **Initialize state management:**
   ```python
   output_file = f"{output_dir}/slides.md"
   state_file = f"{output_dir}/.doc2slides.state.json"

   # Load previous state (for resume capability)
   state = load_state(state_file)
   completed_segments = set(state.get('completed', []))
   ```

2. **Process each segment:**
   ```python
   for i, segment in enumerate(segments):
       # Skip if already completed
       if segment.id in completed_segments:
           print(f"⏭️  跳过: {segment.title}")
           continue

       # Update TodoWrite: mark as in_progress
       update_todo(segment, "in_progress")

       # Convert segment to PPT format
       ppt_content = convert_segment(segment)

       # Immediately append to file (incremental write)
       append_to_file(output_file, ppt_content)

       # Save state
       completed_segments.add(segment.id)
       save_state(state_file, {'completed': list(completed_segments)})

       # Update TodoWrite: mark as completed
       update_todo(segment, "completed")

       print(f"✅ 完成 ({i+1}/{len(segments)}): {segment.title}")
   ```

3. **Segment conversion logic:**
   ```python
   def convert_segment(segment):
       ppt_parts = []

       # Segment title page
       ppt_parts.append(f"""
---

## {segment.title}

{segment.intro if segment.intro else ''}

---
""")

       # Process content blocks
       for block in segment.blocks:
           if block.type == 'text':
               # Text blocks: check length
               if len(block.content) > 800:
                   # Split long text into multiple slides
                   ppt_parts.extend(split_long_text(block.content))
               else:
                   ppt_parts.append(f"\n{block.content}\n---\n")

           elif block.type == 'code':
               # Code blocks: CRITICAL - enforce line width
               code = block.content

               # Check line width (ABSOLUTE CONSTRAINT)
               lines = code.split('\n')
               for i, line in enumerate(lines):
                   if len(line) > 100:
                       # Auto-wrap long lines
                       code = wrap_code_lines(code, max_width=100)
                       break

               # Add code slide
               ppt_parts.append(f"""
---

### 💻 代码示例

```{block.language}
{code}
```

---
""")

           elif block.type == 'table':
               # Tables: check width
               if is_table_too_wide(block.content):
                   # Convert to list format
                   list_content = table_to_list(block.content)
                   ppt_parts.append(f"\n{list_content}\n---\n")
               else:
                   ppt_parts.append(f"\n{block.content}\n---\n")

           elif block.type == 'image':
               # Images: separate slide
               ppt_parts.append(f"""
---

### 📸 {block.title}

![{block.alt}]({block.url})

---
""")

       return '\n'.join(ppt_parts)
   ```

**Key helpers:**

**Code line wrapping** (CRITICAL for preventing overflow):
```python
def wrap_code_lines(code, max_width=100):
    """Wrap code lines exceeding max_width."""
    lines = code.split('\n')
    wrapped = []

    for line in lines:
        if len(line) <= max_width:
            wrapped.append(line)
        else:
            # Smart wrapping: break at logical points
            # Priority: after commas, operators, before keywords
            wrapped.extend(smart_wrap_line(line, max_width))

    return '\n'.join(wrapped)
```

**Long text splitting:**
```python
def split_long_text(text, max_words=150):
    """Split text into multiple slides."""
    paragraphs = text.split('\n\n')
    slides = []
    current_slide = []
    current_words = 0

    for para in paragraphs:
        para_words = len(para.split())
        if current_words + para_words > max_words and current_slide:
            slides.append('\n\n'.join(current_slide) + '\n---\n')
            current_slide = [para]
            current_words = para_words
        else:
            current_slide.append(para)
            current_words += para_words

    if current_slide:
        slides.append('\n\n'.join(current_slide) + '\n---\n')

    return slides
```

**Output:** slides.md file with incrementally added content, state.json for resume

**Constraints:**
- ❌ **FORBIDDEN**: Generate entire document in one go (causes failures)
- ❌ **FORBIDDEN**: Allow code lines > 100 characters (causes horizontal overflow)
- ❌ **FORBIDDEN**: Skip state persistence (loses progress on failure)
- ✅ **REQUIRED**: Write to file after each segment completion
- ✅ **REQUIRED**: Auto-wrap long code lines

---

### Step 4: Layout Rules Application

**Purpose:** Apply frontmatter and ensure style consistency.

**Actions:**

1. **Generate frontmatter** (if not exists):
   ```python
   if not file_has_frontmatter(output_file):
       frontmatter = """---
theme: simple
highlightTheme: github
css:
  - ./doc2slides-style.css
---

# {title}
## {subtitle}

---

## 课程大纲

{table_of_contents}

---

"""
       prepend_to_file(output_file, frontmatter)
   ```

2. **Copy CSS file** to output directory:
   ```python
   css_source = "{skill_dir}/assets/doc2slides-style.css"
   css_dest = f"{output_dir}/doc2slides-style.css"
   copy_file(css_source, css_dest)
   ```

3. **Add summary slide**:
   ```python
   summary = f"""

---

## 总结

**本教程覆盖:**
{bullet_list_of_chapters}

**延伸阅读:**
- 📚 深入相关主题
- 🔧 实践应用

---

**生成信息:**
- 工具: doc2slides
- 时间: {current_time}
- 总页数: {total_slides}

---
"""
   append_to_file(output_file, summary)
   ```

**Output:** Complete slides.md with proper frontmatter and styling

**Constraints:**
- ❌ **FORBIDDEN**: Modify CSS colors or fonts (keep conservative)
- ❌ **FORBIDDEN**: Skip frontmatter (causes styling failures)
- ✅ **REQUIRED**: Always include css reference in frontmatter
- ✅ **REQUIRED**: Copy CSS file to output directory

---

### Step 5: Quality Validation

**Purpose:** Detect layout issues before rendering.

**Validation checklist:**

1. **Code line width scan** (CRITICAL):
   ```python
   def validate_code_width(slides_md):
       issues = []
       code_blocks = extract_code_blocks(slides_md)

       for block in code_blocks:
           lines = block.content.split('\n')
           for i, line in enumerate(lines):
               if len(line) > 100:
                   issues.append({
                       'type': 'code_overflow',
                       'line': i + 1,
                       'length': len(line),
                       'preview': line[:50] + '...'
                   })

       return issues
   ```

2. **Horizontal overflow detection**:
   ```python
   def detect_horizontal_overflow(slides_md):
       issues = []

       # Check for long unbroken strings
       for line in slides_md.split('\n'):
           words = line.split()
           for word in words:
               if len(word) > 50:  # Likely to cause overflow
                   issues.append({
                       'type': 'long_word',
                       'word': word[:30] + '...',
                       'length': len(word)
                   })

       # Check table widths
       tables = extract_tables(slides_md)
       for table in tables:
           if estimate_table_width(table) > 100:
               issues.append({
                   'type': 'wide_table',
                   'columns': table.column_count
               })

       return issues
   ```

3. **Style application verification**:
   ```python
   def verify_style_application(slides_md):
       # Check frontmatter exists
       has_frontmatter = slides_md.startswith('---\n')

       # Check CSS reference
       has_css = 'doc2slides-style.css' in slides_md

       # Check CSS file exists
       css_exists = file_exists('doc2slides-style.css')

       return {
           'frontmatter': has_frontmatter,
           'css_reference': has_css,
           'css_file': css_exists
       }
   ```

**Actions after validation:**
```python
# Run all validations
code_issues = validate_code_width(slides_md)
overflow_issues = detect_horizontal_overflow(slides_md)
style_check = verify_style_application(slides_md)

# Report results
if code_issues or overflow_issues:
    print(f"⚠️  发现 {len(code_issues) + len(overflow_issues)} 个问题:")

    for issue in code_issues:
        print(f"   - 代码行宽超限: 第{issue['line']}行 ({issue['length']}字符)")

    for issue in overflow_issues:
        print(f"   - 可能溢出: {issue['type']}")

    # Auto-fix if possible
    print("🔧 尝试自动修复...")
    fixed_content = auto_fix_issues(slides_md, code_issues, overflow_issues)
    write_file(output_file, fixed_content)
    print("✅ 问题已修复")
else:
    print("✅ 质量检查通过")

if not all(style_check.values()):
    print("⚠️  样式配置不完整:")
    print(f"   - Frontmatter: {'✅' if style_check['frontmatter'] else '❌'}")
    print(f"   - CSS引用: {'✅' if style_check['css_reference'] else '❌'}")
    print(f"   - CSS文件: {'✅' if style_check['css_file'] else '❌'}")
```

**Output:** Validation report + auto-fixed content (if issues found)

**Constraints:**
- ❌ **FORBIDDEN**: Skip validation (may cause rendering issues)
- ❌ **FORBIDDEN**: Ignore code width issues (causes horizontal scroll)
- ✅ **REQUIRED**: Auto-fix code width issues when detected
- ✅ **REQUIRED**: Report all issues to user

---

### Step 6: Rendering and Final Output

**Purpose:** Generate HTML slides and provide usage instructions.

**Actions:**

1. **Render using reveal-md**:
   ```bash
   cd {output_dir}
   reveal-md slides.md --css doc2slides-style.css --static slides-output
   ```

   Or for live preview:
   ```bash
   reveal-md slides.md --css doc2slides-style.css
   ```

2. **Verify rendering**:
   ```python
   if rendering_successful:
       print("✅ 渲染完成")
       print(f"📁 输出目录: {output_dir}")
       print(f"📄 源文件: slides.md")
       print(f"🌐 HTML: slides-output/index.html")
   else:
       print("❌ 渲染失败，请检查reveal-md安装")
       print("💡 安装命令: npm install -g reveal-md")
   ```

3. **Clean up temporary files**:
   ```python
   # Remove state file (no longer needed)
   if file_exists(state_file):
       delete_file(state_file)
   ```

4. **Generate usage instructions**:
   ```markdown
   ## 使用方式

   **方式1: 静态HTML (推荐)**
   直接打开: {output_dir}/slides-output/index.html

   **方式2: 本地预览**
   cd {output_dir}
   reveal-md slides.md --css doc2slides-style.css

   **方式3: 导出PDF**
   reveal-md slides.md --css doc2slides-style.css --print slides.pdf

   ## 键盘快捷键
   - 空格/→: 下一页
   - ←: 上一页
   - Esc: 概览模式
   - F: 全屏
   ```

**Output:** Complete slides package with usage instructions

**Constraints:**
- ❌ **FORBIDDEN**: Skip cleanup (leaves temp files)
- ✅ **REQUIRED**: Provide clear usage instructions
- ✅ **REQUIRED**: Verify reveal-md availability

---

## Layout Constraints (CRITICAL)

These constraints are **ABSOLUTE** and must never be violated:

### ❌ FORBIDDEN (Causes failures)

1. **Horizontal overflow**
   - Code lines > 100 characters
   - Tables wider than container
   - Long unbroken strings
   - **Consequence:** Content invisible, horizontal scrollbar

2. **Font chaos**
   - Modifying base font size (must stay 20px)
   - Using custom fonts beyond system stack
   - Random font-weight changes
   - **Consequence:** Unreadable, inconsistent typography

3. **Style complexity**
   - Multiple background colors
   - Gradients and animations
   - Shadow effects (except code blocks)
   - **Consequence:** Visual clutter, distraction

4. **Batch generation**
   - Generating entire document without incremental writes
   - **Consequence:** Token limits, lost progress on failure

### ✅ REQUIRED (Must implement)

1. **Line width enforcement**
   - Auto-wrap code lines at 100 characters
   - Break long words in text content
   - Convert wide tables to lists

2. **Fixed typography**
   - Base font: 20px (never change)
   - Code font: 16px (0.8em)
   - Line height: 1.6 (never change)

3. **Incremental generation**
   - Write after each segment
   - Save state for resume
   - Update TodoWrite in real-time

4. **Conservative styling**
   - Use provided CSS without modification
   - White background + dark gray text only
   - Single accent color (#42b983)

## MCP Tool Usage Strategy

Use MCP tools sparingly based on complexity:

### Default: Local Processing (80%)
For standard Markdown with normal structure:
- Use built-in parsing and conversion
- Apply local algorithms for segmentation
- No external tools needed

### SearXNG (15%)
When encountering unfamiliar terms or concepts:
```python
if need_clarification(term):
    result = mcp__searxng__searxng_web_search(
        query=f"{term} 教程 2025",
        language="zh"
    )
```

### Context7 (3%)
Only for major frameworks mentioned in document:
```python
MAJOR_LIBRARIES = [
    'facebook/react',
    'vuejs/core',
    'microsoft/TypeScript',
    'tiangolo/fastapi'
]

if library_name in document and library_name in MAJOR_LIBRARIES:
    docs = mcp__context7__get_library_docs(
        context7CompatibleLibraryID=f"/{library_name}"
    )
```

### Sequential Thinking (2%)
Only when structure is highly irregular:
```python
def is_complex(analysis):
    return (
        analysis['irregular_headings'] or
        analysis['code_density'] > 0.006 or
        analysis['avg_section_length'] > 3000
    )

if is_complex(analysis):
    strategy = mcp__sequential-thinking__sequentialthinking(
        thought="分析这个复杂文档的最佳分段策略..."
    )
```

## Collaboration with make-ppt

This skill is designed to work standalone or as part of a pipeline with make-ppt:

**Standalone usage:**
```
User: "Convert my README.md to slides"
→ doc2slides processes README.md directly
```

**Pipeline usage:**
```
User: "Generate React tutorial slides"
→ make-ppt: Research + generate react-tutorial.md
→ make-ppt asks: "Convert to slides?"
→ User: "Yes"
→ doc2slides: Convert react-tutorial.md to slides
```

**Division of responsibilities:**
- **make-ppt**: Content generation, research, quality
- **doc2slides**: Layout, styling, reliable conversion

## Resources

### assets/

**doc2slides-style.css** - Conservative professional styling:
- Base colors: white background + dark gray text
- Fixed typography: 20px base, 16px code
- Layout constraints: no horizontal overflow
- Non-essential styling avoided

This CSS file must be:
- Copied to output directory during Step 4
- Referenced in frontmatter
- Never modified (保守原则)

**Note:** No scripts/ or references/ needed for this skill. All logic is procedural and described in the workflow above.

---

## Success Criteria

A successful conversion must meet all of these:

✅ No horizontal scrollbar (code lines ≤ 100 chars)
✅ Base font is 20px, code font is 16px
✅ White background with dark gray text only
✅ All segments processed without errors
✅ TodoWrite shows all tasks completed
✅ CSS file present and referenced
✅ slides.md renders correctly in reveal-md

If any criterion fails, re-run the failed step with corrections.
