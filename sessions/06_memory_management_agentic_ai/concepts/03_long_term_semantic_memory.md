# 03. Long-Term and Semantic Memory

Long-term memory stores information that should survive beyond the current
conversation. Semantic memory is long-term memory organized by meaning, so the
agent can retrieve relevant facts even when the user uses different words.

---

## DevOps Analogy First

Long-term memory is like your persistent operational knowledge:

- Runbooks
- Architecture docs
- Service ownership
- Previous design decisions
- User preferences
- Known limitations
- Troubleshooting notes

You do not load all of it into every incident bridge. You search and retrieve
the parts that matter.

---

## What Belongs in Long-Term Memory

Good candidates:

- Stable user preferences
- Project-specific facts
- Team conventions
- Domain terminology
- Reusable examples
- Decisions and rationale
- Curated knowledge base snippets

Poor candidates:

- Raw secrets
- Temporary task state
- Unverified claims
- One-off messages with no future value
- Data that has a strict retention requirement unless the system enforces it

---

## Memory Record Shape

A useful memory record needs more than text.

```json
{
  "id": "mem-001",
  "kind": "user_preference",
  "text": "User prefers teaching sessions in concept-demo-lab format.",
  "source": "conversation",
  "created_at": "2026-05-06T10:00:00Z",
  "confidence": 0.9,
  "tags": ["teaching", "format"]
}
```

Metadata supports filtering, trust decisions, retention, and debugging.

---

## Retrieval Flow

Typical semantic memory retrieval:

```
new request -> embed query -> search memory vectors -> filter by metadata -> inject top results
```

The search step finds candidates. The filtering step decides what is allowed and
useful.

---

## Over-Retrieval Problem

Retrieving too much memory can make an agent worse.

Symptoms:

- The answer mentions unrelated preferences
- Old project facts override current instructions
- The prompt becomes expensive
- The model follows irrelevant examples

Production systems usually cap memory injection:

- top 3 to 8 memories
- minimum similarity threshold
- recency or confidence filters
- memory type filters

---

## Semantic vs Exact Retrieval

Exact retrieval:

```
query: lesson format
match: lesson format
```

Semantic retrieval:

```
query: how should I structure the next class?
match: User prefers concept-demo-lab sessions.
```

Semantic retrieval is powerful because users rarely repeat exact wording.

---

## Design Rule

Long-term memory should answer:

> What durable knowledge is relevant to this request, and is it trustworthy enough to use?

Do not use memory just because it exists. Retrieve, filter, and cite internally.

