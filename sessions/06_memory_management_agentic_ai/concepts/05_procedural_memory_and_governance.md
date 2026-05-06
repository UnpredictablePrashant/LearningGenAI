# 05. Procedural Memory and Governance

Procedural memory stores how to do a task. Governance defines what memory is
allowed to store, retrieve, and use.

---

## DevOps Analogy First

Procedural memory is a runbook:

```text
Procedure: Handle SEV1 authentication outage
1. Confirm customer impact
2. Page identity on-call
3. Check recent deploys
4. Review auth service health
5. Roll back if deploy is correlated
6. Post updates every 15 minutes
```

For agents, procedural memory is the reusable workflow that guides execution.

---

## What Procedural Memory Stores

Procedural memory can include:

- Step-by-step workflows
- Tool selection rules
- Output templates
- Quality checks
- Escalation rules
- Domain-specific playbooks

Example:

```json
{
  "name": "create_teaching_session",
  "steps": [
    "Define learning outcomes",
    "Explain concepts with a DevOps analogy",
    "Add runnable demos",
    "Create TODO-based labs",
    "Provide reference solutions",
    "Run syntax checks"
  ]
}
```

---

## Why Procedural Memory Is Different

Long-term memory stores facts:

```text
User prefers concept-demo-lab format.
```

Procedural memory stores behavior:

```text
When creating a session, produce README, concepts, demos, labs, and solutions.
```

One answers "what is true?" The other answers "what should I do?"

---

## Governance Questions

Any serious memory system needs answers to these questions:

| Question | Why It Matters |
|----------|----------------|
| What can be stored? | Prevents retaining secrets or sensitive data |
| Who can read memory? | Prevents cross-user leakage |
| How long is memory kept? | Supports retention and compliance |
| Can users inspect and delete memory? | Provides control and trust |
| How is confidence tracked? | Avoids treating weak memories as facts |
| How are stale memories handled? | Prevents outdated behavior |

---

## Memory Write Policy

Do not store every message. Use a policy.

Example policy:

```text
Store only:
- stable user preferences
- explicit project facts
- completed task episodes
- reflections from user feedback
- reusable procedures

Do not store:
- credentials
- raw private data
- temporary task chatter
- unverified claims
```

---

## Memory Retrieval Policy

Retrieval should be selective:

```text
For a lesson-planning request:
- Retrieve user preferences tagged "teaching"
- Retrieve procedure "create_teaching_session"
- Retrieve similar previous session episodes
- Retrieve reflections with apply_when matching "teaching"
- Ignore unrelated incident memories
```

---

## Design Rule

Procedural memory should answer:

> What workflow should the agent follow?

Governance should answer:

> Is this memory allowed, relevant, current, and safe to use?

