#!/usr/bin/env python3
"""
Lab 01: Short-Term Memory
=========================
Build a rolling working memory object for an agent.

Key insight: short-term memory is not "store every message forever".
It is the small, curated working set the agent needs for the current task.

Run:
    python lab.py

When stuck: check solution.py
"""

from dataclasses import dataclass, field


def compact(text: str, max_words: int = 12) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."


@dataclass
class ShortTermMemory:
    max_recent_messages: int = 4
    summary: list[str] = field(default_factory=list)
    recent_messages: list[dict] = field(default_factory=list)
    task_state: dict = field(
        default_factory=lambda: {
            "goal": None,
            "constraints": [],
            "completed": [],
        }
    )

    def add_message(self, role: str, content: str) -> None:
        # TODO 1:
        # Append a message dict to recent_messages.
        # Shape: {"role": role, "content": content}
        #
        # TODO 2:
        # Call _update_task_state(role, content), then _compress_if_needed().
        pass

    def _update_task_state(self, role: str, content: str) -> None:
        # TODO 3:
        # Update task_state using simple rules:
        # - If a user message starts with "Goal:", store the rest as task_state["goal"].
        # - If a user message starts with "Constraint:", append the rest to "constraints".
        # - If an assistant message starts with "Done:", append the rest to "completed".
        pass

    def _compress_if_needed(self) -> None:
        # TODO 4:
        # While recent_messages is longer than max_recent_messages:
        # - pop the oldest message
        # - append a compact summary line to summary, like "user: Goal: ..."
        pass

    def build_prompt_context(self) -> str:
        # TODO 5:
        # Return a string with three sections:
        # - SUMMARY
        # - TASK STATE
        # - RECENT MESSAGES
        #
        # Keep the output readable. This is the context an agent would inject
        # into a prompt before the latest user request.
        pass


def main() -> None:
    print("\nLab 01: Short-Term Memory\n")

    memory = ShortTermMemory(max_recent_messages=3)
    turns = [
        ("user", "Goal: Create a session on Memory Management in Agentic AI."),
        ("user", "Constraint: Follow the same structure as previous sessions."),
        ("assistant", "Done: inspected existing README, concepts, demos, and labs."),
        ("user", "Constraint: Include short-term and long-term memory."),
        ("assistant", "Done: drafted the concept map."),
    ]

    for role, content in turns:
        memory.add_message(role, content)

    if not memory.recent_messages:
        print("TODO 1 not complete: no recent messages were stored.")
        return

    context = memory.build_prompt_context()
    if context is None:
        print("TODO 5 not complete: build_prompt_context returned None.")
        return

    print(context)


if __name__ == "__main__":
    main()

