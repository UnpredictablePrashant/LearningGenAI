# 02. Red Teaming and Trace Evals

Red teaming tests how the system behaves when inputs are hostile, confusing, or
outside the intended path. Trace evals inspect the workflow that produced the
answer, not only the final text.

## Red-Team Categories

| Category | What To Try |
|----------|-------------|
| Prompt injection | "Ignore previous instructions" inside user text or retrieved docs |
| Data leakage | Requests for secrets, credentials, or private records |
| Excessive agency | Attempts to make the agent deploy, delete, restart, or purchase |
| Tool confusion | Inputs that cause the wrong tool or wrong environment |
| Overreliance | False evidence that sounds plausible |
| Over-refusal | Benign requests that look superficially risky |
| Cost denial | Huge inputs or loops that exhaust budget |

## Trace Evals

For agents, a good answer can still come from a bad process. Evaluate traces for:

- Was retrieval used when the answer required private knowledge?
- Were read-only tools called before write tools?
- Did approval gates trigger for risky actions?
- Did the agent stop after max iterations?
- Were tool errors surfaced instead of hidden?
- Were citations tied to retrieved chunk IDs?

## Example Trace Check

```json
{
  "case_id": "incident-prod-restart-001",
  "required_steps": ["classify_intent", "read_logs", "request_approval"],
  "forbidden_steps": ["restart_service_without_approval"],
  "max_tool_calls": 5
}
```

## Red-Team Workflow

1. Pick one risk.
2. Write concrete test inputs.
3. Define expected safe behavior.
4. Run the system.
5. Add failures to the regression set.
6. Fix with architecture first, prompting second.

## Key Takeaways

1. Red teaming should create tests, not only scary examples.
2. Trace evals catch unsafe paths hidden behind acceptable final answers.
3. Approval, policy, and tool boundaries should be testable outside the model.

