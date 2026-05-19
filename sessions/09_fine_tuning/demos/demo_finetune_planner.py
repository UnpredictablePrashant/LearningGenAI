#!/usr/bin/env python3
"""
Demo: Fine-Tuning Job Planner
=============================
Create a safe fine-tuning job plan without uploading files or calling an API.

No API key required. Uses Python standard library only.

Run:
    python demos/demo_finetune_planner.py
"""

from __future__ import annotations

import json


def choose_hyperparameters(example_count: int, avg_tokens: int) -> dict:
    if example_count < 50:
        risk = "too_few_examples"
        n_epochs = 3
    elif example_count < 500:
        risk = "medium_dataset"
        n_epochs = "auto"
    else:
        risk = "large_dataset"
        n_epochs = "auto"

    if avg_tokens > 2000:
        batch_size = "auto"
        note = "Long examples: watch cost, truncation, and overfitting."
    else:
        batch_size = "auto"
        note = "Use provider defaults first; tune only after evals."

    return {
        "n_epochs": n_epochs,
        "batch_size": batch_size,
        "learning_rate_multiplier": "auto",
        "risk": risk,
        "note": note,
    }


def build_job_plan(
    task_name: str,
    base_model: str,
    training_file_id: str,
    validation_file_id: str,
    example_count: int,
    avg_tokens: int,
) -> dict:
    hyperparameters = choose_hyperparameters(example_count, avg_tokens)
    return {
        "task_name": task_name,
        "base_model": base_model,
        "training_file": training_file_id,
        "validation_file": validation_file_id,
        "method": {
            "type": "supervised",
            "supervised": {
                "hyperparameters": {
                    "n_epochs": hyperparameters["n_epochs"],
                    "batch_size": hyperparameters["batch_size"],
                    "learning_rate_multiplier": hyperparameters["learning_rate_multiplier"],
                }
            },
        },
        "suffix": f"{task_name}-v1",
        "metadata": {
            "dataset_version": "tickets-v3",
            "eval_version": "ticket-router-eval-v2",
            "owner": "platform-ai",
        },
        "risk_flags": [hyperparameters["risk"]],
        "notes": [hyperparameters["note"], "Deploy only if holdout eval beats baseline."],
    }


def main() -> None:
    print("\nDemo: Fine-Tuning Job Planner\n")

    plan = build_job_plan(
        task_name="ticket-router",
        base_model="gpt-4.1-mini-2025-04-14",
        training_file_id="file-train-placeholder",
        validation_file_id="file-valid-placeholder",
        example_count=420,
        avg_tokens=350,
    )
    print(json.dumps(plan, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

