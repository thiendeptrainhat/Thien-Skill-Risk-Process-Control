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
9. Khung workflow 14 bước theo phạm vi và dependency
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
- Một logical control có thể có nhiều observations khác layer/scope/kỳ; không gộp các observations mâu thuẫn thành một fact.
- Chỉ dùng object/view cần cho câu hỏi. Template đầy đủ không buộc tạo đủ mọi record, evidence, gap hoặc action.

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
- `ProcessReferenceMapping`
- `ControlBaselineLink`
- `ControlObservation`
- `ControlComparison`
- `NoChangeScenario`
- `DesignOpportunity`

## 3. Trường nền tảng

Mỗi object dùng các trường nền tảng sau khi phù hợp:

| Field | Quy tắc |
|---|---|
| `object_id` | Duy nhất, ổn định, không tái sử dụng cho object khác. |
| `object_type` | Một giá trị trong object register. |
| `title` | Tên ngắn, cụ thể, không suy diễn. |
| `description` | Mô tả có thể kiểm chứng. |
| `analysis_layer` | `As-Documented`, `As-Designed`, `As-Performed` hoặc `Target-State` khi có cơ sở; chưa biết thì giữ null/unresolved. Source-use metadata không tự là một layer của tổ chức. |
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

Giữ hai chuỗi truy nguyên sau cho các nhánh thuộc phạm vi và có dữ liệu. Đây là quan hệ nghiệp vụ, không phải lệnh sinh đủ mọi object. Nhánh chưa có evidence hoặc không được yêu cầu phải giữ limitation/reason; không tạo Evidence, TestAttribute hoặc Gap giả để hoàn thiện chuỗi:

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

### Extensions 1.1.0: identity, source và comparison

| Object/field | Prefix cho record mới | Quy tắc |
|---|---|---|
| `source_id` trong source register | `SRC-` | Giữ source/evidence/document IDs đã có và mapping từ upstream; không đổi ID cũ chỉ để khớp prefix. |
| `process_reference_mapping_id` | `MAP-` | Internal process ID khác `reference_library_id`/`reference_item_id`. External ID chỉ ghi khi thực đọc; proposed E2E name không giả làm tên/ID chuẩn. |
| `baseline_link_id` | `CBL-` | Liên kết source/requirement → control objective → candidate control; có applicability, mandatory/advisory và interpretation rationale. Analyst proposal không có citation bịa. |
| `control_observation_id` | `OBS-` | Liên kết về logical `control_id`; có layer, assessed scope/period, description, source/evidence và assessment riêng. |
| `comparison_id` | `CMP-` | Liên kết baseline và đúng observation IDs theo lớp/phạm vi/kỳ; không chỉ link logical CTL rồi suy current performance. |
| `no_change_scenario_id` | `NCS-` | Kịch bản nếu giữ nguyên, có basis/uncertainty; không phải incident record. |
| `design_opportunity_id` | `OPP-` | Cho đề xuất/greenfield chưa có actual gap; recommendation/action không cần một GAP giả. |

`controls.control_id` giữ logical identity và các trường 1.0.0 tiếp đọc được. `control_observations` trong control register chứa những ghi nhận/assessment có scope riêng. Cùng một control dùng cho nhiều E2E giữ ID chung khi có căn cứ; trùng tên không đủ để gộp controls. Keyness và design assessment phụ thuộc observation/context, không phải một quyết định đã phê duyệt áp dụng mặc định cho mọi kỳ.

Nếu SOP mô tả hai cấp duyệt nhưng log có một giao dịch chỉ một cấp: giữ nguồn SOP và log, dùng hai observations riêng nối cùng logical control nếu identity đã xác định. Không ghi đè description SOP bằng log và không dùng SOP để điền bằng chứng vận hành còn thiếu. `documented_observation_ids`, `designed_observation_ids`, `performed_observation_ids`, `target_observation_ids` chỉ nhận đúng layer và scope/period được hỗ trợ. RCM row dùng `control_observation_id` phải resolve về cùng `control_id`/layer; so sánh xuyên lớp nằm ở comparison record.

### Giữ cách đọc output 1.0.0

