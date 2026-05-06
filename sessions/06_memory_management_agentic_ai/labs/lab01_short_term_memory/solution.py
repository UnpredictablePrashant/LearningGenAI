#!/usr/bin/env python3
"""Lab 01: Short-Term Memory (SOLUTION)"""

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
        self.recent_messages.append({"role": role, "content": content})
        self._update_task_state(role, content)
        self._compress_if_needed()

    def _update_task_state(self, role: str, content: str) -> None:
        if role == "user" and content.startswith("Goal:"):
            self.task_state["goal"] = content.replace("Goal:", "", 1).strip()
        elif role == "user" and content.startswith("Constraint:"):
            self.task_state["constraints"].append(
                content.replace("Constraint:", "", 1).strip()
            )
        elif role == "assistant" and content.startswith("Done:"):
            self.task_state["completed"].append(content.replace("Done:", "", 1).strip())

    def _compress_if_needed(self) -> None:
        while len(self.recent_messages) > self.max_recent_messages:
            oldest = self.recent_messages.pop(0)
            self.summary.append(f"{oldest['role']}: {compact(oldest['content'])}")

    def build_prompt_context(self) -> str:
        summary = "\n".join(self.summary) or "(no compressed history)"
        recent = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in self.recent_messages
        )
        return (
            "SUMMARY\n"
            f"{summary}\n\n"
            "TASK STATE\n"
            f"{self.task_state}\n\n"
            "RECENT MESSAGES\n"
            f"{recent}"
        )


def main() -> None:
    print("\nLab 01: Short-Term Memory (Solution)\n")

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

    print(memory.build_prompt_context())


if __name__ == "__main__":
    main()

