#!/usr/bin/env python3
"""
Lab 01: AgentCard Discovery
===========================
Create and validate AgentCards, then select a compatible agent for a requested
skill and modality.

Run:
    python lab.py

When stuck: check solution.py
"""

import json


def build_agent_card(
    name: str,
    url: str,
    skill_id: str,
    tags: list[str],
    input_modes: list[str],
    output_modes: list[str],
    required_scopes: list[str],
    streaming: bool = False,
) -> dict:
    # TODO 1:
    # Return an AgentCard-like dict with:
    # name, url, protocolVersion, version, capabilities, securitySchemes, skills.
    # Keep protocolVersion as "1.0" and version as "1.0.0".
    pass


def validate_agent_card(card: dict) -> list[str]:
    # TODO 2:
    # Return a list of validation errors.
    # Check required top-level fields: name, url, protocolVersion, capabilities, skills.
    # Check every skill has id, name, inputModes, outputModes.
    pass


def card_supports(card: dict, skill_id: str, input_mode: str, output_mode: str) -> bool:
    # TODO 3:
    # Return True if any skill matches skill_id and supports both modes.
    pass


def card_scopes(card: dict) -> set[str]:
    # TODO 4:
    # Return all scopes declared under securitySchemes.
    pass


def select_agent(cards: list[dict], skill_id: str, input_mode: str, output_mode: str, caller_scopes: set[str]) -> dict | None:
    # TODO 5:
    # Return the first compatible card where caller_scopes intersects required scopes.
    # Prefer cards with streaming capability when multiple cards match.
    pass


def main() -> None:
    print("\nLab 01: AgentCard Discovery\n")

    cards = [
        build_agent_card(
            "sre-incident-agent",
            "https://agents.example.com/sre",
            "incident_triage",
            ["sre", "incident", "kubernetes"],
            ["text/plain", "application/json"],
            ["text/plain", "application/json"],
            ["incidents:triage"],
            streaming=True,
        ),
        build_agent_card(
            "cost-agent",
            "https://agents.example.com/cost",
            "cost_anomaly_analysis",
            ["finops", "aws", "cost"],
            ["application/json"],
            ["application/json"],
            ["cost:read"],
        ),
    ]

    if any(card is None for card in cards):
        print("TODO 1 not complete: build_agent_card returned None.")
        return

    for card in cards:
        errors = validate_agent_card(card)
        print(f"{card['name']} validation errors: {errors}")

    selected = select_agent(
        cards,
        skill_id="incident_triage",
        input_mode="application/json",
        output_mode="application/json",
        caller_scopes={"incidents:triage"},
    )

    print("\nSelected card:")
    print(json.dumps(selected, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

