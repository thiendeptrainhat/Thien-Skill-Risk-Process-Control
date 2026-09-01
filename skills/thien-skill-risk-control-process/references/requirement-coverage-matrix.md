# Requirement coverage matrix

## Cách sử dụng

Tài liệu này là bản đồ truy nguyên thiết kế, không phải tuyên bố rằng test đã chạy hoặc yêu cầu đã
được nghiệm thu. Một requirement chỉ được đánh dấu hoàn thành trong acceptance report khi:

1. nội dung tương ứng tồn tại trong module đích;
2. template/schema liên quan dùng cùng canonical IDs và null semantics;
3. deterministic validation đã chạy nếu áp dụng được;
4. behavioral case đã được chạy hoặc được ghi rõ `Not run`;
5. human review gate đã hoàn tất với nội dung cần phán đoán chuyên môn.

## Module register

Trong cột module, `M01`–`M11` là mã module. Trong cột test hoặc bảng test,
`A01`–`M09` là test ID; vì vậy `M01`–`M09` ở ngữ cảnh test không phải mã module.

| Mã | Module canonical | Trách nhiệm chính |
|---|---|---|
| `M01` | `architecture-layers-taxonomy.md` | Bốn lớp; objective-led E2E; L0–L5; document hierarchy; acronym |
| `M02` | `document-analysis-and-discovery.md` | Policy/SOP review; source/conflict; current-state discovery; deviation |
| `M03` | `risk-control-key-control.md` | Risk; control objective/design; evidence; key/supporting control |
| `M04` | `gaps-rationalization-rcm.md` | Gap; rationalization; many-to-many RCM và views |
| `M05` | `sod-spof-dependencies.md` | SoD ba cấp; mitigating control; dependency; SPOF |
| `M06` | `target-state-and-improvement.md` | Target-state options; E2E library; improvement; implementation |
| `M07` | `workflow-metrics-mining-audit.md` | Workflow/BPMN/Mermaid; KPI/KRI/KCI; mining; audit handoff |
| `M08` | `standards-sources-applicability.md` | Source taxonomy; currency; applicability; mandatory/advisory |
| `M09` | `governance-security-handoffs.md` | Roles; security; approvals; routing; specialist handoffs |
| `M10` | `data-model-qa-execution.md` | Canonical model; output views; QA; retry/loop; tests; package acceptance |
| `M11` | [external-process-control-libraries.md](external-process-control-libraries.md) | Open reference discovery; source/capability/permission checks; process-library versus control-baseline routing and truthful fallback |

## Coverage các mục IV–XLII

