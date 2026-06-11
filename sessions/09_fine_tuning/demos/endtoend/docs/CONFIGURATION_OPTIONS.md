# Configuration Options

This document explains the default choices in the end-to-end fine-tuning demo
and what you should change for common scenarios.

## Study Order

Read the documents in this order:

1. `README.md`
2. `DATASET_GUIDE.md`
3. `EC2_UBUNTU_SETUP.md`
4. `CONFIGURATION_OPTIONS.md`
5. `TRAINING_RUNBOOK.md`
6. `PROMPT_CHECKS.md`
7. `sample_prompts.md`

Why this order:

- `README.md` explains the folder layout and high-level pipeline.
- `DATASET_GUIDE.md` explains the objective, dataset columns, labels, and
  target JSON response.
- `EC2_UBUNTU_SETUP.md` gets Ubuntu, NVIDIA, PyTorch, and dependencies ready.
- `CONFIGURATION_OPTIONS.md` explains the defaults and what can be changed.
- `TRAINING_RUNBOOK.md` gives the exact commands to run.
- `PROMPT_CHECKS.md` explains how to prove before/after behavior changed.
- `sample_prompts.md` contains the actual prompts used for before/after checks.

## Default Pipeline

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
Run using Ollama/local runtime if desired
```

## Default Machine Target

```text
EC2 instance: g6.xlarge
GPU: NVIDIA L4, 24 GB VRAM
Storage: 100 GB EBS
OS: Ubuntu
Runtime target: 1-2 hours
```

## Default Training Options

The default command is:

```bash
python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py
```

Important defaults:

```text
--model-name Qwen/Qwen2.5-0.5B-Instruct
--training-mode qlora
--profile ec2_1_to_2_hour
--epochs 8
--max-length 1536
--batch-size 1
--gradient-accumulation-steps 8
--lora-r 32
--lora-alpha 64
--learning-rate 2e-4
--dataloader-num-workers 1
```

The provided CSV dataset has:

```text
Total rows: 4,800
Training rows after split: 4,320
Validation rows after split: 240
Test rows after split: 240
Rows per action: 800
```

This satisfies the requirement that the model trains on more than 2,000 data
points. The actual training split contains 4,320 examples.

## Default Paths

Dataset folder:

```text
sessions/09_fine_tuning/demos/endtoend/datasets/
```

Requirements file:

```text
sessions/09_fine_tuning/demos/endtoend/requirements.txt
```

Code folder:

```text
sessions/09_fine_tuning/demos/endtoend/codes/
```

Docs folder:

```text
sessions/09_fine_tuning/demos/endtoend/docs/
```

Output folder:

```text
sessions/09_fine_tuning/demos/endtoend/output/
```

Hugging Face cache:

```text
sessions/09_fine_tuning/demos/endtoend/output/hf_cache/
```

## What To Change

Use this table when you want to adjust the run.

| Goal | Change | Example |
|------|--------|---------|
| Fast installation test | Use smoke profile | `--profile smoke --max-steps 20` |
| Full 1-2 hour class demo | Keep defaults | no changes |
| Longer quality run on same dataset | Use longer profile | `--profile longer_quality` |
| Less VRAM pressure | Keep QLoRA | default |
| Plain LoRA instead of QLoRA | Change training mode | `--training-mode lora` |
| Different output location | Change output dir | `--output-dir path/to/output` |
| Different provided dataset | Change dataset path | `--dataset path/to/file.csv` |
| Resume interrupted run | Use checkpoint path | `--resume-from-checkpoint path/to/checkpoint` |
| Optional merged model | Merge adapter | `--merge-adapter` |

## Recommended Sequence For g6.xlarge

For your target run, do not change the defaults unless you are doing a smoke
test first.

Recommended sequence:

```bash
python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py --profile smoke --max-steps 20
python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py
```

The first command verifies the environment.

The second command is the real 1-2 hour fine-tuning run.

## Console Output

The script prints numbered step headers like:

```text
[Step 01/16] Locate provided training dataset
[Step 02/16] Load and validate instruction dataset
[Step 03/16] Split dataset into train, validation, and test
...
[Step 16/16] Write final run summary
```

This is intentional so students can see exactly what is happening during a long
EC2 run.
