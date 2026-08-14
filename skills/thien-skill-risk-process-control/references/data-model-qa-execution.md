# Common data model, QA và execution control

## Mục lục

1. Mục đích và nguyên tắc
2. Object model
3. Trường nền tảng
4. Quan hệ và ID
5. Null, confidence và evidence
6. Template views
7. QA theo object
8. Cross-document tie-out
9. Workflow chuẩn 14 bước
10. Execution, retry và stop rules
11. Acceptance evidence

## 1. Mục đích và nguyên tắc

Dùng một common data model làm nguồn chuẩn cho mọi process map, register, RCM, diagram, report và handoff. Không duy trì nhiều định nghĩa khác nhau cho cùng một field.

Áp dụng các nguyên tắc sau:

- Tạo object một lần, tái sử dụng bằng ID trong các view.
- Không sao chép control thành nhiều control mới chỉ vì nó xử lý nhiều risks.
- Không sao chép risk thành nhiều risk mới chỉ vì nó xuất hiện trong nhiều views.
- Giữ `analysis_layer`, `source_reference`, `confidence` và `review_status` trên mọi record trọng yếu.
- Dùng templates như output views, không dùng chúng làm bằng chứng.
- Giữ raw source tách khỏi normalized record.

Schema machine-readable nằm tại [common-data-model.yaml](../templates/common-data-model.yaml).

## 2. Object model

Hỗ trợ tối thiểu các object:

- `EnterpriseValueChain`
- `EndToEndProcess`
- `Process`
- `Subprocess`
- `Activity`
- `Task`
- `BusinessObjective`
- `ProcessObjective`
- `Trigger`
- `Input`
- `Output`
- `Stakeholder`
- `Customer`
- `Supplier`
- `Role`
- `Responsibility`
- `System`
- `Application`
- `DataObject`
- `Document`
- `Policy`
- `Standard`
- `SOP`
- `Procedure`
- `WorkInstruction`
- `Form`
- `Evidence`
- `Risk`
- `ControlObjective`
- `Control`
- `ControlSource`
- `Requirement`
- `KPI`
- `KRI`
- `KCI`
- `Decision`
- `Approval`
- `Exception`
- `Escalation`
- `Dependency`
- `SPOF`
- `SoDConflict`
- `RCMRelationship`
- `ProcessDeviation`
- `Gap`
- `Recommendation`
- `Action`
- `Workflow`
- `Diagram`
- `TestAttribute`

## 3. Trường nền tảng

Mỗi object dùng các trường nền tảng sau khi phù hợp:

| Field | Quy tắc |
|---|---|
| `object_id` | Duy nhất, ổn định, không tái sử dụng cho object khác. |
| `object_type` | Một giá trị trong object register. |
| `title` | Tên ngắn, cụ thể, không suy diễn. |
| `description` | Mô tả có thể kiểm chứng. |
| `analysis_layer` | `As-Documented`, `As-Designed`, `As-Performed` hoặc `Target-State`. |
| `source` | Loại nguồn: document, interview, walkthrough, data, evidence, external source hoặc proposal. |
| `source_reference` | Trang, điều khoản, record, transaction, timestamp hoặc locator khác. |
| `version` | Version object/source nếu có. |
| `status` | Draft, proposed, current, superseded, approved, rejected hoặc unresolved. |
| `created_at` | ISO 8601 nếu biết; nếu không, `Not provided`. |
| `updated_at` | ISO 8601 nếu biết; nếu không, `Not provided`. |
| `created_by` | Người/hệ thống tạo record nếu biết. |
| `reviewed_by` | Reviewer; không điền tên suy đoán. |
| `approved_by` | Approver; chỉ điền khi có evidence phê duyệt. |
| `data_classification` | Public, Internal, Confidential, Restricted hoặc lớp chuyên biệt. |
| `confidence` | High, Medium, Low hoặc Unresolved kèm basis. |
| `assumptions` | Chỉ giả định đã được công khai; không dùng cho missing facts trọng yếu. |
| `related_objects` | Danh sách ID có relationship type. |
| `supporting_evidence` | Danh sách evidence IDs hoặc source locators. |
| `review_status` | Not reviewed, under review, validated, approved hoặc rejected. |

