#!/usr/bin/env python3
"""Lab 01: Trace Builder (SOLUTION)"""

from datetime import datetime, timezone
import json
import uuid


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def redact(text: str) -> str:
    text = text.replace("sk-", "[REDACTED]-")
    text = text.replace("password=", "password=[REDACTED]")
    return text


def make_span(name: str, attributes: dict, events: list[dict] | None = None) -> dict:
    return {
        "span_id": uuid.uuid4().hex[:12],
        "name": name,
        "time": now(),
        "attributes": attributes,
        "events": events or [],
    }


def build_trace() -> dict:
    trace_id = f"trace_{uuid.uuid4().hex[:8]}"
    spans = [
        make_span(
            "retrieval.query",
            {"db.system": "chroma", "retrieved.chunk_ids": ["runbook-01", "incident-22"]},
        ),
        make_span(
            "genai.chat",
            {
                "gen_ai.system": "openai-compatible",
                "gen_ai.operation.name": "chat",
                "gen_ai.request.model": "incident-triage",
                "gen_ai.usage.input_tokens": 900,
                "gen_ai.usage.output_tokens": 140,
            },
            [{"name": "prompt.preview", "body": redact("user pasted sk-demo and password=hunter2")}],
        ),
        make_span(
            "tool.call",
            {"tool.name": "read_logs", "tool.status": "ok", "service.name": "payment-api"},
        ),
    ]
    return {"trace_id": trace_id, "spans": spans}


def main() -> None:
    print("\nLab 01: Trace Builder (Solution)\n")
    print(json.dumps(build_trace(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

