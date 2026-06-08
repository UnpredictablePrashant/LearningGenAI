#!/usr/bin/env python3
"""Lab 01: Capacity Planning (SOLUTION)"""


MODELS = [
    {"name": "7b-int4", "weights_gb": 4.5, "kv_gb_per_request": 0.35},
    {"name": "13b-int4", "weights_gb": 8.5, "kv_gb_per_request": 0.55},
    {"name": "70b-int4", "weights_gb": 42.0, "kv_gb_per_request": 1.60},
]


def available_for_kv(gpu_gb: float, overhead_gb: float, weights_gb: float) -> float:
    return max(0.0, gpu_gb - overhead_gb - weights_gb)


def max_concurrency(gpu_gb: float, overhead_gb: float, model: dict) -> int:
    available = available_for_kv(gpu_gb, overhead_gb, model["weights_gb"])
    return max(0, int(available // model["kv_gb_per_request"]))


def choose_models_that_fit(gpu_gb: float, overhead_gb: float, min_concurrency: int) -> list[str]:
    return [
        model["name"]
        for model in MODELS
        if max_concurrency(gpu_gb, overhead_gb, model) >= min_concurrency
    ]


def main() -> None:
    print("\nLab 01: Capacity Planning (Solution)\n")

    for model in MODELS:
        print(f"{model['name']:<10} max concurrency: {max_concurrency(24, 2, model)}")
    print("\nFit for 24GB GPU and concurrency >= 8:", choose_models_that_fit(24, 2, 8))


if __name__ == "__main__":
    main()

