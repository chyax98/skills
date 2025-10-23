---
name: input2slides
description: This skill should be used when the user wants to convert any input (URL/topic/markdown file) into beautifully formatted Marp presentation slides. Handles content extraction, layout optimization, and automatic slide generation from diverse input sources.
license: Apache-2.0
---

# input2slides

Convert any input source into polished, production-ready Marp presentation slides.

## Purpose

This skill transforms diverse input formats (URLs, topics, markdown files) into well-structured Marp presentations. It handles content extraction, intelligent pagination, layout optimization, and ensures all output is properly formatted for successful rendering as HTML or PPTX.

## When to Use This Skill

Trigger this skill when the user requests:
- Converting URLs to presentation slides
- Creating presentations from topics or concepts
- Transforming markdown documents into slide decks
- Generating educational or tutorial presentations
- Any request containing keywords: "slides", "PPT", "presentation", "幻灯片", combined with input sources

## Core Workflow

### 1. Input Identification

Automatically detect input type based on pattern matching:

```python
if input.startswith(('http://', 'https://')):
    input_type = 'url'
elif input.endswith('.md'):
    input_type = 'markdown_file'
else:
    input_type = 'topic'
```

### 2. Content Acquisition

**For URLs:**
- Use `mcp__tavily-mcp__tavily-extract` with `format="markdown"` for clean content extraction
- Fallback to `mcp__searxng__web_url_read` if Tavily extraction fails
- Preserve code blocks, headings, and structure

**For Topics:**
- Use `mcp__searxng__searxng_web_search` with appropriate language settings
- Extract relevant content from top 3-5 search results
- Optionally use `mcp__context7__get_library_docs` for official documentation when topic matches major libraries

**For Markdown Files:**
- Use `Read` tool to load file contents directly
- Validate markdown structure and extract metadata

### 3. Content Analysis

Before generation, analyze the content structure:

```python
analysis = {
    'h1_count': count_of_h1_headers,
    'h2_count': count_of_h2_headers,
    'code_blocks': count_of_code_blocks,
    'total_lines': line_count,
    'estimated_slides': h1_count + h2_count + code_blocks + (paragraphs // 3)
}
```

**Segmentation Decision:**
- If `estimated_slides > 30`: Use segmented generation (防止输出截断)
- If `estimated_slides ≤ 30`: Generate in single pass

### 4. Marp Markdown Generation

#### Required Frontmatter Template

```yaml
---
marp: true
theme: default
paginate: true
backgroundColor: #fff
style: |
  section {
    font-size: 20px;
    line-height: 1.6;
    padding: 30px 40px;
  }

  h1 {
    font-size: 2.2em;
    color: #2c3e50;
    margin-bottom: 0.5em;
  }

  h2 {
    font-size: 1.8em;
    color: #34495e;
    margin-bottom: 0.4em;
  }

  h3 {
    font-size: 1.4em;
    color: #555;
  }

  code {
    background: #f6f8fa;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.8em;
  }

  pre {
    background: #f6f8fa;
    padding: 16px;
    border-radius: 6px;
    max-height: 80vh;
    overflow: auto;
  }

  pre code {
    background: transparent;
    padding: 0;
  }

  ul, ol {
    margin-left: 1.5em;
  }

  li {
    margin-bottom: 0.3em;
  }
---
```

#### Content Conversion Rules

**Slide Pagination:**
- Each H1 (`#`) starts a new slide with `---` separator
- Each H2 (`##`) starts a new slide
- Code blocks >15 lines get dedicated slides
- Long paragraphs (>600 chars) split across slides

**Code Block Handling:**
- Preserve syntax highlighting language tags
- Add warning comment if line width >100 characters
- Keep code blocks under 80vh to prevent overflow

**List Formatting:**
- Maintain original indentation levels
- Convert nested lists to progressive disclosure when >10 items

### 5. Segmented Generation Strategy

When `estimated_slides > 30`, split content into logical parts:

```python
# Split by major sections (H1 headers)
parts = split_by_h1_headers(content)

# Generate each part
for i, part in enumerate(parts, 1):
    part_content = generate_marp_markdown(part)
    Write(f'slides-part{i}.md', part_content)

# Merge all parts
Bash('cat slides-part*.md > slides.md')

# Cleanup temporary files
Bash('rm slides-part*.md')
```

