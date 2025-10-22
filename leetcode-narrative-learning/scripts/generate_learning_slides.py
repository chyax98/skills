#!/usr/bin/env python3
"""
LeetCode Narrative Learning Slides Generator

生成叙事式算法学习 HTML 幻灯片的脚本
"""

import os
import re
from pathlib import Path


def get_reveal_js():
    """返回 reveal.js 的 CDN 链接脚本"""
    return """
<!-- Reveal.js Core -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/black.css">
<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.min.js"></script>

<!-- Code Highlighting -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/styles/dracula.css">
<script src="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/lib/highlight.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/lib/languages/python.min.js"></script>
"""


def load_css():
    """加载自定义 CSS"""
    css_path = Path(__file__).parent.parent / "assets" / "css" / "narrative-learning.css"
    if css_path.exists():
        return css_path.read_text(encoding='utf-8')
    return ""


def load_template():
    """加载 HTML 模板"""
    template_path = Path(__file__).parent.parent / "assets" / "templates" / "narrative-slide-template.html"
    if template_path.exists():
        return template_path.read_text(encoding='utf-8')

    # 如果模板不存在,返回基础模板
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{TITLE}}</title>
    {{REVEAL_JS}}
    <style>{{CUSTOM_CSS}}</style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
            {{SLIDES_CONTENT}}
        </div>
    </div>
    <script>
        Reveal.initialize({
            hash: true,
            slideNumber: true,
            transition: 'fade',
            transitionSpeed: 'slow',
            center: true,
            width: 1200,
            height: 800,
        });
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    </script>
</body>
</html>"""


def sanitize_filename(title):
    """将标题转换为安全的文件名"""
    # 移除特殊字符
    safe = re.sub(r'[^\w\s-]', '', title)
    # 替换空格为下划线
    safe = re.sub(r'[\s]+', '_', safe)
    return safe.lower()


def generate_slides_html(slides_data):
    """
    根据结构化数据生成幻灯片 HTML

    slides_data 格式:
    {
        'title': '题目标题',
        'difficulty': 'Easy/Medium/Hard',
        'slides': [
            {
                'type': 'cover/content/code/...',
                'title': '页面标题',
                'content': '页面内容 (支持 Markdown)',
                ...
            }
        ]
    }
    """
    slides_html = []

    for slide in slides_data['slides']:
        slide_type = slide.get('type', 'content')

        if slide_type == 'cover':
            slides_html.append(generate_cover_slide(slide))
        elif slide_type == 'code':
            slides_html.append(generate_code_slide(slide))
        elif slide_type == 'ascii':
            slides_html.append(generate_ascii_slide(slide))
        elif slide_type == 'related':
            slides_html.append(generate_related_slide(slide))
        elif slide_type == 'references':
            slides_html.append(generate_references_slide(slide))
        elif slide_type == 'takeaway':
            slides_html.append(generate_takeaway_slide(slide))
        else:
            slides_html.append(generate_content_slide(slide))

    return '\n'.join(slides_html)


def generate_cover_slide(slide):
    """生成封面页"""
    difficulty_class = f"difficulty-{slide.get('difficulty', 'medium').lower()}"

    return f"""
<section class="cover-slide">
    <h1>{slide.get('title', '')}</h1>
    <p class="subtitle">{slide.get('subtitle', '')}</p>
    <span class="difficulty {difficulty_class}">{slide.get('difficulty', 'Medium')}</span>
</section>
"""


def generate_content_slide(slide):
    """生成内容页"""
    content = slide.get('content', '')

    return f"""
<section>
    <h2>{slide.get('title', '')}</h2>
    {markdown_to_html(content)}
</section>
"""


def generate_code_slide(slide):
    """生成代码页"""
    code = slide.get('code', '')
    language = slide.get('language', 'python')
    explanation = slide.get('explanation', '')

    return f"""
<section>
    <h2>{slide.get('title', '')}</h2>
    {markdown_to_html(explanation) if explanation else ''}
    <pre><code class="language-{language}">{escape_html(code)}</code></pre>
    {markdown_to_html(slide.get('notes', '')) if slide.get('notes') else ''}
</section>
"""


def generate_ascii_slide(slide):
    """生成 ASCII Art 页"""
    ascii_art = slide.get('ascii_art', '')

    return f"""
