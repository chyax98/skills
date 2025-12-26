#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "docling>=2.0.0",
#     "docling-core>=2.0.0",
# ]
# ///
"""
需求文档 PDF 解析脚本 - 使用 Docling 官方 API

用法:
    uv run parse_pdf.py <pdf_path> [-o output_dir] [--no-ocr]

输出结构:
    output_dir/
    ├── document.md      # Markdown（图片已引用）
    ├── result.json      # 元数据
    └── images/          # 图片文件
"""

import argparse
import json
import sys
import unicodedata
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode


def parse_pdf(
    pdf_path: str,
    output_dir: str = "./parsed_output",
    enable_ocr: bool = True,
) -> dict:
    """解析 PDF 并保存结果"""
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"解析中: {pdf_path}", file=sys.stderr)

    # Docling 配置
    pipeline_options = PdfPipelineOptions(
        do_ocr=enable_ocr,
        do_table_structure=True,
        generate_picture_images=True,
        images_scale=2.0,
    )
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
    pipeline_options.table_structure_options.do_cell_matching = True

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    # 解析
    result = converter.convert(str(pdf_path))
    doc = result.document

    # 统计
    page_count = len(list(doc.pages))
    table_count = len(list(doc.tables))
    image_count = len(list(doc.pictures))

    print(f"完成: {page_count} 页, {image_count} 张图片, {table_count} 个表格", file=sys.stderr)

    # 使用官方 API 保存 Markdown + 图片（ImageRefMode.REFERENCED 自动生成引用）
    md_path = output_dir / "document.md"
    doc.save_as_markdown(
        md_path,
        image_mode=ImageRefMode.REFERENCED,
    )

    # NFKC 规范化修复 CJK 兼容字符乱码
    md_text = md_path.read_text(encoding="utf-8")
    md_text = unicodedata.normalize("NFKC", md_text)
    md_path.write_text(md_text, encoding="utf-8")

    print(f"Markdown: {md_path}", file=sys.stderr)

    # 收集图片路径
    image_paths = sorted([str(p) for p in output_dir.glob("*.png")])

    # 元数据 JSON
    metadata = {
        "source": str(pdf_path),
        "markdown_path": str(md_path),
        "image_paths": image_paths,
        "page_count": page_count,
        "table_count": table_count,
        "image_count": len(image_paths),
    }
    json_path = output_dir / "result.json"
    json_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
    print(f"元数据: {json_path}", file=sys.stderr)

    return metadata


def main():
    parser = argparse.ArgumentParser(
        description="解析需求文档 PDF 为 Markdown + 图片"
    )
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument(
        "-o", "--output", default="./parsed_output", help="输出目录"
    )
    parser.add_argument(
        "--no-ocr", action="store_true", help="禁用 OCR（非扫描件加速）"
    )

    args = parser.parse_args()

    metadata = parse_pdf(
        args.pdf_path,
        output_dir=args.output,
        enable_ocr=not args.no_ocr,
    )

    # 输出 JSON 供 Agent 读取
    print(json.dumps(metadata, ensure_ascii=False))


if __name__ == "__main__":
    main()
