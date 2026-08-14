# Phân tích tài liệu và khám phá quy trình hiện trạng

## Mục lục

1. [Thiết lập phạm vi và bảo toàn nguồn](#1-thiết-lập-phạm-vi-và-bảo-toàn-nguồn)
2. [Phân tích Policy, Standard, SOP và Procedure](#2-phân-tích-policy-standard-sop-và-procedure)
3. [Phát hiện lỗi và mâu thuẫn tài liệu](#3-phát-hiện-lỗi-và-mâu-thuẫn-tài-liệu)
4. [Khám phá current-state process](#4-khám-phá-current-state-process)
5. [Xây dựng step register](#5-xây-dựng-step-register)
6. [Quản lý confidence và corroboration](#6-quản-lý-confidence-và-corroboration)
7. [Ghi nhận deviation](#7-ghi-nhận-deviation)
8. [Phỏng vấn và walkthrough](#8-phỏng-vấn-và-walkthrough)
9. [Kết luận được phép và không được phép](#9-kết-luận-được-phép-và-không-được-phép)
10. [Kiểm tra chất lượng đầu ra](#10-kiểm-tra-chất-lượng-đầu-ra)

## 1. Thiết lập phạm vi và bảo toàn nguồn

Thực hiện intake trước khi phân tích:

1. Xác định business objective, câu hỏi cần trả lời và deliverable.
2. Xác định legal entity, business unit, site, product, transaction type và kỳ áp dụng.
3. Xác định lớp cần phân tích: `As-Documented`, `As-Designed`, `As-Performed` hoặc `Target-State`.
4. Lập source register và giữ nguyên file gốc theo chế độ read-only.
5. Tạo working copy nếu cần annotation; không ghi đè tài liệu hiện hành.
6. Ghi data classification và giới hạn truy cập.
7. Ghi rõ tài liệu hoặc evidence còn thiếu trước khi kết luận.

Dùng source register sau:

| source_id | title | type | version | effective_date | owner | status | confidentiality | location | reliability_note |
|---|---|---|---|---|---|---|---|---|---|
| `<SRC-ID>` | `<title>` | `<Policy/SOP/...>` | `<version>` | `<date>` | `<owner>` | `<active/draft/...>` | `<class>` | `<path/link>` | `<note>` |

Ghi trích dẫn theo section, clause, page, row hoặc event identifier. Không chỉ dẫn chung tới tên file khi phát hiện phụ thuộc một đoạn cụ thể.

## 2. Phân tích Policy, Standard, SOP và Procedure

Đánh giá tối thiểu 14 nhóm sau. Ghi `Present`, `Partial`, `Missing`, `Conflicting`, `Not applicable` và bằng chứng tương ứng.

### 2.1 Document governance

Kiểm tra `document_id`, version, owner, approver, approval date, effective date, review date, superseded version, distribution, confidentiality và revision history. Xác minh tài liệu đang hiệu lực; không mặc định bản mới nhất trong thư mục là bản được phê duyệt.

### 2.2 Purpose và objective

Xác định tài liệu muốn đạt outcome nào. Kiểm tra objective có liên kết business objective, customer/stakeholder need và metric hay không.

### 2.3 Scope

Xác định entity, unit, site, role, product, transaction, system, geography và exclusions. Phát hiện overlap hoặc gap giữa các tài liệu cùng điều chỉnh một phạm vi.

### 2.4 Definitions

Đối chiếu terminology và acronym register. Ghi mọi thuật ngữ không định nghĩa, định nghĩa vòng tròn, collision hoặc khác nghĩa giữa tài liệu.

### 2.5 Roles và responsibilities

Xác định Process Owner, Risk Owner, Control Owner, Performer, Reviewer, Approver, System Owner, Data Owner, Document Owner và Escalation Authority. Không mặc định các vai trò này là một người.

### 2.6 Process flow

Trích xuất trigger, input, boundary, steps, decisions, approvals, handoffs, outputs, exception paths và end condition. Ghi ID cho từng bước trước khi vẽ sơ đồ.

### 2.7 Controls

Trích xuất control objective, risk linkage, control action, owner, frequency/trigger, preventive/detective/corrective type, manual/automated nature, evidence, precision, exception handling và reviewer.

### 2.8 Systems và data

Xác định system of record, source data, required fields, master data, interface, spreadsheet/manual file, access role, configuration dependency và audit trail.

### 2.9 Exceptions

Kiểm tra emergency path, override, waiver, deviation approval, logging, expiry, compensating control, monitoring và escalation. Không coi ngoại lệ không ghi nhận là quy trình được phép.

### 2.10 Records và retention

Xác định record, evidence location, retention period, custodian, access, legal hold, disposal và traceability tới transaction/control.

### 2.11 Monitoring

Xác định KPI, KRI, KCI, exception report, review cadence, threshold owner, escalation và remediation tracking.

### 2.12 Training và communication

Xác định đối tượng đào tạo, timing, nội dung, acknowledgement, completion evidence, refresher requirement và communication khi thay đổi.

### 2.13 Change management

Xác định change requester, impact assessment, approver, version control, effective date, system/configuration alignment, form update, training và withdrawal bản cũ.

### 2.14 Cross-reference

Kiểm tra link tới Policy, Standard, SOP, law/regulation, contract, form, approval matrix, system manual và record retention schedule. Xác minh version và hiệu lực của nguồn được dẫn.

Dùng checklist kết quả:

| check_id | component | status | finding | source | impact | action | owner |
|---|---|---|---|---|---|---|---|
| `<DOC-CHK>` | `<component>` | `<status>` | `<finding>` | `<source_id:location>` | `<impact>` | `<action>` | `<owner>` |

## 3. Phát hiện lỗi và mâu thuẫn tài liệu

Chủ động tìm các tình trạng sau:

- Thiếu scope, owner, approval, effective date hoặc review cycle.
- Tài liệu hết hiệu lực, chưa phê duyệt hoặc reference bản cũ.
- Hai tài liệu mâu thuẫn về role, threshold, sequence, system hoặc evidence.
- Role được nêu nhưng không tồn tại trong RACI hoặc organization structure.
- Flow bị đứt, circular approval, self-approval hoặc decision thiếu outcome.
- Control thiếu risk, objective, owner, timing, evidence, precision hoặc exception handling.
- Exception thiếu authority, expiry, log hoặc compensating control.
- System không hỗ trợ control được mô tả hoặc SOP không phản ánh configuration.
- Form, template hoặc checklist không khớp trường dữ liệu và approval trong SOP.
- Không có retention, escalation, change control, alternate role hoặc contingency.
- Policy bị viết như Work Instruction; SOP chỉ nêu principle; Guideline bị dùng như mandatory requirement.

Phân loại mâu thuẫn trước khi đề xuất xử lý:

| Loại | Ví dụ | Xử lý |
|---|---|---|
| `Authority conflict` | Policy và SOP quy định khác nhau | Xác định hierarchy và approver; không tự chọn bản thuận tiện |
| `Version conflict` | Form cũ dùng với SOP mới | Xác minh effective date và transition |
| `Role conflict` | RACI khác approval matrix | Yêu cầu Process Owner và authority owner xác nhận |
| `System conflict` | SOP yêu cầu bước hệ thống không có | Kiểm tra configuration và workaround thực tế |
| `Threshold conflict` | Hai mức phê duyệt khác nhau | Xác minh Delegation of Authority và ngày hiệu lực |
| `Terminology conflict` | Một thuật ngữ có hai nghĩa | Chuẩn hóa glossary và ghi impact |

Không tự giải quyết mâu thuẫn có ảnh hưởng quyền phê duyệt, compliance hoặc key control. Chuyển human decision gate.

## 4. Khám phá current-state process

Kết hợp nguồn theo độ tin cậy và mục đích:

- Dùng Policy, SOP, flowchart và form để dựng `As-Documented`.
- Dùng interview và workshop để tạo hypothesis và câu hỏi xác minh.
- Dùng walkthrough, screenshot, ticket, email và transaction evidence để xác nhận activity.
- Dùng ERP transaction, event log và analytics để xác nhận sequence, variant, frequency và cycle time.
- Dùng incident, audit finding và complaint để tìm exception, bypass và failure mode.

Thực hiện discovery theo trình tự:

1. Xác định trigger và business outcome.
2. Xác định start/end boundary và customer.
3. Xác định supplier, inputs và outputs.
4. Xác định actor, role, system và data object.
5. Liệt kê happy path theo thời gian.
6. Thêm decision, approval và handoff.
7. Thêm exception, rework, backlog, cancellation và escalation.
8. Gắn risks, controls, evidence và dependencies.
9. Đối chiếu với tài liệu và data.
10. Ghi deviation và unresolved question.
11. Xác nhận bản đồ với performer và Process Owner riêng biệt khi material.

Không bắt đầu bằng sơ đồ đẹp. Hoàn thành step register và source mapping trước.

## 5. Xây dựng step register

Tạo record tối thiểu cho từng bước:

```yaml
step_id: STEP-P2P-PR-010
analysis_layer: As-Performed
step_name: Review purchase request
step_type: manual_task
predecessors: [STEP-P2P-PR-005]
trigger_or_entry_condition: Request submitted
performer: Procurement Analyst
reviewer: null
approver: null
system: ERP
inputs: [purchase_request]
outputs: [validated_request]
decision_rules: []
handoff_to: Procurement Manager
sla: Not defined
risk_ids: [RSK-P2P-003]
control_ids: [CTL-P2P-007]
evidence: [ERP workflow history]
exception_path: EX-P2P-02
source_ids: [SRC-04, EVT-2026-Q2]
confirmation_status: Data-confirmed
confidence: High
```

Giữ task name ở thể chủ động. Tách decision khỏi task nếu decision tạo nhiều route. Ghi rõ manual action, system action và hybrid action.

## 6. Quản lý confidence và corroboration

Áp dụng trạng thái sau cho từng step và finding:

- `Documented`
- `Interview-confirmed`
- `Evidence-confirmed`
- `Data-confirmed`
- `Inferred`
- `Unresolved`

Nâng confidence chỉ khi có nguồn mới hoặc corroboration. Không đổi `Interview-confirmed` thành `Evidence-confirmed` vì Process Owner đồng ý.

Dùng quy tắc:

| Nguồn | Giá trị chính | Hạn chế cần ghi |
|---|---|---|
| Policy/SOP | Authority và thiết kế được tài liệu hóa | Không chứng minh thực hiện |
| Interview | Context, exception và tacit knowledge | Recall bias, management representation |
| Walkthrough | Sequence và evidence của một hoặc vài case | Không đại diện population |
| Event log | Sequence, frequency, variant và timing | Phụ thuộc data lineage và event semantics |
| Sample evidence | Hoạt động trên selected items | Phụ thuộc sampling và completeness |
| Process mining | Pattern toàn population có log | Không tự chứng minh cause hoặc control failure |

Ghi validation action cho mọi item `Low`, `Inferred` hoặc `Unresolved` có ảnh hưởng material.

## 7. Ghi nhận deviation

Tạo deviation record riêng; không sửa trực tiếp As-Documented để phản ánh thực tế.

```yaml
deviation_id: DEV-P2P-014
process_id: P2P-PR
documented_step: Manager approves before PO creation
performed_step: PO created before approval in 18 cases
source: EVT-2026-Q2
frequency: 18/1240
reason: <confirmed reason or Unresolved>
risk: Unauthorized commitment
control_impact: Preventive approval may be bypassed
authorized_or_unauthorized: Unresolved
owner: Procurement Process Owner
recommended_action: Validate emergency-purchase route and approval timestamps
confidence: High
```

Phân biệt:

- `Authorized deviation`: có authority, duration, rationale, logging và compensating control hợp lệ.
- `Unauthorized deviation`: trái yêu cầu hiện hành và không có approval hợp lệ.
- `Unresolved deviation`: chưa đủ bằng chứng về authority hoặc context.
- `Documentation gap`: thực tế được phê duyệt nhưng tài liệu chưa cập nhật.
- `System-enforced variant`: configuration tạo path khác SOP.

Không gọi deviation là control failure trước khi xác minh control design, timing, population và exception rule.

## 8. Phỏng vấn và walkthrough

Yêu cầu người tham gia mô tả một case gần nhất thay vì chỉ mô tả “quy trình chuẩn”. Hỏi theo thứ tự:

1. Điều gì khởi tạo case?
2. Ai nhận input đầu tiên và qua kênh nào?
3. Người thực hiện kiểm tra gì, dựa trên dữ liệu nào?
4. System ghi lại event hoặc evidence nào?
5. Điều kiện nào tạo approval, rejection, rework hoặc escalation?
6. Handoff xảy ra khi nào và bên nhận biết việc bằng cách nào?
7. Exception phổ biến và workaround là gì?
8. Ai có quyền override và dấu vết còn lại là gì?
9. Khi người hoặc system chính không sẵn sàng thì xử lý thế nào?
10. Metric hoặc report nào phát hiện backlog, error hoặc bypass?

Trong walkthrough, chọn case có identifier, lần theo từ trigger đến outcome, thu thập evidence tối thiểu cần thiết và che dữ liệu cá nhân không liên quan.

## 9. Kết luận được phép và không được phép

Khi chỉ có tài liệu, chỉ kết luận về:

- Document completeness.
- Internal consistency.
- Design adequacy ở mức lý thuyết.
- Risk/control coverage theo nội dung được mô tả.
- Testability của control description.

Chỉ chuẩn bị draft operating-effectiveness assessment và test-results handoff khi có testing objective, approved methodology, population, sampling hoặc full-population method, executed procedure, evidence, data-reliability work và test result phù hợp. Skill không tự phát hành formal operating-effectiveness conclusion; assurance owner độc lập có thẩm quyền phải review và kết luận. Nếu chưa đủ, dùng “Potential test of operating effectiveness”.

Không bịa step, role, threshold, configuration, legal requirement, frequency hoặc sample result. Ghi assumption, confidence và validation plan.

## 10. Kiểm tra chất lượng đầu ra

Trước khi bàn giao, xác nhận:

- Source register có version, hiệu lực và provenance.
- Mọi finding dẫn đúng source location.
- As-Documented và As-Performed được tách riêng.
- Step register có trigger, owner, system, input/output, handoff, exception và evidence.
- Mọi deviation có frequency hoặc ghi rõ chưa biết.
- Mọi statement về authority được kiểm tra với hierarchy tài liệu.
- Mọi confidence có căn cứ và validation action khi cần.
- Không đánh giá operating effectiveness chỉ từ SOP, interview hoặc một walkthrough.
- Mọi dữ liệu nhạy cảm được phân loại, tối thiểu hóa và mask phù hợp.
- Mọi mâu thuẫn material có owner và human decision gate.
