#!/usr/bin/env python3
"""
Lab 01: GenAI Threat Model
==========================
Map application features to OWASP-style risks and controls.

Run:
    python lab.py

When stuck: check solution.py
"""


FEATURES = [
    {"name": "RAG over support tickets", "untrusted_text": True, "secrets": True, "tools": False, "writes": False},
    {"name": "Kubernetes restart tool", "untrusted_text": False, "secrets": False, "tools": True, "writes": True},
    {"name": "Chat summary memory", "untrusted_text": True, "secrets": True, "tools": False, "writes": True},
]


def identify_risks(feature: dict) -> list[str]:
    # TODO 1:
    # Return risk names based on feature flags:
    # - untrusted_text -> Prompt Injection
    # - secrets -> Sensitive Information Disclosure
    # - tools -> Insecure Tool Design
    # - writes -> Excessive Agency
    pass


def controls_for_risk(risk: str) -> list[str]:
    # TODO 2:
    # Return practical controls for each risk.
    # Include at least one control per risk.
    pass


def build_threat_model(features: list[dict]) -> list[dict]:
    # TODO 3:
    # Return rows with feature, risks, and controls.
    pass


def main() -> None:
    print("\nLab 01: GenAI Threat Model\n")

    rows = build_threat_model(FEATURES)
    if rows is None:
        print("TODO 3 not complete: build_threat_model returned None.")
        return

    for row in rows:
        print(row["feature"])
        print("  risks:", ", ".join(row["risks"]))
        print("  controls:", ", ".join(row["controls"]))


if __name__ == "__main__":
    main()

