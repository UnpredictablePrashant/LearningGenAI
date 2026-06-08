#!/usr/bin/env python3
"""Demo: production routing by budget instead of model popularity."""


ROUTES = [
    ("cheap", 0.74, 500, 0.001),
    ("standard", 0.86, 900, 0.006),
    ("reasoning", 0.94, 2800, 0.030),
]


def main() -> None:
    print("\nDemo: Cost and Latency Router\n")
    print("Route       quality  p95_ms  cost/request")
    for name, quality, p95_ms, cost in ROUTES:
        print(f"{name:<11} {quality:>7.2f} {p95_ms:>7}  ${cost:.3f}")

    print("\nRouting rule:")
    print("- chat autocomplete: cheap")
    print("- production incident triage: standard")
    print("- postmortem root-cause review: reasoning, probably background mode")


if __name__ == "__main__":
    main()

