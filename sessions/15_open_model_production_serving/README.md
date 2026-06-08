# Session 15: Open Model Production Serving

Move beyond local Ollama demos and learn what changes when open-weight models
must serve production traffic with GPUs, concurrency, batching, observability,
and rollback.

## DevOps Analogy

| Serving Concept | DevOps Equivalent |
|-----------------|-------------------|
| Model server | Application deployment |
| GPU memory | Pod memory limit, but expensive |
| KV cache | Runtime cache/state |
| Continuous batching | Request coalescing |
| Quantization | Smaller image/runtime footprint |
| OpenAI-compatible endpoint | Stable API contract |
| Adapter serving | Runtime plugin or sidecar |
| Autoscaling | HPA/KEDA with GPU constraints |

## What You'll Learn

- Compare Ollama, llama.cpp server, vLLM, SGLang, and Triton-style serving
- Estimate memory for weights, KV cache, and concurrency
- Understand batching, streaming, throughput, and tail latency tradeoffs
- Route OpenAI-compatible clients to local or hosted model servers
- Plan Kubernetes deployment patterns for GPU-backed inference
- Add model versioning, rollback, and eval gates

## Official References

- [vLLM documentation](https://docs.vllm.ai/en/latest/)
- [llama.cpp server documentation](https://www.mintlify.com/ggml-org/llama.cpp/inference/server)
- [NVIDIA Triton TensorRT-LLM Kubernetes autoscaling tutorial](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2550/user-guide/docs/tutorials/Deployment/Kubernetes/TensorRT-LLM_Autoscaling_and_Load_Balancing/README.html)
- [OpenAI-compatible provider pattern from Session 04](../04_tool_calling_function_calling/)

## Prerequisites

```bash
pip install -r ../../requirements.txt

# No GPU required for the core lab.
# The lab is capacity-planning math only.
```

Recommended previous sessions:

- Session 03 for local model basics
- Session 04 for OpenAI-compatible API routing
- Session 09 for LoRA/QLoRA and model artifacts
- Session 11 for production budgets

## Session Structure

```text
15_open_model_production_serving/
|-- concepts/
|   |-- 01_serving_stacks.md
|   `-- 02_capacity_and_kubernetes.md
|-- labs/
|   `-- lab01_capacity_planning/
`-- demos/
    `-- demo_openai_compatible_routing.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_capacity_planning | Estimate serving capacity | weights, KV cache, concurrency, GPU fit |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_openai_compatible_routing.py` | Route local and hosted models behind one API shape |

## Quick Start

```bash
cd sessions/15_open_model_production_serving

cat concepts/01_serving_stacks.md
cat concepts/02_capacity_and_kubernetes.md

python demos/demo_openai_compatible_routing.py
python labs/lab01_capacity_planning/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 45 min |
| Lab | 45 min |
| Demo | 10 min |
| **Total** | **~100 min** |

