#!/usr/bin/env python3
"""
Lab 03: Episodic and Reflective Memory
======================================
Store agent runs as episodes, then convert completed episodes into reflections.

Key insight:
- Episodic memory records what happened.
- Reflective memory records what should be learned from what happened.

Run:
    python lab.py

When stuck: check solution.py
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re


TOKEN_RE = re.compile(r"[a-z0-9_]+")


def tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


def overlap_score(left: str, right: str) -> float:
    # TODO 1:
    # Return Jaccard overlap between token sets:
    # len(intersection) / len(union)
    # Return 0.0 if either side is empty.
    pass


@dataclass
class Episode:
    goal: str
    actions: list[str]
    outcome: str
    lesson: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Reflection:
    insight: str
    apply_when: str
    confidence: float
    source_goal: str


class EpisodeStore:
    def __init__(self) -> None:
        self.episodes: list[Episode] = []
        self.reflections: list[Reflection] = []

    def add_episode(self, episode: Episode) -> None:
        # TODO 2:
        # Append the episode to self.episodes.
        pass

    def find_similar(self, goal: str, top_k: int = 2) -> list[tuple[float, Episode]]:
        # TODO 3:
        # Score each episode against the incoming goal using overlap_score.
        # Sort highest first and return top_k.
        pass

    def create_reflection(self, episode: Episode) -> Reflection:
        # TODO 4:
        # Create a Reflection from the episode.
        # Use episode.lesson as the insight.
        # Use "future tasks similar to: <episode.goal>" as apply_when.
        # Use confidence 0.8 for completed/successful outcomes, otherwise 0.5.
        pass

    def record_completed_task(self, goal: str, actions: list[str], outcome: str, lesson: str) -> None:
        # TODO 5:
        # Create an Episode, add it, create a Reflection from it, and store
        # the reflection in self.reflections.
        pass


def seed_store() -> EpisodeStore:
    store = EpisodeStore()
    store.add_episode(
        Episode(
            goal="Create a session on MCP servers",
            actions=["Compared MCP with function calling", "Built FastMCP labs"],
            outcome="completed",
            lesson="Use previous session knowledge as a bridge to the new topic.",
        )
    )
    store.add_episode(
        Episode(
            goal="Create a session on tool calling",
            actions=["Explained schemas", "Built single-tool and multi-tool loops"],
            outcome="completed",
            lesson="Students understand tools faster when schemas are treated as API contracts.",
        )
    )
    return store


def main() -> None:
    print("\nLab 03: Episodic and Reflective Memory\n")

    store = seed_store()
    if not store.episodes:
        print("TODO 2 not complete: seed episodes were not stored.")
        return

    similar = store.find_similar("Create a session on memory management for agents")
    if similar is None:
        print("TODO 3 not complete: find_similar returned None.")
        return

    print("Similar episodes:")
    for score, episode in similar:
        print(f"{score:.3f} | {episode.goal} | {episode.lesson}")

    store.record_completed_task(
        goal="Create a session on memory management for agents",
        actions=["Defined memory types", "Created labs", "Added demos"],
        outcome="completed",
        lesson="Memory is easiest to teach when separated into type, purpose, and retrieval policy.",
    )

    if not store.reflections:
        print("\nTODO 5 not complete: no reflections were stored.")
        return

    print("\nLatest reflection:")
    print(store.reflections[-1])


if __name__ == "__main__":
    main()

