# End-to-End Local 0.5B LLM Fine-Tuning Demo

This folder contains the end-to-end EC2 GPU fine-tuning demo.

Target machine:

- AWS EC2 `g6.xlarge`
- Ubuntu
- 1 NVIDIA L4 GPU with 24 GB VRAM
- 16 GiB system RAM
- 100 GB EBS storage
- Target runtime: roughly 1-2 hours

The demo fine-tunes `Qwen/Qwen2.5-0.5B-Instruct` with QLoRA on a provided
machine-maintenance instruction dataset. QLoRA loads the base model in 4-bit
precision while training small LoRA adapter weights. The model learns to return
strict JSON maintenance decisions for industrial telemetry reports.

## Objective

The objective is to train a local 0.5B instruction model to act like
`PlantOps-MaintenanceAI`: given machine telemetry and a technician note, it
should return a strict JSON maintenance decision with an action, severity,
confidence, root-cause hypothesis, immediate steps, maintenance plan, and safety
note.

The dataset is a static 4,800-row CSV of hypothetical industrial machine
maintenance examples. The script reads this provided CSV, splits it into
training/validation/test sets, fine-tunes a QLoRA adapter, and compares the
base model with the fine-tuned adapter on the same prompts.

Read `DATASET_GUIDE.md` before running training if you want the exact dataset
objective, action labels, severity labels, and column-by-column explanation.

## Pipeline

```text
Hugging Face model: Qwen/Qwen2.5-0.5B-Instruct
        v
Fine-tune using QLoRA
        v
Save LoRA adapter
        v
Test with Transformers
        v
Optional: merge or prepare local-runtime import files
        v
Run using Ollama or another local runtime
```

## Folder Layout

```text
demos/endtoend/
|-- requirements.txt
|-- codes/
|   `-- finetune_local_05b_llm.py
|-- datasets/
|   `-- machine_maintenance_ollama_instruction_dataset.csv
|-- docs/
|   |-- README.md
|   |-- DATASET_GUIDE.md
|   |-- EC2_UBUNTU_SETUP.md
|   |-- CONFIGURATION_OPTIONS.md
|   |-- TRAINING_RUNBOOK.md
|   |-- PROMPT_CHECKS.md
|   `-- sample_prompts.md
`-- output/
    |-- hf_cache/
    `-- local_05b_machine_assistant/
```

## Read In This Order

1. `README.md`
2. `DATASET_GUIDE.md`
3. `EC2_UBUNTU_SETUP.md`
4. `CONFIGURATION_OPTIONS.md`
5. `TRAINING_RUNBOOK.md`
6. `PROMPT_CHECKS.md`
7. `sample_prompts.md`

## Main Command

From the repository root:

```bash
python -m pip install -r sessions/09_fine_tuning/demos/endtoend/requirements.txt
```

Then run:

```bash
python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py
```

## Included Files And Generated Outputs

The provided dataset is included under:

```text
sessions/09_fine_tuning/demos/endtoend/datasets/
```

Generated output stays under:

```text
sessions/09_fine_tuning/demos/endtoend/output/
```

Markdown documents and prompt handouts stay under:

```text
sessions/09_fine_tuning/demos/endtoend/docs/
```

The most important files are:

- `requirements.txt`
- `datasets/machine_maintenance_ollama_instruction_dataset.csv`
- `docs/DATASET_GUIDE.md`
- `output/local_05b_machine_assistant/adapter/`
- `output/local_05b_machine_assistant/metrics/`
- `output/local_05b_machine_assistant/prompt_checks/base_model_generations.jsonl`
- `output/local_05b_machine_assistant/prompt_checks/fine_tuned_generations.jsonl`
- `output/local_05b_machine_assistant/prompt_checks/before_after_comparison.json`
- `docs/sample_prompts.md`
- `docs/latest_run_summary.md`

## Official References

- PyTorch install selector: https://pytorch.org/get-started/locally/
- Ubuntu on AWS NVIDIA driver setup: https://documentation.ubuntu.com/aws/aws-how-to/instances/install-nvidia-drivers/
- AWS G6 instance specs: https://aws.amazon.com/ec2/instance-types/g6/
- Qwen 0.5B model card: https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct
- Ollama import docs: https://docs.ollama.com/import
