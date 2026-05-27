# 05. Data Formats: SFT, DPO, and RFT

Fine-tuning method determines dataset format. Do not mix formats casually.

The OpenAI API reference states that fine-tuning files are uploaded as JSONL with
purpose `fine-tune`, and the contents differ depending on the model and method.

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

Common mistake: writing one large JSON array. Fine-tuning files usually expect
one complete object per line, not:

```json
[
  {"messages": []},
  {"messages": []}
]
```

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

The assistant output should be exactly the style and shape you want in
production. If production needs JSON, train on valid JSON. If production needs a
short answer, do not train on long essays.

## Prompt/Completion Format

Older datasets and many local examples use:

```json
{"prompt":"Tell me about number 8.","completion":"Number: 8\nParity: Even"}
```

This shape is easy to understand, but chat models usually need message-style
records. You can convert prompt/completion data to chat messages:

```python
def to_chat_record(row: dict) -> dict:
    return {
        "messages": [
            {"role": "system", "content": "Answer using the required number facts template."},
            {"role": "user", "content": row["prompt"]},
            {"role": "assistant", "content": row["completion"]},
        ]
    }
```

For local LoRA/QLoRA training, you may also format the same data as text:

```python
def to_training_text(row: dict) -> str:
    return (
        "### User:\n"
        f"{row['prompt']}\n\n"
        "### Assistant:\n"
        f"{row['completion']}"
    )
```

Same underlying dataset, different wrapper format.

## Classification Format

For classification, keep outputs constrained:

```json
{"label":"networking","confidence":0.91,"rationale":"The ticket mentions DNS and routing failures."}
```

Bad:

```text
I think this is maybe networking because DNS can be tricky.
```

The first output is easier to parse, score, and monitor.

## DPO Preference Format

Direct Preference Optimization uses preference pairs:

```text
prompt + chosen response + rejected response
```

Use it when you can compare two answers and say which is better.

Good for:

- Tone
- Summary focus
- Avoiding verbosity
- Choosing safer phrasing
- Preference alignment

Conceptual example:

```json
{
  "prompt": [{"role": "user", "content": "Summarize this incident."}],
  "chosen": [{"role": "assistant", "content": "Short, accurate summary..."}],
  "rejected": [{"role": "assistant", "content": "Verbose summary with speculation..."}]
}
```

Reference: [OpenAI DPO guide](https://platform.openai.com/docs/guides/direct-preference-optimization)

## RFT Format

Reinforcement fine-tuning uses a grader or reward signal. It is more complex and
is intended for tasks where expert grading can judge response quality.

Good for:

- Domain reasoning
- Legal or medical-style evaluations
- Multi-step decisions with expert scoring
- Cases where the exact target response is less important than a graded outcome

SFT says:

```text
Copy this ideal answer pattern.
```

RFT says:

```text
Try an answer, receive a score, and learn what scores well.
```

Reference: [OpenAI reinforcement fine-tuning guide](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)

## Vision Fine-Tuning

Vision fine-tuning includes image inputs and expected outputs. Use it when the
failure is in understanding images, not only text response style.

Example use cases:

- Product defect classification
- Document image extraction
- Visual inspection labels
- Domain-specific image descriptions

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
- No duplicate examples across train, validation, and holdout.

Minimal JSONL validator:

```python
import json
from pathlib import Path

def validate_jsonl(path: str) -> None:
    for line_number, line in enumerate(Path(path).read_text().splitlines(), start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: invalid JSON: {exc}") from exc

        messages = record.get("messages")
        if not isinstance(messages, list) or not messages:
            raise ValueError(f"line {line_number}: missing messages list")

        if messages[-1].get("role") != "assistant":
            raise ValueError(f"line {line_number}: final message must be assistant")
```

## Key Takeaways

1. JSONL is the file container.
2. SFT learns from ideal outputs.
3. DPO learns from preferences.
4. RFT learns from grader/reward feedback.
5. The same raw examples can be wrapped differently for OpenAI, LoRA, or QLoRA.
6. Dataset validation is not optional.
