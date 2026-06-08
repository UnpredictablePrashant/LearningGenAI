#!/usr/bin/env python3
"""
Lab 01: Agent Trace Contract
============================
Create a minimal trace for a tool-using agent workflow.

Run:
    python lab.py

When stuck: check solution.py
"""

from datetime import datetime, timezone
import json
import uuid


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_trace(goal: str) -> dict:
    # TODO 1:
    # Return a trace dict with id, goal, status="running", and empty steps.
    pass


def add_step(trace: dict, kind: str, name: str, status: str, data: dict | None = None) -> None:
    # TODO 2:
    # Append a step with time, kind, name, status, and data.
    pass


def requires_approval(action: str, environment: str) -> bool:
    # TODO 3:
    # Return True for write actions in prod.
    pass


def finish_trace(trace: dict) -> dict:
    # TODO 4:
    # Set status to completed unless any step has status "blocked".
    # Return trace.
    pass


def main() -> None:
    print("\nLab 01: Agent Trace Contract\n")

    trace = new_trace("Investigate payment-api incident")
    if trace is None:
        print("TODO 1 not complete: new_trace returned None.")
        return

    add_step(trace, "intent", "classify_request", "completed", {"intent": "incident_triage"})
    add_step(trace, "tool", "read_logs", "completed", {"service": "payment-api"})
    status = "blocked" if requires_approval("restart", "prod") else "ready"
    add_step(trace, "approval", "restart_payment_api", status, {"environment": "prod"})
    print(json.dumps(finish_trace(trace), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

