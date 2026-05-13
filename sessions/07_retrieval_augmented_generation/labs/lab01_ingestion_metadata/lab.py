#!/usr/bin/env python3
"""
Lab 01: Ingestion and Metadata
==============================
Create clean page records from raw document text.

In a real RAG pipeline this step might read PDFs with pypdf. This lab uses
in-memory documents so you can focus on extraction shape, cleaning, metadata,
stable IDs, and quality checks.

Run:
    python lab.py

When stuck: check solution.py
"""

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import re


@dataclass
class RawDocument:
    source_file: str
    document_type: str
    visibility: str
    pages: list[str]


@dataclass
class PageRecord:
    page_id: str
    source_file: str
    page_number: int
    title: str
    document_type: str
    visibility: str
    text: str
    char_count: int
    text_hash: str
    ingested_at: str


def clean_text(text: str) -> str:
    # TODO 1:
    # Clean extracted text conservatively:
    # - Return "" for empty input.
    # - Collapse repeated whitespace into one space.
    # - Remove spaces before punctuation marks like "." and ",".
    # - Strip leading/trailing whitespace.
    pass


def title_from_filename(source_file: str) -> str:
    # TODO 2:
    # Convert a filename like "aws-ec2-guide.pdf" into "Aws Ec2 Guide".
    # Remove the file extension, replace "-" and "_" with spaces, and title-case.
    pass


def short_hash(text: str, length: int = 12) -> str:
    # TODO 3:
    # Return the first `length` characters of a SHA-256 hash for text.
    pass


def create_page_records(documents: list[RawDocument]) -> list[PageRecord]:
    # TODO 4:
    # For each non-empty cleaned page, create a PageRecord.
    # Use a stable page_id from source_file, page_number, and text hash.
    # Use datetime.now(timezone.utc).isoformat() for ingested_at.
    pass


def quality_report(records: list[PageRecord]) -> dict:
    # TODO 5:
    # Return a dict with:
    # - page_count
    # - min_chars
    # - max_chars
    # - avg_chars
    # - duplicate_text_hashes
    #
    # If records is empty, return zeros for all numeric values.
    pass


def sample_documents() -> list[RawDocument]:
    return [
        RawDocument(
            source_file="aws-ec2-guide.pdf",
            document_type="guide",
            visibility="internal",
            pages=[
                "Amazon   EC2 provides scalable compute capacity . It lets teams run virtual servers in AWS.",
                "Security groups control inbound and outbound traffic .  Allow port 22 for SSH only from trusted networks.",
                "   ",
            ],
        ),
        RawDocument(
            source_file="kubernetes-runbooks.pdf",
            document_type="runbook",
            visibility="internal",
            pages=[
                "CrashLoopBackOff means a container starts and exits repeatedly. Check previous logs and memory limits.",
                "ImagePullBackOff means Kubernetes cannot pull the image. Check the tag and registry credentials.",
            ],
        ),
    ]


def main() -> None:
    print("\nLab 01: Ingestion and Metadata\n")

    records = create_page_records(sample_documents())
    if records is None:
        print("TODO 4 not complete: create_page_records returned None.")
        return

    report = quality_report(records)
    if report is None:
        print("TODO 5 not complete: quality_report returned None.")
        return

    print("Quality report:")
    for key, value in report.items():
        print(f"  {key}: {value}")

    print("\nPage records:")
    for record in records:
        print(f"- {record.page_id} | {record.source_file} p{record.page_number} | {record.char_count} chars")
        print(f"  title={record.title} visibility={record.visibility} hash={record.text_hash}")
        print(f"  text={record.text}")


if __name__ == "__main__":
    main()

