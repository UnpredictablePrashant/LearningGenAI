# Training Runbook

This runbook explains how to inspect the provided dataset, run the full
fine-tuning job, and inspect the outputs.

## Objective

Fine-tune a local 0.5B chat model with QLoRA so it learns a
machine-maintenance response style.

The exact objective is to train `Qwen/Qwen2.5-0.5B-Instruct` to act like
`PlantOps-MaintenanceAI`. Given a machine telemetry report and technician note,
the fine-tuned adapter should return strict JSON with a recommended maintenance
action, urgency level, confidence, root-cause hypothesis, immediate steps,
maintenance plan, and safety note.

The training target is the full assistant response, not just a class label. The
model is being taught this mapping:

```text
system_prompt + user_prompt -> assistant_response
```

Read `DATASET_GUIDE.md` for the full dataset objective, action labels, severity
labels, and column-by-column explanation.

Base model:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

Target behavior:

```text
Given a machine telemetry prompt, return strict JSON containing:
- recommended_action
- severity
- confidence
- root_cause_hypothesis
- immediate_steps
- maintenance_plan
- safety_note
```

Target machine:

```text
AWS EC2 g6.xlarge, Ubuntu, 100 GB EBS
```

Target runtime:

```text
About 1-2 hours
```

## Fine-Tuning Pipeline

This demo follows the pipeline recommended by your fine-tuning expert:

```text
Hugging Face model
        v
Fine-tune using LoRA / QLoRA
        v
Save adapter
        v
Test with Transformers
        v
Optional: merge or convert/import
        v
Run using Ollama
```

In this specific demo:

```text
Qwen/Qwen2.5-0.5B-Instruct
        v
QLoRA training: 4-bit base model + trained LoRA adapter
        v
Save adapter to output/local_05b_machine_assistant/adapter/
        v
Test before/after prompts with Transformers
        v
Optional: write Ollama Modelfile or merge adapter
        v
Run with Ollama/local runtime if desired
```

## Provided Dataset

The dataset is already included in the repo:

```text
sessions/09_fine_tuning/demos/endtoend/datasets/machine_maintenance_ollama_instruction_dataset.csv
```

Dataset size:

```text
Total rows: 4,800
Actions: 6
Rows per action: 800
Training rows after split: 4,320
Validation rows after split: 240
Test rows after split: 240
```

Dataset meaning:

```text
Each row represents one fictional industrial machine condition.
The input is the system/user prompt built from telemetry and technician context.
The target is a strict JSON assistant response with the desired maintenance decision.
```

The script only reads the provided CSV. It loads, validates, splits, tokenizes,
and trains on that dataset.

For the full explanation of every column, read:

```text
docs/DATASET_GUIDE.md
```

## Default Training Profile

The default profile is `ec2_1_to_2_hour`.

Important defaults:

```text
Epochs: 8
Max sequence length: 1,536
Batch size: 1
Gradient accumulation: 8
Effective batch size: 8
LoRA rank: 32
LoRA alpha: 64
Learning rate: 2e-4
Base model: Qwen/Qwen2.5-0.5B-Instruct
Training mode: QLoRA
```

The dataset is large enough to make the run feel like a real local fine-tuning
job, while still being realistic for one NVIDIA L4 GPU.

## Inspect The Dataset

From the repository root:

```bash
python - <<'PY'
import pandas as pd
path = "sessions/09_fine_tuning/demos/endtoend/datasets/machine_maintenance_ollama_instruction_dataset.csv"
df = pd.read_csv(path)
print("rows:", len(df))
print(df["recommended_action"].value_counts().sort_index())
print(df[["example_id", "machine_type", "recommended_action"]].head())
PY
```

Expected summary:

```text
rows: 4800
800 examples for each of the 6 recommended_action labels
```

## Run Full Fine-Tuning

From the repository root:

```bash
python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py
```

Recommended long-running command inside `tmux`:

```bash
tmux new -s finetune
source .venv/bin/activate
python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py
```

## What Happens During The Run

The script performs these steps:

1. Verifies CUDA GPU availability unless `--allow-cpu` is used.
2. Locates the provided 4,800-row CSV dataset.
3. Loads and validates the dataset schema.
4. Splits the dataset into train, validation, and test sets.
5. Loads `Qwen/Qwen2.5-0.5B-Instruct`.
6. Loads the base model in 4-bit mode and attaches LoRA adapters.
7. Writes prompt-check Markdown into `docs/`.
8. Runs the fixed prompt set before fine-tuning.
9. Tokenizes train/validation/test splits.
10. Fine-tunes LoRA adapter weights using QLoRA.
11. Evaluates the validation split.
12. Saves the LoRA adapter.
13. Runs the same prompt set after fine-tuning.
14. Writes a before/after comparison.
15. Generates held-out test examples.
16. Writes local-runtime helper files and `docs/latest_run_summary.md`.

## Output Files

Dataset:

```text
datasets/machine_maintenance_ollama_instruction_dataset.csv
```

Hugging Face model cache:

```text
output/hf_cache/
```

Fine-tuned adapter:

```text
output/local_05b_machine_assistant/adapter/
```

Checkpoints:

```text
output/local_05b_machine_assistant/checkpoints/
```

Metrics:

```text
output/local_05b_machine_assistant/metrics/train_metrics.json
output/local_05b_machine_assistant/metrics/eval_metrics.json
output/local_05b_machine_assistant/metrics/test_action_accuracy.json
```

Prompt checks:

```text
output/local_05b_machine_assistant/prompt_checks/base_model_generations.jsonl
output/local_05b_machine_assistant/prompt_checks/fine_tuned_generations.jsonl
output/local_05b_machine_assistant/prompt_checks/before_after_comparison.json
```

Markdown documents:

```text
docs/sample_prompts.md
docs/latest_run_summary.md
```

Optional local runtime helper files:

```text
output/local_05b_machine_assistant/ollama/Modelfile.adapter
output/local_05b_machine_assistant/ollama/ollama_commands.txt
```

## Faster Smoke Test

Use this only to verify installation:

```bash
python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py --profile smoke --max-steps 20
```

This is not the 1-2 hour teaching run. It is only a quick sanity check.

## Resume From A Checkpoint

If the EC2 session disconnects or you stop the process after checkpoints are
written, resume with a checkpoint path:

```bash
python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py \
  --resume-from-checkpoint sessions/09_fine_tuning/demos/endtoend/output/local_05b_machine_assistant/checkpoints/checkpoint-200
```

Adjust `checkpoint-200` to the latest checkpoint directory.

## Clean And Rerun

To clean only this demo's output folder before rerunning:

```bash
python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py --clean-output
```

The script refuses to clean paths outside `demos/endtoend`.
