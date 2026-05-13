# 03. AgentCard and Discovery

An AgentCard is the agent's public contract. It tells clients what the agent is,
where it is, what it can do, which modalities it supports, and how to authenticate.

The official docs describe AgentCard as the concept clients inspect to understand
an agent's capabilities.

Reference: [A2A core concepts](https://agent2agent.info/docs/concepts/)

## DevOps Analogy

An AgentCard is like a service catalog record plus a compact API summary:

- Service name
- Owner or provider
- Endpoint URL
- Supported operations
- Auth requirements
- Version
- Tags
- Input/output media types
- Optional capabilities

Without this, clients need out-of-band knowledge.

## What an AgentCard Should Answer

Before sending a task, a client should be able to answer:

- What is this agent called?
- What does it do?
- Where do I send requests?
- Which protocol version does it support?
- Which skills are available?
- What input and output modalities are supported?
- Does it support streaming?
- Does it support push notifications?
- Does it require authentication?
- Is there an extended authenticated card?

## Skills

Skills are the advertised capabilities of the agent.

Example skill:

```json
{
  "id": "incident_triage",
  "name": "Incident triage",
  "description": "Triage cloud and Kubernetes incidents.",
  "tags": ["sre", "incident", "kubernetes"],
  "inputModes": ["text/plain", "application/json"],
  "outputModes": ["text/plain", "application/json"]
}
```

Good skills are specific enough for routing. Weak skills are vague:

```
"does AI stuff"
"helps users"
"answers questions"
```

## Capabilities

Capabilities describe optional protocol features.

Common examples:

- Streaming support
- Push notification support
- State transition history
- Extended AgentCard support

In current v1.0-era docs, extended AgentCard support is represented under
capabilities rather than as a top-level `AgentCard` field.

## Public vs Extended Agent Cards

A public AgentCard can be intentionally limited. It may reveal only enough for
discovery.

An extended AgentCard can require authentication and reveal more:

- Internal-only skills
- Higher-risk actions
- Better descriptions
- Tenant-specific capabilities
- Additional output formats

This mirrors public service discovery versus authenticated service metadata.

## Discovery Mechanisms

Common discovery pattern:

```
GET /.well-known/agent-card.json
```

A client can fetch the card, cache it, inspect it, and then decide whether to
send a request.

The official spec also discusses caching headers such as `Cache-Control`, `ETag`,
and `Last-Modified` for AgentCard endpoints.

Reference: [A2A latest specification](https://a2a-protocol.org/latest/specification/)

## Client Selection Logic

Client-side discovery should validate:

- Required protocol version
- Required input mode
- Required output mode
- Required skill
- Security scheme compatibility
- Endpoint trust

Example decision:

```
Need: "summarize incident timeline"
Required input: application/json
Required output: text/plain

Candidate agents:
  incident-agent: yes
  cost-agent: no matching skill
  doc-agent: wrong output mode
```

## Key Takeaways

1. AgentCard is the entry point for A2A discovery.
2. Skills should be specific and routable.
3. Capabilities advertise optional features like streaming and push notifications.
4. Discovery should validate compatibility before sending a task.
5. Public cards can be limited; extended cards can require authentication.