- Giữ nguyên raw input, record gốc, IDs, source locators, giá trị và null; không tự tăng schema version của tài liệu người dùng.
- Các field mới là additive/optional cho legacy input. Missing extension không có nghĩa đã đọc nguồn, được quyền dùng AI, đã thực hiện control, zero hoặc false.
- Giữ nguyên `design_assessment`; `assessment_status`/`evidence_status` bổ sung trạng thái đánh giá/bằng chứng, không đổi tên hay làm mất giá trị cũ. Singular `control_objective_id`, `process_id`, `step_id`, `gap_id` vẫn được đọc; arrays mới không được âm thầm mâu thuẫn hoặc thay thế chúng.
- Chỉ tạo observation khi source record/identity và layer/scope có cơ sở. Giữ `legacy_record_reference`; không copy một legacy description sang layer mới chỉ để lấp schema. Khi chưa xác định, giữ bản gốc và unresolved fields thay vì suy ra As-Performed.
- `legacy_projection_observation_id` chỉ điền khi một projection mới thật sự lấy từ observation đó. Legacy input chưa có mapping thì để null và bảo toàn record gốc; không chọn tùy tiện observation mới nhất để ghi đè.
- Đây là contract bảo toàn dữ liệu/ý nghĩa cho reader 1.1.0, không cam kết mọi consumer 1.0.0 strict-schema sẽ tự nhận field mới. Nếu cần export cho consumer đó, giữ projection có scope/locator rõ và báo extension chưa thể biểu diễn; không làm mất chúng khỏi canonical dataset.
- Nếu không thể giữ compatibility bằng additive mapping, dừng phần migration/schema change và yêu cầu quyết định; không biến phát hiện incompatibility thành kết quả đã tương thích.

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

Giữ `assessment_status: Not assessed` hoặc `evidence_status: Insufficient evidence` khi đúng tình trạng; chúng không thay cho missing source values. `coverage_assessment: evidence_insufficient` không có nghĩa control failed. `documented_gap` trong comparison nghĩa là gap đã có căn cứ trong scope, không phải analysis layer As-Documented; vẫn phải chỉ rõ gap type/rationale.

Trước kiểm tra, new `evidence_status` mặc định `Not checked`, không tự ghi `Insufficient evidence`. `design_assessment` và `assessment_status` giữ `Not assessed` khi chưa đánh giá; baseline/extraction status chưa kiểm tra là `not_checked`. Không dùng các trạng thái này điền vào field fact bị thiếu.

Source-use record giữ riêng `source_type`, `version`, `date_verified`, `source_reference` và các extension `reference_kind`, `content_verification_status`, `content_checked_scope`, `access_status`, `ai_use_status`, `redistribution_status`, `date_checked` cùng basis/limitations. `date_checked` có thể chỉ là lần kiểm tra; không thay bằng ngày verification thành công. `content_verified` chỉ áp dụng cho nội dung/locator đã đọc, không tự chứng minh applicability, currency, quyền dùng AI, tái phân phối hay compliance.

Không dùng một cờ verified cho cả nguồn. Nội dung/điều khoản chưa đọc, snippet hoặc trang giới thiệu chỉ hỗ trợ discovery/metadata. Khi không có nguồn/capability phù hợp, vẫn có thể lập proposal có nhãn và limitations; không gọi nó là standard-derived hoặc fully benchmarked. Xem [external-process-control-libraries.md](external-process-control-libraries.md).

## 6. Template views

Mọi template view kế thừa `base_fields` của common data model. Block `output_metadata` ở đầu mỗi template bảo toàn tối thiểu analysis layers, source references, data classification, assumptions, confidence, unresolved items và review status ở cấp output; record-level fields bổ sung metadata khi cần truy nguyên riêng. Không được xóa metadata này khi chuyển giữa RCM, workflow, report hoặc handoff view.

Dùng các templates sau:

- [process-intake.yaml](../templates/process-intake.yaml)
- [source-document-assessment.yaml](../templates/source-document-assessment.yaml)
- [process-architecture-step-register.yaml](../templates/process-architecture-step-register.yaml)
- [process-deviation-register.yaml](../templates/process-deviation-register.yaml)
- [risk-register.yaml](../templates/risk-register.yaml)
- [control-register.yaml](../templates/control-register.yaml)
- [control-baseline-comparison.yaml](../templates/control-baseline-comparison.yaml)
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

Source register sở hữu source-use metadata; control register sở hữu baseline links và scoped observations; comparison/no-change template chỉ tham chiếu chúng. Action plan giữ recommendation/design-opportunity/action IDs và link về comparison/scenario. Không sao chép nhiều bộ facts riêng để tạo mỗi view.

