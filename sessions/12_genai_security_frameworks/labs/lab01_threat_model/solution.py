#!/usr/bin/env python3
"""Lab 01: GenAI Threat Model (SOLUTION)"""


FEATURES = [
    {"name": "RAG over support tickets", "untrusted_text": True, "secrets": True, "tools": False, "writes": False},
    {"name": "Kubernetes restart tool", "untrusted_text": False, "secrets": False, "tools": True, "writes": True},
    {"name": "Chat summary memory", "untrusted_text": True, "secrets": True, "tools": False, "writes": True},
]


CONTROL_MAP = {
    "Prompt Injection": ["quote retrieved text as data", "ignore instructions from documents"],
    "Sensitive Information Disclosure": ["redact secrets", "filter by access policy"],
    "Insecure Tool Design": ["validate tool args", "use scoped service accounts"],
    "Excessive Agency": ["require approval gates", "separate read and write tools"],
}


def identify_risks(feature: dict) -> list[str]:
    risks: list[str] = []
    if feature["untrusted_text"]:
        risks.append("Prompt Injection")
    if feature["secrets"]:
        risks.append("Sensitive Information Disclosure")
    if feature["tools"]:
        risks.append("Insecure Tool Design")
    if feature["writes"]:
        risks.append("Excessive Agency")
    return risks


def controls_for_risk(risk: str) -> list[str]:
    return CONTROL_MAP.get(risk, ["manual review"])


def build_threat_model(features: list[dict]) -> list[dict]:
    rows = []
    for feature in features:
        risks = identify_risks(feature)
        controls = sorted({control for risk in risks for control in controls_for_risk(risk)})
        rows.append({"feature": feature["name"], "risks": risks, "controls": controls})
    return rows


def main() -> None:
    print("\nLab 01: GenAI Threat Model (Solution)\n")

    for row in build_threat_model(FEATURES):
        print(row["feature"])
        print("  risks:", ", ".join(row["risks"]))
        print("  controls:", ", ".join(row["controls"]))


if __name__ == "__main__":
    main()

