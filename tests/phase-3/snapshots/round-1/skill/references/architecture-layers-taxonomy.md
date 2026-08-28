# Kiến trúc phân tích, phân cấp quy trình và taxonomy

## Mục lục

1. [Áp dụng bốn lớp phân tích](#1-áp-dụng-bốn-lớp-phân-tích)
2. [Quản lý bằng chứng và confidence](#2-quản-lý-bằng-chứng-và-confidence)
3. [Phân cấp quy trình L0-L5](#3-phân-cấp-quy-trình-l0-l5)
4. [Chuẩn hóa process object](#4-chuẩn-hóa-process-object)
5. [Đặt tên và quản lý acronym](#5-đặt-tên-và-quản-lý-acronym)
6. [Phân cấp tài liệu](#6-phân-cấp-tài-liệu)
7. [Đối chiếu lớp, cấp và tài liệu](#7-đối-chiếu-lớp-cấp-và-tài-liệu)
8. [Kiểm tra chất lượng](#8-kiểm-tra-chất-lượng)
9. [Ánh xạ E2E theo phạm vi mở](#9-ánh-xạ-e2e-theo-phạm-vi-mở)

## 1. Áp dụng bốn lớp phân tích

Gắn nhãn từng ghi nhận bằng lớp có căn cứ; chưa biết thì giữ null/Unresolved và nêu phần cần xác nhận. Không trộn các lớp vào một bản đồ duy nhất nếu không biểu diễn rõ nguồn gốc và chênh lệch.

| Lớp | Câu hỏi phải trả lời | Nguồn được dùng | Điều không được kết luận |
|---|---|---|---|
| `As-Documented` | Tài liệu hiện hành quy định phải làm gì? | Policy, Standard, SOP, Procedure, Work Instruction, approval matrix, form, system manual, contract, nghĩa vụ pháp lý | Không suy ra rằng hoạt động đã vận hành thực tế |
| `As-Designed` | Thiết kế hiện trạng được xác nhận ra sao? | Tài liệu, thiết kế hệ thống, control design hoặc architecture có căn cứ xác nhận | Không coi đề xuất của analyst là thiết kế hiện hành hoặc bằng chứng operating effectiveness |
| `As-Performed` | Người và hệ thống thực tế đã làm gì? | Walkthrough, observation, event log, transaction data, email, ticket, evidence, sample testing, process mining | Không xác nhận chỉ dựa vào policy, SOP hoặc management representation |
| `Target-State` | Quy trình tương lai nên vận hành ra sao? | Mục tiêu, risk appetite, nghĩa vụ, technology, capacity, cost, best practice và practicality | Không trình bày đề xuất như trạng thái hiện hành hoặc quyết định đã phê duyệt |

Thực hiện theo thứ tự sau:

1. Xác định lớp mà người dùng yêu cầu.
2. Tách các nguồn theo lớp trước khi trích xuất bước.
3. Gắn `analysis_layer` cho từng object.
4. Ghi `source_id`, `source_location`, `source_date` và `confidence`.
5. Lập deviation record khi hai lớp không khớp.
6. Yêu cầu xác nhận khi nguồn không đủ để nâng confidence.
7. Gắn mọi Target-State là `draft` cho đến khi có human approval.

Biểu diễn so sánh nhiều lớp bằng ma trận:

| process_step_id | As-Documented | As-Designed | As-Performed | Target-State | gap_or_change | evidence |
|---|---|---|---|---|---|---|
| `<ID>` | `<quy định>` | `<logic thiết kế>` | `<thực tế>` | `<đề xuất>` | `<chênh lệch>` | `<source_id>` |

Không để ô trống gây hiểu nhầm. Với dữ liệu thiếu, dùng null semantics chuẩn: `Not provided`, `Not applicable`, `To be validated` hoặc `Unresolved`. Dùng `Not assessed` trong trường `assessment_status` hoặc `design_assessment` khi chưa đánh giá; với `evidence_status`, dùng `Not checked` trước khi kiểm tra và `Insufficient evidence` khi đã đánh giá nhưng bằng chứng chưa đủ. Các trạng thái này không thay thế dữ kiện bị thiếu.

## 2. Quản lý bằng chứng và confidence

Phân loại trạng thái xác nhận của từng bước:

- `Documented`: có nguồn tài liệu xác định.
- `Interview-confirmed`: có người thực hiện hoặc owner xác nhận; vẫn cần corroboration nếu kết luận quan trọng.
- `Evidence-confirmed`: có evidence hoạt động cụ thể.
- `Data-confirmed`: có population hoặc event data đủ tin cậy.
- `Inferred`: suy luận hợp lý nhưng chưa được xác nhận.
- `Unresolved`: nguồn mâu thuẫn hoặc thiếu dữ liệu trọng yếu.

Gán mức confidence theo bằng chứng, không theo cảm giác:

| Confidence | Điều kiện tối thiểu | Cách diễn đạt |
|---|---|---|
| `High` | Nhiều nguồn độc lập nhất quán hoặc data/evidence trực tiếp đã kiểm tra | “Được xác nhận bởi…” |
| `Medium` | Một nguồn đáng tin cậy hoặc nhiều nguồn gián tiếp nhất quán | “Có cơ sở cho thấy…” |
| `Low` | Chỉ có interview, mô tả chưa kiểm chứng hoặc suy luận | “Chưa xác nhận; cần…” |
| `Unresolved` | Không đủ nguồn hoặc nguồn xung đột chưa giải quyết | “Không đủ dữ liệu để kết luận” |

Giữ riêng `evidence_strength` và `design_quality`. Không tăng confidence chỉ vì thiết kế có vẻ hợp lý.

## 3. Phân cấp quy trình L0-L5

Chỉ gán L0–L5 sau khi có đủ boundary, parent, trigger, outcome và object granularity để chứng minh level. Tên process, tên phòng ban hoặc nhãn “silo” không tự chứng minh một object là L1, L2 hay L3. Nếu input chỉ cho biết map chia theo phòng ban, phân loại `department-centric fragmentation`, để `process_level: To be validated`, và đề xuất dựng trigger-to-outcome crosswalk; không khẳng định L1 đang thiếu hoặc các mảnh hiện tại là L2–L3 nếu chưa có source.

Dùng sáu cấp sau làm quy ước nội bộ của skill khi phù hợp. Không coi chúng tương ứng trực tiếp với level/ID của mọi thư viện ngoài, hoặc bắt mọi câu hỏi phải có đủ sáu cấp:

| Cấp | Tên chuẩn | Mục đích | Ví dụ |
|---|---|---|---|
| `L0` | Enterprise Value Chain | Nhóm năng lực tạo giá trị hoặc hỗ trợ toàn doanh nghiệp | Supply Chain |
| `L1` | End-to-End Process | Chuỗi trigger-to-outcome xuyên chức năng | Procure-to-Pay |
| `L2` | Process | Cụm hoạt động tạo một kết quả quản trị rõ ràng | Procurement |
| `L3` | Subprocess | Phần quy trình có boundary và owner xác định | Purchase Requisition |
| `L4` | Activity | Hoạt động nghiệp vụ có đầu vào và đầu ra | Review purchase request |
| `L5` | Task / Work Instruction | Thao tác cụ thể có thể giao cho performer | Check budget code and attachments |

Xác định cấp theo logic, không theo độ dài tên:

1. Chọn `L1` khi object đi từ trigger đến outcome cho customer/stakeholder và thường xuyên qua nhiều chức năng.
2. Chọn `L2-L3` khi object có boundary, owner và output trung gian riêng.
3. Chọn `L4` khi object mô tả một activity có thể đặt trong flow.
4. Chọn `L5` khi object mô tả cách thực hiện chi tiết một task.
5. Không tạo `L4` hoặc `L5` nếu người dùng chỉ yêu cầu architecture-level view.
6. Không dùng department làm process name nếu chưa diễn đạt activity hoặc outcome.

Giữ quan hệ cha-con hợp lệ:

```text
L0 Supply Chain
└── L1 Procure-to-Pay
    └── L2 Procurement
        └── L3 Purchase Requisition
            └── L4 Review purchase request
                └── L5 Check budget code and required attachments
```

## 4. Chuẩn hóa process object

Tạo một record cho mỗi process object. Dùng `null` hoặc trạng thái thiếu dữ liệu rõ ràng; không bịa giá trị.

```yaml
process_id: PROC-P2P-PR-001
parent_process_id: P2P-PR
process_level: L4
process_name: Review purchase request
acronym: null
analysis_layer: As-Documented
objective: <mục tiêu>
trigger: <sự kiện bắt đầu>
start_boundary: <điểm bắt đầu>
end_boundary: <điểm kết thúc>
customer: [<đối tượng nhận kết quả>]
supplier: [<đối tượng cung cấp input>]
inputs: [<input>]
outputs: [<output>]
owner: <process owner>
participants: [<role>]
systems: [<system>]
data: [<data object>]
frequency: <tần suất hoặc trigger>
volume: <khối lượng hoặc Not provided>
service_level: <SLA hoặc Not defined>
risks: [<risk_id>]
controls: [<control_id>]
kpi: [<metric_id>]
kri: [<metric_id>]
kci: [<metric_id>]
dependencies: [<dependency_id>]
exceptions: [<exception_id>]
source_ids: [<source_id>]
confidence: <High|Medium|Low|Unresolved>
```

Bảo toàn `process_id` giữa process map, RACI, RCM, metric register và audit handoff. Không tái sử dụng ID cho object khác.

## 5. Đặt tên và quản lý acronym

Đặt tên quy trình theo các quy tắc sau:

- Dùng động từ và kết quả hoặc cấu trúc `Trigger-to-Outcome`.
- Diễn đạt một outcome đủ cụ thể để phân biệt với quy trình lân cận.
- Tránh tên phòng ban, jargon nội bộ chưa định nghĩa và từ đồng nghĩa trùng lặp.
- Giữ tên ổn định sau khi phát hành; quản lý tên cũ bằng alias.
- Không tự dịch acronym phổ biến nếu làm mất nghĩa chuyên môn.

Quản lý acronym bằng register:

| acronym | canonical_name | aliases | status | collision_rule | owner |
|---|---|---|---|---|---|
| `P2P` | Procure-to-Pay | Purchase-to-Pay | example-only | Candidate: dành `P2P` cho Procure-to-Pay | `Not provided` |
| `P2Prod` | Plan-to-Produce | Plan2Produce | example-only | Candidate: không dùng `P2P` | `Not provided` |
| `R2R` | Record-to-Report | Record-to-Reporting | example-only | Candidate: dành `R2R` cho Record-to-Report | `Not provided` |
| `Risk2Treatment` | Risk-to-Treatment | Risk-to-Response | example-only | Candidate: không dùng `R2R` | `Not provided` |

Các dòng trên chỉ minh họa cách tách collision, không phải acronym đã được organization phê duyệt. Khi input chỉ cho biết có collision, chỉ kết luận `acronym collision`; không tự suy ra process level, trigger, end state, owner, system dependency hoặc tên thay thế chính thức. Ghi các field đó `Not provided`/`To be validated`; nếu nêu alias, đánh dấu rõ là candidate proposal cần Process Owner hoặc process-governance owner phê duyệt. Nếu tạo ID minh họa, dùng prefix canonical trong common data model, không tự tạo prefix khác.

Trước khi cấp acronym mới:

1. Tra register hiện hành.
2. Kiểm tra trùng trong enterprise, function và system namespace.
3. Ưu tiên acronym đã được organization phê duyệt.
4. Đề xuất tên thay thế nếu có collision.
5. Ghi owner, ngày hiệu lực, aliases và deprecated terms.
6. Không tự đặt acronym rồi trình bày như tên chính thức.

## 6. Phân cấp tài liệu

Phân biệt tài liệu theo chức năng quản trị:

| Loại | Nội dung nên có | Không nên dùng thay cho |
|---|---|---|
| `Policy` | Nguyên tắc, mục tiêu, quyền hạn, trách nhiệm, yêu cầu bắt buộc, governance | Work Instruction chi tiết |
| `Standard` | Yêu cầu chi tiết hoặc chuẩn tối thiểu phải đáp ứng | Process flow hoàn chỉnh |
| `Process` | End-to-end flow, boundary và outcome | Hướng dẫn thao tác màn hình |
| `SOP / Procedure` | Trình tự activity, role, control, evidence và exception | Policy-level authority |
| `Work Instruction` | Cách thực hiện task cụ thể | End-to-end process |
| `Guideline` | Khuyến nghị và lựa chọn áp dụng | Mandatory policy nếu chưa được ban hành |
| `Form / Template / Checklist` | Công cụ thực hiện và ghi nhận evidence | Bằng chứng đã hoàn thành tự thân |
| `Record / Evidence` | Dấu vết chứng minh activity hoặc control đã vận hành | Thiết kế quy trình |

Gắn tối thiểu các metadata sau cho mỗi tài liệu: `document_id`, `title`, `document_type`, `version`, `owner`, `approver`, `approval_date`, `effective_date`, `review_date`, `status`, `confidentiality`, `supersedes`, `source_location`.

Phát hiện và ghi issue khi:

- Policy bị viết như Work Instruction.
- SOP chỉ nêu nguyên tắc mà không có sequence, owner, control hoặc evidence.
- Guideline được áp dụng như nghĩa vụ bắt buộc nhưng không có authority.
- Form không liên kết với process step hoặc control.
- Record requirement không quy định nơi lưu, retention hoặc quyền truy cập.
- Hai tài liệu điều chỉnh cùng scope nhưng khác threshold, role hoặc version.

## 7. Đối chiếu lớp, cấp và tài liệu

Thực hiện tie-out theo chuỗi:

```text
Business objective
→ L0 value chain
→ L1 end-to-end process
→ L2-L3 process architecture
→ L4 activities
→ L5 tasks
→ Policy/Standard requirements
→ SOP/Work Instruction execution
→ Form/Record evidence
→ As-Performed validation
→ Target-State change
```

Lập crosswalk tối thiểu:

| process_id | level | document_id | document_type | requirement_or_step | analysis_layer | risk_ids | control_ids |
|---|---|---|---|---|---|---|---|
| `<ID>` | `<L0-L5>` | `<DOC-ID>` | `<type>` | `<text>` | `<layer>` | `<IDs>` | `<IDs>` |

Không ép một tài liệu vào một cấp nếu tài liệu bao phủ nhiều cấp. Tách mapping theo section hoặc clause.

## 8. Kiểm tra chất lượng

Trước khi phát hành output, xác nhận:

- Mọi process object có `analysis_layer`.
- Mọi nhận định As-Performed có evidence ngoài tài liệu thiết kế hoặc được ghi là chưa xác nhận.
- Mọi Target-State được gắn `draft` và có approval owner.
- Mọi object L1 có trigger, outcome, customer và end boundary.
- Mọi quan hệ cha-con dùng cấp liền kề hoặc giải thích ngoại lệ.
- Mọi acronym đã được kiểm tra collision.
- Mọi document type phản ánh đúng chức năng tài liệu.
- Mọi ID nhất quán giữa process map, RACI, RCM, metrics và evidence.
- Mọi trường thiếu dùng trạng thái rõ ràng, không dùng suy đoán ngầm.

## 9. Ánh xạ E2E theo phạm vi mở

94 seed profiles không phải giới hạn phạm vi. Xác định objective, customer, trigger, outcome và boundary trước khi chọn E2E.

- Tách scope tài liệu khỏi E2E lớn hơn: SOP có thể chỉ là một subprocess. Interfaces ngoài tài liệu là candidate cần xác nhận, không phải steps hiện hành đã biết.
- Đối chiếu mục tiêu, inputs/outputs, activities và handoffs; tên gần giống hoặc acronym trùng chưa đủ chứng minh mapping.
- Khi cần, dùng [external-process-control-libraries.md](external-process-control-libraries.md) để tìm nguồn phù hợp trong hoặc ngoài catalog. Taxonomy không tự xác định workflow sequence hay controls.
- Giữ `process_id` nội bộ riêng. `reference_library_id` là ID catalog nội bộ của skill, như `LIB-P01`, không phải ID do publisher cấp; `reference_item_id` là ID item của publisher. Chỉ ghi publisher item ID/version/locator khi đã đọc đúng nguồn; nếu chưa biết thì để null.
- Cho phép một process có nhiều mappings với rationale cho primary, supporting hoặc overlap. Shared logical controls không bị nhân thành controls mới chỉ vì liên quan nhiều E2E.
- Ghi fit_status và rationale/evidence; không tự tạo similarity score. Khi chưa có match đáng tin, giữ unresolved/no_reliable_match và hỏi dữ kiện phân định nếu cần.
- Có thể đề xuất tên và boundary riêng của tổ chức ở Target-State; phải nhận diện đó là đề xuất, không giả làm tên chuẩn của publisher.

Mapping không tự là quyết định áp dụng framework. Dùng các mapping records trong [process-architecture-step-register.yaml](../templates/process-architecture-step-register.yaml), không tạo thêm một nguồn facts độc lập.
