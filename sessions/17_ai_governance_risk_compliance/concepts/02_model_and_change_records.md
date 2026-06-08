# 02. Model and Change Records

Every production AI behavior change should be traceable.

## Version Record

Record:

- Application version
- Model name and version
- Prompt version
- Tool schema version
- RAG index version
- Dataset version
- Eval suite version
- Safety policy version
- Rollback target
- Approver

## Change Record

Example:

```json
{
  "change_id": "ai-change-2026-05-001",
  "system": "incident-triage-assistant",
  "change": "upgrade triage prompt from v7 to v8",
  "eval_report": "evals/incident-triage-v3.json",
  "risk_review": "approved",
  "rollback": "prompt v7"
}
```

## Incident Disclosure

Plan before incidents happen:

- What qualifies as an AI incident?
- Who is paged?
- What logs and traces are preserved?
- What user or customer notification is required?
- How do you disable risky features quickly?
- How do you add regression evals after resolution?

## Key Takeaways

1. AI changes need the same discipline as infrastructure changes.
2. Version records make evals and incidents explainable.
3. Rollback plans should include prompts, models, indexes, tools, and policies.