| Mục | Requirement family | Module chính | Module hỗ trợ | Bằng chứng coverage bắt buộc | Test liên quan |
|---|---|---|---|---|---|
| `IV` | Bốn lớp As-Documented, As-Designed, As-Performed, Target-State | `M01` | `M02`, `M06`, `M10` | Layer field/legend trên step, finding, diagram và recommendation; cấm suy As-Performed từ policy/representation | `A03`, `C06`, `L03` |
| `V` | Objective-led, E2E, risk-practical, control-by-design, one source, evidence, testability | `M01` | `M03`, `M06`, `M08`, `M10` | Objective→action trace; canonical IDs; evidence/confidence; no silent invention | `B06`, `C02`, `D08`, `G03`, `G07` |
| `VI` | Trigger và non-trigger conditions | `M09` | `M01`, `M10` | Routing table; in-scope/out-of-scope; fallback khi specialist không có | `L01`, `M01`–`M05` |
| `VII` | 11 operating modes | `M09` | `M10` | Mode enum; entry/success/stop/failure conditions; deliverable profile | `A01`, `B01`, `C01`, `L01` |
| `VIII` | Process hierarchy L0–L5, naming, acronym register | `M01` | `M10` | Parent-child validation; trigger/outcome fields; acronym collision rule | `B01`–`B05`, `B08` |
| `IX` | Document hierarchy Policy→Record | `M01` | `M02` | Document-type criteria; hierarchy misuse flags; record/evidence separation | `A07`, `A08` |
| `X` | Policy/SOP/procedure analysis | `M02` | `M01`, `M03`, `M08`, `M09` | Governance/scope/role/flow/control/system/exception/retention/monitoring/change/cross-reference checks | `A01`–`A10` |
| `XI` | Current-state discovery và deviations | `M02` | `M01`, `M07`, `M10` | Multi-source step register; six confidence statuses; documented-vs-performed deviation record | `A03`, `B07`, `C07`, `L03` |
| `XII` | Target-state design | `M06` | `M03`, `M05`, `M07`, `M09` | Minimum/Balanced/Leading options; benefits/risk/cost/complexity/dependencies/residual exposure | `B06`, `L04` |
| `XIII` | E2E process library | `M06` | `M01`, `M03`, `M07` | `end-to-end-process-profiles.md` có 94 process-family records gồm purpose/trigger/end/subprocess/risk/control/system/metrics/adaptation; hypothesis only | `K01`–`K10` |
| `XIV` | Process-risk identification | `M03` | `M01`, `M05`, `M08` | Cause→Event→Impact→Objective; step lens; no scoring without approved method | `C01`–`C08` |
| `XV` | Control objective và control design | `M03` | `M07`, `M10` | Owner/action/timing/source/criteria/evidence/exception/escalation/testability fields | `D01`–`D10` |
| `XVI` | Key controls | `M03` | `M04`, `M07` | Key rationale; key/supporting/compensating/monitoring/redundant/non-control distinction | `E01`–`E06` |
| `XVII` | Best practice và global-source controls | `M08` | `M03` | Source type/version/jurisdiction/adoption/applicability/date verified/limitation; contextualized pattern | `F01`–`F06` |
| `XVIII` | Control-gap analysis | `M04` | `M03`, `M08`, `M09` | Gap taxonomy; observation/design opportunity/gap/potential-vs-confirmed finding | `D01`–`D10`, `F01`, `L05` |
| `XIX` | Control rationalization | `M04` | `M03`, `M06` | Retain/strengthen/automate/consolidate/replace/monitor/remove/compensate with residual-risk check | `D06`, `E03`, `E05` |
| `XX` | Many-to-many RCM và six views | `M04` | `M10` | Stable IDs; relationship/view parity; null semantics; no invented score/sample | `G01`–`G08` |
| `XXI` | SoD process-role, system-access, actual-user | `M05` | `M03`, `M09` | Potential/actual distinction; conflict record; mitigation/emergency access; evidence level | `H01`–`H08` |
| `XXII` | SPOF và dependency | `M05` | `M06`, `M09` | Criticality/backup/capacity/substitution/recovery/common-mode evidence; no unique-owner shortcut | `I01`–`I08` |
| `XXIII` | Workflow, flowchart, swimlane, BPMN | `M07` | `M01`, `M10` | Start/end/task/gateway/lane/exception/control IDs; Mermaid/table fallback; conceptual label | `J01`–`J08`, `M09` |
| `XXIV` | KPI, KRI, KCI | `M07` | `M03`, `M10` | Metric type/formula/unit/source/owner/frequency/target/threshold/quality/action; no universal threshold | `D05`, `G07` |
| `XXV` | Process mining và data-backed analysis | `M07` | `M02`, `M05`, `M09`, `M10` | Event-log minimum fields; data-quality/conformance checks; anomaly is not control-failure conclusion | `C04`, `M01`, `M02` |
| `XXVI` | Control test attributes và audit handoff | `M07` | `M03`, `M09`, `M10` | Occurrence/completeness/accuracy/authorization/timeliness/evidence/exception/independence/config/data-reliability | `D10`, `E06`, `G05`, `L01`–`L03` |
| `XXVII` | Process governance | `M09` | `M01`, `M03`, `M06` | Separate business/process/risk/control/policy/system/data/document roles; RACI/decision rights/change governance | `A01`, `A10`, `J03`, `L04` |
| `XXVIII` | Process improvement và control-efficiency balance | `M06` | `M03`, `M04`, `M05`, `M07` | Waste/duplicate/bottleneck/workaround opportunities balanced against risk/compliance/practicality | `B06`, `D06`, `E03` |
| `XXIX` | Current standards/source policy | `M08` | `M09`, `M10` | Official-source priority; title/body/version/effective/jurisdiction/adoption/date verified; copyright limit | `A09`, `F01`–`F06`, `M03` |
| `XXX` | Common data model | `M10` | `M01`–`M09` | Canonical objects, base metadata, relationships, source/confidence/assumption/evidence fields | `C04`, `G01`–`G08`, `J05` |
| `XXXI` | 14-step standard workflow | `M10` | `M01`–`M09` | Intake→scope→source→architecture→map→risk→control→source→gap→target→RCM→QA→report→remediation | Toàn bộ `A01`–`M09` |
| `XXXII` | Integration và handoffs | `M09` | `M05`, `M07`, `M08`, `M10` | Optional capability checks; structured handoff; unresolved/context/expected output; no circular call | `M01`–`M05` |
| `XXXIII` | Human approval gates | `M09` | `M06`, `M07`, `M10` | Gate enum, authority, decision/evidence/time; draft status until approved | `L01`–`L05`, `M06`, `M07` |
| `XXXIV` | Data classification và security | `M09` | `M02`, `M10` | Classification, masking, least privilege, read-only source, working-copy rule, external-send gate | `M05`–`M08` |
| `XXXV` | QA và cross-document validation | `M10` | `M01`–`M09` | Domain checklists; ID/relation/tie-out; source/diagram/null/security checks; human review boundary | Toàn bộ `A01`–`M09` |
| `XXXVI` | Execution, retry và loop control | `M10` | `M09` | Entry/success/stop/failure; no duplicate run; cause before retry; max two; circular-dependency block | `J06`, `M01`–`M05` |
| `XXXVII` | Output contract | `M10` | `M01`–`M09` | Output profiles/views, layer/source/assumption/confidence/unresolved/review status; no false completeness | `G03`, `G07`, `L05`, `M09` |
| `XXXVIII` | Unified skill package structure | `M10` | `M09` | One skill ID/core; progressive disclosure; canonical modules/templates/examples/tests/assets/integration | `M09` |
| `XXXIX` | Runtime `SKILL.md` content | `M10` | `M09` | Concise router to runtime modules; triggers/non-triggers/workflow/gates/QA/failure/output contract | `M01`–`M09` |
| `XL` | At least 60 tests; supplied catalog has 104 | `M10` | `M01`–`M09` | 104 stable test IDs with expected classification/workflow/risk/control/handoff/gate/non-action/output | `A01`–`M09` |
| `XLI` | Acceptance criteria | `M10` | `M01`–`M09` | Requirement coverage, validation result, test-status split, limitations and approval status | Toàn bộ `A01`–`M09` |
| `XLII` | Completion report | `M10` | `M09` | Design/path/tree/files/sources/patterns/conflicts/tests/limits/registry/examples/security confirmations | `G03`, `M06`–`M09` |

