#!/usr/bin/env python3
"""Lab 02: JSONL Validation (SOLUTION)"""

import json
import re


SECRET_RE = re.compile(r"(sk-[A-Za-z0-9_-]+|AKIA[0-9A-Z]{16}|password\s*=)", re.IGNORECASE)
ALLOWED_ROLES = {"system", "user", "assistant"}


def parse_jsonl(text: str) -> list[dict]:
    records: list[dict] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: invalid JSON: {exc}") from exc
    return records


def validate_messages(record: dict) -> list[str]:
    errors: list[str] = []
    messages = record.get("messages")
    if not isinstance(messages, list) or not messages:
        return ["messages must be a non-empty list"]
    if messages[-1].get("role") != "assistant":
        errors.append("final message must be assistant")
    for index, message in enumerate(messages):
        if message.get("role") not in ALLOWED_ROLES:
            errors.append(f"message {index}: invalid role")
        if not message.get("content"):
            errors.append(f"message {index}: content is empty")
    return errors


def detect_secrets(record: dict) -> list[str]:
    findings: list[str] = []
    for index, message in enumerate(record.get("messages", [])):
        if SECRET_RE.search(message.get("content", "")):
            findings.append(f"message {index}: possible secret")
    return findings


def validate_jsonl(text: str) -> dict:
    try:
        records = parse_jsonl(text)
    except ValueError as exc:
        return {"records": 0, "errors": [str(exc)]}

    errors: list[dict] = []
    for line_number, record in enumerate(records, start=1):
        record_errors = validate_messages(record) + detect_secrets(record)
        if record_errors:
            errors.append({"line": line_number, "errors": record_errors})
    return {"records": len(records), "errors": errors}


SAMPLE_JSONL = """
{"messages":[{"role":"system","content":"Classify tickets."},{"role":"user","content":"RDS timeout from app."},{"role":"assistant","content":"{\\"label\\":\\"database\\"}"}]}
{"messages":[{"role":"user","content":"My key is sk-badsecret123"},{"role":"assistant","content":"{\\"label\\":\\"security\\"}"}]}
{"messages":[{"role":"user","content":""},{"role":"assistant","content":"{}"}]}
""".strip()


def main() -> None:
    print("\nLab 02: JSONL Validation (Solution)\n")
    print(json.dumps(validate_jsonl(SAMPLE_JSONL), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

