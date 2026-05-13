# 08. Designing A2A Systems

An A2A system is a network of agents with explicit boundaries. Good design is
less about making agents talk and more about making collaboration reliable,
secure, observable, and debuggable.

## Start With Boundaries

Before adding A2A, ask:

- Is this callee really an independent agent?
- Does it own a workflow?
- Does it need to hide internal implementation?
- Does it have a different owner, trust boundary, or lifecycle?
- Does task state matter?

If the answer is no, a direct function, API endpoint, or MCP tool may be simpler.

## Common Topologies

### Broker/Gateway

```
user-facing agent -> A2A gateway -> specialist agents
```

Useful when:

- Clients should not know every specialist agent.
- Routing policy is centralized.
- Auth and audit need one entry point.

### Peer-to-Peer

```
agent A -> agent B
agent B -> agent C
```

Useful when:

- Agents discover each other directly.
- Teams own independent endpoints.
- Collaboration paths are dynamic.

Harder to govern.

### Orchestrator

```
orchestrator agent
  -> planner agent
  -> retrieval agent
  -> execution agent
  -> review agent
```

Useful for complex workflows. Requires strong task tracing and failure handling.

## Designing Skills

Good skills are:

- Specific
- Routable
- Versioned when behavior changes
- Clear about input/output modes
- Clear about side effects
- Scoped by authorization policy

Bad skill:

```
"help"
```

Better skills:

```
"incident_triage"
"cloud_cost_anomaly_analysis"
"terraform_plan_review"
"vulnerability_impact_assessment"
```

## Task Contract

Define what a task means:

- What starts the task?
- What input is required?
- Which states can occur?
- What artifacts are returned?
- Can it ask for more input?
- Can it be canceled?
- How long can it run?
- What errors are retryable?

If this is unclear, clients will build brittle assumptions.

## Failure Design

Plan failures:

- Agent unavailable
- Unsupported skill
- Unsupported modality
- Auth expired
- Task not found
- Task canceled
- Task failed after partial output
- Stream disconnected
- Artifact unavailable
- Version mismatch

Good clients recover by using task IDs and explicit error handling.

## Compatibility

Compatibility requires discipline:

- Version AgentCards.
- Use protocol version headers where appropriate.
- Avoid breaking skill semantics silently.
- Add capabilities instead of changing behavior in place.
- Keep migration tests.
- Cache AgentCards carefully and refresh on version changes.

## Evaluation

Evaluate A2A systems on:

- Correct routing
- Correct skill selection
- Successful task completion
- Artifact quality
- Latency
- Error handling
- Security policy enforcement
- Trace completeness

Do not only evaluate answer quality. Evaluate protocol behavior.

## Key Takeaways

1. Use A2A when an agent boundary is valuable.
2. AgentCards and skills are product contracts, not documentation afterthoughts.
3. Task lifecycle design matters as much as message payload design.
4. Gateways can simplify policy and observability.
5. Production A2A needs versioning, failure handling, and audits.

