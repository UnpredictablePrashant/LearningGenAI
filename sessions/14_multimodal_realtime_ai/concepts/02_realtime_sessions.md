# 02. Realtime Sessions

Realtime AI applications are event systems. Audio, transcript, model output,
tool calls, interruptions, and connection events arrive over time.

## Event Types

| Event | Meaning |
|-------|---------|
| `audio.started` | User began speaking |
| `transcript.delta` | Partial transcript arrived |
| `transcript.final` | Turn text is finalized |
| `tool.requested` | Model wants external action |
| `tool.completed` | Tool result is available |
| `response.delta` | Partial assistant response |
| `response.completed` | Assistant turn is done |
| `session.closed` | Connection ended |

## Realtime Design Questions

- What is the max acceptable mouth-to-ear latency?
- What events are safe to act on before final transcript?
- Can the user interrupt the model?
- Which tools are allowed during voice?
- How are partial transcripts displayed?
- What is retained after the session?
- What happens when the connection drops?

## Tool Calls During Voice

Voice agents should usually confirm before state-changing tools:

```text
User: restart the production deployment
Agent: I can prepare that, but production restart requires approval. Should I request it?
```

For read-only tools, the agent can often proceed:

```text
User: check payment errors
Agent: I am reading recent payment-api logs now.
```

## Key Takeaways

1. Realtime apps are protocol and state-machine problems.
2. Partial transcripts should not trigger risky actions.
3. Voice agents need the same tool and approval controls as text agents.

