#!/usr/bin/env python3
"""Lab 04: Retrieval and Reranking (SOLUTION)"""

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
    total_docs = len(chunks)
    document_frequency: Counter[str] = Counter()
    for chunk in chunks:
        document_frequency.update(set(tokenize(searchable_text(chunk))))
    return {
        term: math.log((total_docs + 1) / (df + 0.5)) + 1.0
        for term, df in document_frequency.items()
    }


def keyword_search(query: str, chunks: list[Chunk], idf: dict[str, float], top_k: int = 5) -> list[tuple[Chunk, float]]:
    query_terms = tokenize(query)
    scored: list[tuple[Chunk, float]] = []
    for chunk in chunks:
        counts = Counter(tokenize(searchable_text(chunk)))
        score = sum(counts[term] * idf.get(term, 0.0) for term in query_terms)
        if score > 0:
            scored.append((chunk, score))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]


def vector_search(query: str, chunks: list[Chunk], vectors: dict[str, list[float]], top_k: int = 5) -> list[tuple[Chunk, float]]:
    query_vector = embed(query)
    scored = [(chunk, cosine(query_vector, vectors[chunk.chunk_id])) for chunk in chunks]
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


def rerank(query: str, candidates: list[Chunk], top_n: int = 3) -> list[tuple[Chunk, float]]:
    query_terms = set(tokenize(query))
    results: list[tuple[Chunk, float]] = []
    for chunk in candidates:
        text_terms = set(tokenize(chunk.text))
        heading_terms = set(tokenize(chunk.heading_path))
        text_overlap = len(query_terms & text_terms) / (len(query_terms) or 1)
        heading_overlap = len(query_terms & heading_terms) / (len(query_terms) or 1)
        lower_text = chunk.text.lower()
        exact_bonus = 0.2 if "port 22" in lower_text or "ssh" in lower_text else 0.0
        score = text_overlap + 0.5 * heading_overlap + exact_bonus
        results.append((chunk, score))
    return sorted(results, key=lambda item: item[1], reverse=True)[:top_n]


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
    print("\nLab 04: Retrieval and Reranking (Solution)\n")

    chunks = sample_chunks()
    idf = build_idf(chunks)
    vectors = {chunk.chunk_id: embed(searchable_text(chunk)) for chunk in chunks}
    query = "EC2 SSH fails. Which network rules and ports should I check?"

    keyword = keyword_search(query, chunks, idf, top_k=4)
    vector = vector_search(query, chunks, vectors, top_k=4)
    fused = reciprocal_rank_fusion([keyword, vector])
    final = rerank(query, [chunk for chunk, _score in fused], top_n=3)

    print(f"Query: {query}\n")
    for label, results in [("keyword", keyword), ("vector", vector), ("fused", fused), ("reranked", final)]:
        print(label.upper())
        for rank, (chunk, score) in enumerate(results, start=1):
            print(f"  {rank}. {chunk.chunk_id} score={score:.4f} heading={chunk.heading_path}")
        print()


if __name__ == "__main__":
    main()