<section>
    <h2>{slide.get('title', '')}</h2>
    {markdown_to_html(slide.get('description', '')) if slide.get('description') else ''}
    <div class="ascii-art">{escape_html(ascii_art)}</div>
    {markdown_to_html(slide.get('notes', '')) if slide.get('notes') else ''}
</section>
"""


def generate_related_slide(slide):
    """生成相关题目页"""
    problems = slide.get('problems', [])

    problems_html = []
    for p in problems:
        difficulty_class = f"difficulty-{p.get('difficulty', 'medium').lower()}"
        problems_html.append(f"""
<div class="problem-item">
    <div class="problem-title">{p.get('title', '')} <span class="{difficulty_class}">#{p.get('number', '')}</span></div>
    <div class="problem-meta">难度: {p.get('difficulty', 'Medium')}</div>
    <div class="problem-connection">{p.get('connection', '')}</div>
</div>
""")

    return f"""
<section>
    <h2>{slide.get('title', '举一反三')}</h2>
    {markdown_to_html(slide.get('intro', '')) if slide.get('intro') else ''}
    <div class="related-problems">
        {''.join(problems_html)}
    </div>
</section>
"""


def generate_references_slide(slide):
    """生成参考资料页"""
    references = slide.get('references', [])

    refs_html = []
    for ref in references:
        icon = ref.get('icon', '📚')
        refs_html.append(f"""
<div class="reference-item">
    <div class="icon">{icon}</div>
    <div class="content">
        <div class="title">{ref.get('title', '')}</div>
        <div class="description">{ref.get('description', '')}</div>
    </div>
</div>
""")

    return f"""
<section>
    <h2>{slide.get('title', '参考资料')}</h2>
    <div class="references">
        {''.join(refs_html)}
    </div>
</section>
"""


def generate_takeaway_slide(slide):
    """生成总结页"""
    takeaways = slide.get('takeaways', [])

    takeaways_html = '<ul>' + ''.join([f'<li>{t}</li>' for t in takeaways]) + '</ul>'

    return f"""
<section>
    <h2>{slide.get('title', '核心启发')}</h2>
    <div class="takeaway-box">
        <h3>✦ 关键 Takeaway</h3>
        {takeaways_html}
    </div>
    {markdown_to_html(slide.get('next_steps', '')) if slide.get('next_steps') else ''}
</section>
"""


def markdown_to_html(md_text):
    """简单的 Markdown 转 HTML (支持基础语法)"""
    if not md_text:
        return ''

    html = md_text

    # 标题
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)

    # 粗体和斜体
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # 代码
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)

    # 引用
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # 列表 (无序)
    html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\s*)+', r'<ul>\g<0></ul>', html, flags=re.DOTALL)

    # 段落
    paragraphs = html.split('\n\n')
    formatted = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            formatted.append(f'<p>{p}</p>')
        else:
            formatted.append(p)

    return '\n'.join(formatted)


def escape_html(text):
    """转义 HTML 特殊字符"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))


def generate_html(slides_data, output_path=None):
    """
    生成完整的 HTML 文件

    Args:
        slides_data: 幻灯片数据字典
        output_path: 输出文件路径 (可选)

    Returns:
        生成的 HTML 文件路径
    """
    template = load_template()
    css = load_css()
    reveal_js = get_reveal_js()

    slides_html = generate_slides_html(slides_data)

    html = template.replace('{{TITLE}}', slides_data.get('title', 'LeetCode 学习'))
    html = html.replace('{{CUSTOM_CSS}}', css)
    html = html.replace('{{REVEAL_JS}}', reveal_js)
    html = html.replace('{{SLIDES_CONTENT}}', slides_html)

    # 确定输出路径
    if not output_path:
        filename = sanitize_filename(slides_data.get('title', 'leetcode'))
        output_path = f"{filename}_narrative_learning.html"

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return output_path


# 示例使用
if __name__ == '__main__':
    # 示例数据结构
    example_data = {
        'title': 'Two Sum',
        'difficulty': 'Easy',
        'slides': [
            {
                'type': 'cover',
                'title': 'Two Sum',
                'subtitle': '哈希表的空间诗学',
                'difficulty': 'Easy'
            },
            {
                'type': 'content',
                'title': '问题的故事',
                'content': '''
给定一个整数数组和一个目标值,找出数组中和为目标值的两个数。

这不仅仅是一道简单的查找题,它引出了一个深刻的问题:

> **当我们需要快速查找时,如何用空间换取时间?**
'''
            },
        ]
    }

    output = generate_html(example_data)
    print(f"生成成功: {output}")
