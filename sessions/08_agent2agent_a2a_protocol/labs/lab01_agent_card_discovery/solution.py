#!/usr/bin/env python3
"""Lab 01: AgentCard Discovery (SOLUTION)"""

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
    return {
        "name": name,
        "url": url,
        "protocolVersion": "1.0",
        "version": "1.0.0",
        "capabilities": {
            "streaming": streaming,
            "pushNotifications": False,
            "stateTransitionHistory": True,
            "extendedAgentCard": False,
        },
        "securitySchemes": {
            "oauth": {
                "type": "oauth2",
                "scopes": required_scopes,
            }
        },
        "skills": [
            {
                "id": skill_id,
                "name": skill_id.replace("_", " ").title(),
                "description": f"Performs {skill_id.replace('_', ' ')}.",
                "tags": tags,
                "inputModes": input_modes,
                "outputModes": output_modes,
            }
        ],
    }


def validate_agent_card(card: dict) -> list[str]:
    errors: list[str] = []
    required = ["name", "url", "protocolVersion", "capabilities", "skills"]
    for field in required:
        if field not in card:
            errors.append(f"missing top-level field: {field}")

    for index, skill in enumerate(card.get("skills", [])):
        for field in ["id", "name", "inputModes", "outputModes"]:
            if field not in skill:
                errors.append(f"skill {index} missing field: {field}")

    return errors


def card_supports(card: dict, skill_id: str, input_mode: str, output_mode: str) -> bool:
    for skill in card.get("skills", []):
        if skill.get("id") != skill_id:
            continue
        if input_mode not in skill.get("inputModes", []):
            continue
        if output_mode not in skill.get("outputModes", []):
            continue
        return True
    return False


def card_scopes(card: dict) -> set[str]:
    scopes: set[str] = set()
    for scheme in card.get("securitySchemes", {}).values():
        scopes.update(scheme.get("scopes", []))
    return scopes


def select_agent(cards: list[dict], skill_id: str, input_mode: str, output_mode: str, caller_scopes: set[str]) -> dict | None:
    candidates = [
        card
        for card in cards
        if card_supports(card, skill_id, input_mode, output_mode)
        and bool(card_scopes(card) & caller_scopes)
    ]
    if not candidates:
        return None
    return sorted(
        candidates,
        key=lambda card: bool(card.get("capabilities", {}).get("streaming")),
        reverse=True,
    )[0]


def main() -> None:
    print("\nLab 01: AgentCard Discovery (Solution)\n")

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

