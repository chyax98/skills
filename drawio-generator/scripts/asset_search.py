#!/usr/bin/env python3
"""
Asset Search - 素材库语义检索工具

用法:
    # 构建索引
    python asset_search.py --build --references ../references/

    # 搜索素材
    python asset_search.py --query "数据库圆柱形状"
    python asset_search.py --query "蓝色渐变配色" --top 5

    # 查看索引状态
    python asset_search.py --status

输入: 自然语言查询
输出: 相关素材片段 + 来源文件
"""

import json
import os
import re
import sys
import argparse
import pickle
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# 尝试导入 embedding 库
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_EMBEDDING = True
except ImportError:
    HAS_EMBEDDING = False


@dataclass
class AssetChunk:
    """素材片段"""
    id: str
    title: str
    content: str
    source_file: str
    section_path: List[str]  # 层级路径 ["# 主标题", "## 子标题"]
    chunk_type: str  # heading, table, code, text


class AssetIndexer:
    """素材索引器"""

    def __init__(self, model_name: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        """
        初始化索引器

        Args:
            model_name: sentence-transformers 模型名
                - paraphrase-multilingual-MiniLM-L12-v2: 多语言，较小
                - all-MiniLM-L6-v2: 英文，最小最快
                - paraphrase-mpnet-base-v2: 英文，最准
        """
        self.model_name = model_name
        self.model = None
        self.chunks: List[AssetChunk] = []
        self.embeddings: Optional[np.ndarray] = None

    def _load_model(self):
        """延迟加载模型"""
        if self.model is None:
            if not HAS_EMBEDDING:
                raise ImportError("需要安装 sentence-transformers: pip install sentence-transformers")
            print(f"⏳ 加载模型: {self.model_name}", file=sys.stderr)
            self.model = SentenceTransformer(self.model_name)

    def parse_markdown(self, filepath: Path) -> List[AssetChunk]:
        """解析 Markdown 文件，按标题分块"""
        chunks = []
        content = filepath.read_text(encoding='utf-8')
        lines = content.split('\n')

        current_sections = []  # 层级标题栈
        current_content = []
        current_title = filepath.stem
        chunk_id = 0

        def save_chunk():
            nonlocal chunk_id
            if current_content:
                text = '\n'.join(current_content).strip()
                if text:
                    # 判断内容类型
                    chunk_type = 'text'
                    if '```' in text:
                        chunk_type = 'code'
                    elif '|' in text and text.count('|') > 2:
                        chunk_type = 'table'

                    chunks.append(AssetChunk(
                        id=f"{filepath.stem}_{chunk_id}",
                        title=current_title,
                        content=text,
                        source_file=filepath.name,
                        section_path=current_sections.copy(),
                        chunk_type=chunk_type
                    ))
                    chunk_id += 1

        for line in lines:
            # 检测标题
            heading_match = re.match(r'^(#{1,4})\s+(.+)$', line)
            if heading_match:
                # 保存当前块
                save_chunk()
                current_content = []

                level = len(heading_match.group(1))
                title = heading_match.group(2)

                # 更新层级
                while len(current_sections) >= level:
                    current_sections.pop()
                current_sections.append(f"{'#' * level} {title}")
                current_title = title
            else:
                current_content.append(line)

        # 保存最后一块
        save_chunk()

        return chunks

    def build_index(self, references_dir: Path) -> int:
        """构建索引"""
        self._load_model()

        # 解析所有 markdown 文件
        self.chunks = []
        md_files = list(references_dir.glob("*.md"))

        for md_file in md_files:
            file_chunks = self.parse_markdown(md_file)
            self.chunks.extend(file_chunks)
            print(f"  📄 {md_file.name}: {len(file_chunks)} 块", file=sys.stderr)

        if not self.chunks:
            print("⚠️  未找到任何素材", file=sys.stderr)
            return 0

        # 生成 embeddings
        print(f"⏳ 生成 {len(self.chunks)} 个 embeddings...", file=sys.stderr)
        texts = [self._chunk_to_text(c) for c in self.chunks]
        self.embeddings = self.model.encode(texts, show_progress_bar=True)

        print(f"✅ 索引构建完成: {len(self.chunks)} 块", file=sys.stderr)
        return len(self.chunks)

    def _chunk_to_text(self, chunk: AssetChunk) -> str:
        """将 chunk 转为用于 embedding 的文本"""
        parts = []
        if chunk.section_path:
            parts.append(' > '.join(chunk.section_path))
        parts.append(chunk.title)
        parts.append(chunk.content[:500])  # 截断过长内容
        return '\n'.join(parts)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[AssetChunk, float]]:
        """语义搜索"""
        if self.embeddings is None or len(self.chunks) == 0:
            return []

        self._load_model()

        # 编码查询
        query_embedding = self.model.encode([query])[0]

        # 计算相似度
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )

        # 排序
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append((self.chunks[idx], float(similarities[idx])))

        return results

    def save(self, filepath: Path):
        """保存索引"""
        data = {
            'model_name': self.model_name,
            'chunks': [asdict(c) for c in self.chunks],
            'embeddings': self.embeddings.tolist() if self.embeddings is not None else None
        }
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"✅ 索引已保存: {filepath}", file=sys.stderr)

    def load(self, filepath: Path) -> bool:
        """加载索引"""
        if not filepath.exists():
            return False

        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        self.model_name = data['model_name']
        self.chunks = [AssetChunk(**c) for c in data['chunks']]
        self.embeddings = np.array(data['embeddings']) if data['embeddings'] else None

        return True


