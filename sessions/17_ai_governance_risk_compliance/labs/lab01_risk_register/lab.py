#!/usr/bin/env python3
"""
Lab 01: AI Risk Register
========================
Create a small risk register for a GenAI feature.

Run:
    python lab.py

When stuck: check solution.py
"""


RISKS = [
    {"id": "R1", "use_case": "incident triage", "risk": "unsafe restart recommendation", "impact": 5, "likelihood": 3},
    {"id": "R2", "use_case": "ticket RAG", "risk": "sensitive ticket text disclosed", "impact": 5, "likelihood": 2},
    {"id": "R3", "use_case": "voice assistant", "risk": "tool action triggered from partial transcript", "impact": 4, "likelihood": 3},
]


def risk_score(risk: dict) -> int:
    # TODO 1:
    # Return impact * likelihood.
    pass


def classify_function(risk: dict) -> str:
    # TODO 2:
    # Return one of: govern, map, measure, manage.
    # Hint:
    # - disclosure relates to govern
    # - partial transcript relates to map
    # - unsafe action relates to manage
    pass


def control_for_risk(risk: dict) -> str:
    # TODO 3:
    # Return a practical control string for each risk.
    pass


def build_register(risks: list[dict]) -> list[dict]:
    # TODO 4:
    # Return register rows sorted by score descending.
    pass


def main() -> None:
    print("\nLab 01: AI Risk Register\n")

    rows = build_register(RISKS)
    if rows is None:
        print("TODO 4 not complete: build_register returned None.")
        return

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()

