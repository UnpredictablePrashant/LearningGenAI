# Session 08: Agent2Agent (A2A) Protocol

Build a practical mental model for the Agent2Agent protocol: how agents
discover each other, advertise capabilities, exchange messages, manage tasks,
stream updates, return artifacts, and enforce security boundaries.

As of May 13, 2026, the official A2A specification page lists latest released
version `1.0.0`.

## DevOps Analogy

| A2A Concept | DevOps Equivalent |
|-------------|-------------------|
| AgentCard | Service catalog entry / OpenAPI summary |
| Skill | Supported endpoint or operational capability |
| Message | Request payload sent between services |
| Part | Typed payload section: text, file, structured data |
| Task | Durable job or workflow execution |
| Artifact | Output object produced by a job |
| Streaming update | Server-sent progress event / watch stream |
| Push notification | Webhook callback for long-running work |
| JSON-RPC binding | RPC API over HTTP |
| Security schemes | AuthN/AuthZ contract for service calls |

## What You'll Learn

- Explain what A2A solves and when it is useful
- Compare A2A with MCP, tool calling, and internal agent orchestration
- Design an AgentCard with capabilities, skills, modalities, and security
- Model A2A messages using typed parts
- Track a task lifecycle from submission to completion or cancellation
- Return artifacts as structured outputs
- Understand JSON-RPC, HTTP+JSON/REST, and gRPC bindings at a practical level
- Simulate streaming task updates and asynchronous completion
- Apply authentication, authorization, versioning, and observability controls
- Build a small A2A-style gateway that routes requests to specialist agents

## Official References

- [A2A latest specification](https://a2a-protocol.org/latest/specification/)
- [A2A core protocol guide](https://agent2agent.info/specification/core/)
- [A2A core concepts](https://agent2agent.info/docs/concepts/)

## Prerequisites

```bash
pip install -r ../../requirements.txt

# No API key required for this session.
# Labs use Python standard library only.
```

Recommended previous sessions:

- Session 04 for tool calling and JSON schemas
- Session 05 for MCP servers and protocol thinking
- Session 06 for task state and agent memory
- Session 07 for retrieval systems that an A2A server agent might use internally

## Session Structure

```
08_agent2agent_a2a_protocol/
|-- concepts/
|   |-- 01_what_is_a2a.md
|   |-- 02_a2a_vs_mcp_tool_calling.md
|   |-- 03_agent_card_discovery.md
|   |-- 04_messages_parts_tasks_artifacts.md
|   |-- 05_protocol_bindings_json_rpc.md
|   |-- 06_streaming_async_push.md
|   |-- 07_security_governance_observability.md
|   `-- 08_designing_a2a_systems.md
|-- labs/
|   |-- lab01_agent_card_discovery/
|   |-- lab02_messages_tasks_artifacts/
|   |-- lab03_json_rpc_binding/
|   |-- lab04_streaming_and_async/
|   `-- lab05_gateway_security/
`-- demos/
    |-- demo_agent_card_discovery.py
    |-- demo_task_lifecycle.py
    `-- demo_a2a_gateway.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_agent_card_discovery | AgentCard design | skills, capabilities, modalities, auth hints |
| lab02_messages_tasks_artifacts | Core data model | Message, Part, Task, Artifact |
| lab03_json_rpc_binding | Protocol binding | JSON-RPC envelopes, method dispatch, errors |
| lab04_streaming_and_async | Long-running work | task states, events, SSE formatting |
| lab05_gateway_security | A2A gateway | discovery, routing, scopes, authorization |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_agent_card_discovery.py` | How clients inspect AgentCards and choose a compatible agent |
| `demo_task_lifecycle.py` | SendMessage, GetTask, CancelTask style lifecycle simulation |
| `demo_a2a_gateway.py` | A gateway routing requests to specialist agents with scope checks |

## Quick Start

```bash
cd sessions/08_agent2agent_a2a_protocol

# Read concepts first
cat concepts/01_what_is_a2a.md
cat concepts/02_a2a_vs_mcp_tool_calling.md
cat concepts/03_agent_card_discovery.md

# Run demos
python demos/demo_agent_card_discovery.py
python demos/demo_task_lifecycle.py
python demos/demo_a2a_gateway.py

# Work through labs
python labs/lab01_agent_card_discovery/lab.py
python labs/lab02_messages_tasks_artifacts/lab.py
python labs/lab03_json_rpc_binding/lab.py
python labs/lab04_streaming_and_async/lab.py
python labs/lab05_gateway_security/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 80 min |
| 5 labs | 140 min |
| Demos | 30 min |
| **Total** | **~4 hours** |

