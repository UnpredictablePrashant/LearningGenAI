# 01. Why Agents Need Memory

An LLM call is stateless by default. It only knows what is inside the current
prompt. An agent, however, usually runs across multiple steps, tools, files,
sessions, and decisions. That requires memory.

---

## DevOps Analogy First

Imagine an incident bridge where every engineer forgets the last five minutes.
People would repeat commands, page the wrong teams, lose context, and miss
important constraints.

Agent memory solves the same problem:

| Incident Response | Agentic AI |
|-------------------|------------|
| Bridge notes | Short-term memory |
| Runbooks | Procedural memory |
| CMDB / service catalog | Long-term memory |
| Incident timeline | Episodic memory |
| Postmortem action items | Reflective memory |
| Retention and redaction policy | Memory governance |

Memory is the agent's operational state.

---

## Stateless Chatbot vs Memory-Aware Agent

### Stateless chatbot

```
User: I prefer Python examples and concise lesson plans.
Assistant: Got it.

Later:
User: Create a session on tool calling.
Assistant: Here is a general explanation...
```

The preference disappears unless it is repeated in the prompt.

### Memory-aware agent

```
Stored memory:
user_pref.language = Python
user_pref.format = concise concept-demo-lab sessions

Later:
User: Create a session on tool calling.
Assistant: Uses Python examples and concept-demo-lab structure.
```

The agent retrieves memory before responding.

---

## Main Memory Types

| Memory Type | Question It Answers | Example |
|-------------|---------------------|---------|
| Short-term memory | What is happening right now? | Current task, recent turns, active plan |
| Long-term memory | What should be remembered across sessions? | User preferences, project facts, domain notes |
| Episodic memory | What happened before? | Previous session created, tools called, outcome |
| Reflective memory | What did we learn from what happened? | "Start with analogies before code for beginners." |
| Procedural memory | How should this task be done? | Steps for creating a lesson plan |

These are design categories. In code, they may all live in the same database,
but they should not be treated the same way.

---

## Why Memory Makes Agents Better

Memory helps agents:

1. Preserve continuity across steps.
2. Personalize output without repeating preferences.
3. Avoid retrying failed approaches.
4. Reuse proven workflows.
5. Ground answers in previous project context.
6. Explain why they made a decision.

Without memory, an agent has to infer everything from the latest prompt. That
makes long-running work brittle.

---

## Why Memory Makes Agents Riskier

Bad memory is worse than no memory.

Common failures:

- Storing sensitive data that should not be retained
- Retrieving irrelevant memories and polluting the prompt
- Treating outdated facts as current
- Letting the model invent memories
- Mixing user preference with hard policy
- Keeping too much conversation history instead of summarizing task state

Production memory needs clear write rules, retrieval rules, retention rules, and
inspection tools.

---

## Mental Model

Do not think of memory as "make the prompt bigger."

Think of it as a pipeline:

```
observe -> decide what to store -> store with metadata -> retrieve selectively -> use with confidence checks
```

Every step is an engineering decision.