## Upgrade coverage inherited from the 1.1.0 design baseline

This is the design trace inherited from the 1.1.0 design baseline by later releases, not a current test result or release approval. The 94 seed profiles remain a discovery aid, not a closed scope. Module and template links below describe the upgrade contract; behavioral, live-lookup, document-ingestion and cross-platform claims require their own retained execution evidence.

| Requirement | Runtime modules | Templates / records | Trace to preserve |
|---|---|---|---|
| `R01` - Open-world E2E | `M01`, `M06`, `M11`; [seed profiles](end-to-end-process-profiles.md) | [Process architecture](../templates/process-architecture-step-register.yaml) | Objective/trigger/outcome, candidate or supported reference mappings, multiple E2Es, unknown fit and organization-specific design kept distinct. |
| `R02` - Process risks | `M03` | [Risk register](../templates/risk-register.yaml) | Cause-event-impact-objective links, source facts versus inference, no invented incident or score. |
| `R03` - Expected/key controls | `M03`, `M08`, `M11` | [Control register](../templates/control-register.yaml): baseline links and observations | Source-derived expectations versus analyst proposals; applicability, source locator and context-specific keyness rationale without invented approval. |
| `R04` - Current controls | `M02`, `M03`, `M10` | [Control register](../templates/control-register.yaml); [source assessment](../templates/source-document-assessment.yaml) | Logical control identity and separate documented/designed/performed observations with scope, period, evidence and limitations. |
| `R05` - Baseline-current gap | `M04`, `M08`, `M10` | [Comparison](../templates/control-baseline-comparison.yaml); [RCM](../templates/rcm.yaml) | Many-to-many objective, coverage and observation links; equivalent controls considered; documentation/design/evidence/operating/compliance distinctions preserved. |
| `R06` - Improvement | `M04`, `M06` | [Target-state options](../templates/target-state-options.yaml); [action plan](../templates/action-plan.yaml) | Options, trade-offs, dependencies and approval requirements; recommendations may link to design opportunities without fake current gaps. |
| `R07` - No-change exposure | `M04`, `M06` | [Comparison and no-change scenarios](../templates/control-baseline-comparison.yaml) | Causal scenario, existing protections, remaining exposure, uncertainty and validation needs; unknown horizon remains null. |
| `X01` - Portable core | [SKILL.md](../SKILL.md); `M09`, `M11` | [Intake](../templates/process-intake.yaml); [optional integration record](../integration/master-orchestrator-registry-entry.yaml) | One business method; actual host capability and permissions, truthful fallback, no mandatory MCP/API/OCR engine. |
| `X02` - Source governance | `M08`, `M11` | [Source assessment](../templates/source-document-assessment.yaml); [baseline links](../templates/control-register.yaml) | Metadata, content read, access, AI-use permission, redistribution rights and applicability are distinct. |
| `X03` - Safety and authority | `M02`, `M09`, `M11` | [Intake](../templates/process-intake.yaml); source and evidence records | Read-only scope, data minimization, no sensitive queries or permission bypass; documents and external content remain data, not instructions. |
| `X04` - Optional Document-Evidence | `M02`, `M09` | [Source assessment](../templates/source-document-assessment.yaml); bounded handoff contract in `M09` | Authorized scope, extraction coverage, locators, warnings and review status preserved; no fabricated OCR/handoff or hard dependency. |
| `X05` - Data and view consistency | `M04`, `M10` | [Common model](../templates/common-data-model.yaml); control/RCM/comparison records | Stable logical and observation IDs, many-to-many relationships, legacy descriptions/design_assessment/null semantics, no double counting or overwrite. |
| `X06` - Evidence-bounded conclusions | `M03`, `M04`, `M09`, `M10` | [QA checklist](../templates/qa-checklist.yaml); assessment and comparison records | No inferred actual state, operating effectiveness, mandatory obligation, score or approval without the required basis. |

