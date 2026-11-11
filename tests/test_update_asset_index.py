import csv
import tempfile
import unittest
from pathlib import Path

from tools.update_asset_index import ASSET_FIELDS, LOG_FIELDS, main, render_index


class AssetIndexTests(unittest.TestCase):
    def test_dry_run_writes_nothing_and_apply_preserves_review_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); root = base / "scan"; out = base / "out"
            root.mkdir(); out.mkdir()
            (root / "one.txt").write_text("first", encoding="utf-8")
            with (out / "assets.csv").open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, ASSET_FIELDS); w.writeheader()
                w.writerow(dict(asset_id="KEEP-1", path="old.txt", filename="old.txt", sha256="a"*64, size_bytes="1", modified_utc="", status="APPROVED", notes="human"))
            (out / "ASSET_INDEX.md").write_text("Manual text stays.\n", encoding="utf-8")
            self.assertEqual(main(["--root", str(root), "--output-dir", str(out)]), 0)
            self.assertFalse((out / "change_log.csv").exists())
            self.assertNotIn("ASSET-001:GENERATED:START", (out / "ASSET_INDEX.md").read_text(encoding="utf-8"))
            self.assertEqual(main(["--root", str(root), "--output-dir", str(out), "--apply"]), 0)
            with (out / "assets.csv").open(newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            old = next(r for r in rows if r["asset_id"] == "KEEP-1")
            candidate = next(r for r in rows if r["path"] == "one.txt")
            self.assertEqual((old["status"], old["notes"]), ("APPROVED", "human"))
            self.assertEqual(candidate["status"], "CANDIDATE")
            self.assertIn("Manual text stays.", (out / "ASSET_INDEX.md").read_text(encoding="utf-8"))
            with (out / "change_log.csv").open(newline="", encoding="utf-8") as f:
                self.assertEqual(len(list(csv.DictReader(f))), 1)

    def test_managed_block_preserves_surrounding_content(self):
        source = "Before\n" + "<!-- ASSET-001:GENERATED:START -->\nold\n<!-- ASSET-001:GENERATED:END -->" + "\nAfter\n"
        result = render_index(source, [])
        self.assertTrue(result.startswith("Before\n"))
        self.assertTrue(result.endswith("\nAfter\n"))

    def test_changed_content_keeps_id_and_status_and_logs_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); root = base / "scan"; out = base / "out"
            root.mkdir(); out.mkdir(); (root / "kept.txt").write_text("new", encoding="utf-8")
            with (out / "assets.csv").open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, ASSET_FIELDS); w.writeheader()
                w.writerow(dict(asset_id="KEEP", path="kept.txt", filename="kept.txt", sha256="0"*64, size_bytes="3", modified_utc="", status="APPROVED", notes="reviewed"))
            self.assertEqual(main(["--root", str(root), "--output-dir", str(out), "--apply"]), 0)
            with (out / "assets.csv").open(newline="", encoding="utf-8") as f:
                row, = list(csv.DictReader(f))
            self.assertEqual((row["asset_id"], row["status"], row["notes"]), ("KEEP", "APPROVED", "reviewed"))
            with (out / "change_log.csv").open(newline="", encoding="utf-8") as f:
                change, = list(csv.DictReader(f))
            self.assertEqual(change["action"], "CONTENT_UPDATED")

    def test_duplicate_hash_is_report_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); root = base / "scan"; out = base / "out"
            root.mkdir(); out.mkdir(); (root / "copy.txt").write_text("same", encoding="utf-8")
            import hashlib
            sha = hashlib.sha256(b"same").hexdigest()
            with (out / "assets.csv").open("w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, ASSET_FIELDS); w.writeheader()
                w.writerow(dict(asset_id="ORIGINAL", path="other.txt", filename="other.txt", sha256=sha, size_bytes="4", modified_utc="", status="CONFIRMED", notes=""))
            self.assertEqual(main(["--root", str(root), "--output-dir", str(out)]), 0)
            with (out / "assets.csv").open(newline="", encoding="utf-8") as f:
                self.assertEqual(len(list(csv.DictReader(f))), 1)


if __name__ == "__main__":
    unittest.main()
