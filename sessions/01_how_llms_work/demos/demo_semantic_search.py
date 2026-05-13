#!/usr/bin/env python3
"""
Demo: Semantic Search over DevOps Runbooks
============================================
This demo shows how semantic search works in practice.
We embed a corpus of runbook titles and search it with queries phrased
differently from the original text — and watch semantic search succeed
where keyword search fails.

No API key required. Model downloads ~80MB on first run.

Usage:
    python demo_semantic_search.py
"""

import numpy as np
from sentence_transformers import SentenceTransformer


# ── Knowledge Base ─────────────────────────────────────────────────────────────
# A realistic corpus of runbook and KB article summaries.
# Notice the mix of K8s, AWS, databases, and networking topics.

KNOWLEDGE_BASE = [
    # Kubernetes
    "CrashLoopBackOff: Pod repeatedly starts and crashes. Check kubectl logs --previous for the crash reason.",
    "OOMKilled: Container exceeded memory limit and was killed by kernel. Increase memory limit or fix memory leak.",
    "ImagePullBackOff: Kubernetes cannot pull the container image. Verify image name, tag, and registry credentials.",
    "Node NotReady: Kubelet stopped reporting. Check node via SSH, inspect kubelet logs and disk space.",
    "Pending Pod: Pod stuck in Pending state. Check for insufficient resources or unsatisfiable node selectors.",
    "Pod Evicted: Pod was evicted due to resource pressure (disk or memory). Check node resource usage.",
    "HPA not scaling: Horizontal Pod Autoscaler not triggering. Verify metrics-server is running and CPU metrics are available.",
    # Networking
    "Nginx 502 Bad Gateway: Upstream service unavailable. Check backend pod health and nginx error logs.",
    "DNS resolution failure: Service name not resolving inside cluster. Check CoreDNS pods and ConfigMap.",
    "Service not reachable: ClusterIP service not responding. Verify pod selector labels match Service selector.",
    "Certificate expired: TLS certificate expired causing HTTPS failures. Renew via cert-manager or manually.",
    "Network policy blocking traffic: Pod cannot communicate. Check NetworkPolicy resources in the namespace.",
    # AWS / Cloud
    "S3 Access Denied: IAM role lacks s3:GetObject permission. Check role policy and bucket policy.",
    "EC2 instance unreachable: Security group or NACL blocking SSH/connection. Verify inbound rules on port 22.",
    "RDS connection timeout: Database security group not allowing connection from application subnet. Update inbound rules.",
    "Lambda cold start latency: Function initializing slowly. Consider provisioned concurrency or reducing package size.",
    "AWS Cost spike: Unexpected cost increase. Check Cost Explorer, look for NAT gateway data transfer or EC2 instance type changes.",
    # Databases
    "PostgreSQL connection pool exhausted: Max connections reached. Use PgBouncer connection pooler or increase max_connections.",
    "PostgreSQL slow queries: Long-running queries blocking others. Use EXPLAIN ANALYZE and check for missing indexes.",
    "Redis OOM: Redis out of memory. Set maxmemory policy, check for key expiry configuration.",
    "MongoDB replication lag: Secondary replica falling behind primary. Check network bandwidth and disk I/O on secondaries.",
    # CI/CD
    "Pipeline failing on Docker build: Build context too large or base image unavailable. Use .dockerignore and verify registry.",
    "Terraform state lock: Previous Terraform run did not release lock. Use terraform force-unlock with the lock ID.",
    "Helm deployment failed: Chart values incorrect or resource conflict. Run helm status and check events in namespace.",
    "GitHub Actions runner out of disk: Self-hosted runner disk full. Clean up Docker images and workspace artifacts.",
    # Application
    "High CPU throttling: Container hitting CPU limit. Increase CPU limit or optimize application code.",
    "Memory leak detected: Container memory grows unboundedly. Profile application heap and check for unclosed connections.",
    "gRPC deadline exceeded: Service call timing out. Check downstream service latency and increase deadline budget.",
    "Graceful shutdown not working: Container not handling SIGTERM. Implement signal handler to drain connections before exit.",
]


