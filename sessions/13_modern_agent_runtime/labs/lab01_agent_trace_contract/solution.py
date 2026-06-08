#!/usr/bin/env python3
"""Lab 01: Agent Trace Contract (SOLUTION)"""

from datetime import datetime, timezone
import json
import uuid


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_trace(goal: str) -> dict:
    return {
        "id": f"trace_{uuid.uuid4().hex[:8]}",
        "goal": goal,
        "status": "running",
        "steps": [],
        "created_at": now(),
    }


def add_step(trace: dict, kind: str, name: str, status: str, data: dict | None = None) -> None:
    trace["steps"].append(
        {
            "time": now(),
            "kind": kind,
            "name": name,
            "status": status,
            "data": data or {},
        }
    )


def requires_approval(action: str, environment: str) -> bool:
    write_actions = {"restart", "deploy", "delete", "update", "scale"}
    return environment == "prod" and action in write_actions


def finish_trace(trace: dict) -> dict:
    trace["status"] = "blocked" if any(step["status"] == "blocked" for step in trace["steps"]) else "completed"
    trace["finished_at"] = now()
    return trace


def main() -> None:
    print("\nLab 01: Agent Trace Contract (Solution)\n")

    trace = new_trace("Investigate payment-api incident")
    add_step(trace, "intent", "classify_request", "completed", {"intent": "incident_triage"})
    add_step(trace, "tool", "read_logs", "completed", {"service": "payment-api"})
    status = "blocked" if requires_approval("restart", "prod") else "ready"
    add_step(trace, "approval", "restart_payment_api", status, {"environment": "prod"})
    print(json.dumps(finish_trace(trace), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

