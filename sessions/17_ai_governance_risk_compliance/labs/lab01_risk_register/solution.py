#!/usr/bin/env python3
"""Lab 01: AI Risk Register (SOLUTION)"""


RISKS = [
    {"id": "R1", "use_case": "incident triage", "risk": "unsafe restart recommendation", "impact": 5, "likelihood": 3},
    {"id": "R2", "use_case": "ticket RAG", "risk": "sensitive ticket text disclosed", "impact": 5, "likelihood": 2},
    {"id": "R3", "use_case": "voice assistant", "risk": "tool action triggered from partial transcript", "impact": 4, "likelihood": 3},
]


def risk_score(risk: dict) -> int:
    return risk["impact"] * risk["likelihood"]


def classify_function(risk: dict) -> str:
    text = risk["risk"]
    if "disclosed" in text:
        return "govern"
    if "partial transcript" in text:
        return "map"
    if "unsafe" in text:
        return "manage"
    return "measure"


def control_for_risk(risk: dict) -> str:
    text = risk["risk"]
    if "restart" in text:
        return "approval gate for production actions"
    if "disclosed" in text:
        return "access filtering and redaction"
    if "partial transcript" in text:
        return "execute tools only after final transcript"
    return "manual review"


def build_register(risks: list[dict]) -> list[dict]:
    rows = []
    for risk in risks:
        rows.append(
            {
                "id": risk["id"],
                "use_case": risk["use_case"],
                "risk": risk["risk"],
                "function": classify_function(risk),
                "score": risk_score(risk),
                "control": control_for_risk(risk),
                "owner": "platform-team",
                "evidence": "eval report + trace sample",
            }
        )
    return sorted(rows, key=lambda row: row["score"], reverse=True)


def main() -> None:
    print("\nLab 01: AI Risk Register (Solution)\n")

    for row in build_register(RISKS):
        print(row)


if __name__ == "__main__":
    main()

