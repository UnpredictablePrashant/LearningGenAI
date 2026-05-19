#!/usr/bin/env python3
"""Lab 01: Dataset Design (SOLUTION)"""

import json


ALLOWED_LABELS = {"networking", "compute", "database", "security", "billing", "unknown"}


def make_system_prompt() -> str:
    labels = ", ".join(sorted(ALLOWED_LABELS))
    return (
        "You classify cloud support tickets. Return strict JSON with keys "
        f"label, confidence, and rationale. Allowed labels: {labels}. "
        "Use unknown when the ticket lacks enough evidence."
    )


def make_target(label: str, confidence: float, rationale: str) -> str:
    if label not in ALLOWED_LABELS:
        raise ValueError(f"invalid label: {label}")
    if not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    return json.dumps(
        {"label": label, "confidence": confidence, "rationale": rationale},
        sort_keys=True,
    )


def make_sft_example(ticket: str, label: str, confidence: float, rationale: str) -> dict:
    return {
        "messages": [
            {"role": "system", "content": make_system_prompt()},
            {"role": "user", "content": ticket},
            {"role": "assistant", "content": make_target(label, confidence, rationale)},
        ]
    }


def quality_checks(example: dict) -> list[str]:
    errors: list[str] = []
    messages = example.get("messages")
    if not isinstance(messages, list):
        return ["messages missing"]
    if not messages or messages[-1].get("role") != "assistant":
        errors.append("final message must be assistant")
        return errors
    try:
        output = json.loads(messages[-1].get("content", ""))
    except json.JSONDecodeError:
        return ["assistant content is not valid JSON"]
    if output.get("label") not in ALLOWED_LABELS:
        errors.append("invalid label")
    confidence = output.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        errors.append("confidence missing or outside [0, 1]")
    return errors


def main() -> None:
    print("\nLab 01: Dataset Design (Solution)\n")

    example = make_sft_example(
        ticket="S3 AccessDenied after IAM role policy update.",
        label="security",
        confidence=0.93,
        rationale="The ticket is about access control and IAM policy.",
    )

    print(json.dumps(example, indent=2, sort_keys=True))
    print("\nQuality checks:", quality_checks(example))


if __name__ == "__main__":
    main()

