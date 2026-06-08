# 02. Cost, Latency, and Resilience

Production GenAI is usually constrained by three forces: quality, latency, and
cost. A route is good only if it fits the workflow.

## Latency Patterns

| Pattern | Use When |
|---------|----------|
| Synchronous request | User needs an immediate answer |
| Streaming | User waits, but should see progress |
| Background mode | Task may take seconds or minutes |
| Batch processing | Work is offline, large, or not user-blocking |
| Cached prefix | Long stable context repeats often |

## Retry Policy

Retries should be bounded. Good retry policy includes:

- Max attempts
- Timeout per attempt
- Backoff with jitter
- Retryable error list
- Total request budget
- Fallback route

Never retry unsafe tool actions blindly. Retrying a read call is different from
retrying "restart production service".

## Cost Controls

Track:

- Input tokens
- Cached input tokens
- Output tokens
- Tool call fees
- Batch discounts or async processing choices
- Cost per successful task
- Cost per failed task

## Fallbacks

Fallback is not only "use a cheaper model".

Useful fallback options:

- Smaller model with stricter prompt
- Read-only answer without tool action
- Retrieval-only answer with citations
- Ask a clarification question
- Queue for human review
- Degrade to summary instead of full diagnosis

## Key Takeaways

1. Production routing is a budget decision, not only a model choice.
2. Retries need a stop condition.
3. Fallbacks should preserve safety and explain reduced confidence.

