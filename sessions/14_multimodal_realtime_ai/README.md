# Session 14: Multimodal and Realtime AI

Build a practical mental model for applications that use text, images, audio,
speech, and low-latency event streams.

## DevOps Analogy

| Multimodal/Realtime Concept | DevOps Equivalent |
|----------------------------|-------------------|
| Audio stream | Log stream / websocket feed |
| Transcript delta | Incremental event |
| Voice activity detection | Idle timeout / connection state |
| Image input | Binary artifact with metadata |
| Tool call during voice | Interactive runbook action |
| Realtime session | Stateful connection |
| Turn-taking | Protocol state machine |

## What You'll Learn

- Decide when text-only is not enough
- Model image, document, audio, and transcript inputs
- Understand realtime sessions, event streams, and turn-taking
- Handle partial transcripts and final transcripts differently
- Design tool calls that can happen during an audio interaction
- Budget latency and cost for realtime experiences
- Add safety boundaries for voice agents and image/document analysis

## Official References

- [OpenAI images and vision](https://developers.openai.com/api/docs/guides/images-vision)
- [OpenAI audio and speech](https://developers.openai.com/api/docs/guides/audio)
- [OpenAI Realtime API](https://developers.openai.com/api/docs/guides/realtime)
- [OpenAI realtime prompting guide](https://developers.openai.com/api/docs/guides/realtime-models-prompting)
- [OpenAI voice agents](https://developers.openai.com/api/docs/guides/voice-agents)

## Prerequisites

```bash
pip install -r ../../requirements.txt

# No API key required for the core lab.
# Optional realtime demos can use provider APIs later.
```

Recommended previous sessions:

- Session 01 for tokens and context limits
- Session 03 for streaming basics
- Session 04 for tool calls
- Session 10 for evals

## Session Structure

```text
14_multimodal_realtime_ai/
|-- concepts/
|   |-- 01_multimodal_inputs.md
|   `-- 02_realtime_sessions.md
|-- labs/
|   `-- lab01_realtime_event_flow/
`-- demos/
    `-- demo_realtime_event_flow.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_realtime_event_flow | Process realtime events | transcript deltas, final messages, tool triggers |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_realtime_event_flow.py` | A tiny event loop for transcript and tool-call events |

## Quick Start

```bash
cd sessions/14_multimodal_realtime_ai

cat concepts/01_multimodal_inputs.md
cat concepts/02_realtime_sessions.md

python demos/demo_realtime_event_flow.py
python labs/lab01_realtime_event_flow/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 35 min |
| Lab | 40 min |
| Demo | 10 min |
| **Total** | **~85 min** |
