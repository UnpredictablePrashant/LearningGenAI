#!/usr/bin/env python3
"""
Lab 01: Capacity Planning
=========================
Estimate whether a model route fits on a GPU after weights and KV cache.

Run:
    python lab.py

When stuck: check solution.py
"""


MODELS = [
    {"name": "7b-int4", "weights_gb": 4.5, "kv_gb_per_request": 0.35},
    {"name": "13b-int4", "weights_gb": 8.5, "kv_gb_per_request": 0.55},
    {"name": "70b-int4", "weights_gb": 42.0, "kv_gb_per_request": 1.60},
]


def available_for_kv(gpu_gb: float, overhead_gb: float, weights_gb: float) -> float:
    # TODO 1:
    # Return remaining GB after overhead and weights.
    pass


def max_concurrency(gpu_gb: float, overhead_gb: float, model: dict) -> int:
    # TODO 2:
    # Return floor(available_for_kv / kv_gb_per_request), never below 0.
    pass


def choose_models_that_fit(gpu_gb: float, overhead_gb: float, min_concurrency: int) -> list[str]:
    # TODO 3:
    # Return model names whose max_concurrency is at least min_concurrency.
    pass


def main() -> None:
    print("\nLab 01: Capacity Planning\n")

    fit = choose_models_that_fit(gpu_gb=24, overhead_gb=2, min_concurrency=8)
    if fit is None:
        print("TODO 3 not complete: choose_models_that_fit returned None.")
        return

    for model in MODELS:
        print(f"{model['name']:<10} max concurrency: {max_concurrency(24, 2, model)}")
    print("\nFit for 24GB GPU and concurrency >= 8:", fit)


if __name__ == "__main__":
    main()