## 7. QA theo object

### Process

Kiểm tra objective, trigger, start/end boundary, owner, inputs, outputs, customer, roles, systems, exceptions và evidence. Phát hiện orphan step, circular flow, decision không có outcome và handoff không có owner.

Với E2E mapping, kiểm tra boundary của tài liệu so với E2E lớn hơn, nhiều E2E liên quan, reference ID/source và rationale. 94 seed profiles không phải danh mục đóng. No reliable match là kết quả hợp lệ; không dùng số similarity không có methodology hoặc chọn acronym theo suy đoán.

### Risk

Kiểm tra cause, event, impact, affected objective, process/step linkage, source và confidence. Không chấp nhận mô tả chỉ có “risk of failure” hoặc chỉ lặp tên control.

### Control

Kiểm tra owner/performer, action, frequency/trigger, population, criteria/precision, evidence, exception handling, escalation, risk linkage, control objective, source và testability. Không chấp nhận “manager reviews” nếu thiếu subject, criteria và evidence.

Giữ logical identity riêng với observation; kiểm tra mỗi scoped description dùng đúng source/layer/kỳ và không mất conflict. Thiếu thuộc tính trong SOP là limitation/design question, không tự là proof control không tồn tại hoặc đã failed.

### Key control

Kiểm tra rationale, significant-risk linkage, alternatives, dependency và consequence of failure. Phát hiện over-classification khi gần như mọi control đều được đánh dấu key.

Kiểm tra source → control objective → risk → candidate control → keyness rationale. Supporting/alternative/compensating control không tự bị loại vì khác hình thức; library label hoặc analyst assessment không thay evidence phê duyệt keyness của tổ chức.

### External source

Kiểm tra official title, issuing body, version, effective date, jurisdiction, mandatory/advisory status, adoption và date verified. Không coi framework alignment là certification hoặc legal compliance.

Kiểm tra riêng content scope, access, AI-use và redistribution basis. Thiếu một nguồn không ngăn phần phân tích độc lập; giữ proposal/provisional nếu chưa có external baseline phù hợp. Không đánh dấu `content_verified` từ trang overview, quyền mua tài liệu hoặc tên framework.

### RCM

Kiểm tra ID existence, many-to-many integrity, view completeness, evidence linkage, null semantics, rating methodology và source references. Không tự sinh residual risk hoặc sample size.

Kiểm tra baseline links, observation ownership/layer/scope/period, equivalent-control rationale và link gap/recommendation/no-change. Nếu chỉ có tài liệu, performed observation list không được làm đầy từ documented list. Giữ evidence limitation riêng với design gap/observed deviation; không dùng comparison để tuyên bố formal OE.

### Input, handoff và legacy compatibility

Ghi actual capability/permission, không suy từ tên host. Document-Evidence là optional: giữ upstream IDs, source locators, coverage, method, warnings và review status; consumer-only receipt không chứng minh specialist/OCR đã chạy. Nếu native text đủ thì đọc trực tiếp; nếu phần quyết định không đọc được thì giữ partial coverage và xin bản rõ/human review.

Đối chiếu original 1.0.0 fields/IDs/null/design_assessment với projection mới; không xóa data chỉ vì thiếu extension. QA booleans legacy mặc định false chưa phải kết quả fail: phải có check execution status, evidence/rationale và scope. Chỉ đánh dấu pass cho kiểm tra thực sự đã thực hiện.

### SoD

Kiểm tra activity pair, risk, role/user/system, potential/actual status, business justification, mitigation, monitoring và owner. Không kết luận actual conflict nếu chỉ có role design mà chưa có user assignment.

### SPOF

Kiểm tra criticality, backup, substitute capacity, lead time, recovery time, documentation, cross-training, common-mode failure và evidence. Không kết luận SPOF chỉ từ unique owner.

### Diagram

Kiểm tra start/end, no orphan node, decision routes, owner/lane, exception path, loop termination, IDs và layer legend. Chỉ ghi `syntax_validated: true` khi parser thực sự chạy; chỉ ghi `visually_verified: true` khi đã render và kiểm tra.

## 8. Cross-document tie-out

Trong scope của engagement, đối chiếu các cặp liên quan sau; cặp không áp dụng không buộc tạo thêm tài liệu:

