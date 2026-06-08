#!/usr/bin/env python3
"""
Lab 01: Realtime Event Flow
===========================
Process transcript deltas, final transcripts, and tool requests.

Run:
    python lab.py

When stuck: check solution.py
"""


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
    # TODO 1:
    # Return state with partial_transcript, final_transcript, tools, and response.
    pass


def handle_event(state: dict, event: dict) -> None:
    # TODO 2:
    # Update state based on event type.
    # Deltas append to partial_transcript.
    # Final transcript sets final_transcript and clears partial_transcript.
    # Tool events append to tools.
    # Response completed sets response.
    pass


def can_execute_tool(event: dict) -> bool:
    # TODO 3:
    # Return True for read_* tools.
    # Return False for write/restart/delete tools.
    pass


def main() -> None:
    print("\nLab 01: Realtime Event Flow\n")

    state = initial_state()
    if state is None:
        print("TODO 1 not complete: initial_state returned None.")
        return

    for event in EVENTS:
        if event["type"] == "tool.requested" and not can_execute_tool(event):
            print("Tool blocked:", event["name"])
            continue
        handle_event(state, event)

    print(state)


if __name__ == "__main__":
    main()

