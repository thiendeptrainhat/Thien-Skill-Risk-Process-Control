# Phase 3 verifier self-tests

These tests exercise tooling with explicitly synthetic receipts in temporary
directories. They do not invoke a model and are **not** behavioral evidence for
the skill, a platform, a document-reading capability or an acceptance case.
Never move their dummy receipts into the real evidence index.

From the repository root:

```sh
python3 -B -m unittest discover -s tests/phase-3/tooling -p test_phase3_evidence_validator.py -v
```

The standard library is sufficient for the self-tests. Real non-JSON YAML
requires Ruby's safe YAML parser, already available on the authoring host. No
dependency is downloaded or installed; unavailable parsing produces a failure,
not an unchecked pass.

## Read-only evidence validation

```sh
python3 -B scripts/run_tests.py --phase3 --json
```

Optional `--phase3-matrix` and `--phase3-evidence` take repository-relative paths.
Defaults are `tests/phase-3/acceptance-matrix.json` and
`tests/phase-3/evidence-index.json`. The matrix envelope contains `source`
(`path`, `sha256`) and `matrix`, exactly equal to the safely parsed approved
`docs/phase-1/ACCEPTANCE-MATRIX.yaml`. It cannot silently omit variants or weaken
invariants. The index has `schema_version: "1"`, `matrix_source_sha256`, `runs`
and `group_reviews`.

The original command without `--phase3` retains its legacy static/registry
contract, including `status: "pass"`. Phase 3 does not overwrite historical
104-case/28-summary records. Combining `--phase3` with `--write-results` is an
error before any writes.

## What a receipt establishes

- Every artifact reference is `{path, sha256}` for retained, repository-relative
  bytes. Traversal, absolute paths, symlinks, hash mismatches and missing files
  are rejected. Raw prompt, inputs, raw output, tool trace and JSON execution
  metadata are distinct from a review or an expected answer.
- Frozen snapshot manifests record `skill_id`, `skill_version`, `source_root`,
  `canonical_source` and the complete `files` inventory. `source_root` lives
  under `tests/phase-3/snapshots/`; `canonical_source` names the mutable skill.
  File hashes, SKILL name and integration version are checked. Historical
  snapshots remain reviewable but are ineligible for current-release claims
  when their relative paths/content differ from current canonical content.
- Model receipts name platform, surface, runtime and the host-provided model
  identifier, or explicit `not_available`/`not_provided` with `model: null` and
  limitations. They record capabilities, permission conditions,
  `capability_simulation`, `fresh_context: true`, timestamp/timezone, authorized
  source scope, fixture IDs/versions/hashes and optional `retest_of` links.
  Static receipts use `verification_mode: "static"`, `model: null` and
  `model_identifier_status: "not_applicable"`. Static receipts never count as
  model/platform execution.
- Reviews bind the run and approved rubric SHA, identify the reviewer and
  `independent`/`self_check` relationship, and assess **every** applicable
  invariant. IDs are 1-based `case.must_observe.N`,
  `case.must_not_observe.N`, `variant.must_observe.N` and
  `variant.must_not_observe.N`. A pass for a forbidden behavior means it was
  **not observed**, not that it occurred. Each judgment needs a rationale and
  evidence references to `raw_output`, `tool_trace` or `execution_record` with
  `L1`, `L1-L5` or `entire_artifact` locators. At least one raw-output citation
  is required. Review result must agree with all checks; counts are not a pass.
- Cross-format group reviews assess `case.group_must_observe.N`, refer to every
  compared run's output and use one runtime/model/snapshot context. A group
  review of older outputs cannot cover a later retest. The latest run for each
  variant/context is selected; an earlier pass cannot hide a later failure.
- `not_run`, `blocked`, `executed_unreviewed`, `inconclusive` and `fail` remain
  nonpass. Missing evidence never creates a pass. Every planned variant appears
  in `variant_coverage`, including those without any run. Capability simulations
  cannot verify live lookup, file-input parity or live Document-Evidence handoff.

## Reading the result

`integrity_status` checks the receipt structure and retained bytes. Individual
claims are in `claims_by_context`; `eligible_for_current_release` additionally
requires matching current canonical content. `current_release_gate` needs core
business logic and backward compatibility in the same model context,
distribution integrity on the same source content, and a passing separate legacy
static/registry check. Per-platform `tested_partial` is not a platform-wide pass.

Exit code `0` means valid evidence structure, **not** complete acceptance. Check
`acceptance_status`, claims, limitations and the release gate separately. The
validator does not authenticate executor identity, reconstruct hidden prompts,
independently judge semantics or convert self-checks into independent reviews.
Those remain explicit limitations of the retained evidence. No test result
grants installation, publication or human-approval authority.

## Retaining a real execution

Use a fresh delegated context with the saved prompt, frozen skill and only its
fixture. After that executor finishes, capture its actual output directory:

```sh
python3 -B scripts/capture_phase3_run.py --run-id P1-U04-V01-R2 --output-dir /private/tmp/thien-rpc-phase3.xGeed0/P1-U04-V01-R2 --agent-task /root/p1_u04_v01_r2 --snapshot round-2 --retest-of P1-U04-V01-R1
```

The example records an execution that actually occurred; do not reuse its ID
for a new run. The capture helper copies bytes and refuses differing overwrites;
it cannot generate a model answer or pass. Author a separate per-invariant review
in `tests/phase-3/reviews/<run-id>.json` after reading actual outputs and traces.
Then refresh the derived index (original receipts/reviews are not overwritten):

```sh
python3 -B scripts/assemble_phase3_evidence.py --write
python3 -B scripts/run_tests.py --phase3 --json
```

`generate_document_fixtures.py` and `validate_document_fixtures.py` require the
already available document runtime (`python-docx`, `reportlab`, `Pillow`, `pypdf`).
They are authoring/test tools, not skill dependencies. Do not regenerate hashed
fixtures after dispatch; retain a new fixture version and rerun if changed.
Semantic preflight and actual rendered-page inspection live in `fixtures/qa/`;
neither substitutes for the three independent U15 answers and their group review.
