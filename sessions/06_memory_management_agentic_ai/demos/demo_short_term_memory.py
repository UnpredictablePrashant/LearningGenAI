#!/usr/bin/env python3
"""Demo: short-term memory with a rolling buffer and task state."""

from dataclasses import dataclass, field


def compact(text: str, max_words: int = 14) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."


@dataclass
class WorkingMemory:
    """A small working memory object for the current task."""

    max_recent_messages: int = 4
    summary: list[str] = field(default_factory=list)
    recent_messages: list[dict] = field(default_factory=list)
    task_state: dict = field(
        default_factory=lambda: {
            "goal": None,
            "preferences": [],
            "completed": [],
            "open_questions": [],
        }
    )

    def add_message(self, role: str, content: str) -> None:
        self.recent_messages.append({"role": role, "content": content})
        self._update_task_state(role, content)
        self._compress_if_needed()

    def _update_task_state(self, role: str, content: str) -> None:
        text = content.lower()

        if role == "user" and "session on" in text:
            self.task_state["goal"] = content

        if "prefer" in text or "should follow" in text:
            self.task_state["preferences"].append(compact(content))

        if content.startswith("DONE:"):
            self.task_state["completed"].append(content.replace("DONE:", "").strip())

        if "?" in content:
            self.task_state["open_questions"].append(compact(content))

    def _compress_if_needed(self) -> None:
        while len(self.recent_messages) > self.max_recent_messages:
            old = self.recent_messages.pop(0)
            self.summary.append(f"{old['role']}: {compact(old['content'])}")

    def prompt_context(self) -> str:
        recent = "\n".join(
            f"{message['role']}: {message['content']}" for message in self.recent_messages
        )
        summary = "\n".join(self.summary[-5:]) or "(no compressed history yet)"
        return (
            "WORKING SUMMARY\n"
            f"{summary}\n\n"
            "TASK STATE\n"
            f"{self.task_state}\n\n"
            "RECENT MESSAGES\n"
            f"{recent}"
        )


def main() -> None:
    memory = WorkingMemory(max_recent_messages=4)

    conversation = [
        ("user", "Create the next session on Memory Management in Agentic AI."),
        ("assistant", "DONE: created initial outline with memory types."),
        ("user", "It should follow the same structure as the other sessions."),
        ("assistant", "DONE: checked existing session layout."),
        ("user", "Include short term, long term, episodic, reflective, and procedural memory."),
        ("assistant", "DONE: mapped memory types to concepts, demos, and labs."),
    ]

    for role, content in conversation:
        memory.add_message(role, content)

    print("\nShort-Term Memory Demo\n")
    print(memory.prompt_context())


if __name__ == "__main__":
    main()

