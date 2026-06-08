# Session 12: GenAI Security Frameworks

Turn prompt-injection awareness into a broader security practice for LLM
applications, RAG systems, tools, plugins, MCP servers, and agents.

## DevOps Analogy

| GenAI Security Concept | DevOps Equivalent |
|------------------------|-------------------|
| Prompt injection | SQL injection / command injection |
| Insecure output handling | Unsafe deserialization |
| Excessive agency | Over-privileged service account |
| Model denial of service | Expensive unbounded workload |
| Supply-chain risk | Compromised dependency or image |
| Sensitive disclosure | Secret leakage in logs |
| Plugin/tool risk | Unsafe internal admin endpoint |

## What You'll Learn

- Map GenAI app features to OWASP LLM Top 10 risk categories
- Separate control-plane instructions from untrusted data
- Design least-privilege tools and approval gates
- Validate model outputs before downstream execution
- Threat-model RAG indexes, tool schemas, MCP servers, and agent workflows
- Add mitigations that live outside the prompt
- Produce a concise security review record for a GenAI feature

## Official References

- [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [OpenAI safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [OpenAI safety checks](https://developers.openai.com/api/docs/guides/safety-checks)

## Prerequisites

```bash
pip install -r ../../requirements.txt

# No API key required.
```

Recommended previous sessions:

- Session 02 for prompt injection
- Session 04 for tool-calling validation
- Session 05 for MCP server trust boundaries
- Session 07 for RAG prompt injection and data access

## Session Structure

```text
12_genai_security_frameworks/
|-- concepts/
|   |-- 01_owasp_llm_top10.md
|   `-- 02_security_controls_for_agents.md
|-- labs/
|   `-- lab01_threat_model/
`-- demos/
    `-- demo_security_control_matrix.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_threat_model | Build a GenAI threat model | OWASP mapping, mitigations, residual risk |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_security_control_matrix.py` | How risks map to controls outside the model |

## Quick Start

```bash
cd sessions/12_genai_security_frameworks

cat concepts/01_owasp_llm_top10.md
cat concepts/02_security_controls_for_agents.md

python demos/demo_security_control_matrix.py
python labs/lab01_threat_model/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 40 min |
| Lab | 45 min |
| Demo | 10 min |
| **Total** | **~95 min** |

