# 07. Security, Governance, and Observability

A2A connects independent agents. That means every A2A boundary is also a security
and operational boundary.

The official spec treats A2A agents as enterprise applications and relies on
standard web security practices such as HTTPS/TLS, authentication, and
authorization.

Reference: [A2A security section](https://a2a-protocol.org/latest/specification/#7-authentication-and-authorization)

## Security Baseline

Production A2A deployments should enforce:

- HTTPS or TLS
- Server identity verification
- Client authentication
- Authorization policies
- Input validation
- Output filtering
- Audit logging
- Rate limiting
- Tenant isolation

Do not let a model decide whether a request is authorized.

## AgentCard Security Schemes

The AgentCard should advertise security requirements so clients know what
credentials are needed.

Examples:

- API key
- OAuth 2.0 bearer token
- OpenID Connect
- Mutual TLS

The card tells clients what is required. The server still must enforce it on
every request.

## Authorization

Authentication answers:

```
Who is calling?
```

Authorization answers:

```
What is this caller allowed to do?
```

Authorization may depend on:

- Requested skill
- Tenant
- Data classification
- User role
- OAuth scopes
- Task action
- Output modality

Example:

```
scope: incidents:triage -> can request incident summaries
scope: incidents:remediate -> can request remediation plans
scope: incidents:execute -> can request action execution
```

## Prompt Injection and Tool Risk

An A2A server agent may receive untrusted text from another agent. Treat it as
data, not instructions.

Mitigations:

- Strong system boundaries inside the server agent
- Tool allowlists
- Schema validation
- Human approval for risky actions
- Explicit scopes for destructive operations
- No secret leakage in artifacts

## Observability

Log enough to debug and audit:

- Client identity
- AgentCard version
- Protocol version
- Request ID
- Task ID
- Context ID
- Method name
- Skill requested
- Input and output modalities
- State transitions
- Error codes
- Latency
- Artifact metadata

Avoid logging sensitive payloads unless policy allows it.

## Governance

A2A systems need operational policy:

- Which agents are trusted?
- Who owns each AgentCard?
- Who approves new skills?
- What version compatibility is required?
- Which tasks require human approval?
- What artifacts are retained?
- How are incidents traced across agent boundaries?

This is service governance applied to agents.

## Key Takeaways

1. A2A is an application boundary and must be secured like one.
2. Authentication is not authorization.
3. AgentCard security metadata is not enforcement by itself.
4. Task IDs, request IDs, and state transitions must be observable.
5. Risky agent actions require explicit policy outside the model.

