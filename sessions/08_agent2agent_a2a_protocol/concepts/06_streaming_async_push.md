# 06. Streaming, Async, and Push Notifications

A2A is designed for work that may not complete immediately. Some tasks take
seconds. Others take minutes and involve external systems or humans.

This is why task state matters.

## Why Async Matters

Agent work can include:

- Reading documents
- Calling tools
- Waiting for approvals
- Running diagnostics
- Generating files
- Coordinating with another team or agent

Blocking one HTTP request until everything finishes is fragile.

## Polling

Simple async pattern:

```
SendMessage -> task id
GetTask(task id) -> submitted
GetTask(task id) -> working
GetTask(task id) -> completed with artifacts
```

Polling is easy to implement and debug. It is inefficient for many long-running
tasks because clients repeatedly ask for status.

## Streaming

Streaming sends updates as the task progresses.

The JSON-RPC binding uses Server-Sent Events for streaming according to the
official spec.

Reference: [JSON-RPC protocol binding](https://a2a-protocol.org/latest/specification/#9-json-rpc-protocol-binding)

Example event sequence:

```text
event: task_status
data: {"taskId": "task-001", "state": "TASK_STATE_WORKING"}

event: artifact_delta
data: {"taskId": "task-001", "text": "Checking security groups..."}

event: task_status
data: {"taskId": "task-001", "state": "TASK_STATE_COMPLETED"}
```

## Push Notifications

Push notification flow:

```
client configures callback
server processes long task
server calls callback when state changes or completes
```

This is useful when:

- Tasks are very long.
- Clients cannot keep a stream open.
- Completion needs to wake another workflow.

Push notifications require stronger security thinking:

- Verify callback ownership.
- Sign callbacks.
- Prevent SSRF.
- Retry safely.
- Deduplicate events.

## State Transition History

State transition history helps debugging:

```json
[
  {"state": "TASK_STATE_SUBMITTED", "timestamp": "..."},
  {"state": "TASK_STATE_WORKING", "timestamp": "..."},
  {"state": "TASK_STATE_INPUT_REQUIRED", "timestamp": "..."},
  {"state": "TASK_STATE_COMPLETED", "timestamp": "..."}
]
```

This is the agent equivalent of job history in CI/CD.

## Client Behavior

Clients should handle:

- Task completes normally.
- Task asks for more input.
- Task fails.
- Task is canceled.
- Stream disconnects.
- Server returns unknown task.
- Version or extension mismatch.

Do not assume a stream will always end cleanly. Persist task IDs and support
recovery with `GetTask`.

## Key Takeaways

1. A2A treats long-running work as a first-class concern.
2. Polling is simple; streaming improves responsiveness.
3. Push notifications are powerful but security-sensitive.
4. Clients need recovery logic for disconnected streams.
5. Task history is critical for debugging and auditability.

