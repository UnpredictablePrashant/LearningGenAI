#!/usr/bin/env python3
"""Lab 03: Episodic and Reflective Memory (SOLUTION)"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import re


TOKEN_RE = re.compile(r"[a-z0-9_]+")


def tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


def overlap_score(left: str, right: str) -> float:
    left_tokens = tokens(left)
    right_tokens = tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


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
        self.episodes.append(episode)

    def find_similar(self, goal: str, top_k: int = 2) -> list[tuple[float, Episode]]:
        scored = [
            (overlap_score(goal, episode.goal), episode)
            for episode in self.episodes
        ]
        return sorted(scored, key=lambda item: item[0], reverse=True)[:top_k]

    def create_reflection(self, episode: Episode) -> Reflection:
        outcome = episode.outcome.lower()
        confidence = 0.8 if "completed" in outcome or "success" in outcome else 0.5
        return Reflection(
            insight=episode.lesson,
            apply_when=f"future tasks similar to: {episode.goal}",
            confidence=confidence,
            source_goal=episode.goal,
        )

    def record_completed_task(self, goal: str, actions: list[str], outcome: str, lesson: str) -> None:
        episode = Episode(goal=goal, actions=actions, outcome=outcome, lesson=lesson)
        self.add_episode(episode)
        self.reflections.append(self.create_reflection(episode))


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
    print("\nLab 03: Episodic and Reflective Memory (Solution)\n")

    store = seed_store()
    similar = store.find_similar("Create a session on memory management for agents")

    print("Similar episodes:")
    for score, episode in similar:
        print(f"{score:.3f} | {episode.goal} | {episode.lesson}")

    store.record_completed_task(
        goal="Create a session on memory management for agents",
        actions=["Defined memory types", "Created labs", "Added demos"],
        outcome="completed",
        lesson="Memory is easiest to teach when separated into type, purpose, and retrieval policy.",
    )

    print("\nLatest reflection:")
    print(store.reflections[-1])


if __name__ == "__main__":
    main()

