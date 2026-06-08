# Session 17: AI Governance, Risk, and Compliance

Turn GenAI engineering work into governable product work: risk registers,
model/version records, data policy, approvals, incident disclosure, and audit
evidence.

## DevOps Analogy

| AI Governance Concept | DevOps Equivalent |
|-----------------------|-------------------|
| Risk register | Service risk register |
| Model card | Service catalog metadata |
| Data provenance | Artifact supply chain |
| Approval workflow | Change advisory gate |
| Incident disclosure | Incident management process |
| Audit evidence | Change logs and access logs |
| Decommissioning | Service retirement plan |

## What You'll Learn

- Use NIST AI RMF functions as a practical governance scaffold
- Create a risk register for GenAI features
- Record model, prompt, dataset, index, and eval versions
- Define data retention, access, and deletion rules
- Connect governance to evals, observability, and release gates
- Prepare incident and rollback records for AI behavior changes

## Official References

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI 600-1 Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- [OpenAI API data privacy controls](https://developers.openai.com/api/docs/guides/your-data)

## Prerequisites

```bash
pip install -r ../../requirements.txt

# No API key required.
```

Recommended previous sessions:

- Session 09 for model cards and fine-tuning governance
- Session 10 for eval evidence
- Session 11 for deployment gates
- Session 12 for security risk mapping
- Session 16 for audit traces

## Session Structure

```text
17_ai_governance_risk_compliance/
|-- concepts/
|   |-- 01_ai_risk_management.md
|   `-- 02_model_and_change_records.md
|-- labs/
|   `-- lab01_risk_register/
`-- demos/
    `-- demo_ai_change_record.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_risk_register | Build an AI risk register | NIST functions, owners, controls, evidence |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_ai_change_record.py` | A deployable AI change record with versions and evidence |

## Quick Start

```bash
cd sessions/17_ai_governance_risk_compliance

cat concepts/01_ai_risk_management.md
cat concepts/02_model_and_change_records.md

python demos/demo_ai_change_record.py
python labs/lab01_risk_register/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 40 min |
| Lab | 45 min |
| Demo | 10 min |
| **Total** | **~95 min** |

