# Session 11: LLMOps and Production GenAI

Operate GenAI applications like production services: budgeted, observable,
resilient, rate-limit aware, and deployable through controlled release gates.

## DevOps Analogy

| LLMOps Concept | DevOps Equivalent |
|----------------|-------------------|
| Model gateway | API gateway / service mesh |
| Rate limit | Upstream quota |
| Retry with backoff | Resilient client policy |
| Fallback model | Multi-region failover |
| Prompt cache | CDN/cache hit |
| Batch processing | Async job queue |
| Cost budget | Cloud spend guardrail |
| Release gate | CI/CD approval |

## What You'll Learn

- Estimate token, latency, and cost budgets before launch
- Design retry, timeout, fallback, and circuit breaker policies
- Decide when to use synchronous calls, background work, or batch jobs
- Use prompt caching and context compaction to reduce repeated input cost
- Track model, prompt, dataset, and eval versions
- Build deployment gates for accuracy, safety, cost, and latency
- Plan incident response for model/API degradation

## Official References

- [OpenAI production best practices](https://developers.openai.com/api/docs/guides/production-best-practices)
- [OpenAI deployment checklist](https://developers.openai.com/api/docs/guides/deployment-checklist)
- [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- [OpenAI Batch API](https://developers.openai.com/api/docs/guides/batch)
- [OpenAI cost optimization](https://developers.openai.com/api/docs/guides/cost-optimization)

## Prerequisites

```bash
pip install -r ../../requirements.txt

# No API key required for the core lab.
# Optional production experiments can use OPENAI_API_KEY or another provider.
```

Recommended previous sessions:

- Session 04 for provider-compatible tool loops
- Session 07 for RAG production constraints
- Session 10 for eval gates

## Session Structure

```text
11_llmops_production_genai/
|-- concepts/
|   |-- 01_operating_model_apis.md
|   `-- 02_cost_latency_resilience.md
|-- labs/
|   `-- lab01_budget_router/
`-- demos/
    `-- demo_cost_latency_router.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_budget_router | Pick a model route under constraints | budgets, retries, fallbacks, batch decisions |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_cost_latency_router.py` | Route requests by quality, latency, and cost budget |

## Quick Start

```bash
cd sessions/11_llmops_production_genai

cat concepts/01_operating_model_apis.md
cat concepts/02_cost_latency_resilience.md

python demos/demo_cost_latency_router.py
python labs/lab01_budget_router/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 35 min |
| Lab | 45 min |
| Demo | 10 min |
| **Total** | **~90 min** |