def load_model() -> SentenceTransformer:
    print("Loading embedding model (downloads ~80MB on first run)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print(f"  Model loaded. Embedding dimension: {model.get_sentence_embedding_dimension()}")
    return model


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def semantic_search(
    query: str,
    corpus: list[str],
    corpus_embeddings: np.ndarray,
    model: SentenceTransformer,
    top_k: int = 3,
) -> list[tuple[str, float]]:
    """Return top_k (text, score) pairs most similar to query."""
    query_vec = model.encode([query])[0]
    scores = [
        (corpus[i], cosine_similarity(query_vec, corpus_embeddings[i]))
        for i in range(len(corpus))
    ]
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


def keyword_search(query: str, corpus: list[str], top_k: int = 3) -> list[tuple[str, int]]:
    """Simple keyword overlap search. Returns (text, overlap_count) pairs."""
    query_words = set(query.lower().split())
    scored = []
    for text in corpus:
        words = set(text.lower().split())
        overlap = len(query_words & words)
        if overlap > 0:
            scored.append((text, overlap))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def display_results(
    query: str,
    semantic_results: list[tuple[str, float]],
    keyword_results: list[tuple[str, int]],
) -> None:
    print(f"\n{'─' * 70}")
    print(f"Query: \"{query}\"")
    print(f"{'─' * 70}")

    print("\n  SEMANTIC SEARCH (finds by meaning):")
    if semantic_results:
        for i, (text, score) in enumerate(semantic_results, 1):
            bar = "█" * int(score * 20)
            short_text = text[:65] + "..." if len(text) > 68 else text
            print(f"  {i}. [{score:.3f}] {bar}")
            print(f"        {short_text}")
    else:
        print("     (no results)")

    print("\n  KEYWORD SEARCH (finds by word match):")
    if keyword_results:
        for i, (text, overlap) in enumerate(keyword_results, 1):
            short_text = text[:65] + "..." if len(text) > 68 else text
            print(f"  {i}. [{overlap} word overlap] {short_text}")
    else:
        print("     (no results — none of the query words appear in any document)")


def main() -> None:
    print("\n" + "=" * 70)
    print("  DEMO: Semantic Search over DevOps Runbooks")
    print("=" * 70)
    print(f"\n  Corpus: {len(KNOWLEDGE_BASE)} runbook/KB articles")

    model = load_model()

    print("\nComputing corpus embeddings...")
    corpus_embeddings = model.encode(KNOWLEDGE_BASE)
    print(f"  Done. Shape: {corpus_embeddings.shape}")

    # ── Search examples ────────────────────────────────────────────────────────
    # These queries are intentionally phrased differently from the KB articles.
    # Semantic search should still find the right answer.
    # Keyword search will often fail completely.

    queries = [
        # Queries where semantic wins clearly
        "my container keeps dying because it runs out of RAM",        # → OOMKilled
        "kubernetes pod wont start because it cant download the image", # → ImagePullBackOff
        "website is returning 502 from the load balancer",             # → Nginx 502
        "IaC provisioning tool reports the state file is locked",      # → Terraform lock
        "postgres has no more available connections",                  # → Connection pool
        "AWS IAM permissions are stopping S3 reads",                  # → S3 Access Denied
        "TLS handshake failing, certificate no longer valid",         # → Certificate expired
        "service call is exceeding the timeout deadline",             # → gRPC deadline
        # Queries where both might work (good baseline)
        "pod evicted from node",                                       # → Pod Evicted
        "memory leak in container",                                    # → Memory leak
    ]

    for query in queries:
        sem_results = semantic_search(query, KNOWLEDGE_BASE, corpus_embeddings, model, top_k=2)
        kw_results = keyword_search(query, KNOWLEDGE_BASE, top_k=2)
        display_results(query, sem_results, kw_results)

    # ── Summary ────────────────────────────────────────────────────────────────
    print("\n\n" + "=" * 70)
    print("  KEY OBSERVATION")
    print("=" * 70)
    print("""
  For queries phrased differently from the corpus vocabulary:
  - Semantic search surfaces the correct document even without word overlap
  - Keyword search returns 0 results or wrong results

  This is why production search systems for runbooks, documentation,
  and incident knowledge use embeddings rather than full-text search.

  In Session 07 (RAG & Vector Databases), you'll build a full
  retrieval-augmented generation pipeline on top of this foundation.
""")


if __name__ == "__main__":
    main()
