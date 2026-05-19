#!/usr/bin/env python3
"""Lab 05: Fine-Tune Job Spec (SOLUTION)"""

import json


def build_file_manifest(train_path: str, validation_path: str) -> dict:
    return {
        "training": {"path": train_path, "purpose": "fine-tune"},
        "validation": {"path": validation_path, "purpose": "fine-tune"},
    }


def build_supervised_method(n_epochs: int | str = "auto") -> dict:
    return {
        "type": "supervised",
        "supervised": {
            "hyperparameters": {
                "n_epochs": n_epochs,
                "batch_size": "auto",
                "learning_rate_multiplier": "auto",
            }
        },
    }


def build_job_spec(base_model: str, training_file_id: str, validation_file_id: str, suffix: str) -> dict:
    return {
        "model": base_model,
        "training_file": training_file_id,
        "validation_file": validation_file_id,
        "method": build_supervised_method(),
        "suffix": suffix,
        "metadata": {
            "dataset_version": "ticket-router-v1",
            "eval_version": "ticket-router-holdout-v1",
            "owner": "platform-ai",
        },
    }


def deployment_checklist() -> list[str]:
    return [
        "baseline eval recorded",
        "fine-tuned model beats baseline on holdout eval",
        "JSON/schema validity checked",
        "safety and refusal evals passed",
        "staging deployment completed",
        "canary plan defined",
        "rollback model configured",
        "monitoring dashboard updated",
    ]


def main() -> None:
    print("\nLab 05: Fine-Tune Job Spec (Solution)\n")

    manifest = build_file_manifest("data/train.jsonl", "data/validation.jsonl")
    spec = build_job_spec(
        base_model="gpt-4.1-mini-2025-04-14",
        training_file_id="file-train-placeholder",
        validation_file_id="file-valid-placeholder",
        suffix="ticket-router-v1",
    )
    checklist = deployment_checklist()
    print(json.dumps({"files": manifest, "job": spec, "checklist": checklist}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

