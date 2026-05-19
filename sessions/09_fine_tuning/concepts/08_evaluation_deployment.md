# 08. Evaluation and Deployment

Fine-tuning without evals is guessing. You need a baseline before training and a
gate before deployment.

## Eval Sets

Use three splits:

- Training set: used for learning
- Validation set: used during training and iteration
- Holdout set: used only for final evaluation

Never tune repeatedly against the holdout set. It stops being a true holdout.

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
6. Canary small percentage.
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

## Key Takeaways

1. Build evals before training.
2. Compare against a real baseline.
3. Use task-specific metrics.
4. Deploy gradually with rollback.
5. Monitor drift and regressions.

