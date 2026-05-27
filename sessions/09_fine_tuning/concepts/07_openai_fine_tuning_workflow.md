# 07. OpenAI Fine-Tuning Workflow

OpenAI fine-tuning is a hosted workflow. You prepare the data and job
configuration; OpenAI runs the training infrastructure and returns a fine-tuned
model ID when the job succeeds.

Reference: [OpenAI fine-tuning API reference](https://platform.openai.com/docs/api-reference/fine-tuning)

Important availability note: the current OpenAI supervised fine-tuning docs say
the fine-tuning platform is being wound down and is no longer accessible to new
users, while existing users can continue creating jobs for a limited period. Use
the OpenAI hosted steps only if your account has access. The data design,
splitting, validation, and eval workflow still applies directly to LoRA/QLoRA.

## Workflow Overview

1. Prepare JSONL training data.
2. Prepare a validation file.
3. Upload files with purpose `fine-tune`.
4. Create a fine-tuning job.
5. Monitor job status, events, and metrics.
6. Evaluate the resulting fine-tuned model on a holdout test set.
7. Deploy only if evals improve.

Do not skip evals. A successful training job means the job completed, not that
the model is better for your product.

## Supported Methods

The OpenAI model optimization guide documents several optimization methods,
including:

- Supervised fine-tuning (SFT)
- Vision fine-tuning
- Direct preference optimization (DPO)
- Reinforcement fine-tuning (RFT)

It also lists specific model families for each method. At the time this material
was updated, the supervised fine-tuning page listed `gpt-4.1-2025-04-14`,
`gpt-4.1-mini-2025-04-14`, and `gpt-4.1-nano-2025-04-14` for SFT. Check the
official docs before creating a job because supported models and access rules
can change.

Reference: [OpenAI model optimization guide](https://platform.openai.com/docs/guides/fine-tuning)

## Step 1: Prepare JSONL

For SFT with chat-style data, each line should be one training conversation:

```jsonl
{"messages":[{"role":"system","content":"Answer using the required number facts template."},{"role":"user","content":"Tell me about number 8."},{"role":"assistant","content":"Number: 8\nParity: Even\nDouble: 16\nSquare: 64\nSimple explanation: 8 is an even number. Its double is 16 and its square is 64."}]}
```

OpenAI's supervised fine-tuning guide describes the workflow as building a
dataset, uploading examples, creating a job, and evaluating the result.

Reference: [OpenAI supervised fine-tuning guide](https://platform.openai.com/docs/guides/supervised-fine-tuning)

## Step 2: Upload Files

Training files must be uploaded with purpose `fine-tune`.

```python
from openai import OpenAI

client = OpenAI()

training_file = client.files.create(
    file=open("data/train.jsonl", "rb"),
    purpose="fine-tune",
)

validation_file = client.files.create(
    file=open("data/validation.jsonl", "rb"),
    purpose="fine-tune",
)

print(training_file.id)
print(validation_file.id)
```

Keep the returned file IDs. The fine-tuning job uses those IDs, not the local
file paths.

## Step 3: Create a Job

Use a supported base model from the current OpenAI docs. The model below is an
example; always confirm current support before running.

```python
job = client.fine_tuning.jobs.create(
    model="gpt-4.1-nano-2025-04-14",
    training_file=training_file.id,
    validation_file=validation_file.id,
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
        "eval_version": "numbers-holdout-v1",
        "owner": "learning-genai",
    },
)

print(job.id)
```

In the current API reference, fine-tuning method-specific hyperparameters are
passed under `method`. Older examples may show a top-level `hyperparameters`
field; prefer the current API reference.

## What the Important Parameters Mean

| Parameter | Meaning | Beginner Guidance |
|-----------|---------|-------------------|
| `model` | Base model to fine-tune | Use a model listed as fine-tunable in current docs |
| `training_file` | File ID for training examples | Required |
| `validation_file` | File ID for validation examples | Strongly recommended |
| `method.type` | Fine-tuning method | Use `supervised` for standard SFT |
| `n_epochs` | Number of passes over training data | Start with `auto` |
| `batch_size` | Examples per update | Start with `auto` |
| `learning_rate_multiplier` | Scales update size | Start with `auto` |
| `suffix` | Human-readable model suffix | Include task and version |
| `metadata` | Searchable job metadata | Store dataset/eval/owner info |

## Step 4: Monitor the Job

```python
job = client.fine_tuning.jobs.retrieve("ftjob-your-job-id")
print(job.status)
print(job.fine_tuned_model)
```

List events:

```python
events = client.fine_tuning.jobs.list_events(
    fine_tuning_job_id="ftjob-your-job-id",
    limit=20,
)

for event in events.data:
    print(event.created_at, event.message)
```

Important statuses include validating files, queued, running, succeeded, failed,
and cancelled. If a job fails, inspect the error and fix the dataset or job
configuration before retrying.

## Step 5: Evaluate Before Deployment

When the job succeeds, use the fine-tuned model ID on your holdout test set:

```python
fine_tuned_model = job.fine_tuned_model

response = client.responses.create(
    model=fine_tuned_model,
    input="Tell me about number 121.",
)

print(response.output_text)
```

Compare against:

- Base model with your best prompt
- Previous production model, if any
- Deterministic baseline, if relevant
- Holdout expected answers

## Step 6: Deploy Safely

Production config should store the model ID and its lineage:

```json
{
  "task": "number_tutor",
  "model": "ft:...",
  "base_model": "gpt-4.1-nano-2025-04-14",
  "dataset_version": "numbers-v1",
  "eval_version": "numbers-holdout-v1"
}
```

Do not hard-code a fine-tuned model ID across many services. Put it behind a
config value or model alias so rollback is simple.

## Hosted Fine-Tuning vs Local LoRA

Hosted OpenAI fine-tuning:

- No GPU setup
- Provider manages training
- You receive a model ID
- Best when you want OpenAI-hosted inference

Local LoRA/QLoRA:

- You manage the GPU environment
- You choose an open model
- You train and store adapter files
- Best when you need local control or open-source deployment

The dataset design principles are almost the same. The file wrappers and
training code differ.

## Key Takeaways

1. Hosted fine-tuning starts with JSONL files and a fine-tuning job.
2. The file upload purpose must be `fine-tune`.
3. Use the current `method` shape for supervised hyperparameters.
4. Supported models and methods change, so check official docs.
5. Job success is not product success.
6. Deploy only after holdout evals beat the baseline and safety checks pass.
