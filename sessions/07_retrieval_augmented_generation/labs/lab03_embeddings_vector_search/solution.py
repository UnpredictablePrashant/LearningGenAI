#!/usr/bin/env python3
"""Lab 03: Embeddings and Vector Search (SOLUTION)"""

from dataclasses import dataclass, field
import hashlib
import math
import re


TOKEN_RE = re.compile(r"[a-z0-9_./:-]+")


@dataclass
class Chunk:
    chunk_id: str
    text: str
    metadata: dict[str, str] = field(default_factory=dict)


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def embed(text: str, dimensions: int = 96) -> list[float]:
    vector = [0.0] * dimensions
    for token in tokenize(text):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=4).hexdigest()
        index = int(digest, 16) % dimensions
        vector[index] += 1.0

    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    return sum(left * right for left, right in zip(a, b))


def metadata_matches(metadata: dict[str, str], where: dict[str, str] | None) -> bool:
    if where is None:
        return True
    return all(metadata.get(key) == value for key, value in where.items())


class TinyVectorStore:
    def __init__(self) -> None:
        self.chunks: list[Chunk] = []
        self.vectors: dict[str, list[float]] = {}

    def add(self, chunk: Chunk) -> None:
        self.chunks.append(chunk)
        searchable = f"{chunk.metadata.get('title', '')} {chunk.metadata.get('heading_path', '')} {chunk.text}"
        self.vectors[chunk.chunk_id] = embed(searchable)

    def search(self, query: str, top_k: int = 3, where: dict[str, str] | None = None) -> list[tuple[float, Chunk]]:
        query_vector = embed(query)
        scored: list[tuple[float, Chunk]] = []

        for chunk in self.chunks:
            if not metadata_matches(chunk.metadata, where):
                continue
            score = cosine_similarity(query_vector, self.vectors[chunk.chunk_id])
            scored.append((score, chunk))

        return sorted(scored, key=lambda item: item[0], reverse=True)[:top_k]


def seed_store() -> TinyVectorStore:
    store = TinyVectorStore()
    store.add(
        Chunk(
            "ec2-ssh",
            "When SSH to an EC2 instance fails, check security groups, network ACLs, route tables, public IP assignment, and OS firewall rules.",
            {"product": "ec2", "title": "AWS EC2 Guide", "heading_path": "AWS EC2 Guide > Troubleshooting SSH"},
        )
    )
    store.add(
        Chunk(
            "ec2-cost",
            "Idle EC2 instances and unattached EBS volumes can create waste. Use budgets, tags, scheduled stops, and rightsizing.",
            {"product": "ec2", "title": "AWS EC2 Guide", "heading_path": "AWS EC2 Guide > Cost Controls"},
        )
    )
    store.add(
        Chunk(
            "s3-access",
            "S3 AccessDenied errors can come from missing IAM permissions, bucket policy denies, object ownership, or KMS key policy restrictions.",
            {"product": "s3", "title": "AWS S3 Guide", "heading_path": "AWS S3 Guide > AccessDenied"},
        )
    )
    return store


def main() -> None:
    print("\nLab 03: Embeddings and Vector Search (Solution)\n")

    store = seed_store()
    query = "why can I not connect to my instance over ssh?"
    results = store.search(query, top_k=3, where={"product": "ec2"})

    print(f"Query: {query}\n")
    for score, chunk in results:
        print(f"{score:.3f} | {chunk.chunk_id} | {chunk.metadata['heading_path']}")
        print(f"  {chunk.text}")


if __name__ == "__main__":
    main()

