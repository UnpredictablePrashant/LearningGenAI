#!/usr/bin/env python3
"""
Lab 04: Hyperparameter Planning
===============================
Create a conservative fine-tuning plan based on dataset size, token counts, and
risk signals.

Run:
    python lab.py

When stuck: check solution.py
"""

import json


def estimate_effective_tokens(total_tokens: int, n_epochs: int | str) -> int | str:
    # TODO 1:
    # If n_epochs is int, return total_tokens * n_epochs.
    # If n_epochs is "auto", return "auto".
    pass


def recommend_epochs(example_count: int) -> int | str:
    # TODO 2:
    # < 50 examples -> 3
    # 50-1000 -> "auto"
    # > 1000 -> "auto"
    pass


def risk_flags(example_count: int, duplicate_rate: float, avg_tokens: int) -> list[str]:
    # TODO 3:
    # Add flags for too_few_examples, high_duplicate_rate, long_examples.
    pass


def training_plan(example_count: int, total_tokens: int, duplicate_rate: float, avg_tokens: int) -> dict:
    # TODO 4:
    # Return plan with n_epochs, batch_size, learning_rate_multiplier,
    # effective_tokens, risk_flags, and recommendation.
    pass


def main() -> None:
    print("\nLab 04: Hyperparameter Planning\n")
    plan = training_plan(example_count=120, total_tokens=42000, duplicate_rate=0.04, avg_tokens=350)
    if plan is None:
        print("TODO 4 not complete: training_plan returned None.")
        return
    print(json.dumps(plan, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

