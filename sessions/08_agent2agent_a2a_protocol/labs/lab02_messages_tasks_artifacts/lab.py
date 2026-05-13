#!/usr/bin/env python3
"""
Lab 02: Messages, Tasks, and Artifacts
======================================
Build A2A-style messages with typed parts, create a durable task, and complete
it with an artifact.

Run:
    python lab.py

When stuck: check solution.py
"""

from datetime import datetime, timezone
import json
import uuid


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text_part(text: str) -> dict:
    # TODO 1:
    # Return a text part dict.
    pass


def data_part(data: dict) -> dict:
    # TODO 2:
    # Return a structured data part dict.
    pass


def create_message(role: str, parts: list[dict]) -> dict:
    # TODO 3:
    # Return a message with role, parts, and a generated messageId.
    pass


def create_task(message: dict) -> dict:
    # TODO 4:
    # Return a task with generated id/contextId, submitted status, messages,
    # artifacts as empty list, and history containing the submitted status.
    pass


def transition(task: dict, state: str) -> None:
    # TODO 5:
    # Update task["status"] and append to task["history"].
    pass


def complete_task(task: dict, artifact_name: str, artifact_parts: list[dict]) -> dict:
    # TODO 6:
    # Transition to working, add an artifact, transition to completed, return task.
    pass


def main() -> None:
    print("\nLab 02: Messages, Tasks, and Artifacts\n")

    message = create_message(
        "ROLE_USER",
        [
            text_part("Triage this Kubernetes incident."),
            data_part({"service": "payments", "symptom": "CrashLoopBackOff"}),
        ],
    )
    if message is None:
        print("TODO 3 not complete: create_message returned None.")
        return

    task = create_task(message)
    if task is None:
        print("TODO 4 not complete: create_task returned None.")
        return

    complete_task(
        task,
        "incident_triage_summary",
        [
            text_part("Check previous pod logs, deployment config, secrets, and memory limits."),
            data_part({"next_action": "kubectl logs --previous", "confidence": 0.8}),
        ],
    )

    print(json.dumps(task, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

