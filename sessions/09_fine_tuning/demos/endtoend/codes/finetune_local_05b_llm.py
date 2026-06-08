#!/usr/bin/env python3
"""
End-to-End Local 0.5B LLM Fine-Tuning with Optional Local Runtime Export
=======================================================================

Objective
---------
This script fine-tunes a downloaded local chat language model on a hypothetical
machine-maintenance instruction dataset.

This is different from a small classifier fine-tune:

    - The base model is a causal/chat LLM from Hugging Face.
    - The training target is a full assistant response, not just a class id.
    - The model learns to answer machine-maintenance prompts in a specific JSON
      style.
    - The training method is QLoRA by default: the base model is loaded in
      4-bit precision and small LoRA adapter weights are trained.
    - The output is a LoRA adapter that can be used with the same base model.
    - The script also writes optional Ollama/llama.cpp-oriented helper files so
      the fine-tuned result can be packaged for a local runtime after training.

Default base model
------------------
The default is:

    Qwen/Qwen2.5-0.5B-Instruct

It is a real instruction-tuned causal language model with about 0.5B parameters.
That keeps the model inside the requested 0.5B-1B teaching range while still
showing the mechanics of downloading, adapting, evaluating, and saving a local
LLM.

Target EC2 machine and objective
--------------------------------
This example is tuned for the machine you plan to use:

    - EC2 instance: g6.xlarge
    - GPU: 1 NVIDIA L4 GPU with 24 GB VRAM
    - System memory: 16 GiB
    - Storage target: 100 GB EBS volume
    - Teaching objective: a visible local fine-tuning run that completes in
      roughly 1-2 hours

The default profile uses QLoRA, a 4,800-row instruction dataset, 8 epochs, LoRA
rank 32, batch size 1, gradient accumulation 8, and sequence length 1,536. That
is intentionally more work than a quick smoke test, so the workshop can honestly
show that the model spent time adapting to the machine-maintenance task.

What the dataset teaches the model
----------------------------------
Each row describes a fictional industrial machine with telemetry:

    - temperature
    - vibration
    - pressure
    - rpm
    - noise
    - oil quality
    - hours since service
    - error code
    - technician note

The assistant must return strict JSON like:

    {
      "recommended_action": "replace_filter",
      "severity": "medium",
      "confidence": 0.86,
      "root_cause_hypothesis": "Restricted intake filter flow is likely...",
      "immediate_steps": ["Reduce feed rate...", "Inspect filter housing..."],
      "maintenance_plan": "Replace the intake filter...",
      "safety_note": "Do not bypass the filter interlock."
    }

This makes it clear to students that the model is being trained to produce a
specific operational behavior from repeated examples.

Expected runtime on EC2 GPU
---------------------------
The default settings are designed as a classroom-length fine-tuning run.
Actual time depends on instance type, CUDA/PyTorch versions, disk speed, and
whether the base model is already downloaded.

Target EC2 instance:

    - g6.xlarge:
        1 NVIDIA L4 GPU with 24 GB VRAM. This is the target machine for the
        default profile. A 100 GB EBS volume is enough for the dataset, model
        download cache, adapter checkpoints, generated reports, and optional
        runtime files.

Also suitable:

    - g5.xlarge or g5.2xlarge:
        1 NVIDIA A10G GPU with 24 GB VRAM. Good default choice.

    - g6.2xlarge / g5.4xlarge / g6.4xlarge:
        Same single-GPU memory, more CPU/RAM. Useful if preprocessing or disk
        work is slow.

Expected wall-clock time using the default model and default settings:

    - First run including model download: roughly 60-120 minutes on a 24 GB GPU.
    - Later runs after the model is cached: often closer to 45-90 minutes.
    - CPU-only: not recommended; it can take many hours.

Disk requirement:

    - 15-30 GB free disk is comfortable for the default 0.5B model.
    - More is needed if you save a merged model or try a larger 1B-3B model.

GPU memory requirement:

    - Default QLoRA mode with Qwen2.5 0.5B: 8-16 GB VRAM is usually enough.
    - The g6.xlarge 24 GB L4 GPU is recommended for a smooth 1-2 hour classroom run.
    - QLoRA mode with 1B-3B models: 8-16 GB VRAM can work.
    - QLoRA mode with 7B models: 24 GB VRAM recommended, but expect longer runs.

Why LoRA instead of full fine-tuning
------------------------------------
Full fine-tuning updates all model weights and is expensive. LoRA trains small
adapter matrices while keeping the base model frozen. That is the common
teaching-friendly path for local LLM fine-tuning.

Local runtime note
------------------
The local runtime does not train the model in this script. Training happens with
PyTorch, Transformers, and PEFT. After training, the script writes optional
Ollama-oriented helper files that point to:

    - the same base model snapshot
    - the trained LoRA adapter

Adapters must be used with the same base model they were trained from. This
script saves the base snapshot path beside the adapter to make that relationship
visible.

Install on an EC2 GPU machine
-----------------------------
Recommended Ubuntu setup after installing the NVIDIA driver and CUDA-compatible
PyTorch:

    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
    pip install transformers datasets accelerate peft trl bitsandbytes pandas scikit-learn hf_xet

Run the full 1-2 hour EC2 GPU example:

    python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py

Run a shorter smoke test:

    python sessions/09_fine_tuning/demos/endtoend/codes/finetune_local_05b_llm.py --profile smoke --max-steps 20

Optional local runtime import after training
--------------------------------------------
After training finishes, read the generated command file:

    sessions/09_fine_tuning/demos/endtoend/output/local_05b_machine_assistant/ollama/ollama_commands.txt

The important commands will look like:

    cd sessions/09_fine_tuning/demos/endtoend/output/local_05b_machine_assistant/ollama
    ollama create plantops-maintenance-ai -f Modelfile.adapter
    ollama run plantops-maintenance-ai

Expected output files and what they mean
----------------------------------------
The provided training dataset lives under:

    sessions/09_fine_tuning/demos/endtoend/datasets/

The script writes model artifacts and run outputs under:

    sessions/09_fine_tuning/demos/endtoend/output/

Markdown documents and prompt handouts live under:

    sessions/09_fine_tuning/demos/endtoend/docs/

Files and directories:

    datasets/machine_maintenance_ollama_instruction_dataset.csv
        The provided 4,800-row hypothetical instruction dataset.

    output/hf_cache/
        Hugging Face model cache for this demo, kept inside the end-to-end
        output folder instead of the user's home directory by default.

    docs/sample_prompts.md
        The fixed prompts to run before and after fine-tuning. Use these in
        class to show that the same prompt produces better task-specific JSON
        after training.

    docs/latest_run_summary.md
        The latest human-readable run summary written after training.

    adapter/
        The trained LoRA adapter. This is the main fine-tuning artifact. It is
        much smaller than the full base model because it contains only the
        learned adapter weights.

    base_model_snapshot/
        A local copy/snapshot of the base Hugging Face model used for training.
        Any local runtime should use the same base with the adapter.

    training_splits/train.jsonl
    training_splits/validation.jsonl
    training_splits/test.jsonl
        Chat-formatted examples used by the training run. These are useful for
        auditing exactly what text the model saw.

    metrics/train_metrics.json
        Training loss, runtime, and throughput reported by Transformers.

    metrics/eval_metrics.json
        Validation loss after training.

    metrics/test_action_accuracy.json
        A small generation-based test. The script asks the fine-tuned model to
        answer held-out examples and checks whether the generated JSON contains
        the expected recommended_action.

    prompt_checks/base_model_generations.jsonl
        The downloaded base model's answers before fine-tuning.

    prompt_checks/fine_tuned_generations.jsonl
        The fine-tuned adapter model's answers after training.

    prompt_checks/before_after_comparison.json
        A compact comparison of expected action, base-model action, fine-tuned
        action, and whether each answer matched the expected action.

    test_generations.jsonl
        Side-by-side generated outputs for held-out examples. This is useful
        for classroom inspection because students can see what the model says.

    ollama/Modelfile.adapter
        Ollama recipe that uses the local base model plus the LoRA adapter.

    ollama/Modelfile.merged
        Written only if --merge-adapter is used. It points Ollama at a merged
        full-model directory.

    ollama/ollama_commands.txt
        Copy-ready commands for creating and running the Ollama model.

Important teaching caveat
-------------------------
This is still a toy machine dataset. It is excellent for showing the mechanics
of fine-tuning and local deployment, but it should not be used to operate real
industrial equipment.
"""

