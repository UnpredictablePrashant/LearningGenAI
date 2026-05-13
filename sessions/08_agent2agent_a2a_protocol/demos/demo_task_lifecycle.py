#!/usr/bin/env python3
"""
Demo: A2A Task Lifecycle
========================
Simulate SendMessage, GetTask, and CancelTask behavior with durable task state.

No API key required. Uses Python standard library only.

Run:
    python demos/demo_task_lifecycle.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import uuid


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Message:
    role: str
    parts: list[dict]
    message_id: str = field(default_factory=lambda: f"msg-{uuid.uuid4()}")


@dataclass
class Artifact:
    artifact_id: str
    name: str
    parts: list[dict]


@dataclass
class Task:
    task_id: str
    context_id: str
    status: dict
    messages: list[Message] = field(default_factory=list)
    artifacts: list[Artifact] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)

    def transition(self, state: str) -> None:
        event = {"state": state, "timestamp": now()}
        self.status = event
        self.history.append(event)


class IncidentAgent:
    def __init__(self) -> None:
        self.tasks: dict[str, Task] = {}

    def send_message(self, message: Message) -> Task:
        task = Task(
            task_id=f"task-{uuid.uuid4()}",
            context_id=f"ctx-{uuid.uuid4()}",
            status={"state": "TASK_STATE_SUBMITTED", "timestamp": now()},
            messages=[message],
            history=[],
        )
        task.history.append(task.status)
        self.tasks[task.task_id] = task

        task.transition("TASK_STATE_WORKING")
        task.artifacts.append(
            Artifact(
                artifact_id=f"artifact-{uuid.uuid4()}",
                name="incident_triage_summary",
                parts=[
                    {
                        "text": "Likely checks: previous pod logs, recent deployment, missing secrets, and memory limits."
                    },
                    {
                        "data": {
                            "recommended_commands": [
                                "kubectl logs deploy/payments --previous",
                                "kubectl describe pod -l app=payments",
                                "kubectl get events --sort-by=.lastTimestamp",
                            ]
                        }
                    },
                ],
            )
        )
        task.transition("TASK_STATE_COMPLETED")
        return task

    def get_task(self, task_id: str) -> Task | None:
        return self.tasks.get(task_id)

    def cancel_task(self, task_id: str) -> dict:
        task = self.tasks.get(task_id)
        if task is None:
            return {"error": "TaskNotFoundError", "message": "Task does not exist or is not visible."}
        if task.status["state"] == "TASK_STATE_COMPLETED":
            return {"error": "TaskNotCancelableError", "message": "Completed tasks cannot be canceled."}
        task.transition("TASK_STATE_CANCELED")
        return {"task": to_a2a_task(task)}


def to_a2a_message(message: Message) -> dict:
    return {
        "role": message.role,
        "parts": message.parts,
        "messageId": message.message_id,
    }


def to_a2a_artifact(artifact: Artifact) -> dict:
    return {
        "artifactId": artifact.artifact_id,
        "name": artifact.name,
        "parts": artifact.parts,
    }


def to_a2a_task(task: Task) -> dict:
    return {
        "id": task.task_id,
        "contextId": task.context_id,
        "status": task.status,
        "messages": [to_a2a_message(message) for message in task.messages],
        "artifacts": [to_a2a_artifact(artifact) for artifact in task.artifacts],
        "history": task.history,
    }


def main() -> None:
    print("\nDemo: A2A Task Lifecycle\n")

    agent = IncidentAgent()
    message = Message(
        role="ROLE_USER",
        parts=[
            {"text": "Triage this incident: payments deployment is in CrashLoopBackOff."},
            {"data": {"service": "payments", "namespace": "prod", "symptom": "CrashLoopBackOff"}},
        ],
    )

    task = agent.send_message(message)
    fetched = agent.get_task(task.task_id)
    cancel_result = agent.cancel_task(task.task_id)

    print("Created task:")
    print(json.dumps(to_a2a_task(task), indent=2))

    print("\nFetched task status:")
    print(json.dumps(fetched.status if fetched else None, indent=2))

    print("\nCancel completed task:")
    print(json.dumps(cancel_result, indent=2))


if __name__ == "__main__":
    main()
