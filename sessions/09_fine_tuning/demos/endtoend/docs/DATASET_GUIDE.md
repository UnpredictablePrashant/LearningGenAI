# Dataset Guide And Training Objective

This document explains the objective of the fine-tuning demo and the meaning of
every column in the provided CSV dataset.

## Objective

The objective is to fine-tune a downloaded local chat LLM so it behaves like a
small industrial maintenance assistant called `PlantOps-MaintenanceAI`.

The model starts as:

```text
Qwen/Qwen2.5-0.5B-Instruct
```

The training method is:

```text
QLoRA: 4-bit base model loading + trained LoRA adapter weights
```

The target EC2 machine is:

```text
AWS EC2 g6.xlarge
Ubuntu
1 NVIDIA L4 GPU with 24 GB VRAM
100 GB EBS storage
Target run time: roughly 1-2 hours with the default profile
```

The business-style task is:

```text
Given a machine telemetry report and technician note,
return a strict JSON maintenance decision.
```

The fine-tuned model should learn to:

- Read machine telemetry such as temperature, vibration, pressure, rpm, noise,
  oil quality, and hours since last service.
- Use technician notes and simulated error codes as extra context.
- Choose one normalized `recommended_action`.
- Choose one normalized `severity`.
- Return the answer in the exact JSON structure required by the system prompt.
- Produce practical maintenance steps instead of a generic chat response.

This is not a classifier demo where the model only predicts a label. It is
supervised fine-tuning of a causal chat LLM. Each training example teaches the
model the complete response style:

```text
system_prompt + user_prompt -> assistant_response
```

The before/after prompt checks prove whether fine-tuning changed behavior. The
same prompts are sent to the downloaded base model before training and to the
adapter model after training.

## What The Dataset Is About

The dataset is a provided, static CSV file:

```text
sessions/09_fine_tuning/demos/endtoend/datasets/machine_maintenance_ollama_instruction_dataset.csv
```

It contains hypothetical industrial machine maintenance examples. The examples
are fictional and safe for teaching, but they are structured like real training
records: each row has machine state, a prompt, and the target assistant answer.

The training script reads this CSV. It does not create or generate dataset rows
during training.

Dataset size:

```text
Total rows: 4,800
Actions: 6
Rows per action: 800
Training split: 4,320 rows
Validation split: 240 rows
Test split: 240 rows
```

This satisfies the requirement that the fine-tuning run trains on more than
2,000 examples. The actual default training split contains 4,320 examples.

## What The Model Is Trying To Learn

The model is learning a mapping from machine condition to a structured
maintenance decision.

Input:

```text
System instruction + user telemetry prompt
```

Output:

```json
{
  "recommended_action": "replace_filter",
  "severity": "medium",
  "confidence": 0.86,
  "root_cause_hypothesis": "Restricted intake filter flow is likely causing pressure and flow issues.",
  "immediate_steps": [
    "Reduce feed rate if pressure continues to fall.",
    "Inspect the filter housing and upstream intake path."
  ],
  "maintenance_plan": "Replace the intake filter and verify pressure recovery before returning to normal load.",
  "safety_note": "Do not bypass filter or pressure interlocks."
}
```

The key learning goal is consistency. After fine-tuning, the model should more
reliably return the expected JSON keys, use the allowed action labels, and write
maintenance-focused responses for telemetry prompts.

## Action Labels

The dataset is balanced across six `recommended_action` values.

| Action label | Rows | Meaning |
|---|---:|---|
| `normal_operation` | 800 | Machine appears healthy; continue normal production and monitoring. |
| `schedule_inspection` | 800 | Early warning signs exist; plan inspection without immediate shutdown. |
| `reduce_load` | 800 | Machine is stressed under load; reduce throughput or speed to stabilize it. |
| `replace_filter` | 800 | Pressure, flow, or intake evidence suggests a clogged or restricted filter. |
| `lubricate_bearings` | 800 | Vibration, noise, oil quality, or technician notes suggest bearing friction. |
| `emergency_shutdown` | 800 | Severe telemetry or alarm conditions require immediate safe shutdown. |

## Severity Labels

The `severity` column and the `severity` field inside `assistant_response`
describe urgency.

| Severity | Meaning |
|---|---|
| `low` | Healthy or minor condition; monitor or continue normal operation. |
| `medium` | Maintenance attention is needed, but controlled operation may continue. |
| `high` | Serious risk; immediate corrective action or load reduction is needed. |
| `critical` | Unsafe or severe condition; shut down or isolate the machine. |

## Column Reference

