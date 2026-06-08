# 01. Operating Model APIs

Model APIs are dependencies. Production systems should treat them like any other
critical upstream service.

## Production Concerns

| Concern | Question |
|---------|----------|
| Availability | What happens when the provider errors or times out? |
| Rate limits | How does the app behave under 429 responses? |
| Latency | What is the p95 budget for the user workflow? |
| Cost | What is the cost per successful task? |
| Quality | Which eval must pass before rollout? |
| Versioning | Which prompt, model, tool schema, and index produced this output? |
| Data policy | What data can leave the environment? |

## Model Gateway Pattern

A model gateway centralizes:

- Provider selection
- Model allowlists
- Timeout defaults
- Retry policy
- Token counting
- Cost attribution
- Prompt/version metadata
- Safety and logging hooks

For a DevOps team, this is the difference between every service hand-rolling
cloud credentials and using a platform-approved client.

## Request Metadata

Log enough metadata to debug without storing sensitive payloads by default:

```json
{
  "request_id": "req_123",
  "route": "incident_triage_fast",
  "model": "primary-small",
  "prompt_version": "triage-v7",
  "input_tokens": 1250,
  "output_tokens": 220,
  "latency_ms": 840,
  "cache_status": "hit",
  "eval_suite": "incident-triage-v3"
}
```

## Deployment Gate

Before a prompt/model change reaches production:

- Run evals.
- Compare against baseline.
- Confirm latency and cost budgets.
- Review safety failures manually.
- Canary by traffic percentage or internal users.
- Keep rollback metadata.

## Key Takeaways

1. Centralize model access before the fifth application copies the same code.
2. Log versions and budgets, not raw sensitive payloads.
3. Treat model changes like service deployments.

