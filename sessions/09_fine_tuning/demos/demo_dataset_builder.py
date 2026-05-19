#!/usr/bin/env python3
"""
Demo: Fine-Tuning Dataset Builder
=================================
Build SFT-style JSONL records for a cloud ticket classifier and inspect basic
dataset quality.

No API key required. Uses Python standard library only.

Run:
    python demos/demo_dataset_builder.py
"""

from __future__ import annotations

from collections import Counter
import json
import re


LABELS = {"networking", "compute", "database", "security", "billing", "unknown"}
SECRET_RE = re.compile(r"(sk-[A-Za-z0-9_-]+|AKIA[0-9A-Z]{16}|password\s*=)", re.IGNORECASE)


RAW_EXAMPLES = [
    {
        "ticket": "Pods in prod cannot resolve service names after CoreDNS rollout.",
        "label": "networking",
        "confidence": 0.91,
    },
    {
        "ticket": "EC2 instance fails health checks after AMI update.",
        "label": "compute",
        "confidence": 0.83,
    },
    {
        "ticket": "RDS connection timeout from EKS namespace payments.",
        "label": "database",
        "confidence": 0.89,
    },
    {
        "ticket": "S3 AccessDenied after IAM role policy change.",
        "label": "security",
        "confidence": 0.94,
    },
    {
        "ticket": "Unexpected NAT gateway data transfer cost spike.",
        "label": "billing",
        "confidence": 0.88,
    },
    {
        "ticket": "User says it is broken but gives no service or error.",
        "label": "unknown",
        "confidence": 0.52,
    },
]


SYSTEM_PROMPT = (
    "You classify cloud support tickets. Return strict JSON with keys "
    "label, confidence, and rationale. Allowed labels: networking, compute, "
    "database, security, billing, unknown."
)


def target_output(example: dict) -> str:
    return json.dumps(
        {
            "label": example["label"],
            "confidence": example["confidence"],
            "rationale": f"The ticket is best categorized as {example['label']}.",
        },
        sort_keys=True,
    )


def build_sft_record(example: dict) -> dict:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": example["ticket"]},
            {"role": "assistant", "content": target_output(example)},
        ]
    }


def validate_record(record: dict) -> list[str]:
    errors: list[str] = []
    messages = record.get("messages")
    if not isinstance(messages, list) or len(messages) < 2:
        return ["messages must be a list with at least user and assistant turns"]

    roles = [message.get("role") for message in messages]
    if "user" not in roles or roles[-1] != "assistant":
        errors.append("record must contain a user message and end with assistant")

    for index, message in enumerate(messages):
        content = message.get("content", "")
        if not content:
            errors.append(f"message {index} has empty content")
        if SECRET_RE.search(content):
            errors.append(f"message {index} appears to contain a secret")

    try:
        output = json.loads(messages[-1]["content"])
    except json.JSONDecodeError:
        errors.append("assistant output is not valid JSON")
        return errors

    if output.get("label") not in LABELS:
        errors.append(f"invalid label: {output.get('label')}")

    return errors


def dataset_report(records: list[dict]) -> dict:
    labels = []
    errors = []
    for index, record in enumerate(records):
        record_errors = validate_record(record)
        if record_errors:
            errors.append({"line": index + 1, "errors": record_errors})
        else:
            labels.append(json.loads(record["messages"][-1]["content"])["label"])

    return {
        "records": len(records),
        "labels": dict(Counter(labels)),
        "validation_errors": errors,
    }


def main() -> None:
    print("\nDemo: Fine-Tuning Dataset Builder\n")

    records = [build_sft_record(example) for example in RAW_EXAMPLES]
    print("Dataset report:")
    print(json.dumps(dataset_report(records), indent=2, sort_keys=True))

    print("\nJSONL preview:")
    for record in records[:3]:
        print(json.dumps(record, sort_keys=True))


if __name__ == "__main__":
    main()

