#!/usr/bin/env python3
"""Demo: a teaching agent that uses several memory types."""

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
    created_at: str


@dataclass
class TeachingMemory:
    preferences: list[str] = field(default_factory=list)
    procedures: dict[str, list[str]] = field(default_factory=dict)
    episodes: list[Episode] = field(default_factory=list)
    reflections: list[str] = field(default_factory=list)

    def similar_episode(self, topic: str) -> Episode | None:
        if not self.episodes:
            return None
        return max(self.episodes, key=lambda episode: overlap_score(topic, episode.goal))


class MemoryAwareTeachingAgent:
    def __init__(self, memory: TeachingMemory) -> None:
        self.memory = memory

    def create_session(self, topic: str) -> dict:
        procedure = self.memory.procedures["create_teaching_session"]
        previous = self.memory.similar_episode(topic)

        plan = {
            "topic": topic,
            "preferences_used": self.memory.preferences,
            "procedure_used": procedure,
            "previous_episode": previous.goal if previous else None,
            "session_sections": [
                "README with objectives, prerequisites, quick start, and timing",
                "Concept notes with DevOps analogies",
                "Runnable demos",
                "TODO-based labs",
                "Reference solutions",
            ],
        }

        self.memory.episodes.append(
            Episode(
                goal=f"Create teaching session on {topic}",
                actions=plan["session_sections"],
                outcome="draft plan created",
                lesson="Use existing course structure before inventing new materials.",
                created_at=datetime.now(timezone.utc).isoformat(),
            )
        )
        self.memory.reflections.append(
            "For future teaching-session tasks, inspect nearby session folders first."
        )
        return plan


def seed_memory() -> TeachingMemory:
    return TeachingMemory(
        preferences=[
            "Use concept, demo, and lab structure.",
            "Use DevOps analogies for cloud engineers.",
            "Prefer runnable Python scripts over notebooks.",
        ],
        procedures={
            "create_teaching_session": [
                "Read existing session structure",
                "Write README",
                "Write concept docs",
                "Add demos",
                "Add lab skeletons",
                "Add solutions",
                "Run verification",
            ]
        },
        episodes=[
            Episode(
                goal="Create teaching session on MCP servers",
                actions=["Wrote concepts", "Built FastMCP labs", "Added demos"],
                outcome="completed",
                lesson="Compare new agent concepts to earlier sessions.",
                created_at="2026-05-01T10:00:00Z",
            )
        ],
        reflections=[
            "Start new topics with a DevOps analogy before theory.",
        ],
    )


def main() -> None:
    agent = MemoryAwareTeachingAgent(seed_memory())
    plan = agent.create_session("Memory Management in Agentic AI")

    print("\nMemory-Aware Teaching Agent Demo\n")
    for key, value in plan.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()

