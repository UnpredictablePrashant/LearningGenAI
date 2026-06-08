# Session 16: GenAI Observability

Instrument GenAI systems so you can debug, evaluate, audit, and improve them in
production. This session focuses on traces, metrics, structured logs, and
OpenTelemetry-style semantic attributes.

## DevOps Analogy

| GenAI Observability Concept | DevOps Equivalent |
|-----------------------------|-------------------|
| Model span | Downstream service span |
| Tool span | Dependency call span |
| Retrieval span | Database/search query span |
| Token metrics | Request/byte metrics |
| Prompt version | Build SHA or config version |
| Trace eval | Trace-based SLO check |
| Redaction | Sensitive log filtering |

## What You'll Learn

- Decide which GenAI events should become spans, metrics, or logs
- Track prompt, model, tool, retrieval, and memory metadata
- Redact sensitive prompts and tool outputs before logging
- Correlate model calls with tool calls and user-visible outcomes
- Use token, latency, cache, and error metrics for operations
- Connect observability to evals and incident review

## Official References

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [OpenAI Agents SDK integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability)
- [OpenAI production best practices](https://developers.openai.com/api/docs/guides/production-best-practices)

## Prerequisites

```bash
pip install -r ../../requirements.txt

# No API key required.
# The core lab builds trace records with Python dictionaries.
```

Recommended previous sessions:

- Session 04 for tool spans
- Session 07 for retrieval spans
- Session 10 for eval-linked traces
- Session 11 for production metrics
- Session 13 for agent traces

## Session Structure

```text
16_genai_observability/
|-- concepts/
|   |-- 01_traces_metrics_logs.md
|   `-- 02_otel_genai_semantics.md
|-- labs/
|   `-- lab01_trace_builder/
`-- demos/
    `-- demo_trace_waterfall.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_trace_builder | Build a GenAI trace record | spans, attributes, redaction, token metrics |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_trace_waterfall.py` | A readable waterfall for retrieval, model, and tool spans |

## Quick Start

```bash
cd sessions/16_genai_observability

cat concepts/01_traces_metrics_logs.md
cat concepts/02_otel_genai_semantics.md

python demos/demo_trace_waterfall.py
python labs/lab01_trace_builder/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 35 min |
| Lab | 45 min |
| Demo | 10 min |
| **Total** | **~90 min** |
