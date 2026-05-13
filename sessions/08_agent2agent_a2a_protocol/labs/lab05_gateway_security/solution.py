#!/usr/bin/env python3
"""Lab 05: A2A Gateway Security (SOLUTION)"""

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
    scopes: set[str] = set()
    for scheme in card.get("securitySchemes", {}).values():
        scopes.update(scheme.get("scopes", []))
    return scopes


def supports_skill(card: dict, skill_id: str, output_mode: str) -> bool:
    for skill in card.get("skills", []):
        if skill.get("id") == skill_id and output_mode in skill.get("outputModes", []):
            return True
    return False


def authorize(card: dict, caller_scopes: set[str]) -> bool:
    return bool(required_scopes(card) & caller_scopes)


def route(cards: list[dict], skill_id: str, output_mode: str, caller_scopes: set[str], message: str) -> dict:
    matching = [card for card in cards if supports_skill(card, skill_id, output_mode)]
    if not matching:
        return {"error": "UnsupportedOperationError", "message": f"No agent supports {skill_id}"}

    card = matching[0]
    if not authorize(card, caller_scopes):
        return {
            "error": "AuthorizationError",
            "message": f"Missing one of scopes: {sorted(required_scopes(card))}",
        }

    return {
        "task": {
            "id": f"task-{skill_id}",
            "status": {"state": "TASK_STATE_COMPLETED"},
            "artifacts": [
                {
                    "artifactId": f"artifact-{skill_id}",
                    "name": f"{skill_id}_result",
                    "parts": [{"text": f"{card['name']} handled: {message}"}],
                }
            ],
        }
    }


def main() -> None:
    print("\nLab 05: A2A Gateway Security (Solution)\n")

    cards = [
        agent_card("sre-incident-agent", "incident_triage", "incidents:triage", ["application/json"]),
        agent_card("cost-agent", "cost_anomaly_analysis", "cost:read", ["application/json"]),
    ]

    ok = route(cards, "incident_triage", "application/json", {"incidents:triage"}, "Payments API is failing.")
    denied = route(cards, "cost_anomaly_analysis", "application/json", {"incidents:triage"}, "Why did cost spike?")
    missing = route(cards, "document_search", "text/plain", {"docs:search"}, "Find VPN docs.")

    print("Authorized:")
    print(json.dumps(ok, indent=2, sort_keys=True))
    print("\nDenied:")
    print(json.dumps(denied, indent=2, sort_keys=True))
    print("\nMissing:")
    print(json.dumps(missing, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

