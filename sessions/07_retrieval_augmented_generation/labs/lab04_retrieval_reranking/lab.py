#!/usr/bin/env python3
"""
Lab 04: Retrieval and Reranking
===============================
Combine keyword retrieval, vector retrieval, reciprocal rank fusion, and a
simple reranker.

The reranker in this lab is intentionally lightweight. Production systems often
use a CrossEncoder or hosted reranking API.

Run:
    python lab.py

When stuck: check solution.py
"""

from dataclasses import dataclass, field
from collections import Counter, defaultdict
import hashlib
import math
import re


TOKEN_RE = re.compile(r"[a-z0-9_./:-]+")


@dataclass
class Chunk:
    chunk_id: str
    title: str
    heading_path: str
    text: str
    metadata: dict[str, str] = field(default_factory=dict)


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def searchable_text(chunk: Chunk) -> str:
    return f"{chunk.title} {chunk.heading_path} {chunk.text}"


def embed(text: str, dimensions: int = 96) -> list[float]:
    vector = [0.0] * dimensions
    for token in tokenize(text):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=4).hexdigest()
        vector[int(digest, 16) % dimensions] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(left * right for left, right in zip(a, b))


def build_idf(chunks: list[Chunk]) -> dict[str, float]:
    # TODO 1:
    # Compute an IDF value per token:
    # log((total_docs + 1) / (document_frequency + 0.5)) + 1
    pass


def keyword_search(query: str, chunks: list[Chunk], idf: dict[str, float], top_k: int = 5) -> list[tuple[Chunk, float]]:
    # TODO 2:
    # Score chunks by query term frequency weighted by IDF.
    # Return only chunks with score > 0, sorted highest first.
    pass


def vector_search(query: str, chunks: list[Chunk], vectors: dict[str, list[float]], top_k: int = 5) -> list[tuple[Chunk, float]]:
    # TODO 3:
    # Embed the query and return top_k chunks by cosine similarity.
    pass


def reciprocal_rank_fusion(result_lists: list[list[tuple[Chunk, float]]], k: int = 60) -> list[tuple[Chunk, float]]:
    # TODO 4:
    # Combine ranked result lists using RRF:
    # score += 1 / (k + rank)
    pass


def rerank(query: str, candidates: list[Chunk], top_n: int = 3) -> list[tuple[Chunk, float]]:
    # TODO 5:
    # Build a simple relevance score:
    # - overlap of query terms with chunk text
    # - half-weight overlap with heading terms
    # - small bonus when the exact phrase "port 22" or "ssh" appears
    # Return top_n sorted highest first.
    pass


def sample_chunks() -> list[Chunk]:
    return [
        Chunk(
            "ec2-ssh",
            "AWS EC2 Guide",
            "AWS EC2 Guide > Troubleshooting SSH",
            "When an EC2 instance cannot be reached over SSH, check security groups, network ACLs, route tables, public IP assignment, and OS firewall rules.",
            {"product": "ec2"},
        ),
        Chunk(
            "ec2-sg",
            "AWS EC2 Guide",
            "AWS EC2 Guide > Security Groups",
            "Security groups are stateful virtual firewalls. Allow inbound TCP port 22 for SSH and TCP port 443 for HTTPS from trusted sources.",
            {"product": "ec2"},
        ),
        Chunk(
            "s3-access",
            "AWS S3 Guide",
            "AWS S3 Guide > AccessDenied",
            "S3 AccessDenied errors can come from missing IAM permissions, bucket policy denies, object ownership, or KMS key restrictions.",
            {"product": "s3"},
        ),
        Chunk(
            "k8s-crash",
            "Kubernetes Runbooks",
            "Kubernetes Runbooks > CrashLoopBackOff",
            "CrashLoopBackOff means a container starts and exits repeatedly. Check previous logs, environment variables, secrets, and memory limits.",
            {"product": "kubernetes"},
        ),
    ]


def main() -> None:
    print("\nLab 04: Retrieval and Reranking\n")

    chunks = sample_chunks()
    idf = build_idf(chunks)
    if idf is None:
        print("TODO 1 not complete: build_idf returned None.")
        return

    vectors = {chunk.chunk_id: embed(searchable_text(chunk)) for chunk in chunks}
    query = "EC2 SSH fails. Which network rules and ports should I check?"

    keyword = keyword_search(query, chunks, idf, top_k=4)
    vector = vector_search(query, chunks, vectors, top_k=4)
    if keyword is None or vector is None:
        print("TODO 2 or TODO 3 not complete.")
        return

    fused = reciprocal_rank_fusion([keyword, vector])
    if fused is None:
        print("TODO 4 not complete: fusion returned None.")
        return

    final = rerank(query, [chunk for chunk, _score in fused], top_n=3)
    if final is None:
        print("TODO 5 not complete: rerank returned None.")
        return

    print(f"Query: {query}\n")
    for label, results in [("keyword", keyword), ("vector", vector), ("fused", fused), ("reranked", final)]:
        print(label.upper())
        for rank, (chunk, score) in enumerate(results, start=1):
            print(f"  {rank}. {chunk.chunk_id} score={score:.4f} heading={chunk.heading_path}")
        print()


if __name__ == "__main__":
    main()

