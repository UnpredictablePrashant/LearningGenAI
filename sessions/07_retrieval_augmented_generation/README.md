# Session 07: Retrieval-Augmented Generation (RAG)

Build a complete RAG system: ingest documents, clean text, create chunks with
metadata, embed them, retrieve relevant passages, rerank results, and generate
grounded answers with citations.

## DevOps Analogy

| RAG Concept | DevOps Equivalent |
|-------------|-------------------|
| Source documents | Runbooks, architecture docs, postmortems, tickets |
| Ingestion | Log shipping / ETL pipeline |
| Cleaning | Log normalization and parsing |
| Chunking | Splitting large logs into searchable events |
| Metadata | Labels: service, environment, region, owner, version |
| Embeddings | Coordinates for meaning, like semantic labels |
| Vector store | Search index for operational knowledge |
| Retrieval | Finding the right runbook during an incident |
| Reranking | Senior engineer reviewing candidate docs before action |
| Context assembly | Incident brief sent to the responder |
| Grounded answer | Response backed by cited evidence |

## What You'll Learn

- Explain what RAG solves and when it is better than fine-tuning
- Understand the mathematics behind embeddings, cosine similarity, BM25,
  reciprocal rank fusion, and reranking
- Extract and clean document text while preserving provenance
- Design metadata schemas that support filtering, access control, citations,
  freshness, and debugging
- Compare chunking strategies: fixed-size, recursive, heading-aware, semantic,
  parent-child, and sliding-window chunks
- Choose practical embedding models for local learning and production systems
- Build vector retrieval, keyword retrieval, hybrid retrieval, and metadata
  filtered retrieval
- Use rerankers to improve top results before sending context to an LLM
- Assemble grounded prompts with citations and a safe "not found" behavior
- Evaluate RAG quality with retrieval metrics, answer metrics, and production
  observability

## Pipeline From the Notebook

The supplied notebook at `D:/teaching/RAG/rag.ipynb` uses this flow:

```
PDFs -> pages -> cleaned pages -> heading-aware token chunks
     -> merged chunks -> embeddings -> ChromaDB
     -> retrieve top 20 -> rerank top 5 -> answer with citations
```

This session converts that notebook workflow into reusable terminal-friendly
course material.

## Prerequisites

```bash
pip install -r ../../requirements.txt
```

No API key is required for the core labs. Optional demos can use:

```bash
cp ../../.env.example ../../.env
# then set OPENAI_API_KEY if you want generated answers from OpenAI
```

Recommended previous sessions:

- Session 01 for tokens, embeddings, and semantic search
- Session 03 for local model execution with Ollama
- Session 04 for provider-compatible LLM API calls
- Session 06 for memory retrieval patterns

## Session Structure

```
07_retrieval_augmented_generation/
|-- concepts/
|   |-- 01_what_is_rag.md
|   |-- 02_rag_math.md
|   |-- 03_ingestion_cleaning_metadata.md
|   |-- 04_chunking_strategies.md
|   |-- 05_embedding_models.md
|   |-- 06_retrieval_strategies.md
|   |-- 07_reranking_context_assembly.md
|   `-- 08_evaluation_and_production.md
|-- labs/
|   |-- lab01_ingestion_metadata/
|   |-- lab02_chunking_strategy/
|   |-- lab03_embeddings_vector_search/
|   |-- lab04_retrieval_reranking/
|   `-- lab05_rag_answer_citations/
`-- demos/
    |-- demo_chunking_strategies.py
    |-- demo_retrieval_and_reranking.py
    `-- demo_chroma_rag_pipeline.py
```

## Labs

| Lab | Topic | Key Concepts |
|-----|-------|--------------|
| lab01_ingestion_metadata | Document ingestion | cleaning, page records, metadata, stable IDs |
| lab02_chunking_strategy | Token-aware chunking | headings, overlap, small-chunk merging |
| lab03_embeddings_vector_search | Embeddings and vector search | normalization, cosine similarity, metadata filters |
| lab04_retrieval_reranking | Hybrid retrieval | keyword, vector, reciprocal rank fusion, reranking |
| lab05_rag_answer_citations | Grounded answers | context assembly, citations, not-found behavior |

## Demos

| Demo | What it shows |
|------|---------------|
| `demo_chunking_strategies.py` | Why chunk size, overlap, headings, and metadata affect retrieval |
| `demo_retrieval_and_reranking.py` | Vector, keyword, hybrid retrieval, and reranking over a runbook corpus |
| `demo_chroma_rag_pipeline.py` | Optional full local vector DB pipeline with Chroma and sentence-transformers |

## Quick Start

```bash
cd sessions/07_retrieval_augmented_generation

# Read concepts first
cat concepts/01_what_is_rag.md
cat concepts/02_rag_math.md
cat concepts/04_chunking_strategies.md

# Run demos
python demos/demo_chunking_strategies.py
python demos/demo_retrieval_and_reranking.py

# Optional, requires chromadb and sentence-transformers from requirements.txt
python demos/demo_chroma_rag_pipeline.py

# Work through labs
python labs/lab01_ingestion_metadata/lab.py
python labs/lab02_chunking_strategy/lab.py
python labs/lab03_embeddings_vector_search/lab.py
python labs/lab04_retrieval_reranking/lab.py
python labs/lab05_rag_answer_citations/lab.py
```

## Estimated Time

| Activity | Time |
|----------|------|
| Concepts | 90 min |
| 5 labs | 150 min |
| Demos | 40 min |
| **Total** | **~4.5 hours** |

