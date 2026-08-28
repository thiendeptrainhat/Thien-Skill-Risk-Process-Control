#!/usr/bin/env python3
"""Assemble retained receipts and separately authored reviews; never grade."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

def artifact(path, repo):
    if path.is_symlink() or not path.resolve().is_relative_to(repo):
        raise ValueError("Unsafe evidence reference")
    return {"path": path.relative_to(repo).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

def assemble(repo):
    root = repo / "tests/phase-3"
    matrix = json.loads((root / "acceptance-matrix.json").read_text())
    runs = []
    for path in sorted((root / "runs").glob("*/run.json")):
        record = json.loads(path.read_text())
        if record["run_id"] != path.parent.name:
            raise ValueError("Run ID/path mismatch")
        review = root / "reviews" / (record["run_id"] + ".json")
        if review.exists():
            record["review"] = artifact(review, repo)
        runs.append(record)
    group_reviews = [artifact(path, repo) for path in
                     sorted((root / "reviews").glob("group-*.json"))]
    return {"schema_version": "1", "matrix_source_sha256": matrix["source"]["sha256"],
            "runs": runs, "group_reviews": group_reviews}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--write", action="store_true",
                    help="Update only tests/phase-3/evidence-index.json; preserve receipts/reviews")
    args = ap.parse_args()
    repo = args.repo_root.resolve()
    index = assemble(repo)
    if args.write:
        path = repo / "tests/phase-3/evidence-index.json"
        if path.is_symlink():
            raise ValueError("Refusing symlink index")
        path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"assembled_runs": len(index["runs"]),
                          "attached_reviews": sum(r.get("review") is not None for r in index["runs"]),
                          "group_reviews": len(index["group_reviews"]),
                          "status": "assembled_not_graded"}))
    else:
        print(json.dumps(index, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
