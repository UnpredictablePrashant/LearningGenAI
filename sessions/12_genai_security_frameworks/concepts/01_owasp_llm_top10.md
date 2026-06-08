# 01. OWASP LLM Top 10

Prompt injection is only one class of GenAI security failure. Modern LLM apps
combine prompts, tools, documents, plugins, memory, and agents, so the security
model has to cover the full system.

## Practical Risk Map

| OWASP Category | DevOps Mental Model | Typical Control |
|----------------|---------------------|-----------------|
| Prompt injection | User input becomes config | Separate instructions from data |
| Insecure output handling | Trusting unvalidated API response | Schema validation and sandboxing |
| Training data poisoning | Compromised build input | Dataset provenance and review |
| Model denial of service | Expensive unbounded request | Token, tool, and loop budgets |
| Supply-chain vulnerabilities | Bad package/image/model | Pin, scan, and review dependencies |
| Sensitive information disclosure | Secrets in logs | Redaction and data minimization |
| Insecure plugin/tool design | Overpowered internal endpoint | Least privilege and authz |
| Excessive agency | Service account can do too much | Approval gates and scoped tools |
| Overreliance | Alert fatigue or blind trust | Human review for high-risk cases |
| Model theft | Unauthorized model extraction | Access control and anomaly detection |

## Threat Modeling Questions

Ask these before shipping:

- What untrusted text reaches the model?
- What can the model cause the system to do?
- Which tools can mutate state?
- Which data sources include secrets or private data?
- What outputs enter another parser, shell, database, or API?
- What loops can run without a human?
- What is logged, retained, or stored in memory?

## Architecture First

Prompts help, but they are not the main security boundary. Prefer controls that
exist outside the model:

- Capability allowlists
- Tool argument validators
- Environment scoping
- Approval gates
- Read/write separation
- Output schema validation
- Secret scanning
- Audit logs
- Rate limits

## Key Takeaways

1. Prompt injection defense is necessary, but not sufficient.
2. The model should not be the only policy enforcement point.
3. Risk increases when untrusted text, tools, and memory meet.

