#!/usr/bin/env python3
"""Lab 02: Chunking Strategy (SOLUTION)"""

from dataclasses import dataclass
import hashlib
import re


TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+")
MARKDOWN_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")
NUMBERED_HEADING_RE = re.compile(r"^(\d+(?:\.\d+)*\.?)\s+(.+)$")


@dataclass
class PageRecord:
    source_file: str
    page_number: int
    title: str
    text: str


@dataclass
class HeadingBlock:
    source_file: str
    page_number: int
    title: str
    heading_path: str
    text: str


@dataclass
class Chunk:
    chunk_id: str
    source_file: str
    page_number: int
    chunk_index: int
    title: str
    heading_path: str
    text: str
    token_count: int


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text)


def count_tokens(text: str) -> int:
    return len(tokenize(text))


def detect_heading(line: str) -> tuple[int, str] | None:
    line = line.strip()
    markdown = MARKDOWN_HEADING_RE.match(line)
    if markdown:
        return len(markdown.group(1)), markdown.group(2).strip()

    numbered = NUMBERED_HEADING_RE.match(line)
    if numbered and len(line) <= 120:
        number = numbered.group(1).rstrip(".")
        return number.count(".") + 1, numbered.group(2).strip()

    return None


def create_heading_blocks(pages: list[PageRecord]) -> list[HeadingBlock]:
    blocks: list[HeadingBlock] = []

    for page in pages:
        path = [page.title]
        buffer: list[str] = []

        def flush() -> None:
            if not buffer:
                return
            blocks.append(
                HeadingBlock(
                    source_file=page.source_file,
                    page_number=page.page_number,
                    title=page.title,
                    heading_path=" > ".join(path),
                    text=" ".join(buffer).strip(),
                )
            )
            buffer.clear()

        for raw_line in page.text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            heading = detect_heading(line)
            if heading:
                flush()
                level, heading_text = heading
                if level == 1:
                    path[:] = [heading_text]
                else:
                    path[:] = path[: level - 1]
                    path.append(heading_text)
            else:
                buffer.append(line)

        flush()

    return blocks


def split_with_overlap(text: str, max_tokens: int, overlap: int) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(start + max_tokens, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = max(0, end - overlap)
    return chunks


def create_chunk_id(source_file: str, page_number: int, heading_path: str, chunk_index: int, text: str) -> str:
    raw = f"{source_file}|{page_number}|{heading_path}|{chunk_index}|{text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def create_chunks(blocks: list[HeadingBlock], max_tokens: int = 45, overlap: int = 8) -> list[Chunk]:
    chunks: list[Chunk] = []
    for block in blocks:
        parts = split_with_overlap(block.text, max_tokens=max_tokens, overlap=overlap)
        for local_index, part in enumerate(parts):
            chunk_text = f"Heading: {block.heading_path}\n{part}"
            chunks.append(
                Chunk(
                    chunk_id=create_chunk_id(
                        block.source_file,
                        block.page_number,
                        block.heading_path,
                        local_index,
                        chunk_text,
                    ),
                    source_file=block.source_file,
                    page_number=block.page_number,
                    chunk_index=local_index,
                    title=block.title,
                    heading_path=block.heading_path,
                    text=chunk_text,
                    token_count=count_tokens(chunk_text),
                )
            )
    return chunks


def merge_small_chunks(chunks: list[Chunk], min_tokens: int = 18, max_tokens: int = 70) -> list[Chunk]:
    merged: list[Chunk] = []
    buffer: Chunk | None = None

    for chunk in chunks:
        if buffer is None:
            buffer = chunk
            continue

        same_scope = (
            buffer.source_file == chunk.source_file
            and buffer.page_number == chunk.page_number
            and buffer.heading_path == chunk.heading_path
        )
        combined_text = f"{buffer.text}\n{chunk.text}"
        combined_tokens = count_tokens(combined_text)

        if buffer.token_count < min_tokens and same_scope and combined_tokens <= max_tokens:
            buffer = Chunk(
                chunk_id=create_chunk_id(
                    buffer.source_file,
                    buffer.page_number,
                    buffer.heading_path,
                    buffer.chunk_index,
                    combined_text,
                ),
                source_file=buffer.source_file,
                page_number=buffer.page_number,
                chunk_index=buffer.chunk_index,
                title=buffer.title,
                heading_path=buffer.heading_path,
                text=combined_text,
                token_count=combined_tokens,
            )
        else:
            merged.append(buffer)
            buffer = chunk

    if buffer is not None:
        merged.append(buffer)

    return merged


def sample_pages() -> list[PageRecord]:
    return [
        PageRecord(
            source_file="aws-ec2-guide.pdf",
            page_number=1,
            title="AWS EC2 Guide",
            text="""# AWS EC2 Guide
## Overview
Amazon EC2 provides virtual servers called instances. Teams use EC2 when they need control over networking, operating systems, and compute capacity.
## Security Groups
Security groups are stateful firewalls. Inbound rules control traffic into an instance. For SSH, allow TCP port 22 only from trusted networks. For HTTPS, allow TCP port 443 from clients or load balancers.""",
        ),
        PageRecord(
            source_file="aws-ec2-guide.pdf",
            page_number=2,
            title="AWS EC2 Guide",
            text="""## Troubleshooting SSH
When SSH fails, check security groups, network ACLs, route tables, public IP assignment, instance state, and operating system firewall rules.
## Cost Controls
Use tags, budgets, scheduled stops, and rightsizing recommendations. Idle instances and unattached EBS volumes are common waste sources.""",
        ),
    ]


def main() -> None:
    print("\nLab 02: Chunking Strategy (Solution)\n")

    blocks = create_heading_blocks(sample_pages())
    chunks = create_chunks(blocks)
    merged = merge_small_chunks(chunks)

    print(f"Blocks: {len(blocks)}")
    print(f"Initial chunks: {len(chunks)}")
    print(f"Merged chunks: {len(merged)}")
    print()

    for chunk in merged:
        print(f"- {chunk.chunk_id} | p{chunk.page_number} | {chunk.token_count} tokens")
        print(f"  {chunk.heading_path}")
        print(f"  {chunk.text[:180]}...")


if __name__ == "__main__":
    main()
