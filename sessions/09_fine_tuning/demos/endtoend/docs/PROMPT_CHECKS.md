# Prompt Checks

This document explains how to check whether fine-tuning changed the model's
behavior.

## Why Prompt Checks Matter

Fine-tuning should make the model better at the target behavior. For this demo,
the target behavior is:

```text
Read machine telemetry and return strict JSON with a maintenance decision.
```

The script uses the same fixed prompts twice:

1. Before fine-tuning, using the downloaded base model plus untrained LoRA adapters.
2. After fine-tuning, using the trained LoRA adapters.

This lets students compare before and after behavior directly.

## Where The Prompts Are

The sample prompts are written here:

```text
sessions/09_fine_tuning/demos/endtoend/docs/sample_prompts.md
```

They are included with the demo so students can inspect the before/after
prompts before starting the EC2 training run.

## Main Sample Prompt

System prompt:

```text
You are PlantOps-MaintenanceAI, a cautious maintenance assistant for industrial machines. Return strict JSON only. The JSON must contain recommended_action, severity, confidence, root_cause_hypothesis, immediate_steps, maintenance_plan, and safety_note.
```

User prompt:

```text
Analyze this machine telemetry report and return the maintenance decision as strict JSON.

Machine: CNC-9001
Machine type: CNC mill
Plant area: fabrication
Shift: night
Temperature C: 118.2
Vibration mm/s: 10.9
Pressure bar: 12.1
RPM: 2210
Noise dB: 107.4
Oil quality percent: 12.0
Hours since service: 730
Error code: CRIT-900
Technician note: critical alarm is active and visible shaking was reported
Sensor summary: severe multi-sensor alarm
```

Expected fine-tuned answer should contain:

```json
{
  "recommended_action": "emergency_shutdown"
}
```

The full response should also include:

```text
severity
confidence
root_cause_hypothesis
immediate_steps
maintenance_plan
safety_note
```

## Before Fine-Tuning Output

The base model generations are written here:

```text
sessions/09_fine_tuning/demos/endtoend/output/local_05b_machine_assistant/prompt_checks/base_model_generations.jsonl
```

The base model may:

- return valid JSON but use the wrong schema
- omit required keys
- give a generic explanation instead of a maintenance decision
- choose the wrong `recommended_action`

That is useful. It shows why fine-tuning is needed.

## After Fine-Tuning Output

The fine-tuned generations are written here:

```text
sessions/09_fine_tuning/demos/endtoend/output/local_05b_machine_assistant/prompt_checks/fine_tuned_generations.jsonl
```

The fine-tuned model should be more likely to:

- return strict JSON
- include all required keys
- choose the expected `recommended_action`
- use the machine-maintenance wording taught in the dataset

## Before/After Comparison File

The compact comparison is written here:

```text
sessions/09_fine_tuning/demos/endtoend/output/local_05b_machine_assistant/prompt_checks/before_after_comparison.json
```

It contains entries like:

```json
{
  "example_id": "prompt-check-001",
  "expected_action": "emergency_shutdown",
  "base_model_action": null,
  "fine_tuned_action": "emergency_shutdown",
  "base_model_correct": false,
  "fine_tuned_correct": true
}
```

The exact result may vary, but the teaching goal is clear: the post-training
response should be more consistent with the schema and expected action.

## Manual Check After Training

After training, open:

```text
docs/sample_prompts.md
```

Then compare:

```text
output/local_05b_machine_assistant/prompt_checks/base_model_generations.jsonl
output/local_05b_machine_assistant/prompt_checks/fine_tuned_generations.jsonl
```

You should see the fine-tuned model behave more like the training examples.
