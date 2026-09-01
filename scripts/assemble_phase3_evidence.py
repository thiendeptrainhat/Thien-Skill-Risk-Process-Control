#!/usr/bin/env python3
"""Assemble retained receipts and separately authored reviews; never grade."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

from safe_filesystem import (
    absolute_no_resolve, atomic_write, lexists, read_regular_bytes,
    reject_symlink_chain, require_within,
)


def load_json(path: Path, repo: Path, label: str) -> object:
    data = read_regular_bytes(path, repo, label)
    try:
        return json.loads(data)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid JSON in {label} {path}: {exc}") from exc


def safe_directory_entries(path: Path, repo: Path, label: str) -> list[os.DirEntry[str]]:
    path = absolute_no_resolve(path)
    require_within(path, repo, label)
    reject_symlink_chain(path, label)
    try:
        metadata = path.lstat()
    except FileNotFoundError as exc:
        raise ValueError(f"Missing {label}: {path}") from exc
    if not stat.S_ISDIR(metadata.st_mode):
        raise ValueError(f"Expected directory for {label}: {path}")
    try:
        with os.scandir(path) as entries:
            return sorted(entries, key=lambda entry: entry.name)
    except OSError as exc:
        raise ValueError(f"Cannot inspect {label} {path}: {exc}") from exc


def artifact(path: Path, repo: Path) -> dict[str, str]:
    data = read_regular_bytes(path, repo, "evidence reference")
    return {
        "path": absolute_no_resolve(path).relative_to(repo).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def assemble(repo: Path) -> dict[str, object]:
    repo = absolute_no_resolve(repo)
    reject_symlink_chain(repo, "repository root")
    if not repo.is_dir():
        raise ValueError(f"Repository root is not a directory: {repo}")

    root = repo / "tests" / "phase-3"
    matrix = load_json(root / "acceptance-matrix.json", repo, "acceptance matrix")
    if not isinstance(matrix, dict):
        raise ValueError("Acceptance matrix must be a JSON object")
    try:
        source_sha = matrix["source"]["sha256"]
    except (KeyError, TypeError) as exc:
        raise ValueError("Acceptance matrix has no source.sha256") from exc
    if not isinstance(source_sha, str) or not source_sha:
        raise ValueError("Acceptance matrix source.sha256 must be a non-empty string")

    runs: list[dict[str, object]] = []
    runs_root = root / "runs"
    for entry in safe_directory_entries(runs_root, repo, "run directory"):
        entry_path = runs_root / entry.name
        metadata = entry.stat(follow_symlinks=False)
        if stat.S_ISLNK(metadata.st_mode):
            raise ValueError(f"Symlink not permitted in run directory: {entry_path}")
        if not stat.S_ISDIR(metadata.st_mode):
            continue
        run_path = entry_path / "run.json"
        if not lexists(run_path):
            continue
        record = load_json(run_path, repo, "run record")
        if not isinstance(record, dict):
            raise ValueError(f"Run record must be a JSON object: {run_path}")
        if record.get("run_id") != entry.name:
            raise ValueError("Run ID/path mismatch")
        review = root / "reviews" / f"{entry.name}.json"
        if lexists(review):
            record["review"] = artifact(review, repo)
        runs.append(record)

    group_reviews: list[dict[str, str]] = []
    reviews_root = root / "reviews"
    for entry in safe_directory_entries(reviews_root, repo, "review directory"):
        path = reviews_root / entry.name
        metadata = entry.stat(follow_symlinks=False)
        if stat.S_ISLNK(metadata.st_mode):
            raise ValueError(f"Symlink not permitted in review directory: {path}")
        if stat.S_ISREG(metadata.st_mode) and entry.name.startswith("group-") and entry.name.endswith(".json"):
            group_reviews.append(artifact(path, repo))

    return {
        "schema_version": "1",
        "matrix_source_sha256": source_sha,
        "runs": runs,
        "group_reviews": group_reviews,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--write",
        action="store_true",
        help="Update only tests/phase-3/evidence-index.json; preserve receipts/reviews",
    )
    args = parser.parse_args(argv)
    repo = absolute_no_resolve(args.repo_root)
    index = assemble(repo)
    if args.write:
        path = repo / "tests" / "phase-3" / "evidence-index.json"
        atomic_write(
            path,
            (json.dumps(index, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
            repo,
            "evidence index destination",
        )
        print(
            json.dumps(
                {
                    "assembled_runs": len(index["runs"]),
                    "attached_reviews": sum(run.get("review") is not None for run in index["runs"]),
                    "group_reviews": len(index["group_reviews"]),
                    "status": "assembled_not_graded",
                }
            )
        )
    else:
        print(json.dumps(index, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
