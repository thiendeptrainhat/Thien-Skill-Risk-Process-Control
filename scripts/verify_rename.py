#!/usr/bin/env python3
"""Verify the bounded 1.1.0 -> 1.1.1 identity rename without model execution.

Read-only against the checkout. --historical reconstructs the fixed, reviewed Git
baseline in an isolated temporary directory and reruns its receipt validator.
It does not fetch, install, rewrite evidence, or award old passes to the new ID.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

BASELINE = "db9b0f42c1a2ce0938abc888a03699d401b9fd41"
OLD_ID = "thien-skill-risk-process-control"
NEW_ID = "thien-skill-risk-control-process"
URL = "https://github.com/thiendeptrainhat/Thien-Skill-Risk-Process-Control"  # Historical package declaration; preserve its bytes.
CURRENT_URL = "https://github.com/thiendeptrainhat/Thien-Skill-Risk-Control-Process"
IDENTITY_FILES = {
    "SKILL.md", "agents/openai.yaml", "NOTICE", "LICENSE-APPLICATION.md",
    "integration/master-orchestrator-registry-entry.yaml",
    "scripts/validate_package.py", "references/governance-security-handoffs.md",
    "references/source-skill-inventory.md",
}
PRESERVED_ROOTS = (
    "tests", "dist", "docs/phase-1", "docs/phase-2", "docs/phase-3",
)
PRESERVED_FILES = (
    "LICENSE", "LICENSE-VERSION", "THIRD-PARTY-NOTICES.md",
    "scripts/phase3_evidence.py", "scripts/assemble_phase3_evidence.py",
    "scripts/capture_phase3_run.py",
)


def expected_bytes(name: str, original: bytes) -> bytes:
    if name not in IDENTITY_FILES:
        return original
    parts = original.decode("utf-8").split(URL)
    text = URL.join(part.replace(OLD_ID, NEW_ID).replace(
        "Risk-Process-Control", "Risk-Control-Process") for part in parts)
    if name == "LICENSE-APPLICATION.md":
        text = text.replace("`1.1.0`", "`1.1.1`")
    if name == "integration/master-orchestrator-registry-entry.yaml":
        text = text.replace('version: "1.1.0"', 'version: "1.1.1"')
    return text.encode("utf-8")


def git_baseline(repo: Path) -> dict[str, bytes]:
    archive = subprocess.run(
        ["git", "archive", "--format=tar", BASELINE], cwd=repo,
        check=True, capture_output=True, timeout=30,
    ).stdout
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as handle:
        for member in handle.getmembers():
            name = PurePosixPath(member.name)
            if name.is_absolute() or ".." in name.parts or "\\" in member.name:
                raise ValueError("Unsafe Git archive path")
            if member.isdir():
                continue
            if not member.isfile() or member.name in files:
                raise ValueError("Unexpected nonregular or duplicate baseline entry")
            content = handle.extractfile(member)
            assert content is not None
            files[member.name] = content.read()
    return files


def verify(repo: Path, baseline: dict[str, bytes]) -> dict:
    errors = []
    prefix = f"skills/{OLD_ID}/"
    old = {p[len(prefix):]: data for p, data in baseline.items() if p.startswith(prefix)}
    root = repo / "skills" / NEW_ID
    actual = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append("Canonical symlink: " + str(path.relative_to(repo)))
        elif path.is_file():
            actual[path.relative_to(root).as_posix()] = path.read_bytes()
    if set(actual) != set(old):
        errors.append("Canonical inventory differs from the 49-file baseline")
    changed = []
    for name, data in old.items():
        if actual.get(name) != expected_bytes(name, data):
            errors.append("Unexpected content change: " + name)
        if actual.get(name) != data:
            changed.append(name)
    if (repo / "skills" / OLD_ID).exists():
        errors.append("Old canonical directory still exists")

    protected = {p: data for p, data in baseline.items() if p in PRESERVED_FILES or
                 any(p.startswith(root + "/") for root in PRESERVED_ROOTS)}
    for path, data in protected.items():
        current = repo / path
        if current.is_symlink() or not current.is_file() or current.read_bytes() != data:
            errors.append("Historical/license artifact changed: " + path)
    for name in ("NOTICE", "LICENSE-APPLICATION.md"):
        if (repo / name).read_bytes() != expected_bytes(name, baseline[name]):
            errors.append("Unexpected root declaration change: " + name)
    manifest = (repo / "RELEASE-MANIFEST.yaml").read_text()
    if f'url: "{CURRENT_URL}"' not in manifest:
        errors.append("Repository URL does not match the authorized current URL")
    if 'visibility: "public"' not in manifest:
        errors.append("Repository visibility does not match user-confirmed public status")
    if f'skill_id: "{NEW_ID}"' not in manifest or 'skill_version: "1.1.1"' not in manifest:
        errors.append("Release identity/version mismatch")

    link_counts = {}
    for name in ("README.md", "INSTALL.md", "docs/HANDOFF.md"):
        path = repo / name
        text = path.read_text()
        links = re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', text)
        link_counts[name] = len(links)
        for link in links:
            link = link.split("#", 1)[0]
            if not link or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link):
                continue
            if not (path.parent / unquote(link)).exists():
                errors.append(f"Missing local link in {name}: {link}")
    readme = (repo / "README.md").read_text()
    headings = ["## Vai trò của skill", "## Lợi ích và tính năng khi kích hoạt",
                "## Cách sử dụng skill", "## Cài đặt"]
    positions = [readme.find(h) for h in headings]
    if -1 in positions or positions != sorted(positions):
        errors.append("Requested README section order was not preserved")
    return {
        "status": "fail" if errors else "pass", "errors": errors,
        "canonical_files": len(actual), "identity_only_changed_files": sorted(changed),
        "byte_identical_canonical_files": len(old) - len(changed),
        "historical_and_license_files_checked": len(protected),
        "current_doc_link_counts": link_counts,
        "canonical_sha256": {p: hashlib.sha256(data).hexdigest() for p, data in sorted(actual.items())},
    }


def historical_check(baseline: dict[str, bytes]) -> dict:
    with tempfile.TemporaryDirectory(prefix="risk-control-process-history-") as temporary:
        root = Path(temporary)
        for name, data in baseline.items():
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        result = subprocess.run(
            [sys.executable, "-B", str(root / "scripts/run_tests.py"),
             "--repo-root", str(root), "--phase3", "--json"],
            cwd=root, capture_output=True, text=True, timeout=60,
        )
        payload = json.loads(result.stdout)
        return {
            "exit_code": result.returncode, "integrity_status": payload["integrity_status"],
            "error_count": payload["error_count"], "errors": payload["errors"],
            "historical_gate": payload["current_release_gate"],
            "evidence_counts": payload["evidence_counts"],
            "scope": "Frozen 1.1.0 Git baseline only; not current 1.1.1 acceptance or new model executions",
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--historical", action="store_true")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    baseline = git_baseline(repo)
    result = verify(repo, baseline)
    result.update({"baseline_commit": BASELINE, "version": "1.1.1", "skill_id": NEW_ID,
                   "generated_at": datetime.now(timezone.utc).isoformat(),
                   "model_runs_after_rename": "not_run", "native_installation": "not_run",
                   "expected_current_repository_url": CURRENT_URL,
                   "expected_current_repository_visibility": "public"})
    if args.historical:
        result["historical_recheck"] = historical_check(baseline)
        old = result["historical_recheck"]
        if old["exit_code"] or old["integrity_status"] != "pass" or old["historical_gate"]["status"] != "evidence_complete":
            result["errors"].append("Frozen historical evidence did not revalidate")
            result["status"] = "fail"
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
