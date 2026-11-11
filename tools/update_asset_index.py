#!/usr/bin/env python3
"""Incrementally index files without changing records unless --apply is given."""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
from pathlib import Path
import sys
from datetime import datetime, timezone

ASSET_FIELDS = ["asset_id", "path", "filename", "sha256", "size_bytes", "modified_utc", "status", "notes"]
LOG_FIELDS = ["timestamp_utc", "action", "asset_id", "path", "details"]
START = "<!-- ASSET-001:GENERATED:START -->"
END = "<!-- ASSET-001:GENERATED:END -->"


def read_csv(path: Path, fields: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != fields:
            raise ValueError(f"Unexpected CSV header in {path}; expected {','.join(fields)}")
        return [{key: row.get(key, "") or "" for key in fields} for row in reader]


def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def csv_text(fields: list[str], rows: list[dict[str, str]]) -> str:
    import io
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def render_index(original: str, records: list[dict[str, str]]) -> str:
    managed = [START, "", "| Asset ID | File | SHA-256 | Status |", "| --- | --- | --- | --- |"]
    for row in records:
        filename = row["filename"].replace("|", "\\|")
        managed.append(f"| {row['asset_id']} | `{filename}` | `{row['sha256']}` | {row['status']} |")
    managed += ["", END]
    block = "\n".join(managed)
    if START in original or END in original:
        if original.count(START) != 1 or original.count(END) != 1 or original.index(START) > original.index(END):
            raise ValueError("Malformed ASSET-001 managed block markers in ASSET_INDEX.md")
        a, b = original.index(START), original.index(END) + len(END)
        return original[:a] + block + original[b:]
    prefix = original.rstrip()
    return prefix + "\n\n## 自动资产清单（ASSET-001）\n\n" + block + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="directory to scan (default: current directory)")
    parser.add_argument("--output-dir", type=Path, default=Path.cwd(), help="directory containing assets.csv and change_log.csv")
    parser.add_argument("--apply", action="store_true", help="write changes; without this flag only preview")
    parser.add_argument("--include-hidden", action="store_true", help="include hidden files and directories")
    args = parser.parse_args(argv)
    root, outdir = args.root.resolve(), args.output_dir.resolve()
    assets_path, log_path, index_path = outdir / "assets.csv", outdir / "change_log.csv", outdir / "ASSET_INDEX.md"
    if not root.is_dir():
        parser.error(f"scan root is not a directory: {root}")
    existing = read_csv(assets_path, ASSET_FIELDS)
    log = read_csv(log_path, LOG_FIELDS)
    by_path = {r["path"]: r for r in existing}
    known_ids = {r["asset_id"] for r in existing if r["asset_id"]}
    new_rows: list[dict[str, str]] = []
    unchanged = 0
    ignored: list[str] = []
    for file in sorted(root.rglob("*")):
        if not file.is_file():
            continue
        rel = file.relative_to(root).as_posix()
        if not args.include_hidden and any(part.startswith(".") or part == "__pycache__" for part in Path(rel).parts):
            continue
        if file.resolve() in {assets_path, log_path, index_path}:
            continue
        sha = digest_file(file)
        stat = file.stat()
        prior = by_path.get(rel)
        if prior:
            # Preserve identifiers, review status, and notes; refresh observed metadata only.
            row = dict(prior)
            if prior["sha256"] != sha:
                row.update(sha256=sha, size_bytes=str(stat.st_size), modified_utc=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat())
                new_rows.append(row)
            else:
                unchanged += 1
            continue
        # Similar hashes and missing old paths are reported as possible duplicates/renames,
        # never merged automatically.
        matches = [r for r in existing if r["sha256"] == sha]
        aid = "A-" + sha[:12].upper()
        suffix = 2
        base = aid
        while aid in known_ids:
            aid = f"{base}-{suffix}"
            suffix += 1
        known_ids.add(aid)
        row = {"asset_id": aid, "path": rel, "filename": file.name, "sha256": sha,
               "size_bytes": str(stat.st_size), "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
               "status": "CANDIDATE", "notes": ""}
        new_rows.append(row)
        if matches:
            ignored.append(f"possible duplicate hash: {rel} matches {', '.join(r['asset_id'] for r in matches)}")
    updated = [dict(r) for r in existing]
    for row in new_rows:
        if row["asset_id"] in {r["asset_id"] for r in existing}:
            for i, old in enumerate(updated):
                if old["asset_id"] == row["asset_id"]:
                    log.append({"timestamp_utc": datetime.now(timezone.utc).isoformat(), "action": "CONTENT_UPDATED", "asset_id": row["asset_id"], "path": row["path"], "details": "SHA-256 changed at existing path"})
                    updated[i] = row
                    break
        else:
            updated.append(row)
            log.append({"timestamp_utc": datetime.now(timezone.utc).isoformat(), "action": "CANDIDATE_ADDED", "asset_id": row["asset_id"], "path": row["path"], "details": "New file discovered"})
    original_index = index_path.read_text(encoding="utf-8") if index_path.exists() else "# 项目资产索引\n"
    rendered = render_index(original_index, updated)
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Root: {root}")
    print(f"Existing records: {len(existing)}; unchanged: {unchanged}; additions/updates: {len(new_rows)}")
    print(f"Resulting records: {len(updated)}; possible duplicate/rename notices: {len(ignored)}")
    for message in ignored:
        print(f"NOTICE: {message}")
    if args.apply:
        outdir.mkdir(parents=True, exist_ok=True)
        assets_path.write_text(csv_text(ASSET_FIELDS, updated), encoding="utf-8")
        log_path.write_text(csv_text(LOG_FIELDS, log), encoding="utf-8")
        index_path.write_text(rendered, encoding="utf-8")
        print("Wrote assets.csv, change_log.csv, and managed ASSET_INDEX.md block.")
    else:
        print("No files written. Use --apply to commit this preview.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
