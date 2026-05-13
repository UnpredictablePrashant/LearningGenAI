#!/usr/bin/env python3
"""
Demo: Chunking Strategies for RAG
=================================
Compare fixed-size chunking with heading-aware token chunking.

This demo uses a small in-memory document so it is fast and repeatable. It
mirrors the notebook idea: preserve headings, count tokens, create chunk IDs,
and inspect small/large chunks before embedding.

Run:
    python demos/demo_chunking_strategies.py
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
import textwrap


try:
    import tiktoken
except ImportError:  # pragma: no cover - useful before requirements install
    tiktoken = None


DOCUMENT = """
# AWS EC2 Operations Guide

## Overview
Amazon EC2 provides virtual servers called instances. Teams use instances when
they need control over operating systems, networking, storage, and compute
capacity. A RAG assistant should retrieve the exact section that explains the
concept rather than sending an entire cloud guide to the model.

## Instance Types
Instance types define CPU, memory, storage, and networking capacity. General
purpose instances are balanced. Compute optimized instances work well for CPU
heavy workloads. Memory optimized instances are useful for databases and caches.
Burstable instances provide baseline CPU performance and spend credits when they
burst above that baseline.

## Security Groups
Security groups are stateful virtual firewalls attached to ENIs or instances.
Inbound rules control allowed traffic into the instance. Outbound rules control
traffic leaving the instance. If SSH fails, check whether port 22 is allowed from
the operator network. If HTTPS fails, check whether port 443 is allowed from the
load balancer or client network.

## Troubleshooting SSH
When an EC2 instance cannot be reached over SSH, check security groups, network
ACLs, route tables, public IP assignment, instance state, and operating system
firewall rules. Also check whether the correct key pair is being used. For
private instances, connect through a bastion host or Systems Manager Session
Manager.

## Cost Controls
Use tags, budgets, rightsizing recommendations, and scheduled stop policies to
control EC2 cost. Unattached EBS volumes and idle instances are common sources
of waste. Cost-related chunks should preserve metadata such as account, region,
environment, and owner.
""".strip()


TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")


@dataclass
class Chunk:
    chunk_id: str
    heading_path: str
    text: str
    token_count: int
    strategy: str


def count_tokens(text: str) -> int:
    if tiktoken is None:
        return len(TOKEN_RE.findall(text))
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def make_chunk_id(strategy: str, heading_path: str, text: str) -> str:
    raw = f"{strategy}|{heading_path}|{text}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def fixed_word_chunks(text: str, size: int = 70, overlap: int = 15) -> list[Chunk]:
    words = text.split()
    chunks: list[Chunk] = []
    start = 0
    while start < len(words):
        end = min(start + size, len(words))
        chunk_text = " ".join(words[start:end])
        chunks.append(
            Chunk(
                chunk_id=make_chunk_id("fixed", "unknown", chunk_text),
                heading_path="unknown",
                text=chunk_text,
                token_count=count_tokens(chunk_text),
                strategy="fixed_words",
            )
        )
        if end == len(words):
            break
        start = end - overlap
    return chunks


def heading_blocks(markdown_text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    path: list[str] = []
    buffer: list[str] = []

    def flush() -> None:
        if buffer:
            heading_path = " > ".join(path) if path else "Untitled"
            blocks.append((heading_path, " ".join(buffer).strip()))
            buffer.clear()

    for raw_line in markdown_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        match = HEADING_RE.match(line)
        if match:
            flush()
            level = len(match.group(1))
            heading = match.group(2)
            path[:] = path[: level - 1]
            path.append(heading)
        else:
            buffer.append(line)

    flush()
    return blocks


def split_tokens_approximately(text: str, max_tokens: int, overlap: int) -> list[str]:
    words = text.split()
    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(start + max_tokens, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = max(0, end - overlap)
    return chunks


def heading_aware_chunks(text: str, max_tokens: int = 90, overlap: int = 15) -> list[Chunk]:
    chunks: list[Chunk] = []
    for heading_path, block_text in heading_blocks(text):
        for part in split_tokens_approximately(block_text, max_tokens, overlap):
            enriched_text = f"Heading: {heading_path}\n{part}"
            chunks.append(
                Chunk(
                    chunk_id=make_chunk_id("heading", heading_path, enriched_text),
                    heading_path=heading_path,
                    text=enriched_text,
                    token_count=count_tokens(enriched_text),
                    strategy="heading_aware",
                )
            )
    return chunks


def describe(chunks: list[Chunk]) -> None:
    counts = [chunk.token_count for chunk in chunks]
    small = [chunk for chunk in chunks if chunk.token_count < 30]
    large = [chunk for chunk in chunks if chunk.token_count > 120]
    print(f"Chunks: {len(chunks)}")
    print(f"Token count min/avg/max: {min(counts)} / {sum(counts) / len(counts):.1f} / {max(counts)}")
    print(f"Small chunks < 30 tokens: {len(small)}")
    print(f"Large chunks > 120 tokens: {len(large)}")


def preview(chunks: list[Chunk], limit: int = 3) -> None:
    for chunk in chunks[:limit]:
        print("-" * 80)
        print(f"ID: {chunk.chunk_id}")
        print(f"Strategy: {chunk.strategy}")
        print(f"Heading: {chunk.heading_path}")
        print(f"Tokens: {chunk.token_count}")
        print(textwrap.shorten(chunk.text.replace("\n", " "), width=220, placeholder="..."))


def main() -> None:
    print("\nDemo: Chunking Strategies for RAG\n")
    if tiktoken is None:
        print("tiktoken is not installed. Falling back to approximate word counts.\n")

    fixed = fixed_word_chunks(DOCUMENT)
    heading = heading_aware_chunks(DOCUMENT)

    print("Fixed word chunks")
    describe(fixed)
    preview(fixed)

    print("\nHeading-aware chunks")
    describe(heading)
    preview(heading)

    print("\nObservation:")
    print("Fixed chunks are easy, but they lose document structure.")
    print("Heading-aware chunks preserve source context that helps retrieval, reranking, and citations.")


if __name__ == "__main__":
    main()

