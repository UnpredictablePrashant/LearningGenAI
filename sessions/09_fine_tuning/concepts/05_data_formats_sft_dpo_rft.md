# 05. Data Formats: SFT, DPO, and RFT

Fine-tuning method determines dataset format. Do not mix formats casually.

The OpenAI API reference states that fine-tuning files are uploaded as JSONL with
purpose `fine-tune`, and the contents differ depending on the model/method.

Reference: [OpenAI fine-tuning API reference](https://platform.openai.com/docs/api-reference/fine-tuning)

## JSONL

JSONL means one JSON object per line:

```jsonl
{"messages":[{"role":"user","content":"..."}]}
{"messages":[{"role":"user","content":"..."}]}
```

Why JSONL:

- Streamable
- Easy to validate line by line
- Works for large datasets
- One bad line can be reported precisely

## SFT Chat Format

Supervised fine-tuning teaches the model desired outputs.

Typical chat example:

```json
{
  "messages": [
    {"role": "system", "content": "You classify cloud support tickets."},
    {"role": "user", "content": "RDS connection timeout from EKS pods."},
    {"role": "assistant", "content": "{\"label\":\"database\",\"confidence\":0.86}"}
  ]
}
```

The assistant output should be exactly the style and shape you want in production.

## Classification Format

For classification, keep outputs constrained:

```json
{"label":"networking","confidence":0.91,"rationale":"The ticket mentions DNS and routing failures."}
```

Bad:

```text
I think this is maybe networking because DNS can be tricky.
```

If production needs JSON, train on valid JSON.

## DPO Preference Format

Direct Preference Optimization uses preference pairs:

```
prompt + chosen response + rejected response
```

Use it when you can compare two answers and say which is better.

Good for:

- Tone
- Summary focus
- Avoiding verbosity
- Choosing safer phrasing
- Preference alignment

Reference: [OpenAI DPO guide](https://platform.openai.com/docs/guides/direct-preference-optimization)

## RFT Format

Reinforcement fine-tuning uses a grader or reward signal. It is more complex and
is intended for tasks where expert grading can judge response quality.

Good for:

- Domain reasoning
- Legal or medical-style evaluations
- Multi-step decisions with expert scoring
- Cases where the exact target response is less important than a graded outcome

Reference: [OpenAI reinforcement fine-tuning guide](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)

## Vision Fine-Tuning

Vision fine-tuning includes image inputs and expected outputs. Use it when the
failure is in understanding images, not only text response style.

Reference: [OpenAI vision fine-tuning guide](https://platform.openai.com/docs/guides/vision-fine-tuning)

## Validation Rules

Validate:

- Every line is valid JSON.
- Required keys exist.
- Messages are in a supported shape.
- Roles are allowed.
- Assistant target exists for SFT.
- Output schema is valid.
- No empty content.
- No secrets.
- Token length is within model limits.
- No duplicate examples across train/validation/holdout.

## Key Takeaways

1. JSONL is the file container.
2. SFT learns from ideal outputs.
3. DPO learns from preferences.
4. RFT learns from grader/reward feedback.
5. Dataset validation is not optional.
