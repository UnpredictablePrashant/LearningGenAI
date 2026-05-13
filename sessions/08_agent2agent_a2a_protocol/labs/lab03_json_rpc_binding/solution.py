#!/usr/bin/env python3
"""Lab 03: JSON-RPC Binding (SOLUTION)"""

from datetime import datetime, timezone
import json
import uuid


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class MiniA2AServer:
    def __init__(self) -> None:
        self.tasks: dict[str, dict] = {}

    def send_message(self, params: dict) -> dict:
        if "message" not in params:
            raise ValueError("message is required")

        task_id = f"task-{uuid.uuid4()}"
        task = {
            "id": task_id,
            "contextId": f"ctx-{uuid.uuid4()}",
            "status": {"state": "TASK_STATE_COMPLETED", "timestamp": now()},
            "messages": [params["message"]],
            "artifacts": [
                {
                    "artifactId": f"artifact-{uuid.uuid4()}",
                    "name": "summary",
                    "parts": [{"text": "Incident accepted and triaged by mini A2A server."}],
                }
            ],
        }
        self.tasks[task_id] = task
        return {"task": task}

    def get_task(self, params: dict) -> dict:
        task_id = params["id"]
        if task_id not in self.tasks:
            raise KeyError(task_id)
        return {"task": self.tasks[task_id]}

    def cancel_task(self, params: dict) -> dict:
        task_id = params["id"]
        if task_id not in self.tasks:
            raise KeyError(task_id)
        task = self.tasks[task_id]
        if task["status"]["state"] == "TASK_STATE_COMPLETED":
            raise ValueError("TaskNotCancelableError")
        task["status"] = {"state": "TASK_STATE_CANCELED", "timestamp": now()}
        return {"task": task}


def success_response(request_id: str | int | None, result: dict) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def error_response(request_id: str | int | None, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def dispatch(server: MiniA2AServer, request: dict) -> dict:
    request_id = request.get("id")
    if request.get("jsonrpc") != "2.0":
        return error_response(request_id, -32600, "Invalid JSON-RPC request")

    method = request.get("method")
    params = request.get("params", {})

    try:
        if method == "SendMessage":
            return success_response(request_id, server.send_message(params))
        if method == "GetTask":
            return success_response(request_id, server.get_task(params))
        if method == "CancelTask":
            return success_response(request_id, server.cancel_task(params))
        return error_response(request_id, -32601, "Method not found")
    except KeyError:
        return error_response(request_id, -32001, "TaskNotFoundError")
    except ValueError as exc:
        if str(exc) == "TaskNotCancelableError":
            return error_response(request_id, -32002, "TaskNotCancelableError")
        return error_response(request_id, -32602, str(exc))


def main() -> None:
    print("\nLab 03: JSON-RPC Binding (Solution)\n")

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
    task_id = send_response["result"]["task"]["id"]
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

