#!/usr/bin/env python3
"""
Lab 02: Chunking Strategy
=========================
Build heading-aware, token-limited chunks with overlap and small-chunk merging.

This mirrors the notebook's chunking section, but uses only Python standard
library code so the mechanics are visible.

Run:
    python lab.py

When stuck: check solution.py
"""

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
    # TODO 1:
    # Return TOKEN_RE matches from text. Preserve original casing.
    pass


def count_tokens(text: str) -> int:
    # TODO 2:
    # Return the number of approximate tokens in text.
    pass


def detect_heading(line: str) -> tuple[int, str] | None:
    # TODO 3:
    # Detect headings from either Markdown headings like "## Security Groups"
    # or numbered headings like "2.1 Security Groups".
    # Return (level, heading_text), or None.
    #
    # Markdown level is the number of # characters.
    # Numbered level is the count of "." in the number plus 1.
    pass


def create_heading_blocks(pages: list[PageRecord]) -> list[HeadingBlock]:
    # TODO 4:
    # Walk each page line by line.
    # Track a heading path starting with the page title.
    # When a heading is seen, flush the current buffer into a HeadingBlock.
    # Store block text under the current heading path.
    pass


def split_with_overlap(text: str, max_tokens: int, overlap: int) -> list[str]:
    # TODO 5:
    # Split text into word-token chunks with a sliding overlap.
    # If max_tokens=20 and overlap=5, the next chunk starts 15 tokens later.
    pass


def create_chunk_id(source_file: str, page_number: int, heading_path: str, chunk_index: int, text: str) -> str:
    raw = f"{source_file}|{page_number}|{heading_path}|{chunk_index}|{text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def create_chunks(blocks: list[HeadingBlock], max_tokens: int = 45, overlap: int = 8) -> list[Chunk]:
    # TODO 6:
    # Split every block into one or more chunks.
    # Include the heading path in the chunk text so embeddings see context.
    # Fill all Chunk fields and count tokens.
    pass


def merge_small_chunks(chunks: list[Chunk], min_tokens: int = 18, max_tokens: int = 70) -> list[Chunk]:
    # TODO 7:
    # Merge a small chunk with the next chunk only when source_file,
    # page_number, and heading_path match and the merged size <= max_tokens.
    pass


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
    print("\nLab 02: Chunking Strategy\n")

    blocks = create_heading_blocks(sample_pages())
    if blocks is None:
        print("TODO 4 not complete: create_heading_blocks returned None.")
        return

    chunks = create_chunks(blocks)
    if chunks is None:
        print("TODO 6 not complete: create_chunks returned None.")
        return

    merged = merge_small_chunks(chunks)
    if merged is None:
        print("TODO 7 not complete: merge_small_chunks returned None.")
        return

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

