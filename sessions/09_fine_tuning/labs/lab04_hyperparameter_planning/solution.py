#!/usr/bin/env python3
"""Lab 04: Hyperparameter Planning (SOLUTION)"""

import json


def estimate_effective_tokens(total_tokens: int, n_epochs: int | str) -> int | str:
    if n_epochs == "auto":
        return "auto"
    return total_tokens * int(n_epochs)


def recommend_epochs(example_count: int) -> int | str:
    if example_count < 50:
        return 3
    return "auto"


def risk_flags(example_count: int, duplicate_rate: float, avg_tokens: int) -> list[str]:
    flags: list[str] = []
    if example_count < 50:
        flags.append("too_few_examples")
    if duplicate_rate > 0.1:
        flags.append("high_duplicate_rate")
    if avg_tokens > 2000:
        flags.append("long_examples")
    return flags


def training_plan(example_count: int, total_tokens: int, duplicate_rate: float, avg_tokens: int) -> dict:
    n_epochs = recommend_epochs(example_count)
    flags = risk_flags(example_count, duplicate_rate, avg_tokens)
    recommendation = "train only after baseline evals pass and validation set is clean"
    if "too_few_examples" in flags:
        recommendation = "collect more examples or keep using prompt engineering"
    if "high_duplicate_rate" in flags:
        recommendation = "deduplicate before training"

    return {
        "n_epochs": n_epochs,
        "batch_size": "auto",
        "learning_rate_multiplier": "auto",
        "effective_tokens": estimate_effective_tokens(total_tokens, n_epochs),
        "risk_flags": flags,
        "recommendation": recommendation,
    }


def main() -> None:
    print("\nLab 04: Hyperparameter Planning (Solution)\n")
    plan = training_plan(example_count=120, total_tokens=42000, duplicate_rate=0.04, avg_tokens=350)
    print(json.dumps(plan, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

