# Session 02 — Prompt Engineering

> "Writing prompts is the new writing Bash scripts. A poorly written prompt works in the happy path
> and silently fails everywhere else."

---

## Learning Objectives

By the end of this session you will be able to:

1. **Write effective system prompts** — persona, constraints, output format, and tone in one place
2. **Use zero-shot and few-shot prompting** — know when examples help and how to write good ones
3. **Apply chain-of-thought reasoning** — get the model to reason step-by-step for complex problems
4. **Get reliable structured output** — extract JSON/YAML from any LLM response, every time
5. **Defend against prompt injection** — protect AI-powered tools from adversarial inputs
6. **Test prompts systematically** — build a harness that measures prompt quality with a pass rate

---

## Prerequisites

- Session 01 complete (understand tokens, context window, temperature)
- `ANTHROPIC_API_KEY` set in `.env`
- Python 3.10+, `pip install -r ../../requirements.txt`

---

## Estimated Time

| Activity | Time |
|----------|------|
| Read all concept files | 40 min |
| Lab 01 — Zero-shot vs Few-shot | 25 min |
| Lab 02 — Structured Output | 30 min |
| Lab 03 — Chain of Thought | 25 min |
| Lab 04 — Prompt Test Harness | 30 min |
| Demos (all 3) | 20 min |
| **Total** | **~2.5 hours** |

---

## How to Work Through This Session

### Step 1 — Read the concepts (in order)

```
concepts/
├── 01_system_prompts.md          ← Start here
├── 02_zero_and_few_shot.md
├── 03_chain_of_thought.md
├── 04_structured_output.md
└── 05_prompt_injection.md
```

### Step 2 — Run the labs

```bash
# Lab 01: Classifying incident severity — zero-shot vs few-shot
cd labs/lab01_zero_vs_few_shot
python lab.py

# Lab 02: Reliably extracting structured JSON from incident reports
cd labs/lab02_structured_output
python lab.py

# Lab 03: Chain-of-thought for multi-step infrastructure debugging
cd labs/lab03_chain_of_thought
python lab.py

# Lab 04: Build a prompt test harness that scores your prompt
cd labs/lab04_prompt_testing
python lab.py
```

### Step 3 — Run the demos

```bash
cd demos

# Side-by-side prompt strategy comparison
python demo_prompt_playground.py

# Extract structured fields from messy logs with 100% parse rate
python demo_json_extraction.py

# Chain-of-thought for multi-hop incident diagnosis
python demo_cot_debugging.py
```

---

## The Mental Model

Think of a prompt as three layers:

```
┌─────────────────────────────────────────────────────┐
│  SYSTEM PROMPT                                      │
│  "You are a senior SRE. Output only JSON.           │
│   Never guess if you're unsure."                    │
├─────────────────────────────────────────────────────┤
│  FEW-SHOT EXAMPLES (optional)                       │
│  User: [example input]                              │
│  Assistant: [example output]                        │
├─────────────────────────────────────────────────────┤
│  USER MESSAGE                                       │
│  "Classify this alert: [actual input]"              │
└─────────────────────────────────────────────────────┘
```

Each layer shapes the output. Together they form a prompt that behaves like a deterministic function.

---

## What's Next

**Session 03 — Local LLMs with Ollama** teaches you to run models locally.
**Session 07 — RAG & Vector Databases** teaches you to give the model access to private knowledge: runbooks, wikis, and incident history without fine-tuning.

→ See [../03_local_llms_ollama/README.md](../03_local_llms_ollama/README.md) and [../07_retrieval_augmented_generation/README.md](../07_retrieval_augmented_generation/README.md)
