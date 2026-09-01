# Release qualification — 1.2.0

This directory contains the retained qualification evidence created specifically for `Thien-Skill-Risk-Control-Process` version `1.2.0`. It is separate from frozen Phase 1–3 and rename evidence and does not relabel those historical runs.

## Decision

`PASS` for the documented release scope, subject to the untested surfaces below.

- Three independent fresh-context behavioral executions were independently reviewed: 3/3 cases pass, 29 applicable judgments, 0 non-pass.
- Tooling, deterministic registry, canonical package validation, history-preservation and repository-hygiene gates pass.
- Release archives passed the builder's prepare/write, checksum, CRC, normalized-parity, portability, reproducibility and staged-size gates; an idempotent write returned `unchanged`. See [`packaging-report.json`](../../dist/1.2.0/packaging-report.json) and [`SHA256SUMS`](../../dist/1.2.0/SHA256SUMS).

## Retained evidence

| File | Purpose | Retention |
|---|---|---|
| `qualification-results.json` | Machine-readable release gate, source bindings, behavioral hashes and declared limitations | Immutable with release `1.2.0` |
| `behavioral/greenfield-supplier-bank-change.md` | Full R01–R07 greenfield/RCM/options execution | Immutable raw output |
| `behavioral/document-evidence-limitation.md` | Narrow evidence-limitation execution | Immutable raw output |
| `behavioral/standards-applicability.md` | NIST/COBIT applicability and no-false-compliance execution | Immutable raw output |
| `behavioral/review.json` | Independent per-case judgments, locators and source bindings | Immutable review |

## Boundaries

Claude and ChatGPT live-platform runs, native installation/discovery/activation, cross-model variance, organization data, operating-effectiveness testing and formal compliance conclusions were not tested. A valid ZIP or passing deterministic gate does not establish those claims.

The public receipts contain repository-relative paths only. Intermediate files, tool caches and duplicate exports are not retained in this directory.
