# 01. Eval Design

An eval is a repeatable test for model behavior. It should exist before a major
prompt, model, RAG, tool, or fine-tuning change.

## Why Evals Matter

Manual demos hide variance. A model may pass the happy path and still fail on:

- Edge cases
- Ambiguous inputs
- Missing evidence
- Output formatting
- Safety policy
- Tool misuse
- Latency or cost constraints

Treat evals like CI. They are not proof that the system is perfect. They are a
regression net that makes behavior visible.

## Eval Layers

| Layer | What It Measures | Example |
|-------|------------------|---------|
| Task quality | Did the answer solve the task? | Correct incident severity |
| Format compliance | Can downstream code parse it? | Valid JSON with required keys |
| Groundedness | Is the answer supported by evidence? | Citations match retrieved chunks |
| Safety | Did it respect policy? | Refuses secret exfiltration |
| Tool behavior | Did it call the right tools safely? | Read-only before write |
| Trace behavior | Did the workflow follow expected steps? | Retrieval before diagnosis |
| Operations | Is it affordable and fast enough? | p95 latency below budget |

## Golden Dataset

A good golden set is small, versioned, and representative.

Start with 20 to 50 cases:

- 10 common cases
- 5 edge cases
- 5 unsafe/adversarial cases
- 5 missing-information cases
- 5 regression cases from real bugs

Each case should include:

- Input
- Expected behavior
- Scoring rule
- Tags
- Owner
- Reason it exists

## Grader Types

Use the simplest grader that works.

| Grader | Use When | Risk |
|--------|----------|------|
| Exact match | Output has a small finite set | Too strict for prose |
| JSON schema | Output must feed a pipeline | Does not check quality |
| Regex/rule | Policy or format is simple | Brittle if overused |
| Retrieval metric | RAG source selection matters | Does not grade final answer |
| Rubric | Human quality matters | Requires reviewer calibration |
| LLM judge | Open-ended outputs at scale | Needs bias checks and spot review |

## Release Gate

An eval should end in a decision:

```text
Ship only if:
- critical safety failures = 0
- JSON validity >= 0.98
- task accuracy >= baseline + target delta
- groundedness >= target
- p95 latency <= budget
- cost per successful answer <= budget
```

## Key Takeaways

1. Evals are product tests, not model trivia.
2. Score dimensions separately.
3. Keep golden cases versioned with the prompt, model, and retrieval index.
4. Add a regression case every time a real failure is found.

