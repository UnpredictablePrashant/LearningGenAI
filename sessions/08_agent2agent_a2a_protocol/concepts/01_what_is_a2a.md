# 01. What Is A2A?

Agent2Agent (A2A) is an open protocol for communication between independent AI
agent systems. It gives agents a common way to discover each other, understand
capabilities, send messages, manage long-running tasks, and exchange results.

The official specification describes A2A as a protocol for interoperability
between independent and potentially opaque agent systems:

- Agents can be built with different frameworks.
- Agents can run in different organizations or trust domains.
- Agents do not need to expose internal memory, tools, prompts, or plans.
- Agents communicate through declared capabilities and protocol messages.

Reference: [A2A latest specification](https://a2a-protocol.org/latest/specification/)

## The Problem

Without a protocol, agent-to-agent integration becomes custom glue:

```
support-agent calls sre-agent through custom REST
sre-agent calls cloud-agent through a different SDK
cloud-agent returns a custom JSON shape
security-agent requires another auth pattern
```

Every new integration becomes a one-off adapter.

A2A gives those agents a common application-level contract.

## DevOps Analogy

Think about microservices.

Before service discovery, teams hard-coded hostnames and request formats. Mature
platforms introduced:

- Service catalogs
- OpenAPI specs
- Health checks
- Auth policies
- Tracing
- Versioning
- Standard error handling

A2A is similar, but for agent systems.

## Core Flow

Typical A2A flow:

```
client agent
  -> discover server agent's AgentCard
  -> inspect skills, modalities, auth, and endpoint
  -> send a Message
  -> receive or poll a Task
  -> stream or fetch task status
  -> receive Artifacts
```

The server agent owns execution. The client agent does not need to know how the
server agent thinks, which tools it uses, or which model powers it.

## Three-Layer Model

The A2A spec is organized around three layers:

1. Canonical data model
2. Abstract operations
3. Protocol bindings

The data model includes entities such as:

- `AgentCard`
- `Task`
- `Message`
- `Artifact`
- `Part`

The operation layer includes actions such as:

- `SendMessage`
- `SendStreamingMessage`
- `GetTask`
- `ListTasks`
- `CancelTask`
- `SubscribeToTask`
- Push notification configuration
- `GetExtendedAgentCard`

Protocol bindings map those ideas onto concrete transports such as JSON-RPC over
HTTP, gRPC, and HTTP+JSON/REST.

Reference: [A2A core protocol guide](https://agent2agent.info/specification/core/)

## Why "Opaque Agents" Matter

In A2A, an agent can collaborate without revealing:

- System prompt
- Chain of thought
- Internal tool inventory
- Private memory
- Vendor-specific runtime
- Internal workflow graph

This is important for enterprise systems. A finance agent can ask a compliance
agent for a review without getting access to the compliance agent's internal
policy store or private tools.

## When A2A Fits

Use A2A when:

- One agent delegates work to another independent agent.
- Agents belong to different teams, vendors, or trust domains.
- Tasks can be long-running.
- The interaction may produce files or structured artifacts.
- You need discovery and capability negotiation.
- You want a protocol boundary instead of direct code imports.

Examples:

- SRE agent delegates cost analysis to cloud-finops agent.
- Support agent asks a knowledge agent to investigate a customer case.
- Security agent asks a vulnerability agent to triage a CVE.
- Procurement agent asks a vendor agent for quote details.

## When A2A Is Too Much

Do not use A2A for everything.

For simple internal calls, a normal function call or direct Python method may be
enough. For tool access inside one agent, MCP or tool calling may be the better
fit. For shared libraries inside the same codebase, a protocol boundary can add
unnecessary complexity.

Use A2A when the boundary matters.

## Key Takeaways

1. A2A is about agent interoperability, not model prompting.
2. The main unit of durable work is a task.
3. AgentCards advertise capabilities and interaction requirements.
4. Messages and parts carry typed input.
5. Artifacts carry outputs.
6. A2A and MCP are complementary, not replacements for each other.

