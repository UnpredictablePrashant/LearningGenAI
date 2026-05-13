# 04. Chunking Strategies

Chunking is one of the highest-impact RAG decisions. A chunk is the unit that
gets embedded, retrieved, reranked, cited, and sent to the model.

Bad chunks create bad retrieval.

## The Chunking Goal

A good chunk should:

- Contain one coherent idea or section
- Be large enough to carry meaning
- Be small enough to retrieve precisely
- Preserve source and heading metadata
- Fit into the final context budget
- Support useful citations

The goal is not "make every chunk exactly 500 tokens." The goal is retrievable
evidence.

## Fixed-Size Chunking

Fixed-size chunking splits every `N` characters or tokens.

Example:

```
chunk_size = 800 tokens
overlap = 120 tokens
```

Advantages:

- Simple
- Predictable
- Easy to implement
- Works as a baseline

Problems:

- Can split in the middle of a sentence
- Can separate a heading from its content
- Can mix unrelated sections
- Ignores document structure

Use fixed-size chunking as a baseline, not the final strategy for important
documents.

## Recursive Chunking

Recursive chunking tries larger natural boundaries first, then falls back:

```
section break -> paragraph -> sentence -> word -> character
```

This is the strategy used by many text splitters. It is a practical default for
mixed prose documents.

The notebook uses a token-aware recursive splitter with separators:

```python
separators = ["\n\n", "\n", ". ", " ", ""]
```

This means:

1. Prefer paragraph boundaries.
2. If too large, try line boundaries.
3. If still too large, try sentence boundaries.
4. If still too large, split on spaces.
5. Last resort: split raw characters.

## Heading-Aware Chunking

Heading-aware chunking tracks document structure:

```
Document Title > Section Heading > Subheading
```

Then each chunk stores that heading path as metadata.

Benefits:

- Better citations
- Better filtering
- More context for short passages
- Easier debugging
- Better reranking because the heading helps interpret the chunk

In the notebook, each chunk includes:

```json
{
  "title": "Aws Ec2 Guide",
  "section_heading": "Instance Types",
  "subheading": "Burstable Instances",
  "heading_path": "Aws Ec2 Guide > Instance Types > Burstable Instances"
}
```

That is a strong pattern. Keep it.

## Semantic Chunking

Semantic chunking groups text by topic shift rather than fixed length. A semantic
chunker may:

- Embed sentences
- Compare adjacent sentence similarity
- Split when similarity drops
- Keep related sentences together

This can improve quality for long narrative documents, but it is more complex
and slower. It also needs tuning and evaluation.

For a teaching course, start with heading-aware recursive chunking. Add semantic
chunking only when the corpus needs it.

## Parent-Child Chunking

Parent-child chunking stores two granularities:

- Child chunks: small chunks used for retrieval
- Parent chunks: larger sections used for final context

Flow:

```
query -> retrieve child chunks -> map to parent sections -> send parent context
```

This is useful when tiny chunks retrieve well but do not contain enough context
to answer safely.

Example:

- Child: one paragraph about EC2 burst credits
- Parent: full section about burstable instance behavior

## Sliding Window Overlap

Overlap reduces boundary loss.

Without overlap:

```
chunk 1: "... configure the security group"
chunk 2: "to allow inbound port 443 ..."
```

The important sentence is split.

With overlap:

```
chunk 1: "... configure the security group to allow inbound port 443"
chunk 2: "security group to allow inbound port 443 from the load balancer ..."
```

Tradeoff:

- More overlap improves recall near boundaries.
- More overlap increases storage and duplicate retrieval.

Common starting points:

| Corpus | Chunk Size | Overlap |
|--------|------------|---------|
| Short FAQs | 150-300 tokens | 20-50 |
| Product docs | 400-800 tokens | 80-150 |
| Legal/policy docs | 700-1200 tokens | 100-250 |
| Code docs | function/class boundary first | small overlap |

## Small Chunk Problem

Very small chunks often retrieve poorly:

```
"Overview"
"Important"
"EC2"
"See also"
```

These chunks do not carry enough meaning. The notebook detects this:

```python
small_chunks = [c for c in chunks if c["token_count"] < 50]
```

Then it merges small chunks when they share the same source, page, and heading
path, as long as the merged chunk does not exceed a max token limit.

That is a good rule:

```
if chunk is too small
and next chunk has same source/page/heading
and combined size <= max_tokens:
    merge
```

Do not blindly merge across headings. That can mix unrelated topics.

## Large Chunk Problem

Large chunks can hide the answer inside too much text.

Symptoms:

- Top result is technically relevant but unfocused.
- The answer model misses the exact fact.
- Citations point to broad pages rather than precise evidence.
- Reranker scores multiple chunks as similarly relevant.

Track chunks above your target:

```python
large_chunks = [c for c in chunks if c["token_count"] > 500]
```

Large chunks are not always wrong. Tables, policies, and procedures sometimes
need larger context. But inspect them.

## Chunk Text Should Include Context

Sometimes the chunk text should include heading context, not only metadata.

Example stored text:

```
Heading: AWS EC2 Guide > Instance Types > Burstable Instances

Burstable instances provide a baseline level of CPU performance...
```

This can improve embedding quality because the embedding model sees the heading.
It also helps rerankers. Avoid overdoing it; repeated boilerplate in every chunk
can create noisy similarity.

## Practical Starting Strategy

For product docs, cloud docs, and internal runbooks:

1. Extract text by page or section.
2. Clean whitespace conservatively.
3. Detect headings.
4. Create heading-aware blocks.
5. Split blocks recursively with token limits.
6. Use 500-800 token chunks.
7. Use 10-20 percent overlap.
8. Merge chunks below 50-80 tokens when same source and heading.
9. Store title, heading path, page, token count, source hash, and visibility.
10. Evaluate retrieval on real questions.

## Key Takeaways

1. Chunking controls the evidence unit of the RAG system.
2. Heading-aware recursive chunking is a strong practical default.
3. Overlap preserves boundary context but increases duplicates.
4. Small chunks need merging; large chunks need inspection.
5. The best chunk size is chosen by retrieval evaluation, not intuition.

