# 02. RAG Math

RAG looks like an application architecture, but the important operations are
mathematical:

- Text becomes vectors.
- Queries and chunks are compared by distance or similarity.
- Search results are ranked.
- Multiple rankings can be fused.
- Rerankers score query-document pairs.
- Context budgets constrain how much evidence can fit.

You do not need advanced math to build RAG, but you do need the core ideas.

## Embeddings as Vectors

An embedding model converts text into a vector:

```python
"EC2 instances are virtual servers"
-> [0.012, -0.044, 0.118, ..., 0.031]
```

If the model outputs 1536 dimensions, each text is a point in a 1536-dimensional
space. Similar meanings should land near each other.

The individual numbers are not human-readable features. The full pattern matters.

## Dot Product

For two vectors `a` and `b`, the dot product is:

```
dot(a, b) = a1*b1 + a2*b2 + ... + an*bn
```

If vectors point in a similar direction, the dot product is high. If they point
in unrelated directions, it is lower.

## Vector Norm

The L2 norm is the vector length:

```
||a|| = sqrt(a1^2 + a2^2 + ... + an^2)
```

Normalizing a vector means dividing every value by its length:

```
a_normalized = a / ||a||
```

After normalization, the vector length is 1. This makes comparison focus on
direction rather than magnitude.

## Cosine Similarity

Cosine similarity measures the angle between two vectors:

```
cosine(a, b) = dot(a, b) / (||a|| * ||b||)
```

If both vectors are already normalized, cosine similarity becomes:

```
cosine(a, b) = dot(a, b)
```

That is why many embedding pipelines store normalized vectors.

Typical interpretation:

| Score | Meaning |
|-------|---------|
| 0.85+ | Very similar |
| 0.70-0.85 | Related |
| 0.50-0.70 | Maybe related, inspect |
| below 0.50 | Often weak |

These numbers are not universal. They vary by model, domain, chunk size, and
index configuration. Always calibrate on your own documents.

## Distance vs Similarity

Some vector databases return similarity; others return distance.

- Similarity: higher is better.
- Distance: lower is better.

For cosine distance:

```
cosine_distance = 1 - cosine_similarity
```

This causes common bugs. If a database returns distance and your code sorts
largest first, the worst chunks can appear at the top.

## Keyword Retrieval Math

Vector search is not the only retrieval method. Keyword retrieval still matters,
especially for exact names:

- Error codes
- API names
- Incident IDs
- Kubernetes resource names
- File paths
- Product SKUs

BM25 is a common keyword ranking algorithm. The intuition:

- Terms that appear in the query help.
- Rare terms help more than common terms.
- Repeating a term helps, but with diminishing returns.
- Very long documents are normalized so they do not win only by length.

A simplified scoring idea:

```
score(query, document) = sum(term_importance * term_frequency_adjustment)
```

BM25 is often paired with vector search in hybrid RAG.

## Reciprocal Rank Fusion

Hybrid retrieval combines multiple result lists. A simple and effective method is
reciprocal rank fusion (RRF).

For each document:

```
RRF score = sum(1 / (k + rank_in_each_list))
```

Common `k` values are around 60. The exact value is less important than the idea:
documents that rank well in multiple systems move up.

Example:

| Chunk | Vector Rank | Keyword Rank | RRF Intuition |
|-------|-------------|--------------|---------------|
| A | 1 | 9 | strong semantic match |
| B | 4 | 1 | exact keyword match |
| C | 2 | missing | semantic only |
| D | missing | 2 | keyword only |

RRF can keep A and B high without requiring score normalization between vector
similarity and keyword scores.

## Reranker Math

A bi-encoder embedding model encodes query and chunk separately:

```
embed(query) -> q
embed(chunk) -> c
similarity(q, c)
```

This is fast because chunk embeddings are precomputed.

A cross-encoder reranker reads the query and chunk together:

```
reranker("[query] [chunk]") -> relevance score
```

It is slower, but more accurate, because it can inspect exact interactions:

- Does this chunk answer this exact question?
- Is the answer only adjacent but not present?
- Is a term used with the same meaning?
- Is this a definition, example, limitation, or unrelated mention?

Common production flow:

```
retrieve top 20 to 100 candidates -> rerank -> keep top 3 to 8 chunks
```

## Context Budget Math

Every model call has a token budget.

If the model context window is `C`, reserve space for:

- System instructions
- User question
- Tool or conversation state
- Retrieved chunks
- The model's answer

Simple budget:

```
available_for_context =
    model_context_window
    - system_tokens
    - user_question_tokens
    - conversation_tokens
    - expected_answer_tokens
    - safety_margin
```

If available context is 6000 tokens and each chunk is about 500 tokens, you can
send about 12 chunks before citations and metadata. In practice, fewer high
quality chunks usually beat many noisy chunks.

## Chunk Size Tradeoff

Chunk size changes the retrieval geometry.

Small chunks:

- More precise
- Cheaper to inject
- Easier to cite
- Risk losing context

Large chunks:

- Preserve context
- Better for narrative explanations
- Can dilute the exact answer
- More expensive

Overlap helps preserve boundary context:

```
chunk_size = 800 tokens
overlap = 120 tokens
stride = 680 tokens
```

More overlap means more vectors, more storage, and more duplicate retrieval.

## Key Takeaways

1. Normalize embeddings when you want cosine similarity through dot product.
2. Confirm whether your vector database returns distance or similarity.
3. Hybrid search combines semantic recall with exact keyword precision.
4. Reranking is slower but often improves final answer quality.
5. Context budget forces retrieval discipline.

