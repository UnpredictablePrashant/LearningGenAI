#!/usr/bin/env python3
"""
Lab 04: Streaming and Async Task Events
======================================
Create task status events, format them as Server-Sent Events (SSE), and parse
them back.

Run:
    python lab.py

When stuck: check solution.py
"""

from datetime import datetime, timezone
import json


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def task_event(task_id: str, state: str, message: str | None = None) -> dict:
    # TODO 1:
    # Return a task status event dict with taskId, state, timestamp, and optional message.
    pass


def artifact_delta_event(task_id: str, text: str) -> dict:
    # TODO 2:
    # Return an artifact delta event dict with taskId, delta type, and text.
    pass


def event_sequence(task_id: str) -> list[tuple[str, dict]]:
    # TODO 3:
    # Return a sequence of (event_name, payload) tuples:
    # task_status submitted, task_status working, artifact_delta, task_status completed.
    pass


def to_sse(event_name: str, payload: dict) -> str:
    # TODO 4:
    # Format one event as:
    # event: <event_name>
    # data: <json payload>
    #
    pass


def parse_sse(stream_text: str) -> list[tuple[str, dict]]:
    # TODO 5:
    # Parse SSE blocks produced by to_sse back into (event_name, payload).
    pass


def main() -> None:
    print("\nLab 04: Streaming and Async Task Events\n")

    events = event_sequence("task-123")
    if events is None:
        print("TODO 3 not complete: event_sequence returned None.")
        return

    stream = "".join(to_sse(name, payload) for name, payload in events)
    parsed = parse_sse(stream)

    print("SSE stream:")
    print(stream)
    print("Parsed events:")
    print(json.dumps(parsed, indent=2))


if __name__ == "__main__":
    main()

