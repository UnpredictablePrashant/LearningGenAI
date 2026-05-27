# 06. Training Math and Hyperparameters

You do not need to implement backpropagation to use fine-tuning, but you should
understand the knobs and failure modes. Hyperparameters are the training settings
that control how strongly and how often the model learns from your examples.

## Objective

In supervised fine-tuning, the model sees input tokens and target output tokens.
Training adjusts weights so the target output becomes more likely.

At a high level:

```text
prediction = model(prompt)
loss = difference(prediction, target)
weights = update(weights, loss)
```

For language models, loss is commonly token-level cross entropy.

## Cross Entropy Intuition

If the correct next token is `"networking"` and the model assigns it low
probability, loss is high.

If the model assigns high probability to the correct next token, loss is low.

Very simplified:

```text
loss = -log(probability assigned to the correct token)
```

Examples:

```text
correct token probability = 0.90 -> loss ~= 0.11
correct token probability = 0.50 -> loss ~= 0.69
correct token probability = 0.10 -> loss ~= 2.30
```

So training rewards the model for putting more probability on the correct target
tokens.

## Analogy: Turning Many Tiny Dials

Imagine a sound mixing board with billions of tiny dials. A song plays, you
compare it with the desired sound, and the training process nudges many dials a
little. One update is tiny. Many updates across many examples can change the
overall sound.

Model parameters are those dials. Fine-tuning nudges them, or in LoRA it nudges
adapter dials attached to the original board.

## Gradient Descent

Gradient descent updates weights in the direction that reduces loss.

Key idea:

```text
new_weight = old_weight - learning_rate * gradient
```

The real implementation is much more complex, but the intuition matters:

- Too small learning rate: training barely changes behavior.
- Too large learning rate: training destabilizes or overfits.

## Epoch

An epoch is one full pass through the training dataset.

If you have 1000 examples and train for 3 epochs, the model sees 3000 example
presentations.

```text
example_presentations = number_of_examples * epochs
```

More epochs are not always better. Too many can overfit.

## Batch Size

Batch size is how many examples contribute to one weight update.

Small batches:

- More frequent updates
- Noisier gradients
- Can generalize well but be unstable
- Use less memory per step

Large batches:

- Smoother updates
- Fewer updates per epoch
- Need more memory

Number of update steps is roughly:

```text
steps_per_epoch = ceil(training_examples / batch_size)
total_steps = steps_per_epoch * epochs
```

Example:

```text
training_examples = 800
batch_size = 8
epochs = 3

steps_per_epoch = 100
total_steps = 300
```

Hosted platforms often default to `auto` because good values depend on dataset,
model, and infrastructure.

## Gradient Accumulation

Local training often uses gradient accumulation to simulate a larger batch size
without needing all examples in GPU memory at once.

```text
effective_batch_size =
  per_device_batch_size * gradient_accumulation_steps * number_of_gpus
```

Example:

```text
per_device_batch_size = 2
gradient_accumulation_steps = 8
number_of_gpus = 1

effective_batch_size = 16
```

The GPU processes two examples at a time, accumulates gradients for eight mini
steps, and then applies one update.

## Learning Rate Multiplier

Learning rate controls update size. Some hosted APIs expose a learning-rate
multiplier rather than raw learning rate.

Lower learning rate can help when:

- Dataset is small
- You want subtle behavior changes
- Overfitting appears
- The base model is already close to desired behavior

Higher learning rate can help when:

- Dataset is large and consistent
- Base model is far from desired behavior
- Underfitting remains after a clean first run

For beginner projects, use `auto` first when the hosted provider supports it.
Tune only after looking at eval results.

## Warmup and Scheduling

Some local trainers use warmup steps and learning-rate schedules.

Warmup means:

```text
start with a small learning rate -> gradually increase -> train normally
```

This avoids shocking the model at the beginning of training. You do not need to
master schedules immediately, but you should recognize them in local training
configs.

## Overfitting

Overfitting means the model memorizes training examples instead of learning the
general pattern.

Symptoms:

- Training loss improves, validation loss worsens.
- Model repeats training phrasing too literally.
- Holdout examples fail.
- Outputs become less robust to wording changes.

Controls:

- Better data diversity
- Fewer epochs
- Lower learning rate
- More validation examples
- Deduplication
- Earlier checkpoint selection

Analogy: a student memorizes the exact practice questions but fails when the
numbers change.

## Underfitting

Underfitting means training did not move behavior enough.

Symptoms:

- Training and validation both poor.
- Model still ignores target format.
- Same baseline failures remain.

Controls:

- More examples
- Better examples
- More epochs
- Higher learning-rate multiplier
- More capable base model

Analogy: a student attended the class but did not practice enough to change
their habits.

## Token Budget

Training cost and runtime scale with tokens, not just number of examples.

Track:

- Prompt tokens
- Completion tokens
- Total tokens per example
- Maximum example length
- Total training tokens
- Epoch-adjusted tokens

Simple estimate:

```text
effective_training_tokens = total_training_tokens * n_epochs
```

Example:

```text
average tokens per example = 300
training examples = 1000
epochs = 3

total_training_tokens = 300,000
effective_training_tokens = 900,000
```

This is not the full cost model for every provider, but it is the right first
estimate.

## Tiny Estimator

```python
import math

def training_plan(example_count: int, avg_tokens: int, epochs: int, batch_size: int) -> dict:
    total_tokens = example_count * avg_tokens
    steps_per_epoch = math.ceil(example_count / batch_size)
    return {
        "total_tokens": total_tokens,
        "effective_training_tokens": total_tokens * epochs,
        "steps_per_epoch": steps_per_epoch,
        "total_steps": steps_per_epoch * epochs,
    }

print(training_plan(example_count=1000, avg_tokens=300, epochs=3, batch_size=8))
```

## Key Takeaways

1. SFT minimizes loss on target output tokens.
2. Epochs control repeated exposure to the dataset.
3. Batch size controls update granularity and memory use.
4. Learning rate controls update magnitude.
5. Gradient accumulation helps local training with limited GPU memory.
6. Overfitting and underfitting are diagnosed with validation and holdout evals.
