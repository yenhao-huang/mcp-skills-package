"""Page-preserving local paper corpus; document text is untrusted evidence."""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

TARGET = "Agentic Code Optimization via Compiler-LLM Cooperation.pdf"


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def ingest(source: Path, destination: Path) -> list[dict]:
    files = sorted(source.glob("*.pdf"), key=lambda p: (p.name != TARGET, p.name))
    if not files:
        raise ValueError(f"No PDFs found: {source}")
    return ingest_files(files, destination)


def ingest_files(files: list[Path], destination: Path) -> list[dict]:
    """Ingest an explicit selection into a new corpus without copying source PDFs."""
    import pymupdf as fitz

    if not files or len(files) > 99:
        raise ValueError("Select between 1 and 99 PDFs per research job")
    destination.mkdir(parents=True, exist_ok=True)
    records = []
    for index, path in enumerate(files, 1):
        with fitz.open(path) as pdf:
            pages = [
                {"page": i + 1, "text": page.get_text()} for i, page in enumerate(pdf)
            ]
        if any(not p["text"].strip() for p in pages):
            raise ValueError(f"Empty text page; OCR/manual review needed: {path.name}")
        record = {
            "id": f"P{index:02d}",
            "source": str(path.resolve()),
            "filename": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "page_count": len(pages),
            "pages": pages,
        }
        (destination / f"{record['id']}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        text = "\n\n".join(
            f"=== {record['id']} p.{p['page']} ===\n{p['text']}" for p in pages
        )
        (destination / f"{record['id']}.txt").write_text(text, encoding="utf-8")
        records.append({k: v for k, v in record.items() if k != "pages"})
    (destination.parent / "manifest.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return records


class Corpus:
    def __init__(self, directory: Path, allowed_ids: list[str] | None = None):
        self.papers = {}
        for path in sorted(directory.glob("P[0-9][0-9].json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            if allowed_ids is None or record["id"] in allowed_ids:
                self.papers[record["id"]] = record
        if not self.papers:
            raise ValueError("Corpus is empty")
        if allowed_ids and set(allowed_ids) - self.papers.keys():
            raise ValueError("Requested paper missing from corpus")
        self.accessed: set[tuple[str, int]] = set()

    def catalog(self) -> list[dict]:
        return [
            {k: p[k] for k in ("id", "filename", "page_count", "sha256")}
            for p in self.papers.values()
        ]

    def read(self, paper_id: str, page: int) -> dict:
        if paper_id not in self.papers:
            raise ValueError("Unknown or out-of-scope paper ID")
        paper = self.papers[paper_id]
        if page < 1 or page > paper["page_count"]:
            raise ValueError("Page out of range (1-based)")
        self.accessed.add((paper_id, page))
        return {
            "paper_id": paper_id,
            "page": page,
            "text": paper["pages"][page - 1]["text"],
        }

    def search(self, query: str, limit: int = 8) -> list[dict]:
        """Deterministic TF-IDF page ranking; this is not semantic retrieval."""
        if not 1 <= limit <= 20:
            raise ValueError("limit must be 1..20")
        query_tokens = set(tokens(query))
        documents = [
            (pid, p, Counter(tokens(p["text"])))
            for pid, paper in self.papers.items()
            for p in paper["pages"]
        ]
        frequency = Counter(t for _, _, bag in documents for t in bag)
        scored = []
        for pid, page, bag in documents:
            score = sum(
                (1 + math.log(bag[t])) * math.log(1 + len(documents) / frequency[t])
                for t in query_tokens
                if bag[t]
            ) / math.sqrt(max(1, sum(bag.values())))
            if score > 0:
                scored.append((score, pid, page["page"]))
        return [
            {"score": round(score, 6), **self.read(pid, page)}
            for score, pid, page in sorted(scored, key=lambda x: (-x[0], x[1], x[2]))[
                :limit
            ]
        ]

    def validate_report(self, report: dict, required_ids: list[str]) -> dict:
        """Validate provenance mechanically, never assert semantic correctness."""
        claims = report.get("claims", [])
        if not isinstance(claims, list) or not claims:
            raise ValueError("No claims returned")
        covered = set()
        for index, claim in enumerate(claims, 1):
            if (
                not isinstance(claim.get("statement"), str)
                or not claim["statement"].strip()
            ):
                raise ValueError("Empty claim statement")
            evidence = claim.get("evidence", [])
            if not evidence:
                raise ValueError("Claim without evidence")
            for item in evidence:
                pid, page = item["paper_id"], item["page"]
                if (pid, page) not in self.accessed:
                    raise ValueError("Citation was not retrieved in this run")
                quote = item.get("quote", "")
                if len(quote.strip()) < 12:
                    raise ValueError("Evidence quote too short")
                normalize = lambda s: " ".join(s.split())
                if normalize(quote) not in normalize(self.read(pid, page)["text"]):
                    raise ValueError(
                        f"Evidence quote not present on cited page: claim {index}, {pid} p.{page}, "
                        f"quote={quote[:120]!r}. Copy the exact substring from read_paper_page."
                    )
                covered.add(pid)
        missing = set(required_ids) - covered
        if missing:
            raise ValueError(f"Missing paper coverage: {sorted(missing)}")
        return {
            "claims": len(claims),
            "papers_covered": sorted(covered),
            "retrieved_pages": len(self.accessed),
            "provenance_valid": True,
            "semantic_support": "requires human review",
        }
