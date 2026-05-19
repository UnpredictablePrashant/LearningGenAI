# 02. When To Fine-Tune

Fine-tuning is powerful, but it is not the default answer to every model problem.
Use it when the failure is behavioral and repeatable.

## Decision Matrix

| Problem | Best First Move |
|---------|-----------------|
| Model lacks private facts | RAG |
| Model needs live data | Tool calling |
| Model output format is inconsistent | Prompting, then fine-tuning |
| Model needs company tone | Fine-tuning if prompt examples are not enough |
| Model must cite sources | RAG |
| Model must call APIs | Tool calling or MCP |
| Model makes domain-specific classification errors | Fine-tuning |
| Model is too expensive with long prompts | Fine-tune a smaller model |
| Model must follow rare edge-case policy | Fine-tuning plus evals |

## Good Fine-Tuning Use Cases

Good candidates:

- Alert classification
- Ticket routing
- JSON extraction
- Customer support tone
- Code review comment style
- Domain-specific translation
- Summarization with strict focus
- Structured answer schemas
- Short command generation with strict constraints

These tasks have stable behavior. You can provide many input-output examples.

## Poor Fine-Tuning Use Cases

Weak candidates:

- "Teach the model our whole wiki."
- "Make the model know today's inventory."
- "Make the model never hallucinate."
- "Make the model execute Kubernetes commands."
- "Make the model know customer permissions."
- "Replace retrieval with memorization."

These need retrieval, tools, authorization checks, or evaluation gates.

## Fine-Tuning vs RAG

Fine-tuning changes behavior.

RAG supplies information.

Example:

```
Question: What is our VPN setup for the Budapest office?
```

Use RAG. The answer depends on internal docs and may change.

Example:

```
Classify this alert as sev1/sev2/sev3 using our escalation style.
```

Fine-tuning may help. The desired behavior is a stable classification policy.

## Fine-Tuning vs Prompt Engineering

Prompting is cheaper to iterate.

Fine-tuning is slower, more expensive, and needs dataset governance.

Use prompt engineering first when:

- You have fewer than 20 examples.
- The task is still changing.
- The output schema is not stable.
- You do not have evals.
- You are still learning what good looks like.

Use fine-tuning when:

- You have enough high-quality examples.
- The prompt is long because it carries many examples.
- The base model repeatedly fails the same cases.
- The task is stable enough to train.
- The eval set proves prompting is insufficient.

## Fine-Tuning vs Distillation

Distillation is the process of using a stronger model or system to create
training data for a smaller model. Fine-tuning is often the training step that
uses that data.

Pattern:

```
large model + human review -> high-quality examples -> fine-tune smaller model
```

This can reduce cost and latency, but only if the training data is validated.

## Fine-Tuning vs Tools

Fine-tuning should not replace deterministic systems.

Do not fine-tune a model to calculate billing totals. Call the billing system.

Do not fine-tune a model to know whether a user has access. Call the auth system.

Do not fine-tune a model to deploy infrastructure. Use tools with approvals.

## Readiness Checklist

Fine-tune only when you can answer:

- What exact behavior should improve?
- What metric will prove improvement?
- What baseline are we comparing against?
- What examples show good behavior?
- What examples show known failure cases?
- What data must be excluded?
- How will we test safety and regressions?
- How will we roll back?

## Key Takeaways

1. Fine-tuning is for stable behavior, not dynamic facts.
2. RAG and tools are often better first choices.
3. Evals must come before training.
4. Do not train until you can describe the failure and success metric.

