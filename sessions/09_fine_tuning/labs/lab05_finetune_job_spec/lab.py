#!/usr/bin/env python3
"""
Lab 05: Fine-Tune Job Spec
==========================
Build a provider-agnostic job specification and deployment checklist. This lab
does not call an API.

Run:
    python lab.py

When stuck: check solution.py
"""

import json


def build_file_manifest(train_path: str, validation_path: str) -> dict:
    # TODO 1:
    # Return file manifest entries with purpose "fine-tune".
    pass


def build_supervised_method(n_epochs: int | str = "auto") -> dict:
    # TODO 2:
    # Return method dict for supervised fine-tuning with hyperparameters.
    pass


def build_job_spec(base_model: str, training_file_id: str, validation_file_id: str, suffix: str) -> dict:
    # TODO 3:
    # Return job spec with model, training_file, validation_file, method, suffix, metadata.
    pass


def deployment_checklist() -> list[str]:
    # TODO 4:
    # Return checklist items for evals, safety, staging, canary, rollback, monitoring.
    pass


def main() -> None:
    print("\nLab 05: Fine-Tune Job Spec\n")

    manifest = build_file_manifest("data/train.jsonl", "data/validation.jsonl")
    spec = build_job_spec(
        base_model="gpt-4.1-mini-2025-04-14",
        training_file_id="file-train-placeholder",
        validation_file_id="file-valid-placeholder",
        suffix="ticket-router-v1",
    )
    checklist = deployment_checklist()
    if manifest is None or spec is None or checklist is None:
        print("TODOs not complete.")
        return

    print(json.dumps({"files": manifest, "job": spec, "checklist": checklist}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

