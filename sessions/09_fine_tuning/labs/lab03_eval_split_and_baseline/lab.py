#!/usr/bin/env python3
"""
Lab 03: Eval Split and Baseline
===============================
Create deterministic train/validation/holdout splits and evaluate a simple
baseline classifier before fine-tuning.

Run:
    python lab.py

When stuck: check solution.py
"""

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
    # TODO 1:
    # Return a deterministic bucket number from 0 to buckets - 1 using sha256.
    pass


def split_examples(examples: list[dict]) -> dict[str, list[dict]]:
    # TODO 2:
    # Use stable_bucket(example["text"]):
    # < 70 train, < 85 validation, else holdout.
    pass


def baseline_predict(text: str) -> str:
    # TODO 3:
    # Keyword baseline. Return label with most keyword matches, or unknown.
    pass


def evaluate(examples: list[dict]) -> dict:
    # TODO 4:
    # Return accuracy, rows, and confusion matrix.
    pass


def main() -> None:
    print("\nLab 03: Eval Split and Baseline\n")

    splits = split_examples(EXAMPLES)
    if splits is None:
        print("TODO 2 not complete: split_examples returned None.")
        return

    report = {name: evaluate(rows) for name, rows in splits.items()}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

