# 01. Multimodal Inputs

Multimodal systems use more than text. They may inspect screenshots, invoices,
diagrams, logs as images, audio, speech, or mixed documents.

## Input Types

| Input | Useful For | Important Metadata |
|-------|------------|--------------------|
| Image | Screenshots, diagrams, receipts | source, timestamp, resolution |
| PDF/page image | Forms, scanned docs, runbooks | page number, doc ID, access policy |
| Audio | Calls, meetings, voice commands | speaker, language, consent |
| Transcript | Searchable audio-derived text | confidence, timestamps |
| Video frames | Visual process evidence | frame time, sampling policy |

## Design Rules

- Preserve source metadata.
- Keep raw artifacts separate from extracted text.
- Track confidence for OCR/transcription.
- Use citations for document/image answers.
- Do not store voice or image data longer than policy allows.
- Redact sensitive content before durable logging.

## Failure Modes

| Failure | Example |
|---------|---------|
| OCR error | `prod` read as `prd` |
| Missing visual context | A cropped screenshot hides the warning |
| Audio hallucination | Transcript guesses a word under noise |
| Speaker confusion | Action attributed to the wrong speaker |
| Untrusted document instruction | A PDF tells the model to ignore policy |

## Key Takeaways

1. Multimodal inputs need provenance and confidence metadata.
2. Extracted text is not the same thing as source truth.
3. Safety policy must cover the artifact, the extraction, and the final answer.

