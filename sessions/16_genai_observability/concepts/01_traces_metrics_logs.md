# 01. Traces, Metrics, and Logs

GenAI observability should answer three questions:

1. What happened?
2. Why did the system choose that path?
3. Was the outcome good, safe, fast, and affordable?

## What To Trace

| Span | Examples |
|------|----------|
| Request intake | user message received, request ID assigned |
| Context assembly | memory and history selected |
| Retrieval | query, filters, chunk IDs, scores |
| Model call | model, prompt version, token usage, latency |
| Tool call | tool name, validated args, result status |
| Guardrail | policy checked, allow/block/escalate |
| Final answer | citation IDs, refusal flag, confidence |

## Metrics

Track:

- Request count by route
- Error rate by provider/model/tool
- p50/p95/p99 latency
- Input and output tokens
- Cached input tokens
- Retrieval hit rate
- Tool success rate
- Safety block rate
- Eval pass rate by version
- Cost per successful task

## Logs

Structured logs should be useful without becoming a data leak.

Log:

- IDs and versions
- Status codes
- Error categories
- Redacted summaries
- Chunk IDs, not full sensitive chunks
- Tool names and result status

Avoid logging:

- Raw secrets
- Full private documents
- Credentials
- Unredacted user content where policy forbids it

## Key Takeaways

1. Trace the workflow, not only the final API call.
2. Metrics should connect quality, latency, safety, and cost.
3. Redaction is part of observability design.