from __future__ import annotations

import argparse
import inspect
import json
import math
import os
import re
import shutil
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ENDTOEND_DIR = SCRIPT_DIR.parent
DEFAULT_DOCS_DIR = ENDTOEND_DIR / "docs"
DEFAULT_DATASET_PATH = ENDTOEND_DIR / "datasets" / "machine_maintenance_ollama_instruction_dataset.csv"
DEFAULT_OUTPUT_DIR = ENDTOEND_DIR / "output" / "local_05b_machine_assistant"
DEFAULT_CACHE_DIR = ENDTOEND_DIR / "output" / "hf_cache"
DEFAULT_BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
DEFAULT_OLLAMA_MODEL_NAME = "plantops-maintenance-ai"
TOTAL_RUN_STEPS = 16

os.environ.setdefault("HF_HOME", str(DEFAULT_CACHE_DIR))
os.environ.setdefault("HF_HUB_CACHE", str(DEFAULT_CACHE_DIR / "hub"))
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


SYSTEM_PROMPT = (
    "You are PlantOps-MaintenanceAI, a cautious maintenance assistant for "
    "industrial machines. Return strict JSON only. The JSON must contain "
    "recommended_action, severity, confidence, root_cause_hypothesis, "
    "immediate_steps, maintenance_plan, and safety_note."
)


ACTION_LABELS = [
    "normal_operation",
    "schedule_inspection",
    "reduce_load",
    "replace_filter",
    "lubricate_bearings",
    "emergency_shutdown",
]


def print_step(step: int, total: int, title: str, detail: str | None = None) -> None:
    """Print a visible step header for long EC2 console runs."""

    line = f"[Step {step:02d}/{total:02d}] {title}"
    print("\n" + "=" * len(line))
    print(line)
    print("=" * len(line))
    if detail:
        print(detail)


def build_user_prompt(row: dict[str, Any]) -> str:
    """
    Build the user message for instruction tuning.

    This is the prompt the fine-tuned LLM will learn to answer. It intentionally
    reads like a real operator/maintenance request.
    """

    return (
        "Analyze this machine telemetry report and return the maintenance "
        "decision as strict JSON.\n\n"
        f"Machine: {row['machine_id']}\n"
        f"Machine type: {row['machine_type']}\n"
        f"Plant area: {row['plant_area']}\n"
        f"Shift: {row['shift']}\n"
        f"Temperature C: {row['temperature_c']}\n"
        f"Vibration mm/s: {row['vibration_mm_s']}\n"
        f"Pressure bar: {row['pressure_bar']}\n"
        f"RPM: {row['rpm']}\n"
        f"Noise dB: {row['noise_db']}\n"
        f"Oil quality percent: {row['oil_quality_pct']}\n"
        f"Hours since service: {row['hours_since_service']}\n"
        f"Error code: {row['error_code']}\n"
        f"Technician note: {row['technician_note']}\n"
        f"Sensor summary: {row['sensor_summary']}"
    )


def sample_prompt_rows() -> list[dict[str, Any]]:
    """
    Return fixed prompts for before/after fine-tuning checks.

    These examples are deliberately not pulled from the training CSV. They are
    small, stable teaching probes that make it easy to compare the downloaded
    base model with the fine-tuned adapter model.
    """

    rows = [
        {
            "example_id": "prompt-check-001",
            "machine_id": "CNC-9001",
            "machine_type": "CNC mill",
            "plant_area": "fabrication",
            "shift": "night",
            "temperature_c": 118.2,
            "vibration_mm_s": 10.9,
            "pressure_bar": 12.1,
            "rpm": 2210,
            "noise_db": 107.4,
            "oil_quality_pct": 12.0,
            "hours_since_service": 730,
            "error_code": "CRIT-900",
            "technician_note": "critical alarm is active and visible shaking was reported",
            "sensor_summary": "severe multi-sensor alarm",
            "recommended_action": "emergency_shutdown",
        },
        {
            "example_id": "prompt-check-002",
            "machine_id": "PMP-8102",
            "machine_type": "industrial pump",
            "plant_area": "utilities",
            "shift": "morning",
            "temperature_c": 70.4,
            "vibration_mm_s": 2.0,
            "pressure_bar": 3.1,
            "rpm": 1320,
            "noise_db": 69.2,
            "oil_quality_pct": 61.0,
            "hours_since_service": 410,
            "error_code": "FILTER-401",
            "technician_note": "inlet pressure is low and flow is restricted",
            "sensor_summary": "clogged filter pattern",
            "recommended_action": "replace_filter",
        },
        {
            "example_id": "prompt-check-003",
            "machine_id": "CNV-7203",
            "machine_type": "conveyor drive",
            "plant_area": "line 2",
            "shift": "afternoon",
            "temperature_c": 84.8,
            "vibration_mm_s": 7.2,
            "pressure_bar": 6.2,
            "rpm": 1440,
            "noise_db": 91.3,
            "oil_quality_pct": 27.0,
            "hours_since_service": 560,
            "error_code": "LUBE-510",
            "technician_note": "operator reports a dry squeal during startup and shutdown",
            "sensor_summary": "dry bearing signature",
            "recommended_action": "lubricate_bearings",
        },
        {
            "example_id": "prompt-check-004",
            "machine_id": "PKG-6304",
            "machine_type": "packaging line",
            "plant_area": "line 1",
            "shift": "night",
            "temperature_c": 91.5,
            "vibration_mm_s": 4.6,
            "pressure_bar": 8.7,
            "rpm": 1780,
            "noise_db": 81.0,
            "oil_quality_pct": 55.0,
            "hours_since_service": 250,
            "error_code": "LOAD-330",
            "technician_note": "machine recovers when the feed rate is lowered",
            "sensor_summary": "temperature rising under load",
            "recommended_action": "reduce_load",
        },
        {
            "example_id": "prompt-check-005",
            "machine_id": "MLD-5405",
            "machine_type": "injection molder",
            "plant_area": "quality lab",
            "shift": "morning",
            "temperature_c": 76.1,
            "vibration_mm_s": 3.4,
            "pressure_bar": 6.3,
            "rpm": 1260,
            "noise_db": 72.5,
            "oil_quality_pct": 58.0,
            "hours_since_service": 310,
            "error_code": "DRIFT-305",
            "technician_note": "minor drift was noticed across two shifts but production is continuing",
            "sensor_summary": "early warning trend",
            "recommended_action": "schedule_inspection",
        },
        {
            "example_id": "prompt-check-006",
            "machine_id": "CMP-4506",
            "machine_type": "compressor",
            "plant_area": "warehouse",
            "shift": "afternoon",
            "temperature_c": 56.4,
            "vibration_mm_s": 1.5,
            "pressure_bar": 6.4,
            "rpm": 1390,
            "noise_db": 64.8,
            "oil_quality_pct": 88.0,
            "hours_since_service": 96,
            "error_code": "OK",
            "technician_note": "routine production is continuing with no abnormal sound reported",
            "sensor_summary": "healthy telemetry profile",
            "recommended_action": "normal_operation",
        },
    ]

    for row in rows:
        row["system_prompt"] = SYSTEM_PROMPT
        row["user_prompt"] = build_user_prompt(row)
    return rows


