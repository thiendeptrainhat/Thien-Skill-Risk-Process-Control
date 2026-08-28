# P1-P03-V01-R1 — release-evidence audit

No material documentation-overclaim defect was identified in the defined scope. All four P03 invariants are supported by the inspected evidence. This is a static documentation-review result, **not** a declaration that the overall release gate is complete.

- `result: pass`
- `qa_disposition: ready` — only for the four documentation/evidence assertions below.
- `approval_status: not_requested`
- `release_gate_observed: incomplete`
- Issued: 2026-08-27T20:23:23.332Z; user timezone: Asia/Ho_Chi_Minh.
- Reviewer: `/root/p1_p03_v01_r1`; relationship: `peer_review`. I did not author the five reviewed release documents. This is same-team review, not organizationally independent or third-party assurance.

## Review contract and procedures

Objective: determine whether README, INSTALL, the release manifest, Phase 3 report and platform guidance fairly represent retained release evidence under P1-P03. Criteria are the approved `docs/phase-1/ACCEPTANCE-MATRIX.yaml`, P1-P03, mirrored by `tests/phase-3/acceptance-matrix.json`; approved rubric SHA-256 is `69db89db1ccd63703526aee9c0bc6305a5499905ec75f656a754ecce5840fbcb`. Intended audience is the release owner and user; working classification is internal/private-repository material; report language is English.

QA selection: `L1_targeted`, `evidence_traceability` and `report_language_cross_artifact`, phase `initial_review`, with the security/privacy handling overlay. The QA-methodology skill supplies the separation between review result, remaining gate work and human approval.

Plan P1-P03-V01-R1-PLAN: inspect all five release-facing documents; reconcile the immutable pre-review result, current review records and static outputs; challenge selected live-capability claims; run the actual read-only validator; report each P03 invariant. All four invariant families were covered. I checked the result/evidence-reference metadata of all 29 current model reviews (95 mandatory per-run checks), the U15 group review and the P01/P02 reviews; I inspected selected detailed rationales and U06/U16 raw output/trace evidence. This was not a new grading of all 29 business answers.

The complete hashed list of 71 directly relied-on files and key executed validator dependencies is in `inputs.json`. `tests/phase-3/static/pre-release-report-review-results.json` is the immutable result basis. The mutable evidence index was read and recorded in the trace, but neither it nor `acceptance-results.json` is a hashed receipt input. The latter was not read; actual validator stdout is retained separately.

## Four invariant conclusions

### case.must_observe.1 — PASS

**Criterion:** keep static/package, behavioral and per-platform status separate.

README lines 193–201, REPORT lines 23–40 and 64–75, and manifest lines 31–43 explicitly distinguish the 29 current model variants, 61 tooling tests, registry/structure/ZIP checks and untested native surfaces. INSTALL lines 134–153 separates artifact, discovery, activation and behavior. Platform guidance lines 3–9 and 39–50 states that guidance and file placement are not live acceptance.

The evidence supports those categories: current model context `0303a497434fb718` has 29 reviewed passes; the separate static context `4a134d99a9f37949` contains P01/P02. Their actual outputs report 48/49/49 files, normalized parity and matching package hashes, and expressly disclaim model/installation acceptance. Current review records contain 95/95 passing mandatory judgments and nonempty evidence references, with a separate passing U15 cross-format comparison.

Evidence locators: `pre-release-report-review-results.json#/claims_by_context`, `#/evidence_counts`, `#/per_platform`; `reviews/P1-U*.json#/checks` for the 29 enumerated files in inputs; `reviews/group-P1-U15-R1.json#/checks/case.group_must_observe.1`; `runs/P1-P01-V01-R1/artifacts/output.json#/packages` and the equivalent P02 output; `static/final-verification-commands.json#/commands`. Paths in this paragraph are under `tests/phase-3/`.

### case.must_observe.2 — PASS

**Criterion:** unrun cases remain not_run; missing evidence remains inconclusive or executed_unreviewed, not pass.

REPORT lines 5, 36, 69–75 and 81–84 and README lines 197–201 preserve the boundaries. The pre-review snapshot and this audit's actual validator result both retain the four round-1 U01/U02/U04/U19 runs as `executed_unreviewed`; that older snapshot is ineligible for the current release. Claude Desktop/Web and ChatGPT Desktop/Web remain `not_run`. The plan-label Codex surface also remains `not_run`, distinct from the actual delegated surface reported as `tested_partial`.

At validator time, P03 itself is `not_run` in `variant_coverage`, with no recorded result; distribution integrity is `partial` and the gate is `incomplete`. REPORT deliberately delegates final gate status to the derived result and does not self-certify P03. That sequencing is expected, not a defect.

Evidence locators: `tests/phase-3/static/pre-release-report-review-results.json#/runs`, `#/claims_by_context`, `#/variant_coverage`, `#/current_release_gate`; matching fields in retained `validator-output.json`. U16 raw output lines 49–53 and its retained specialist trace preserve the unresolved approval-role field and three pending human-review items even though the bounded behavior review passed.

### case.must_observe.3 — PASS

**Criterion:** retain the historical 104 registry / 28 provisional records separately from new-release results.

