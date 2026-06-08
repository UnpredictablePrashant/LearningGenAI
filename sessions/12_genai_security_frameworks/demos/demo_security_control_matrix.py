#!/usr/bin/env python3
"""Demo: risk-to-control mapping for GenAI applications."""


ROWS = [
    ("Prompt injection", "structural separation, source labels, retrieval filtering"),
    ("Insecure output handling", "schema validation, sandboxed execution, escaping"),
    ("Excessive agency", "least privilege tools, approval gates, action budgets"),
    ("Sensitive disclosure", "redaction, access control, retention policy"),
]


def main() -> None:
    print("\nDemo: Security Control Matrix\n")
    for risk, controls in ROWS:
        print(f"{risk:<26} -> {controls}")


if __name__ == "__main__":
    main()

