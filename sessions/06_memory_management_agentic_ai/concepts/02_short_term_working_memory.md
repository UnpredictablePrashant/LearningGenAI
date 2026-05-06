# 02. Short-Term Memory and Working State

Short-term memory is the agent's active workspace. It contains the information
needed to finish the current task, not everything the user has ever said.

---

## DevOps Analogy First

During an incident, the active bridge notes contain:

- Current hypothesis
- Commands already run
- Current owner
- Open questions
- Recent findings
- Next action

You would not paste the entire company wiki into bridge notes. You keep the
working set small and useful.

Short-term memory plays the same role for an agent.

---

## What Goes Into Short-Term Memory

Short-term memory often includes:

- Recent conversation turns
- Current task summary
- Active plan
- Tool outputs from the current run
- Constraints from the user
- Intermediate artifacts
- Open decisions

It is usually stored in the prompt context, a state object, or both.

---

## Context Window Is Not Memory Design

Large context windows are useful, but they do not remove the need for memory
management.

Problems with dumping all history into context:

- Cost grows with every turn
- Relevant facts get buried
- Old instructions can conflict with new ones
- Sensitive details stay active longer than needed
- The model may overfit to stale context

Working memory should be curated.

---

## Common Patterns

### Recent message buffer

Keep only the last N turns.

```python
recent_messages = messages[-8:]
```

Good for local coherence. Bad for long tasks unless paired with summaries.

### Rolling summary

Compress older turns into a task summary.

```python
working_memory = {
    "summary": "User is building a concept-demo-lab session on memory management.",
    "recent_messages": [...],
}
```

Good for long conversations. Risky if the summary drops important constraints.

### Task state object

Represent progress explicitly.

```python
task_state = {
    "goal": "Create Session 06",
    "completed": ["README", "concept files"],
    "remaining": ["labs", "demos", "verification"],
}
```

Good for agents that execute multi-step work.

---

## What Not To Store

Short-term memory should not keep:

- Secrets
- Full tool logs when a small result summary is enough
- Every previous conversation turn
- Irrelevant user chatter
- Reflections meant for future sessions
- Durable user preferences that belong in long-term memory

---

## Prompt Assembly Pattern

A memory-aware agent often builds the prompt like this:

```text
System instructions

Relevant long-term memories

Current task summary

Recent messages

Latest user request
```

Short-term memory is only one part of the assembled context.

---

## Design Rule

Short-term memory should answer:

> What does the agent need to know right now to make the next correct move?

If a detail does not help the next move, summarize it, archive it as an episode,
or drop it.

