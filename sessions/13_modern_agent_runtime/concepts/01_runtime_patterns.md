# 01. Runtime Patterns

An agent runtime is the control plane around the model. It decides how state,
tools, guardrails, traces, handoffs, and final results are managed.

## Four Patterns

| Pattern | Use When | Tradeoff |
|---------|----------|----------|
| Direct model call | Simple single response | Little workflow control |
| Manual tool loop | You need explicit tool dispatch | You own all state and retries |
| Agent SDK | You want tools, handoffs, guardrails, traces | Framework shapes the runtime |
| Graph workflow | You need deterministic state transitions | More upfront design |

## Runtime Responsibilities

A production runtime should own:

- Conversation and task state
- Tool registry
- Guardrail checks
- Human approval states
- Handoff contracts
- Trace collection
- Retry and timeout policy
- Final result assembly
- Eval hooks

The model should decide language and reasoning. The runtime should enforce the
workflow.

## Graph Mental Model

```text
intake -> classify -> retrieve evidence -> call tool -> review risk -> compose
                           |                              |
                           +-------- missing info --------+
```

This is familiar to DevOps engineers: workflows become visible once state
transitions are explicit.

## Key Takeaways

1. Agent runtime is orchestration infrastructure.
2. Explicit state beats hidden conversation history for production workflows.
3. Frameworks help, but the architecture choices still matter.

