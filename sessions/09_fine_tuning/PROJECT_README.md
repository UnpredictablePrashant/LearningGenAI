# Complete Fine-Tuning Project Walkthrough

This README walks through one complete beginner-friendly fine-tuning project.
It uses the existing dataset in this session:

```text
number_finetune_data.jsonl
```

The same dataset is used in three ways:

1. OpenAI hosted supervised fine-tuning.
2. Local LoRA fine-tuning with Hugging Face.
3. Local QLoRA fine-tuning with Hugging Face and 4-bit quantization.

The project is intentionally simple. The goal is to learn the complete process,
not to build the most impressive model.

## What You Will Produce

By the end of the walkthrough, you should understand and have files for:

- A raw prompt/completion dataset.
- A validation script for the raw dataset.
- OpenAI-compatible chat JSONL files.
- Local Hugging Face-compatible text JSONL files.
- Train, validation, and test splits.
- A baseline evaluation process.
- An OpenAI hosted fine-tuning job plan and runnable scripts, if your account has access.
- A LoRA training script for a small open model.
- A QLoRA training script for lower-memory GPU training.
- A local inference script that loads a base model plus adapter.
- A mental model for hardware, AWS EC2 setup, cost, and cleanup.
- A checklist for deciding whether a fine-tuned model is ready to deploy.

The final deliverable is not just a model. The final deliverable is a repeatable
fine-tuning workflow.

## Beginner Roadmap

Read this README in this order:

1. First pass: read the concepts and commands without running paid training.
2. Second pass: run the local no-API scripts for validation and splitting.
3. Third pass: choose either OpenAI hosted fine-tuning or local LoRA/QLoRA.
4. Final pass: compare results, write an experiment note, and decide whether the
   trained model is better than the baseline.

If you are completely new, do not start with GPU setup. Start with the dataset,
splits, and eval sections. They are the heart of fine-tuning.

## Project Goal

Build a "number tutor" model.

Input:

```text
Tell me about number 8.
```

Expected output:

```text
Number: 8
Parity: Even
Double: 16
Square: 64
Simple explanation: 8 is an even number. Its double is 16 and its square is 64.
```

Why this project is good for beginners:

- The answers are easy to verify.
- The output format is strict.
- The same data can be converted for hosted and local training.
- You can learn splitting, validation, training, eval, and deployment without
  needing private data.

## What the Model Is Learning

The model is not learning mathematics from scratch. A capable base model already
knows that `8 * 2 = 16` and `8 * 8 = 64`. The project teaches a repeated output
contract:

```text
Number: <n>
Parity: <Even/Odd>
Double: <2n>
Square: <n*n>
Simple explanation: ...
```

This matters because many production fine-tuning tasks are similar. You often
fine-tune to improve consistency, schema following, tone, classification labels,
or domain-specific phrasing. You usually do not fine-tune to store changing
facts.

## Concept Map

| Project Step | Fine-Tuning Concept | Why It Matters |
|--------------|---------------------|----------------|
| Create examples | Data design | Examples define the behavior you want |
| Validate data | Data governance | Bad rows become bad training signals |
| Split data | Evaluation hygiene | Test data must remain unseen |
| Baseline eval | Measurement | You need something to beat |
| OpenAI SFT | Hosted fine-tuning | Provider handles training infrastructure |
| LoRA | Adapter tuning | Train small adapter weights instead of all weights |
| QLoRA | Quantized adapter tuning | Reduce GPU memory by loading base model in 4-bit |
| Holdout eval | Deployment gate | Job success is not the same as model quality |
| AWS EC2 | Cloud training | Use rented GPU when local hardware is not enough |

## Big Picture

Fine-tuning is not one command. It is a pipeline:

```text
collect data
-> clean and validate
-> split into train/validation/test
-> run baseline eval
-> train
-> evaluate fine-tuned model
-> compare with baseline
-> deploy only if better
```

Analogy: do not treat fine-tuning like pressing "enhance." Treat it like
building and testing a release artifact.

## Three Training Paths

This README shows three paths because real teams choose different deployment
targets.

| Path | Training Runs Where | Inference Runs Where | What You Get |
|------|---------------------|----------------------|--------------|
| OpenAI hosted SFT | OpenAI platform | OpenAI API | Fine-tuned model ID |
| LoRA | Your GPU or cloud GPU | Your runtime with base model plus adapter | Adapter files |
| QLoRA | Your GPU or cloud GPU | Your runtime with base model plus adapter | Adapter files trained with lower memory |

All three paths use the same core workflow:

```text
data -> validation -> split -> train -> evaluate -> decide
```

## Folder Setup

From this directory:

```bash
cd sessions/09_fine_tuning
mkdir -p data/openai data/local outputs scripts
```

On Windows PowerShell:

```powershell
Set-Location sessions\09_fine_tuning
New-Item -ItemType Directory -Force data\openai, data\local, outputs, scripts
```

Expected project tree after the preparation scripts run:

```text
09_fine_tuning/
|-- number_finetune_data.jsonl
|-- PROJECT_README.md
|-- data/
|   |-- openai/
|   |   |-- train.jsonl
|   |   |-- validation.jsonl
|   |   `-- test.jsonl
|   `-- local/
|       |-- train.jsonl
|       |-- validation.jsonl
|       |-- test.jsonl
|       |-- train_raw.jsonl
|       |-- validation_raw.jsonl
|       `-- test_raw.jsonl
|-- scripts/
|   |-- validate_number_dataset.py
|   |-- prepare_splits.py
|   |-- validate_openai_jsonl.py
|   |-- eval_number_outputs.py
|   |-- openai_upload_files.py
|   |-- openai_create_finetune.py
|   |-- openai_monitor_finetune.py
|   |-- openai_try_finetuned_model.py
|   |-- openai_eval_finetuned_model.py
|   |-- local_lora_train.py
|   |-- local_qlora_train.py
|   `-- local_try_adapter.py
`-- outputs/
    |-- number-tutor-lora/
    `-- number-tutor-qlora/
```

You do not need all files on day one. The point of the tree is to keep raw data,
converted data, scripts, and model outputs separate.

## Environment Checklist

For the data preparation sections:

- Python 3.10 or newer is recommended.
- No API key is required.
- No GPU is required.

For OpenAI hosted fine-tuning:

- `openai` Python package.
- `OPENAI_API_KEY`.
- Account access to hosted fine-tuning.

For local LoRA/QLoRA:

- NVIDIA GPU strongly recommended.
- CUDA-compatible PyTorch.
- `transformers`, `datasets`, `accelerate`, `peft`, `trl`, and `bitsandbytes`.
- Enough disk space for downloaded models and adapter outputs.

Quick environment check:

```bash
python --version
python -c "import platform; print(platform.platform())"
```

GPU check:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

If `torch.cuda.is_available()` prints `False`, local GPU training will not work
until PyTorch, CUDA, drivers, and hardware are correctly configured.

## Step 1: Data Collection

In a real project, data may come from tickets, chats, support macros, expert
labels, or reviewed model outputs. In this teaching project, we can generate
clean examples because the task is based on numbers.

