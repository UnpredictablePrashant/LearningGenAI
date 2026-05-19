# 08. Local Fine-Tuning, LoRA, and QLoRA

Hosted fine-tuning is not the only path. Open-source workflows let you fine-tune
local models using libraries such as Hugging Face Transformers, TRL, and PEFT.

This session does not require GPU training, but you should understand the local
workflow.

## Full Fine-Tuning

Full fine-tuning updates all model weights.

Pros:

- Maximum flexibility
- Can adapt deeply

Cons:

- Expensive
- Requires significant GPU memory
- Produces a full model checkpoint
- Higher risk of catastrophic forgetting

## Parameter-Efficient Fine-Tuning

Parameter-efficient fine-tuning updates a smaller number of trainable parameters.

LoRA is a common method. Instead of updating every weight matrix directly, LoRA
adds low-rank adapter matrices and trains those.

Hugging Face PEFT documents LoRA as a parameter-efficient approach that can be
configured and wrapped around supported models.

Reference: [Hugging Face PEFT LoRA docs](https://huggingface.co/docs/peft/main/en/developer_guides/lora)

## QLoRA

QLoRA combines quantization with LoRA-style adapter training. The base model is
loaded in a quantized form to reduce memory, while adapters are trained.

Use QLoRA when:

- You have limited GPU memory.
- You want to fine-tune a larger local model.
- You can tolerate extra complexity.

## TRL SFTTrainer

Hugging Face TRL provides `SFTTrainer` for supervised fine-tuning workflows.

Reference: [Hugging Face TRL SFTTrainer docs](https://huggingface.co/docs/trl/main/en/sft_trainer)

Conceptual shape:

```python
from trl import SFTConfig, SFTTrainer

config = SFTConfig(
    output_dir="outputs/ticket-router",
    num_train_epochs=3,
    per_device_train_batch_size=2,
)

trainer = SFTTrainer(
    model=model,
    args=config,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    peft_config=lora_config,
)

trainer.train()
```

Exact APIs change by version. Use current library docs.

## Local Data Format

Local frameworks support multiple formats:

- `text` column containing fully formatted prompts
- Chat message lists
- Prompt/completion pairs
- Instruction/input/output records

Pick one format and write a formatting function. Do not mix formats without a
clear data loader.

## Hardware Planning

Local fine-tuning depends on:

- Model size
- Sequence length
- Batch size
- Precision
- Quantization
- Optimizer
- LoRA rank
- GPU memory

If a run fails with out-of-memory:

- Reduce sequence length.
- Reduce batch size.
- Use gradient accumulation.
- Use LoRA/QLoRA.
- Use a smaller base model.

## Key Takeaways

1. Full fine-tuning updates all weights; LoRA trains lightweight adapters.
2. QLoRA reduces memory by quantizing the base model.
3. TRL SFTTrainer is a common local SFT workflow.
4. Local APIs change quickly, so pin versions.
5. Evaluate local fine-tunes with the same rigor as hosted fine-tunes.