## 4. Quan hệ và ID

Giữ tối thiểu hai chuỗi truy nguyên:

```text
BusinessObjective
→ EndToEndProcess
→ Process
→ Subprocess
→ Activity
→ Task
→ Risk
→ ControlObjective
→ Control
→ Evidence
→ TestAttribute
→ Gap
→ Recommendation
→ Action
```

```text
Requirement
→ Process/Task
→ Risk
→ ControlObjective
→ Control
→ Evidence
```

Dùng prefix rõ nghĩa, ví dụ `OBJ-`, `E2E-`, `PROC-`, `STEP-`, `RSK-`, `COBJ-`, `CTL-`, `EVD-`, `GAP-`, `REC-`, `ACT-`, `SOD-`, `DEP-` và `MET-`. Không đổi ID khi chỉ thay title. Không dùng position trong spreadsheet làm ID bền vững.

Biểu diễn quan hệ many-to-many bằng relationship record, không bằng cách gộp nhiều ID thành free text. Mỗi relationship record phải nêu `from_id`, `relationship_type`, `to_id`, source và review status.

## 5. Null, confidence và evidence

Chỉ dùng một trong các giá trị sau khi dữ liệu chưa có:

- `null`: chưa có giá trị trong dữ liệu có cấu trúc;
- `Not provided`: nguồn không cung cấp;
- `Not applicable`: field không áp dụng, kèm reason khi không hiển nhiên;
- `To be validated`: có assertion nhưng chưa đủ evidence;
- `Unresolved`: có xung đột hoặc chưa thể quyết định.

Không thay null bằng nội dung “hợp lý”. Không nâng `Inferred` thành `Confirmed` chỉ vì nhiều nguồn thứ cấp lặp lại cùng assertion.

Ghi confidence basis bằng một hoặc nhiều trạng thái:

- `Documented`
- `Interview-confirmed`
- `Evidence-confirmed`
- `Data-confirmed`
- `Inferred`
- `Unresolved`

`As-Performed` cần ít nhất một nguồn phù hợp ngoài policy/SOP hoặc representation đơn thuần.

## 6. Template views

Mọi template view kế thừa `base_fields` của common data model. Block `output_metadata` ở đầu mỗi template bảo toàn tối thiểu analysis layers, source references, data classification, assumptions, confidence, unresolved items và review status ở cấp output; record-level fields bổ sung metadata khi cần truy nguyên riêng. Không được xóa metadata này khi chuyển giữa RCM, workflow, report hoặc handoff view.

Dùng các templates sau:

- [process-intake.yaml](../templates/process-intake.yaml)
- [source-document-assessment.yaml](../templates/source-document-assessment.yaml)
- [process-architecture-step-register.yaml](../templates/process-architecture-step-register.yaml)
- [process-deviation-register.yaml](../templates/process-deviation-register.yaml)
- [risk-register.yaml](../templates/risk-register.yaml)
- [control-register.yaml](../templates/control-register.yaml)
- [rcm.yaml](../templates/rcm.yaml)
- [sod-conflict-register.yaml](../templates/sod-conflict-register.yaml)
- [spof-dependency-register.yaml](../templates/spof-dependency-register.yaml)
- [metric-register.yaml](../templates/metric-register.yaml)
- [workflow-definition.yaml](../templates/workflow-definition.yaml)
- [target-state-options.yaml](../templates/target-state-options.yaml)
- [assessment-scorecard.yaml](../templates/assessment-scorecard.yaml)
- [training-exercise.yaml](../templates/training-exercise.yaml)
- [audit-handoff.yaml](../templates/audit-handoff.yaml)
- [action-plan.yaml](../templates/action-plan.yaml)
- [qa-checklist.yaml](../templates/qa-checklist.yaml)