- Policy ↔ SOP/Procedure
- SOP ↔ Workflow/Step Register
- Workflow ↔ RACI/Approval Matrix
- Workflow ↔ RCM/Control Library
- RCM ↔ Audit Handoff/Test Attributes
- Control ↔ Evidence/Retention
- Requirement ↔ Control Source/Applicability
- Target State ↔ Action Plan/Roadmap
- KPI/KRI/KCI ↔ Objective/Risk/Control
- Process Reference Mapping ↔ Source/External Reference Item
- Baseline Link ↔ Control Objective/Scoped Observation/Comparison
- Comparison/No-change Scenario ↔ Recommendation/Design Opportunity/Action

Kiểm tra consistency của role names, thresholds, process boundaries, control IDs, frequencies, systems, version và analysis layer. Ghi conflict thay vì tự chọn nguồn thắng khi authority chưa được xác định.

## 9. Khung workflow 14 bước theo phạm vi và dependency

Đây là khung cho engagement đầy đủ, không phải chuỗi 14 bước bắt buộc cho mọi câu hỏi. Với yêu cầu hẹp, chỉ dùng module/bước và output liên quan, nêu scope/limitation cần thiết; không ép lập tất cả registers hoặc xin xác nhận mọi field. Với engagement đầy đủ, ghi coverage và lý do nhánh chưa áp dụng/chưa đủ dữ liệu, không giả đã hoàn tất.

Điều kiện bước là dependency của claim/phần việc tương ứng. Thiếu external baseline, tool hoặc operating evidence chỉ chặn kết luận phụ thuộc chúng; vẫn có thể phân tích documented state, lập proposal có nhãn và tiếp tục phần độc lập an toàn. Approval chấp nhận phạm vi hạn chế không biến nội dung chưa biết thành fact, source đã xác minh hoặc control đã hoạt động.

| Bước | Entry/action khi thuộc scope | Output hoặc success condition | Stop/approval gate theo dependency |
|---:|---|---|---|
| 1 | Intake objective, entity/site, industry, process, documents, systems, data, stakeholders, jurisdiction, audience, deliverable và mode. | Intake record và missing-information register. | Dừng nếu objective hoặc authority xử lý dữ liệu chưa đủ để xác định scope an toàn. |
| 2 | Chốt start/end, in/out, process level và các layer `As-Documented`, `As-Designed`, `As-Performed`, `Target-State` cần dùng. | Scope record có boundary và layer riêng biệt. | Người dùng/process owner duyệt thay đổi scope trọng yếu. |
| 3 | Lập source register với version, effective status, owner, provenance, content scope, access/rights, conflict và missing source. | Source register, capability limitations và conflict log. | Không chọn nguồn thắng khi authority chưa xác định; nguồn thiếu chỉ chặn baseline claim phụ thuộc nguồn đó. |
| 4 | Dựng value chain/E2E/process hierarchy L0–L5 theo evidence; dùng seed hoặc tra cứu nguồn phù hợp khi có. | Architecture/mappings với stable IDs, candidate rationale, ownership status và no reliable match khi cần. | Không tự gán level/owner từ phòng ban, ép vào 94 profiles hoặc bịa external ID; vẫn có thể đề xuất organization-specific design có nhãn. |
| 5 | Map trigger, input, step, decision, role, system, output, exception, rework, handoff và evidence. | Step register, workflow source và deviation candidates. | `As-Performed` chỉ khi có evidence phù hợp ngoài policy hoặc assertion đơn thuần. |
| 6 | Viết risk theo Cause → Event → Impact → Objective và link tới step/objective. | Risk register có source, layer và confidence. | Không tự chấm rating/threshold nếu methodology chưa được duyệt. |
| 7 | Xác định control objective, logical control và scoped observations; đánh giá key/supporting/alternatives, design, evidence và testability. | Control register, scoped keyness rationale và test-attribute draft khi được yêu cầu. | SOP-only không tạo performed observation; assessment không thay organizational approval hoặc formal OE. |
| 8 | Xác minh nội dung nguồn thực dùng, version/kỳ, applicability, jurisdiction, adoption, mandatory/advisory và quyền dùng. | Baseline links/source-use records; analyst proposal có nhãn khi chưa có verified source. | Thiếu nguồn/quyền chặn standard/compliance claim, không chặn proposal độc lập; kết luận legal/compliance trọng yếu cần người có thẩm quyền. |
| 9 | So baseline–documented–designed–performed theo objective/coverage, xét controls tương đương; phân tích gap, SoD, SPOF và rationalization khi trong scope. | Comparison với đúng observation IDs, gap/limitation, dependency và no-change scenario. | Không coi thiếu evidence là absence/failure; không biến candidate gap thành audit finding hoặc potential conflict thành actual conflict. |
| 10 | Thiết kế target-state options từ objective, obligation, appetite, capacity, technology và practicality. | Options có benefit, risk, cost, complexity, dependency, metric và residual exposure. | Process/risk owner duyệt option; không mặc định option phức tạp nhất. |
| 11 | Tạo các view RCM/workflow/RACI/overlay thực sự cần từ cùng object/relationship set. | Views tie-out theo logical IDs và scoped observations/source; giữ legacy fields nếu đọc input cũ. | Không duy trì view độc lập không có reconciliation rule hoặc ghi đè source để hòa giải conflict. |
| 12 | QA objects, diagram nếu có, nulls, observation links, legacy mapping và cross-document tie-out trong scope. | QA execution record, conflict/unresolved items và correction log. | Chặn claim/phát hành trong phạm vi còn lỗi trọng yếu; có thể bàn giao partial draft với giới hạn rõ, không dùng waiver để chứng minh fact thiếu. |
| 13 | Trả structured content/Markdown tương xứng; chỉ handoff Word, Excel, PowerPoint hoặc dashboard khi được yêu cầu và có capability. | Deliverable draft giữ source, limitations, confidence và review status. | Format đẹp không phải evidence; không gửi ngoài tổ chức nếu chưa được duyệt. |
| 14 | Chuyển recommendation hoặc design opportunity thành action handoff khi phù hợp. | Action plan liên kết no-change exposure, dependency, approval, owner/date basis chưa biết thì để thiếu. | Không tạo fake current gap, tự sửa source/ERP/production hoặc đóng action thiếu closure evidence. |

