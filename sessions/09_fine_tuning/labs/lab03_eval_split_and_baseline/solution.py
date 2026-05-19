#!/usr/bin/env python3
"""Lab 03: Eval Split and Baseline (SOLUTION)"""

from collections import Counter, defaultdict
import hashlib
import json


EXAMPLES = [
    {"text": "CoreDNS failing after rollout", "label": "networking"},
    {"text": "Security group blocks ALB traffic", "label": "networking"},
    {"text": "RDS max connections reached", "label": "database"},
    {"text": "Postgres slow query after deploy", "label": "database"},
    {"text": "S3 AccessDenied for app role", "label": "security"},
    {"text": "KMS key policy blocks decrypt", "label": "security"},
    {"text": "NAT gateway cost spike", "label": "billing"},
    {"text": "Monthly AWS bill doubled", "label": "billing"},
    {"text": "EC2 CPU throttling", "label": "compute"},
    {"text": "Node AMI launch failure", "label": "compute"},
    {"text": "It is broken", "label": "unknown"},
    {"text": "Need help", "label": "unknown"},
]


KEYWORDS = {
    "networking": ["dns", "coredns", "security group", "alb", "route"],
    "database": ["rds", "postgres", "query", "connections"],
    "security": ["iam", "accessdenied", "kms", "policy", "decrypt"],
    "billing": ["cost", "bill", "billing", "nat gateway"],
    "compute": ["ec2", "cpu", "node", "ami", "instance"],
}


def stable_bucket(text: str, buckets: int = 100) -> int:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(digest, 16) % buckets


def split_examples(examples: list[dict]) -> dict[str, list[dict]]:
    splits = {"train": [], "validation": [], "holdout": []}
    for example in examples:
        bucket = stable_bucket(example["text"])
        if bucket < 70:
            splits["train"].append(example)
        elif bucket < 85:
            splits["validation"].append(example)
        else:
            splits["holdout"].append(example)
    return splits


def baseline_predict(text: str) -> str:
    text_lower = text.lower()
    scores = Counter()
    for label, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                scores[label] += 1
    return scores.most_common(1)[0][0] if scores else "unknown"


def evaluate(examples: list[dict]) -> dict:
    if not examples:
        return {"accuracy": None, "rows": [], "confusion": {}}

    correct = 0
    rows = []
    confusion: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for example in examples:
        predicted = baseline_predict(example["text"])
        expected = example["label"]
        correct += int(predicted == expected)
        confusion[expected][predicted] += 1
        rows.append({"text": example["text"], "expected": expected, "predicted": predicted})

    return {
        "accuracy": correct / len(examples),
        "rows": rows,
        "confusion": {label: dict(counts) for label, counts in confusion.items()},
    }


def main() -> None:
    print("\nLab 03: Eval Split and Baseline (Solution)\n")
    splits = split_examples(EXAMPLES)
    report = {name: evaluate(rows) for name, rows in splits.items()}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