Data collection is where many fine-tuning projects succeed or fail. The model
learns from the examples you provide, so unclear examples create unclear model
behavior.

For every project, write a short task definition before collecting examples:

```text
Task: Given a user asking about a number, answer with number facts.
Input: A natural-language prompt containing one integer.
Output: A five-line template with number, parity, double, square, and explanation.
Allowed variation: None for labels and headings. Explanation can only vary if the project says so.
Safety: No private data or user-specific information is needed.
```

For production, this definition might be longer and include label rules,
redaction rules, refusal rules, and examples of known edge cases.

The existing file already contains examples from 1 to 200:

```jsonl
{"prompt": "Tell me about number 1.", "completion": "Number: 1\nParity: Odd\nDouble: 2\nSquare: 1\nSimple explanation: 1 is an odd number. Its double is 2 and its square is 1."}
```

If you wanted to regenerate the raw dataset, the idea is:

```python
import json

def make_example(n: int) -> dict:
    parity = "Even" if n % 2 == 0 else "Odd"
    return {
        "prompt": f"Tell me about number {n}.",
        "completion": (
            f"Number: {n}\n"
            f"Parity: {parity}\n"
            f"Double: {n * 2}\n"
            f"Square: {n * n}\n"
            f"Simple explanation: {n} is an {parity.lower()} number. "
            f"Its double is {n * 2} and its square is {n * n}."
        ),
    }

with open("number_finetune_data.jsonl", "w", encoding="utf-8") as f:
    for n in range(1, 201):
        f.write(json.dumps(make_example(n)) + "\n")
```

Concept link: data collection defines what "good" means. The model learns the
pattern repeated in these examples.

### What Good Data Looks Like

For this project, a good example has:

- One clear user prompt.
- One complete assistant completion.
- Correct arithmetic.
- Consistent capitalization.
- Consistent line order.
- No extra commentary.
- No markdown fences around the answer.

Good:

```jsonl
{"prompt":"Tell me about number 12.","completion":"Number: 12\nParity: Even\nDouble: 24\nSquare: 144\nSimple explanation: 12 is an even number. Its double is 24 and its square is 144."}
```

Weak:

```jsonl
{"prompt":"number 12 info","completion":"12 is even. Double 24. Square 144."}
```

The weak example contains correct facts, but it does not teach the exact output
contract. If you mix both styles in training, the model may mix styles in
production.

### Real-World Data Collection Pattern

For a support-ticket fine-tune, a real data collection plan could be:

1. Export 500 historical tickets.
2. Remove customer names, secrets, account IDs, and unnecessary logs.
3. Ask a domain expert to label each ticket.
4. Add a second reviewer for ambiguous examples.
5. Create a labeling guide that explains each label.
6. Keep 10-20% of examples as a holdout test set before anyone tunes prompts or
   training settings.

That workflow is slower than dumping logs into a JSONL file, but it produces a
model you can trust.

### Data Card Template

For serious projects, create a small data card:

```text
Dataset name: numbers-v1
Owner: learning-genai
Source: generated examples for numbers 1-200
Rows: 200
Task: number facts template generation
Contains personal data: no
Contains secrets: no
Train/validation/test split: 160/20/20
Known limitations: toy arithmetic task; not representative of messy production text
Approved for provider upload: yes/no
```

This is especially useful when multiple experiments happen over time.

## Step 2: Validate the Raw Dataset

Before training, validate:

- Every line is valid JSON.
- Every row has `prompt` and `completion`.
- No prompt or completion is empty.
- No duplicate prompts exist.
- The expected format is consistent.

Validation is a safety net. It catches problems before they become expensive
training failures or subtle model behavior issues.

Think of validation like unit tests for your dataset.

Create `scripts/validate_number_dataset.py`:

```python
import json
from pathlib import Path

path = Path("number_finetune_data.jsonl")
seen_prompts = set()
errors = []

for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
    try:
        row = json.loads(line)
    except json.JSONDecodeError as exc:
        errors.append(f"line {line_number}: invalid JSON: {exc}")
        continue

    prompt = row.get("prompt")
    completion = row.get("completion")

    if not prompt:
        errors.append(f"line {line_number}: missing prompt")
    if not completion:
        errors.append(f"line {line_number}: missing completion")
    if prompt in seen_prompts:
        errors.append(f"line {line_number}: duplicate prompt: {prompt}")
    seen_prompts.add(prompt)

    required_phrases = ["Number:", "Parity:", "Double:", "Square:", "Simple explanation:"]
    if completion and not all(phrase in completion for phrase in required_phrases):
        errors.append(f"line {line_number}: completion does not match required template")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)

print(f"Dataset valid: {len(seen_prompts)} examples")
```

Run:

```bash
python scripts/validate_number_dataset.py
```

Concept link: validation prevents bad examples from becoming model behavior.

### Add Stronger Validation for This Dataset

The previous validator checks structure. We can also check that the arithmetic
inside the completion is correct.

Add this helper if you want stricter validation:

```python
import re

def expected_values(prompt: str) -> dict:
    match = re.search(r"number (\d+)", prompt)
    if not match:
        raise ValueError(f"prompt does not contain a number: {prompt}")

    n = int(match.group(1))
    return {
        "number": n,
        "parity": "Even" if n % 2 == 0 else "Odd",
        "double": n * 2,
        "square": n * n,
    }

def completion_matches(row: dict) -> bool:
    values = expected_values(row["prompt"])
    completion = row["completion"]
    return (
        f"Number: {values['number']}" in completion
        and f"Parity: {values['parity']}" in completion
        and f"Double: {values['double']}" in completion
        and f"Square: {values['square']}" in completion
    )
```

For a real support-ticket project, equivalent checks might validate JSON schema,
allowed labels, confidence range, redaction, and forbidden terms.

### Validation Checklist

Before training, confirm:

- Raw file exists.
- File is JSONL, not a JSON array.
- Every row has required fields.
- Every target answer follows the desired format.
- There are no exact duplicate prompts.
- There are no obvious secrets.
- The dataset has enough examples for a first experiment.
- The data owner approves the data for the chosen training provider or runtime.

## Step 3: Split Into Train, Validation, and Test

Use three sets:

- Train: used to update the model.
- Validation: used during training to watch generalization.
- Test: untouched holdout used for final evaluation.

Beginner split:

```text
80% train, 10% validation, 10% test
```

For 200 examples:

```text
160 train
20 validation
20 test
```

Why not train on all 200 examples?

Because you need unseen examples to measure whether the model learned a general
pattern. If you test on the same examples used for training, the model may look
better than it really is.

Analogy:

```text
training set = homework
validation set = practice quiz
test set = final exam
```

You can learn from homework and practice quizzes. You should not tune your
entire course around the final exam answers.

Create `scripts/prepare_splits.py`:

