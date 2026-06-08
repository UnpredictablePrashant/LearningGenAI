#!/usr/bin/env python3
"""Lab 01: Realtime Event Flow (SOLUTION)"""


EVENTS = [
    {"type": "audio.started"},
    {"type": "transcript.delta", "text": "check pay"},
    {"type": "transcript.delta", "text": "ment errors"},
    {"type": "transcript.final", "text": "check payment errors"},
    {"type": "tool.requested", "name": "read_logs", "args": {"service": "payment-api"}},
    {"type": "tool.completed", "name": "read_logs", "result": "503 spike at 14:05"},
    {"type": "response.completed", "text": "Payment errors spiked at 14:05."},
]


def initial_state() -> dict:
    return {"partial_transcript": "", "final_transcript": "", "tools": [], "response": ""}


def handle_event(state: dict, event: dict) -> None:
    event_type = event["type"]
    if event_type == "transcript.delta":
        state["partial_transcript"] += event["text"]
    elif event_type == "transcript.final":
        state["final_transcript"] = event["text"]
        state["partial_transcript"] = ""
    elif event_type in {"tool.requested", "tool.completed"}:
        state["tools"].append(event)
    elif event_type == "response.completed":
        state["response"] = event["text"]


def can_execute_tool(event: dict) -> bool:
    return event.get("name", "").startswith("read_")


def main() -> None:
    print("\nLab 01: Realtime Event Flow (Solution)\n")

    state = initial_state()
    for event in EVENTS:
        if event["type"] == "tool.requested" and not can_execute_tool(event):
            print("Tool blocked:", event["name"])
            continue
        handle_event(state, event)

    print(state)


if __name__ == "__main__":
    main()

