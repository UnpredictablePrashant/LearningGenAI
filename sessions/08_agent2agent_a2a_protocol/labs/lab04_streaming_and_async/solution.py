#!/usr/bin/env python3
"""Lab 04: Streaming and Async Task Events (SOLUTION)"""

from datetime import datetime, timezone
import json


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def task_event(task_id: str, state: str, message: str | None = None) -> dict:
    event = {"taskId": task_id, "state": state, "timestamp": now()}
    if message:
        event["message"] = message
    return event


def artifact_delta_event(task_id: str, text: str) -> dict:
    return {"taskId": task_id, "delta": {"type": "text", "text": text}, "timestamp": now()}


def event_sequence(task_id: str) -> list[tuple[str, dict]]:
    return [
        ("task_status", task_event(task_id, "TASK_STATE_SUBMITTED")),
        ("task_status", task_event(task_id, "TASK_STATE_WORKING", "Checking cluster state.")),
        ("artifact_delta", artifact_delta_event(task_id, "Found recent deployment and restart loop.")),
        ("task_status", task_event(task_id, "TASK_STATE_COMPLETED")),
    ]


def to_sse(event_name: str, payload: dict) -> str:
    return f"event: {event_name}\ndata: {json.dumps(payload, sort_keys=True)}\n\n"


def parse_sse(stream_text: str) -> list[tuple[str, dict]]:
    parsed: list[tuple[str, dict]] = []
    for block in stream_text.strip().split("\n\n"):
        event_name = ""
        data = ""
        for line in block.splitlines():
            if line.startswith("event: "):
                event_name = line.removeprefix("event: ").strip()
            elif line.startswith("data: "):
                data = line.removeprefix("data: ").strip()
        if event_name and data:
            parsed.append((event_name, json.loads(data)))
    return parsed


def main() -> None:
    print("\nLab 04: Streaming and Async Task Events (Solution)\n")

    events = event_sequence("task-123")
    stream = "".join(to_sse(name, payload) for name, payload in events)
    parsed = parse_sse(stream)

    print("SSE stream:")
    print(stream)
    print("Parsed events:")
    print(json.dumps(parsed, indent=2))


if __name__ == "__main__":
    main()