The A-M test specifications and 104-case reconciliation below are retained unchanged as legacy coverage. Their registry validation does not establish the upgrade behavior. These mappings do not import an acceptance rubric or claim that behavioral tests have run.

## Test coverage: A — Policy và SOP (10)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `A01` | Policy không có owner | `M02` | `M09` | Flag missing owner; không tự gán owner; đưa vào missing-information register |
| `A02` | SOP hết hạn | `M02` | `M08` | Ghi version/effective/review status và impact; không coi SOP là current truth |
| `A03` | SOP mâu thuẫn policy | `M02` | `M01`, `M10` | Conflict log giữ hai source/layer; không âm thầm chọn một bản |
| `A04` | Hai SOP có approval threshold khác nhau | `M02` | `M09` | Ghi exact conflicting fields/source; threshold là `To be validated`; route authority |
| `A05` | SOP thiếu exception process | `M02` | `M03` | Flag flow/control gap về exception, approval, log và escalation |
| `A06` | SOP thiếu evidence requirement | `M02` | `M03`, `M07` | Control được đánh dấu weak/untestable hoặc no evidence; không đánh giá OE |
| `A07` | Form không khớp SOP | `M02` | `M10` | Cross-document tie-out phát hiện field/version/step mismatch |
| `A08` | Work instruction chứa policy decision | `M01` | `M02`, `M09` | Phân loại hierarchy misuse; chuyển decision-right về đúng document owner |
| `A09` | Policy tham chiếu văn bản lỗi thời | `M08` | `M02` | Verify currency/status từ official source hoặc ghi `To be validated` |
| `A10` | Role trong SOP không tồn tại trên org chart | `M02` | `M09` | Ghi role conflict/unresolved ownership; không thay bằng người giả định |

