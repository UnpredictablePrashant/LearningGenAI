#!/usr/bin/env python3
"""
Lab 04: Memory-Aware Teaching Agent
===================================
Capstone lab: combine short-term, long-term, episodic, reflective, and
procedural memory into one small agent.

The agent does not call an LLM. Instead, you implement the memory decisions an
agent would make before prompting a model.

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
        # TODO 1:
        # Return preferences that overlap with the request OR contain "teaching".
        # Use overlap_score for the request comparison.
        pass

    def get_procedure(self, procedure_name: str) -> list[str]:
        # TODO 2:
        # Return the requested procedure from memory.
        # If missing, return an empty list.
        pass

    def find_similar_episode(self, request: str) -> Episode | None:
        # TODO 3:
        # Return the episode with the highest overlap against the request.
        # Return None if there are no episodes.
        pass

    def select_reflections(self, request: str) -> list[str]:
        # TODO 4:
        # Return reflections that overlap with the request.
        # If none match, return at most the first reflection as a default hint.
        pass

    def create_session_plan(self, request: str) -> dict:
        # TODO 5:
        # Build and return a plan dict with these keys:
        # - request
        # - short_term_task
        # - preferences
        # - procedure
        # - similar_episode
        # - reflections
        # - deliverables
        #
        # Use the other methods in this class. Deliverables should include:
        # README, concepts, demos, labs, and solutions.
        pass

    def store_episode_and_reflection(self, request: str, plan: dict) -> None:
        # TODO 6:
        # Append a new Episode to memory.episodes and a new reflection to
        # memory.reflections after creating the plan.
        pass


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
    print("\nLab 04: Memory-Aware Teaching Agent\n")

    request = "Create a session on Memory Management in Agentic AI."
    agent = TeachingAgent(seed_memory())
    plan = agent.create_session_plan(request)

    if plan is None:
        print("TODO 5 not complete: create_session_plan returned None.")
        return

    agent.store_episode_and_reflection(request, plan)

    if len(agent.memory.episodes) < 2 or len(agent.memory.reflections) < 2:
        print("TODO 6 not complete: episode and reflection were not stored.")
        return

    print("Plan:")
    for key, value in plan.items():
        print(f"{key}: {value}")

    print("\nStored episode count:", len(agent.memory.episodes))
    print("Stored reflection count:", len(agent.memory.reflections))


if __name__ == "__main__":
    main()