**Part Structure:**
- Each part starts with proper Marp frontmatter
- Parts connect seamlessly without duplicate headers
- Final merge removes redundant frontmatter blocks (keep only first)

### 6. Output Validation

Before completion, verify:

```python
validation_checks = {
    'has_frontmatter': check_yaml_frontmatter(),
    'marp_true': 'marp: true' in frontmatter,
    'has_content': line_count > 10,
    'proper_separators': '---' separators present,
    'no_overflow': max_line_length < 120
}
```

If validation fails, regenerate problematic sections.

### 7. User Delivery

Provide clear rendering instructions:

```
✅ slides.md generated successfully

Render to HTML:
  marp slides.md -o slides.html
  open slides.html

Render to PPTX:
  marp slides.md -o slides.pptx
  open slides.pptx

Preview:
  marp -p slides.md
```

## Layout Standards

### Typography (Fixed Sizes)

| Element | Size | Color |
|---------|------|-------|
| Base text | 20px | #333 |
| H1 | 44px (2.2em) | #2c3e50 |
| H2 | 36px (1.8em) | #34495e |
| H3 | 28px (1.4em) | #555 |
| Code inline | 16px (0.8em) | - |
| Code block | 16px (0.8em) | - |

### Spacing

- Section padding: `30px 40px`
- Line height: `1.6`
- Heading bottom margin: `0.4-0.5em`
- List item margin: `0.3em`

### Code Blocks

- Max height: `80vh` (scrollable)
- Background: `#f6f8fa`
- Padding: `16px`
- Border radius: `6px`
- Warn if line width >100 chars

## Best Practices

### Content Optimization

1. **Title Slides**: Always create an engaging title slide with clear topic statement
2. **Progressive Disclosure**: Break complex topics into 3-5 concept slides
3. **Visual Hierarchy**: Use H1 for sections, H2 for subsections, H3 for details
4. **Code Examples**: Always include syntax highlighting, add explanatory comments

### Performance

1. **Parallel Operations**: When extracting from URLs, batch multiple `Read` or fetch operations
2. **Token Efficiency**: For long documents, analyze structure before full content generation
3. **Incremental Output**: Use segmented generation for >30 estimated slides

### Error Handling

1. **URL Extraction Failure**: Try Tavily → SearXNG → ask user for alternative
2. **Topic Too Broad**: Suggest narrowing scope or create overview presentation
3. **Malformed Markdown**: Auto-fix common issues (missing separators, unclosed code blocks)

## Success Criteria

- ✅ Marp frontmatter complete and valid
- ✅ Content properly paginated with `---` separators
- ✅ No layout overflow (text/code fits viewport)
- ✅ Renders successfully to HTML/PPTX without errors
- ✅ All code blocks have syntax highlighting
- ✅ Proper visual hierarchy maintained

## Example Usage Patterns

**Pattern 1: URL to Slides**
```
User: "Convert this article to slides: https://example.com/tutorial"
→ Extract content with Tavily
→ Analyze structure (20 estimated slides)
→ Generate single-pass Marp markdown
→ Output slides.md
```

**Pattern 2: Topic to Slides**
```
User: "Create presentation about TypeScript Generics"
→ Search with SearXNG
→ Extract top 3 results
→ Synthesize content (35 estimated slides)
→ Segment generation (3 parts)
→ Merge and output slides.md
```

**Pattern 3: Markdown File to Slides**
```
User: "Turn tutorial.md into presentation"
→ Read tutorial.md
→ Analyze structure (12 estimated slides)
→ Convert with layout optimization
→ Output slides.md
```

## Notes

- This skill focuses exclusively on input→slides conversion; it does not handle pre-processing like research depth or content enhancement (those are handled externally if needed)
- Always prioritize layout correctness over content volume - better to have 50 well-formatted slides than 100 overflowing ones
- Default to Chinese language for search/content unless user specifies otherwise
- Marp CLI must be installed separately: `npm install -g @marp-team/marp-cli`
