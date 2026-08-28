#!/usr/bin/env python3
"""Read-only structural validator for Thien-Skill-Risk-Process-Control.

The validator intentionally uses only the Python standard library.  It does not
attempt to be a complete YAML parser; JSON-compatible YAML is parsed as JSON and
ordinary YAML receives conservative, line-oriented syntax checks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote


SKILL_ID = "thien-skill-risk-process-control"
BASE_REQUIRED_DIRECTORIES = (
    "assets",
    "examples",
    "integration",
    "references",
    "scripts",
    "templates",
)
BASE_REQUIRED_FILES = (
    "SKILL.md",
    "LICENSE",
    "LICENSE-APPLICATION.md",
    "LICENSE-VERSION",
    "NOTICE",
    "THIRD-PARTY-NOTICES.md",
    "assets/PROVENANCE.md",
    "assets/icon-128.png",
    "assets/icon-512.png",
    "assets/logo-1100.png",
    "assets/logo-original.png",
    "examples/catalog.md",
    "integration/master-orchestrator-registry-entry.yaml",
    "references/requirement-coverage-matrix.md",
    "references/data-model-qa-execution.md",
    "templates/common-data-model.yaml",
)
OPENAI_REQUIRED_DIRECTORIES = ("agents",)
OPENAI_REQUIRED_FILES = ("agents/openai.yaml",)
LICENSE_FILES = (
    "LICENSE",
    "LICENSE-APPLICATION.md",
    "LICENSE-VERSION",
    "NOTICE",
    "THIRD-PARTY-NOTICES.md",
)
PNG_DIMENSIONS = {
    "assets/icon-128.png": (128, 128),
    "assets/icon-512.png": (512, 512),
    "assets/logo-1100.png": (1100, 1100),
    "assets/logo-original.png": (1100, 1100),
}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt"}
TEXT_BASENAMES = {"LICENSE", "LICENSE-VERSION", "NOTICE", "SKILL.md"}


class Report:
    """Accumulate machine-readable validation findings."""

    def __init__(self, skill_path: Path, target: str) -> None:
        self.skill_path = skill_path
        self.target = target
        self.errors: list[dict[str, Any]] = []
        self.warnings: list[dict[str, Any]] = []
        self.checks: dict[str, str] = {}

    def error(self, code: str, message: str, path: Path | None = None) -> None:
        item: dict[str, Any] = {"code": code, "message": message}
        if path is not None:
            item["path"] = display_path(path, self.skill_path)
        self.errors.append(item)

    def warning(self, code: str, message: str, path: Path | None = None) -> None:
        item: dict[str, Any] = {"code": code, "message": message}
        if path is not None:
            item["path"] = display_path(path, self.skill_path)
        self.warnings.append(item)

    def mark(self, check: str, before: int) -> None:
        self.checks[check] = "pass" if len(self.errors) == before else "fail"

    def payload(self) -> dict[str, Any]:
        return {
            "validator": "validate_package.py",
            "skill_id": SKILL_ID,
            "skill_path": self.skill_path.name,
            "target": self.target,
            "status": "pass" if not self.errors else "fail",
            "checks": self.checks,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
        }


def display_path(path: Path, skill_path: Path) -> str:
    try:
        return str(path.relative_to(skill_path))
    except ValueError:
        return path.name


def read_text(path: Path, report: Report) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        report.error("read-error", f"Cannot read UTF-8 text: {exc}", path)
        return None


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "SKILL.md must start with YAML frontmatter delimiter '---'."
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, "SKILL.md frontmatter has no closing '---' delimiter."
    fields: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*", line)
        if not match:
            return {}, f"Unsupported frontmatter syntax on line {number}."
        key, value = match.groups()
        fields[key] = value.strip().strip("\"'")
    return fields, None


def validate_frontmatter(skill_path: Path, report: Report) -> None:
    before = len(report.errors)
    path = skill_path / "SKILL.md"
    text = read_text(path, report)
    if text is None:
        report.mark("skill_frontmatter", before)
        return
    fields, error = parse_frontmatter(text)
    if error:
        report.error("frontmatter", error, path)
    else:
        if fields.get("name") != SKILL_ID:
            report.error(
                "skill-name",
                f"Frontmatter name must be exactly {SKILL_ID!r}.",
                path,
            )
        description = fields.get("description", "").strip()
        if not description:
            report.error("skill-description", "Frontmatter description is required.", path)
        unknown = sorted(set(fields) - {"name", "description", "license", "compatibility", "metadata"})
        if unknown:
            report.warning(
                "frontmatter-extra",
                "Review non-core frontmatter fields: " + ", ".join(unknown),
                path,
            )
    report.mark("skill_frontmatter", before)


def resolve_target(skill_path: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    return "canonical" if (skill_path / "agents" / "openai.yaml").is_file() else "claude"


def validate_required_structure(skill_path: Path, report: Report, target: str) -> None:
    before = len(report.errors)
    if not skill_path.is_dir():
        report.error("skill-path", "Skill path does not exist or is not a directory.", skill_path)
        report.mark("required_structure", before)
        return
    required_directories = list(BASE_REQUIRED_DIRECTORIES)
    required_files = list(BASE_REQUIRED_FILES)
    if target in {"canonical", "chatgpt", "universal"}:
        required_directories.extend(OPENAI_REQUIRED_DIRECTORIES)
        required_files.extend(OPENAI_REQUIRED_FILES)
    for relative in required_directories:
        path = skill_path / relative
        if not path.is_dir():
            report.error("missing-directory", f"Required directory is missing: {relative}", path)
    for relative in required_files:
        path = skill_path / relative
        if not path.is_file():
            report.error("missing-file", f"Required file is missing: {relative}", path)
    report.mark("required_structure", before)


def iter_text_files(skill_path: Path) -> Iterable[Path]:
    for path in sorted(skill_path.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_BASENAMES:
            yield path


MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def validate_markdown_links(skill_path: Path, report: Report) -> None:
    before = len(report.errors)
    for path in sorted(skill_path.rglob("*.md")):
        text = read_text(path, report)
        if text is None:
            continue
        for raw in MARKDOWN_LINK.findall(text):
            destination = raw.strip()
            if destination.startswith("<") and ">" in destination:
                destination = destination[1 : destination.index(">")]
            else:
                destination = destination.split(maxsplit=1)[0]
            if not destination or destination.startswith(("#", "http://", "https://", "mailto:")):
                continue
            destination = unquote(destination.split("#", 1)[0])
            if not destination:
                continue
            target = (path.parent / destination).resolve()
            try:
                target.relative_to(skill_path.resolve())
            except ValueError:
                report.error(
                    "link-escape",
                    f"Relative Markdown link leaves the skill package: {raw}",
                    path,
                )
                continue
            if not target.exists():
                report.error("broken-link", f"Markdown target does not exist: {raw}", path)
    report.mark("relative_markdown_links", before)


FORBIDDEN_TEXT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("absolute-macos-user-path", re.compile(r"/Users/[^/\s`]+/")),
    ("absolute-linux-user-path", re.compile(r"/home/[^/\s`]+/")),
    ("absolute-windows-user-path", re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\s]+\\\\")),
    ("local-session-path", re.compile(r"local-agent-mode-sessions|\.codex/attachments", re.I)),
    ("unfinished-marker", re.compile(r"\b(?:TODO|TBD|FIXME)\b\s*(?::|\[|$)", re.I | re.M)),
    ("template-marker", re.compile(r"\{\{[^{}]+\}\}|<<[^<>]+>>|<(?:INSERT|PLACEHOLDER|TODO)[^>]*>", re.I)),
    ("your-value-marker", re.compile(r"\bYOUR_[A-Z0-9_]{2,}\b")),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("openai-like-secret", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    (
        "assigned-secret",
        re.compile(
            r"\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*[\"'][^\"'\n]{8,}[\"']",
            re.I,
        ),
    ),
)


def validate_sensitive_and_unfinished_text(skill_path: Path, report: Report) -> None:
    before = len(report.errors)
    for path in iter_text_files(skill_path):
        text = read_text(path, report)
        if text is None:
            continue
        for code, pattern in FORBIDDEN_TEXT_PATTERNS:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                report.error(code, f"Forbidden or release-unsafe text on line {line}.", path)
    report.mark("release_safe_text", before)


def simple_yaml_lint(path: Path, text: str, report: Report) -> None:
    stripped = text.lstrip()
    if stripped.startswith(("{", "[")):
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            report.error("json-compatible-yaml", f"Invalid JSON-compatible YAML: {exc}", path)
        return

    block_parent_indent: int | None = None
    for number, raw_line in enumerate(text.splitlines(), start=1):
        if "\t" in raw_line[: len(raw_line) - len(raw_line.lstrip())]:
            report.error("yaml-tab", f"Tab indentation is not allowed (line {number}).", path)
            continue
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent % 2:
            report.error("yaml-indent", f"Indentation must use multiples of two spaces (line {number}).", path)
        if block_parent_indent is not None:
            if indent > block_parent_indent:
                continue
            block_parent_indent = None
        content = raw_line.strip()
        if re.match(r"^(?:-\s+)?[^:#][^:]*:\s*[|>][-+]?\s*(?:#.*)?$", content):
            block_parent_indent = indent
            continue
        if content.startswith("-"):
            remainder = content[1:].strip()
            if not remainder:
                continue
            if ":" in remainder or remainder.startswith(("'", '"', "[", "{")):
                continue
            # Plain scalar list entries are valid YAML.
            continue
        if not re.match(r"^[^:#][^:]*:\s*(?:.*)?$", content):
            report.error("yaml-structure", f"Expected a mapping or list item on line {number}.", path)


def validate_structured_files(skill_path: Path, report: Report) -> None:
    before = len(report.errors)
    for path in sorted(skill_path.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        if path.suffix.lower() == ".json":
            text = read_text(path, report)
            if text is None:
                continue
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                report.error("json-syntax", f"Invalid JSON: {exc}", path)
        elif path.suffix.lower() in {".yaml", ".yml"}:
            text = read_text(path, report)
            if text is not None:
                simple_yaml_lint(path, text, report)
    report.mark("structured_file_syntax", before)


NULL_VALUES = {"", "null", "~", "[]", "{}", "\"\"", "''"}
PRIMARY_ID_RE = re.compile(r"^\s*-\s+([A-Za-z][A-Za-z0-9_-]*_id):\s*(.*?)\s*$")
SCALAR_ID_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*_id):\s*(.*?)\s*$")
ID_LIST_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_-]*_ids):\s*(\[.*\])\s*$")


def clean_yaml_scalar(raw: str) -> str | None:
    value = raw.split(" #", 1)[0].strip()
    if value.lower() in NULL_VALUES:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value or None


def id_prefix(value: str) -> str:
    return re.split(r"[-_:]", value, maxsplit=1)[0].upper()


def validate_template_ids(skill_path: Path, report: Report) -> None:
    before = len(report.errors)
    definitions: dict[str, tuple[Path, int]] = {}
    references: list[tuple[str, Path, int]] = []
    for path in sorted((skill_path / "templates").glob("*.yaml")):
        text = read_text(path, report)
        if text is None:
            continue
        for number, line in enumerate(text.splitlines(), start=1):
            primary = PRIMARY_ID_RE.match(line)
            if primary:
                value = clean_yaml_scalar(primary.group(2))
                if value is not None:
                    if value in definitions:
                        previous_path, previous_line = definitions[value]
                        report.error(
                            "duplicate-id",
                            f"Duplicate primary ID {value!r}; first seen at "
                            f"{display_path(previous_path, skill_path)}:{previous_line}.",
                            path,
                        )
                    else:
                        definitions[value] = (path, number)
                continue
            scalar = SCALAR_ID_RE.match(line)
            if scalar:
                value = clean_yaml_scalar(scalar.group(2))
                if value is not None:
                    references.append((value, path, number))
                continue
            listed = ID_LIST_RE.match(line)
            if listed and listed.group(2) != "[]":
                try:
                    values = json.loads(listed.group(2))
                except json.JSONDecodeError:
                    report.error(
                        "id-list-syntax",
                        f"Populated ID list must use JSON-compatible inline syntax (line {number}).",
                        path,
                    )
                    continue
                if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
                    report.error("id-list-type", f"ID list must contain strings (line {number}).", path)
                else:
                    references.extend((item, path, number) for item in values)

    defined_prefixes = {id_prefix(value) for value in definitions}
    for value, path, number in references:
        if id_prefix(value) in defined_prefixes and value not in definitions:
            report.error(
                "broken-id-reference",
                f"Reference {value!r} on line {number} has no matching primary ID.",
                path,
            )
    report.mark("template_ids_and_relationships", before)


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("not a valid PNG header")
    return struct.unpack(">II", header[16:24])


def validate_assets(skill_path: Path, report: Report) -> None:
    before = len(report.errors)
    for relative, expected in PNG_DIMENSIONS.items():
        path = skill_path / relative
        if not path.is_file():
            continue  # Required-file validation reports this once.
        try:
            actual = png_dimensions(path)
        except (OSError, ValueError, struct.error) as exc:
            report.error("png-header", f"Cannot validate PNG: {exc}", path)
            continue
        if actual != expected:
            report.error(
                "png-dimensions",
                f"Expected {expected[0]}x{expected[1]}, found {actual[0]}x{actual[1]}.",
                path,
            )
    report.mark("assets", before)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_license_copies(skill_path: Path, repo_root: Path | None, report: Report) -> None:
    before = len(report.errors)
    if repo_root is None:
        report.checks["license_copies"] = "not_requested"
        return
    repo_root = repo_root.resolve()
    for relative in LICENSE_FILES:
        root_file = repo_root / relative
        skill_file = skill_path / relative
        if not root_file.is_file():
            report.error("missing-root-license-file", f"Repository copy is missing: {relative}", root_file)
            continue
        if not skill_file.is_file():
            continue  # Required-file validation reports this once.
        try:
            root_hash = sha256(root_file)
            skill_hash = sha256(skill_file)
        except OSError as exc:
            report.error("license-read", f"Cannot hash license file: {exc}", root_file)
            continue
        if root_hash != skill_hash:
            report.error(
                "license-mismatch",
                f"Repository and canonical skill copies differ: {relative}",
                skill_file,
            )
    report.mark("license_copies", before)


def validate_symlinks(skill_path: Path, report: Report) -> None:
    before = len(report.errors)
    for path in sorted(skill_path.rglob("*")):
        if path.is_symlink():
            report.error("symlink", "Release packages must not contain symbolic links.", path)
    report.mark("no_symlinks", before)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "skill_path",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Canonical skill directory (default: parent of this script directory).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="If supplied, require byte-identical repository and skill license documents.",
    )
    parser.add_argument(
        "--target",
        choices=("auto", "canonical", "claude", "chatgpt", "universal"),
        default="auto",
        help="Package layout to validate. Auto detects Claude when agents/openai.yaml is absent.",
    )
    parser.add_argument("--json", action="store_true", help="Emit a JSON report.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    skill_path = args.skill_path.resolve()
    target = resolve_target(skill_path, args.target)
    report = Report(skill_path, target)

    validate_required_structure(skill_path, report, target)
    if skill_path.is_dir():
        validate_frontmatter(skill_path, report)
        validate_symlinks(skill_path, report)
        validate_markdown_links(skill_path, report)
        validate_sensitive_and_unfinished_text(skill_path, report)
        validate_structured_files(skill_path, report)
        validate_template_ids(skill_path, report)
        validate_assets(skill_path, report)
        validate_license_copies(skill_path, args.repo_root, report)

    payload = report.payload()
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"Package validation: {payload['status'].upper()}")
        print(f"Skill: {skill_path}")
        for check, status in report.checks.items():
            print(f"  {status.upper():13} {check}")
        for item in report.errors:
            location = f" [{item['path']}]" if "path" in item else ""
            print(f"ERROR {item['code']}{location}: {item['message']}")
        for item in report.warnings:
            location = f" [{item['path']}]" if "path" in item else ""
            print(f"WARN  {item['code']}{location}: {item['message']}")
    return 0 if not report.errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