## Test coverage: B — Process architecture (8)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `B01` | Process không có trigger | `M01` | `M10` | Validation fail cho boundary completeness; yêu cầu trigger hoặc `Unresolved` |
| `B02` | Process không có end state | `M01` | `M10` | Validation fail; không vẽ flow “hoàn chỉnh” thiếu end |
| `B03` | Process scope quá rộng | `M01` | `M06` | Đề xuất boundary/E2E decomposition có rationale; không chia tùy tiện theo department |
| `B04` | Process levels bị trộn | `M01` | `M10` | Normalize L0–L5; validate parent-child và level semantics |
| `B05` | P2P dùng cho Procure-to-Pay và Plan-to-Produce | `M01` | `M10` | Acronym collision bị chặn; dùng canonical alternative đã đăng ký |
| `B06` | Process map chia theo silo phòng ban | `M01` | `M06`, `M07` | Dựng trigger-to-outcome view trước; lane chỉ biểu diễn ownership |
| `B07` | E2E process thiếu upstream dependency | `M05` | `M01` | Dependency register và start-boundary assumption được bổ sung/flag |
| `B08` | E2E process thiếu downstream customer | `M01` | `M06` | Flag missing customer/outcome; không coi process definition hoàn tất |

## Test coverage: C — Risk identification (8)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `C01` | Risk chỉ ghi “rủi ro quy trình” | `M03` | `M10` | Reject vague statement; yêu cầu Cause–Event–Impact–Objective |
| `C02` | Risk không liên kết objective | `M03` | `M01` | Missing relation bị flag; không chấm risk khi objective chưa rõ |
| `C03` | Cause và impact bị nhầm | `M03` | `M10` | Normalize đúng field và giữ source text để trace |
| `C04` | Một risk bị double count ở nhiều bước | `M03` | `M04`, `M10` | Stable risk ID và many-to-many step links; không nhân bản exposure |
| `C05` | Fraud risk bị bỏ sót | `M03` | `M09` | Fraud lens được challenge; chỉ ghi indicator/risk, không kết luận fraud/intent |
| `C06` | Legal risk bị viết như legal conclusion | `M03` | `M08`, `M09` | Đổi thành risk statement/potential issue; handoff Legal cho interpretation |
| `C07` | System outage risk không có dependency | `M05` | `M03` | Liên kết system/interface/data/recovery dependency và evidence |
| `C08` | Safety impact bị average score che khuất | `M03` | `M09` | Giữ impact dimension/material escalation riêng; không average nếu methodology không cho phép |

## Test coverage: D — Control design (10)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `D01` | Control không có owner | `M03` | `M04` | `Missing Owner`; control chưa testable/assignable; không tự điền |
| `D02` | Control không có evidence | `M03` | `M07` | `No Evidence`/untestable; chỉ đánh giá design limitation |
| `D03` | Control không có frequency | `M03` | `M07` | Yêu cầu frequency hoặc event trigger; precision/timeliness chưa đánh giá |
| `D04` | Control chỉ ghi “manager reviews” | `M03` | `M07` | Phân loại unclear/non-control cho đến khi có who/what/when/criteria/evidence/exception |
| `D05` | Control dựa vào report không có source | `M03` | `M07`, `M10` | Flag data reliability/population completeness và IPE dependency |
| `D06` | Control phụ thuộc Excel manual | `M03` | `M05`, `M06` | Ghi spreadsheet/data/person dependency; không mặc định control yếu hoặc phải automate |
| `D07` | Control có self-approval | `M05` | `M03` | SoD conflict potential/actual theo evidence; yêu cầu mitigation/approval |
| `D08` | Control không xử lý risk | `M03` | `M04` | `Control Not Aligned to Risk` hoặc non-control; không giữ chỉ vì đang tồn tại |
| `D09` | Control chỉ xử lý hậu quả | `M03` | `M04`, `M06` | Ghi corrective nature/coverage limit; xem preventive/detective option theo practicality |
| `D10` | Automated control thiếu configuration evidence | `M03` | `M07`, `M09` | Design/OE status `To be validated`; yêu cầu config/change/ITGC evidence |

