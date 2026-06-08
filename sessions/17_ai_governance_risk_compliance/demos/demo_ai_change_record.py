#!/usr/bin/env python3
"""Demo: minimal AI change record for release review."""

import json


CHANGE = {
    "change_id": "ai-change-001",
    "system": "incident-triage-assistant",
    "model": "primary-small@2026-05",
    "prompt_version": "triage-v8",
    "rag_index": "runbooks-2026-05-20",
    "eval_suite": "incident-triage-v3",
    "safety_review": "passed",
    "rollback": {"prompt_version": "triage-v7", "rag_index": "runbooks-2026-05-01"},
    "approver": "platform-owner",
}


def main() -> None:
    print("\nDemo: AI Change Record\n")
    print(json.dumps(CHANGE, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