```python
import json
import random
from pathlib import Path

SYSTEM_PROMPT = "Answer using the required number facts template."
random.seed(42)

raw_path = Path("number_finetune_data.jsonl")
openai_dir = Path("data/openai")
local_dir = Path("data/local")
openai_dir.mkdir(parents=True, exist_ok=True)
local_dir.mkdir(parents=True, exist_ok=True)

rows = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines()]
random.shuffle(rows)

train_end = int(len(rows) * 0.80)
validation_end = int(len(rows) * 0.90)

splits = {
    "train": rows[:train_end],
    "validation": rows[train_end:validation_end],
    "test": rows[validation_end:],
}

def to_openai_chat(row: dict) -> dict:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": row["prompt"]},
            {"role": "assistant", "content": row["completion"]},
        ]
    }

def to_local_text(row: dict) -> dict:
    return {
        "text": (
            "### System:\n"
            f"{SYSTEM_PROMPT}\n\n"
            "### User:\n"
            f"{row['prompt']}\n\n"
            "### Assistant:\n"
            f"{row['completion']}"
        )
    }

for split_name, split_rows in splits.items():
    with (openai_dir / f"{split_name}.jsonl").open("w", encoding="utf-8") as f:
        for row in split_rows:
            f.write(json.dumps(to_openai_chat(row)) + "\n")

    with (local_dir / f"{split_name}.jsonl").open("w", encoding="utf-8") as f:
        for row in split_rows:
            f.write(json.dumps(to_local_text(row)) + "\n")

    with (local_dir / f"{split_name}_raw.jsonl").open("w", encoding="utf-8") as f:
        for row in split_rows:
            f.write(json.dumps(row) + "\n")

print({name: len(value) for name, value in splits.items()})
```

Run:

```bash
python scripts/prepare_splits.py
```

Concept link: the same raw examples are wrapped differently for different
training systems.

### Why We Use a Random Seed

The script uses:

```python
random.seed(42)
```

This makes the split reproducible. If two students run the script, they get the
same train/validation/test files. Reproducibility matters because fine-tuning is
an experiment. If the split changes every time, eval scores become harder to
compare.

### What Each Split File Means

| File | Used By | Purpose |
|------|---------|---------|
| `data/openai/train.jsonl` | OpenAI SFT | Training examples in chat format |
| `data/openai/validation.jsonl` | OpenAI SFT | Validation examples in chat format |
| `data/openai/test.jsonl` | Optional eval scripts | Holdout chat examples |
| `data/local/train.jsonl` | TRL SFTTrainer | Training examples as formatted text |
| `data/local/validation.jsonl` | TRL SFTTrainer | Validation examples as formatted text |
| `data/local/test.jsonl` | Optional local eval | Holdout examples as formatted text |
| `data/local/test_raw.jsonl` | Eval scripts | Raw prompt/completion test rows |

Do not edit the generated split files by hand unless you also record what
changed. Prefer editing raw data and regenerating splits.

### Stratified Splits for Classification

This number dataset is balanced by construction. In classification projects, use
stratified splitting so each label appears in each split.

Example:

```text
If security examples are rare, make sure security appears in train,
validation, and test. Otherwise the model and eval will not learn or measure
that label properly.
```

For very small classes, collect more examples before training.

## Step 4: Validate OpenAI Chat JSONL

Create `scripts/validate_openai_jsonl.py`:

```python
import json
from pathlib import Path

def validate(path: Path) -> None:
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        record = json.loads(line)
        messages = record.get("messages")

        if not isinstance(messages, list) or len(messages) < 3:
            raise ValueError(f"{path}:{line_number}: messages must contain system, user, assistant")

        if messages[-1].get("role") != "assistant":
            raise ValueError(f"{path}:{line_number}: final message must be assistant")

        for message in messages:
            if message.get("role") not in {"system", "user", "assistant"}:
                raise ValueError(f"{path}:{line_number}: invalid role")
            if not message.get("content"):
                raise ValueError(f"{path}:{line_number}: empty content")

for name in ["train", "validation", "test"]:
    validate(Path(f"data/openai/{name}.jsonl"))

print("OpenAI JSONL files are valid")
```

Run:

```bash
python scripts/validate_openai_jsonl.py
```

### Why Convert to Chat Format?

OpenAI chat fine-tuning examples use messages. The same training idea is still:

```text
user input -> ideal assistant output
```

But the message wrapper lets you include:

- System instruction
- User turn
- Assistant target
- Multi-turn conversations, if needed

For this project, every row has one system message, one user message, and one
assistant target. That is enough to teach the number tutor behavior.

### Inspect a Converted Row

Use this quick command:

```bash
python -c "import json; print(json.dumps(json.loads(open('data/openai/train.jsonl').readline()), indent=2))"
```

PowerShell:

```powershell
python -c "import json; print(json.dumps(json.loads(open('data/openai/train.jsonl').readline()), indent=2))"
```

You should see:

```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

If the assistant message is missing, SFT has no target answer to learn from.

## Step 5: Create a Baseline

A baseline tells you what the model or system does before fine-tuning.

For this toy project, an exact formula can solve the task. In real projects,
your baseline might be:

- Base model with a strong prompt.
- Current production model.
- Simple rules.
- RAG or tools.

The baseline is your "before" picture. Without it, you cannot say whether the
fine-tune helped.

For the number tutor project, exact match is a strict metric:

```text
exact_match = number of exactly correct outputs / number of test examples
```

If 18 out of 20 test outputs match exactly:

```text
exact_match = 18 / 20 = 0.90
```

Strict exact match is useful here because the desired format is deterministic.
For open-ended tasks like summarization, you would use rubrics, human review,
or task-specific checks instead.

Create `scripts/eval_number_outputs.py`:

```python
import json
import re
from pathlib import Path

def expected_completion(prompt: str) -> str:
    match = re.search(r"number (\d+)", prompt)
    if not match:
        raise ValueError(f"could not extract number from prompt: {prompt}")

    n = int(match.group(1))
    parity = "Even" if n % 2 == 0 else "Odd"
    return (
        f"Number: {n}\n"
        f"Parity: {parity}\n"
        f"Double: {n * 2}\n"
        f"Square: {n * n}\n"
        f"Simple explanation: {n} is an {parity.lower()} number. "
        f"Its double is {n * 2} and its square is {n * n}."
    )

def normalize(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())

rows = [json.loads(line) for line in Path("data/local/test_raw.jsonl").read_text(encoding="utf-8").splitlines()]

correct = 0
for row in rows:
    expected = normalize(row["completion"])
    predicted = normalize(expected_completion(row["prompt"]))
    correct += int(expected == predicted)