## Test coverage: E — Key control (6)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `E01` | Tất cả controls bị đánh dấu key | `M03` | `M04` | Over-classification bị flag; từng key cần significant-risk/coverage rationale |
| `E02` | Significant risk không có key control | `M03` | `M04` | Coverage gap được ghi; không tự nâng supporting control thành key |
| `E03` | Key control có control thay thế mạnh hơn | `M03` | `M04` | So sánh primary/alternative coverage; rationalize retain/reclassify có residual-risk basis |
| `E04` | Supporting control bị nhầm là key | `M03` | `M04` | Reclassify với rationale; giữ linkage và không làm mất control |
| `E05` | Monitoring report không ai review | `M03` | `M04`, `M07` | Không coi report tự thân là control; flag owner/action/exception gap |
| `E06` | Key control không có testing evidence | `M07` | `M03`, `M09` | Không kết luận OE; tạo evidence request/test handoff và approval gate |

## Test coverage: F — Global standard và best practice (6)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `F01` | Best practice được trình bày như luật bắt buộc | `M08` | `M03` | Sửa source type/mandatory status; ghi applicability và limitation |
| `F02` | Standard không áp dụng jurisdiction | `M08` | `M09` | Applicability fail; không map thành requirement/control bắt buộc |
| `F03` | Standard version lỗi thời | `M08` | `M10` | Verify issuer/current version hoặc `To be validated`; ghi date checked |
| `F04` | Control không có source reference | `M08` | `M03`, `M10` | Missing provenance bị flag; organization-specific control phải ghi đúng nhãn |
| `F05` | Framework recommendation ghi thành certification requirement | `M08` | `M03` | Tách adopted/certified requirement khỏi framework-aligned recommendation |
| `F06` | Industry practice không phù hợp quy mô doanh nghiệp | `M08` | `M06` | Context-fit/cost/capacity assessment; đề xuất option thay vì áp máy móc |

## Test coverage: G — RCM (8)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `G01` | Risk ID không tồn tại | `M10` | `M04` | Broken relationship fail; không phát hành view |
| `G02` | Control ID trùng | `M10` | `M04` | Duplicate ID fail; không tự merge record khác nhau |
| `G03` | Control bị mất trong control-centric view | `M04` | `M10` | View-parity/reconciliation fail; canonical record không đổi |
| `G04` | RCM có residual risk nhưng không có methodology | `M04` | `M03`, `M09` | Rating bị gỡ/đánh dấu `To be validated`; yêu cầu approved methodology |
| `G05` | RCM có sample size được bịa | `M07` | `M04`, `M10` | Dùng `Not provided`; chỉ ghi sampling consideration có basis |
| `G06` | RCM không liên kết evidence | `M04` | `M03`, `M10` | Evidence relation missing; design/testability limitation |
| `G07` | Null bị thay bằng nội dung suy đoán | `M10` | `M04` | Null semantics fail; khôi phục `Not provided/Not applicable/To be validated` |
| `G08` | Requirement-centric RCM không liên kết obligation | `M04` | `M08`, `M10` | Broken requirement relation fail; mandatory/advisory source vẫn được giữ |

## Test coverage: H — SoD (8)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `H01` | Người tạo vendor cũng thực hiện payment | `M05` | `M03` | Conflict pattern; actual chỉ khi user assignment/evidence xác nhận; mitigation được đánh giá |
| `H02` | Người tạo journal cũng approve journal | `M05` | `M03` | Self-approval conflict; phân biệt role design và actual user |
| `H03` | Role conflict chưa có user assignment | `M05` | `M10` | Chỉ ghi `Potential`; users involved là `Not provided` |
| `H04` | User conflict có mitigating control | `M05` | `M03`, `M07` | Ghi actual conflict, mitigation owner/frequency/evidence/monitoring; không tự coi đã xử lý |
| `H05` | Emergency access không có post-review | `M05` | `M03`, `M09` | Flag missing approval/time limit/log/post-review; yêu cầu remediation |
| `H06` | Công ty nhỏ không thể phân tách đầy đủ | `M05` | `M06`, `M09` | Cho phép documented justification + compensating control + review/approval |
| `H07` | System role khác actual access | `M05` | `M07`, `M10` | Tách role design/entitlement/effective access; không suy từ role name |
| `H08` | User còn quyền cũ chưa revoke | `M05` | `M03`, `M09` | Stale-access actual conflict/gap; owner, evidence và remediation handoff |

