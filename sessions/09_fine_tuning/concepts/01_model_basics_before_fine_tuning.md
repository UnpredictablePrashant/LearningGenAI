# 01. Model Basics Before Fine-Tuning

Before fine-tuning, you need a clear mental model of what an LLM is doing during
inference and what training changes. This section starts from the basics:

- weights
- biases
- parameters
- tokens
- logits
- probabilities
- inference
- training
- quantization
- checkpoints
- adapters

## The Smallest Mental Model

A neural network is a large mathematical function:

```text
input tokens -> model -> next-token probabilities
```

For a language model, the main job is:

```text
Given the tokens so far, predict the next token.
```

Example:

```text
Input:  "Kubernetes pods run inside a"
Likely next tokens:
  "cluster"    0.42
  "node"       0.21
  "namespace" 0.08
  ...
```

The model does not store English sentences as rules. It stores numbers. Those
numbers are called parameters.

## What Is a Weight?

A weight is a learned number that controls how strongly one internal signal
affects another.

Simple example:

```python
score = weight * input_value
```

If:

```python
weight = 2.0
input_value = 3.0
```

Then:

```python
score = 6.0
```

The weight decides how much the input matters.

## DevOps Analogy

Think of an alert routing rule:

```text
if service == payments: add 5 priority points
if severity == SEV1: add 10 priority points
if environment == dev: subtract 3 priority points
```

Those point values are like weights. They decide how strongly a signal affects
the final routing decision.

In an LLM, there are billions or trillions of such learned numbers.

## What Is a Bias?

A bias is a learned offset added to a calculation.

Simple example:

```python
score = weight * input_value + bias
```

If:

```python
weight = 2.0
input_value = 3.0
bias = 1.0
```

Then:

```python
score = 7.0
```

The bias shifts the result up or down even when the input is small.

## DevOps Analogy

Imagine an autoscaling policy:

```text
desired_replicas = cpu_pressure * scale_factor + minimum_replicas
```

`minimum_replicas` is like a bias. It keeps the output from starting at zero.

## What Is a Parameter?

Parameter is the general term for learned numbers in the model. Weights and
biases are parameters.

When someone says:

```text
"This model has 7B parameters."
```

They mean the model contains about 7 billion learned numbers.

These numbers are what training changes.

## What Does a Layer Do?

An LLM has many layers. Each layer transforms the representation of the input.

Very simplified:

```text
tokens -> layer 1 -> layer 2 -> layer 3 -> ... -> output probabilities
```

Early layers may learn simple patterns. Later layers combine patterns into more
abstract behavior. In transformer models, attention layers help tokens interact
with other tokens in the context.

## What Is an Activation?

An activation is the intermediate value produced inside the network while it is
running.

Parameters are stored in the model.

Activations are created for a specific request.

Analogy:

- Parameters are like code and config baked into a container image.
- Activations are like runtime memory while the container handles one request.

## Tokens

Models do not read raw text directly. Text is split into tokens.

Example:

```text
"kubectl get pods"
-> ["kub", "ectl", " get", " pods"]  # simplified example
```

The exact tokenization depends on the tokenizer.

Fine-tuning examples are ultimately converted into tokens. Training cost and
context usage are based on tokens, not characters or words.

## Embeddings

Each token is converted into a vector of numbers called an embedding.

```text
token id -> embedding vector
```

This lets the model do math on token meaning and context.

Do not confuse:

- Token embeddings inside an LLM
- Text embeddings used for semantic search in RAG

They are related ideas, but used differently.

## Logits

Before a model chooses the next token, it produces raw scores called logits.

Example:

```text
cluster:    4.2
node:       3.5
namespace: 2.4
banana:   -1.2
```

Logits are not probabilities yet. They are unnormalized scores.

## Softmax

Softmax converts logits into probabilities.

Simplified:

```text
logits -> softmax -> probabilities
```

Example:

```text
cluster:    0.58
node:       0.29
namespace: 0.10
banana:    0.03
```

The model can then choose a token. Temperature and sampling settings affect how
deterministic that choice is.

## What Is Inference?

Inference is using a trained model to produce an output.

```text
prompt -> model weights -> generated answer
```

During inference, the model's weights normally do not change.

DevOps analogy:

```text
Running a container from an image.
```

