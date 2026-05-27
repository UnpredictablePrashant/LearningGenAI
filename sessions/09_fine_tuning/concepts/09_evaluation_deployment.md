# 09. Evaluation and Deployment

Fine-tuning without evals is guessing. You need a baseline before training and a
gate before deployment.

The question is not:

```text
Did the training job finish?
```

The question is:

```text
Does the fine-tuned model perform better than the baseline on examples it did
not train on?
```

## Eval Sets

Use three splits:

- Training set: used for learning
- Validation set: used during training and iteration
- Holdout test set: used only for final evaluation

Never tune repeatedly against the holdout set. It stops being a true holdout.

Analogy: if a student practices the exact final exam questions, the score no
longer measures general understanding.

## Baseline

Evaluate before training:

- Prompt-only base model
- RAG or tool-based solution if relevant
- Current production model
- Simple rules baseline for classification

If fine-tuning cannot beat the baseline, do not deploy it.

## Metrics

Choose metrics by task:

| Task | Useful Metrics |
|------|----------------|
| Classification | accuracy, precision, recall, F1, confusion matrix |
| Extraction | exact match, JSON validity, field-level F1 |
| Summarization | human rubric, coverage, citation support |
| Style | human preference, pairwise comparison |
| JSON output | parse rate, schema validity |
| Safety | refusal accuracy, policy violation rate |

Do not use one metric for every task.

## Basic Classification Math

For a label like `billing`:

```text
precision = correct billing predictions / all billing predictions
recall    = correct billing predictions / all actual billing examples
```

Example:

```text
The model predicted billing 10 times.
8 were actually billing.
There were 12 billing examples in the test set.

precision = 8 / 10 = 0.80
recall    = 8 / 12 = 0.67
```

Precision answers: "When the model says billing, how often is it right?"

Recall answers: "Of all real billing cases, how many did the model catch?"

## Confusion Matrix

A confusion matrix shows which labels are being mixed up.

```text
expected \ predicted | billing | security | unknown
billing              |    8    |    1     |   3
security             |    0    |   11     |   1
unknown              |    2    |    0     |   6
```

This is more useful than accuracy alone. If billing and unknown are confused,
you improve examples and label rules around ambiguous billing tickets.

## Tiny Eval Harness

```python
import json

def exact_match_score(expected: str, actual: str) -> bool:
    return expected.strip() == actual.strip()

def evaluate(rows, predict):
    correct = 0
    results = []

    for row in rows:
        actual = predict(row["prompt"])
        ok = exact_match_score(row["completion"], actual)
        correct += int(ok)
        results.append({
            "prompt": row["prompt"],
            "expected": row["completion"],
            "actual": actual,
            "correct": ok,
        })

    return {
        "accuracy": correct / len(rows),
        "results": results,
    }

print(json.dumps(evaluate(test_rows, predict), indent=2))
```

For real projects, add schema validation, label metrics, safety checks, and
human review where needed.

## Regression Tests

Create regression cases:

- Previously failing examples
- Prompt injection attempts
- Out-of-domain requests
- Ambiguous inputs
- Safety-sensitive requests
- Schema edge cases
- Very short and very long inputs

Fine-tuning can improve one behavior and regress another.

## Deployment Pattern

Treat fine-tuned models like deployable artifacts:

1. Create model version record.
2. Store dataset version.
3. Store eval version and scores.
4. Deploy to staging.
5. Run shadow traffic or offline replay.
6. Canary a small percentage.
7. Monitor metrics and costs.
8. Roll back on regression.

## Monitoring

Track:

- Request volume
- Latency
- Token usage
- Parse errors
- Schema failures
- Safety refusals
- User corrections
- Drift in input distribution
- Eval replay over time

If production inputs drift, the fine-tuned model may degrade.

## Deployment Gate

Before deployment, require:

- Holdout score beats baseline.
- JSON/schema validity meets threshold.
- Safety eval does not regress.
- Latency and cost are acceptable.
- Rollback config is ready.
- Owner approves the model version.

The exact thresholds depend on the application. A customer-facing support tool
needs stricter gates than an internal learning demo.

## Key Takeaways

1. Build evals before training.
2. Compare against a real baseline.
3. Use task-specific metrics.
4. Keep the holdout test set clean.
5. Deploy gradually with rollback.
6. Monitor drift and regressions.