def import_training_dependencies() -> dict[str, Any]:
    """
    Import GPU/ML libraries only when training is requested.

    The static CSV dataset is already provided in demos/endtoend/datasets.
    """

    try:
        import pandas as pd
        import torch
        from datasets import Dataset, DatasetDict
        from huggingface_hub import snapshot_download
        from peft import LoraConfig, PeftModel, get_peft_model, prepare_model_for_kbit_training
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            BitsAndBytesConfig,
            Trainer,
            TrainingArguments,
            set_seed,
        )
    except ImportError as exc:
        raise SystemExit(
            "\nMissing local LLM fine-tuning dependency.\n\n"
            "Install the required packages on your EC2 GPU machine:\n\n"
            "    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126\n"
            "    pip install transformers datasets accelerate peft trl bitsandbytes pandas scikit-learn hf_xet\n\n"
            "Original import error:\n"
            f"    {exc}\n"
        ) from exc

    return {
        "pd": pd,
        "torch": torch,
        "Dataset": Dataset,
        "DatasetDict": DatasetDict,
        "snapshot_download": snapshot_download,
        "LoraConfig": LoraConfig,
        "PeftModel": PeftModel,
        "get_peft_model": get_peft_model,
        "prepare_model_for_kbit_training": prepare_model_for_kbit_training,
        "AutoModelForCausalLM": AutoModelForCausalLM,
        "AutoTokenizer": AutoTokenizer,
        "BitsAndBytesConfig": BitsAndBytesConfig,
        "Trainer": Trainer,
        "TrainingArguments": TrainingArguments,
        "set_seed": set_seed,
    }


def validate_dataset_frame(df: Any) -> None:
    """Validate the CSV before fine-tuning starts."""

    required_columns = {
        "system_prompt",
        "user_prompt",
        "assistant_response",
        "recommended_action",
    }
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Dataset missing required columns: {sorted(missing_columns)}")

    if len(df) < 500:
        raise ValueError(f"Dataset has {len(df)} rows. Use at least 500 rows.")

    unexpected_labels = sorted(set(df["recommended_action"]) - set(ACTION_LABELS))
    if unexpected_labels:
        raise ValueError(f"Dataset contains unexpected recommended_action values: {unexpected_labels}")

    for column in ["system_prompt", "user_prompt", "assistant_response"]:
        empty_count = df[column].isna().sum() + (df[column].astype(str).str.strip() == "").sum()
        if empty_count:
            raise ValueError(f"Column {column} contains {empty_count} empty values.")

    # Make sure target responses are valid JSON. This matters because the model
    # is being trained to emit JSON, and bad target rows teach bad behavior.
    for index, value in enumerate(df["assistant_response"], start=1):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"assistant_response is invalid JSON at CSV row {index}: {exc}") from exc
        if parsed.get("recommended_action") not in ACTION_LABELS:
            raise ValueError(f"assistant_response has an invalid action at CSV row {index}: {parsed}")


def profile_defaults(profile: str) -> dict[str, Any]:
    """
    Return defaults for a training profile.

    The ec2_1_to_2_hour profile intentionally does enough work to feel like a
    real fine-tuning session in a class or workshop.
    """

    profiles = {
        "smoke": {
            "epochs": 1.0,
            "max_steps": 40,
            "max_length": 768,
            "batch_size": 1,
            "gradient_accumulation_steps": 4,
            "lora_r": 8,
            "lora_alpha": 16,
            "learning_rate": 2e-4,
            "save_steps": 20,
            "eval_steps": 20,
            "logging_steps": 5,
        },
        "ec2_1_to_2_hour": {
            "epochs": 8.0,
            "max_steps": -1,
            "max_length": 1536,
            "batch_size": 1,
            "gradient_accumulation_steps": 8,
            "lora_r": 32,
            "lora_alpha": 64,
            "learning_rate": 2e-4,
            "save_steps": 200,
            "eval_steps": 200,
            "logging_steps": 10,
        },
        "longer_quality": {
            "epochs": 10.0,
            "max_steps": -1,
            "max_length": 1536,
            "batch_size": 1,
            "gradient_accumulation_steps": 8,
            "lora_r": 32,
            "lora_alpha": 64,
            "learning_rate": 1.5e-4,
            "save_steps": 150,
            "eval_steps": 150,
            "logging_steps": 10,
        },
    }
    if profile not in profiles:
        raise ValueError(f"Unknown profile: {profile}")
    return profiles[profile]


def apply_profile_defaults(args: argparse.Namespace) -> argparse.Namespace:
    """Fill unset training arguments from the chosen profile."""

    defaults = profile_defaults(args.profile)
    for key, value in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, value)
    return args


def split_dataframe(df: Any, seed: int) -> tuple[Any, Any, Any]:
    """Create reproducible train/validation/test splits without extra packages."""

    train_parts = []
    validation_parts = []
    test_parts = []

    for _, group in df.groupby("recommended_action"):
        shuffled = group.sample(frac=1.0, random_state=seed)
        total = len(shuffled)
        train_end = math.floor(total * 0.90)
        validation_end = math.floor(total * 0.95)
        train_parts.append(shuffled.iloc[:train_end])
        validation_parts.append(shuffled.iloc[train_end:validation_end])
        test_parts.append(shuffled.iloc[validation_end:])

    pd = df.__class__
    # pandas exposes concat as a module function, so use the originating module
    # from the dataframe class to avoid importing pandas globally.
    pandas_module = __import__(pd.__module__.split(".")[0])
    train_df = pandas_module.concat(train_parts).sample(frac=1.0, random_state=seed).reset_index(drop=True)
    validation_df = pandas_module.concat(validation_parts).sample(frac=1.0, random_state=seed).reset_index(drop=True)
    test_df = pandas_module.concat(test_parts).sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return train_df, validation_df, test_df


def messages_from_row(row: dict[str, Any], include_assistant: bool) -> list[dict[str, str]]:
    """Build chat messages for a dataset row."""

    messages = [
        {"role": "system", "content": str(row["system_prompt"])},
        {"role": "user", "content": str(row["user_prompt"])},
    ]
    if include_assistant:
        messages.append({"role": "assistant", "content": str(row["assistant_response"])})
    return messages


def format_messages(tokenizer: Any, messages: list[dict[str, str]], add_generation_prompt: bool) -> str:
    """
    Format chat messages using the tokenizer's chat template when available.

    If a model does not define a chat template, use a simple readable fallback.
    """

    try:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=add_generation_prompt,
        )
    except Exception:
        rendered: list[str] = []
        for message in messages:
            role = message["role"].upper()
            rendered.append(f"{role}:\n{message['content']}")
        if add_generation_prompt:
            rendered.append("ASSISTANT:\n")
        return "\n\n".join(rendered)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write JSONL records for auditability."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=True) + "\n")


