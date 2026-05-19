# 07. OpenAI Fine-Tuning Workflow

OpenAI fine-tuning is a hosted workflow:

1. Prepare JSONL training data.
2. Upload the file with purpose `fine-tune`.
3. Create a fine-tuning job.
4. Monitor job status and events.
5. Evaluate the resulting fine-tuned model.
6. Deploy only if evals improve.

Reference: [OpenAI fine-tuning API reference](https://platform.openai.com/docs/api-reference/fine-tuning)

## Supported Methods

The OpenAI model optimization guide currently documents:

- Supervised fine-tuning (SFT)
- Vision fine-tuning
- Direct preference optimization (DPO)
- Reinforcement fine-tuning (RFT)

It also lists specific model families for each method. Check the official docs
before creating a job because supported models can change.

Reference: [OpenAI model optimization guide](https://platform.openai.com/docs/guides/fine-tuning)

## File Upload

Training files must be JSONL and uploaded for fine-tuning.

Conceptual API shape:

```python
training_file = client.files.create(
    file=open("train.jsonl", "rb"),
    purpose="fine-tune",
)
```

The returned file ID is used in the job request.

## Create Job

Conceptual API shape:

```python
job = client.fine_tuning.jobs.create(
    model="gpt-4.1-mini-2025-04-14",
    training_file=training_file.id,
    validation_file=validation_file.id,
    method={
        "type": "supervised",
        "supervised": {
            "hyperparameters": {
                "n_epochs": "auto",
                "batch_size": "auto",
                "learning_rate_multiplier": "auto"
            }
        }
    },
    suffix="ticket-router-v1",
)
```

Use current docs for exact method shape and supported model names.

## Job Lifecycle

Track:

- Job ID
- Base model
- Training file
- Validation file
- Status
- Error
- Result files
- Fine-tuned model name
- Created/finished timestamps

Do not deploy just because a job succeeded. A successful job only means training
completed.

## Events and Metrics

Monitor:

- Training loss
- Validation loss
- Job errors
- Warnings
- Result files
- Eval scores

If validation gets worse while training improves, suspect overfitting.

## Using the Fine-Tuned Model

After a successful job, the platform returns a fine-tuned model name. Use it like
another model ID in inference calls, subject to the API surface supported by that
model.

Production config should store:

```json
{
  "task": "ticket_router",
  "model": "ft:...",
  "base_model": "gpt-4.1-mini-2025-04-14",
  "dataset_version": "tickets-v3",
  "eval_version": "ticket-router-eval-v2"
}
```

## Key Takeaways

1. Hosted fine-tuning starts with JSONL files and a fine-tuning job.
2. The file upload purpose must be `fine-tune`.
3. Supported models and methods change, so check official docs.
4. Job success is not product success.
5. Deploy only after evals beat the baseline and safety checks pass.
