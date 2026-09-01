#!/usr/bin/env python3
"""Retain actual delegated-run artifacts. Never generates answers or grades."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import uuid
from zoneinfo import ZoneInfo

from safe_filesystem import (
    absolute_no_resolve, lexists, read_regular_bytes, read_tree,
    reject_symlink_chain, require_within,
)


RUN_ID_RE = re.compile(r"P1-U\d{2}-V\d{2}-R\d+")
SNAPSHOT_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def artifact_bytes(relative: Path, data: bytes) -> dict[str, str]:
    return {"path": relative.as_posix(), "sha256": hashlib.sha256(data).hexdigest()}


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_staged_tree(stage: Path, files: dict[Path, bytes]) -> None:
    for relative, data in sorted(files.items(), key=lambda item: item[0].as_posix()):
        destination = stage / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())


def publish_run_directory(
    stage: Path,
    run_dir: Path,
    original_seed: dict[Path, bytes],
) -> None:
    """Publish a complete run and restore the seed directory if publication fails."""
    runs_root = run_dir.parent
    reject_symlink_chain(runs_root, "run destination")
    reject_symlink_chain(run_dir, "run destination")
    if read_tree(run_dir, "run seed") != original_seed:
        raise ValueError("Run seed changed while capture was being staged")

    backup = runs_root / f".capture-backup-{run_dir.name}-{uuid.uuid4().hex}"
    if lexists(backup):
        raise ValueError(f"Unexpected capture backup collision: {backup}")
    os.rename(run_dir, backup)
    try:
        os.rename(stage, run_dir)
    except BaseException:
        try:
            if lexists(run_dir):
                raise RuntimeError(f"Cannot restore run seed because destination reappeared: {run_dir}")
            os.rename(backup, run_dir)
        except BaseException as restore_exc:
            raise RuntimeError(
                f"Capture publication failed and automatic seed restoration also failed: {restore_exc}"
            ) from restore_exc
        raise
    shutil.rmtree(backup)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--agent-task", required=True)
    parser.add_argument("--snapshot", default="round-1")
    parser.add_argument("--retest-of", action="append", default=[])
    args = parser.parse_args(argv)

    if not RUN_ID_RE.fullmatch(args.run_id):
        raise ValueError("Unexpected run ID")
    if not SNAPSHOT_RE.fullmatch(args.snapshot):
        raise ValueError("Unexpected snapshot ID")
    if any(not RUN_ID_RE.fullmatch(run_id) for run_id in args.retest_of):
        raise ValueError("Unexpected retest run ID")

    repo = absolute_no_resolve(args.repo_root)
    reject_symlink_chain(repo, "repository root")
    if not repo.is_dir():
        raise ValueError(f"Repository root is not a directory: {repo}")

    runs_root = repo / "tests" / "phase-3" / "runs"
    run_dir = runs_root / args.run_id
    require_within(run_dir, repo, "Run destination")
    reject_symlink_chain(run_dir, "run destination")
    if not runs_root.is_dir():
        raise ValueError(f"Missing retained-run directory: {runs_root}")

    run_record_path = run_dir / "run.json"
    if lexists(run_record_path):
        read_regular_bytes(run_record_path, repo, "retained run record")
        print(f"Already captured: {args.run_id}; no evidence overwritten")
        return 0

    # The dispatched prompt is intentionally seeded before execution. Snapshot it
    # and any other dispatch records so a complete replacement directory can be
    # published without mutating retained files in place.
    seed = read_tree(run_dir, "run seed")
    if Path("prompt.txt") not in seed:
        raise ValueError(f"Missing actual dispatched prompt: {run_dir / 'prompt.txt'}")
    reserved = [
        relative
        for relative in seed
        if relative == Path("execution-record.json")
        or relative == Path("run.json")
        or relative.parts[:1] == ("artifacts",)
    ]
    if reserved:
        raise ValueError(
            "Refusing to incorporate partial prior capture files: "
            + ", ".join(path.as_posix() for path in sorted(reserved))
        )

    output_dir = absolute_no_resolve(args.output_dir)
    private_tmp = Path("/private/tmp")
    require_within(output_dir, private_tmp, "Execution output")
    if output_dir == private_tmp:
        raise ValueError("Execution output must be an isolated child directory of /private/tmp")
    reject_symlink_chain(output_dir, "execution output")
    output_files = read_tree(output_dir, "execution output")
    for filename in (Path("output.md"), Path("tool-trace.json")):
        if filename not in output_files:
            raise ValueError(f"Missing actual executor artifact: {filename.as_posix()}")
    try:
        trace = json.loads(output_files[Path("tool-trace.json")])
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid executor tool trace: {exc}") from exc
    if not isinstance(trace, dict):
        raise ValueError("Executor tool trace must be a JSON object")

    variant = args.run_id.rsplit("-R", 1)[0]
    case = variant.rsplit("-V", 1)[0]
    matrix_path = repo / "tests" / "phase-3" / "acceptance-matrix.json"
    matrix_bytes = read_regular_bytes(matrix_path, repo, "acceptance matrix")
    try:
        matrix = json.loads(matrix_bytes)
        cases = matrix["matrix"]["cases"]
        case_spec = next(item for item in cases if item.get("id") == case)
    except (UnicodeError, json.JSONDecodeError, KeyError, TypeError, StopIteration) as exc:
        raise ValueError(f"Acceptance matrix has no valid specification for {case}: {exc}") from exc
    if not isinstance(case_spec.get("requirements"), list):
        raise ValueError(f"Acceptance matrix requirements are invalid for {case}")

    fixture_dir = repo / "tests" / "phase-3" / "fixtures" / variant
    fixture_files = read_tree(fixture_dir, "fixture directory")
    harness_relative = Path("tests/phase-3/harness.md")
    harness_bytes = read_regular_bytes(repo / harness_relative, repo, "execution harness")
    snapshot_relative = Path("tests/phase-3/snapshots") / args.snapshot / "manifest.json"
    snapshot_bytes = read_regular_bytes(repo / snapshot_relative, repo, "skill snapshot manifest")

    # Everything above is validation/read-only. Only now may staging begin.
    now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()
    execution = {
        "run_id": args.run_id, "task_name": args.agent_task,
        "dispatch_mechanism": "collaboration.spawn_agent", "fork_turns": "none", "recorded_at": now,
        "execution_observed_by": "root Codex task",
        "retention_method": "Copy actual files written by the delegated executor after completion",
        "model_identifier": "not_available",
        "limitations": ["No full exported host transcript is available; tool-trace.json is executor-maintained.",
                        "Fresh context is from fork_turns=none; inherited system/developer instructions still apply."],
    }
    execution_relative = Path("tests/phase-3/runs") / args.run_id / "execution-record.json"
    execution_bytes = json_bytes(execution)

    inputs = [{"fixture_id": f"{variant}:{relative.name}", "version": "1",
               "artifact": artifact_bytes(Path("tests/phase-3/fixtures") / variant / relative, data)}
              for relative, data in sorted(fixture_files.items(), key=lambda item: item[0].as_posix())]
    inputs.append({"fixture_id": "execution-harness", "version": "1",
                   "artifact": artifact_bytes(harness_relative, harness_bytes)})

    run_prefix = Path("tests/phase-3/runs") / args.run_id
    retained = [
        artifact_bytes(run_prefix / "artifacts" / relative, data)
        for relative, data in sorted(output_files.items(), key=lambda item: item[0].as_posix())
    ]
    simulated = case in {"P1-U07", "P1-U08", "P1-U17"}
    record = {
        "run_id": args.run_id, "case_id": case, "variant_id": variant,
        "requirement_ids": case_spec["requirements"], "timestamp": trace.get("started_at", now),
        "verification_mode": "model", "execution_status": "executed",
        "runtime": {
            "platform": "Codex", "surface": "Codex desktop delegated local runtime",
            "runtime": "collaboration.spawn_agent", "model": None,
            "model_identifier_status": "not_available", "fresh_context": True,
            "capabilities": {
                "local_file_read": "available",
                "external_lookup": "authorized_read_only" if case == "P1-U06" else "prohibited_by_run_policy",
                "specialist": "authorized_local_document_evidence" if variant == "P1-U16-V01" else "not_invoked",
            },
            "capability_simulation": simulated,
        },
        "authorized_source_scope": "Frozen skill; this fixture; harness; necessary local readers. Public official web only for U06; local Document-Evidence only for U16-V01.",
        "inputs": inputs,
        "skill_snapshot": artifact_bytes(snapshot_relative, snapshot_bytes),
        "raw_prompt": artifact_bytes(run_prefix / "prompt.txt", seed[Path("prompt.txt")]),
        "raw_output": artifact_bytes(run_prefix / "artifacts/output.md", output_files[Path("output.md")]),
        "tool_trace": artifact_bytes(run_prefix / "artifacts/tool-trace.json", output_files[Path("tool-trace.json")]),
        "execution_record": artifact_bytes(execution_relative, execution_bytes),
        "review": None, "retest_of": args.retest_of, "additional_artifacts": retained,
        "limitations": ["Synthetic business inputs, not real-organization assurance.",
                        "Executor-maintained trace, not a complete exported host transcript.",
                        "Exact model identifier is not exposed by this delegation interface."],
    }
    if simulated:
        record["limitations"].append(
            "Capability/access conditions are simulated test conditions; not platform capability verification."
        )

    staged_files = dict(seed)
    for relative, data in output_files.items():
        staged_files[Path("artifacts") / relative] = data
    staged_files[Path("execution-record.json")] = execution_bytes
    staged_files[Path("run.json")] = json_bytes(record)

    stage = Path(tempfile.mkdtemp(prefix=f".capture-stage-{args.run_id}-", dir=runs_root))
    try:
        write_staged_tree(stage, staged_files)
        publish_run_directory(stage, run_dir, seed)
    except BaseException:
        if lexists(stage):
            shutil.rmtree(stage)
        raise

    print(json.dumps({"captured": args.run_id, "retained_artifacts": len(retained),
                      "review_status": "executed_unreviewed"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
