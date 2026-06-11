# Session 09: Fine-Tuning LLMs

Learn when fine-tuning is the right tool, how to design high-quality training
data, how supervised fine-tuning differs from preference and reinforcement
fine-tuning, how to evaluate the result, and how to operate fine-tuned models
in production.

This session is intentionally detailed. The goal is to make fine-tuning feel
like an engineering workflow rather than a magic training button.

For a complete beginner-friendly project walkthrough, read
[PROJECT_README.md](PROJECT_README.md). It uses the included number dataset and
walks through data collection, train/validation/test splitting, OpenAI hosted
fine-tuning, LoRA, QLoRA, local hardware planning, and AWS EC2 setup.

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
- Explain weights, biases, parameters, logits, inference, training, checkpoints, adapters, and quantization from first principles
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
- [Ollama model import docs](https://docs.ollama.com/import)
- [Ollama Modelfile reference](https://docs.ollama.com/modelfile)

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
|-- PROJECT_README.md
|-- concepts/
|   |-- 01_model_basics_before_fine_tuning.md
|   |-- 02_what_is_fine_tuning.md
|   |-- 03_when_to_finetune.md
|   |-- 04_training_data_design.md
|   |-- 05_data_formats_sft_dpo_rft.md
|   |-- 06_training_math_and_hyperparameters.md
|   |-- 07_openai_fine_tuning_workflow.md
|   |-- 08_local_lora_qlora.md
|   |-- 09_evaluation_deployment.md
|   `-- 10_safety_cost_governance.md
|-- labs/
|   |-- lab01_dataset_design/
|   |-- lab02_jsonl_validation/
|   |-- lab03_eval_split_and_baseline/
|   |-- lab04_hyperparameter_planning/
|   `-- lab05_finetune_job_spec/
`-- demos/
    |-- demo_model_basics.py
    |-- demo_dataset_builder.py
    |-- demo_eval_harness.py
    |-- demo_finetune_planner.py
    `-- endtoend/
        |-- requirements.txt
        |-- docs/
        |   |-- README.md
        |   |-- DATASET_GUIDE.md
        |   |-- EC2_UBUNTU_SETUP.md
        |   |-- CONFIGURATION_OPTIONS.md
        |   |-- TRAINING_RUNBOOK.md
        |   |-- PROMPT_CHECKS.md
        |   `-- sample_prompts.md
        |-- datasets/
        |   `-- machine_maintenance_ollama_instruction_dataset.csv
        |-- codes/
        |   `-- finetune_local_05b_llm.py
        `-- output/
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
| `demo_model_basics.py` | Weights, bias, logits, softmax, inference, and simple quantization |
| `demo_dataset_builder.py` | Build SFT JSONL records and inspect dataset quality |
| `demo_eval_harness.py` | Run a small baseline eval before fine-tuning |
| `demo_finetune_planner.py` | Create a safe fine-tuning job plan without calling an API |
| `endtoend/codes/finetune_local_05b_llm.py` | Fine-tune `Qwen/Qwen2.5-0.5B-Instruct` on Ubuntu EC2 `g6.xlarge` with QLoRA; dataset, docs, code, and outputs stay under `demos/endtoend` |

## Quick Start

```bash
cd sessions/09_fine_tuning

# Read concepts first
cat concepts/01_model_basics_before_fine_tuning.md
cat concepts/02_what_is_fine_tuning.md
cat concepts/04_training_data_design.md

# Then follow the full project walkthrough
cat PROJECT_README.md

# Run demos
python demos/demo_model_basics.py
python demos/demo_dataset_builder.py
python demos/demo_eval_harness.py
python demos/demo_finetune_planner.py

# Optional EC2 GPU local 0.5B LLM QLoRA fine-tune.
# Target: g6.xlarge, 100 GB EBS, roughly 1-2 hours.
cat demos/endtoend/docs/README.md
cat demos/endtoend/docs/DATASET_GUIDE.md
cat demos/endtoend/docs/EC2_UBUNTU_SETUP.md
cat demos/endtoend/docs/CONFIGURATION_OPTIONS.md
cat demos/endtoend/docs/TRAINING_RUNBOOK.md
python -m pip install -r demos/endtoend/requirements.txt
python demos/endtoend/codes/finetune_local_05b_llm.py

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
| Concepts | 130 min |
| 5 labs | 160 min |
| Demos | 45 min |
| Full project walkthrough | 2-4 hours without paid training, longer with OpenAI/EC2 runs |
| **Total** | **~8-10 hours with the walkthrough** |
