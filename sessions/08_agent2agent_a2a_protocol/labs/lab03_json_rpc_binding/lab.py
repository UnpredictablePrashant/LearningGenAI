#!/usr/bin/env python3
"""
Lab 03: JSON-RPC Binding
========================
Implement a small JSON-RPC dispatcher for A2A-style methods:
SendMessage, GetTask, and CancelTask.

Run:
    python lab.py

When stuck: check solution.py
"""

from datetime import datetime, timezone
import json
import uuid


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class MiniA2AServer:
    def __init__(self) -> None:
        self.tasks: dict[str, dict] = {}

    def send_message(self, params: dict) -> dict:
        # TODO 1:
        # Validate params contains "message".
        # Create a completed task with one text artifact.
        # Store it in self.tasks and return {"task": task}.
        pass

    def get_task(self, params: dict) -> dict:
        # TODO 2:
        # Return {"task": task} for params["id"], or raise KeyError if missing.
        pass

    def cancel_task(self, params: dict) -> dict:
        # TODO 3:
        # If task missing, raise KeyError.
        # If task completed, raise ValueError("TaskNotCancelableError").
        # Otherwise set state to TASK_STATE_CANCELED and return {"task": task}.
        pass


def success_response(request_id: str | int | None, result: dict) -> dict:
    # TODO 4:
    # Return JSON-RPC success envelope.
    pass


def error_response(request_id: str | int | None, code: int, message: str) -> dict:
    # TODO 5:
    # Return JSON-RPC error envelope.
    pass


def dispatch(server: MiniA2AServer, request: dict) -> dict:
    # TODO 6:
    # Validate jsonrpc == "2.0".
    # Dispatch methods: SendMessage, GetTask, CancelTask.
    # Map:
    # - unknown method -> -32601
    # - invalid params -> -32602
    # - task not found -> -32001
    # - not cancelable -> -32002
    pass


def main() -> None:
    print("\nLab 03: JSON-RPC Binding\n")

    server = MiniA2AServer()
    send_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "SendMessage",
        "params": {
            "message": {
                "role": "ROLE_USER",
                "parts": [{"text": "Triage incident INC-1001"}],
                "messageId": "msg-001",
            }
        },
    }

    send_response = dispatch(server, send_request)
    if send_response is None:
        print("TODO 6 not complete: dispatch returned None.")
        return

    task_id = send_response.get("result", {}).get("task", {}).get("id")
    get_response = dispatch(server, {"jsonrpc": "2.0", "id": 2, "method": "GetTask", "params": {"id": task_id}})
    cancel_response = dispatch(server, {"jsonrpc": "2.0", "id": 3, "method": "CancelTask", "params": {"id": task_id}})

    print("SendMessage response:")
    print(json.dumps(send_response, indent=2, sort_keys=True))
    print("\nGetTask response:")
    print(json.dumps(get_response, indent=2, sort_keys=True))
    print("\nCancelTask response:")
    print(json.dumps(cancel_response, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

