# 02. State, Guardrails, and Handoffs

The three runtime features that usually separate demos from production agents
are durable state, enforceable guardrails, and typed handoffs.

## Durable State

Store:

- Request ID
- User/session ID
- Current task state
- Selected route
- Tool calls and outputs
- Guardrail decisions
- Approval state
- Final answer and limitations

Do not rely on the prompt transcript as the only state store.

## Guardrails

Guardrails should run at multiple points:

- Input guardrails before planning
- Tool argument guardrails before execution
- Output guardrails before final response
- Memory guardrails before durable writes

## Handoffs

A handoff should include:

- Source agent
- Target agent
- Task objective
- Evidence bundle
- Allowed actions
- Required output schema
- Timeout and fallback

```json
{
  "from": "sre_agent",
  "to": "security_agent",
  "objective": "Review IAM-related root cause",
  "allowed_actions": ["read_evidence", "summarize"],
  "output_schema": "security_review_v1"
}
```

## Key Takeaways

1. State makes agents restartable and auditable.
2. Guardrails should be code paths, not only instructions.
3. Handoffs should pass evidence and constraints, not raw user prompts.

