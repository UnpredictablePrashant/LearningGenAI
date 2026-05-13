#!/usr/bin/env python3
"""Lab 01: Ingestion and Metadata (SOLUTION)"""

from dataclasses import dataclass
from datetime import datetime, timezone
from collections import Counter
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
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    return text.strip()


def title_from_filename(source_file: str) -> str:
    stem = source_file.rsplit(".", 1)[0]
    stem = stem.replace("-", " ").replace("_", " ")
    return stem.title()


def short_hash(text: str, length: int = 12) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def create_page_records(documents: list[RawDocument]) -> list[PageRecord]:
    records: list[PageRecord] = []
    ingested_at = datetime.now(timezone.utc).isoformat()

    for document in documents:
        title = title_from_filename(document.source_file)
        for page_number, raw_text in enumerate(document.pages, start=1):
            text = clean_text(raw_text)
            if not text:
                continue

            text_hash = short_hash(text)
            page_id = short_hash(f"{document.source_file}|{page_number}|{text_hash}")
            records.append(
                PageRecord(
                    page_id=page_id,
                    source_file=document.source_file,
                    page_number=page_number,
                    title=title,
                    document_type=document.document_type,
                    visibility=document.visibility,
                    text=text,
                    char_count=len(text),
                    text_hash=text_hash,
                    ingested_at=ingested_at,
                )
            )

    return records


def quality_report(records: list[PageRecord]) -> dict:
    if not records:
        return {
            "page_count": 0,
            "min_chars": 0,
            "max_chars": 0,
            "avg_chars": 0,
            "duplicate_text_hashes": 0,
        }

    counts = [record.char_count for record in records]
    hash_counts = Counter(record.text_hash for record in records)
    duplicate_hashes = sum(1 for count in hash_counts.values() if count > 1)
    return {
        "page_count": len(records),
        "min_chars": min(counts),
        "max_chars": max(counts),
        "avg_chars": round(sum(counts) / len(counts), 1),
        "duplicate_text_hashes": duplicate_hashes,
    }


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
    print("\nLab 01: Ingestion and Metadata (Solution)\n")

    records = create_page_records(sample_documents())
    report = quality_report(records)

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