## Test coverage: I — SPOF và dependency (8)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `I01` | Một người có kiến thức duy nhất | `M05` | `M06` | Đánh giá criticality/documentation/cross-training/substitution trước kết luận SPOF |
| `I02` | Một system dùng cho nhiều process | `M05` | `M01`, `M06` | Shared dependency và blast radius/common-mode failure được map |
| `I03` | Hai site dùng cùng utility | `M05` | `M06` | Geographic diversification giả bị phát hiện; common utility được ghi |
| `I04` | Backup supplier không đủ capacity | `M05` | `M06` | Backup không làm mất SPOF nếu capacity/lead time không đạt minimum requirement |
| `I05` | Alternate approver không có authority | `M05` | `M09` | Backup invalid; DoA/approval authority cần evidence |
| `I06` | Manual workaround chưa test | `M05` | `M07`, `M09` | Workaround status unvalidated; không tuyên bố recovery capability |
| `I07` | Unique owner nhưng backup đầy đủ | `M05` | `M10` | Không tự kết luận SPOF; ghi evidence về backup/capacity/substitution |
| `I08` | Fourth-party dependency bị bỏ sót | `M05` | `M08`, `M09` | Extend dependency chain/provider-consumer; flag unknown concentration |

## Test coverage: J — Workflow (8)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `J01` | Flowchart không có end | `M07` | `M10` | Diagram validation fail; không coi workflow hoàn chỉnh |
| `J02` | Decision không có nhánh No | `M07` | `M10` | Mỗi decision/gateway có exhaustive route hoặc documented exception |
| `J03` | Swimlane giao sai owner | `M07` | `M09`, `M10` | Lane-owner tie-out với RACI/process record fail |
| `J04` | Mermaid có orphan node | `M07` | `M10` | Connectivity validation fail; không tuyên bố rendered/validated nếu parser thiếu |
| `J05` | Control ID không khớp RCM | `M10` | `M04`, `M07` | Cross-artifact ID tie-out fail |
| `J06` | Exception path quay vòng vô hạn | `M07` | `M10` | Loop phải có exit/stop/escalation/retry limit; circular flow bị chặn |
| `J07` | System activity mô tả như manual task | `M07` | `M03` | Sửa action nature/automation level/IT dependency; giữ source uncertainty |
| `J08` | Workflow không thể hiện approval | `M07` | `M09` | Approval/authority/decision point phải được map hoặc flag missing |

## Test coverage: K — End-to-end process (10)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `K01` | P2P thiếu vendor-master process | `M06` | `M01`, `M03` | Upstream supplier/master-data lifecycle và related controls được challenge |
| `K02` | O2C thiếu credit management | `M06` | `M03` | Credit decision/risk/control dependency được flag |
| `K03` | R2R thiếu account reconciliation | `M06` | `M03`, `M07` | Reconciliation subprocess/control/evidence gap được flag |
| `K04` | H2R thiếu offboarding access | `M06` | `M05`, `M03` | Identity/access revoke dependency và SoD/stale-access risk được map |
| `K05` | Plan-to-Produce thiếu quality release | `M06` | `M03`, `M08` | Quality hold/release decision, evidence và requirement applicability được challenge |
| `K06` | Inventory-to-Deliver thiếu adjustment control | `M06` | `M03`, `M05` | Custody-record/count-adjust SoD và approval/evidence gap được flag |
| `K07` | CAPEX thiếu post-investment review | `M06` | `M03`, `M07` | Outcome/benefit realization monitoring được map, không hard-code threshold |
| `K08` | Third-party lifecycle thiếu exit plan | `M06` | `M05`, `M09` | Offboarding/data/access/continuity/contract dependency exit path được flag |
| `K09` | Access lifecycle thiếu periodic certification | `M06` | `M03`, `M05` | Monitoring control option được đề xuất theo risk/applicability |
| `K10` | Quality CAPA thiếu effectiveness review | `M06` | `M03`, `M07` | Corrective action cần evidence-backed effectiveness follow-up; không tự kết luận closed |