print({"examples": len(rows), "exact_match": correct / len(rows)})
```

Run:

```bash
python scripts/eval_number_outputs.py
```

Concept link: evals must exist before training. Otherwise you cannot prove the
fine-tuned model improved.

### What This Baseline Really Measures

This baseline uses a formula, so it should score 1.0 if the dataset is clean.
That does not mean fine-tuning is useless. It means this toy task has a perfect
deterministic solution, which is useful for learning evaluation.

In real projects, the baseline might score lower:

```text
Base prompt JSON validity: 82%
Fine-tuned JSON validity: 97%
Base classification accuracy: 74%
Fine-tuned classification accuracy: 86%
```

The decision to deploy should depend on this type of comparison.

### Evaluation Report Template

Create an eval note for every experiment:

```text
Experiment: number-tutor-openai-sft-v1
Dataset version: numbers-v1
Train/validation/test: 160/20/20
Base model: gpt-4.1-nano-2025-04-14
Fine-tuned model or adapter: ft:... or outputs/number-tutor-lora/final
Baseline exact match: 1.00 formula baseline, or <base model score>
Fine-tuned exact match: <score>
Failures:
- prompt:
- expected:
- actual:
Decision: deploy / do not deploy / collect more data
Notes:
```

This habit makes your fine-tuning work much more professional.

### Common Eval Mistakes

Avoid:

- Testing only examples from the training file.
- Looking at two examples and calling the model good.
- Changing the test set after seeing failures.
- Reporting only accuracy when schema validity or safety matters.
- Ignoring latency and cost.

For this project, exact match is enough to learn the loop. For production,
choose metrics that match the product behavior.

## Step 6: OpenAI Hosted Fine-Tuning

Use hosted fine-tuning when:

- You want OpenAI-hosted inference.
- You do not want to manage GPUs.
- Your dataset can be uploaded according to your data policy.
- The task matches a supported fine-tuning method and model.

Important availability note: the current OpenAI supervised fine-tuning docs say
the fine-tuning platform is being wound down and is no longer accessible to new
users, while existing users can continue creating jobs for a limited period. If
your account does not have hosted fine-tuning access, still complete the data
preparation, splitting, validation, and eval sections, then use the LoRA/QLoRA
path below.

Computer specification:

- Any normal laptop is enough for data preparation.
- No local GPU is required.
- You need Python and an OpenAI API key.

Hosted fine-tuning moves the expensive training work to the provider. Your local
machine only prepares files, uploads them, starts a job, and calls the resulting
model.

Conceptually:

```text
local JSONL files -> upload -> file IDs -> fine-tuning job -> fine-tuned model ID
```

The file ID is like an artifact reference in CI/CD. The job does not read your
local path after upload; it reads the provider-hosted file.

Install:

```bash
pip install -U openai python-dotenv
```

Set environment variable:

```bash
export OPENAI_API_KEY="your-key"
```

PowerShell:

```powershell
$env:OPENAI_API_KEY="your-key"
```

### Upload Files

Create `scripts/openai_upload_files.py`:

```python
from openai import OpenAI

client = OpenAI()

train = client.files.create(
    file=open("data/openai/train.jsonl", "rb"),
    purpose="fine-tune",
)

validation = client.files.create(
    file=open("data/openai/validation.jsonl", "rb"),
    purpose="fine-tune",
)

print("TRAINING_FILE_ID=", train.id)
print("VALIDATION_FILE_ID=", validation.id)
```

Run:

```bash
python scripts/openai_upload_files.py
```

Save the printed IDs.

Record the IDs in an experiment note:

```text
training_file: file-...
validation_file: file-...
dataset_version: numbers-v1
created_by: your-name
```

Do not commit API keys or secret-bearing environment files.

### Create Fine-Tuning Job

Create `scripts/openai_create_finetune.py`:

```python
import os
from openai import OpenAI

client = OpenAI()

training_file_id = os.environ["TRAINING_FILE_ID"]
validation_file_id = os.environ["VALIDATION_FILE_ID"]

job = client.fine_tuning.jobs.create(
    model="gpt-4.1-nano-2025-04-14",
    training_file=training_file_id,
    validation_file=validation_file_id,
    method={
        "type": "supervised",
        "supervised": {
            "hyperparameters": {
                "n_epochs": "auto",
                "batch_size": "auto",
                "learning_rate_multiplier": "auto",
            }
        },
    },
    suffix="number-tutor-v1",
    metadata={
        "dataset_version": "numbers-v1",
        "eval_version": "numbers-test-v1",
        "owner": "learning-genai",
    },
)

print(job.id)
```

Run:

```bash
export TRAINING_FILE_ID="file-..."
export VALIDATION_FILE_ID="file-..."
python scripts/openai_create_finetune.py
```

PowerShell:

```powershell
$env:TRAINING_FILE_ID="file-..."
$env:VALIDATION_FILE_ID="file-..."
python scripts\openai_create_finetune.py
```

### Parameter Meaning

| Parameter | What it means | Beginner advice |
|-----------|---------------|-----------------|
| `model` | Base model being adapted | Use a currently supported fine-tunable model |
| `training_file` | Uploaded train JSONL file ID | Required |
| `validation_file` | Uploaded validation JSONL file ID | Use it unless you have a strong reason not to |
| `method.type` | Fine-tuning method | Use `supervised` for this project |
| `n_epochs` | Full passes over training data | Start with `auto` |
| `batch_size` | Examples per training update | Start with `auto` |
| `learning_rate_multiplier` | How strongly updates move the model | Start with `auto` |
| `suffix` | Name suffix for the output model | Include task and version |
| `metadata` | Extra searchable information | Store dataset and eval versions |

OpenAI supported models and method shapes can change. Check the official docs
before running a paid job.

### Hyperparameters in Plain English

The job uses:

```json
{
  "n_epochs": "auto",
  "batch_size": "auto",
  "learning_rate_multiplier": "auto"
}
```

These are the training knobs:

| Hyperparameter | Plain Meaning | If Too Low | If Too High |
|----------------|---------------|------------|-------------|
| `n_epochs` | How many times the trainer sees the full training set | Model may not learn the pattern | Model may memorize examples |
| `batch_size` | How many examples are grouped into one update | Updates may be noisy | Needs more memory; may generalize worse |
| `learning_rate_multiplier` | How strongly each update changes behavior | Model barely changes | Model may overfit or become unstable |

Use `auto` for a first run. Change these only after reviewing eval failures.

Beginner rule:

```text
First improve data. Then consider hyperparameters.
```

### Job Metadata

The `metadata` block is optional but useful:

```json
{
  "dataset_version": "numbers-v1",
  "eval_version": "numbers-test-v1",
  "owner": "learning-genai"
}
```

It helps future you answer:

- Which dataset produced this model?
- Which eval set was used?
- Who owns the experiment?
- Is this model safe to delete?

### Dry Run Before Starting a Paid Job

Before creating the job, confirm:

- `data/openai/train.jsonl` exists.
- `data/openai/validation.jsonl` exists.
- JSONL validation passes.
- You know which base model is supported.
- You understand pricing and availability.
- You have permission to upload the dataset.
- You have a test set that will not be used for training.

For this toy project, the data is safe. For real projects, this check is
non-negotiable.

### Monitor the Job

Create `scripts/openai_monitor_finetune.py`:

```python
import os
from openai import OpenAI

client = OpenAI()
job_id = os.environ["FINE_TUNE_JOB_ID"]

job = client.fine_tuning.jobs.retrieve(job_id)
print("status:", job.status)
print("fine_tuned_model:", job.fine_tuned_model)