Tạo risk-centric, control-centric, requirement-centric và audit-test RCM bằng view/filter từ cùng relationship set. Không duy trì các workbook nguồn độc lập nếu không có reconciliation rule.

## 7. QA theo object

### Process

Kiểm tra objective, trigger, start/end boundary, owner, inputs, outputs, customer, roles, systems, exceptions và evidence. Phát hiện orphan step, circular flow, decision không có outcome và handoff không có owner.

### Risk

Kiểm tra cause, event, impact, affected objective, process/step linkage, source và confidence. Không chấp nhận mô tả chỉ có “risk of failure” hoặc chỉ lặp tên control.

### Control

Kiểm tra owner/performer, action, frequency/trigger, population, criteria/precision, evidence, exception handling, escalation, risk linkage, control objective, source và testability. Không chấp nhận “manager reviews” nếu thiếu subject, criteria và evidence.

### Key control

Kiểm tra rationale, significant-risk linkage, alternatives, dependency và consequence of failure. Phát hiện over-classification khi gần như mọi control đều được đánh dấu key.

### External source

Kiểm tra official title, issuing body, version, effective date, jurisdiction, mandatory/advisory status, adoption và date verified. Không coi framework alignment là certification hoặc legal compliance.

### RCM

Kiểm tra ID existence, many-to-many integrity, view completeness, evidence linkage, null semantics, rating methodology và source references. Không tự sinh residual risk hoặc sample size.

### SoD

Kiểm tra activity pair, risk, role/user/system, potential/actual status, business justification, mitigation, monitoring và owner. Không kết luận actual conflict nếu chỉ có role design mà chưa có user assignment.

### SPOF

Kiểm tra criticality, backup, substitute capacity, lead time, recovery time, documentation, cross-training, common-mode failure và evidence. Không kết luận SPOF chỉ từ unique owner.

### Diagram

Kiểm tra start/end, no orphan node, decision routes, owner/lane, exception path, loop termination, IDs và layer legend. Chỉ ghi `syntax_validated: true` khi parser thực sự chạy; chỉ ghi `visually_verified: true` khi đã render và kiểm tra.

## 8. Cross-document tie-out

Đối chiếu ít nhất các cặp sau:

- Policy ↔ SOP/Procedure
- SOP ↔ Workflow/Step Register
- Workflow ↔ RACI/Approval Matrix
- Workflow ↔ RCM/Control Library
- RCM ↔ Audit Handoff/Test Attributes
- Control ↔ Evidence/Retention
- Requirement ↔ Control Source/Applicability
- Target State ↔ Action Plan/Roadmap
- KPI/KRI/KCI ↔ Objective/Risk/Control

Kiểm tra consistency của role names, thresholds, process boundaries, control IDs, frequencies, systems, version và analysis layer. Ghi conflict thay vì tự chọn nguồn thắng khi authority chưa được xác định.

## 9. Workflow chuẩn 14 bước

Áp dụng bảng này cho engagement đầy đủ. Có thể thu gọn deliverable nhưng không được âm thầm bỏ bước; bước không áp dụng phải ghi `Not applicable` và reason. Mỗi bước chỉ chuyển tiếp khi success condition đạt hoặc có approval chấp nhận phần còn thiếu.

