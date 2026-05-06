# Session 06: Memory Management in Agentic AI

Teach agents to remember the right things, forget the wrong things, and use memory
as a controlled part of the agent loop.

## DevOps Analogy

| Agent Memory Concept | DevOps Equivalent |
|----------------------|-------------------|
| Short-term memory | Current incident bridge notes / active terminal state |
| Long-term memory | Runbook library / CMDB / knowledge base |
| Episodic memory | Incident timeline / postmortem event log |
| Reflective memory | Postmortem lessons learned |
| Procedural memory | Standard operating procedure / runbook workflow |
| Memory retrieval | Searching logs, docs, and previous incidents before acting |
| Memory governance | Retention, access control, redaction, audit logs |

## What You'll Learn

- Separate working context from durable memory
- Decide what belongs in short-term, long-term, episodic, reflective, and procedural memory
- Build a rolling short-term memory buffer
- Retrieve long-term memories with vector-style similarity
- Store episodes and convert them into useful reflections
- Combine all memory types into a simple teaching agent
- Avoid common memory failures: stale facts, privacy leaks, over-retrieval, and untrusted memories

## Why Memory Management Matters

Agents often fail because they treat every prompt as a brand-new world. Real agentic
systems need continuity:

- What is the current task?
- What has already been tried?
- What does this user prefer?
- What previous incident or session is similar?
- What procedure should be followed?
- Which stored memory is trustworthy enough to use?

Memory turns a stateless model call into a stateful system. That makes it powerful,
but also risky. This session focuses on memory as an engineered subsystem, not a
magical feature.

## Prerequisites

```bash
pip install -r ../../requirements.txt

# No API key required for this session.
# Labs use local Python data structures and lightweight vector-style retrieval.
```

Recommended previous sessions:

- Session 01 for embeddings and context windows
- Session 04 for agent loops and tool execution
- Session 05 for stateful servers and reusable agent capabilities

## Session Structure

```
06_memory_management_agentic_ai/
|-- concepts/
|   |-- 01_why_agents_need_memory.md
|   |-- 02_short_term_working_memory.md
|   |-- 03_long_term_semantic_memory.md
|   |-- 04_episodic_and_reflective_memory.md
|   `-- 05_procedural_memory_and_governance.md
|-- labs/
|   |-- lab01_short_term_memory/
|   |-- lab02_long_term_vector_memory/
|   |-- lab03_episodic_reflective_memory/
|   `-- lab04_memory_aware_teaching_agent/
`-- demos/
    |-- demo_short_term_memory.py
    |-- demo_long_term_memory_retrieval.py
    `-- demo_memory_aware_teaching_agent.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_short_term_memory | Rolling working memory | message buffer, task state, compression |
| lab02_long_term_vector_memory | Persistent semantic memory | memory records, embeddings, similarity search |
| lab03_episodic_reflective_memory | Learning from past runs | episodes, outcomes, reflections |
| lab04_memory_aware_teaching_agent | Capstone agent | all memory types working together |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_short_term_memory.py` | Active task state plus rolling conversation summary |
| `demo_long_term_memory_retrieval.py` | Retrieving durable memories relevant to a new request |
| `demo_memory_aware_teaching_agent.py` | A teaching agent using preferences, procedures, episodes, and reflections |

## Quick Start

```bash
cd sessions/06_memory_management_agentic_ai

# Read concepts first
cat concepts/01_why_agents_need_memory.md
cat concepts/02_short_term_working_memory.md

# Run demos
python demos/demo_short_term_memory.py
python demos/demo_long_term_memory_retrieval.py
python demos/demo_memory_aware_teaching_agent.py

# Work through labs
python labs/lab01_short_term_memory/lab.py
python labs/lab02_long_term_vector_memory/lab.py
python labs/lab03_episodic_reflective_memory/lab.py
python labs/lab04_memory_aware_teaching_agent/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 40 min |
| 4 labs | 110 min |
| Demos | 20 min |
| **Total** | **~2.5 hours** |