events = client.fine_tuning.jobs.list_events(
    fine_tuning_job_id=job_id,
    limit=10,
)

for event in events.data:
    print(event.created_at, event.message)
```

Run:

```bash
export FINE_TUNE_JOB_ID="ftjob-..."
python scripts/openai_monitor_finetune.py
```

### Job Statuses

You may see statuses like:

| Status | Meaning | What To Do |
|--------|---------|------------|
| `validating_files` | Files are being checked | Wait |
| `queued` | Job is waiting for capacity | Wait |
| `running` | Training is in progress | Monitor events |
| `succeeded` | Training completed | Run holdout eval |
| `failed` | Training did not complete | Inspect error, fix data/config |
| `cancelled` | Job was cancelled | Confirm whether cleanup is needed |

Do not deploy at `succeeded` automatically. Move to evaluation.

### If the Job Fails

Common causes:

- Invalid JSONL.
- Unsupported model or method.
- File uploaded with the wrong purpose.
- Dataset too small or malformed.
- Account does not have fine-tuning access.
- API key lacks required permissions.

Fix the cause, create a new version note, and retry. Do not overwrite your
experiment record.

### Use the Fine-Tuned Model

Create `scripts/openai_try_finetuned_model.py`:

```python
import os
from openai import OpenAI

client = OpenAI()
model = os.environ["FINE_TUNED_MODEL"]

response = client.responses.create(
    model=model,
    input=[
        {"role": "system", "content": "Answer using the required number facts template."},
        {"role": "user", "content": "Tell me about number 121."},
    ],
)

print(response.output_text)
```

Run:

```bash
export FINE_TUNED_MODEL="ft:..."
python scripts/openai_try_finetuned_model.py
```

### Evaluate the Fine-Tuned Model on Test Data

Create `scripts/openai_eval_finetuned_model.py`:

```python
import json
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI()
model = os.environ["FINE_TUNED_MODEL"]

def normalize(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())

rows = [json.loads(line) for line in Path("data/local/test_raw.jsonl").read_text(encoding="utf-8").splitlines()]

correct = 0
for row in rows:
    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": "Answer using the required number facts template."},
            {"role": "user", "content": row["prompt"]},
        ],
    )

    actual = normalize(response.output_text)
    expected = normalize(row["completion"])
    correct += int(actual == expected)

print({"examples": len(rows), "exact_match": correct / len(rows)})
```

Concept link: deployment should depend on holdout performance, not training job
status.

### OpenAI Deployment Pattern

In a production app, avoid scattering the fine-tuned model ID through code.
Put it in config:

```json
{
  "number_tutor": {
    "model": "ft:...",
    "fallback_model": "gpt-4.1-nano-2025-04-14",
    "dataset_version": "numbers-v1",
    "eval_version": "numbers-test-v1"
  }
}
```

Then your app reads the config:

```python
MODEL_CONFIG = {
    "number_tutor": {
        "model": "ft:...",
        "fallback_model": "gpt-4.1-nano-2025-04-14",
    }
}
```

This makes rollback simple. Change config, redeploy, and the app returns to the
previous model.

### OpenAI Path Checklist

Complete this before calling the OpenAI path done:

- Training file uploaded.
- Validation file uploaded.
- Fine-tuning job created.
- Job status checked.
- Fine-tuned model ID recorded.
- Test-set eval run.
- Failures inspected.
- Deployment decision documented.
- Cost and usage reviewed.

## Step 7: Local LoRA Fine-Tuning

Use local LoRA when:

- You want to train an open model.
- You need local or self-hosted deployment.
- You have access to a GPU.
- You want small adapter files instead of a full fine-tuned model.

LoRA stands for Low-Rank Adaptation. Instead of changing all model weights, it
adds small trainable adapter matrices to selected layers. The base model stays
mostly frozen.

Mental model:

```text
base model knowledge + small trainable adapter = task-specific behavior
```

This is why LoRA is popular: adapter files are much smaller than full model
checkpoints.

Computer specification:

- CPU only: okay for reading code, not practical for real training.
- 8 GB VRAM: try very small models only.
- 12-16 GB VRAM: small 1B-3B models with careful settings.
- 24 GB VRAM: more comfortable for 3B-7B QLoRA.
- 48 GB+ VRAM: larger models or longer sequence lengths.

Install:

```bash
pip install -U transformers datasets accelerate peft trl bitsandbytes
```

For native Windows, GPU training can be tricky. WSL2 or Linux is usually easier.

### Local Setup Checklist

Before running LoRA training:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
python -c "import transformers, datasets, peft, trl; print('libraries ok')"
```

If CUDA is available, you should see:

```text
True
```

If not, fix your PyTorch/CUDA/driver setup or use AWS EC2.

### Optional: Configure Accelerate

`accelerate` helps launch training consistently.

```bash
accelerate config
```

For a simple single-GPU beginner setup, choose answers like:

```text
compute environment: This machine
distributed training: No distributed training
mixed precision: bf16 if supported, otherwise fp16 or no
```

You can also run scripts directly with `python`, but `accelerate launch` is a
good habit for training workflows.

### Download the Base Model

This example uses a small open instruct model:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
)
```

The first run downloads model files from Hugging Face into the local cache.
Always check the model license before using a model commercially.

### Choosing a Base Model

For learning, choose a small instruct model:

| Model Size | Beginner Use |
|------------|--------------|
| 0.5B-1B | Best for first workflow tests |
| 2B-3B | Better quality, more GPU memory |
| 7B | Common practical size, usually needs QLoRA on 24 GB GPUs |
| 13B+ | More advanced, higher cost and memory |

The example uses `Qwen/Qwen2.5-0.5B-Instruct` because it is small enough for
learning. For real use, model choice depends on license, quality, language,
context length, hardware, and deployment plan.

### Train a LoRA Adapter

Create `scripts/local_lora_train.py`:

```python
from datasets import load_dataset
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

dataset = load_dataset(
    "json",
    data_files={
        "train": "data/local/train.jsonl",
        "validation": "data/local/validation.jsonl",
    },
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules="all-linear",
    task_type="CAUSAL_LM",
)

args = SFTConfig(
    output_dir="outputs/number-tutor-lora",
    max_length=512,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    logging_steps=10,
    save_strategy="epoch",
    eval_strategy="epoch",
)

trainer = SFTTrainer(
    model=model_name,
    args=args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    peft_config=lora_config,
)

