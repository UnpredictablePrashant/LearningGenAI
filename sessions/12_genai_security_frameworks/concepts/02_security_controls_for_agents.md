# 02. Security Controls for Agents

Agentic systems raise the security stakes because they can choose actions, call
tools, retain memory, delegate tasks, and run loops.

## Agent Control Points

| Control Point | What To Enforce |
|---------------|-----------------|
| Intake | Input validation, tenant scope, abuse limits |
| Context assembly | Access control, data minimization, source labels |
| Planning | Risk scoring, approval requirements, blocked routes |
| Tool dispatch | Schema validation, authz, read/write separation |
| Memory writes | Secret screening, retention policy, confidence metadata |
| Final response | Citation checks, refusal policy, disclosure review |
| Logging | Redaction, trace IDs, audit retention |

## Least Privilege Tools

Prefer narrow tools:

```text
GOOD: get_pod_logs(namespace, pod, since_minutes)
BAD: run_kubectl(command)

GOOD: create_staging_deploy_plan(service, version)
BAD: deploy_anything(environment, command)
```

Narrow tools make policy enforceable. They also make evals and audit logs easier
to understand.

## Approval Gates

Require approval before:

- Production mutations
- Deletions
- Credential changes
- Public communication
- Purchases or cost-incurring actions
- Memory writes involving sensitive user facts

## Security Test Cases

Every agent should have tests for:

- Direct prompt injection
- Indirect prompt injection in retrieved docs
- Unsafe tool arguments
- Wrong environment targeting
- Secret exfiltration
- Infinite or expensive loops
- Missing approval gate
- Benign request that should not be over-refused

## Key Takeaways

1. Agent security is workflow security.
2. Tool design is a security control.
3. Approval gates should be explicit state transitions, not hidden prompt text.

