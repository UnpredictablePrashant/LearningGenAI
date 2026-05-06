#!/usr/bin/env python3
"""Demo: long-term memory retrieval with lightweight vector-style search."""

from dataclasses import dataclass, field
import hashlib
import math
import re


TOKEN_RE = re.compile(r"[a-z0-9_]+")


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())


def embed(text: str, dimensions: int = 64) -> list[float]:
    """Create a deterministic toy embedding using hashed token buckets."""
    vector = [0.0] * dimensions
    for token in tokenize(text):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=4).hexdigest()
        index = int(digest, 16) % dimensions
        vector[index] += 1.0

    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(left * right for left, right in zip(a, b))


@dataclass
class MemoryRecord:
    memory_id: str
    kind: str
    text: str
    tags: list[str] = field(default_factory=list)
    confidence: float = 1.0


class LongTermMemory:
    def __init__(self) -> None:
        self.records: list[MemoryRecord] = []
        self.vectors: dict[str, list[float]] = {}

    def add(self, record: MemoryRecord) -> None:
        self.records.append(record)
        searchable_text = f"{record.kind} {' '.join(record.tags)} {record.text}"
        self.vectors[record.memory_id] = embed(searchable_text)

    def search(self, query: str, *, kind: str | None = None, top_k: int = 3) -> list[tuple[float, MemoryRecord]]:
        query_vector = embed(query)
        scored: list[tuple[float, MemoryRecord]] = []

        for record in self.records:
            if kind and record.kind != kind:
                continue
            score = cosine(query_vector, self.vectors[record.memory_id])
            scored.append((score, record))

        return sorted(scored, key=lambda item: item[0], reverse=True)[:top_k]


def seed_memory() -> LongTermMemory:
    memory = LongTermMemory()
    memory.add(
        MemoryRecord(
            memory_id="mem-001",
            kind="user_preference",
            text="User prefers teaching sessions with concept, demo, and lab sections.",
            tags=["teaching", "format"],
            confidence=0.95,
        )
    )
    memory.add(
        MemoryRecord(
            memory_id="mem-002",
            kind="user_preference",
            text="User prefers examples grounded in cloud and DevOps engineering.",
            tags=["teaching", "devops"],
            confidence=0.9,
        )
    )
    memory.add(
        MemoryRecord(
            memory_id="mem-003",
            kind="project_fact",
            text="The course stores every session under sessions/XX_topic_name.",
            tags=["repo", "structure"],
            confidence=1.0,
        )
    )
    memory.add(
        MemoryRecord(
            memory_id="mem-004",
            kind="procedure",
            text="To create a session, write README, concepts, demos, labs, and solutions.",
            tags=["workflow", "session"],
            confidence=0.9,
        )
    )
    return memory


def main() -> None:
    memory = seed_memory()
    query = "teaching format concept demo lab sections"

    print("\nLong-Term Memory Retrieval Demo\n")
    print(f"Query: {query}\n")

    for score, record in memory.search(query, top_k=3):
        print(f"{score:.3f} | {record.kind} | {record.memory_id}")
        print(f"      {record.text}")


if __name__ == "__main__":
    main()
