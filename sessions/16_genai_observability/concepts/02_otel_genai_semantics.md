# 02. OpenTelemetry GenAI Semantics

OpenTelemetry semantic conventions give teams a shared language for describing
GenAI spans and metrics.

## Attribute Mental Model

Use attributes to describe:

- System/provider
- Request model
- Operation name
- Token usage
- Tool names
- Response model
- Finish reason
- Error type

Example shape:

```json
{
  "span_name": "genai.chat",
  "attributes": {
    "gen_ai.system": "openai",
    "gen_ai.request.model": "example-model",
    "gen_ai.operation.name": "chat",
    "gen_ai.usage.input_tokens": 1200,
    "gen_ai.usage.output_tokens": 180
  }
}
```

## Trace Design

For an agent:

```text
root request
|-- context assembly
|-- retrieval query
|-- model call
|-- tool call
|-- model call
`-- final response
```

Each child span should keep correlation IDs so you can reconstruct the path.

## Redaction Strategy

Redact at the edge:

- Before logs
- Before traces leave the service boundary
- Before long-term storage
- Before sharing traces in bug reports

Keep stable IDs so operators can retrieve source data through approved systems
when needed.

## Key Takeaways

1. Semantic conventions make traces comparable across providers and apps.
2. Token and latency attributes are operational data.
3. Store references to sensitive evidence, not raw sensitive evidence.