def write_training_splits(
    split_dir: Path,
    tokenizer: Any,
    train_df: Any,
    validation_df: Any,
    test_df: Any,
) -> None:
    """
    Save chat-formatted train/validation/test splits.

    These files are not strictly required by Trainer, but they are valuable in a
    teaching repo because they show exactly what the LLM is trained to imitate.
    """

    split_dir.mkdir(parents=True, exist_ok=True)

    for split_name, frame in [
        ("train", train_df),
        ("validation", validation_df),
        ("test", test_df),
    ]:
        records = []
        for row in frame.to_dict(orient="records"):
            messages = messages_from_row(row, include_assistant=True)
            records.append(
                {
                    "example_id": row["example_id"],
                    "recommended_action": row["recommended_action"],
                    "messages": messages,
                    "text": format_messages(tokenizer, messages, add_generation_prompt=False),
                }
            )
        write_jsonl(split_dir / f"{split_name}.jsonl", records)


@dataclass
class CausalLMCollator:
    """
    Pad input_ids, attention_mask, and labels for causal language modeling.

    Label value -100 tells PyTorch to ignore that token in the loss. We use this
    to ignore the prompt and train the model mostly on the assistant answer.
    """

    tokenizer: Any
    torch: Any

    def __call__(self, features: list[dict[str, list[int]]]) -> dict[str, Any]:
        pad_token_id = self.tokenizer.pad_token_id
        if pad_token_id is None:
            pad_token_id = self.tokenizer.eos_token_id

        max_length = max(len(feature["input_ids"]) for feature in features)
        batch_input_ids = []
        batch_attention_mask = []
        batch_labels = []

        for feature in features:
            input_ids = feature["input_ids"]
            attention_mask = feature["attention_mask"]
            labels = feature["labels"]
            padding = max_length - len(input_ids)
            batch_input_ids.append(input_ids + [pad_token_id] * padding)
            batch_attention_mask.append(attention_mask + [0] * padding)
            batch_labels.append(labels + [-100] * padding)

        return {
            "input_ids": self.torch.tensor(batch_input_ids, dtype=self.torch.long),
            "attention_mask": self.torch.tensor(batch_attention_mask, dtype=self.torch.long),
            "labels": self.torch.tensor(batch_labels, dtype=self.torch.long),
        }


def tokenize_for_sft(tokenizer: Any, row: dict[str, Any], max_length: int) -> dict[str, list[int]]:
    """
    Tokenize one instruction-tuning example.

    The prompt tokens are masked with -100 so the loss focuses on learning the
    assistant response. This is closer to real instruction fine-tuning than
    training the model to reproduce both the user prompt and the answer.
    """

    prompt_messages = messages_from_row(row, include_assistant=False)
    full_messages = messages_from_row(row, include_assistant=True)

    prompt_text = format_messages(tokenizer, prompt_messages, add_generation_prompt=True)
    full_text = format_messages(tokenizer, full_messages, add_generation_prompt=False)

    prompt_tokens = tokenizer(
        prompt_text,
        truncation=True,
        max_length=max_length,
        add_special_tokens=False,
    )
    full_tokens = tokenizer(
        full_text,
        truncation=True,
        max_length=max_length,
        add_special_tokens=False,
    )

    input_ids = full_tokens["input_ids"]
    attention_mask = full_tokens["attention_mask"]
    labels = input_ids.copy()
    prompt_length = min(len(prompt_tokens["input_ids"]), len(labels))

    if prompt_length < len(labels):
        labels[:prompt_length] = [-100] * prompt_length
    else:
        # If the answer was truncated away, keep the last few tokens trainable
        # instead of dropping the example. This should be rare with the default
        # max_length.
        keep = min(32, len(labels))
        labels[:-keep] = [-100] * (len(labels) - keep)

    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels,
    }


def training_arguments_compat(TrainingArguments: Any, **kwargs: Any) -> Any:
    """Create TrainingArguments across old/new Transformers versions."""

    signature = inspect.signature(TrainingArguments.__init__)
    if "eval_strategy" in signature.parameters:
        kwargs["eval_strategy"] = kwargs.pop("evaluation_strategy")
    return TrainingArguments(**kwargs)


def trainer_compat(Trainer: Any, tokenizer: Any, **kwargs: Any) -> Any:
    """Create Trainer across old/new Transformers versions."""

    signature = inspect.signature(Trainer.__init__)
    if "processing_class" in signature.parameters:
        kwargs["processing_class"] = tokenizer
    else:
        kwargs["tokenizer"] = tokenizer
    return Trainer(**kwargs)


def hardware_report(torch: Any, allow_cpu: bool) -> dict[str, Any]:
    """Inspect hardware and fail early if the user forgot the GPU."""

    report: dict[str, Any] = {
        "cuda_available": bool(torch.cuda.is_available()),
        "device": "cpu",
        "gpu_name": None,
        "gpu_memory_gb": None,
        "bf16_supported": False,
    }

    print("\nHardware check")
    print("--------------")

    if torch.cuda.is_available():
        props = torch.cuda.get_device_properties(0)
        report.update(
            {
                "device": "cuda",
                "gpu_name": torch.cuda.get_device_name(0),
                "gpu_memory_gb": round(props.total_memory / (1024**3), 2),
                "bf16_supported": bool(torch.cuda.is_bf16_supported()),
            }
        )
        print(f"CUDA GPU detected: {report['gpu_name']}")
        print(f"GPU memory: {report['gpu_memory_gb']} GB")
        print(f"BF16 supported: {report['bf16_supported']}")
        return report

    print("No CUDA GPU detected.")
    if not allow_cpu:
        raise SystemExit(
            "\nThis Ollama-style LLM fine-tuning script is designed for an EC2 GPU.\n"
            "Rerun on a GPU instance, or pass --allow-cpu for a very slow local test.\n"
        )

    print("Continuing on CPU because --allow-cpu was provided. This can take many hours.")
    return report


def load_tokenizer(AutoTokenizer: Any, model_name: str) -> Any:
    """Load tokenizer and ensure a pad token exists."""

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    return tokenizer


def load_model_with_lora(
    deps: dict[str, Any],
    args: argparse.Namespace,
    compute_dtype: Any,
) -> Any:
    """Load a causal LLM and attach trainable LoRA adapters."""

    torch = deps["torch"]
    AutoModelForCausalLM = deps["AutoModelForCausalLM"]
    BitsAndBytesConfig = deps["BitsAndBytesConfig"]
    LoraConfig = deps["LoraConfig"]
    get_peft_model = deps["get_peft_model"]
    prepare_model_for_kbit_training = deps["prepare_model_for_kbit_training"]

    quantization_config = None
    if args.training_mode == "qlora":
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=compute_dtype,
        )

    model_kwargs = {
        "torch_dtype": compute_dtype if torch.cuda.is_available() else torch.float32,
        "device_map": "auto" if torch.cuda.is_available() else None,
    }
    if quantization_config is not None:
        model_kwargs["quantization_config"] = quantization_config

    print("\nLoading base chat model")
    print("-----------------------")
    print(f"Base model: {args.model_name}")
    print(f"Training mode: {args.training_mode}")
    print("The first run will download model files from Hugging Face if they are not cached.")

    model = AutoModelForCausalLM.from_pretrained(args.model_name, **model_kwargs)
    model.config.use_cache = False

    if args.training_mode == "qlora":
        model = prepare_model_for_kbit_training(model)
    elif args.gradient_checkpointing:
        model.gradient_checkpointing_enable()

    target_modules = [module.strip() for module in args.target_modules.split(",") if module.strip()]
    lora_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        target_modules=target_modules,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    return model