The image is fixed. Each request creates runtime state, but the image does not
rewrite itself.

## What Is Training?

Training changes the model's parameters.

```text
examples -> loss -> gradients -> weight updates -> new model checkpoint
```

DevOps analogy:

```text
Building a new container image.
```

Training produces a modified artifact. Inference runs that artifact.

## What Is Fine-Tuning?

Fine-tuning is training that starts from an existing pretrained model instead of
starting from random weights.

```text
pretrained base model + task examples -> fine-tuned model
```

The base model already knows general language. Fine-tuning adjusts behavior for
your specific task.

## What Is Loss?

Loss measures how wrong the model was on a training example.

Example:

Target answer:

```json
{"label":"security"}
```

If the model predicts:

```json
{"label":"billing"}
```

Loss is high.

If the model predicts the correct JSON, loss is lower.

Training tries to reduce average loss.

## What Is a Gradient?

A gradient tells the optimizer how to change parameters to reduce loss.

Simple intuition:

```text
This weight made the answer worse. Move it down.
This weight made the answer better. Move it up.
```

The optimizer applies many tiny updates across many examples.

## What Is a Checkpoint?

A checkpoint is a saved model state.

It contains:

- Model architecture reference
- Learned parameters
- Sometimes optimizer state
- Metadata about training

Hosted fine-tuning returns a fine-tuned model ID. Local fine-tuning creates model
checkpoint files or adapter files.

## What Is Quantization?

Quantization stores model numbers with fewer bits.

Common formats:

| Format | Rough Meaning | Use |
|--------|---------------|-----|
| FP32 | 32-bit floating point | Training, high precision |
| FP16 | 16-bit floating point | Faster GPU inference/training |
| BF16 | 16-bit brain float | Stable modern training/inference |
| INT8 | 8-bit integer | Smaller/faster inference |
| 4-bit | Very compact | Local inference and QLoRA-style training |

If a model has billions of parameters, storing each number with fewer bits saves
memory.

Example:

```text
7B parameters * 16 bits ~= 14 GB just for weights
7B parameters * 4 bits  ~= 3.5 GB just for weights
```

Real memory use includes overhead, activations, KV cache, runtime, and optimizer
state.

## Why Quantization Matters

Quantization helps run larger models on smaller hardware.

Tradeoffs:

- Lower memory use
- Faster inference in some setups
- Possible quality loss
- More compatibility constraints

For fine-tuning, quantization is important in QLoRA. QLoRA keeps the base model
quantized and trains small adapter weights.

## What Is an Adapter?

An adapter is a small set of trainable parameters added to a frozen base model.

LoRA is a popular adapter method.

Instead of updating all model weights:

```text
base model weights: frozen
adapter weights: trained
```

Benefits:

- Much smaller training artifact
- Lower GPU memory requirements
- Easier to swap task-specific adapters

## Base Model vs Fine-Tuned Model

Base model:

```text
General-purpose behavior
```

Fine-tuned model:

```text
Base model plus training updates for a specific task
```

Adapter-tuned model:

```text
Base model plus separate adapter weights
```

## Inference vs Training Summary

| Concept | Inference | Training/Fine-Tuning |
|---------|-----------|----------------------|
| Purpose | Generate outputs | Improve future outputs |
| Weights change? | No | Yes, or adapter weights change |
| Uses examples? | Prompt/context | Training dataset |
| Produces | Answer | New model or adapter |
| Main risk | Bad answer | Bad model behavior learned |
| DevOps analogy | Run container | Build image |

## Why This Matters for Fine-Tuning

Fine-tuning is not editing a prompt. It changes learned behavior.

That means:

- Bad examples can become bad model behavior.
- Repeated style patterns can become defaults.
- Missing refusal examples can weaken safety.
- Duplicated examples can cause memorization.
- Too many epochs can overfit.
- Quantization can make local training feasible but may affect quality.

## Key Takeaways

1. Weights and biases are learned numbers.
2. Parameters are the model's learned state.
3. Inference uses weights; training changes weights.
4. Loss measures wrongness; gradients guide updates.
5. Quantization stores numbers with fewer bits to reduce memory.
6. Fine-tuning starts from a base model and adapts it with examples.
7. LoRA/QLoRA often train adapters instead of all parameters.

