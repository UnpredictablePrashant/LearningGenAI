#!/usr/bin/env python3
"""Lab 04: Memory-Aware Teaching Agent (SOLUTION)"""

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
    outcome: str
    lesson: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class TeachingMemory:
    short_term_task: dict = field(default_factory=dict)
    long_term_preferences: list[str] = field(default_factory=list)
    procedures: dict[str, list[str]] = field(default_factory=dict)
    episodes: list[Episode] = field(default_factory=list)
    reflections: list[str] = field(default_factory=list)


class TeachingAgent:
    def __init__(self, memory: TeachingMemory) -> None:
        self.memory = memory

    def select_relevant_preferences(self, request: str) -> list[str]:
        selected = [
            preference
            for preference in self.memory.long_term_preferences
            if "teaching" in preference.lower() or overlap_score(request, preference) > 0
        ]
        return selected

    def get_procedure(self, procedure_name: str) -> list[str]:
        return self.memory.procedures.get(procedure_name, [])

    def find_similar_episode(self, request: str) -> Episode | None:
        if not self.memory.episodes:
            return None
        return max(
            self.memory.episodes,
            key=lambda episode: overlap_score(request, episode.goal),
        )

    def select_reflections(self, request: str) -> list[str]:
        selected = [
            reflection
            for reflection in self.memory.reflections
            if overlap_score(request, reflection) > 0
        ]
        if selected:
            return selected
        return self.memory.reflections[:1]

    def create_session_plan(self, request: str) -> dict:
        similar = self.find_similar_episode(request)
        return {
            "request": request,
            "short_term_task": self.memory.short_term_task,
            "preferences": self.select_relevant_preferences(request),
            "procedure": self.get_procedure("create_teaching_session"),
            "similar_episode": similar.goal if similar else None,
            "reflections": self.select_reflections(request),
            "deliverables": [
                "README.md",
                "concepts/01_why_agents_need_memory.md",
                "concepts/02_short_term_working_memory.md",
                "concepts/03_long_term_semantic_memory.md",
                "concepts/04_episodic_and_reflective_memory.md",
                "concepts/05_procedural_memory_and_governance.md",
                "demos/*.py",
                "labs/*/lab.py",
                "labs/*/solution.py",
            ],
        }

    def store_episode_and_reflection(self, request: str, plan: dict) -> None:
        self.memory.episodes.append(
            Episode(
                goal=request,
                outcome="planned",
                lesson="A memory-aware teaching agent should retrieve preferences, procedures, episodes, and reflections before drafting.",
            )
        )
        self.memory.reflections.append(
            "For future session planning, assemble memory context before generating deliverables."
        )


def seed_memory() -> TeachingMemory:
    return TeachingMemory(
        short_term_task={
            "current_goal": "Create Session 06 on memory management",
            "latest_constraint": "Follow the existing session structure",
        },
        long_term_preferences=[
            "Use concept, demo, and lab structure for teaching sessions.",
            "Use DevOps analogies for cloud engineers.",
            "Prefer runnable Python scripts over notebooks.",
        ],
        procedures={
            "create_teaching_session": [
                "Inspect existing session structure",
                "Write README with objectives and quick start",
                "Write concept docs",
                "Add runnable demos",
                "Add TODO-based labs",
                "Add reference solutions",
                "Run syntax checks",
            ]
        },
        episodes=[
            Episode(
                goal="Create a session on MCP servers",
                outcome="completed",
                lesson="Connect the new topic to the previous session before introducing new abstractions.",
            )
        ],
        reflections=[
            "Start new Agentic AI sessions with a practical DevOps analogy.",
        ],
    )


def main() -> None:
    print("\nLab 04: Memory-Aware Teaching Agent (Solution)\n")

    request = "Create a session on Memory Management in Agentic AI."
    agent = TeachingAgent(seed_memory())
    plan = agent.create_session_plan(request)
    agent.store_episode_and_reflection(request, plan)

    print("Plan:")
    for key, value in plan.items():
        print(f"{key}: {value}")

    print("\nStored episode count:", len(agent.memory.episodes))
    print("Stored reflection count:", len(agent.memory.reflections))


if __name__ == "__main__":
    main()

