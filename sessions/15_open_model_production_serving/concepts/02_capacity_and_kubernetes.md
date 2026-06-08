# 02. Capacity and Kubernetes

GPU inference capacity planning has different bottlenecks than normal web apps.

## Memory Components

| Component | Meaning |
|-----------|---------|
| Weights | The model parameters loaded into VRAM |
| KV cache | Runtime attention cache for active requests |
| Activations/overhead | Framework and temporary memory |
| Adapters | LoRA or other adapter weights |

## Throughput vs Latency

Batching improves throughput, but can increase waiting time. Streaming improves
user-perceived latency, but does not make generation free.

Measure:

- Time to first token
- Tokens per second
- Requests per second
- p95/p99 latency
- Queue depth
- GPU utilization
- KV cache pressure

## Kubernetes Pattern

Start simple:

```text
ingress -> model gateway -> model server deployment -> GPU node pool
                         -> metrics/traces/logs
```

Add:

- Node labels and taints for GPU pools
- Requests/limits for GPU resources
- Readiness checks that load the model
- Separate canary deployment for new model versions
- Queue-depth or latency-based autoscaling
- Graceful draining before pod termination

## Key Takeaways

1. GPU autoscaling is slower and more constrained than CPU autoscaling.
2. Queue depth and time-to-first-token matter more than raw request count.
3. Canary and rollback plans are mandatory for model artifact changes.

