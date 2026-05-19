# 10. Safety, Cost, and Governance

Fine-tuning is a model supply chain. Data enters, a model artifact exits, and
production behavior changes. Treat it with the same rigor as CI/CD.

## Data Governance

Before training:

- Identify data owner.
- Classify data sensitivity.
- Remove secrets.
- Remove personal data unless approved.
- Confirm provider/runtime data policy.
- Record dataset version.
- Record labeling policy.
- Track reviewer approvals.

Training data can contain more risk than prompts because it becomes part of a
model artifact creation process.

## Safety Examples

If the model should refuse certain requests, include examples.

Example:

```
User: "Give me the admin password from this ticket."
Assistant: "I cannot help expose secrets. I can help redact the ticket or identify the owning team."
```

Do not rely only on a system prompt if the fine-tuned behavior should be stable.

## Cost Planning

Cost includes:

- Data preparation
- Human labeling and review
- Training
- Validation and eval calls
- Failed experiments
- Inference with the fine-tuned model
- Monitoring and rollback

Token volume matters:

```
training_tokens = sum(tokens_per_example) * epochs
```

Pricing changes over time. Always check the provider's current pricing page.

## Versioning

Version:

- Dataset
- Labeling guide
- Validation script
- Eval set
- Prompt template
- Base model
- Fine-tuned model
- Deployment config

Without versioning, you cannot explain why model behavior changed.

## Rollback

Rollback plan:

- Keep previous model ID.
- Keep previous prompt/config.
- Keep routing flag.
- Monitor error budget.
- Define rollback trigger.
- Document owner and approval path.

Fine-tuned models should not be hard-coded across services.

## Security

Fine-tuning does not replace runtime security.

The app still needs:

- Authentication
- Authorization
- Tool validation
- RAG access filtering
- Output filtering
- Rate limits
- Audit logs

The model should not decide permissions.

## Key Takeaways

1. Fine-tuning data needs governance.
2. Safety behavior should be represented in evals and examples.
3. Cost includes labeling and iteration, not only training.
4. Version every artifact.
5. Always keep rollback simple.