def estimate_training_shape(train_rows: int, args: argparse.Namespace) -> dict[str, Any]:
    """Estimate optimizer steps so learners know why the run takes time."""

    effective_batch = args.batch_size * args.gradient_accumulation_steps
    steps_per_epoch = math.ceil(train_rows / effective_batch)
    planned_steps = args.max_steps if args.max_steps and args.max_steps > 0 else math.ceil(steps_per_epoch * args.epochs)
    return {
        "train_rows": train_rows,
        "per_device_batch_size": args.batch_size,
        "gradient_accumulation_steps": args.gradient_accumulation_steps,
        "effective_batch_size": effective_batch,
        "steps_per_epoch": steps_per_epoch,
        "planned_optimizer_steps": planned_steps,
    }


def save_base_model_snapshot(snapshot_download: Any, args: argparse.Namespace, base_snapshot_dir: Path) -> None:
    """
    Save the base model beside the adapter.

    This makes the Ollama import recipe easier because the Modelfile can point
    to a visible local base model path.
    """

    if base_snapshot_dir.exists() and any(base_snapshot_dir.iterdir()):
        print(f"Base model snapshot already exists: {base_snapshot_dir}")
        return

    print("\nSaving base model snapshot for Ollama")
    print("-------------------------------------")
    print(f"Snapshot target: {base_snapshot_dir}")
    base_snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=args.model_name,
        local_dir=str(base_snapshot_dir),
        local_dir_use_symlinks=False,
        ignore_patterns=["*.msgpack", "*.h5", "*.ot"],
    )


