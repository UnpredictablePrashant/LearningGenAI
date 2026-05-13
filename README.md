# Learning GenAI & Agentic AI

> A hands-on learning repository for **Cloud and DevOps engineers** stepping into Generative AI and Agentic AI.
> Every concept is grounded in infrastructure analogies you already know.

---

## Who Is This For?

You deploy containers. You write Terraform. You've been paged at 3am.
Now AI is showing up everywhere in your stack — in CI/CD pipelines, incident response tooling, and the platforms your company is building.

This repo takes you from "I've used ChatGPT" to "I understand how this works and I can build with it."

**Assumed background:**
- Comfortable with Python (scripts, not data science)
- Hands-on experience with Kubernetes, Terraform, Docker, or similar cloud/DevOps tools
- Some AWS/GCP/Azure exposure helpful but not required

**Not required:**
- Math background
- Machine learning experience
- Data science background

---

## Curriculum Map

| # | Session | Key Tools | API Key? | Status |
|---|---------|-----------|----------|--------|
| 01 | [How LLMs Actually Work](./sessions/01_how_llms_work/) | `tiktoken`, `sentence-transformers` | No | ✅ Available |
| 02 | [Prompt Engineering](./sessions/02_prompt_engineering/) | `anthropic` | Yes | ✅ Available |
| 03 | [Local LLMs with Ollama](./sessions/03_local_llms_ollama/) | `ollama`, `requests` | No (local) | ✅ Available |
| 04 | [Tool Calling (Function Calling)](./sessions/04_tool_calling_function_calling/) | `openai`, `ollama` | Depends on provider | ✅ Available |
| 05 | [MCP Servers with FastMCP](./sessions/05_mcp_servers/) | `fastmcp`, `mcp` | No | ✅ Available |
| 06 | [Memory Management in Agentic AI](./sessions/06_memory_management_agentic_ai/) | Python standard library | No | ✅ Available |
| 07 | [Retrieval-Augmented Generation (RAG)](./sessions/07_retrieval_augmented_generation/) | `pypdf`, `tiktoken`, `sentence-transformers`, `chromadb`, `openai` | Optional | ✅ Available |

---

## How Each Session Is Structured

```
sessions/XX_topic_name/
├── README.md          ← Start here: objectives, prereqs, estimated time
├── concepts/          ← The "why" and "how" — read before coding
│   ├── 01_topic.md
│   └── ...
├── labs/              ← Hands-on coding exercises
│   ├── lab01_name/
│   │   ├── lab.py     ← You write the code (has TODO markers)
│   │   └── solution.py ← Reference implementation (peek only when stuck)
│   └── ...
└── demos/             ← Ready-to-run scripts — observe and learn
    └── ...
```

**How to use labs:**
1. Open `lab.py` and read it top to bottom — understand the goal
2. Fill in the `# TODO` sections — use the concept docs if stuck
3. Run with `python lab.py` and verify your output matches the expected output in comments
4. If truly stuck after trying: check `solution.py`

---

## Quick Start

```bash
# 1. Clone
git clone <repo-url>
cd LearningGenAI

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify your setup
python setup_check.py

# 5. Start Session 01
cd sessions/01_how_llms_work
cat README.md
```

> **Session 01 requires no API key.** You learn tokenization and embeddings completely offline.

---

## API Key Setup

For cloud-provider labs, copy and configure `.env`:

```bash
cp .env.example .env
# Open .env and fill only the keys you need:
# - ANTHROPIC_API_KEY (Session 02)
# - OPENAI_API_KEY / provider-compatible keys (Session 04)
```

Optional local path:
- Session 03 runs fully local with Ollama.
- Session 04 can also run locally through Ollama's OpenAI-compatible `/v1` endpoint.
- Sessions 05 and 06 do not require API keys for the included labs and demos.
- Session 07 core labs run without API keys; the optional generated-answer demo can use `OPENAI_API_KEY`.

---

## Repository Philosophy

- **No notebooks.** DevOps engineers live in terminals and editors. Every exercise is a plain `.py` script.
- **Offline-first.** Session 01 runs entirely without an internet connection after the initial `pip install`.
- **DevOps analogies first.** Every concept is introduced with an infrastructure analogy before the AI theory.
- **Build things that matter.** Labs produce code patterns (semantic search, context management, agent loops) you will actually use in production.

---

## Contributing

Found a bug, a better analogy, or want to contribute a session? Open an issue or PR — contributions welcome.

---

## License

MIT — use freely for learning and teaching.
