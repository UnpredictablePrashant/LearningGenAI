# Session 13: Modern Agent Runtime

Build a practical mental model for modern agent runtimes: stateful Responses-style
APIs, agent SDKs, graph workflows, guardrails, handoffs, traces, and durable task
state.

## DevOps Analogy

| Agent Runtime Concept | DevOps Equivalent |
|-----------------------|-------------------|
| Agent definition | Service deployment spec |
| Tool | Downstream API |
| Handoff | Service-to-service delegation |
| Guardrail | Admission controller |
| Trace | Distributed trace |
| Agent state | Workflow state |
| Background run | Async job |
| Human approval | Manual gate in a pipeline |

## What You'll Learn

- Compare direct API calls, tool loops, SDK agents, and graph workflows
- Understand why state, trace, and guardrails belong in the runtime
- Design agent handoffs with typed inputs and outputs
- Keep durable task state outside the model
- Add human approval states for risky actions
- Evaluate agent traces as part of the release process
- Connect this runtime thinking to the multi-agent project guide

## Official References

- [OpenAI Responses API migration guide](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents)
- [OpenAI Agents SDK guardrails and approvals](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals)
- [LangGraph workflows and agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

## Prerequisites

```bash
pip install -r ../../requirements.txt

# No API key required for the core lab.
```

Recommended previous sessions:

- Session 04 for tool calling
- Session 05 for MCP
- Session 06 for memory
- Session 08 for A2A
- Session 10 for agent evals

## Session Structure

```text
13_modern_agent_runtime/
|-- concepts/
|   |-- 01_runtime_patterns.md
|   `-- 02_state_guardrails_handoffs.md
|-- labs/
|   `-- lab01_agent_trace_contract/
`-- demos/
    `-- demo_agent_runtime_trace.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_agent_trace_contract | Build a trace contract | steps, tools, guardrails, handoffs |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_agent_runtime_trace.py` | A minimal stateful agent trace without external APIs |

## Quick Start

```bash
cd sessions/13_modern_agent_runtime

cat concepts/01_runtime_patterns.md
cat concepts/02_state_guardrails_handoffs.md

python demos/demo_agent_runtime_trace.py
python labs/lab01_agent_trace_contract/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 40 min |
| Lab | 45 min |
| Demo | 10 min |
| **Total** | **~95 min** |
