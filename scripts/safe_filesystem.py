"""Small stdlib-only primitives for safe repository reads and publications."""
from __future__ import annotations

import os
from pathlib import Path
import stat
import tempfile
from typing import Mapping


def absolute_no_resolve(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def lexists(path: Path) -> bool:
    return os.path.lexists(os.fspath(path))


def require_within(path: Path, root: Path, label: str) -> None:
    try:
        absolute_no_resolve(path).relative_to(absolute_no_resolve(root))
    except ValueError as exc:
        raise ValueError(f"{label} escapes its permitted root: {path}") from exc


def reject_symlink_chain(path: Path, label: str) -> None:
    """Reject symlinks, including dangling ones, in existing path components."""
    path = absolute_no_resolve(path)
    missing = False
    for component in [*reversed(path.parents), path]:
        if missing:
            continue
        try:
            metadata = component.lstat()
        except FileNotFoundError:
            missing = True
            continue
        except OSError as exc:
            raise ValueError(f"Cannot inspect {label} path component {component}: {exc}") from exc
        if stat.S_ISLNK(metadata.st_mode):
            raise ValueError(f"Symlink not permitted in {label} path: {component}")


def read_regular_bytes(path: Path, root: Path | None = None, label: str = "file") -> bytes:
    path = absolute_no_resolve(path)
    if root is not None:
        require_within(path, root, label)
    reject_symlink_chain(path, label)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise ValueError(f"Cannot open {label} as a regular file: {path}: {exc}") from exc
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError(f"Expected regular {label}: {path}")
        with os.fdopen(descriptor, "rb", closefd=False) as handle:
            return handle.read()
    finally:
        os.close(descriptor)


def read_tree(root: Path, label: str) -> dict[Path, bytes]:
    """Snapshot a tree without following links or accepting special files."""
    root = absolute_no_resolve(root)
    reject_symlink_chain(root, label)
    try:
        metadata = root.lstat()
    except FileNotFoundError as exc:
        raise ValueError(f"Missing {label}: {root}") from exc
    if not stat.S_ISDIR(metadata.st_mode):
        raise ValueError(f"Expected directory for {label}: {root}")
    files: dict[Path, bytes] = {}

    def walk(directory: Path, relative: Path) -> None:
        try:
            with os.scandir(directory) as iterator:
                names = sorted(entry.name for entry in iterator)
        except OSError as exc:
            raise ValueError(f"Cannot inspect {label} {directory}: {exc}") from exc
        for name in names:
            child, child_relative = directory / name, relative / name
            try:
                child_metadata = child.lstat()
            except OSError as exc:
                raise ValueError(f"Cannot inspect {label} entry {child}: {exc}") from exc
            if stat.S_ISLNK(child_metadata.st_mode):
                raise ValueError(f"Symlink not permitted in {label}: {child}")
            if stat.S_ISDIR(child_metadata.st_mode):
                walk(child, child_relative)
            elif stat.S_ISREG(child_metadata.st_mode):
                files[child_relative] = read_regular_bytes(child, label=label)
            else:
                raise ValueError(f"Special file not permitted in {label}: {child}")

    walk(root, Path())
    return files


def file_identity(path: Path) -> tuple[int, int, int, int] | None:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(metadata.st_mode):
        raise ValueError(f"Atomic output target is not a regular file: {path}")
    return metadata.st_dev, metadata.st_ino, metadata.st_size, metadata.st_mtime_ns


def _stage(path: Path, data: bytes, mode: int) -> Path:
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    staged = Path(name)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        os.close(descriptor)
        descriptor = -1
        if lexists(staged):
            staged.unlink()
        raise
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    return staged


def atomic_write_many(outputs: Mapping[Path, bytes], root: Path, label: str) -> None:
    """Stage all outputs, publish per file, and roll back a process-level failure."""
    root = absolute_no_resolve(root)
    originals: dict[Path, tuple[tuple[int, int, int, int] | None, bytes | None, int]] = {}
    normalized: dict[Path, bytes] = {}
    for supplied, data in outputs.items():
        path = absolute_no_resolve(supplied)
        if path in normalized:
            raise ValueError(f"Duplicate {label}: {path}")
        require_within(path, root, label)
        reject_symlink_chain(path, label)
        if not path.parent.is_dir():
            raise ValueError(f"{label} parent is not a directory: {path.parent}")
        identity = file_identity(path)
        old = read_regular_bytes(path, root, label) if identity is not None else None
        mode = stat.S_IMODE(path.lstat().st_mode) if identity is not None else 0o644
        originals[path] = identity, old, mode
        normalized[path] = data

    staged: dict[Path, Path] = {}
    published: list[Path] = []
    try:
        for path, data in normalized.items():
            staged[path] = _stage(path, data, originals[path][2])
        for path in normalized:
            reject_symlink_chain(path, label)
            if file_identity(path) != originals[path][0]:
                raise ValueError(f"{label} changed while replacement was staged: {path}")
            os.replace(staged[path], path)
            published.append(path)
        staged.clear()
    except BaseException as exc:
        rollback_error: BaseException | None = None
        for path in reversed(published):
            try:
                _, old, mode = originals[path]
                if old is None:
                    path.unlink()
                else:
                    restoration = _stage(path, old, mode)
                    try:
                        os.replace(restoration, path)
                    finally:
                        if lexists(restoration):
                            restoration.unlink()
            except BaseException as restore_exc:
                rollback_error = restore_exc
        if rollback_error is not None:
            raise RuntimeError(f"{label} publication and rollback failed: {rollback_error}") from exc
        raise
    finally:
        for temporary in staged.values():
            if lexists(temporary):
                temporary.unlink()


def atomic_write(path: Path, data: bytes, root: Path, label: str) -> None:
    atomic_write_many({path: data}, root, label)
