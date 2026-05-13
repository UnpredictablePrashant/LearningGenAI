# 03. Ingestion, Cleaning, and Metadata

RAG quality starts before embeddings. If the text extraction is messy, the
embedding model encodes messy text. If metadata is weak, the system cannot
filter, cite, audit, or debug results.

The notebook pipeline begins with PDFs:

```
PDF files -> page text -> cleaned pages -> structured page records
```

That is the right mental model. Treat ingestion like a production data pipeline.

## Ingestion Goals

For every source document, capture:

- Text content
- Source file
- Page number or section location
- Document title
- Document version or modified time
- Access policy
- Ingestion timestamp
- Parser used
- Hash of the source or extracted text

Do not store anonymous text blobs. Anonymous chunks are painful to debug and
dangerous to cite.

## PDF Extraction Reality

PDFs are display formats, not clean semantic document formats. Extraction can
produce:

- Broken words
- Missing spaces
- Repeated headers and footers
- Page numbers in the middle of sentences
- Tables flattened into unreadable text
- Columns merged in the wrong order
- Empty pages
- OCR errors

Always inspect samples after extraction.

## Basic Page Record

A page record is the first useful unit:

```json
{
  "source_file": "aws-ec2-guide.pdf",
  "page_number": 12,
  "title": "AWS EC2 Guide",
  "text": "Amazon EC2 provides scalable compute capacity...",
  "char_count": 812,
  "text_hash": "6e2b...",
  "parser": "pypdf",
  "ingested_at": "2026-05-12T08:00:00Z"
}
```

This record is not yet the final retrieval chunk. It is an auditable extraction
artifact.

## Cleaning

Cleaning should make text consistent without destroying meaning.

Reasonable cleaning:

- Collapse repeated whitespace.
- Remove spaces before punctuation.
- Remove repeated headers and footers when confidently detected.
- Drop empty pages.
- Normalize common OCR artifacts.
- Preserve section boundaries when possible.

Dangerous cleaning:

- Removing all punctuation.
- Lowercasing everything when product names are case-sensitive.
- Removing code fences, YAML indentation, or table structure.
- Stripping page numbers when page citations are required.
- Deleting "small" lines that may be headings.

Cleaning is not cosmetic. It changes retrieval behavior.

## Metadata Schema

Useful chunk metadata:

```json
{
  "chunk_id": "c8b2a5d31e0f",
  "source_file": "aws-ec2-guide.pdf",
  "page_number": 12,
  "chunk_index": 3,
  "title": "AWS EC2 Guide",
  "section_heading": "Instance Types",
  "subheading": "Burstable Instances",
  "heading_path": "AWS EC2 Guide > Instance Types > Burstable Instances",
  "token_count": 386,
  "document_type": "guide",
  "product": "ec2",
  "version": "2026-04",
  "visibility": "internal",
  "source_hash": "..."
}
```

This metadata supports:

- Citations: source file, page, heading
- Filtering: product, environment, team, visibility
- Debugging: parser, hash, ingestion timestamp
- Freshness: version, modified time
- Governance: owner, access policy, retention

## Metadata Should Be Queryable

Metadata is not only for display. It affects retrieval.

Examples:

```python
# Only retrieve current docs
where={"version": "2026-04"}

# Only retrieve content the user is allowed to see
where={"visibility": {"$in": ["public", "internal-platform"]}}

# Only retrieve EC2 docs
where={"product": "ec2"}
```

Apply security filters before final context assembly. In high-risk systems, apply
them before vector search or inside the vector database query itself.

## Stable IDs

Chunk IDs should be stable across indexing runs when the chunk content and source
location are unchanged. Stable IDs make upserts safe.

Reasonable ID input:

```
source_file + page_number + heading_path + chunk_index + chunk_text_hash
```

Avoid IDs based only on a loop counter unless the corpus never changes. If one
page is added near the beginning of a document, every later loop counter shifts.

## Provenance

A grounded answer should trace back to evidence:

```
Answer sentence -> chunk -> page -> document -> source system
```

If you cannot trace an answer to a source, it is not grounded. It may still be
useful, but it should not be presented as a cited RAG answer.

## Data Quality Checks

Run checks after ingestion:

- Number of source files found
- Number of pages extracted
- Empty page count
- Minimum, maximum, and average characters per page
- Duplicate page hashes
- Suspiciously short documents
- Suspiciously large pages
- Parser failures

Run checks after chunking:

- Number of chunks
- Minimum, maximum, and average tokens per chunk
- Count of chunks below the minimum useful size
- Count of chunks above target size
- Duplicate chunk IDs
- Missing metadata fields

## Key Takeaways

1. Ingestion is a data engineering problem, not a model problem.
2. Metadata is required for filtering, citations, debugging, and governance.
3. Cleaning should improve consistency without erasing meaning.
4. Stable IDs make reindexing and upserts reliable.

