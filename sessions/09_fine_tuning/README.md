# Session 09: Fine-Tuning LLMs

Learn when fine-tuning is the right tool, how to design high-quality training
data, how supervised fine-tuning differs from preference and reinforcement
fine-tuning, how to evaluate the result, and how to operate fine-tuned models
in production.

This session is intentionally detailed. The goal is to make fine-tuning feel
like an engineering workflow rather than a magic training button.

## DevOps Analogy

| Fine-Tuning Concept | DevOps Equivalent |
|---------------------|-------------------|
| Base model | Golden VM image / base container image |
| Training examples | Integration test fixtures / runbook examples |
| Validation set | Pre-prod acceptance tests |
| Eval suite | CI quality gate |
| Hyperparameters | Deployment tuning knobs |
| Epoch | One full pass through the training set |
| Overfitting | Config works only for one staging environment |
| Fine-tuned model | Custom image built from a base image |
| Deployment | Promote artifact through environments |
| Rollback | Revert to previous model snapshot |

## What You'll Learn

- Decide between prompt engineering, RAG, fine-tuning, and tool use
- Understand what fine-tuning changes inside a model and what it does not
- Design SFT datasets for style, schema, classification, extraction, and domain behavior
- Validate JSONL training files before uploading them
- Split datasets into train, validation, and holdout eval sets
- Understand loss, gradient descent, epochs, batch size, learning rate, and overfitting
- Compare SFT, DPO, RFT, vision fine-tuning, LoRA, and QLoRA
- Build an eval harness before training
- Plan an OpenAI fine-tuning job without accidentally leaking secrets
- Understand local fine-tuning with Hugging Face TRL and PEFT/LoRA
- Create a deployment checklist for fine-tuned models
- Avoid common failures: bad examples, data leakage, weak evals, overtraining, and unsafe behavior

## Official References

- [OpenAI model optimization and fine-tuning guide](https://platform.openai.com/docs/guides/fine-tuning)
- [OpenAI supervised fine-tuning guide](https://platform.openai.com/docs/guides/supervised-fine-tuning)
- [OpenAI fine-tuning API reference](https://platform.openai.com/docs/api-reference/fine-tuning)
- [OpenAI DPO guide](https://platform.openai.com/docs/guides/direct-preference-optimization)
- [OpenAI reinforcement fine-tuning guide](https://platform.openai.com/docs/guides/reinforcement-fine-tuning)
- [Hugging Face TRL SFTTrainer docs](https://huggingface.co/docs/trl/main/en/sft_trainer)
- [Hugging Face PEFT LoRA docs](https://huggingface.co/docs/peft/main/en/developer_guides/lora)

## Prerequisites

```bash
pip install -r ../../requirements.txt

# No API key required for the core labs.
# Optional hosted fine-tuning examples use OPENAI_API_KEY.
```

Recommended previous sessions:

- Session 01 for tokens, embeddings, and model basics
- Session 02 for prompt engineering
- Session 04 for provider APIs
- Session 07 for deciding when RAG is better than fine-tuning

## Session Structure

```
09_fine_tuning/
|-- concepts/
|   |-- 01_what_is_fine_tuning.md
|   |-- 02_when_to_finetune.md
|   |-- 03_training_data_design.md
|   |-- 04_data_formats_sft_dpo_rft.md
|   |-- 05_training_math_and_hyperparameters.md
|   |-- 06_openai_fine_tuning_workflow.md
|   |-- 07_local_lora_qlora.md
|   |-- 08_evaluation_deployment.md
|   `-- 09_safety_cost_governance.md
|-- labs/
|   |-- lab01_dataset_design/
|   |-- lab02_jsonl_validation/
|   |-- lab03_eval_split_and_baseline/
|   |-- lab04_hyperparameter_planning/
|   `-- lab05_finetune_job_spec/
`-- demos/
    |-- demo_dataset_builder.py
    |-- demo_eval_harness.py
    `-- demo_finetune_planner.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_dataset_design | Training examples | task definition, quality rubric, example schema |
| lab02_jsonl_validation | Dataset validation | JSONL, chat message format, leakage checks |
| lab03_eval_split_and_baseline | Evals before training | train/validation/holdout split, baseline scoring |
| lab04_hyperparameter_planning | Training knobs | epochs, batch size, learning-rate multiplier, risk flags |
| lab05_finetune_job_spec | Job planning | file purpose, method, suffix, metadata, deployment checklist |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_dataset_builder.py` | Build SFT JSONL records and inspect dataset quality |
| `demo_eval_harness.py` | Run a small baseline eval before fine-tuning |
| `demo_finetune_planner.py` | Create a safe fine-tuning job plan without calling an API |

## Quick Start

```bash
cd sessions/09_fine_tuning

# Read concepts first
cat concepts/01_what_is_fine_tuning.md
cat concepts/02_when_to_finetune.md
cat concepts/03_training_data_design.md

# Run demos
python demos/demo_dataset_builder.py
python demos/demo_eval_harness.py
python demos/demo_finetune_planner.py

# Work through labs
python labs/lab01_dataset_design/lab.py
python labs/lab02_jsonl_validation/lab.py
python labs/lab03_eval_split_and_baseline/lab.py
python labs/lab04_hyperparameter_planning/lab.py
python labs/lab05_finetune_job_spec/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 110 min |
| 5 labs | 160 min |
| Demos | 35 min |
| **Total** | **~5 hours** |

