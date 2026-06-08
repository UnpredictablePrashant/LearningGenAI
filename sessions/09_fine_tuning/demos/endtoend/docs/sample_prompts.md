# Fine-Tuning Prompt Checks

Use these exact prompts before and after fine-tuning.
The expected action is shown above each prompt for instructor reference.

## Prompt 1: emergency_shutdown

Expected recommended_action: `emergency_shutdown`

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

## Prompt 2: replace_filter

Expected recommended_action: `replace_filter`

System prompt:

```text
You are PlantOps-MaintenanceAI, a cautious maintenance assistant for industrial machines. Return strict JSON only. The JSON must contain recommended_action, severity, confidence, root_cause_hypothesis, immediate_steps, maintenance_plan, and safety_note.
```

User prompt:

```text
Analyze this machine telemetry report and return the maintenance decision as strict JSON.

Machine: PMP-8102
Machine type: industrial pump
Plant area: utilities
Shift: morning
Temperature C: 70.4
Vibration mm/s: 2.0
Pressure bar: 3.1
RPM: 1320
Noise dB: 69.2
Oil quality percent: 61.0
Hours since service: 410
Error code: FILTER-401
Technician note: inlet pressure is low and flow is restricted
Sensor summary: clogged filter pattern
```

## Prompt 3: lubricate_bearings

Expected recommended_action: `lubricate_bearings`

System prompt:

```text
You are PlantOps-MaintenanceAI, a cautious maintenance assistant for industrial machines. Return strict JSON only. The JSON must contain recommended_action, severity, confidence, root_cause_hypothesis, immediate_steps, maintenance_plan, and safety_note.
```

User prompt:

```text
Analyze this machine telemetry report and return the maintenance decision as strict JSON.

Machine: CNV-7203
Machine type: conveyor drive
Plant area: line 2
Shift: afternoon
Temperature C: 84.8
Vibration mm/s: 7.2
Pressure bar: 6.2
RPM: 1440
Noise dB: 91.3
Oil quality percent: 27.0
Hours since service: 560
Error code: LUBE-510
Technician note: operator reports a dry squeal during startup and shutdown
Sensor summary: dry bearing signature
```

## Prompt 4: reduce_load

Expected recommended_action: `reduce_load`

System prompt:

```text
You are PlantOps-MaintenanceAI, a cautious maintenance assistant for industrial machines. Return strict JSON only. The JSON must contain recommended_action, severity, confidence, root_cause_hypothesis, immediate_steps, maintenance_plan, and safety_note.
```

User prompt:

```text
Analyze this machine telemetry report and return the maintenance decision as strict JSON.

Machine: PKG-6304
Machine type: packaging line
Plant area: line 1
Shift: night
Temperature C: 91.5
Vibration mm/s: 4.6
Pressure bar: 8.7
RPM: 1780
Noise dB: 81.0
Oil quality percent: 55.0
Hours since service: 250
Error code: LOAD-330
Technician note: machine recovers when the feed rate is lowered
Sensor summary: temperature rising under load
```

## Prompt 5: schedule_inspection

Expected recommended_action: `schedule_inspection`

System prompt:

```text
You are PlantOps-MaintenanceAI, a cautious maintenance assistant for industrial machines. Return strict JSON only. The JSON must contain recommended_action, severity, confidence, root_cause_hypothesis, immediate_steps, maintenance_plan, and safety_note.
```

User prompt:

```text
Analyze this machine telemetry report and return the maintenance decision as strict JSON.

Machine: MLD-5405
Machine type: injection molder
Plant area: quality lab
Shift: morning
Temperature C: 76.1
Vibration mm/s: 3.4
Pressure bar: 6.3
RPM: 1260
Noise dB: 72.5
Oil quality percent: 58.0
Hours since service: 310
Error code: DRIFT-305
Technician note: minor drift was noticed across two shifts but production is continuing
Sensor summary: early warning trend
```

## Prompt 6: normal_operation

Expected recommended_action: `normal_operation`

System prompt:

```text
You are PlantOps-MaintenanceAI, a cautious maintenance assistant for industrial machines. Return strict JSON only. The JSON must contain recommended_action, severity, confidence, root_cause_hypothesis, immediate_steps, maintenance_plan, and safety_note.
```

User prompt:

```text
Analyze this machine telemetry report and return the maintenance decision as strict JSON.

Machine: CMP-4506
Machine type: compressor
Plant area: warehouse
Shift: afternoon
Temperature C: 56.4
Vibration mm/s: 1.5
Pressure bar: 6.4
RPM: 1390
Noise dB: 64.8
Oil quality percent: 88.0
Hours since service: 96
Error code: OK
Technician note: routine production is continuing with no abnormal sound reported
Sensor summary: healthy telemetry profile
```