trainer.train()
trainer.save_model("outputs/number-tutor-lora/final")
```

Run:

```bash
accelerate launch scripts/local_lora_train.py
```

Concept link: the base model stays mostly frozen. LoRA trains small adapter
weights that steer the model toward the number tutor format.

### LoRA Parameter Meaning

| Parameter | Meaning | Beginner Guidance |
|-----------|---------|-------------------|
| `r` | LoRA rank, adapter capacity | Start with 8 or 16 |
| `lora_alpha` | Scaling factor for adapter updates | Often 2x `r`, such as 32 for `r=16` |
| `lora_dropout` | Dropout regularization | 0.0-0.1 is common |
| `target_modules` | Which model layers get adapters | `all-linear` is convenient when supported |
| `num_train_epochs` | Full passes over train set | Start with 1-3 |
| `per_device_train_batch_size` | Examples per GPU step | Lower if out of memory |
| `gradient_accumulation_steps` | Mini-steps before one optimizer update | Increase to simulate bigger batch |
| `learning_rate` | Update size | `2e-4` is a common LoRA starting point |
| `max_length` | Maximum token length per example | Lower to reduce memory |

### Effective Batch Size

Local training often uses gradient accumulation.

```text
effective_batch_size =
  per_device_train_batch_size * gradient_accumulation_steps * number_of_gpus
```

For the example:

```text
2 * 8 * 1 = 16
```

That means the trainer applies one optimizer update after accumulating the
effect of 16 examples.

### What Training Output Means

During training, you may see:

```text
loss: 1.842
loss: 0.913
eval_loss: 0.721
```

Loss going down usually means the model is learning the target tokens. But low
loss does not automatically mean the model is useful. Always run the test-set
eval after training.

### What Gets Saved

The LoRA output directory usually contains adapter files such as:

```text
adapter_config.json
adapter_model.safetensors
tokenizer files or training metadata
```

The adapter is not the full base model. To use it, load:

```text
base model + adapter
```

If you move the adapter to another machine, that machine also needs access to
the same base model.

## Step 8: Local QLoRA Fine-Tuning

QLoRA is LoRA plus 4-bit quantization. It reduces memory by loading the base
model in a compact format.

Use QLoRA when the LoRA version runs out of GPU memory.

The tradeoff is complexity. QLoRA needs quantization support, usually through
`bitsandbytes`, and tends to be smoother on Linux with NVIDIA GPUs.

Mental model:

```text
LoRA:  full-precision base model + train adapters
QLoRA: 4-bit base model + train adapters
```

The base model is compact, but the adapters still learn useful task-specific
updates.

Create `scripts/local_qlora_train.py`:

```python
import torch
from datasets import load_dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

dataset = load_dataset(
    "json",
    data_files={
        "train": "data/local/train.jsonl",
        "validation": "data/local/validation.jsonl",
    },
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quant_config,
    device_map="auto",
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules="all-linear",
    task_type="CAUSAL_LM",
)

args = SFTConfig(
    output_dir="outputs/number-tutor-qlora",
    max_length=512,
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,
    learning_rate=2e-4,
    logging_steps=10,
    save_strategy="epoch",
    eval_strategy="epoch",
)

trainer = SFTTrainer(
    model=model,
    processing_class=tokenizer,
    args=args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    peft_config=lora_config,
)

trainer.train()
trainer.save_model("outputs/number-tutor-qlora/final")
```

Run:

```bash
accelerate launch scripts/local_qlora_train.py
```

Concept link: QLoRA keeps the big base model compact and trains small adapter
weights. This is why it can fit on smaller GPUs than full fine-tuning.

### QLoRA Parameter Meaning

| Parameter | Meaning |
|-----------|---------|
| `load_in_4bit=True` | Load base model weights in 4-bit |
| `bnb_4bit_quant_type="nf4"` | Use NormalFloat 4-bit quantization, common for QLoRA |
| `bnb_4bit_compute_dtype=torch.bfloat16` | Use BF16 for compute when supported |
| `bnb_4bit_use_double_quant=True` | Add nested quantization to reduce memory further |
| `per_device_train_batch_size=1` | Lower memory than batch size 2 |
| `gradient_accumulation_steps=16` | Keeps effective batch size reasonable |

If BF16 is not supported on your GPU, try FP16:

```python
bnb_4bit_compute_dtype=torch.float16
```

### LoRA vs QLoRA Decision

Use LoRA when:

- The base model fits comfortably in GPU memory.
- You want a simpler setup.
- Training speed is acceptable.

Use QLoRA when:

- You get out-of-memory errors with LoRA.
- You want to try a larger model on the same GPU.
- You are comfortable debugging CUDA/bitsandbytes issues.

### Out-of-Memory Checklist

If training fails with CUDA out-of-memory:

1. Reduce `per_device_train_batch_size`.
2. Reduce `max_length`.
3. Increase `gradient_accumulation_steps`.
4. Use QLoRA instead of LoRA.
5. Lower LoRA rank from `16` to `8`.
6. Use a smaller base model.
7. Restart the Python process to clear GPU memory.

Check GPU memory:

```bash
nvidia-smi
```

You can watch memory during training:

```bash
watch -n 1 nvidia-smi
```

On Windows PowerShell:

```powershell
while ($true) { nvidia-smi; Start-Sleep -Seconds 1; Clear-Host }
```

## Step 9: Local Inference With the Adapter

Create `scripts/local_try_adapter.py`:

```python
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model = "Qwen/Qwen2.5-0.5B-Instruct"
adapter_path = "outputs/number-tutor-lora/final"

tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
model = PeftModel.from_pretrained(model, adapter_path)

