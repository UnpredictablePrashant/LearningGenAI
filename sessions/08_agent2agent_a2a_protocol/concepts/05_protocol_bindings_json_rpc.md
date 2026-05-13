# 05. Protocol Bindings and JSON-RPC

A2A defines abstract operations, then maps them to concrete protocol bindings.

The official specification lists JSON-RPC over HTTP, gRPC, and HTTP+JSON/REST as
protocol bindings. This session focuses on JSON-RPC because it is easy to model
with plain Python.

Reference: [A2A latest specification](https://a2a-protocol.org/latest/specification/)

## JSON-RPC Mental Model

JSON-RPC sends a method name and parameters in a standard envelope:

```json
{
  "jsonrpc": "2.0",
  "id": "request-001",
  "method": "SendMessage",
  "params": {
    "message": {
      "role": "ROLE_USER",
      "parts": [{"text": "Summarize incident INC-1001"}],
      "messageId": "msg-001"
    }
  }
}
```

The response uses the same request ID:

```json
{
  "jsonrpc": "2.0",
  "id": "request-001",
  "result": {
    "task": {
      "id": "task-001",
      "status": {"state": "TASK_STATE_SUBMITTED"}
    }
  }
}
```

## Core Methods

Common A2A operations include:

- `SendMessage`
- `SendStreamingMessage`
- `GetTask`
- `ListTasks`
- `CancelTask`
- `SubscribeToTask`
- Push notification config operations
- `GetExtendedAgentCard`

The exact method names and payload shapes should follow the current spec and SDK.

## HTTP Headers

The JSON-RPC binding runs over HTTP(S). Protocol service parameters can travel as
headers, including:

- `A2A-Version`
- `A2A-Extensions`

Production requests also need normal security headers:

- `Authorization`
- Correlation or trace IDs
- Content type

## Error Handling

JSON-RPC has standard error codes:

- Parse error
- Invalid request
- Method not found
- Invalid params
- Internal error

A2A adds protocol-specific errors for cases like:

- Task not found
- Task not cancelable
- Push notifications not supported
- Unsupported operation
- Unsupported content type

Good clients should distinguish:

- Retryable server error
- Permanent validation error
- Authorization failure
- Missing task
- Unsupported feature

## Version Compatibility

The A2A docs call out protocol-version governance as important. A client should
not assume every server supports the same version or optional extensions.

Practical checks:

- Fetch AgentCard.
- Validate protocol version.
- Validate capability flags.
- Send `A2A-Version` where required by the binding.
- Have tests for version mismatch.

## Key Takeaways

1. A2A data model is transport-independent.
2. Bindings map operations onto JSON-RPC, gRPC, or HTTP+JSON/REST.
3. JSON-RPC uses a simple method/params envelope.
4. Error mapping and version negotiation are production concerns.
5. Header handling matters for version, extensions, auth, and tracing.

