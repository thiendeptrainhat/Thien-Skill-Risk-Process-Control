# Phase 3 — retained acceptance evidence

This directory separates test design, actual execution, review and derived release claims.
It is not part of any installable ZIP.

## Records

- `acceptance-matrix.json`: faithful JSON envelope of the approved
  [Phase 1 matrix](../../docs/phase-1/ACCEPTANCE-MATRIX.yaml), including its source hash.
  A specification is not an executed test.
- `fixtures/`: synthetic business inputs and requests. Document variants share an
  independently checked semantic source; render QA is in `fixtures/qa/`.
- `fixture-manifest.json`: hashes for the frozen inputs and document preflight.
- `harness.md`: execution logistics, scope and permitted capabilities; no answer key.
- `snapshots/round-1/` and `snapshots/round-2/`: exact runtime source files plus
  manifests. Round 1 is historical; a registry evidence-description correction
  produced round 2. See the [work log](../../docs/phase-3/WORKLOG.md).
- `runs/<run-id>/prompt.txt`: actual dispatched prompt. Each model variant uses a
  separate `collaboration.spawn_agent` invocation with `fork_turns=none`.
- `runs/<run-id>/artifacts/`: retained bytes produced by the executor, including
  the raw answer and its tool trace. These are not rewritten during grading.
- `runs/<run-id>/execution-record.json` and `run.json`: execution provenance,
  input/snapshot hashes and artifact pointers. An executed run is unreviewed until
  a separate review is attached.
- `reviews/`: invariant-by-invariant judgments with raw-output locators, reviewer
  identity and limitations. Supporting deterministic checks are not substituted
  for the answer being reviewed.
- `evidence-index.json`: derived assembly of run records and reviews, not a manual
  pass-count ledger.
- `acceptance-results.json`: retained output of the Phase 3 validator after the
  reviewed release evidence is assembled. Inspect `current_release_gate`, not
  only `integrity_status` or the process exit code.
- `tooling/`: fixture generators/preflight, evidence-integrity tests and
  package-builder tests. Passing tooling tests is not model acceptance.

## Validation

From the repository root:

```sh
python3 -B scripts/assemble_phase3_evidence.py --write
python3 -B scripts/run_tests.py --phase3 --json
python3 -B -m unittest discover -s tests/phase-3/tooling -v
```

The Phase 3 runner validates retained evidence. It does **not** generate a model
answer, perform installation, run the specialist or fetch external sources.
A successful process exit means evidence integrity passed; inspect the separate
claim and release-gate fields before saying the release is accepted.
Missing runs stay `not_run`; missing or inconsistent evidence is not promoted to
pass. A pass for `must_not_observe` means the forbidden behavior was not observed.

Do not use `--write-results` with `--phase3`. The historical 104-case registry and
28 provisional execution summaries remain separate and unchanged.
Do not regenerate or edit a fixture/snapshot after it is hashed and used in a
run. Remediation requires new evidence with an explicit retest relationship.

## Scope and limitations

- Inputs are synthetic, not real-company assurance. A finite fixture set does not
  establish correctness for every possible end-to-end process.
- Fresh delegated contexts do not receive prior conversation or acceptance
  answers; system/developer instructions still apply.
- The exact model identifier is not exposed by the delegation interface and
  remains null, never guessed.
- Tool traces are executor-maintained records, not a complete exported host
  transcript. Failed/truncated calls and unavailable capabilities must be
  retained or disclosed.
- The root reviewer did not produce delegated answers, but authored the fixtures
  and skill update. This is not third-party independent assurance.
- Simulated no-network, access restrictions or unavailable-specialist profiles
  verify behavior under those conditions, not native platform capabilities.
- Local file extraction and live specialist cooperation require their own actual
  evidence. A synthetic extraction packet does not prove an OCR or specialist run.
- Codex delegated-runtime evidence does not prove Claude or ChatGPT installation,
  discovery, native UI behavior or universal cross-platform acceptance.
