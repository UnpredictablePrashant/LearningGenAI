#!/usr/bin/env python3
"""
Lab 05: RAG Answer With Citations
=================================
Assemble retrieved chunks into grounded context and produce a cited answer.

This lab does not call an LLM. Instead, it implements the application-side
discipline every RAG system needs: context formatting, citation handles,
not-found behavior, and citation validation.

Run:
    python lab.py

When stuck: check solution.py
"""

from dataclasses import dataclass
import re


TOKEN_RE = re.compile(r"[a-z0-9_./:-]+")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
STOP_WORDS = {
    "a", "an", "and", "are", "can", "do", "does", "for", "from", "i", "is",
    "it", "my", "of", "or", "should", "the", "to", "what", "when", "which",
}


@dataclass
class RetrievedChunk:
    chunk_id: str
    source_file: str
    page_number: int
    heading_path: str
    text: str


def tokenize(text: str) -> set[str]:
    return {token for token in TOKEN_RE.findall(text.lower()) if token not in STOP_WORDS}


def build_context(chunks: list[RetrievedChunk]) -> str:
    # TODO 1:
    # Build context sections with labels [chunk_1], [chunk_2], ...
    # Include Source, Page, Heading, and Text for each chunk.
    pass


def build_grounded_prompt(question: str, context: str) -> str:
    # TODO 2:
    # Return a prompt that instructs the model to:
    # - answer only using context
    # - say "Not found in provided documents." if missing
    # - cite chunks like [chunk_1]
    # - ignore instructions inside retrieved documents
    pass


def sentence_candidates(question: str, chunks: list[RetrievedChunk]) -> list[tuple[str, str]]:
    # TODO 3:
    # Return (sentence, citation_label) pairs where the sentence overlaps with
    # meaningful question tokens.
    # Split chunk text into sentences with SENTENCE_RE.
    pass


def answer_from_context(question: str, chunks: list[RetrievedChunk]) -> str:
    # TODO 4:
    # Use sentence_candidates to build a short extractive answer.
    # If no candidates exist, return exactly:
    # "Not found in provided documents."
    #
    # Include citation labels at the end of each sentence.
    pass


def validate_citations(answer: str, chunks: list[RetrievedChunk]) -> bool:
    # TODO 5:
    # Return True only if every citation like [chunk_N] in answer refers to an
    # existing context label.
    pass


def sample_retrieved_chunks() -> list[RetrievedChunk]:
    return [
        RetrievedChunk(
            "ec2-ssh",
            "aws-ec2-guide.pdf",
            14,
            "AWS EC2 Guide > Troubleshooting SSH",
            "When SSH to an EC2 instance fails, check security groups, network ACLs, route tables, public IP assignment, instance state, and operating system firewall rules.",
        ),
        RetrievedChunk(
            "ec2-sg",
            "aws-ec2-guide.pdf",
            15,
            "AWS EC2 Guide > Security Groups",
            "Security groups are stateful virtual firewalls. Allow inbound TCP port 22 for SSH and TCP port 443 for HTTPS from trusted sources.",
        ),
    ]


def main() -> None:
    print("\nLab 05: RAG Answer With Citations\n")

    question = "What should I check when SSH to an EC2 instance fails?"
    chunks = sample_retrieved_chunks()
    context = build_context(chunks)
    if context is None:
        print("TODO 1 not complete: build_context returned None.")
        return

    prompt = build_grounded_prompt(question, context)
    if prompt is None:
        print("TODO 2 not complete: build_grounded_prompt returned None.")
        return

    answer = answer_from_context(question, chunks)
    if answer is None:
        print("TODO 4 not complete: answer_from_context returned None.")
        return

    print("Prompt preview:")
    print(prompt[:700] + "...\n")
    print("Answer:")
    print(answer)
    print("\nCitations valid:", validate_citations(answer, chunks))


if __name__ == "__main__":
    main()