def format_result(chunk: AssetChunk, score: float) -> str:
    """格式化搜索结果"""
    lines = [
        f"📎 [{chunk.source_file}] {chunk.title} (相似度: {score:.3f})",
        f"   路径: {' > '.join(chunk.section_path) if chunk.section_path else '(顶层)'}",
        f"   类型: {chunk.chunk_type}",
        "   内容:",
    ]

    # 截断过长内容
    content = chunk.content
    if len(content) > 500:
        content = content[:500] + "..."

    for line in content.split('\n')[:10]:  # 最多显示 10 行
        lines.append(f"   {line}")

    if content.count('\n') > 10:
        lines.append("   ...")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Asset Search - 素材库语义检索')
    parser.add_argument('--build', action='store_true', help='构建索引')
    parser.add_argument('--references', '-r', help='references 目录路径')
    parser.add_argument('--query', '-q', help='搜索查询')
    parser.add_argument('--top', '-k', type=int, default=3, help='返回结果数量')
    parser.add_argument('--status', action='store_true', help='查看索引状态')
    parser.add_argument('--index', '-i', help='索引文件路径')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')

    args = parser.parse_args()

    # 默认索引路径
    script_dir = Path(__file__).parent
    default_index = script_dir / '.asset_index.pkl'
    default_refs = script_dir.parent / 'references'
    index_path = Path(args.index) if args.index else default_index

    indexer = AssetIndexer()

    if args.build:
        # 构建索引
        refs_dir = Path(args.references) if args.references else default_refs
        if not refs_dir.exists():
            print(f"❌ 目录不存在: {refs_dir}", file=sys.stderr)
            sys.exit(1)

        print(f"🔨 构建索引: {refs_dir}", file=sys.stderr)
        count = indexer.build_index(refs_dir)
        if count > 0:
            indexer.save(index_path)

    elif args.status:
        # 查看状态
        if indexer.load(index_path):
            print(f"✅ 索引已加载: {index_path}")
            print(f"   模型: {indexer.model_name}")
            print(f"   素材块: {len(indexer.chunks)}")

            # 统计来源
            sources = {}
            for c in indexer.chunks:
                sources[c.source_file] = sources.get(c.source_file, 0) + 1
            print("   来源分布:")
            for src, cnt in sorted(sources.items()):
                print(f"     {src}: {cnt}")
        else:
            print(f"❌ 索引不存在: {index_path}")
            print(f"   请先运行: python {__file__} --build")

    elif args.query:
        # 搜索
        if not indexer.load(index_path):
            print(f"❌ 索引不存在，请先构建: python {__file__} --build", file=sys.stderr)
            sys.exit(1)

        results = indexer.search(args.query, top_k=args.top)

        if args.json:
            output = []
            for chunk, score in results:
                output.append({
                    **asdict(chunk),
                    'score': score
                })
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔍 搜索: \"{args.query}\"\n")
            print("=" * 60)
            for chunk, score in results:
                print(format_result(chunk, score))
                print("-" * 60)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
