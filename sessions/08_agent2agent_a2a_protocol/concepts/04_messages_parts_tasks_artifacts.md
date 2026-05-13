# 04. Messages, Parts, Tasks, and Artifacts

A2A's core data model separates interaction payloads, durable work, and outputs.

The key objects:

- `Message`
- `Part`
- `Task`
- `Artifact`

## Message

A message is the communication unit between client and agent. It carries role,
content parts, metadata, and identifiers.

In practice, a message is like an HTTP request body or queue message sent to an
agent.

Example:

```json
{
  "role": "ROLE_USER",
  "messageId": "msg-001",
  "parts": [
    {"text": "Triage this Kubernetes CrashLoopBackOff incident."}
  ]
}
```

## Part

A part is a typed unit inside a message or artifact.

Common part categories:

- Text
- File reference
- Structured data

Why parts matter:

- Agents may handle text, files, and structured data differently.
- A task can include multiple pieces of evidence.
- Artifacts can return both narrative summaries and machine-readable data.

Example with structured data:

```json
{
  "role": "ROLE_USER",
  "parts": [
    {"text": "Summarize this incident."},
    {
      "data": {
        "incident_id": "INC-1001",
        "service": "payments",
        "symptom": "CrashLoopBackOff"
      }
    }
  ]
}
```

## Task

A task is the durable work unit.

A task needs:

- Server-generated ID
- Context ID
- Status
- Optional messages
- Optional artifacts
- Optional history

Long-running work should be represented as task state rather than a single
blocking request.

Common lifecycle:

```
submitted -> working -> input_required -> working -> completed
```

Other outcomes:

- failed
- canceled
- rejected
- unknown or unavailable, depending on implementation

The exact state names should follow the protocol version and SDK you are using.

## Artifact

An artifact is output produced by a task.

Examples:

- Text summary
- JSON report
- PDF
- Image
- CSV
- Remediation plan
- Terraform patch

Artifacts can contain parts, just like messages.

Example:

```json
{
  "artifactId": "artifact-001",
  "name": "incident_triage_report",
  "parts": [
    {"text": "The payment API is restarting because the DB password secret is missing."},
    {"data": {"root_cause": "missing_secret", "confidence": 0.82}}
  ]
}
```

## Why This Separation Matters

Messages are conversation payload.

Tasks are durable work state.

Artifacts are outputs.

Do not blur them. If a system stores final reports as messages only, clients have
to scrape conversation history. If it treats every message as a new task, it
cannot manage multi-turn workflows cleanly.

## Key Takeaways

1. Message carries interaction input.
2. Part is a typed piece of content.
3. Task is the durable unit of work.
4. Artifact is the output of task execution.
5. Good A2A systems keep these boundaries clear.

