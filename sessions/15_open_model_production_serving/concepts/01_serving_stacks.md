# 01. Serving Stacks

Running a local model for yourself is different from serving an open model to a
team or product.

## Common Stacks

| Stack | Good For | Notes |
|-------|----------|-------|
| Ollama | Developer laptops, simple local APIs | Easiest path for learning |
| llama.cpp server | CPU/GPU GGUF serving, edge boxes | Lightweight and OpenAI-compatible |
| vLLM | High-throughput GPU serving | Continuous batching, paged KV cache |
| SGLang | Structured generation and serving | Useful for agent/tool workloads |
| Triton/TensorRT-LLM | Enterprise GPU inference | Strong Kubernetes and NVIDIA ecosystem |

## OpenAI-Compatible Contract

Many local servers expose endpoints shaped like:

```text
/v1/chat/completions
/v1/completions
/v1/embeddings
```

That lets application code use one client interface while changing the base URL.
Compatibility still needs testing. Streaming, tool calling, structured outputs,
and error shapes may vary.

## Serving Questions

- Which model and quantization?
- How much VRAM do weights require?
- How much KV cache is needed for the context window and concurrency?
- Is streaming required?
- Are adapters loaded dynamically or merged?
- How will you route fallback traffic?
- Which eval suite gates model upgrades?

## Key Takeaways

1. OpenAI-compatible does not mean feature-identical.
2. Serving capacity is mostly memory plus concurrency math.
3. Eval and rollback are required when changing model artifacts.

