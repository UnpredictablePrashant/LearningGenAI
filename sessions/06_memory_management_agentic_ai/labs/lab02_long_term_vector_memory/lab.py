#!/usr/bin/env python3
"""
Lab 02: Long-Term Vector Memory
===============================
Build a small long-term memory store with vector-style retrieval.

This lab uses a lightweight hashed embedding so it runs without an API key or
model download. Production systems usually use real embedding models and a
database, but the retrieval flow is the same.

Run:
    python lab.py

When stuck: check solution.py
"""

from dataclasses import dataclass, field
import hashlib
import math
import re


TOKEN_RE = re.compile(r"[a-z0-9_]+")


@dataclass
class MemoryRecord:
    memory_id: str
    kind: str
    text: str
    tags: list[str] = field(default_factory=list)
    confidence: float = 1.0


def tokenize(text: str) -> list[str]:
    # TODO 1:
    # Lowercase the text and return TOKEN_RE matches.
    pass


def embed(text: str, dimensions: int = 64) -> list[float]:
    # TODO 2:
    # Convert text into a deterministic vector:
    # - tokenize text
    # - hash each token with hashlib.blake2b(..., digest_size=4)
    # - map each token to index int(digest, 16) % dimensions
    # - increment that vector bucket
    # - L2 normalize the vector before returning it
    pass


def cosine_similarity(a: list[float], b: list[float]) -> float:
    # TODO 3:
    # Return the dot product of normalized vectors a and b.
    pass


class LongTermMemory:
    def __init__(self) -> None:
        self.records: list[MemoryRecord] = []
        self.vectors: dict[str, list[float]] = {}

    def add(self, record: MemoryRecord) -> None:
        # TODO 4:
        # Store the record and precompute its vector.
        # Include kind and tags in the searchable text so metadata helps search.
        pass

    def search(self, query: str, *, kind: str | None = None, top_k: int = 3) -> list[tuple[float, MemoryRecord]]:
        # TODO 5:
        # Embed the query, score records by cosine similarity, optionally filter
        # by kind, sort highest score first, and return top_k results.
        pass


def seed_memory() -> LongTermMemory:
    memory = LongTermMemory()
    memory.add(
        MemoryRecord(
            memory_id="mem-001",
            kind="user_preference",
            text="User prefers concept-demo-lab structure for teaching sessions.",
            tags=["teaching", "format"],
            confidence=0.95,
        )
    )
    memory.add(
        MemoryRecord(
            memory_id="mem-002",
            kind="project_fact",
            text="Course sessions are stored under sessions/XX_topic_name.",
            tags=["repo", "structure"],
        )
    )
    memory.add(
        MemoryRecord(
            memory_id="mem-003",
            kind="procedure",
            text="Create session materials with README, concepts, demos, labs, and solutions.",
            tags=["workflow", "session"],
        )
    )
    return memory


def main() -> None:
    print("\nLab 02: Long-Term Vector Memory\n")

    memory = seed_memory()
    if not memory.records:
        print("TODO 4 not complete: no records were stored.")
        return

    results = memory.search("How should I create the next teaching session?")
    if results is None:
        print("TODO 5 not complete: search returned None.")
        return

    for score, record in results:
        print(f"{score:.3f} | {record.kind} | {record.text}")


if __name__ == "__main__":
    main()