def extract_first_json_object(text: str) -> dict[str, Any] | None:
    """Best-effort JSON extraction from a model generation."""

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def get_model_device(model: Any, torch: Any) -> Any:
    """Return the first parameter device for a model."""

    try:
        return next(model.parameters()).device
    except StopIteration:
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def write_sample_prompt_markdown(prompt_dir: Path, rows: list[dict[str, Any]]) -> Path:
    """
    Save the fixed before/after prompts as a readable Markdown file.

    Students can copy these prompts into the base model and fine-tuned model
    manually, or they can inspect the generated JSONL files produced by this
    script.
    """

    prompt_dir.mkdir(parents=True, exist_ok=True)
    path = prompt_dir / "sample_prompts.md"
    lines = [
        "# Fine-Tuning Prompt Checks",
        "",
        "Use these exact prompts before and after fine-tuning.",
        "The expected action is shown above each prompt for instructor reference.",
        "",
    ]

    for index, row in enumerate(rows, start=1):
        lines.extend(
            [
                f"## Prompt {index}: {row['recommended_action']}",
                "",
                f"Expected recommended_action: `{row['recommended_action']}`",
                "",
                "System prompt:",
                "",
                "```text",
                SYSTEM_PROMPT,
                "```",
                "",
                "User prompt:",
                "",
                "```text",
                row["user_prompt"],
                "```",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def generate_prompt_check_outputs(
    torch: Any,
    model: Any,
    tokenizer: Any,
    rows: list[dict[str, Any]],
    output_path: Path,
    max_new_tokens: int,
    label: str,
) -> list[dict[str, Any]]:
    """
    Generate outputs for the fixed prompt checks.

    This function is used twice:

        1. before training, to capture the downloaded base model behavior
        2. after training, to capture the fine-tuned adapter behavior
    """

    model.eval()
    model_device = get_model_device(model, torch)
    records = []

    for row in rows:
        messages = messages_from_row(row, include_assistant=False)
        prompt = format_messages(tokenizer, messages, add_generation_prompt=True)
        encoded = tokenizer(prompt, return_tensors="pt")
        encoded = {key: value.to(model_device) for key, value in encoded.items()}

        with torch.no_grad():
            generated = model.generate(
                **encoded,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                temperature=None,
                top_p=None,
                pad_token_id=tokenizer.eos_token_id,
            )

        new_tokens = generated[0][encoded["input_ids"].shape[-1] :]
        generated_text = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        parsed = extract_first_json_object(generated_text)
        predicted_action = parsed.get("recommended_action") if parsed else None
        expected_action = row["recommended_action"]

        records.append(
            {
                "phase": label,
                "example_id": row["example_id"],
                "expected_action": expected_action,
                "predicted_action": predicted_action,
                "correct": predicted_action == expected_action,
                "prompt": prompt,
                "generated_response": generated_text,
                "parsed_json": parsed,
            }
        )

    write_jsonl(output_path, records)
    return records


def write_prompt_check_comparison(
    output_path: Path,
    base_records: list[dict[str, Any]],
    fine_tuned_records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Write a compact before/after comparison for the fixed prompt checks."""

    by_id = {record["example_id"]: record for record in fine_tuned_records}
    comparisons = []

    for base_record in base_records:
        after_record = by_id[base_record["example_id"]]
        comparisons.append(
            {
                "example_id": base_record["example_id"],
                "expected_action": base_record["expected_action"],
                "base_model_action": base_record["predicted_action"],
                "fine_tuned_action": after_record["predicted_action"],
                "base_model_correct": base_record["correct"],
                "fine_tuned_correct": after_record["correct"],
            }
        )

    base_correct = sum(1 for record in base_records if record["correct"])
    fine_tuned_correct = sum(1 for record in fine_tuned_records if record["correct"])
    summary = {
        "sample_count": len(comparisons),
        "base_model_correct": base_correct,
        "base_model_accuracy": base_correct / len(comparisons) if comparisons else 0.0,
        "fine_tuned_correct": fine_tuned_correct,
        "fine_tuned_accuracy": fine_tuned_correct / len(comparisons) if comparisons else 0.0,
        "comparisons": comparisons,
    }
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def generate_test_predictions(
    torch: Any,
    model: Any,
    tokenizer: Any,
    test_df: Any,
    output_path: Path,
    sample_count: int,
    max_new_tokens: int,
) -> dict[str, Any]:
    """
    Generate answers for held-out examples and score recommended_action.

    This is not a replacement for a production eval suite. It is a transparent
    classroom check that shows whether the fine-tuned model learned the action
    schema.
    """

    model.eval()
    samples = test_df.head(sample_count).to_dict(orient="records")
    correct = 0
    records = []

    for row in samples:
        messages = messages_from_row(row, include_assistant=False)
        prompt = format_messages(tokenizer, messages, add_generation_prompt=True)
        encoded = tokenizer(prompt, return_tensors="pt")
        model_device = get_model_device(model, torch)
        encoded = {key: value.to(model_device) for key, value in encoded.items()}

        with torch.no_grad():
            generated = model.generate(
                **encoded,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                temperature=None,
                top_p=None,
                pad_token_id=tokenizer.eos_token_id,
            )

        new_tokens = generated[0][encoded["input_ids"].shape[-1] :]
        generated_text = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        parsed = extract_first_json_object(generated_text)
        predicted_action = parsed.get("recommended_action") if parsed else None
        expected_action = row["recommended_action"]
        is_correct = predicted_action == expected_action
        correct += int(is_correct)

        records.append(
            {
                "example_id": row["example_id"],
                "expected_action": expected_action,
                "predicted_action": predicted_action,
                "correct": is_correct,
                "prompt": prompt,
                "expected_response": row["assistant_response"],
                "generated_response": generated_text,
            }
        )

    write_jsonl(output_path, records)
    accuracy = correct / len(records) if records else 0.0
    return {
        "sample_count": len(records),
        "recommended_action_accuracy": accuracy,
        "correct": correct,
        "output_file": str(output_path),
    }


def write_ollama_files(
    ollama_dir: Path,
    output_dir: Path,
    adapter_dir: Path,
    base_snapshot_dir: Path,
    merged_model_dir: Path,
    args: argparse.Namespace,
    wrote_merged: bool,
) -> None:
    """
    Write Ollama Modelfiles and copy-ready commands.

    The adapter Modelfile is the default path for this script. It keeps the
    base model and LoRA adapter separate, which makes the fine-tuned artifact
    easy to inspect.
    """

    ollama_dir.mkdir(parents=True, exist_ok=True)

    adapter_modelfile = ollama_dir / "Modelfile.adapter"
    adapter_modelfile.write_text(
        "\n".join(
            [
                "# Ollama Modelfile generated by finetune_local_05b_llm.py",
                "# It uses the same base model snapshot that was used during fine-tuning.",
                f"FROM {base_snapshot_dir.resolve()}",
                f"ADAPTER {adapter_dir.resolve()}",
                "PARAMETER temperature 0.2",
                "PARAMETER top_p 0.9",
                "PARAMETER num_ctx 2048",
                f'SYSTEM """{SYSTEM_PROMPT}"""',
                "",
            ]
        ),
        encoding="utf-8",
    )

    command_lines = [
        "# Run these after installing Ollama on the EC2 instance or on another machine.",
        "# Build the Ollama model from the base snapshot plus LoRA adapter:",
        f"cd {ollama_dir.resolve()}",
        f"ollama create {args.ollama_model_name} -f Modelfile.adapter",
        f"ollama run {args.ollama_model_name}",
        "",
        "# Example prompt to paste into ollama run:",
        "Analyze this machine telemetry report and return the maintenance decision as strict JSON.",
        "Machine: CNC-9001",
        "Machine type: CNC mill",
        "Plant area: fabrication",
        "Shift: night",
        "Temperature C: 118.2",
        "Vibration mm/s: 10.9",
        "Pressure bar: 12.1",
        "RPM: 2210",
        "Noise dB: 107.4",
        "Oil quality percent: 12.0",
        "Hours since service: 730",
        "Error code: CRIT-900",
        "Technician note: critical alarm is active and visible shaking was reported",
        "Sensor summary: severe multi-sensor alarm",
        "",
    ]

    if wrote_merged:
        merged_modelfile = ollama_dir / "Modelfile.merged"
        merged_modelfile.write_text(
            "\n".join(
                [
                    "# Ollama Modelfile for the optional merged full model.",
                    f"FROM {merged_model_dir.resolve()}",
                    "PARAMETER temperature 0.2",
                    "PARAMETER top_p 0.9",
                    "PARAMETER num_ctx 2048",
                    f'SYSTEM """{SYSTEM_PROMPT}"""',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        command_lines.extend(
            [
                "# Optional merged-model import:",
                f"ollama create {args.ollama_model_name}-merged -f Modelfile.merged",
                f"ollama run {args.ollama_model_name}-merged",
                "",
            ]
        )

    (ollama_dir / "ollama_commands.txt").write_text("\n".join(command_lines), encoding="utf-8")


def write_run_summary(
    summary_path: Path,
    args: argparse.Namespace,
    hardware: dict[str, Any],
    dataset_counts: dict[str, int],
    step_shape: dict[str, Any],
    files: dict[str, str],
    metrics: dict[str, Any],
) -> None:
    """Write a human-readable summary for learners."""

    lines = [
        "# Local 0.5B LLM Fine-Tuning Run",
        "",
        "## Objective",
        "",
        "Fine-tune a local 0.5B chat LLM to analyze hypothetical machine telemetry and return maintenance decisions as strict JSON.",
        "",
        "Target machine: AWS EC2 g6.xlarge with a 24 GB NVIDIA L4 GPU and a 100 GB EBS volume.",
        "Target runtime: roughly 1-2 hours with the default `ec2_1_to_2_hour` profile.",
        "",
        "## Hardware",
        "",
        f"- Device: {hardware['device']}",
        f"- GPU: {hardware.get('gpu_name')}",
        f"- GPU memory GB: {hardware.get('gpu_memory_gb')}",
        f"- BF16 supported: {hardware.get('bf16_supported')}",
        "",
        "## Training Configuration",
        "",
        f"- Base model: {args.model_name}",
        f"- Training mode: {args.training_mode}",
        f"- Profile: {args.profile}",
        f"- Dataset rows: {sum(dataset_counts.values())}",
        f"- Epochs: {args.epochs}",
        f"- Max steps: {args.max_steps}",
        f"- Max sequence length: {args.max_length}",
        f"- Batch size: {args.batch_size}",
        f"- Gradient accumulation steps: {args.gradient_accumulation_steps}",
        f"- Effective batch size: {step_shape['effective_batch_size']}",
        f"- Planned optimizer steps: {step_shape['planned_optimizer_steps']}",
        f"- LoRA rank: {args.lora_r}",
        f"- LoRA alpha: {args.lora_alpha}",
        f"- Learning rate: {args.learning_rate}",
        "",
        "## Dataset Counts",
        "",
    ]
    for label, count in sorted(dataset_counts.items()):
        lines.append(f"- {label}: {count}")

    lines.extend(
        [
            "",
            "## Output Files",
            "",
            f"- Adapter: {files['adapter_dir']}",
            f"- Base model snapshot: {files['base_snapshot_dir']}",
            f"- Training splits: {files['split_dir']}",
            f"- Metrics directory: {files['metrics_dir']}",
            f"- Sample prompts: {files['sample_prompts']}",
            f"- Before/after prompt comparison: {files['prompt_comparison']}",
            f"- Test generations: {files['test_generations']}",
            f"- Prompt checks: {files['prompt_check_dir']}",
            f"- Ollama directory: {files['ollama_dir']}",
            "",
            "## Metrics",
            "",
            "```json",
            json.dumps(metrics, indent=2, sort_keys=True),
            "```",
            "",
            "## Ollama Next Step",
            "",
            "Open `ollama/ollama_commands.txt` and run the generated `ollama create` command.",
            "",
        ]
    )
    summary_path.write_text("\n".join(lines), encoding="utf-8")


def merge_adapter_if_requested(
    deps: dict[str, Any],
    args: argparse.Namespace,
    adapter_dir: Path,
    merged_model_dir: Path,
    tokenizer: Any,
) -> bool:
    """
    Optionally merge LoRA adapter weights into the base model.

    This produces a larger full-model directory. It can be useful if you prefer
    importing a single model directory into Ollama, but it needs more memory and
    disk than keeping adapter and base separate.
    """

    if not args.merge_adapter:
        return False

    torch = deps["torch"]
    AutoModelForCausalLM = deps["AutoModelForCausalLM"]
    PeftModel = deps["PeftModel"]

    print("\nMerging adapter into full model")
    print("--------------------------------")
    print("This can need significant CPU RAM/GPU VRAM and disk space.")

    dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float16
    base_model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        torch_dtype=dtype if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    merged = PeftModel.from_pretrained(base_model, adapter_dir)
    merged = merged.merge_and_unload()
    merged_model_dir.mkdir(parents=True, exist_ok=True)
    merged.save_pretrained(merged_model_dir, safe_serialization=True)
    tokenizer.save_pretrained(merged_model_dir)
    print(f"Merged model saved to: {merged_model_dir}")
    return True


def run_training(args: argparse.Namespace) -> None:
    """Run the complete local LLM fine-tuning workflow."""

    args = apply_profile_defaults(args)
    deps = import_training_dependencies()
    pd = deps["pd"]
    torch = deps["torch"]
    Dataset = deps["Dataset"]
    DatasetDict = deps["DatasetDict"]
    AutoTokenizer = deps["AutoTokenizer"]
    Trainer = deps["Trainer"]
    TrainingArguments = deps["TrainingArguments"]
    set_seed = deps["set_seed"]
    snapshot_download = deps["snapshot_download"]

    set_seed(args.seed)
    hardware = hardware_report(torch, allow_cpu=args.allow_cpu)

    dataset_path = Path(args.dataset).resolve()
    output_dir = Path(args.output_dir).resolve()
    docs_dir = Path(args.docs_dir).resolve()
    adapter_dir = output_dir / "adapter"
    base_snapshot_dir = output_dir / "base_model_snapshot"
    split_dir = output_dir / "training_splits"
    metrics_dir = output_dir / "metrics"
    ollama_dir = output_dir / "ollama"
    merged_model_dir = output_dir / "merged_model"
    test_generations_path = output_dir / "test_generations.jsonl"
    prompt_check_dir = output_dir / "prompt_checks"
    sample_prompts_path = docs_dir / "sample_prompts.md"
    base_prompt_check_path = prompt_check_dir / "base_model_generations.jsonl"
    fine_tuned_prompt_check_path = prompt_check_dir / "fine_tuned_generations.jsonl"
    prompt_comparison_path = prompt_check_dir / "before_after_comparison.json"

    if args.clean_output and output_dir.exists():
        resolved_output = output_dir.resolve()
        resolved_endtoend = ENDTOEND_DIR.resolve()
        if resolved_output == resolved_endtoend or not str(resolved_output).startswith(str(resolved_endtoend)):
            raise SystemExit(f"Refusing to clean output outside the endtoend directory: {resolved_output}")
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    print_step(
        1,
        TOTAL_RUN_STEPS,
        "Locate provided training dataset",
        f"Expected CSV: {dataset_path}",
    )
    if not dataset_path.exists():
        raise SystemExit(
            "\nTraining dataset not found.\n\n"
            f"Expected file:\n  {dataset_path}\n\n"
            "This demo expects the course CSV to already exist under demos/endtoend/datasets.\n"
        )
    print("Using the provided course dataset. The training script only reads dataset rows.")

    print_step(2, TOTAL_RUN_STEPS, "Load and validate instruction dataset", f"Dataset path: {dataset_path}")
    df = pd.read_csv(dataset_path)
    validate_dataset_frame(df)
    dataset_counts = dict(Counter(df["recommended_action"]))
    print(f"Dataset path: {dataset_path}")
    print(f"Rows: {len(df)}")
    print("Training objective: system_prompt + user_prompt -> assistant_response strict JSON maintenance decision.")
    print("Action distribution:")
    print(df["recommended_action"].value_counts().sort_index().to_string())

    train_df, validation_df, test_df = split_dataframe(df, seed=args.seed)
    print_step(3, TOTAL_RUN_STEPS, "Split dataset into train, validation, and test")
    print(f"Train rows:      {len(train_df)}")
    print(f"Validation rows: {len(validation_df)}")
    print(f"Test rows:       {len(test_df)}")
    print("Training objective check: the model will train on more than 2,000 examples.")

    print_step(4, TOTAL_RUN_STEPS, "Load tokenizer and write audit files")
    tokenizer = load_tokenizer(AutoTokenizer, args.model_name)
    write_training_splits(split_dir, tokenizer, train_df, validation_df, test_df)
    prompt_rows = sample_prompt_rows()
    sample_prompts_path = write_sample_prompt_markdown(docs_dir, prompt_rows)
    print(f"Training split audit files: {split_dir}")
    print(f"Sample prompt handout:      {sample_prompts_path}")

    dataset = DatasetDict(
        {
            "train": Dataset.from_pandas(train_df.reset_index(drop=True)),
            "validation": Dataset.from_pandas(validation_df.reset_index(drop=True)),
            "test": Dataset.from_pandas(test_df.reset_index(drop=True)),
        }
    )

    def tokenize_batch(batch: dict[str, list[Any]]) -> dict[str, list[list[int]]]:
        tokenized = {"input_ids": [], "attention_mask": [], "labels": []}
        batch_rows = [dict(zip(batch.keys(), values)) for values in zip(*batch.values())]
        for row in batch_rows:
            item = tokenize_for_sft(tokenizer, row, max_length=args.max_length)
            tokenized["input_ids"].append(item["input_ids"])
            tokenized["attention_mask"].append(item["attention_mask"])
            tokenized["labels"].append(item["labels"])
        return tokenized

    print_step(5, TOTAL_RUN_STEPS, "Tokenize instruction examples")
    tokenized_dataset = dataset.map(
        tokenize_batch,
        batched=True,
        remove_columns=dataset["train"].column_names,
    )

    compute_dtype = torch.float32
    use_bf16 = False
    use_fp16 = False
    if torch.cuda.is_available():
        if torch.cuda.is_bf16_supported():
            compute_dtype = torch.bfloat16
            use_bf16 = True
        else:
            compute_dtype = torch.float16
            use_fp16 = True

    print_step(
        6,
        TOTAL_RUN_STEPS,
        "Load Hugging Face base model and attach QLoRA adapters",
        f"Base model: {args.model_name}; training mode: {args.training_mode}",
    )
    model = load_model_with_lora(deps, args, compute_dtype=compute_dtype)
    collator = CausalLMCollator(tokenizer=tokenizer, torch=torch)
    step_shape = estimate_training_shape(len(train_df), args)

    print_step(7, TOTAL_RUN_STEPS, "Run before-fine-tuning prompt check")
    print("Running fixed prompts against the downloaded base model behavior.")
    base_prompt_records = generate_prompt_check_outputs(
        torch=torch,
        model=model,
        tokenizer=tokenizer,
        rows=prompt_rows,
        output_path=base_prompt_check_path,
        max_new_tokens=args.max_new_tokens,
        label="before_fine_tuning",
    )
    print(f"Base-model prompt check saved to: {base_prompt_check_path}")

    print_step(8, TOTAL_RUN_STEPS, "Show training plan and estimated step count")
    print(json.dumps(step_shape, indent=2))
    print("Expected classroom runtime on a 24 GB EC2 GPU: roughly 1-2 hours with the default profile.")

    training_args = training_arguments_compat(
        TrainingArguments,
        output_dir=str(output_dir / "checkpoints"),
        num_train_epochs=args.epochs,
        max_steps=args.max_steps,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        warmup_ratio=args.warmup_ratio,
        lr_scheduler_type=args.lr_scheduler_type,
        logging_steps=args.logging_steps,
        save_steps=args.save_steps,
        save_total_limit=args.save_total_limit,
        evaluation_strategy="steps",
        eval_steps=args.eval_steps,
        bf16=use_bf16,
        fp16=use_fp16,
        tf32=torch.cuda.is_available(),
        gradient_checkpointing=args.gradient_checkpointing,
        optim=args.optim,
        report_to="none",
        remove_unused_columns=False,
        group_by_length=True,
        dataloader_num_workers=args.dataloader_num_workers,
        dataloader_pin_memory=torch.cuda.is_available(),
        seed=args.seed,
    )

    trainer = trainer_compat(
        Trainer,
        tokenizer=tokenizer,
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        data_collator=collator,
    )

    print_step(9, TOTAL_RUN_STEPS, "Start QLoRA fine-tuning")
    print("The base model is frozen; LoRA adapter weights are being trained.")
    train_result = trainer.train(resume_from_checkpoint=args.resume_from_checkpoint)
    train_metrics = train_result.metrics
    trainer.save_metrics("train", train_metrics)
    (metrics_dir / "train_metrics.json").write_text(json.dumps(train_metrics, indent=2), encoding="utf-8")

    print_step(10, TOTAL_RUN_STEPS, "Evaluate validation split")
    eval_metrics = trainer.evaluate(tokenized_dataset["validation"])
    trainer.save_metrics("eval", eval_metrics)
    (metrics_dir / "eval_metrics.json").write_text(json.dumps(eval_metrics, indent=2), encoding="utf-8")

    print_step(11, TOTAL_RUN_STEPS, "Save trained LoRA adapter")
    adapter_dir.mkdir(parents=True, exist_ok=True)
    trainer.model.save_pretrained(adapter_dir)
    tokenizer.save_pretrained(adapter_dir)
    print(f"Adapter saved to: {adapter_dir}")

    print_step(12, TOTAL_RUN_STEPS, "Run after-fine-tuning prompt check")
    print("Running the same fixed prompts against the fine-tuned adapter model.")
    fine_tuned_prompt_records = generate_prompt_check_outputs(
        torch=torch,
        model=trainer.model,
        tokenizer=tokenizer,
        rows=prompt_rows,
        output_path=fine_tuned_prompt_check_path,
        max_new_tokens=args.max_new_tokens,
        label="after_fine_tuning",
    )
    prompt_comparison = write_prompt_check_comparison(
        output_path=prompt_comparison_path,
        base_records=base_prompt_records,
        fine_tuned_records=fine_tuned_prompt_records,
    )
    print(f"Before/after prompt comparison saved to: {prompt_comparison_path}")
    print(json.dumps(prompt_comparison, indent=2))

    if args.save_base_snapshot:
        print_step(13, TOTAL_RUN_STEPS, "Save base model snapshot for local runtime import")
        save_base_model_snapshot(snapshot_download, args, base_snapshot_dir)
    else:
        print_step(13, TOTAL_RUN_STEPS, "Skip base model snapshot")
        base_snapshot_dir.mkdir(parents=True, exist_ok=True)
        (base_snapshot_dir / "README.txt").write_text(
            "Base model snapshot was skipped. Rerun with --save-base-snapshot to create Ollama-ready Modelfile paths.\n",
            encoding="utf-8",
        )

    print_step(14, TOTAL_RUN_STEPS, "Generate held-out test samples")
    test_accuracy = generate_test_predictions(
        torch=torch,
        model=trainer.model,
        tokenizer=tokenizer,
        test_df=test_df,
        output_path=test_generations_path,
        sample_count=args.test_generation_samples,
        max_new_tokens=args.max_new_tokens,
    )
    (metrics_dir / "test_action_accuracy.json").write_text(
        json.dumps(test_accuracy, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(test_accuracy, indent=2))

    print_step(15, TOTAL_RUN_STEPS, "Write optional local-runtime files")
    wrote_merged = merge_adapter_if_requested(deps, args, adapter_dir, merged_model_dir, tokenizer)
    write_ollama_files(
        ollama_dir=ollama_dir,
        output_dir=output_dir,
        adapter_dir=adapter_dir,
        base_snapshot_dir=base_snapshot_dir,
        merged_model_dir=merged_model_dir,
        args=args,
        wrote_merged=wrote_merged,
    )

    files = {
        "adapter_dir": str(adapter_dir),
        "base_snapshot_dir": str(base_snapshot_dir),
        "split_dir": str(split_dir),
        "metrics_dir": str(metrics_dir),
        "test_generations": str(test_generations_path),
        "prompt_check_dir": str(prompt_check_dir),
        "sample_prompts": str(sample_prompts_path),
        "prompt_comparison": str(prompt_comparison_path),
        "ollama_dir": str(ollama_dir),
    }
    combined_metrics = {
        "train": train_metrics,
        "validation": eval_metrics,
        "prompt_check": prompt_comparison,
        "test_generation": test_accuracy,
    }
    print_step(16, TOTAL_RUN_STEPS, "Write final run summary")
    write_run_summary(
        summary_path=docs_dir / "latest_run_summary.md",
        args=args,
        hardware=hardware,
        dataset_counts=dataset_counts,
        step_shape=step_shape,
        files=files,
        metrics=combined_metrics,
    )

    print("\nDone")
    print("----")
    print(f"Run summary: {docs_dir / 'latest_run_summary.md'}")
    print(f"Before/after prompt checks: {prompt_comparison_path}")
    print(f"Ollama commands: {ollama_dir / 'ollama_commands.txt'}")
    print(f"Main fine-tuned artifact: {adapter_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fine-tune a local 0.5B chat LLM with QLoRA by default and write optional runtime import files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--docs-dir", type=Path, default=DEFAULT_DOCS_DIR)
    parser.add_argument("--model-name", default=DEFAULT_BASE_MODEL)
    parser.add_argument("--ollama-model-name", default=DEFAULT_OLLAMA_MODEL_NAME)
    parser.add_argument(
        "--profile",
        choices=["smoke", "ec2_1_to_2_hour", "longer_quality"],
        default="ec2_1_to_2_hour",
        help="Preset controlling training duration and hyperparameters.",
    )
    parser.add_argument("--epochs", type=float, default=None)
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--max-length", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--gradient-accumulation-steps", type=int, default=None)
    parser.add_argument("--learning-rate", type=float, default=None)
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument("--warmup-ratio", type=float, default=0.03)
    parser.add_argument("--lr-scheduler-type", default="cosine")
    parser.add_argument("--lora-r", type=int, default=None)
    parser.add_argument("--lora-alpha", type=int, default=None)
    parser.add_argument("--lora-dropout", type=float, default=0.05)
    parser.add_argument(
        "--target-modules",
        default="q_proj,k_proj,v_proj,o_proj,gate_proj,up_proj,down_proj",
        help="Comma-separated module names where LoRA adapters are attached.",
    )
    parser.add_argument(
        "--training-mode",
        choices=["lora", "qlora"],
        default="qlora",
        help="Use qlora for the default 4-bit base-model training path; use lora for plain adapter training.",
    )
    parser.add_argument("--optim", default="adamw_torch")
    parser.add_argument("--save-steps", type=int, default=None)
    parser.add_argument("--eval-steps", type=int, default=None)
    parser.add_argument("--logging-steps", type=int, default=None)
    parser.add_argument("--save-total-limit", type=int, default=3)
    parser.add_argument("--dataloader-num-workers", type=int, default=1)
    parser.add_argument("--test-generation-samples", type=int, default=24)
    parser.add_argument("--max-new-tokens", type=int, default=220)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--allow-cpu", action="store_true")
    parser.add_argument("--clean-output", action="store_true")
    parser.add_argument("--gradient-checkpointing", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--save-base-snapshot", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--merge-adapter", action="store_true")
    parser.add_argument("--resume-from-checkpoint", default=None)
    return parser.parse_args()


def main() -> None:
    args = apply_profile_defaults(parse_args())

    print("\nEnd-to-End Local 0.5B LLM Fine-Tuning")
    print("=====================================")
    print("Objective: train a downloaded 0.5B chat model with QLoRA adapters.")
    print(f"Profile: {args.profile}")
    print(f"Expected EC2 GPU runtime: {'short smoke test' if args.profile == 'smoke' else 'roughly 1-2 hours'}")

    run_training(args)


if __name__ == "__main__":
    main()
