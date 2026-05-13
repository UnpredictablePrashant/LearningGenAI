#!/usr/bin/env python3
"""
Demo: A2A AgentCard Discovery
=============================
Inspect AgentCards and choose an agent compatible with the request.

No API key required. Uses Python standard library only.

Run:
    python demos/demo_agent_card_discovery.py
"""

from __future__ import annotations

import json


AGENT_CARDS = [
    {
        "name": "sre-incident-agent",
        "version": "1.2.0",
        "url": "https://agents.example.com/sre",
        "protocolVersion": "1.0",
        "capabilities": {
            "streaming": True,
            "pushNotifications": False,
            "stateTransitionHistory": True,
            "extendedAgentCard": True,
        },
        "securitySchemes": {
            "oauth": {"type": "oauth2", "scopes": ["incidents:triage", "incidents:read"]}
        },
        "skills": [
            {
                "id": "incident_triage",
                "name": "Incident triage",
                "description": "Triage Kubernetes and cloud incidents.",
                "tags": ["sre", "incident", "kubernetes", "aws"],
                "inputModes": ["text/plain", "application/json"],
                "outputModes": ["text/plain", "application/json"],
            }
        ],
    },
    {
        "name": "cloud-cost-agent",
        "version": "0.9.0",
        "url": "https://agents.example.com/cost",
        "protocolVersion": "1.0",
        "capabilities": {"streaming": False, "pushNotifications": True},
        "securitySchemes": {
            "api_key": {"type": "apiKey", "scopes": ["cost:read"]}
        },
        "skills": [
            {
                "id": "cost_anomaly_analysis",
                "name": "Cost anomaly analysis",
                "description": "Analyze cloud cost spikes and idle resources.",
                "tags": ["finops", "aws", "cost"],
                "inputModes": ["application/json"],
                "outputModes": ["text/plain", "application/json"],
            }
        ],
    },
    {
        "name": "doc-retrieval-agent",
        "version": "2.1.0",
        "url": "https://agents.example.com/docs",
        "protocolVersion": "1.0",
        "capabilities": {"streaming": True, "pushNotifications": False},
        "securitySchemes": {
            "oauth": {"type": "oauth2", "scopes": ["docs:search"]}
        },
        "skills": [
            {
                "id": "document_search",
                "name": "Document search",
                "description": "Search internal runbooks and architecture docs.",
                "tags": ["rag", "docs", "search"],
                "inputModes": ["text/plain"],
                "outputModes": ["text/plain"],
            }
        ],
    },
]


def supports_skill(card: dict, skill_id: str) -> bool:
    return any(skill["id"] == skill_id for skill in card.get("skills", []))


def supports_modes(card: dict, input_mode: str, output_mode: str) -> bool:
    for skill in card.get("skills", []):
        if input_mode in skill.get("inputModes", []) and output_mode in skill.get("outputModes", []):
            return True
    return False


def requires_scope(card: dict) -> set[str]:
    scopes: set[str] = set()
    for scheme in card.get("securitySchemes", {}).values():
        scopes.update(scheme.get("scopes", []))
    return scopes


def choose_agent(skill_id: str, input_mode: str, output_mode: str, available_scopes: set[str]) -> dict | None:
    candidates: list[dict] = []
    for card in AGENT_CARDS:
        if not supports_skill(card, skill_id):
            continue
        if not supports_modes(card, input_mode, output_mode):
            continue
        if not requires_scope(card) & available_scopes:
            continue
        candidates.append(card)

    if not candidates:
        return None

    return sorted(
        candidates,
        key=lambda card: (
            bool(card.get("capabilities", {}).get("streaming")),
            card.get("version", ""),
        ),
        reverse=True,
    )[0]


def main() -> None:
    print("\nDemo: A2A AgentCard Discovery\n")
    print("Discovered cards:")
    for card in AGENT_CARDS:
        skill_ids = [skill["id"] for skill in card["skills"]]
        print(f"- {card['name']} version={card['version']} skills={skill_ids}")

    request = {
        "skill_id": "incident_triage",
        "input_mode": "application/json",
        "output_mode": "application/json",
        "available_scopes": {"incidents:triage", "docs:search"},
    }

    print("\nSelection request:")
    printable_request = {**request, "available_scopes": sorted(request["available_scopes"])}
    print(json.dumps(printable_request, indent=2, sort_keys=True))

    selected = choose_agent(**request)
    print("\nSelected agent:")
    if selected is None:
        print("No compatible agent found.")
    else:
        print(json.dumps(selected, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
