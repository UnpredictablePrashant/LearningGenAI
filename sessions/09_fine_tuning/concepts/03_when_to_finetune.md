# 03. When To Fine-Tune

Fine-tuning is powerful, but it is not the default answer to every model
problem. Use it when the failure is behavioral, stable, repeatable, and
measurable.

The key question is:

```text
Is the model missing information, or is it behaving in the wrong pattern?
```

If it is missing information, use retrieval or tools. If it is behaving in the
wrong pattern even after good prompting, fine-tuning may help.

## Decision Matrix

| Problem | Best First Move | Why |
|---------|-----------------|-----|
| Model lacks private facts | RAG | Facts belong in a retrievable source, not model memory |
| Model needs live data | Tool calling | Live data changes after training |
| Model output format is inconsistent | Prompting, then fine-tuning | Format is a behavior pattern |
| Model needs company tone | Prompting, then fine-tuning | Tone can be learned from examples |
| Model must cite sources | RAG | Citations require source documents |
| Model must call APIs | Tool calling or MCP | API execution must be explicit and controlled |
| Model makes domain-specific classification errors | Fine-tuning | Stable label boundaries can be learned |
| Model is too expensive with long prompts | Fine-tune a smaller model | Repeated examples can move from prompt to training |
| Model must follow rare edge-case policy | Fine-tuning plus evals | Edge cases need examples and regression tests |

## Analogy: Wrong Tool for the Job

If a student gets a math problem wrong because they do not know the formula, you
teach the concept. If they get it wrong because the numbers changed, you give
them the current numbers. Fine-tuning is teaching the pattern. RAG and tools
provide the current numbers.

Another way to say it:

```text
Fine-tuning = habit training
RAG = open the right book
Tools = use the calculator or system of record
Prompting = give clearer instructions now
```

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
- Refusal wording for recurring unsafe request types

These tasks have stable behavior. You can provide many input-output examples,
and you can decide whether an output is correct.

## Poor Fine-Tuning Use Cases

Weak candidates:

- "Teach the model our whole wiki."
- "Make the model know today's inventory."
- "Make the model never hallucinate."
- "Make the model execute Kubernetes commands."
- "Make the model know customer permissions."
- "Replace retrieval with memorization."
- "Fix a task we cannot clearly describe."
- "Improve everything in general."

These need retrieval, tools, authorization checks, better product design, or
clearer evals.

## Fine-Tuning vs RAG

Fine-tuning changes behavior.

RAG supplies information.

Example:

```text
Question: What is our VPN setup for the Budapest office?
```

Use RAG. The answer depends on internal docs and may change.

Example:

```text
Classify this alert as sev1/sev2/sev3 using our escalation style.
```

Fine-tuning may help. The desired behavior is a stable classification policy.

## Fine-Tuning vs Prompt Engineering

Prompting is cheaper to iterate.

Fine-tuning is slower, more expensive, and needs dataset governance.

Use prompt engineering first when:

- You have fewer than 20-50 examples.
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

```text
large model + human review -> high-quality examples -> fine-tune smaller model
```

This can reduce cost and latency, but only if the training data is validated.
If the stronger model produces wrong examples and nobody reviews them, the
smaller model learns those mistakes.

## Fine-Tuning vs Tools

Fine-tuning should not replace deterministic systems.

Do not fine-tune a model to calculate billing totals. Call the billing system.

Do not fine-tune a model to know whether a user has access. Call the auth
system.

Do not fine-tune a model to deploy infrastructure. Use tools with approvals.

The model can decide which kind of help the user needs, but the actual
permission check, calculation, or deployment should stay in code.

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

If one of these is missing, the next step is usually not training. The next step
is task definition, data design, or eval design.

## Basic Scoring Before You Train

For a classification task, start with a tiny baseline. Even a keyword baseline
is useful because it gives you something to beat.

```python
from collections import Counter

KEYWORDS = {
    "billing": ["invoice", "cost", "charge"],
    "security": ["iam", "permission", "accessdenied"],
    "database": ["rds", "postgres", "query"],
}

def predict(text: str) -> str:
    scores = Counter()
    lower = text.lower()
    for label, words in KEYWORDS.items():
        for word in words:
            if word in lower:
                scores[label] += 1
    return scores.most_common(1)[0][0] if scores else "unknown"
```

If a simple baseline already solves the problem, you may not need fine-tuning.
If the baseline fails in nuanced but repeatable ways, fine-tuning becomes more
reasonable.

## Key Takeaways

1. Fine-tuning is for stable behavior, not dynamic facts.
2. RAG and tools are often better first choices.
3. Evals must come before training.
4. Do not train until you can describe the failure and success metric.
5. A weak baseline is still valuable because it prevents training by guesswork.
