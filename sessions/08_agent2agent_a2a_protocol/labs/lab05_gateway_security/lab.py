#!/usr/bin/env python3
"""
Lab 05: A2A Gateway Security
============================
Route a request to a specialist agent only when the AgentCard supports the
requested skill and the caller has the required scope.

Run:
    python lab.py

When stuck: check solution.py
"""

import json


def agent_card(name: str, skill_id: str, required_scope: str, output_modes: list[str]) -> dict:
    return {
        "name": name,
        "protocolVersion": "1.0",
        "capabilities": {"streaming": True},
        "securitySchemes": {"oauth": {"type": "oauth2", "scopes": [required_scope]}},
        "skills": [
            {
                "id": skill_id,
                "name": skill_id.replace("_", " ").title(),
                "inputModes": ["text/plain", "application/json"],
                "outputModes": output_modes,
            }
        ],
    }


def required_scopes(card: dict) -> set[str]:
    # TODO 1:
    # Return all scopes declared by the card.
    pass


def supports_skill(card: dict, skill_id: str, output_mode: str) -> bool:
    # TODO 2:
    # Return True if card has skill_id and supports output_mode.
    pass


def authorize(card: dict, caller_scopes: set[str]) -> bool:
    # TODO 3:
    # Return True if caller_scopes includes at least one required card scope.
    pass


def route(cards: list[dict], skill_id: str, output_mode: str, caller_scopes: set[str], message: str) -> dict:
    # TODO 4:
    # Find a card that supports the skill/output_mode.
    # If none, return UnsupportedOperationError.
    # If found but caller lacks scope, return AuthorizationError.
    # Otherwise return a completed task with one artifact text.
    pass


def main() -> None:
    print("\nLab 05: A2A Gateway Security\n")

    cards = [
        agent_card("sre-incident-agent", "incident_triage", "incidents:triage", ["application/json"]),
        agent_card("cost-agent", "cost_anomaly_analysis", "cost:read", ["application/json"]),
    ]

    ok = route(cards, "incident_triage", "application/json", {"incidents:triage"}, "Payments API is failing.")
    denied = route(cards, "cost_anomaly_analysis", "application/json", {"incidents:triage"}, "Why did cost spike?")
    missing = route(cards, "document_search", "text/plain", {"docs:search"}, "Find VPN docs.")
    if ok is None or denied is None or missing is None:
        print("TODO 4 not complete: route returned None.")
        return

    print("Authorized:")
    print(json.dumps(ok, indent=2, sort_keys=True))
    print("\nDenied:")
    print(json.dumps(denied, indent=2, sort_keys=True))
    print("\nMissing:")
    print(json.dumps(missing, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