| Column | Used as model input? | Used as target/eval? | Meaning |
|---|---|---|---|
| `example_id` | No | Audit only | Unique identifier for the row. It helps trace a training, validation, or test example back to the CSV. |
| `machine_id` | Yes, inside prompts | Audit context | Fictional asset identifier such as `PKG-3973`. |
| `machine_type` | Yes, inside prompts | Audit context | Equipment category, for example packaging line, compressor, pump, conveyor, CNC machine, mixer, or press. |
| `plant_area` | Yes, inside prompts | Audit context | Fictional plant location where the machine is operating. |
| `shift` | Yes, inside prompts | Audit context | Operating shift such as morning, afternoon, night, or weekend. |
| `temperature_c` | Yes | Signal for action/severity | Machine temperature in Celsius. Higher values can indicate overload, friction, cooling issues, or unsafe operation. |
| `vibration_mm_s` | Yes | Signal for action/severity | Vibration velocity in millimeters per second. High vibration can suggest bearing wear, imbalance, or severe mechanical risk. |
| `pressure_bar` | Yes | Signal for action/severity | Operating pressure in bar. Abnormal low or high pressure can indicate filter blockage, flow restriction, or process stress. |
| `rpm` | Yes | Signal for action/severity | Machine speed or rotational load. This helps the model connect faults to load conditions. |
| `noise_db` | Yes | Signal for action/severity | Noise level in decibels. Elevated noise can support bearing, load, or emergency conditions. |
| `oil_quality_pct` | Yes | Signal for action/severity | Simulated oil or lubricant quality percentage. Low values can support lubrication or bearing-related recommendations. |
| `hours_since_service` | Yes | Signal for action/severity | Hours since the last service event. Higher values can support inspection or maintenance recommendations. |
| `error_code` | Yes | Signal for action/severity | Simulated machine status or fault code. This gives the prompt a recognizable operational clue. |
| `technician_note` | Yes | Signal for action/severity | Human observation from an operator or technician. This teaches the model to combine sensor values with field notes. |
| `sensor_summary` | Yes | Signal for action/severity | Short summary of the telemetry pattern, such as clogged filter pattern or severe multi-sensor alarm. |
| `machine_report` | Yes, indirectly | Source text for prompt | Human-readable summary of the structured telemetry fields. It makes the prompt easier to inspect and teach from. |
| `system_prompt` | Yes | Training instruction | Role and output contract. It tells the model to act as PlantOps-MaintenanceAI and return strict JSON only. |
| `user_prompt` | Yes | Main input | The actual user message given to the model during training and prompt checks. |
| `assistant_response` | No | Main target | The ideal assistant answer. During fine-tuning, the model learns to generate this style of JSON response. |
| `recommended_action` | No | Label and eval field | Normalized expected action. The script uses it to balance splits and to check generated held-out predictions. |
| `severity` | No | Label and eval field | Normalized urgency label. It should match the severity inside the target JSON response. |

## Input Columns Vs Target Columns

During fine-tuning, the script converts each CSV row into chat messages:

```text
system message:    system_prompt
user message:      user_prompt
assistant message: assistant_response
```

The model learns by predicting the assistant message tokens after seeing the
system and user messages. In simple terms:

```text
Question/context: system_prompt + user_prompt
Correct answer:   assistant_response
```

The other columns are still important because they make the dataset explainable.
They show where each prompt came from, what machine condition is represented,
and what normalized label should be found in the target response.

## Expected JSON Response Contract

Every `assistant_response` should be valid JSON with these fields:

| JSON field | Meaning |
|---|---|
| `recommended_action` | One of the six allowed action labels. |
| `severity` | Urgency level for the machine condition. |
| `confidence` | Decimal confidence score for the recommendation. |
| `root_cause_hypothesis` | Short explanation of the most likely cause. |
| `immediate_steps` | Practical actions to take right away. |
| `maintenance_plan` | Follow-up plan for maintenance or continued operation. |
| `safety_note` | Safety reminder matched to the condition. |

This contract is the main reason fine-tuning is useful in the demo. The desired
output is not only a correct answer, but a repeatable answer format.

## Example Training Row

Simplified example:

```text
machine_type: packaging line
temperature_c: 74.9
vibration_mm_s: 5.5
pressure_bar: 6.4
rpm: 1516
noise_db: 94.7
oil_quality_pct: 29.2
hours_since_service: 413
error_code: BEARING-201
technician_note: vibration increases at steady rpm even when load is unchanged
recommended_action: lubricate_bearings
severity: high
```

The matching target response teaches the model to return JSON recommending
`lubricate_bearings`, explain a bearing-friction hypothesis, give immediate
maintenance steps, and include a safety note.

## How To Verify The Dataset

From the repository root:

```bash
python - <<'PY'
import pandas as pd

path = "sessions/09_fine_tuning/demos/endtoend/datasets/machine_maintenance_ollama_instruction_dataset.csv"
df = pd.read_csv(path)

print("rows:", len(df))
print("columns:", list(df.columns))
print(df["recommended_action"].value_counts().sort_index())
print(df[["example_id", "machine_type", "recommended_action", "severity"]].head())
PY
```

Expected result:

```text
rows: 4800
800 examples for each recommended_action label
```

## What Success Looks Like

Before fine-tuning, the base model may answer in a generic way, omit required
JSON fields, or choose inconsistent action labels.

After fine-tuning, the adapter model should more often:

- Return parseable JSON.
- Use the exact required keys.
- Use one of the six allowed `recommended_action` values.
- Match the expected action on held-out examples more often than the base model.
- Give maintenance-specific steps that match the telemetry condition.

The files to inspect after a run are:

```text
output/local_05b_machine_assistant/prompt_checks/base_model_generations.jsonl
output/local_05b_machine_assistant/prompt_checks/fine_tuned_generations.jsonl
output/local_05b_machine_assistant/prompt_checks/before_after_comparison.json
output/local_05b_machine_assistant/metrics/test_action_accuracy.json
docs/latest_run_summary.md
```
