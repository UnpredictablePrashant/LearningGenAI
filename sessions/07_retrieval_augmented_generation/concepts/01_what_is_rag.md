# 01. What Is RAG?

Retrieval-Augmented Generation is an architecture pattern where the system
retrieves relevant knowledge before asking a language model to answer.

The model does not magically know your private runbooks, PDFs, tickets, or
architecture docs. RAG gives the model a small, carefully selected evidence pack
at answer time.

```
user question
  -> retrieve relevant chunks
  -> optionally rerank them
  -> build prompt context
  -> generate grounded answer
  -> cite sources
```

## Why RAG Exists

LLMs are trained on broad public and licensed data. They are not a database.
They have three important limitations:

- They may not know private or recent information.
- They can compress and confuse facts from training.
- They can answer confidently even when evidence is missing.

RAG addresses these limitations by adding a retrieval system around the model.
The model is still useful for synthesis, explanation, and formatting, but the
facts come from retrieved documents.

## DevOps Analogy

During an incident, you do not ask a senior engineer to answer from memory only.
You give them:

- The alert
- Recent logs
- The relevant runbook
- Recent deploys
- The service ownership record
- Similar past incidents

That is RAG. The LLM is the engineer writing the response. Retrieval is the
incident context gathering step.

## RAG vs Fine-Tuning

RAG and fine-tuning solve different problems.

Use RAG when the system needs:

- Private knowledge
- Frequently changing facts
- Citations and source traceability
- Access control over documents
- Easy document updates without retraining
- Answers constrained to a known knowledge base

Use fine-tuning when the system needs:

- A consistent style or format
- Better task-specific behavior
- Domain-specific output conventions
- Lower prompt length for repeated behavior
- A model to learn a pattern, not memorize a document

Fine-tuning is not a reliable way to inject thousands of changing documents.
RAG is the right default for knowledge-heavy applications.

## The Core RAG Loop

1. Ingest documents.
2. Clean and normalize text.
3. Split text into chunks.
4. Attach metadata to each chunk.
5. Convert chunks into embeddings.
6. Store text, metadata, and vectors.
7. Embed the user query.
8. Retrieve candidate chunks.
9. Filter and rerank candidates.
10. Assemble prompt context.
11. Generate an answer with citations.
12. Log the retrieval and answer for evaluation.

Each step is an engineering decision. Bad chunking, weak metadata, or poor
reranking can break the system even if the LLM is strong.

## Why "Just Send the Whole PDF" Fails

Sending entire documents into the prompt is tempting but fragile:

- Context windows are finite.
- Long prompts are expensive.
- Relevant facts get buried in irrelevant text.
- Models can miss details in the middle of long context.
- You cannot easily apply document-level access control.
- Citations become vague.

RAG is selective. It tries to send the minimum evidence needed for a good answer.

## RAG Is a Search System First

Many RAG failures are search failures:

- The answer is wrong because the correct chunk was never retrieved.
- The context contains adjacent but irrelevant text.
- The retrieval query uses different vocabulary from the documents.
- The system retrieves old docs instead of current docs.
- Metadata filters remove the right answer.
- Access control is applied after retrieval instead of before retrieval.

Before blaming the LLM, inspect the retrieved chunks.

## Common RAG Failure Modes

**No retrieval:** The answer is generated from model prior knowledge.

**Weak retrieval:** The right document exists but is ranked too low.

**Over-retrieval:** Too many chunks are stuffed into context, adding noise.

**Under-chunking:** Chunks are too large and dilute the useful fact.

**Over-chunking:** Chunks are too small and lose context.

**Metadata loss:** The answer cannot cite source, page, owner, version, or date.

**Stale data:** Old documents outrank new documents.

**Prompt injection:** Retrieved text contains instructions that try to control
the assistant.

**Permission leak:** Retrieval returns content the user should not see.

## A Production Mental Model

Think of RAG as a controlled data plane:

```
documents -> indexed knowledge -> retrieval policy -> prompt evidence -> answer
```

Every arrow needs observability:

- What document version was indexed?
- How was it chunked?
- Which embedding model created the vector?
- What query was used?
- Which chunks were retrieved?
- Which chunks were reranked into the final context?
- Which citations appeared in the answer?

If you cannot answer those questions, you cannot debug your RAG system.

## Key Takeaways

1. RAG is not "LLM plus vector database"; it is a retrieval pipeline plus a
   generation pipeline.
2. Retrieval quality usually matters more than generation model size.
3. Chunking and metadata design are first-class system design decisions.
4. A good RAG answer should be grounded, citeable, and allowed by policy.

