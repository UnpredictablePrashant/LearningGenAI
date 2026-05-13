#!/usr/bin/env python3
"""
Demo: Retrieval and Reranking
=============================
Compare vector-style retrieval, keyword retrieval, hybrid fusion, and reranking
over a small DevOps knowledge base.

No API key required. No external packages required.

Run:
    python demos/demo_retrieval_and_reranking.py
"""

from __future__ import annotations

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


CHUNKS = [
    Chunk(
        "rb-001",
        "EC2 Operations",
        "EC2 Operations > Troubleshooting SSH",
        "If an EC2 instance cannot be reached over SSH, check security groups, network ACLs, route tables, public IP assignment, instance state, and OS firewall rules.",
        {"product": "ec2", "doc_type": "runbook"},
    ),
    Chunk(
        "rb-002",
        "EC2 Operations",
        "EC2 Operations > Security Groups",
        "Security groups are stateful virtual firewalls. Allow inbound port 22 for SSH and port 443 for HTTPS from trusted sources.",
        {"product": "ec2", "doc_type": "guide"},
    ),
    Chunk(
        "rb-003",
        "S3 Access",
        "S3 Access > AccessDenied",
        "S3 AccessDenied errors usually mean the IAM principal lacks s3:GetObject, the bucket policy denies access, or the object is encrypted with a KMS key the principal cannot use.",
        {"product": "s3", "doc_type": "runbook"},
    ),
    Chunk(
        "rb-004",
        "Kubernetes Operations",
        "Kubernetes Operations > CrashLoopBackOff",
        "CrashLoopBackOff means a container starts and exits repeatedly. Check kubectl logs --previous, environment variables, mounted secrets, and memory limits.",
        {"product": "kubernetes", "doc_type": "runbook"},
    ),
    Chunk(
        "rb-005",
        "Terraform Operations",
        "Terraform Operations > State Lock",
        "A Terraform state lock prevents concurrent writes. Confirm no active run is still executing before using terraform force-unlock with the lock ID.",
        {"product": "terraform", "doc_type": "runbook"},
    ),
    Chunk(
        "rb-006",
        "EC2 Cost",
        "EC2 Cost > Idle Instances",
        "Idle EC2 instances and unattached EBS volumes can create waste. Use tags, budgets, scheduled stops, and rightsizing recommendations.",
        {"product": "ec2", "doc_type": "guide"},
    ),
]


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def hashed_embedding(text: str, dimensions: int = 96) -> list[float]:
    vector = [0.0] * dimensions
    for token in tokenize(text):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=4).hexdigest()
        vector[int(digest, 16) % dimensions] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(left * right for left, right in zip(a, b))


def searchable_text(chunk: Chunk) -> str:
    return f"{chunk.title} {chunk.heading_path} {chunk.text}"


CHUNK_VECTORS = {chunk.chunk_id: hashed_embedding(searchable_text(chunk)) for chunk in CHUNKS}


def vector_search(query: str, top_k: int = 4) -> list[tuple[Chunk, float]]:
    query_vector = hashed_embedding(query)
    scored = [(chunk, cosine(query_vector, CHUNK_VECTORS[chunk.chunk_id])) for chunk in CHUNKS]
    return sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]


def idf_values(chunks: list[Chunk]) -> dict[str, float]:
    document_frequency: Counter[str] = Counter()
    for chunk in chunks:
        document_frequency.update(set(tokenize(searchable_text(chunk))))
    total_docs = len(chunks)
    return {
        term: math.log((total_docs + 1) / (df + 0.5)) + 1.0
        for term, df in document_frequency.items()
    }


IDF = idf_values(CHUNKS)


def keyword_search(query: str, top_k: int = 4) -> list[tuple[Chunk, float]]:
    query_terms = tokenize(query)
    scored: list[tuple[Chunk, float]] = []
    for chunk in CHUNKS:
        doc_counts = Counter(tokenize(searchable_text(chunk)))
        score = sum(doc_counts[term] * IDF.get(term, 0.0) for term in query_terms)
        if score > 0:
            scored.append((chunk, score))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]


def reciprocal_rank_fusion(result_lists: list[list[tuple[Chunk, float]]], k: int = 60) -> list[tuple[Chunk, float]]:
    scores: defaultdict[str, float] = defaultdict(float)
    chunks_by_id: dict[str, Chunk] = {}
    for results in result_lists:
        for rank, (chunk, _score) in enumerate(results, start=1):
            scores[chunk.chunk_id] += 1 / (k + rank)
            chunks_by_id[chunk.chunk_id] = chunk
    fused = [(chunks_by_id[chunk_id], score) for chunk_id, score in scores.items()]
    return sorted(fused, key=lambda item: item[1], reverse=True)


def simple_rerank(query: str, candidates: list[Chunk], top_n: int = 3) -> list[tuple[Chunk, float]]:
    query_terms = set(tokenize(query))
    reranked: list[tuple[Chunk, float]] = []
    for chunk in candidates:
        text_terms = set(tokenize(chunk.text))
        heading_terms = set(tokenize(chunk.heading_path))
        exact_bonus = 0.2 if any(term in chunk.text.lower() for term in ["ssh", "port 22", "https", "443"]) else 0.0
        score = (
            len(query_terms & text_terms) / (len(query_terms) or 1)
            + 0.5 * len(query_terms & heading_terms) / (len(query_terms) or 1)
            + exact_bonus
        )
        reranked.append((chunk, score))
    return sorted(reranked, key=lambda item: item[1], reverse=True)[:top_n]


def print_results(label: str, results: list[tuple[Chunk, float]]) -> None:
    print(f"\n{label}")
    print("-" * len(label))
    for rank, (chunk, score) in enumerate(results, start=1):
        print(f"{rank}. {chunk.chunk_id} score={score:.4f} | {chunk.heading_path}")
        print(f"   {chunk.text[:120]}...")


def main() -> None:
    query = "I cannot SSH to my EC2 instance. Which network rules should I check?"

    print("\nDemo: Retrieval and Reranking\n")
    print(f"Query: {query}")

    vector_results = vector_search(query)
    keyword_results = keyword_search(query)
    hybrid_results = reciprocal_rank_fusion([vector_results, keyword_results])
    reranked = simple_rerank(query, [chunk for chunk, _score in hybrid_results], top_n=3)

    print_results("Vector search", vector_results)
    print_results("Keyword search", keyword_results)
    print_results("Hybrid retrieval with RRF", hybrid_results[:4])
    print_results("Reranked final context", reranked)

    print("\nObservation:")
    print("Vector search finds semantic neighbors. Keyword search protects exact terms.")
    print("Hybrid retrieval improves recall, and reranking chooses the most answer-like chunks.")


if __name__ == "__main__":
    main()

