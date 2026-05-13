#!/usr/bin/env python3
"""Lab 02: Messages, Tasks, and Artifacts (SOLUTION)"""

from datetime import datetime, timezone
import json
import uuid


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def text_part(text: str) -> dict:
    return {"text": text}


def data_part(data: dict) -> dict:
    return {"data": data}


def create_message(role: str, parts: list[dict]) -> dict:
    return {
        "role": role,
        "parts": parts,
        "messageId": f"msg-{uuid.uuid4()}",
    }


def create_task(message: dict) -> dict:
    status = {"state": "TASK_STATE_SUBMITTED", "timestamp": now()}
    return {
        "id": f"task-{uuid.uuid4()}",
        "contextId": f"ctx-{uuid.uuid4()}",
        "status": status,
        "messages": [message],
        "artifacts": [],
        "history": [status],
    }


def transition(task: dict, state: str) -> None:
    status = {"state": state, "timestamp": now()}
    task["status"] = status
    task.setdefault("history", []).append(status)


def complete_task(task: dict, artifact_name: str, artifact_parts: list[dict]) -> dict:
    transition(task, "TASK_STATE_WORKING")
    task.setdefault("artifacts", []).append(
        {
            "artifactId": f"artifact-{uuid.uuid4()}",
            "name": artifact_name,
            "parts": artifact_parts,
        }
    )
    transition(task, "TASK_STATE_COMPLETED")
    return task


def main() -> None:
    print("\nLab 02: Messages, Tasks, and Artifacts (Solution)\n")

    message = create_message(
        "ROLE_USER",
        [
            text_part("Triage this Kubernetes incident."),
            data_part({"service": "payments", "symptom": "CrashLoopBackOff"}),
        ],
    )
    task = create_task(message)
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

