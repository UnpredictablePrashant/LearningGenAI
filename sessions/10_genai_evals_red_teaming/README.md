# Session 10: GenAI Evals and Red Teaming

Build evaluation systems for prompts, RAG pipelines, tool-using agents, and
fine-tuned models. The goal is to move from "the demo looked good" to a repeatable
quality gate that catches regressions before users do.

## DevOps Analogy

| GenAI Eval Concept | DevOps Equivalent |
|--------------------|-------------------|
| Golden dataset | Regression test suite |
| Grader | CI assertion |
| Human review rubric | Pull request review checklist |
| Red-team case | Chaos/security test |
| Trace eval | Distributed trace analysis |
| Eval report | Release readiness report |

## What You'll Learn

- Separate task accuracy, format compliance, groundedness, safety, and latency
- Build small golden datasets before changing prompts, models, tools, or RAG indexes
- Use deterministic graders when the output contract is strict
- Use rubric and LLM-as-judge style graders only when deterministic scoring is not enough
- Red-team prompt injection, over-refusal, excessive agency, data leakage, and tool misuse
- Evaluate agent traces, not only final answers
- Turn eval results into deployment gates

## Official References

- [OpenAI evals guide](https://developers.openai.com/api/docs/guides/evals)
- [OpenAI agent evals guide](https://developers.openai.com/api/docs/guides/agent-evals)
- [OpenAI red teaming guide](https://developers.openai.com/api/docs/guides/red-teaming)
- [OpenAI graders guide](https://developers.openai.com/api/docs/guides/graders)

## Prerequisites

```bash
pip install -r ../../requirements.txt

# No API key required for the core lab.
# Optional extensions can use provider eval APIs later.
```

Recommended previous sessions:

- Session 02 for prompt testing
- Session 04 for tool calling
- Session 07 for RAG quality metrics
- Session 09 for fine-tuning eval hygiene

## Session Structure

```text
10_genai_evals_red_teaming/
|-- concepts/
|   |-- 01_eval_design.md
|   `-- 02_red_teaming_and_trace_evals.md
|-- labs/
|   `-- lab01_eval_scorecard/
`-- demos/
    `-- demo_eval_scorecard.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_eval_scorecard | Build a simple eval scorecard | deterministic graders, safety cases, release gates |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_eval_scorecard.py` | How accuracy, format, safety, and latency combine into a release decision |

## Quick Start

```bash
cd sessions/10_genai_evals_red_teaming

cat concepts/01_eval_design.md
cat concepts/02_red_teaming_and_trace_evals.md

python demos/demo_eval_scorecard.py
python labs/lab01_eval_scorecard/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 35 min |
| Lab | 45 min |
| Demo | 10 min |
| **Total** | **~90 min** |