| Bước | Entry/action bắt buộc | Output hoặc success condition | Stop/approval gate chính |
|---:|---|---|---|
| 1 | Intake objective, entity/site, industry, process, documents, systems, data, stakeholders, jurisdiction, audience, deliverable và mode. | Intake record và missing-information register. | Dừng nếu objective hoặc authority xử lý dữ liệu chưa đủ để xác định scope an toàn. |
| 2 | Chốt start/end, in/out, process level và các layer `As-Documented`, `As-Designed`, `As-Performed`, `Target-State` cần dùng. | Scope record có boundary và layer riêng biệt. | Người dùng/process owner duyệt thay đổi scope trọng yếu. |
| 3 | Lập source register với version, effective status, owner, provenance, conflict và missing source. | Source register và conflict log. | Không chọn nguồn thắng khi authority chưa được xác định. |
| 4 | Dựng value chain/E2E/process hierarchy L0–L5 theo evidence. | Architecture/catalog với stable IDs và ownership status. | Không tự gán level hoặc owner từ tên phòng ban. |
| 5 | Map trigger, input, step, decision, role, system, output, exception, rework, handoff và evidence. | Step register, workflow source và deviation candidates. | `As-Performed` chỉ khi có evidence phù hợp ngoài policy hoặc assertion đơn thuần. |
| 6 | Viết risk theo Cause → Event → Impact → Objective và link tới step/objective. | Risk register có source, layer và confidence. | Không tự chấm rating/threshold nếu methodology chưa được duyệt. |
| 7 | Xác định control objective, current/key/supporting control, design quality, evidence và testability. | Control register, key-control rationale và test-attribute draft. | Không kết luận operating effectiveness; formal conclusion thuộc assurance owner độc lập. |
| 8 | Xác minh external source, version/effective status, jurisdiction, adoption và mandatory/advisory status. | Requirement/control-source mapping. | Legal/compliance conclusion trọng yếu phải handoff cho người có thẩm quyền. |
| 9 | Phân tích gap, SoD, SPOF/dependency, duplicate, redundant, over-control và bottleneck. | Gap, SoD, dependency/SPOF và rationalization records. | Không biến candidate gap thành audit finding hoặc potential conflict thành actual conflict. |
| 10 | Thiết kế target-state options từ objective, obligation, appetite, capacity, technology và practicality. | Options có benefit, risk, cost, complexity, dependency, metric và residual exposure. | Process/risk owner duyệt option; không mặc định option phức tạp nhất. |
| 11 | Tạo RCM, workflow, RACI và control overlay từ cùng object/relationship set. | Views tie-out theo stable IDs, source và layer. | Không duy trì view độc lập không có reconciliation rule. |
| 12 | QA object, diagram, null semantics, relationship integrity và cross-document tie-out. | QA checklist, conflict/unresolved register và correction log. | Không phát hành khi còn unresolved Critical/High không có waiver có owner. |
| 13 | Chuẩn bị structured content trước rồi handoff sang Word, Excel, PowerPoint hoặc dashboard capability khi có. | Deliverable draft giữ source, assumption, confidence và review status. | Format đẹp không phải evidence; không gửi ngoài tổ chức nếu chưa được duyệt. |
| 14 | Chuyển recommendation thành remediation/action handoff khi phù hợp. | Action plan có owner, dependency, approval, due-date basis, status và follow-up. | Không tự sửa source/ERP/production hoặc đóng action khi thiếu closure evidence. |

## 10. Execution, retry và stop rules

Trước mỗi subtask, xác định:

- `entry_condition`
- `success_criteria`
- `stop_condition`
- `failure_condition`
- `authorized_actions`
- `approval_gate`

Không chạy lại cùng analysis với cùng input và cùng method. Retry tối đa hai lần, mỗi lần phải ghi nguyên nhân lỗi và thay đổi phương pháp. Sau hai lần thất bại, dừng và trả partial result, failure record và human-review request.

Dừng ngay khi:

- thiếu authority cho external/destructive/production action;
- nguồn trọng yếu không thể truy cập và không có phương án kiểm chứng;
- inputs mâu thuẫn làm thay đổi material conclusion;
- workstream yêu cầu legal/audit/technical conclusion ngoài phạm vi;
- data classification không cho phép tiếp tục xử lý.

## 11. Acceptance evidence

Tách bốn loại kết quả kiểm thử:

- `structural`: package, metadata, files, links và schema;
- `deterministic`: IDs, relationships, required fields và invariant rules;
- `behavioral`: forward-test bằng model trên raw task/artifact;
- `manual`: visual, professional hoặc legal review.

Không gộp chúng thành một tỷ lệ pass duy nhất. Ghi platform, model, date, skill version/hash, test input hash, result, evidence, reviewer, limitation và remediation status.
