# 06. Retrieval Strategies

Retrieval decides which evidence the model sees. If retrieval misses the answer,
generation cannot reliably recover.

Good RAG systems often use multiple retrieval strategies together.

## Vector Retrieval

Vector retrieval searches by semantic similarity:

```
query -> embedding -> nearest chunks
```

Strengths:

- Handles paraphrases.
- Finds conceptually related passages.
- Works when query and document use different words.

Weaknesses:

- Can miss exact identifiers.
- Can retrieve broadly related but non-answering chunks.
- Depends heavily on chunking and embedding quality.

Example:

```
Query: "my instance cannot be reached over SSH"
Retrieved: "EC2 security groups control inbound access to instances."
```

## Keyword Retrieval

Keyword retrieval searches exact or near-exact terms.

Strengths:

- Error codes
- API names
- Resource IDs
- File paths
- Command names
- Exact product names

Weaknesses:

- Fails on paraphrases.
- Can over-rank documents with repeated terms.
- Does not understand meaning.

Example:

```
Query: "AccessDeniedException"
Retrieved: chunks containing "AccessDeniedException"
```

## Hybrid Retrieval

Hybrid retrieval combines vector and keyword results.

Common flow:

```
query
  -> vector top 20
  -> keyword top 20
  -> fuse rankings
  -> rerank top candidates
```

Hybrid search is a strong default for operational knowledge bases because
engineers ask both semantic and exact questions.

## Metadata Filtering

Metadata filtering narrows the search space.

Examples:

- Product: only EC2 docs
- Environment: production only
- Team: platform-owned docs
- Version: latest release only
- Access: only docs visible to this user
- Document type: runbooks only

Filtering can happen:

- Before vector search
- During vector database query
- After retrieval

For security-sensitive filters, do not rely only on post-filtering. Prevent
unauthorized content from entering candidates in the first place.

## Query Rewriting

User questions are often too vague for retrieval.

Original:

```
"Why is it failing?"
```

Rewritten with conversation context:

```
"Why is the Kubernetes payment-api pod failing with CrashLoopBackOff after deployment?"
```

Query rewriting can improve recall, but it adds risk. A bad rewrite can retrieve
the wrong documents. Log both original and rewritten queries.

## Multi-Query Retrieval

Instead of one query, generate several:

```
1. "EC2 instance cannot connect over SSH"
2. "security group inbound rule port 22"
3. "NACL blocking SSH traffic EC2"
```

Retrieve for each query, then fuse results.

This improves recall for broad questions. It costs more and needs deduplication.

## MMR: Maximal Marginal Relevance

MMR tries to balance relevance and diversity.

Without diversity, top results may be near-duplicates:

```
chunk 1: EC2 security group SSH rule
chunk 2: EC2 security group SSH rule repeated
chunk 3: EC2 security group SSH rule in another paragraph
```

MMR prefers:

```
chunk 1: security group
chunk 2: NACL
chunk 3: route table
```

Use MMR when duplicate chunks crowd out useful context.

## Parent-Child Retrieval

Small child chunks retrieve accurately. Larger parent chunks answer safely.

Flow:

```
retrieve child paragraphs -> map to parent section -> pass parent section
```

This is useful for policy, legal, and architecture docs where a paragraph alone
may omit important constraints.

## Thresholds

Top-k alone is not enough.

Bad:

```python
always_return_top_5()
```

Better:

```python
return chunks where score >= threshold, up to top_k
```

But thresholds must be calibrated per model and corpus. A score that is strong
for one embedding model may be weak for another.

## Retrieval Debugging Checklist

When a RAG answer is bad, inspect:

- Was the correct document indexed?
- Was it chunked into a retrievable unit?
- Did the chunk include enough context?
- Did metadata filters exclude it?
- Did vector search retrieve it in top 20?
- Did keyword search retrieve it?
- Did fusion demote it?
- Did reranking remove it?
- Did context budget truncate it?
- Did the generator ignore it?

## Key Takeaways

1. Use vector retrieval for meaning and keyword retrieval for exact terms.
2. Hybrid retrieval is a practical default for DevOps and cloud docs.
3. Metadata filters are part of correctness, security, and freshness.
4. Query rewriting and multi-query retrieval improve recall but need logging.
5. Always debug retrieved chunks before debugging the LLM answer.