## 10. Execution, retry và stop rules

Trước mỗi subtask, xác định:

- `entry_condition`
- `success_criteria`
- `stop_condition`
- `failure_condition`
- `authorized_actions`
- `approval_gate`

Không chạy lại cùng analysis với cùng input và cùng method. Với lỗi kỹ thuật có thể khắc phục trong quyền hiện có, retry tối đa hai lần, ghi nguyên nhân và thay đổi phương pháp. Sau hai lần thất bại, dừng phần bị ảnh hưởng và trả partial result/failure record/human-review request. Permission denial, paywall hoặc authority không rõ là stop ngay cho hành động đó, không phải lý do retry thử đường truy cập khác để vượt chặn.

Dừng ngay phần hành động/kết luận bị ảnh hưởng khi:

- thiếu authority cho external/destructive/production action;
- nguồn trọng yếu không thể truy cập và không có phương án kiểm chứng;
- inputs mâu thuẫn làm thay đổi material conclusion;
- workstream yêu cầu legal/audit/technical conclusion ngoài phạm vi;
- data classification không cho phép tiếp tục xử lý.

Phần độc lập có authority và dữ liệu phù hợp vẫn có thể tiếp tục. Không nhận thiếu external baseline là lý do dừng mọi proposal, nhưng phải giữ nhãn provisional và giới hạn benchmark. Không nêu toàn engagement hoàn thành khi còn phần trọng yếu chưa xử lý; không suy phê duyệt từ tool access hoặc việc người dùng chấp nhận một partial draft.

## 11. Acceptance evidence

Tách bốn loại kết quả kiểm thử:

- `structural`: package, metadata, files, links và schema;
- `deterministic`: IDs, relationships, required fields và invariant rules;
- `behavioral`: forward-test bằng model trên raw task/artifact;
- `manual`: visual, professional hoặc legal review.

Không gộp chúng thành một tỷ lệ pass duy nhất. Ghi platform, model, date, skill version/hash, test input hash, result, evidence, reviewer, limitation và remediation status.

Behavioral evidence cần raw prompt/input/output, actual tool/source trace, case/variant ID và rubric tách khỏi model under test. Case hoặc platform chưa chạy giữ not_run; missing run evidence không tính verified pass. Static YAML/schema validation, template completeness hoặc parity ZIP không chứng minh E2E reasoning, OCR/handoff đã chạy hay compatibility trên mọi host. Ghi model identifier đúng mức host cung cấp, không tự điền metadata còn thiếu.
