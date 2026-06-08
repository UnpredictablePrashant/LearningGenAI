#!/usr/bin/env python3
"""Demo: combine eval dimensions into a release scorecard."""


RUNS = [
    {"name": "baseline", "accuracy": 0.82, "json": 0.99, "safety": 1.0, "p95_ms": 1400},
    {"name": "new_prompt", "accuracy": 0.88, "json": 0.96, "safety": 0.98, "p95_ms": 980},
    {"name": "fixed_guardrail", "accuracy": 0.86, "json": 0.98, "safety": 1.0, "p95_ms": 990},
]


def decision(run: dict) -> str:
    if run["safety"] < 1.0:
        return "BLOCK: safety regression"
    if run["json"] < 0.98:
        return "BLOCK: format regression"
    if run["accuracy"] < 0.85:
        return "BLOCK: accuracy below target"
    if run["p95_ms"] > 1000:
        return "BLOCK: latency budget exceeded"
    return "SHIP"


def main() -> None:
    print("\nDemo: Eval Scorecard\n")
    for run in RUNS:
        print(
            f"{run['name']:<16} accuracy={run['accuracy']:.2f} "
            f"json={run['json']:.2f} safety={run['safety']:.2f} "
            f"p95={run['p95_ms']}ms -> {decision(run)}"
        )


if __name__ == "__main__":
    main()