README lines 195–201 and REPORT lines 34 and 79–84 do not count the legacy registry or provisional summaries as 1.1.0 behavioral passes. The original `tests/acceptance-report.md`, “Behavioral status”, says the deterministic runner did not execute the 28 planned tests. `tests/behavioral-report.md` reports 28 provisional summaries, zero verified passes and evidence-incomplete acceptance.

The current legacy registry output separately reports 104 cases, 0 behavioral executions and 28 selected/not_run. The P01/P02 actual outputs' `preserved_historical_files` entries are all true for the legacy reports, case/results files and 1.0.0 archives; the later final-verification record repeats the preservation checker successfully. I inspected those retained preservation results rather than independently reperforming Git-baseline byte comparisons.

Evidence locators: `tests/phase-3/static/legacy-registry.json#/case_count` and `#/behavioral`; both historical reports above; `tests/phase-3/runs/P1-P02-V01-R1/artifacts/output.json#/preserved_historical_files`; `tests/phase-3/static/final-verification-commands.json#/commands` for `inspect_release.py`.

### case.must_not_observe.1 — PASS — forbidden behavior not observed

**Criterion:** do not claim cross-platform verification from one runtime or award pass to a test specification.

README lines 11–12, 63–78 and 195–201, INSTALL lines 3, 34, 86–112 and 174–176, manifest lines 34–43, REPORT lines 5, 11, 19 and 64–88, and platform guidance lines 6–9 and 62–79 consistently qualify the scope. The exact model ID stays null/not_available. Instructions to install, smoke prompts and the approved not_run specification are not presented as executed acceptance. Reviewer involvement in skill/fixture authoring and the absence of third-party assurance are disclosed.

The selected capability claims also stay within retained evidence: U06 raw output lines 19–33 distinguishes NIST passages actually read from the oversized/unread catalog; its trace records actual web calls 14–21 and failures. U16 retains a fresh specialist dispatch, a 37-event specialist trace, one page with zero native-text characters, local rendering/platform-native vision and “OCR NOT_EXECUTED”; the report makes the same distinctions. No new web request, OCR or specialist invocation occurred in this audit.

Evidence locators: `tests/phase-3/reviews/P1-U06-V01-R1.json#/checks`; `runs/P1-U06-V01-R1/artifacts/tool-trace.json#/tool_calls`; `runs/P1-U16-V01-R1/artifacts/specialist-dispatch-tool-call.json`; `runs/P1-U16-V01-R1/artifacts/document-evidence/tool-trace.json#/methods`, `#/coverage` and `#/unresolved_review_items`; `runs/P1-U16-V01-R1/artifacts/document-evidence/native-inspection.json#/pages/0/native_text_char_count`. The shortened run paths are under `tests/phase-3/`.

## Actual validator result and reconciliations

Executed once, read-only: `python3 -B scripts/run_tests.py --phase3 --json`. Exit code **0**; generated_at **2026-08-27T20:17:08+00:00**. Complete parsed stdout is retained in `validator-output.json`.

- Integrity: `pass`; errors: **0**.
- Acceptance and current release gate: **incomplete**, with P03 not yet registered.
- 35 retained receipts = **29 current model + 2 static + 4 historical unreviewed**. The 31 pass receipts are 29 model plus two static, not 31 model passes.
- Current model claims for core business logic, backward compatibility and the separately tested capabilities are verified in the scoped current context; distribution integrity is partial pending P03.
- Current model runs comprise **23 nonsimulated + 6 simulated-capability profiles**. The per-platform aggregate of 27 nonsimulated runs also includes four historical runs; it is not the denominator for current model acceptance.
- Current snapshot has **49 files** and content SHA-256 `c438e1c23ea70b5ea14e5092841580cb3938a14e49499f870db0eb6aaf9adc2a`, matches canonical, and is distinct from the historical snapshot.
- Retained static records support 61 tooling tests, nine canonical check groups, 21 YAML files/174-character description, 64 fixture hashes, and reproducible package checks. The supplemental final build reports `publication: unchanged` and `release_acceptance: not_determined_by_builder`.

## Findings, limits and handoff

Open defect counts: Critical 0, High 0, Medium 0, Low 0. No source repair was made or is proposed by this audit. Absence of an identified P03 defect is not assurance that all source content, external guidance, business answers or platforms are correct.

Limitations: targeted static review; no fresh business/model runs, native installation/discovery, UI or external-source revalidation, complete security/legal/content-rights assessment, independent host-transcript authentication or new Git-baseline preservation reperformance. The traces are executor-maintained, not complete host transcripts; hidden context and exact model identity remain unavailable. Finite synthetic runs and simulated capability restrictions do not establish general performance or platform capability. Official platform URLs were not reopened because this audit prohibits network use.

Parent action: retain these artifacts, perform the separate root per-invariant review, register the actual P03 evidence and regenerate the derived acceptance result. Only then report the gate actually returned. Keep installation, human approval and publication authority separate. The remaining registration step does not change this audit's bounded documentation conclusion.

The initial dispatch was truncated; the parent's clarification directed me to the full saved dispatch prompt. That clarification, actual command/read list, output-display recoveries and timestamps are retained in `tool-trace.json`.
