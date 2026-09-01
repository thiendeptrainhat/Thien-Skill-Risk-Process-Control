# Thiết kế Target-State và cải tiến quy trình

## Mục lục

1. [Điều kiện đầu vào](#1-điều-kiện-đầu-vào)
2. [Quy trình thiết kế Target-State](#2-quy-trình-thiết-kế-target-state)
3. [Xây dựng và so sánh phương án](#3-xây-dựng-và-so-sánh-phương-án)
4. [Thiết kế control by design](#4-thiết-kế-control-by-design)
5. [Cải tiến process và control efficiency](#5-cải-tiến-process-và-control-efficiency)
6. [Thư viện End-to-End process](#6-thư-viện-end-to-end-process)
7. [Đặc tả process family](#7-đặc-tả-process-family)
8. [Lập roadmap chuyển đổi](#8-lập-roadmap-chuyển-đổi)
9. [Approval và tiêu chí chấp nhận](#9-approval-và-tiêu-chí-chấp-nhận)

## 1. Điều kiện đầu vào

### Khi chỉ có một câu mô tả coverage gap

Nếu input chỉ nêu một process family “thiếu” một subprocess/control (không kèm artifact), phân loại `candidate end-to-end coverage gap` ở mức hypothesis. Không tự kết luận current control vắng mặt, không tự cấp gap/risk/control-objective/control ID, và không giả định source system, owner, SLA, population hoặc operating failure. Đưa risks, control objectives, target steps, control patterns và metrics dưới nhãn `candidate`; giữ ID `Not provided` cho đến khi có canonical register hoặc người dùng yêu cầu tạo draft ID. Khi tạo draft ID, chỉ dùng prefix từ common data model: `GAP-`, `RSK-`, `COBJ-`, `CTL-`, `STEP-`, `MET-`. Mọi typical system chỉ là system class hypothesis, không phải fact của organization.

Không thiết kế Target-State bằng cách chỉ sao chép và tô lại current-state. Thu thập hoặc ghi rõ trạng thái thiếu của:

- Business objective và customer/stakeholder outcome.
- Trigger, start boundary, end boundary và expected output.
- Current-state baseline theo đúng lớp `As-Documented`, `As-Designed` và `As-Performed`.
- Mandatory legal/regulatory, contractual, adopted-standard và policy requirements.
- Risk appetite, significant risks và control objectives.
- Volume, frequency, product/entity/site complexity và seasonality.
- Current và target service level.
- Capacity, skill, organization, technology và data constraints.
- Cost envelope, implementation horizon và dependency.
- Known incidents, audit findings, deviations, backlog và pain points.

Gắn `Target-State`, `draft`, owner, version và approval status cho mọi artifact. Không trình bày Target-State như configuration hoặc process đã được ban hành.

Với quy trình mới hoặc chưa có SOP, current-state baseline có thể là `Not provided`; vẫn thiết kế được Target-State trong phạm vi objective đã biết. Không tạo current controls, operating failures hoặc fake gaps để hoàn thành bảng. Recommendation có thể gắn trực tiếp design opportunity/control objective, không bắt buộc có gap hiện trạng.

## 2. Quy trình thiết kế Target-State

Dùng các bước sau theo dependency và mức chi tiết cần thiết; không ép câu hỏi hẹp phải thực hiện toàn bộ:

1. Xác nhận objective-led scope và measurable outcome.
2. Xác định trigger-to-outcome end-to-end trước khi chia theo function.
3. Chốt requirement baseline và phân loại mandatory/advisory.
4. Xác định risk appetite, control objectives và non-negotiable controls.
5. Phân tích volume, variation, exception và service demand.
6. Xác định process architecture L0-L5 ở mức cần thiết.
7. Loại bỏ bước không tạo giá trị hoặc không đáp ứng requirement.
8. Đơn giản hóa decision, handoff, role và data entry.
9. Thiết kế happy path, exception path, escalation và contingency.
10. Gán Process Owner, performer, reviewer, approver, System Owner và Data Owner.
11. Chọn system of record, source of truth và integration boundary.
12. Tích hợp controls vào process và system khi phù hợp.
13. Định nghĩa evidence, record retention và audit trail.
14. Định nghĩa KPI, KRI, KCI, target, threshold owner và response.
15. So sánh ít nhất các phương án phù hợp.
16. Đánh giá residual risk, feasibility và implementation dependency.
17. Thiết kế transition, training, change governance và rollback/contingency.
18. Đưa phương án khuyến nghị qua human approval gate.

Nếu nguồn chuẩn chưa được xác minh hoặc chưa được phép dùng, giữ phần phụ thuộc đó là chưa xác minh và ghi rõ phần thiết kế là analyst proposal. Role, system, threshold, mục tiêu đo lường và ngân sách chưa được cung cấp phải là đề xuất cần quyết định hoặc dữ kiện thiếu, không thành actual state.

Ghi traceability:

| target_step_id | objective | source_requirement | risk_id | control_objective | control_id | owner | system | metric_id | approval_status |
|---|---|---|---|---|---|---|---|---|---|
| `<ID>` | `<objective>` | `<source>` | `<risk>` | `<objective>` | `<control>` | `<role>` | `<system>` | `<metric>` | `draft` |

## 3. Xây dựng và so sánh phương án

Không mặc định mọi engagement cần đủ ba phương án. Khi lựa chọn có trade-off material, xây dựng tối thiểu các option sau hoặc giải thích vì sao không phù hợp.

### Option A — Minimum compliant / Minimum-control proposal

Chỉ dùng nhãn `Minimum compliant` khi mandatory baseline đã được xác minh và phương án được đối chiếu với baseline đó. Nếu baseline thiếu/chưa xác minh, dùng `Minimum-control proposal — compliance unverified` và ghi phần còn cần kiểm chứng; không suy compliance từ một proposal.

Hướng thiết kế là đáp ứng requirement bắt buộc đã xác minh và significant risk ở mức tối thiểu chấp nhận được. Ưu tiên thay đổi nhỏ, chi phí thấp và implementation nhanh. Ghi rõ manual-control burden, scalability và residual risk. Nhãn phương án không là kết luận formal compliance hoặc bằng chứng controls đã vận hành.

### Option B — Balanced control and efficiency

Cân bằng risk reduction, control effectiveness, customer experience, cycle time, cost, capacity và change effort. Dùng làm baseline so sánh, không mặc định là lựa chọn cuối cùng.

### Option C — Leading practice / automation-first

Tận dụng workflow integration, straight-through processing, preventive automated control, continuous monitoring và integrated data. Chỉ đề xuất khi process đã đủ chuẩn hóa, data đủ chất lượng và business case hợp lý.

So sánh options theo cùng căn cứ. Chỉ chấm điểm/trọng số khi có methodology được chấp thuận; nếu chưa có, dùng rationale định tính và để trống dữ liệu có trạng thái rõ:

| Tiêu chí | A | B | C | Trọng số | Căn cứ |
|---|---:|---:|---:|---:|---|
| Requirement coverage | `<score>` | `<score>` | `<score>` | `<%>` | `<source>` |
| Risk reduction / residual risk |  |  |  |  |  |
| Control effectiveness / testability |  |  |  |  |  |
| Customer experience / service level |  |  |  |  |  |
| Cycle time / capacity |  |  |  |  |  |
| Cost / benefit |  |  |  |  |  |
| Technology / data readiness |  |  |  |  |  |
| People / change impact |  |  |  |  |  |
| Implementation time / complexity |  |  |  |  |  |
| Dependency / delivery risk |  |  |  |  |  |

Với mỗi option, nêu rõ `benefits`, `risks`, `cost range`, `complexity`, `technology`, `people`, `implementation time`, `residual risk`, `dependencies`, `assumptions` và `confidence`.

Không chọn phương án có điểm tổng cao nếu vi phạm mandatory requirement hoặc vượt risk appetite. Tách constraint bắt buộc khỏi tiêu chí chấm điểm.

## 4. Thiết kế control by design

Xử lý risk theo thứ tự cân nhắc, không coi thứ tự là quy tắc tuyệt đối:

```text
Eliminate risk
→ Simplify process
→ Preventive automated control
→ Preventive manual control
→ Detective automated control
→ Detective manual control
→ Corrective control
```

Với mỗi control đề xuất, ghi:

- Risk và control objective được xử lý.
- Control Owner, performer và independent reviewer nếu có.
- Action, timing/trigger, population và criteria.
- Precision, threshold và source authority.
- System/data dependency và data-quality control.
- Evidence, retention và exception handling.
- Automation boundary và manual fallback.
- Cost, operational burden và testability.
- Key/supporting-control rationale.

Không tự động cho rằng automated control tốt hơn manual control. Kiểm tra configuration governance, access, change management, interface completeness, explainability và fallback trước khi đề xuất tự động hóa.

Không bỏ control chỉ vì làm chậm process. Xác định risk coverage và compensating control trước khi rationalize.

## 5. Cải tiến process và control efficiency

Tìm và lượng hóa khi có dữ liệu:

- Waste và non-value-added activity.
- Duplicate entry, duplicate control và duplicate approval.
- Rework, repeated error và incomplete-first-time rate.
- Handoff delay, queue, backlog và bottleneck.
- Manual reconciliation và spreadsheet dependency.
- Excessive control, missing control hoặc control không testable.
- Low-value report, unused report và monitoring không dẫn tới action.
- Poor master data, fragmented ownership và unclear accountability.
- System workaround, offline approval và manual bypass.
- Poor exception management, open-ended waiver và escalation chậm.

Áp dụng improvement pattern phù hợp:

| Pattern | Dùng khi | Không dùng khi |
|---|---|---|
| Eliminate | Bước không tạo value và không đáp ứng requirement/control | Bước là mandatory hoặc significant-risk control chưa có thay thế |
| Simplify | Decision, form hoặc handoff quá phức tạp | Complexity phản ánh requirement thực sự khác nhau |
| Standardize | Variant không có business rationale | Local/legal differences cần được duy trì |
| Consolidate | Nhiều review/control trùng objective và evidence | Cần independence hoặc SoD |
| Automate | Rule ổn định, data tốt, volume đủ và exception kiểm soát được | Process chưa chuẩn hóa hoặc logic thường xuyên thay đổi |
| Parallelize | Tasks độc lập và không phá sequence/control | Có dependency, authorization hoặc data prerequisite |
| Shift-left | Có thể phòng ngừa error sớm hơn | Chuyển burden nhưng không giảm risk/cost tổng thể |
| Continuous monitoring | Event/data đủ complete và timely | Data lineage hoặc alert ownership chưa đạt |

Đo baseline và target bằng cùng định nghĩa. Không tuyên bố benefit định lượng nếu chưa có volume, effort, unit cost hoặc phương pháp ước tính.

## 6. Thư viện End-to-End process

Dùng 94 families dưới đây như seed index cho discovery, không phải danh mục đầy đủ mọi E2E. Không từ chối quy trình ngoài seed hoặc ép một nhóm quy trình vào một family. Điều chỉnh theo objective, industry, business model, jurisdiction và organization.

Với quy trình mới hoặc nhiều E2E giao nhau, dùng [open-world mapping](architecture-layers-taxonomy.md#9-ánh-xạ-e2e-theo-phạm-vi-mở). Khi cần benchmark bên ngoài, dùng [external-process-control-libraries.md](external-process-control-libraries.md); taxonomy và vendor blueprint không tự là control standard.

Khi cần profile cụ thể cho một family, chỉ đọc đúng group liên quan trong [end-to-end-process-profiles.md](end-to-end-process-profiles.md). File đó cung cấp purpose, trigger, end state, subprocess hypotheses, risks, control objectives/patterns, system classes, KPI/KRI/KCI và adaptation notes cho đủ 94 family; tất cả vẫn là discovery hypothesis cần xác minh.

### A. Strategy, Governance và Risk

- Strategy-to-Execution
- Objective-to-Performance
- Policy-to-Compliance
- Risk-to-Treatment
- Audit-to-Remediation
- Issue-to-Closure
- Decision-to-Implementation
- Board-Meeting-to-Action

### B. Commercial và Customer

- Market-to-Lead
- Lead-to-Opportunity
- Lead-to-Order
- Quote-to-Cash
- Order-to-Cash
- Contract-to-Revenue
- Customer-Onboarding-to-Offboarding
- Complaint-to-Resolution
- Return-to-Refund
- Campaign-to-Conversion

### C. Procurement và Supplier

- Supplier-Onboarding-to-Offboarding
- Source-to-Contract
- Procure-to-Pay
- Request-to-Purchase
- Purchase-to-Receive
- Invoice-to-Payment
- Supplier-Performance-to-Remediation
- Supplier-Incident-to-Recovery

### D. Supply Chain và Manufacturing

- Demand-to-Plan
- Forecast-to-Fulfill
- Plan-to-Produce
- Material-to-Production
- Production-to-Inventory
- Inventory-to-Deliver
- Warehouse-to-Dispatch
- Transport-to-Delivery
- Quality-Event-to-CAPA
- Maintenance-to-Reliability
- Farm-to-Production
- Feed-to-Finish
- Harvest-to-Sale
- Recall-to-Closure

### E. Finance, Accounting và Tax

- Budget-to-Forecast
- Transaction-to-Record
- Record-to-Report
- Close-to-Disclose
- Invoice-to-Collection
- Treasury-to-Liquidity
- Cash-to-Reconciliation
- Tax-to-File
- Tax-to-Report
- Expense-to-Reimbursement
- Intercompany-to-Settlement
- Fixed-Asset-Acquisition-to-Retirement
- CAPEX-Idea-to-Asset

### F. Human Resources

- Workforce-Plan-to-Hire
- Hire-to-Retire
- Employee-Onboarding-to-Productivity
- Time-to-Payroll
- Payroll-to-Payment
- Learn-to-Perform
- Performance-to-Reward
- Employee-Case-to-Resolution
- Exit-to-Final-Settlement

### G. IT, Data và Cyber

- IT-Demand-to-Delivery
- Project-to-Deploy
- Change-to-Release
- Incident-to-Resolution
- Problem-to-Prevention
- Request-to-Fulfillment
- Identity-to-Access-to-Revoke
- Data-Creation-to-Disposal
- Data-to-Insight
- Model-Development-to-Monitoring
- Cyber-Alert-to-Incident-Closure
- Backup-to-Recovery

### H. Asset, Project và Investment

- Idea-to-Business-Case
- Business-Case-to-Investment
- Project-to-Closure
- Target-to-Acquisition
- Acquisition-to-Integration
- Acquire-to-Retire
- Site-Selection-to-Operation
- Construction-to-Handover

### I. Compliance, Legal và Third Party

- Obligation-to-Control
- Contract-Request-to-Execution
- Legal-Matter-to-Closure
- License-to-Renewal
- Third-Party-Due-Diligence-to-Offboarding
- Regulatory-Change-to-Implementation
- Whistleblowing-to-Resolution

### J. Resilience và Crisis

- Incident-to-Activation
- Disruption-to-Recovery
- Crisis-to-Stabilization
- Crisis-Communication-to-Reputation-Recovery
- Exercise-to-Improvement

Kiểm tra acronym collision trước khi dùng tên viết tắt. Trong seed index này, `P2P` chỉ Procure-to-Pay; không dùng quy ước này để đoán ý người dùng khi họ chỉ nói “P2P”. Hỏi objective/trigger/outcome hoặc context phân định trước khi kết luận.

## 7. Đặc tả process family

Khi dùng một process family, tạo profile:

```yaml
process_family: Procure-to-Pay
purpose: <business purpose>
trigger: <start event>
end_state: <measurable outcome>
typical_subprocesses: []
typical_risks: []
typical_control_objectives: []
typical_control_patterns: []
typical_systems: []
typical_kpi: []
typical_kri: []
typical_kci: []
industry_adaptation_notes: []
assumptions: []
validation_required: []
```

Gắn mọi nội dung “typical” là hypothesis cho discovery. Không trình bày role, threshold, control hoặc system từ thư viện như fact của organization.

## 8. Lập roadmap chuyển đổi

Tách thay đổi thành waves có dependency và acceptance criteria:

1. `Stabilize`: xử lý significant gap, clarify owner, cập nhật emergency control.
2. `Standardize`: thống nhất process, data, form, role và taxonomy.
3. `Simplify`: bỏ waste và rationalize control sau risk review.
4. `Digitize`: thay giấy/spreadsheet bằng controlled workflow.
5. `Automate`: tự động hóa rule ổn định và control đủ testable.
6. `Monitor`: triển khai KPI/KRI/KCI và continuous monitoring.

Với mỗi initiative, ghi `initiative_id`, current pain, target outcome, scope, owner, benefits, cost, dependency, risk, control impact, approval, target date, acceptance criteria và rollback/contingency.

Không triển khai automation trước khi chốt requirement, process standard, data quality, exception path và control ownership.

Đối chiếu cải tiến với trường hợp giữ nguyên: risk driver, protection hiện có, exposure còn lại và điều kiện cần xác minh. Dùng no-change scenario trong [gaps-rationalization-rcm.md](gaps-rationalization-rcm.md); không tự lượng hóa loss/probability hoặc coi sự cố tương lai là chắc chắn. Chỉ gán owner, due date và resources khi có căn cứ.

Nếu người dùng yêu cầu engagement đầy đủ theo R01–R07, luôn có một kết quả riêng cho R07. Với greenfield hoặc khi current gap chưa được chứng minh, dùng `scenario_basis: Design hypothesis` hoặc `Unverified gap hypothesis`: mô tả điều có thể xảy ra nếu không thiết lập thiết kế tối thiểu, ghi existing protection là `Not provided` khi chưa có dữ kiện, và nêu uncertainty/validation needed. Không biến giả thuyết này thành current deficiency hoặc incident.

## 9. Approval và tiêu chí chấp nhận

Yêu cầu human approval trước khi:

- Phê duyệt Target-State.
- Thay đổi authority, SoD, role hoặc organization.
- Bỏ key control hoặc giảm frequency/precision.
- Thay manual control bằng automated control.
- Thay production workflow hoặc configuration.
- Chấp nhận control gap hoặc residual risk.
- Phát hành Policy, SOP, RCM hoặc metric threshold chính thức.

Chỉ chuyển Target-State từ `draft` sang `approved` khi:

- Objective, trigger, outcome và boundary đã rõ.
- Mandatory requirements có traceability.
- Risks và control objectives có owner.
- Happy path, exception, escalation và contingency đầy đủ.
- SoD, data, security và resilience impacts đã được review.
- Metrics, evidence và governance đã được định nghĩa.
- Option rationale, assumptions, residual risk và dependencies đã được công bố.
- Approver có đúng authority và approval evidence được lưu.