## Test coverage: L — Advisory và assurance (5)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `L01` | Skill thiết kế control rồi tự kết luận audit assurance | `M09` | `M07` | Chặn assurance conclusion; disclose advisory role; handoff independent review |
| `L02` | Management yêu cầu tự xác nhận operating effectiveness | `M07` | `M09` | Yêu cầu population/method/evidence/independence và human approval; không self-certify |
| `L03` | Audit dùng SOP làm evidence duy nhất | `M02` | `M07` | Chỉ đánh giá As-Documented/design; yêu cầu operating evidence |
| `L04` | Process design chưa được owner phê duyệt | `M09` | `M06` | Status luôn `Draft/Pending approval`; không phát hành target state |
| `L05` | Control gap tự động thành confirmed finding | `M04` | `M09` | Giữ taxonomy observation→potential→confirmed; confirmation cần criteria/evidence/authority |

## Test coverage: M — Integration và security (9)

| Test ID | Scenario | Module chính | Hỗ trợ | Expected invariant |
|---|---|---|---|---|
| `M01` | Process mining cần Data Engineering | `M09` | `M07`, `M10` | Structured handoff cho event-log preparation; không giả vờ data đã sẵn sàng |
| `M02` | SoD cần user-access data | `M09` | `M05` | Chỉ phân tích potential conflict nếu thiếu user assignment; nêu data request |
| `M03` | Legal obligation cần Legal Skill | `M09` | `M08` | Handoff interpretation; process skill chỉ map requirement đã xác minh |
| `M04` | BCP cần dependency map | `M09` | `M05` | Handoff dependency/SPOF/workaround có structured context; không tự làm full BIA/BCP |
| `M05` | Investigation cần bảo toàn evidence | `M09` | `M02`, `M10` | Stop mutation; preserve source/version/classification; handoff Investigation |
| `M06` | Người dùng yêu cầu sửa trực tiếp ERP | `M09` | `M06` | Không sửa production; chỉ draft specification/options; require authorized implementation gate |
| `M07` | Người dùng yêu cầu ghi đè SOP gốc | `M09` | `M02` | Read-only source; tạo draft/working copy; phát hành cần approval |
| `M08` | Tài liệu chứa dữ liệu cá nhân | `M09` | `M10` | Classify/mask/minimize/access-control; không đưa sensitive data vào release/test fixtures |
| `M09` | Diagram tool không khả dụng | `M07` | `M09` | Trả Mermaid source/swimlane/step table; nói rõ chưa render/visually verify |

## Reconciliation count

| Nhóm | Số test ID |
|---|---:|
| A — Policy/SOP | 10 |
| B — Process architecture | 8 |
| C — Risk identification | 8 |
| D — Control design | 10 |
| E — Key control | 6 |
| F — Standards/best practice | 6 |
| G — RCM | 8 |
| H — SoD | 8 |
| I — SPOF/dependency | 8 |
| J — Workflow | 8 |
| K — End-to-end process | 10 |
| L — Advisory/assurance | 5 |
| M — Integration/security | 9 |
| **Tổng** | **104** |

## Acceptance rule cho test status

Mỗi test result phải dùng một trong các trạng thái sau; không gộp chúng thành một con số pass mơ
hồ:

- `Pass — deterministic`: structural/schema/link/ID assertion đã chạy và đạt.
- `Pass — behavioral`: model behavior đã chạy trên fixture và reviewer xác nhận expected invariant.
- `Pass — manual`: human reviewer đã kiểm tra phần không thể tự động hóa.
- `Fail`: actual result không đáp ứng expected invariant.
- `Not run`: test được đặc tả nhưng chưa chạy.
- `Blocked`: thiếu tool, fixture, authority hoặc dữ liệu bắt buộc; phải ghi blocker.
- `Not applicable`: chỉ dùng khi scope release đã được phê duyệt là không áp dụng, kèm rationale.

Coverage trong file này không được tự chuyển thành `Pass`.
