# Governance, security, approval gates và handoffs

## Mục lục

1. [Thiết lập process governance](#1-thiết-lập-process-governance)
2. [Phân định vai trò và decision rights](#2-phân-định-vai-trò-và-decision-rights)
3. [Áp dụng human approval gates](#3-áp-dụng-human-approval-gates)
4. [Phân loại và bảo vệ dữ liệu](#4-phân-loại-và-bảo-vệ-dữ-liệu)
5. [Điều phối integration và specialist handoff](#5-điều-phối-integration-và-specialist-handoff)
6. [Dùng handoff contract](#6-dùng-handoff-contract)
7. [Kiểm soát external action và tool](#7-kiểm-soát-external-action-và-tool)
8. [Quản lý retry, loop và failure](#8-quản-lý-retry-loop-và-failure)
9. [Thực hiện QA và cross-document tie-out](#9-thực-hiện-qa-và-cross-document-tie-out)

## 1. Thiết lập process governance

Xác định governance theo mức độ phức tạp và risk. Không tạo committee nếu owner, cadence và decision right đơn giản đã đủ.

Thiết lập tối thiểu:

- Process Owner và phạm vi accountability.
- Process review cycle và event kích hoạt review đột xuất.
- KPI/KRI/KCI review cadence, threshold owner và escalation.
- Control certification hoặc control-owner attestation khi phù hợp.
- Policy/SOP review, version, approval và withdrawal process.
- Change intake, impact assessment, approval, implementation và post-implementation review.
- Issue, action, due date, evidence và closure authority.
- Process council hoặc cross-functional forum khi L1 process đi qua nhiều function.

Tạo governance calendar:

| governance_event | cadence/trigger | owner | participants | inputs | decision/output | evidence |
|---|---|---|---|---|---|---|
| Process performance review | Monthly | Process Owner | Control/Data/System Owners | KPI/KRI/KCI pack | Actions and escalation | Approved minutes |

Không coi meeting là control nếu không có objective, criteria, evidence, exception follow-up và accountable owner.

## 2. Phân định vai trò và decision rights

Phân biệt rõ:

| Vai trò | Trách nhiệm chính |
|---|---|
| Business Owner | Bảo trợ business outcome, resource và strategic decision |
| Process Owner | Chịu trách nhiệm end-to-end process performance và design |
| Subprocess Owner | Quản lý boundary được giao trong process architecture |
| Risk Owner | Chịu trách nhiệm risk response và residual-risk decision trong authority |
| Control Owner | Chịu trách nhiệm control design, vận hành và remediation |
| Control Performer | Thực hiện control action |
| Control Reviewer | Review độc lập theo design |
| Policy Owner | Quản lý policy authority, content và lifecycle |
| System Owner | Quản lý system capability, access, configuration và lifecycle |
| Data Owner | Quyết định definition, quality, access và retention của data domain |
| Document Owner | Quản lý version, publication và review của document |
| Approver | Ra quyết định trong Delegation of Authority |

Không mặc định Process Owner đồng thời là Risk Owner, Control Owner, Policy Owner, System Owner hoặc Data Owner.

Áp dụng:

- RACI cho activity responsibility.
- Decision-right matrix cho threshold, entity, risk hoặc exception-dependent authority.
- Delegation of Authority cho approval hierarchy.
- SoD matrix cho incompatible duties.
- Alternate/delegate register cho continuity.

Kiểm tra authority tại ngày giao dịch hoặc ngày phê duyệt; không dùng matrix hiện tại để xác nhận lịch sử nếu matrix đã thay đổi.

## 3. Áp dụng human approval gates

Giữ mọi Policy, SOP, RCM và Target-State ở trạng thái `draft` cho đến khi đúng người có authority phê duyệt.

Yêu cầu human approval trước khi:

- Phê duyệt Target-State process.
- Phát hành hoặc thay đổi Policy, Standard, SOP, Procedure hay Work Instruction.
- Thay đổi approval authority, RACI, job responsibility hoặc organization structure.
- Thay đổi SoD rule, role access hoặc privileged access.
- Bỏ key control, giảm control frequency/precision hoặc chấp nhận compensating control.
- Thay manual control bằng automated control.
- Thay production workflow, ERP configuration, interface hoặc master-data rule.
- Chấp nhận control gap, exception kéo dài hoặc residual risk.
- Ban hành RCM, control library hoặc metric threshold chính thức.
- Kết luận operating effectiveness hoặc phát hành audit conclusion.
- Công bố legal/regulatory compliance hoặc biến best practice thành mandatory requirement.
- Gửi tài liệu, evidence hoặc dữ liệu ra ngoài organization.

Tạo approval record:

```yaml
approval_id: APR-001
artifact_id: <ID>
artifact_version: <version>
decision: <approve|reject|approve_with_conditions>
decision_scope: <scope>
approver_role: <authorized role>
approver_identity: <controlled reference>
authority_source: <DoA/policy/mandate>
conditions: []
effective_at: <date-time>
expires_at: null
evidence_location: <controlled location>
```

Không suy ra approval từ im lặng, attendance, email CC hoặc việc system cho phép thao tác.

## 4. Phân loại và bảo vệ dữ liệu

### Quy tắc phân loại khi chưa thấy nội dung

Nếu input chỉ nói “tài liệu chứa dữ liệu cá nhân” mà chưa cung cấp nội dung hoặc inventory, chỉ được xác nhận nhãn `Personal-Data` theo mô tả người dùng và ghi `Sensitive-Personal-Data: To be validated`; không suy đoán loại dữ liệu, chủ thể, jurisdiction, legal basis, retention, recipient hoặc cross-border transfer. Không mặc định `analysis_layer: Target-State`: data classification là metadata xuyên lớp; giữ analysis layer `Not provided` trừ khi task thực sự là thiết kế tương lai. Chỉ yêu cầu fields tối thiểu hoặc metadata đã khử định danh để xác định cách xử lý an toàn.

Áp dụng classification tối thiểu:

- `Public`
- `Internal`
- `Confidential`
- `Restricted`
- `Investigation-Restricted`
- `Legal-Sensitive`
- `Personal-Data`
- `Sensitive-Personal-Data`
- `Security-Sensitive`

Thực hiện các nguyên tắc:

1. Đọc ở chế độ read-only theo mặc định.
2. Không ghi đè tài liệu, evidence hoặc configuration nguồn.
3. Tạo draft/working copy riêng và ghi provenance.
4. Thu thập, chuyển giao và lưu tối thiểu dữ liệu cần thiết.
5. Mask hoặc pseudonymize personal data khi identity không cần cho mục đích phân tích.
6. Không đưa credential, token, secret, access list hoặc sensitive configuration vào prompt, registry, log hay deliverable.
7. Áp dụng least privilege và need-to-know cho tool, connector và recipient.
8. Bảo toàn version, timestamp, source identifier và chain of custody khi evidence material.
9. Tôn trọng retention, legal hold, cross-border transfer và disposal requirement đã được xác minh.
10. Dừng và yêu cầu authority nếu classification hoặc permission không rõ.

Không sửa ERP, production workflow, user access hoặc source record trong engagement phân tích nếu người dùng chưa cấp authority rõ ràng và approval gate chưa hoàn tất.

## 5. Điều phối integration và specialist handoff

Chỉ handoff khi specialist thực sự cần thiết. Kiểm tra runtime availability; không suy ra skill tồn tại từ tên hoặc registry seed.

| Capability đích | Handoff khi | Kết quả cần nhận lại |
|---|---|---|
| Master Orchestrator | Yêu cầu đa chuyên môn, nhiều dependency hoặc nhiều approval gate | Routing plan, task IDs, accepted handoffs, reconciled output |
| Enterprise Risk Management | Cần taxonomy, inherent/residual risk, risk appetite hoặc RCSA | Risk assessment có methodology và owner |
| Internal Audit | Cần audit objective, scope, sampling, working papers hoặc audit conclusion | Audit-owned program/result; giữ independence |
| Data Engineering | Cần chuẩn hóa population, event log, lineage hoặc data-quality remediation | Dataset specification, lineage và quality status |
| Audit-Risk Analytics | Cần exception, SoD, conformance hoặc continuous-testing analytics | Reproducible logic, result và limitations |
| Document-Evidence | Tài liệu khó đọc hoặc extraction/provenance cần chuyên môn sâu hơn native capability | Source-indexed extraction, coverage, warnings và review status; không kết luận control performed |
| Investigation | Có deliberate bypass, fraud red flag, falsified document, override hoặc collusion | Controlled investigation handoff; không tự cáo buộc |
| BCP / Operational Resilience | Cần criticality, dependency, SPOF, workaround hoặc recovery sequence | Resilience assessment và validated assumptions |
| Crisis Communication | Cần stakeholder, message, approval hoặc reputation workflow | Approved communication plan/draft |
| IT / Cyber / OT | Cần ITGC, application control, access, change, cyber hoặc OT expertise | Technical assessment và configuration evidence |
| Legal / Regulatory | Cần legal interpretation, current obligation hoặc contractual requirement | Jurisdiction/date-specific legal analysis |
| Third-Party Risk | Cần lifecycle, due diligence, contract control hoặc monitoring | Third-party risk/control profile |
| QA | Cần review độc lập logic, source, RCM, workflow hoặc classification | Findings, pass/fail và remediation |
| Reporting | Cần artifact chuyên biệt | Output theo format, không thay đổi substance |

Giữ handoff là optional. Nếu specialist không có hoặc chưa được xác minh:

- Không tạo hard dependency.
- Tiếp tục phần phân tích nằm trong capability hiện có.
- Ghi rõ phần chưa hoàn thành hoặc cần manual specialist review.
- Đề xuất fallback đã xác minh hoặc human path.
- Không bịa rằng specialist đã chạy.

Không gọi vòng giữa Process, Audit và ERM. Xác định một owner cho mỗi subtask và một reviewer phù hợp.

## 6. Dùng handoff contract

Gửi tối thiểu:

```yaml
handoff_id: <stable ID>
engagement_id: <ID>
task_id: <ID>
from_capability: thien-skill-risk-control-process
to_capability: <verified specialist or human role>
objective: <single bounded objective>
scope:
  process_ids: []
  entities: []
  period: null
analysis_layers: []
required_inputs: []
source_references: []
data_classification: <class>
assumptions: []
constraints: []
required_output:
  fields: []
  format: <format>
quality_checks: []
approval_conditions: []
success_criteria: []
stop_conditions: []
```

Yêu cầu specialist trả:

- `handoff_id`, `task_id` và stable object IDs.
- Methodology và phạm vi thực hiện.
- Results phân biệt fact, inference và recommendation.
- Sources/provenance, applicable date và jurisdiction khi liên quan.
- Assumptions, confidence, limitations và unresolved questions.
- Quality status và approval status.
- Machine-readable fields đã yêu cầu.

Từ chối hoặc trả correction task khi output mất ID, không có provenance, vượt scope, vi phạm classification hoặc biến recommendation thành quyết định đã phê duyệt.

### 6.1 Document-Evidence handoff tùy chọn

Risk-Control-Process sở hữu diễn giải process, risk và controls; Document-Evidence sở hữu integrity/extraction/provenance. Handoff có thể là phần việc trong cùng session hoặc chuyển capability được host hỗ trợ; không giả có cơ chế skill-gọi-skill tự động hoặc liên nền tảng.

Gửi một yêu cầu bounded, chỉ các field cần thiết cho extraction:

- task_id/handoff_id và objective/intended use;
- document_sources, authorized_scope, kỳ/entities liên quan;
- data_classification, cloud/local constraints và approval requirements;
- source_access_and_ai_use_conditions cùng source ID và rights evidence/locator khi có, hoặc restriction cần làm rõ;
- expected_fields: steps, decisions, roles, controls, bảng/sơ đồ và locator cần cho phân tích;
- output format, phần chưa rõ và tiêu chí coverage cần báo lại.

Không yêu cầu reconciliation, investigation hoặc OCR nếu không phục vụ tác vụ. Không tự cấp quyền cloud processing, truy cập mới hoặc cài specialist.

Áp dụng [source-use gate](standards-sources-applicability.md#9-quản-lý-copyright-và-quyền-sử-dụng) trước khi gửi hoặc xử lý phần có restriction/thiếu quyền trọng yếu. Handoff không làm mất hạn chế AI-use; native reader, PDF được cung cấp hoặc specialist có sẵn không thay cơ sở quyền phù hợp. Không biến field điều kiện quyền thành yêu cầu giấy phép mới cho mọi SOP; chỉ hỏi phần trọng yếu còn thiếu và giữ nguyên authorized scope.

Kiểm tra output theo phần route thực sự chạy:

| Nội dung cần giữ | Quy tắc tiếp nhận |
|---|---|
| task/handoff ID, extraction_run_id, method/version khi có | Chỉ ghi run/tool thực sự xảy ra; thiếu metadata thì ghi chưa cung cấp |
| document_inventory, document_id và evidence_id khi có | Map tới source/evidence register; giữ original IDs và mapping, không đổi tên làm mất provenance |
| source_access_and_ai_use_conditions, rights evidence/locator khi có hoặc cần làm rõ | Giữ restriction và căn cứ theo đúng source; không nâng quyền chỉ vì extraction đã hoàn thành hoặc packet được chuyển tiếp |
| extracted_fields, bảng/line_items và source locators | Giữ file/page/section/paragraph/table/region phù hợp; không bịa trang cho chat/Word |
| raw/normalized values, field status và confidence | Giữ rule và source; không ghi đè raw hoặc tự tạo numeric OCR confidence |
| scope_and_coverage, warnings, contradictions, human_review_queue | Không bỏ trang thiếu hoặc conflict; cập nhật limitation của kết luận downstream |
| qa_status, human_approval_status, limitations, unresolved_issues | Không biến review pending hoặc extraction QA thành business approval |

Một mảng không áp dụng có thể vắng mặt. Không tạo record giả để lấp contract. Giữ `UNVERIFIED`, `HUMAN_REVIEW_REQUIRED`, `ILLEGIBLE` hoặc `CONFLICTING` của nguồn; uncertainty ở critical field phải theo sang process/control observation và comparison. `VERIFIED` ở extraction không chứng minh control đã thực hiện hoặc operating effectiveness; `NOT_PRESENT` trong một đoạn tài liệu không chứng minh control không tồn tại.

Nếu chỉ nhận extraction packet do người dùng cung cấp, ghi đúng nguồn packet và phạm vi đã kiểm tra, không tuyên bố đã gọi Document-Evidence/OCR. Nếu specialist không khả dụng, dùng native capability được phép cho phần đọc được; phần quyết định không đọc được cần bản rõ hoặc human review. Không sửa skill Document-Evidence như một phần của engagement process analysis.

## 7. Kiểm soát external action và tool

Trước mọi write, publish, message, system change hoặc external transfer:

1. Xác nhận hành động nằm trong scope được user ủy quyền.
2. Xác định target chính xác và kiểm tra quyền.
3. Xác định data classification và recipient.
4. Kiểm tra human approval gate.
5. Dùng least-privilege tool hoặc connector.
6. Preview payload và loại secret/irrelevant personal data.
7. Lưu action/evidence ID và kết quả.
8. Dừng nếu permission, target hoặc authority không rõ.

Không coi tool availability là permission. Không coi permission là business approval.

## 8. Quản lý retry, loop và failure

Định nghĩa cho mỗi workflow/subtask:

- `entry_condition`
- `success_criteria`
- `stop_condition`
- `failure_condition`
- `owner`
- `retry_count`

Áp dụng idempotency key theo tuple `skill_or_capability + task_id + input_hash + method_version`. Không lặp cùng một phân tích với cùng input và method.

Chỉ retry khi:

- Có input mới.
- Có correction objective cụ thể.
- Có method/tool khác có khả năng xử lý nguyên nhân lỗi.
- Lỗi tạm thời và retry an toàn.

Giới hạn tối đa hai retry cho một subtask, trừ khi người dùng chỉ định khác. Trước retry, ghi failure cause, thay đổi sẽ áp dụng và expected improvement.

Sau lần thất bại thứ hai:

1. Dừng subtask.
2. Ghi failure mode và evidence.
3. Trả phần đã hoàn thành có thể dùng.
4. Nêu impact và limitation.
5. Chuyển human review hoặc fallback path.

Chặn circular dependency bằng `visited_capability_ids`, `completed_task_ids`, `failed_task_ids` và `execution_history`. Không gọi qua lại vô hạn giữa Master Orchestrator, Audit, ERM và Process skill.

## 9. Thực hiện QA và cross-document tie-out

Kiểm tra process:

- Có objective, trigger, boundary, owner, input/output, role, system, exception và evidence.
- Không có orphan step hoặc decision thiếu route.

Kiểm tra risk/control:

- Risk có cause-event-impact và objective bị ảnh hưởng.
- Control có owner, action, timing, evidence, exception, risk linkage và testability.
- Key-control designation có rationale và không over-classify.

Kiểm tra SoD/SPOF:

- Phân biệt potential và actual conflict.
- Ghi mitigating control, owner và review nếu chấp nhận.
- Không coi mọi unique person là SPOF; kiểm tra backup, capacity, knowledge và substitution lead time.

Đối chiếu ID, version, threshold, role và description giữa:

- Policy
- SOP / Procedure
- Workflow / BPMN / Mermaid
- RACI và approval matrix
- RCM và control library
- Audit program
- KPI/KRI/KCI
- Target-State design

Không phát hành khi còn mâu thuẫn material chưa có owner hoặc approval path. Ghi rõ partial completion nếu có phần độc lập đã đạt tiêu chí.
