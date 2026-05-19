#!/usr/bin/env python3
"""
Lab 01: Dataset Design
======================
Design high-quality supervised fine-tuning examples for a cloud ticket
classifier.

Run:
    python lab.py

When stuck: check solution.py
"""

import json


ALLOWED_LABELS = {"networking", "compute", "database", "security", "billing", "unknown"}


def make_system_prompt() -> str:
    # TODO 1:
    # Return a system prompt that tells the model:
    # - it classifies cloud support tickets
    # - it must return strict JSON
    # - allowed labels are ALLOWED_LABELS
    pass


def make_target(label: str, confidence: float, rationale: str) -> str:
    # TODO 2:
    # Validate label is allowed and confidence is between 0 and 1.
    # Return a JSON string with label, confidence, rationale.
    pass


def make_sft_example(ticket: str, label: str, confidence: float, rationale: str) -> dict:
    # TODO 3:
    # Return a chat SFT record with system, user, and assistant messages.
    pass


def quality_checks(example: dict) -> list[str]:
    # TODO 4:
    # Return errors if:
    # - messages missing
    # - final assistant content is not valid JSON
    # - label is invalid
    # - confidence missing or outside [0, 1]
    pass


def main() -> None:
    print("\nLab 01: Dataset Design\n")

    example = make_sft_example(
        ticket="S3 AccessDenied after IAM role policy update.",
        label="security",
        confidence=0.93,
        rationale="The ticket is about access control and IAM policy.",
    )
    if example is None:
        print("TODO 3 not complete: make_sft_example returned None.")
        return

    print(json.dumps(example, indent=2, sort_keys=True))
    print("\nQuality checks:", quality_checks(example))


if __name__ == "__main__":
    main()

