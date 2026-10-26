"""Offline tests. Set START_DEER_TEST_RUNTIME for real DeerFlow protocol jobs."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf
import setup_runtime
import start_deer
from deer_research.corpus import Corpus


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.getenv("START_DEER_TEST_TEMP"))
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.papers = self.root / "papers"
        self.papers.mkdir()
        self.pdfs = []
        for name in ["First paper.PDF", "Second paper.pdf"]:
            path = self.papers / name
            with pymupdf.open() as pdf:
                pdf.new_page().insert_text(
                    (72, 72),
                    "Synthetic paper: compiler feedback and reproducible testing.",
                )
                pdf.save(path)
            self.pdfs.append(path)

    def test_selection_deduplicates_and_accepts_uppercase(self):
        self.assertEqual(start_deer.select_pdfs([self.papers, self.pdfs[0]]), self.pdfs)

    def test_single_refuses_multiple_files_before_creating_output(self):
        output = self.root / "job"
        with self.assertRaises(ValueError):
            start_deer.prepare_job(
                self.root, self.pdfs, "single", "question", output, 24
            )
        self.assertFalse(output.exists())

    def test_explicit_selection_isolates_and_preserves_input(self):
        original = self.pdfs[1].read_bytes()
        job, task = start_deer.prepare_job(
            self.root, [self.pdfs[1]], "auto", "custom topic", self.root / "job", 8
        )
        self.assertEqual(task, "single")
        manifest = json.loads((job / "data/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest[0]["source"], str(self.pdfs[1]))
        self.assertIn(
            "custom topic", (job / "configs/single.md").read_text(encoding="utf-8")
        )
        self.assertEqual(original, self.pdfs[1].read_bytes())
        with self.assertRaises(FileExistsError):
            start_deer.prepare_job(self.root, [self.pdfs[1]], "auto", "topic", job, 8)

    def test_unread_and_forged_quotes_are_rejected(self):
        job, _ = start_deer.prepare_job(
            self.root, self.pdfs[:1], "single", "topic", self.root / "job", 8
        )
        corpus = Corpus(job / "data/corpus")
        claim = {
            "claims": [
                {
                    "statement": "test",
                    "evidence": [
                        {
                            "paper_id": "P01",
                            "page": 1,
                            "quote": "An invented sentence absent from this paper.",
                        }
                    ],
                }
            ]
        }
        with self.assertRaisesRegex(ValueError, "not retrieved"):
            corpus.validate_report(claim, ["P01"])
        corpus.read("P01", 1)
        with self.assertRaisesRegex(ValueError, "not present"):
            corpus.validate_report(claim, ["P01"])

    def test_remove_refuses_unmarked_directory(self):
        sentinel = self.root / "keep.txt"
        sentinel.write_text("preserve", encoding="utf-8")
        with self.assertRaises(FileNotFoundError):
            setup_runtime.remove(self.root)
        self.assertTrue(sentinel.exists())

    def test_remove_refuses_unrelated_files_even_with_marker(self):
        (self.root / setup_runtime.MARKER).write_text(
            json.dumps({"kind": "start-deer-runtime-v1", "root": str(self.root)}),
            encoding="utf-8",
        )
        sentinel = self.root / "keep.txt"
        sentinel.write_text("preserve", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unrelated"):
            setup_runtime.remove(self.root)
        self.assertTrue(sentinel.exists())

    def protocol_job(self, source, count):
        runtime = os.getenv("START_DEER_TEST_RUNTIME")
        if not runtime:
            self.skipTest(
                "Set START_DEER_TEST_RUNTIME to enable real offline graph tests"
            )
        output = self.root / "protocol output"
        command = [
            sys.executable,
            str(Path(__file__).with_name("start_deer.py")),
            "--framework-root",
            runtime,
            "--source",
            str(source),
            "--topic",
            "Synthetic test",
            "--output",
            str(output),
            "--mode",
            "protocol",
        ]
        subprocess.run(
            command, cwd=self.root, check=True, capture_output=True, timeout=180
        )
        job = json.loads((output / "job.json").read_text(encoding="utf-8"))
        self.assertEqual(job["status"], "passed")
        status = json.loads(
            (Path(job["output"]) / "status.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(status["validation"]["papers_covered"]), count)
        self.assertTrue(Path(job["report"]).is_file())
        self.assertEqual(status["model"], "scripted-protocol-fixture")

    def test_real_graph_single_from_different_working_directory(self):
        self.protocol_job(self.pdfs[0], 1)

    def test_real_graph_multi_from_different_working_directory(self):
        self.protocol_job(self.papers, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
