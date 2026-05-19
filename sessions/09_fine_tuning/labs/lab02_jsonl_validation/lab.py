#!/usr/bin/env python3
"""
Lab 02: JSONL Validation
========================
Validate fine-tuning JSONL records before upload.

Run:
    python lab.py

When stuck: check solution.py
"""

import json
import re


SECRET_RE = re.compile(r"(sk-[A-Za-z0-9_-]+|AKIA[0-9A-Z]{16}|password\s*=)", re.IGNORECASE)
ALLOWED_ROLES = {"system", "user", "assistant"}


def parse_jsonl(text: str) -> list[dict]:
    # TODO 1:
    # Parse non-empty JSONL lines into dicts.
    # Raise ValueError with line number on invalid JSON.
    pass


def validate_messages(record: dict) -> list[str]:
    # TODO 2:
    # Validate messages list exists, roles are allowed, content is non-empty,
    # and final message role is assistant.
    pass


def detect_secrets(record: dict) -> list[str]:
    # TODO 3:
    # Return findings for any message content matching SECRET_RE.
    pass


def validate_jsonl(text: str) -> dict:
    # TODO 4:
    # Parse records and return {"records": count, "errors": [...]}.
    # Include line numbers in errors.
    pass


SAMPLE_JSONL = """
{"messages":[{"role":"system","content":"Classify tickets."},{"role":"user","content":"RDS timeout from app."},{"role":"assistant","content":"{\\"label\\":\\"database\\"}"}]}
{"messages":[{"role":"user","content":"My key is sk-badsecret123"},{"role":"assistant","content":"{\\"label\\":\\"security\\"}"}]}
{"messages":[{"role":"user","content":""},{"role":"assistant","content":"{}"}]}
""".strip()


def main() -> None:
    print("\nLab 02: JSONL Validation\n")
    result = validate_jsonl(SAMPLE_JSONL)
    if result is None:
        print("TODO 4 not complete: validate_jsonl returned None.")
        return
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

