# 02. What Is Fine-Tuning?

Fine-tuning adapts a pretrained model to behave better for a specific task,
style, domain, or output contract by training it on examples.

The base model already knows language, reasoning patterns, code, and broad world
knowledge. Fine-tuning changes the model's behavior by showing it repeated,
high-quality examples of what "good" looks like for your application.

## DevOps Analogy

A base model is like a golden container image:

```
ubuntu:latest
```

It is general-purpose. Fine-tuning is like building a custom image:

```
FROM ubuntu
COPY company-runner-config /etc/runner
RUN install-required-tools
```

The custom image is not a new operating system. It is the base image adapted for
your workload.

Fine-tuning is similar. You are not teaching a model from scratch. You are
adapting an already-trained model.

## What Fine-Tuning Changes

Fine-tuning can improve:

- Response format consistency
- Domain-specific tone
- Classification boundaries
- Extraction behavior
- Short prompts for repeated tasks
- Following specific schemas
- Handling task-specific edge cases
- Using preferred wording or style

Fine-tuning does not reliably solve:

- Missing private facts that change frequently
- Need for citations from documents
- Runtime access to databases or APIs
- Math correctness without verification
- Tool execution
- Authorization
- Secret handling

For dynamic knowledge, use RAG or tools. For consistent behavior, consider
fine-tuning.

## Why Fine-Tune Instead of Prompt?

Prompt engineering can include examples in the prompt. That works well up to a
point.

Fine-tuning helps when:

- You have many examples that cannot fit in every prompt.
- You need consistent output across thousands of calls.
- You want shorter prompts for latency and cost.
- A smaller model should learn a narrow task.
- The model repeatedly misses the same behavior despite good prompts.

The OpenAI fine-tuning guide frames model optimization as a loop of evals,
prompt engineering, and fine-tuning, rather than fine-tuning as the first step.

Reference: [OpenAI model optimization guide](https://platform.openai.com/docs/guides/fine-tuning)

## Types of Fine-Tuning

Common techniques:

| Method | What You Provide | Best For |
|--------|------------------|----------|
| SFT | Prompt plus ideal answer | Format, style, extraction, classification |
| DPO | Prompt plus preferred and rejected answers | Tone, preference, summary focus |
| RFT | Prompt plus grader/reward signal | Domain reasoning tasks with expert grading |
| Vision fine-tuning | Image inputs plus expected outputs | Image classification and multimodal behavior |
| LoRA/QLoRA | Local adapter training | Efficient local customization |

The OpenAI platform currently documents SFT, vision fine-tuning, DPO, and RFT as
fine-tuning methods. Local open-source workflows often use SFT plus LoRA or
QLoRA.

## Fine-Tuning Workflow

The engineering workflow:

1. Define the task.
2. Build an eval set first.
3. Establish a baseline with the base model.
4. Decide if prompting or RAG is enough.
5. Create high-quality training examples.
6. Validate JSONL format and data safety.
7. Split train/validation/holdout.
8. Train.
9. Evaluate against baseline.
10. Inspect failure cases.
11. Iterate data, not only hyperparameters.
12. Deploy behind a versioned model alias/config.
13. Monitor production behavior.

## Key Takeaways

1. Fine-tuning adapts behavior; it is not a database.
2. Start with evals and prompting before training.
3. Training data quality matters more than dataset size.
4. Use RAG for changing facts and citations.
5. Treat a fine-tuned model as a deployable artifact with versioning and rollback.
