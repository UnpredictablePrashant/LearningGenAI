# 04. Episodic and Reflective Memory

Episodic memory stores what happened. Reflective memory stores what was learned.
They are related, but they are not the same thing.

---

## DevOps Analogy First

In incident management:

- The incident timeline is episodic memory.
- The postmortem lessons learned are reflective memory.

The timeline says:

```text
14:03 - Deployment started
14:07 - Error rate increased
14:10 - Rolled back service
14:15 - Error rate recovered
```

The reflection says:

```text
Canary checks did not include payment callback errors. Add callback SLI to release gates.
```

Agents need both.

---

## Episodic Memory

Episodic memory records an agent's past experience:

```json
{
  "goal": "Create a session on MCP servers",
  "actions": ["Created concepts", "Added FastMCP labs", "Ran syntax checks"],
  "outcome": "completed",
  "lesson": "Students need a clear comparison with function calling."
}
```

It helps answer:

- Have we done something similar before?
- What was attempted?
- What worked?
- What failed?
- What artifacts were produced?

---

## Reflective Memory

Reflective memory extracts a reusable insight:

```json
{
  "insight": "When teaching new Agentic AI topics, start with a DevOps analogy.",
  "apply_when": "Creating future sessions for cloud and DevOps engineers",
  "confidence": 0.85
}
```

It helps future behavior improve without replaying every old event.

---

## Reflection Loop

A simple reflection loop runs after a task:

```
goal + actions + outcome + feedback -> reflection -> long-term storage
```

Useful reflection questions:

1. Did the task meet the user's goal?
2. What assumption was wrong?
3. Which step created the most value?
4. What should be reused next time?
5. What should be avoided next time?

---

## Failure Modes

Episodic memory failures:

- Stores too much raw detail
- Does not capture outcome
- Cannot be searched by goal or tags
- Logs sensitive tool outputs

Reflective memory failures:

- Converts one event into an overgeneralized rule
- Stores a model hallucination as a lesson
- Keeps stale preferences forever
- Treats weak feedback as strong evidence

---

## Design Rule

Episodic memory should answer:

> What happened before?

Reflective memory should answer:

> What should change because of what happened before?

Keep the event and the lesson separate.

