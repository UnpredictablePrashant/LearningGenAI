#!/usr/bin/env python3
"""
Lab 03: Embeddings and Vector Search
====================================
Build a tiny vector store with deterministic toy embeddings.

Production RAG uses real embedding models and vector databases. This lab keeps
the math visible: tokenize, embed, normalize, cosine search, and metadata filter.

Run:
    python lab.py

When stuck: check solution.py
"""

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
    # TODO 1:
    # Lowercase text and return TOKEN_RE matches.
    pass


def embed(text: str, dimensions: int = 96) -> list[float]:
    # TODO 2:
    # Create a deterministic normalized vector:
    # - tokenize text
    # - hash each token with hashlib.blake2b(..., digest_size=4)
    # - map hash to a vector index with modulo dimensions
    # - increment that bucket
    # - L2 normalize the vector
    pass


def cosine_similarity(a: list[float], b: list[float]) -> float:
    # TODO 3:
    # Return dot product. Vectors are normalized, so this is cosine similarity.
    pass


def metadata_matches(metadata: dict[str, str], where: dict[str, str] | None) -> bool:
    # TODO 4:
    # Return True when where is None or every key/value in where matches metadata.
    pass


class TinyVectorStore:
    def __init__(self) -> None:
        self.chunks: list[Chunk] = []
        self.vectors: dict[str, list[float]] = {}

    def add(self, chunk: Chunk) -> None:
        # TODO 5:
        # Store the chunk and precompute its vector.
        # Include title and heading_path metadata in the embedded text.
        pass

    def search(self, query: str, top_k: int = 3, where: dict[str, str] | None = None) -> list[tuple[float, Chunk]]:
        # TODO 6:
        # Embed the query, score matching chunks, sort highest first, return top_k.
        pass


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
    print("\nLab 03: Embeddings and Vector Search\n")

    store = seed_store()
    if not store.chunks:
        print("TODO 5 not complete: no chunks stored.")
        return

    query = "why can I not connect to my instance over ssh?"
    results = store.search(query, top_k=3, where={"product": "ec2"})
    if results is None:
        print("TODO 6 not complete: search returned None.")
        return

    print(f"Query: {query}\n")
    for score, chunk in results:
        print(f"{score:.3f} | {chunk.chunk_id} | {chunk.metadata['heading_path']}")
        print(f"  {chunk.text}")


if __name__ == "__main__":
    main()

