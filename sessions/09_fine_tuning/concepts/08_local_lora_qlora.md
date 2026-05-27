# 08. Local Fine-Tuning, LoRA, and QLoRA

Hosted fine-tuning is not the only path. Open-source workflows let you fine-tune
local models using libraries such as Hugging Face Transformers, TRL, PEFT, and
bitsandbytes.

This session does not require GPU training, but you should understand the local
workflow because the concepts transfer directly to real projects.

References:

- [Hugging Face TRL SFTTrainer docs](https://huggingface.co/docs/trl/sft_trainer)
- [Hugging Face PEFT LoRA docs](https://huggingface.co/docs/peft/main/en/developer_guides/lora)
- [Hugging Face bitsandbytes quantization docs](https://huggingface.co/docs/transformers/quantization/bitsandbytes)

## Full Fine-Tuning

Full fine-tuning updates all model weights.

Pros:

- Maximum flexibility
- Can adapt deeply
- Produces one self-contained model checkpoint

Cons:

- Expensive
- Requires significant GPU memory
- Produces a large checkpoint
- Higher risk of catastrophic forgetting

Catastrophic forgetting means the model becomes better at your narrow examples
but worse at general behavior it previously handled well.

## Parameter-Efficient Fine-Tuning

Parameter-efficient fine-tuning updates a smaller number of trainable
parameters. The base model stays mostly frozen.

LoRA is a common method. Instead of updating every weight matrix directly, LoRA
adds small trainable matrices.

Simplified math:

```text
original output = W x
LoRA output     = W x + (B A) x
```

Where:

- `W` is the frozen original weight matrix.
- `A` and `B` are small trainable adapter matrices.
- `B A` is low-rank, meaning it is much smaller than `W`.

Analogy: instead of rebuilding the whole engine, you add a small tuning module
that changes how the engine behaves for your task.

## LoRA Rank

The LoRA rank, often written as `r`, controls adapter size.

```text
higher rank -> more trainable capacity -> more memory and overfitting risk
lower rank  -> smaller adapter -> less capacity
```

Common beginner values:

```text
r = 8, 16, or 32
```

Start small. Increase rank only if the model underfits and the dataset is good.

## QLoRA

QLoRA combines quantization with LoRA-style adapter training. The base model is
loaded in a compact 4-bit form to reduce memory, while adapters are trained in a
higher precision.

Use QLoRA when:

- You have limited GPU memory.
- You want to fine-tune a larger local model.
- You can tolerate extra environment complexity.

QLoRA mental model:

```text
large base model stored compactly + small trainable adapters = practical local training
```

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

Rough beginner guidance:

| Hardware | Practical Path |
|----------|----------------|
| CPU only | Learn the workflow, but real training will be painfully slow |
| 6-8 GB GPU | Tiny models only; try 0.5B-1B with QLoRA |
| 12-16 GB GPU | 1B-3B models with QLoRA, careful batch sizes |
| 24 GB GPU | 3B-7B models with QLoRA, sometimes LoRA |
| 48 GB+ GPU | Larger models, longer context, or more comfortable LoRA |
| Multi-GPU | Larger models and faster experiments, but more setup complexity |

These are rough rules, not guarantees. Sequence length and batch size can change
memory use dramatically.

## If You Hit Out-of-Memory

Try:

- Reduce `max_length`.
- Reduce `per_device_train_batch_size`.
- Increase `gradient_accumulation_steps`.
- Use QLoRA instead of LoRA.
- Use a smaller base model.
- Lower LoRA rank.
- Disable unnecessary logging/eval during quick tests.

## Local Environment

For CUDA GPU training, Linux is usually smoother than native Windows. Windows
users often use WSL2 or a cloud GPU instance.

Typical packages:

```bash
pip install -U transformers datasets accelerate peft trl bitsandbytes
```

If `bitsandbytes` cannot see your GPU, check:

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

## Downloading a Model

Hugging Face models download automatically the first time you load them:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
)
```

For gated models, authenticate first:

```bash
huggingface-cli login
```

Always check the model license before using it in a project.

## TRL SFTTrainer

Hugging Face TRL provides `SFTTrainer` for supervised fine-tuning workflows. It
supports common dataset formats, including conversational and text datasets.

Conceptual LoRA training shape:

```python
from datasets import load_dataset
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

dataset = load_dataset("json", data_files={
    "train": "data/train_text.jsonl",
    "validation": "data/validation_text.jsonl",
})

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules="all-linear",
    task_type="CAUSAL_LM",
)

training_args = SFTConfig(
    output_dir="outputs/number-tutor-lora",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    max_length=512,
    logging_steps=10,
    save_strategy="epoch",
    eval_strategy="epoch",
)

trainer = SFTTrainer(
    model=model_name,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    peft_config=lora_config,
)

trainer.train()
trainer.save_model("outputs/number-tutor-lora/final")
```

Exact APIs change by version. Pin versions in serious projects and check the
current TRL docs.

## QLoRA Model Loading

QLoRA loads the base model in 4-bit:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quant_config,
    device_map="auto",
)
```

Then pass `model` into `SFTTrainer` with a LoRA config. The adapters train while
the compact base model stays frozen.

## Local Data Format

Local frameworks support multiple formats:

- `text` column containing fully formatted prompts
- Chat message lists
- Prompt/completion pairs
- Instruction/input/output records

Pick one format and write a formatting function. Do not mix formats without a
clear data loader.

Example text row:

```json
{"text":"### User:\nTell me about number 8.\n\n### Assistant:\nNumber: 8\nParity: Even\nDouble: 16\nSquare: 64"}
```

## What You Save

With LoRA/QLoRA, the output is often adapter weights, not a full model:

```text
base model: Qwen/Qwen2.5-0.5B-Instruct
adapter: outputs/number-tutor-lora/final
```

For inference, you load the base model plus adapter. You can also merge adapters
into a full model in some workflows, but keeping adapters separate is convenient
for experiments.

## Key Takeaways

1. Full fine-tuning updates all weights; LoRA trains lightweight adapters.
2. QLoRA reduces memory by quantizing the base model.
3. LoRA rank controls adapter capacity.
4. TRL SFTTrainer is a common local SFT workflow.
5. Pin library versions and check current docs before real training.
6. Evaluate local fine-tunes with the same rigor as hosted fine-tunes.
