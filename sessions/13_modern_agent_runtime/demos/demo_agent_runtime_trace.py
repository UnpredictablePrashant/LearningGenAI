#!/usr/bin/env python3
"""Demo: minimal stateful agent runtime trace."""


STEPS = [
    ("intake", "received user incident report"),
    ("classify", "selected incident_triage route"),
    ("retrieve", "loaded crashloop runbook"),
    ("tool", "read previous pod logs"),
    ("guardrail", "prod restart requires approval"),
    ("compose", "returned evidence and next action"),
]


def main() -> None:
    print("\nDemo: Agent Runtime Trace\n")
    for index, (kind, detail) in enumerate(STEPS, start=1):
        print(f"{index}. {kind:<10} {detail}")


if __name__ == "__main__":
    main()

