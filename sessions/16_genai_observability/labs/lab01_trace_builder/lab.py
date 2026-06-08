#!/usr/bin/env python3
"""
Lab 01: Trace Builder
=====================
Build a redacted GenAI trace record with model, retrieval, and tool spans.

Run:
    python lab.py

When stuck: check solution.py
"""

from datetime import datetime, timezone
import json
import uuid


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def redact(text: str) -> str:
    # TODO 1:
    # Replace obvious secret markers "sk-" and "password=" with "[REDACTED]".
    pass


def make_span(name: str, attributes: dict, events: list[dict] | None = None) -> dict:
    # TODO 2:
    # Return a span dict with id, name, time, attributes, and events.
    pass


def build_trace() -> dict:
    # TODO 3:
    # Return a trace with one retrieval span, one model span, and one tool span.
    # Include token usage on the model span.
    pass


def main() -> None:
    print("\nLab 01: Trace Builder\n")

    trace = build_trace()
    if trace is None:
        print("TODO 3 not complete: build_trace returned None.")
        return
    print(json.dumps(trace, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

