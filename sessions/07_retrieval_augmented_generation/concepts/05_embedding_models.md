# 05. Embedding Models

Embeddings turn text into vectors so retrieval can search by meaning instead of
only exact words.

This session uses two categories:

- Local embedding models for learning and offline demos
- API embedding models for production-quality managed systems

## What an Embedding Model Must Do

For RAG, a useful embedding model should place questions near chunks that answer
them.

Example:

```
Query: "How do I fix a pod that keeps restarting?"
Should be near: "CrashLoopBackOff means the container repeatedly starts and exits."
Should be far from: "S3 bucket policy denies GetObject."
```

The model is judged by retrieval quality, not by how impressive the vector looks.

## Local Models

Local models are useful for:

- Teaching
- Offline labs
- Prototyping
- Privacy-sensitive experiments
- Cheap batch indexing

Practical defaults:

| Model | Dimensions | Strength | Tradeoff |
|-------|------------|----------|----------|
| `sentence-transformers/all-MiniLM-L6-v2` | 384 | Fast, small, CPU-friendly | Lower quality than larger models |
| `sentence-transformers/all-mpnet-base-v2` | 768 | Better semantic quality | Larger and slower |
| `sentence-transformers/multi-qa-MiniLM-L6-cos-v1` | 384 | Tuned for question-answer retrieval | Narrower general use |

For this course, `all-MiniLM-L6-v2` is a good default because it is small, fast,
and works on normal laptops.

## API Models

API embedding models are useful when:

- You need stronger retrieval quality.
- You do not want to host embedding infrastructure.
- You need multilingual quality.
- You need consistent managed availability.
- You can send the text to the provider under your data policy.

OpenAI's current embedding documentation lists:

| Model | Dimensions | Practical Use |
|-------|------------|---------------|
| `text-embedding-3-small` | 1536 | Good default for cost-sensitive production RAG |
| `text-embedding-3-large` | 3072 | Higher quality when retrieval quality matters more than cost |

Official references:

- [OpenAI embeddings guide](https://platform.openai.com/docs/guides/embeddings)
- [text-embedding-3-small](https://platform.openai.com/docs/models/text-embedding-3-small)
- [text-embedding-3-large](https://platform.openai.com/docs/models/text-embedding-3-large)

## Which Model Is Good?

There is no universal best embedding model. Use this decision rule:

| Situation | Good Starting Choice |
|-----------|----------------------|
| Course lab, no API key | `all-MiniLM-L6-v2` |
| Local prototype with better quality | `all-mpnet-base-v2` |
| Question-answer retrieval, local | `multi-qa-MiniLM-L6-cos-v1` |
| Production, cost-sensitive | `text-embedding-3-small` |
| Production, quality-sensitive | `text-embedding-3-large` |
| Multilingual or specialized domain | Benchmark several models on your own corpus |

Choose by evaluation:

1. Create 30-100 realistic user questions.
2. Label the chunks that should answer each question.
3. Index the same corpus with candidate models.
4. Measure recall@k and MRR.
5. Inspect failures manually.
6. Choose the cheapest model that meets quality targets.

## Normalization

Many sentence-transformer examples return non-normalized vectors by default.
When using cosine similarity, normalize vectors:

```python
embeddings = model.encode(texts, normalize_embeddings=True)
```

If vectors are normalized, dot product equals cosine similarity. This is faster
and less error-prone.

## Embedding Input Text

The text passed into the embedding model matters.

Weak input:

```
Burst credits are spent when CPU usage exceeds baseline.
```

Stronger input:

```
AWS EC2 Guide > Instance Types > Burstable Instances
Burst credits are spent when CPU usage exceeds baseline.
```

The heading gives the embedding model context. This is especially useful when the
chunk is short.

## Batching

Embedding documents one at a time is slow. Batch them:

```python
embeddings = model.encode(
    texts,
    batch_size=64,
    show_progress_bar=True,
    normalize_embeddings=True,
)
```

Batch size depends on hardware and model. If you run out of memory, reduce it.

## Reindexing

Changing embedding model means reindexing. Do not mix vectors from different
models in one collection unless the database explicitly supports separate vector
fields and your retrieval code knows which field to query.

Store embedding metadata:

```json
{
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "embedding_dimension": 384,
  "normalized": true,
  "indexed_at": "2026-05-12T08:00:00Z"
}
```

## Domain Vocabulary

Embedding models can struggle with:

- Internal service names
- Ticket IDs
- Error codes
- Acronyms
- Product-specific terms
- Code identifiers

Use hybrid retrieval for these. Keyword search often catches identifiers better
than semantic search.

## Key Takeaways

1. Pick embedding models by measured retrieval quality, not by popularity.
2. `all-MiniLM-L6-v2` is a strong course default.
3. `text-embedding-3-small` is a practical API default; `text-embedding-3-large`
   is the higher-quality OpenAI embedding option.
4. Normalize embeddings for cosine similarity.
5. Changing embedding model requires reindexing.

