#!/usr/bin/env python3
"""
Demo: A2A Gateway
=================
Route requests to specialist agents using AgentCard skills and caller scopes.

No API key required. Uses Python standard library only.

Run:
    python demos/demo_a2a_gateway.py
"""

from __future__ import annotations

from dataclasses import dataclass
import json


@dataclass
class Caller:
    subject: str
    scopes: set[str]


@dataclass
class SpecialistAgent:
    name: str
    skill_id: str
    required_scope: str
    output_mode: str

    def agent_card(self) -> dict:
        return {
            "name": self.name,
            "protocolVersion": "1.0",
            "capabilities": {"streaming": True, "stateTransitionHistory": True},
            "skills": [
                {
                    "id": self.skill_id,
                    "name": self.skill_id.replace("_", " ").title(),
                    "inputModes": ["text/plain", "application/json"],
                    "outputModes": [self.output_mode],
                }
            ],
            "securitySchemes": {
                "oauth": {"type": "oauth2", "scopes": [self.required_scope]}
            },
        }

    def handle(self, message: dict) -> dict:
        text = " ".join(part.get("text", "") for part in message.get("parts", []))
        return {
            "task": {
                "id": f"task-{self.skill_id}",
                "status": {"state": "TASK_STATE_COMPLETED"},
                "artifacts": [
                    {
                        "artifactId": f"artifact-{self.skill_id}",
                        "name": f"{self.skill_id}_result",
                        "parts": [
                            {
                                "text": f"{self.name} handled request: {text}"
                            }
                        ],
                    }
                ],
            }
        }


class A2AGateway:
    def __init__(self, agents: list[SpecialistAgent]) -> None:
        self.agents = agents

    def discover(self) -> list[dict]:
        return [agent.agent_card() for agent in self.agents]

    def route(self, caller: Caller, skill_id: str, message: dict) -> dict:
        for agent in self.agents:
            if agent.skill_id != skill_id:
                continue
            if agent.required_scope not in caller.scopes:
                return {
                    "error": "AuthorizationError",
                    "message": f"{caller.subject} lacks scope {agent.required_scope}",
                }
            return agent.handle(message)

        return {"error": "UnsupportedOperationError", "message": f"No agent supports {skill_id}"}


def main() -> None:
    print("\nDemo: A2A Gateway\n")

    gateway = A2AGateway(
        [
            SpecialistAgent("sre-incident-agent", "incident_triage", "incidents:triage", "application/json"),
            SpecialistAgent("cloud-cost-agent", "cost_anomaly_analysis", "cost:read", "application/json"),
            SpecialistAgent("doc-retrieval-agent", "document_search", "docs:search", "text/plain"),
        ]
    )

    caller = Caller("support-agent", {"incidents:triage", "docs:search"})
    message = {
        "role": "ROLE_USER",
        "parts": [
            {"text": "Payments API is returning 500s after the latest deployment."},
            {"data": {"service": "payments", "environment": "prod"}},
        ],
    }

    print("Discovered agents:")
    print(json.dumps(gateway.discover(), indent=2))

    print("\nAuthorized route:")
    print(json.dumps(gateway.route(caller, "incident_triage", message), indent=2))

    print("\nUnauthorized route:")
    print(json.dumps(gateway.route(caller, "cost_anomaly_analysis", message), indent=2))


if __name__ == "__main__":
    main()

