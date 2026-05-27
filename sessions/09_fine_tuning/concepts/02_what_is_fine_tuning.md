# 02. What Is Fine-Tuning?

Fine-tuning adapts a pretrained model so it behaves better for a specific task,
style, domain, or output contract. Instead of teaching a model language from
zero, you start from a model that already understands language and then show it
many examples of the behavior you want.

Simple mental model:

```text
base model + high-quality examples -> model behavior moves toward those examples
```

The important word is behavior. Fine-tuning is usually not the best way to add
fresh facts. It is a way to make the model answer in a more reliable pattern.

## Why Fine-Tuning Exists

Large models are trained on broad data. That gives them general ability, but your
application may need a narrow habit:

- Always return strict JSON.
- Classify support tickets using your labels.
- Write answers in your company's support tone.
- Extract only the fields your downstream system expects.
- Refuse specific unsafe requests in a consistent way.

You can put examples in a prompt, but prompts have limits. They increase token
cost, can be ignored, and become awkward when you need dozens or hundreds of
examples. Fine-tuning moves some of that repeated behavior into the model itself.

## Analogy: Training a New Support Agent

Imagine hiring a smart support engineer. They already know English and basic
technology. You do not teach them what a sentence is. You show them:

- Your ticket categories
- Good examples of routed tickets
- Bad examples and why they are wrong
- The exact JSON format your internal tool accepts
- Edge cases where the correct answer is `unknown`

After seeing enough reviewed examples, they develop a habit. Fine-tuning does a
similar thing for a model.

## DevOps Analogy

A base model is like a golden container image:

```text
ubuntu:latest
```

It is general-purpose. Fine-tuning is like building a custom image:

```dockerfile
FROM ubuntu
COPY company-runner-config /etc/runner
RUN install-required-tools
```

The custom image is not a new operating system. It is the base image adapted for
your workload.

Fine-tuning is similar. You are not creating intelligence from scratch. You are
adapting an already trained artifact.

## What Actually Changes?

During fine-tuning, the training system compares the model's output with the
target output in your dataset. When the target output is more correct, the
training process adjusts model parameters, or adapter parameters, so similar
outputs become more likely next time.

High-level loop:

```text
example prompt -> model output -> compare with target -> compute loss -> update weights/adapters
```

For hosted fine-tuning, the provider manages the infrastructure and returns a
fine-tuned model ID. For LoRA or QLoRA, you usually train adapter files locally
or on a cloud GPU.

## What Fine-Tuning Can Improve

Fine-tuning can improve:

- Response format consistency
- Domain-specific tone
- Classification boundaries
- Extraction behavior
- Short prompts for repeated tasks
- Following specific schemas
- Handling task-specific edge cases
- Using preferred wording or style
- Reducing repeated instruction-following mistakes

Example: if the base model often returns:

```text
This looks like a billing issue.
```

but production needs:

```json
{"label":"billing","confidence":0.88,"rationale":"The ticket mentions unexpected cost."}
```

fine-tuning can teach the model that the JSON shape is the expected answer.

## What Fine-Tuning Does Not Reliably Solve

Fine-tuning does not reliably solve:

- Missing private facts that change frequently
- Need for citations from documents
- Runtime access to databases or APIs
- Exact arithmetic without verification
- Tool execution
- Authorization
- Secret handling
- "Never hallucinate" as a general guarantee

For dynamic knowledge, use RAG. For live actions, use tools. For permissions,
use deterministic authorization checks. Fine-tuning can support these systems,
but it should not replace them.

## Fine-Tuning vs Prompting

Prompt engineering says:

```text
Here are instructions and examples. Follow them now.
```

Fine-tuning says:

```text
Here are many examples. Adjust future behavior to match them.
```

Prompting is faster to try. Fine-tuning is slower but can be better when the
same behavior must repeat across many requests.

Use prompting first when:

- The task is new or still changing.
- You have only a few examples.
- The expected output is not stable.
- You do not have evals yet.

Use fine-tuning when:

- The task is stable.
- You have enough high-quality examples.
- Prompt examples are too long or still unreliable.
- You can measure improvement with evals.

The OpenAI model optimization guidance frames fine-tuning as part of an
iteration loop with evals and prompting, not as the first move for every problem.

Reference: [OpenAI model optimization guide](https://platform.openai.com/docs/guides/fine-tuning)

## Types of Fine-Tuning

Common techniques:

| Method | What You Provide | Best For |
|--------|------------------|----------|
| SFT | Prompt plus ideal answer | Format, style, extraction, classification |
| DPO | Prompt plus preferred and rejected answers | Tone, preference, summary focus |
| RFT | Prompt plus grader/reward signal | Domain reasoning tasks with expert grading |
| Vision fine-tuning | Image inputs plus expected outputs | Image classification and multimodal behavior |
| LoRA | Local adapter training on an open model | Efficient customization without full retraining |
| QLoRA | Quantized base model plus LoRA adapters | Lower-memory local fine-tuning |

The OpenAI platform documents supervised fine-tuning, vision fine-tuning, direct
preference optimization, and reinforcement fine-tuning. Local open-source
workflows commonly use supervised fine-tuning with LoRA or QLoRA.

## A Tiny Example

Suppose the task is:

```text
Input: Tell me about number 7.
Output:
Number: 7
Parity: Odd
Double: 14
Square: 49
```

A base model may know the math, but it may not use this exact format every time.
Fine-tuning shows the model many examples:

```text
Tell me about number 1. -> exact template
Tell me about number 2. -> exact template
Tell me about number 3. -> exact template
...
```

The goal is not to teach the model that `7 * 7 = 49` from scratch. The goal is
to teach the format and behavior pattern.

## Fine-Tuning Workflow

The engineering workflow:

1. Define the task.
2. Build an eval set first.
3. Establish a baseline with the base model.
4. Decide if prompting or RAG is enough.
5. Create high-quality training examples.
6. Validate JSONL format and data safety.
7. Split train, validation, and holdout test data.
8. Train.
9. Evaluate against the baseline.
10. Inspect failure cases.
11. Improve the data and repeat only if needed.
12. Deploy behind a versioned model config.
13. Monitor production behavior.

## Key Takeaways

1. Fine-tuning adapts behavior; it is not a database.
2. Start with evals and prompting before training.
3. Training data quality matters more than dataset size.
4. Use RAG for changing facts and citations.
5. Treat a fine-tuned model as a deployable artifact with versioning and rollback.
