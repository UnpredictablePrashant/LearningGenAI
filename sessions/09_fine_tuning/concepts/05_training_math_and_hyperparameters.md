# 05. Training Math and Hyperparameters

You do not need to implement backpropagation to use fine-tuning, but you should
understand the knobs and failure modes.

## Objective

In supervised fine-tuning, the model sees input tokens and target output tokens.
Training adjusts weights so the target output becomes more likely.

At a high level:

```
prediction = model(prompt)
loss = difference(prediction, target)
weights = update(weights, loss)
```

For language models, loss is commonly token-level cross entropy.

## Cross Entropy Intuition

If the correct next token is `"networking"` and the model assigns it low
probability, loss is high.

If the model assigns high probability to the correct next token, loss is low.

Training minimizes average loss across examples.

## Gradient Descent

Gradient descent updates weights in the direction that reduces loss.

Key idea:

```
new_weights = old_weights - learning_rate * gradient
```

The real implementation is much more complex, but the intuition matters:

- Too small learning rate: training barely changes behavior.
- Too large learning rate: training destabilizes or overfits.

## Epoch

An epoch is one full pass through the training dataset.

If you have 1000 examples and train for 3 epochs, the model sees 3000 example
presentations.

More epochs are not always better. Too many can overfit.

## Batch Size

Batch size is how many examples contribute to one weight update.

Small batches:

- More frequent updates
- Noisier gradients
- Can generalize well but be unstable

Large batches:

- Smoother updates
- Fewer updates per epoch
- Need more memory

Hosted platforms often default to `auto` because good values depend on dataset
and model.

## Learning Rate Multiplier

Learning rate controls update size. Some hosted APIs expose a learning-rate
multiplier rather than raw learning rate.

Lower learning rate can help when:

- Dataset is small
- You want subtle behavior changes
- Overfitting appears

Higher learning rate can help when:

- Dataset is large and consistent
- Base model is far from desired behavior

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

```
effective_training_tokens = total_training_tokens * n_epochs
```

## Key Takeaways

1. SFT minimizes loss on target outputs.
2. Epochs control repeated exposure to the dataset.
3. Batch size controls update granularity.
4. Learning rate controls update magnitude.
5. Overfitting and underfitting are diagnosed with validation and holdout evals.