prompt = (
    "### System:\n"
    "Answer using the required number facts template.\n\n"
    "### User:\n"
    "Tell me about number 121.\n\n"
    "### Assistant:\n"
)

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(
    **inputs,
    max_new_tokens=120,
    temperature=0.0,
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

For QLoRA, change:

```python
adapter_path = "outputs/number-tutor-qlora/final"
```

### Evaluate the Adapter on the Test Set

Trying one prompt is useful, but it is not evaluation. Create a script that runs
the adapter against every holdout example.

Create `scripts/local_eval_adapter.py`:

```python
import json
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model = "Qwen/Qwen2.5-0.5B-Instruct"
adapter_path = "outputs/number-tutor-lora/final"

tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
model = PeftModel.from_pretrained(model, adapter_path)
model.eval()

def normalize(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())

def predict(prompt_text: str) -> str:
    prompt = (
        "### System:\n"
        "Answer using the required number facts template.\n\n"
        "### User:\n"
        f"{prompt_text}\n\n"
        "### Assistant:\n"
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=False,
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded.split("### Assistant:")[-1].strip()

rows = [
    json.loads(line)
    for line in Path("data/local/test_raw.jsonl").read_text(encoding="utf-8").splitlines()
]

correct = 0
failures = []

for row in rows:
    actual = normalize(predict(row["prompt"]))
    expected = normalize(row["completion"])
    ok = actual == expected
    correct += int(ok)
    if not ok:
        failures.append({
            "prompt": row["prompt"],
            "expected": expected,
            "actual": actual,
        })

print({"examples": len(rows), "exact_match": correct / len(rows)})
print(json.dumps(failures[:5], indent=2))
```

Run:

```bash
python scripts/local_eval_adapter.py
```

If the adapter path points to the QLoRA output, change:

```python
adapter_path = "outputs/number-tutor-qlora/final"
```

### Reading Local Eval Failures

If the model gets the numbers right but changes headings, the model learned the
math but not the format.

If it keeps the headings but gets arithmetic wrong, the model learned the format
but generation quality is weak.

If it outputs long unrelated text, check:

- Prompt formatting.
- Whether the correct adapter path is loaded.
- Whether training actually completed.
- Whether the base model's chat format differs from your simple template.

This is why the test set and failure inspection matter.

## Step 10: AWS EC2 When Your Computer Is Not Enough

Use AWS EC2 when:

- Your local machine has no NVIDIA GPU.
- Your GPU has too little VRAM.
- You need a Linux CUDA environment.
- You want to run experiments without changing your laptop setup.

Cloud GPU setup has three jobs:

1. Rent the right GPU.
2. Set up a safe Linux training environment.
3. Shut it down correctly when finished.

Most beginner mistakes are in job 3. GPU instances can be expensive if left
running.

Official AWS references:

- [EC2 accelerated computing instance types](https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html)
- [Get started with GPU accelerated instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/gpu-instances-started.html)
- [AWS Deep Learning AMIs](https://docs.aws.amazon.com/dlami/latest/devguide/)

### Choosing an Instance

Beginner options:

| Instance family | Typical use |
|-----------------|-------------|
| G4dn | Older NVIDIA T4 option, useful for small experiments |
| G5 | NVIDIA A10G, common for small/medium LLM experiments |
| G6 | Newer GPU family where available |
| P4/P5/P6 | Larger training, expensive, usually not needed for this project |

For this number tutor project, start with a modest GPU instance such as a G5 or
G6 size if available in your region. Check quotas before launching.

### Before You Launch

Check:

- AWS account has permission to launch EC2 instances.
- Your region has GPU capacity.
- Your service quota allows the GPU instance family.
- You understand hourly pricing.
- You have an SSH key pair.
- You know whether you plan to stop or terminate the instance after training.

If AWS says your quota is too low, request a quota increase for the specific GPU
instance family in the target region.

### Storage Planning

Model files can be large. Use enough EBS storage:

| Project Type | Suggested Storage |
|--------------|-------------------|
| This tiny walkthrough | 50-100 GB |
| Small open models | 100-200 GB |
| Multiple 7B experiments | 200 GB+ |

Hugging Face caches models under a cache directory, often in the user's home
directory. If storage fills up, training can fail even if GPU memory is fine.

### Launch Checklist

In the AWS console:

1. Choose an Ubuntu or AWS Deep Learning AMI with GPU support.
2. Choose a GPU instance type.
3. Use at least 100 GB EBS storage for model files and caches.
4. Create or select an SSH key pair.
5. Restrict SSH port 22 to your own IP address.
6. Launch the instance.
7. Stop or terminate it when finished to avoid ongoing cost.

Security group guidance:

```text
Inbound SSH:
  Type: SSH
  Port: 22
  Source: your current public IP only
```

Do not open SSH to `0.0.0.0/0` for a teaching project.

### Connect

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_PUBLIC_IP
```

On some AMIs, the user may be `ec2-user` instead of `ubuntu`.

If SSH fails:

- Confirm the instance is running.
- Confirm you used the correct public IP.
- Confirm the security group allows your current IP.
- Confirm the key file matches the selected key pair.
- Confirm the username for the AMI.

### Verify GPU

```bash
nvidia-smi
python3 -c "import torch; print(torch.cuda.is_available())"
```

If PyTorch is not installed yet, create an environment first.

Expected `nvidia-smi` output includes:

- Driver version
- CUDA version
- GPU name
- Memory usage

If `nvidia-smi` is missing, you may have chosen a non-GPU AMI or need to install
drivers. Using an AWS Deep Learning AMI often avoids this.

### Set Up Python Environment

```bash
sudo apt update
sudo apt install -y python3-venv git

python3 -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install -U transformers datasets accelerate peft trl bitsandbytes
```

Optional but useful:

```bash
sudo apt install -y tmux htop nvtop
```

Use `tmux` so training keeps running if your SSH connection drops:

```bash
tmux new -s finetune
accelerate launch scripts/local_qlora_train.py
```

Detach from tmux:

```text
Ctrl-b then d
```

Reconnect:

```bash
tmux attach -t finetune
```

### Move the Project to EC2

Option 1: clone your repository:

```bash
git clone YOUR_REPO_URL
cd LearningGenAI/sessions/09_fine_tuning
```

Option 2: copy only the session folder:

```bash
scp -i your-key.pem -r sessions/09_fine_tuning ubuntu@YOUR_PUBLIC_IP:~/09_fine_tuning
```

Then run:

```bash
python scripts/validate_number_dataset.py
python scripts/prepare_splits.py
accelerate launch scripts/local_qlora_train.py
```

### Download Results Back to Your Machine

Copy adapter outputs back:

```bash
scp -i your-key.pem -r ubuntu@YOUR_PUBLIC_IP:~/09_fine_tuning/outputs ./outputs_from_ec2
```

If you cloned the full repo into `~/LearningGenAI`, adjust the path:

```bash
scp -i your-key.pem -r ubuntu@YOUR_PUBLIC_IP:~/LearningGenAI/sessions/09_fine_tuning/outputs ./outputs_from_ec2
```

Keep:

- Adapter directory
- Training logs
- Eval report
- Exact script versions
- Dataset split files

These are the artifacts needed to reproduce the experiment.

### EC2 Cost Safety

Before leaving:

```bash
exit
```

Then stop or terminate the instance in the AWS console. Stopping usually stops
compute charges, but storage charges can continue. Terminating deletes the
instance, and depending on settings may delete attached storage.

Cost safety checklist:

- Stop or terminate the instance.
- Delete unused EBS volumes if they are no longer needed.
- Delete old snapshots if created.
- Check the AWS billing dashboard.
- Record approximate cost in the experiment note.

### EC2 Troubleshooting

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Cannot SSH | Wrong username, key, IP, or security group | Recheck AMI username and inbound rules |
| `nvidia-smi` not found | No GPU driver or wrong AMI | Use Deep Learning AMI or install drivers |
| PyTorch CUDA is false | CPU PyTorch installed or CUDA mismatch | Install CUDA-compatible PyTorch |
| Out of disk | Model cache or outputs filled EBS | Increase EBS or clean cache |
| Out of memory | Model too large or batch too high | Use QLoRA, smaller batch, smaller model |
| Training stops when laptop sleeps | SSH disconnected without tmux | Run training inside `tmux` |
| Bill is higher than expected | Instance left running | Stop/terminate and set billing alerts |

## Step 11: Compare the Three Paths

| Path | Best When | Output Artifact |
|------|-----------|-----------------|
| OpenAI hosted fine-tuning | You want managed training and OpenAI-hosted inference | Fine-tuned model ID |
| Local LoRA | You have enough GPU memory for the base model | Adapter directory |
| Local QLoRA | You need lower GPU memory use | Adapter directory trained with quantized base |

All three paths still need:

- Good data
- Clean splits
- Validation
- Baseline eval
- Holdout test eval
- Versioning
- Rollback plan

### Comparison Questions

After running one or more paths, answer:

- Which path was easiest to run?
- Which path produced the best holdout score?
- Which path had the lowest operational burden?
- Which path fits your deployment target?
- Which path is easiest to roll back?
- Which path has acceptable cost and latency?

For this toy project, the hosted and local paths are mostly learning exercises.
For a real project, these questions decide architecture.

### Result Table Template

```text
Dataset: numbers-v1
Test examples: 20

| System | Exact Match | Notes |
|--------|-------------|-------|
| Formula baseline | 1.00 | Deterministic upper reference |
| Base model prompt | <score> | Prompt used: ... |
| OpenAI SFT | <score> | Model ID: ft:... |
| LoRA adapter | <score> | Adapter: outputs/number-tutor-lora/final |
| QLoRA adapter | <score> | Adapter: outputs/number-tutor-qlora/final |
```

If a fine-tuned model does not beat the best practical baseline, do not deploy
it. Fine-tuning is valuable only when it improves the actual workflow.

## Step 12: Deployment Decision

Deployment is a decision, not an automatic next step after training.

For this number tutor project, deployment might mean "we can use this adapter in
a demo." For production, deployment means routing real user traffic.

### Deploy Only If

- Holdout eval beats the baseline that matters.
- Output format is reliable enough for downstream code.
- Safety checks pass.
- Latency is acceptable.
- Cost is acceptable.
- Rollback is simple.
- The model version is documented.

### Do Not Deploy If

- It only performs well on training examples.
- It fails common holdout cases.
- It is slower or more expensive without a quality gain.
- It returns invalid schema too often.
- You cannot explain what data trained it.
- You cannot roll back quickly.

### Model Version Record

Create a model record:

```json
{
  "model_name": "number-tutor-lora-v1",
  "training_path": "local_lora",
  "base_model": "Qwen/Qwen2.5-0.5B-Instruct",
  "adapter_path": "outputs/number-tutor-lora/final",
  "dataset_version": "numbers-v1",
  "split_seed": 42,
  "train_examples": 160,
  "validation_examples": 20,
  "test_examples": 20,
  "test_exact_match": 0.0,
  "approved_for_demo": false,
  "owner": "learning-genai"
}
```

Update the score and approval fields after evaluation.

## Step 13: Troubleshooting Guide

| Symptom | What It Usually Means | First Fix |
|---------|-----------------------|-----------|
| JSONL upload fails | Bad JSONL structure | Run validators and inspect line number |
| Fine-tuned output has wrong format | Training examples inconsistent or too few | Fix data and add format-focused examples |
| Model memorizes examples | Overfitting | Fewer epochs, more varied data, lower LR |
| Model ignores task | Underfitting or prompt mismatch | More examples, stronger prompt, check formatting |
| Local training OOM | GPU memory too small | Use QLoRA, smaller batch, smaller model |
| Adapter output is nonsense | Prompt format mismatch or wrong adapter | Match training prompt and check adapter path |
| Eval score looks perfect | Possible leakage | Ensure test examples were not in train |
| OpenAI access denied | Fine-tuning unavailable or key lacks access | Use local LoRA/QLoRA path |
| AWS bill surprise | Instance left running | Stop/terminate and set billing alerts |

## Step 14: Beginner Glossary

| Term | Meaning |
|------|---------|
| Base model | The pretrained model before your training |
| Fine-tuned model | A model adapted with your examples |
| Adapter | Small trainable weights attached to a frozen base model |
| LoRA | Adapter method that trains low-rank matrices |
| QLoRA | LoRA with a quantized base model to save memory |
| JSONL | One JSON object per line |
| Train set | Examples used for learning |
| Validation set | Examples used to monitor and tune experiments |
| Test set | Held-out examples used for final evaluation |
| Epoch | One full pass through the training set |
| Batch size | Number of examples used in one training update |
| Learning rate | How large each update is |
| Loss | A number measuring how wrong the model was during training |
| Overfitting | Memorizing training examples instead of learning the pattern |
| Underfitting | Not learning enough from the examples |
| Checkpoint | Saved model or adapter state |
| Quantization | Storing model weights with fewer bits |
| VRAM | GPU memory |

## Step 15: End-to-End Checklist

Use this as the final project checklist:

```text
[ ] I can explain what behavior the model should learn.
[ ] I inspected the raw dataset.
[ ] I validated raw JSONL.
[ ] I created train/validation/test splits.
[ ] I know which files are for OpenAI and which are for local training.
[ ] I ran a baseline eval.
[ ] I understand the OpenAI hosted path and its availability caveat.
[ ] I understand what LoRA trains.
[ ] I understand why QLoRA uses less memory.
[ ] I can choose local hardware or AWS EC2 for training.
[ ] I can run or explain the training script.
[ ] I can load an adapter for inference.
[ ] I can evaluate the trained model on the holdout test set.
[ ] I can document whether the fine-tune should be deployed.
[ ] I know how to roll back.
```

## Step 16: How to Extend This Project

Once you finish the number tutor project, try one extension:

- Add numbers 201-500 and compare results.
- Add negative numbers and update validation.
- Change the output to strict JSON.
- Build a ticket classifier dataset.
- Add a safety/refusal category.
- Compare base model prompting vs LoRA.
- Try a larger model on EC2 with QLoRA.

The most useful next exercise is converting the output to strict JSON because it
resembles many real application fine-tuning tasks.

Example target:

```json
{
  "number": 8,
  "parity": "even",
  "double": 16,
  "square": 64,
  "explanation": "8 is an even number. Its double is 16 and its square is 64."
}
```

## Common Beginner Mistakes

Avoid:

- Training before defining success.
- Evaluating on the training set.
- Mixing train and test examples.
- Uploading secrets or personal data.
- Changing many hyperparameters before fixing bad data.
- Assuming a successful job means a better model.
- Using local LoRA results without testing the same holdout set.
- Forgetting cloud instances are still billable when left running.

## Suggested Learning Order

1. Read the concept files in `concepts/`.
2. Validate the existing dataset.
3. Create train/validation/test splits.
4. Run the no-API local validation scripts.
5. Try OpenAI hosted fine-tuning if you have an API key.
6. Try local LoRA/QLoRA if you have a CUDA GPU or EC2 instance.
7. Compare results on the same test set.

## References

- [OpenAI model optimization guide](https://platform.openai.com/docs/guides/fine-tuning)
- [OpenAI supervised fine-tuning guide](https://platform.openai.com/docs/guides/supervised-fine-tuning)
- [OpenAI fine-tuning API reference](https://platform.openai.com/docs/api-reference/fine-tuning)
- [Hugging Face TRL SFTTrainer docs](https://huggingface.co/docs/trl/sft_trainer)
- [Hugging Face PEFT LoRA docs](https://huggingface.co/docs/peft/main/en/developer_guides/lora)
- [Hugging Face bitsandbytes quantization docs](https://huggingface.co/docs/transformers/quantization/bitsandbytes)
- [AWS EC2 accelerated computing instance types](https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html)
- [AWS GPU accelerated instances guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/gpu-instances-started.html)
