#!/usr/bin/env python3
"""
Demo: Fine-Tuning Eval Harness
==============================
Run a simple baseline classifier before fine-tuning and compute accuracy plus a
confusion matrix.

No API key required. Uses Python standard library only.

Run:
    python demos/demo_eval_harness.py
"""

from __future__ import annotations

from collections import Counter, defaultdict
import json


EVAL_CASES = [
    ("CoreDNS pods crash and services no longer resolve.", "networking"),
    ("RDS max connections reached for checkout service.", "database"),
    ("IAM policy denies s3:GetObject for app role.", "security"),
    ("NAT gateway transfer charges doubled overnight.", "billing"),
    ("Invoice includes unused EC2 instances from old environments.", "billing"),
    ("The app is bad and users are angry.", "unknown"),
    ("Security group does not allow port 443 from ALB.", "networking"),
    ("Postgres query latency increased after missing index.", "database"),
]


KEYWORDS = {
    "networking": {"dns", "coredns", "resolve", "security group", "port", "alb", "route", "nacl"},
    "database": {"rds", "postgres", "query", "connections", "index", "database"},
    "security": {"iam", "accessdenied", "policy", "permission", "kms", "role"},
    "billing": {"cost", "charges", "budget", "nat gateway", "spike"},
    "compute": {"ec2", "instance", "node", "ami", "launch", "cpu", "memory"},
}


def baseline_predict(text: str) -> str:
    text_lower = text.lower()
    scores = Counter()
    for label, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[label] += 1

    if not scores:
        return "unknown"
    return scores.most_common(1)[0][0]


def evaluate(cases: list[tuple[str, str]]) -> dict:
    confusion: defaultdict[str, Counter[str]] = defaultdict(Counter)
    correct = 0
    rows = []

    for text, expected in cases:
        predicted = baseline_predict(text)
        correct += int(predicted == expected)
        confusion[expected][predicted] += 1
        rows.append({"text": text, "expected": expected, "predicted": predicted, "correct": predicted == expected})

    return {
        "accuracy": correct / len(cases),
        "rows": rows,
        "confusion": {label: dict(counts) for label, counts in confusion.items()},
    }


def main() -> None:
    print("\nDemo: Fine-Tuning Eval Harness\n")
    result = evaluate(EVAL_CASES)
    print(json.dumps(result, indent=2, sort_keys=True))
    print("\nUse these failures to decide whether more prompting, better retrieval, or fine-tuning is justified.")


if __name__ == "__main__":
    main()
