#!/usr/bin/env python3
"""Demo: readable GenAI trace waterfall."""


SPANS = [
    ("context", 20, "selected 6 history messages"),
    ("retrieval", 85, "returned chunks runbook-01, incident-22"),
    ("model", 920, "input=900 output=140"),
    ("tool", 140, "read_logs ok"),
    ("model", 480, "final answer"),
]


def main() -> None:
    print("\nDemo: Trace Waterfall\n")
    for name, ms, detail in SPANS:
        bar = "#" * max(1, ms // 80)
        print(f"{name:<10} {ms:>4}ms {bar:<12} {detail}")


if __name__ == "__main__":
    main()

