---
case_id: R120-BEH-001
release_candidate: 1.2.0
execution_mode: independent_fresh_context
executor_relation: independent
status: executed_unreviewed
---

## (1) Nguyên văn response nghiệp vụ hoàn chỉnh

# Dự thảo Target-State: Supplier-Bank-Detail-Change-to-Payment-Release

## Kết luận điều hành

Working recommendation là **Option B — Balanced control and efficiency**, dưới dạng `Target-State / draft / Not reviewed`.

Phương án này phù hợp nhất cho bối cảnh nhiều đơn vị vì tạo một control core chung, giữ local overlay cho từng đơn vị, liên kết trực tiếp thay đổi tài khoản ngân hàng với payment release, và cho phép tự động hóa có chọn lọc sau khi process, data và exception rules được xác nhận.

Đây không phải:

- kết luận compliance;
- mô tả current state;
- xác nhận control hiện hữu hoặc operating effectiveness;
- RCM đã được phê duyệt;
- risk rating hoặc key-control designation chính thức.

Jurisdiction, mandatory baseline, official roles, authority matrix, systems, thresholds, owner, deadline, risk methodology và operating evidence đều là `Not provided` hoặc `To be validated`.

## Intake và source status

| Thuộc tính | Trạng thái |
|---|---|
| Mode | `target-state-design`, `risk-control-analysis`, `rcm`, có SoD/dependency design challenge |
| Process | Supplier-Bank-Detail-Change-to-Payment-Release |
| Organization scope | Nhiều đơn vị; entity/site cụ thể `Not provided` |
| Analysis layer | `Target-State`; ba lớp current state chưa có căn cứ |
| Process level | `To be validated` |
| Jurisdiction | `Not provided` |
| Mandatory baseline | `Not provided`; chưa đủ điều kiện gọi phương án nào là “compliant” |
| Risk appetite/methodology | `Not provided`; không chấm risk score |
| Current controls | `Not provided`; không được hiểu là controls không tồn tại |
| Operating evidence | `Not provided`; operating effectiveness `Not assessed` |
| Data classification | `To be validated`; least privilege và masking là design proposal |
| Review status | `Not reviewed`; cần human approval trước khi ban hành hoặc triển khai |
| Confidence | Facts về input: dựa trên brief; applicability của design: `Low / Inferred` |

Source register:

- `SRC-001` — Brief của người dùng: hỗ trợ tên process, bối cảnh greenfield, multi-entity và danh sách thông tin chưa được cung cấp.
- `SRC-002` — Analyst Target-State proposal: hỗ trợ các risk/control/options dưới đây; không phải external authority, mandatory baseline hay evidence vận hành.
- SOP, policy, authority matrix, current-state workflow, system configuration, transaction data, logs, contracts và nguồn pháp lý: `Not provided`.

Không có dữ kiện thiếu nào chặn việc lập proposal có điều kiện; chúng chặn kết luận current-state, compliance, control gap, key-control status và operating effectiveness.

## R01 — Objective, boundary và E2E mapping

### Business objectives dự thảo

| ID | Objective |
|---|---|
| `OBJ-001` | Chỉ yêu cầu thay đổi bank details có tính xác thực và được phép mới được xử lý. |
| `OBJ-002` | Payment release sử dụng đúng beneficiary, bank details và dữ liệu giao dịch đã được phép. |
| `OBJ-003` | Mọi quyết định, thay đổi, exception và release đều truy nguyên được; dữ liệu nhạy cảm được bảo vệ. |
| `OBJ-004` | Quy trình vận hành nhất quán giữa các đơn vị, không lan truyền thay đổi sai scope và không tạo gián đoạn không kiểm soát. |

Các objective này là đề xuất, chưa phải objective chính thức của doanh nghiệp.

### Boundary dự thảo

- `process_id`: `E2E-001`
- `process_name`: Supplier-Bank-Detail-Change-to-Payment-Release
- `trigger`: một yêu cầu thay đổi bank details của supplier được tiếp nhận.
- `start boundary`: thời điểm tổ chức nhận và ghi nhận yêu cầu gốc.
- `end boundary`: payment bị ảnh hưởng được release hợp lệ, hoặc bị block/reject với lý do và decision trail được lưu.
- `in scope`:
  - tiếp nhận và xác thực yêu cầu;
  - xác minh beneficiary/bank details;
  - xác định supplier và entity scope;
  - ghi nhận, phê duyệt và kích hoạt thay đổi;
  - nhận diện payment bị ảnh hưởng;
  - authorization và payment release;
  - exception, override, audit trail, access, monitoring và controlled handoff.
- `out of scope`, trừ khi được mở rộng:
  - supplier due diligence/onboarding đầy đủ;
  - xác nhận tính hợp lệ của invoice ngoài dependency cần cho release;
  - settlement và bank reconciliation hoàn chỉnh sau release;
  - legal/compliance opinion;
  - operating-effectiveness testing.

### Open-world mapping

Không có một seed family duy nhất bao phủ chính xác boundary này. Mapping dự thảo là:

| Mapping ID | Candidate relationship | Fit status |
|---|---|---|
| `MAP-001` | Supplier-Onboarding-to-Offboarding — phần supplier master-data change | `candidate_overlap` |
| `MAP-002` | Invoice-to-Payment — phần bank-change check và payment release | `candidate_overlap` |
| `MAP-003` | Procure-to-Pay — broader context | `supporting_context` |

Đây là organization-specific cross-E2E design; không có external reference ID hoặc official taxonomy ID được gán.

### Step register dự thảo

Mọi performer, reviewer, approver, system, SLA và evidence-retention period đều `To be validated`.

| Step ID | Target-State activity | Main decision/exception |
|---|---|---|
| `STEP-001` | Nhận yêu cầu, cấp case reference và giữ nguyên request/source gốc | Yêu cầu thiếu, trùng hoặc không xác định được supplier → exception |
| `STEP-002` | Xác thực requestor và supplier bằng nguồn/kênh tin cậy độc lập | Không xác thực được → không tiếp tục thay đổi |
| `STEP-003` | Xác minh beneficiary và bank details theo phương pháp được phê duyệt | Kết quả không nhất quán hoặc không đủ evidence → exception |
| `STEP-004` | Xác định supplier record, entity scope, effective scope, bất thường và các payment bị ảnh hưởng | Cross-entity conflict, repeated change, shared account hoặc pending payment → enhanced review theo rule chưa xác định |
| `STEP-005` | Ghi proposed change, giữ old/new values và submission snapshot | Không cho phép record chưa duyệt tự trở thành active |
| `STEP-006` | Independent approval và controlled activation | Reject, return hoặc activate; decision trail bắt buộc |
| `STEP-007` | Liên kết payment bị ảnh hưởng với bank-change case và tái xác minh trước release | Không đạt approved gate → block/exception |
| `STEP-008` | Independent payment authorization và release trên approved data snapshot | Data thay đổi hoặc integrity check không đạt → revalidation/reapproval |
| `STEP-009` | Ghi kết quả release/rejection, đóng hoặc chuyển exception và handoff sang downstream monitoring/reconciliation | Exception chưa đóng không được coi là hoàn tất |

Happy path, exception path, emergency path, bulk-change path, offline/manual fallback và cross-entity propagation rule đều cần được phê duyệt trước go-live.

## R02 — Risk analysis

Mọi risk dưới đây là `Target-State design hypothesis`, không phải incident hoặc current deficiency. `risk owner: To be validated`; inherent/residual rating: `Not assessed`.

| Risk ID | Cause → Event → Impact → Objective | Linked steps |
|---|---|---|
| `RSK-001` | Do yêu cầu hoặc contact details có thể đến từ kênh bị giả mạo và không được xác thực độc lập, một bank-change request không hợp lệ có thể được chấp nhận, dẫn đến payment cho beneficiary ngoài ý định hoặc khó thu hồi, ảnh hưởng `OBJ-001`, `OBJ-002`. | `STEP-001`–`003` |
| `RSK-002` | Do dữ liệu thiếu/sai hoặc account ownership không được xác minh đủ, bank details không hợp lệ có thể được kích hoạt, dẫn đến misdirected, failed hoặc delayed payment và supplier dispute, ảnh hưởng `OBJ-002`, `OBJ-004`. | `STEP-003`–`006` |
| `RSK-003` | Do supplier record dùng chung và entity scope/effective date không rõ, một thay đổi hợp lệ cho một đơn vị có thể bị áp dụng sai hoặc không nhất quán ở đơn vị khác, dẫn đến payment và master data sai, ảnh hưởng `OBJ-002`, `OBJ-004`. | `STEP-004`–`006` |
| `RSK-004` | Do incompatible duties hoặc effective access không được tách, một identity có thể tạo, phê duyệt bank change và/hoặc chuẩn bị, release payment rồi che giấu hành vi, dẫn đến unauthorized payment hoặc override, ảnh hưởng `OBJ-001`–`003`. | `STEP-005`–`008` |
| `RSK-005` | Do bank-change case không được liên kết với pending/first affected payment, payment có thể được release bằng dữ liệu cũ hoặc dữ liệu mới chưa tái xác minh trong khoảng chuyển đổi, dẫn đến payment sai, trùng hoặc trễ, ảnh hưởng `OBJ-002`, `OBJ-004`. | `STEP-004`, `007`, `008` |
| `RSK-006` | Do thay đổi trái phép hoặc interface failure giữa approval và release, beneficiary, account hoặc transaction instruction được release có thể khác approved snapshot, dẫn đến unauthorized hoặc inaccurate payment, ảnh hưởng `OBJ-002`, `OBJ-003`. | `STEP-007`, `008` |
| `RSK-007` | Do emergency, bulk, offline hoặc manual exception có thể bypass normal checks, thay đổi hoặc payment chưa được xác minh có thể được thực hiện, dẫn đến fraud, error hoặc unresolved exposure, ảnh hưởng `OBJ-001`–`003`. | Toàn bộ flow |
| `RSK-008` | Do audit trail, monitoring hoặc retention không đầy đủ, unauthorized change, exception hoặc release anomaly có thể không được phát hiện, điều tra hoặc xử lý, ảnh hưởng khả năng recovery và governance theo `OBJ-003`. | `STEP-001`, `006`, `009` |
| `RSK-009` | Do phụ thuộc vào system, trusted-contact data, validation capability, knowledge hoặc một resource chung chưa có fallback đủ, quy trình có thể bị trì hoãn hoặc bị bypass khi dependency không sẵn sàng, ảnh hưởng `OBJ-002`, `OBJ-004`. | Toàn bộ flow |
| `RSK-010` | Do access, transmission hoặc retention đối với supplier/bank data không được kiểm soát, dữ liệu có thể bị xem, thay đổi hoặc tiết lộ không phù hợp, gây security, privacy, operational hoặc reputational impact; legal impact cần xác minh theo jurisdiction, ảnh hưởng `OBJ-003`. | Toàn bộ flow |

## R03 — Expected/key controls có căn cứ

### Giới hạn baseline

Không có source-derived expected baseline nào đã được xác minh. Các controls dưới đây là **analyst design proposals**, truy nguyên từ risk và control objective; không được gọi là mandatory, compliant hoặc standard-derived.

### Control objectives

| ID | Control objective |
|---|---|
| `COBJ-001` | Authenticity, authority và scope của change request được xác lập độc lập trước khi thay đổi master data. |
| `COBJ-002` | Beneficiary và bank details được xác minh là hợp lệ cho supplier dự kiến. |
| `COBJ-003` | Old/new values, supplier identity, entity scope, version và effective state chính xác, đầy đủ, truy nguyên được. |
| `COBJ-004` | Incompatible duties/access không cho phép một identity tự tạo, tự phê duyệt và tự release; nếu không thể tách hoàn toàn phải có mitigation độc lập được phê duyệt. |
| `COBJ-005` | Mọi payment bị ảnh hưởng bởi bank change được nhận diện và phải qua approved gate trước release. |
| `COBJ-006` | Payment instruction được release khớp approved snapshot và được bảo vệ khỏi thay đổi trái phép. |
| `COBJ-007` | Exception, emergency, override, bulk và manual path được cho phép, giới hạn, ghi log, review và đóng có kiểm soát. |
| `COBJ-008` | Case lifecycle, decisions, evidence và anomalies được ghi nhận, truy xuất và theo dõi đầy đủ. |
| `COBJ-009` | Process có authorized fallback, backup và recovery arrangement đủ dùng theo tolerance được phê duyệt. |
| `COBJ-010` | Confidentiality, integrity, access và retention của supplier/bank data được kiểm soát theo basis đã được phê duyệt. |

### Target-State control register

Mỗi logical control có một observation dự thảo tương ứng `OBS-TGT-nnn`, `analysis_layer: Target-State`. Actual evidence IDs vẫn rỗng. Owner, performer, approver, system, detailed frequency, threshold, retention và escalation timeframe đều `To be validated`.

| Control / observation | Risks / objectives | Design proposal | Keyness status | Proposed evidence và test attribute |
|---|---|---|---|---|
| `CTL-001` / `OBS-TGT-001` | `RSK-001`, `RSK-008`; `COBJ-001`, `008` | Controlled intake với unique case reference; lưu request gốc, channel, supplier/entity scope, old/new data và attachments | Supporting candidate; `To be validated` | Case record đầy đủ, request gốc còn nguyên, duplicate/incomplete case có disposition |
| `CTL-002` / `OBS-TGT-002` | `RSK-001`; `COBJ-001` | Xác thực request qua trusted contact/channel tồn tại độc lập trước request; không dùng chính contact details mới làm nguồn duy nhất | Candidate key; `To be validated` | Evidence chứng minh nguồn contact, người thực hiện duty độc lập, thời điểm, kết quả và exception |
| `CTL-003` / `OBS-TGT-003` | `RSK-001`, `RSK-002`; `COBJ-002` | Xác minh beneficiary/account ownership bằng phương pháp và criteria được phê duyệt, tách khỏi nguồn request khi phù hợp | Candidate key; `To be validated` | Validation record nêu method, source, result, reviewer/challenge và exception disposition |
| `CTL-004` / `OBS-TGT-004` | `RSK-002`, `RSK-003`; `COBJ-002`, `003` | Kiểm tra format/completeness, supplier identity, duplicate/shared account, repeated change, inactive record và cross-entity impact theo approved criteria | Supporting candidate | Check output bao phủ relevant population và có documented disposition |
| `CTL-005` / `OBS-TGT-005` | `RSK-003`, `RSK-004`; `COBJ-003`, `004` | Maker-checker cho proposed bank change; distinct effective identities và không self-approval | Candidate key; `To be validated` | Workflow/access evidence cho thấy sequence, distinct identities, scope và decision |
| `CTL-006` / `OBS-TGT-006` | `RSK-002`, `RSK-003`, `RSK-008`; `COBJ-003`, `008` | Controlled activation, versioning và tamper-evident audit trail với old/new values, entity scope và effective state | Supporting candidate | Master-data log tie-out với case và approval; unauthorized alteration được ngăn hoặc phát hiện |
| `CTL-007` / `OBS-TGT-007` | `RSK-005`; `COBJ-005` | Nhận diện affected payments và áp dụng release gate/revalidation; holding hoặc escalation criteria cần phê duyệt | Candidate key; `To be validated` | Payment-to-change linkage, gate result và evidence không release trước khi condition được đáp ứng |
| `CTL-008` / `OBS-TGT-008` | `RSK-004`–`006`; `COBJ-004`, `006` | Payment authorization/release độc lập với bank-change entry và payment preparation; kiểm tra approved beneficiary/data snapshot | Candidate key; `To be validated` | Release record chứng minh independence, approved snapshot match và decision |
| `CTL-009` / `OBS-TGT-009` | `RSK-005`, `RSK-006`; `COBJ-006` | Bảo vệ integrity từ approval đến release; thay đổi dữ liệu sau approval phải gây block hoặc revalidation/reapproval | Candidate key; `To be validated` | Interface/instruction audit trail và evidence xử lý post-approval change |
| `CTL-010` / `OBS-TGT-010` | `RSK-007`, `RSK-009`; `COBJ-007` | Exception/override/emergency/bulk/manual path có reason, authorization, scoped access, logging, independent post-review và closure | Supporting/compensating candidate | Exception record đầy đủ; temporary access có expiry khi áp dụng; post-review và closure có evidence |
| `CTL-011` / `OBS-TGT-011` | `RSK-007`, `RSK-008`; `COBJ-008` | Monitoring change-to-payment population và anomalies, gồm unresolved exceptions, repeated changes, shared accounts, rejected/returned payments và overrides | Monitoring candidate | Population completeness/data lineage, review evidence, investigation và closure; criteria/frequency `To be validated` |
| `CTL-012` / `OBS-TGT-012` | `RSK-004`, `RSK-010`; `COBJ-004`, `008`, `010` | Least privilege, controlled provisioning/change/revocation và independent review của privileged activity | Supporting candidate; keyness depends on system design | Effective-access map, privileged logs, review evidence và exception follow-up |
| `CTL-013` / `OBS-TGT-013` | `RSK-009`; `COBJ-009` | Authorized backup và controlled fallback; manual workaround phải có capacity, approvals, evidence, reconciliation và test status | Supporting/compensating candidate | Backup authority/access, fallback test hoặc walkthrough, transaction reconciliation sau restoration |
| `CTL-014` / `OBS-TGT-014` | `RSK-010`; `COBJ-010` | Access restriction, secure transfer, masking và retention/disposal theo approved classification và applicable baseline | Supporting candidate | Access/transfer/retention evidence; period và legal basis `To be validated` |

“Candidate key” chỉ là điểm cần governance challenge. Không thể chốt key-control status khi chưa có significant-risk methodology, risk appetite, alternative-control assessment và organizational approval.

### SoD design challenge

Chưa có role matrix, entitlements hoặc actual-user evidence. Vì vậy chỉ có thể nhận diện design conflicts `Potential`:

| Potential incompatible activities | Status | Candidate mitigation |
|---|---|---|
| Tiếp nhận/ghi change và tự xác thực request | `Potential` | `CTL-002` với duty độc lập |
| Nhập bank change và tự approve/activate | `Potential` | `CTL-005` |
| Thay đổi bank details và release payment bị ảnh hưởng | `Potential` | `CTL-005`, `CTL-007`, `CTL-008` |
| Chuẩn bị payment và release cùng payment | `Potential` | `CTL-008` |
| Quản trị access và review privileged logs | `Potential` | `CTL-012` |

System-level và actual-user conflicts: `Not assessed`. Không có căn cứ kết luận actual conflict hoặc conflict exercised.

### Dependency/SPOF challenge

| Dependency ID | Candidate dependency | Unresolved fields |
|---|---|---|
| `DEP-001` | Trusted supplier-contact registry hoặc independent channel | Provider, completeness, access, fallback |
| `DEP-002` | Supplier master, unique identity và entity mapping | Data owner, quality, synchronization, propagation rules |
| `DEP-003` | Workflow, identity/access và audit logging | System/configuration, availability, privileged access |
| `DEP-004` | Payment platform, interface và bank release channel | Integrity controls, outage tolerance, recovery capability |
| `DEP-005` | Beneficiary/account validation capability hoặc provider | Applicability, coverage, reliability, fourth-party dependency |
| `DEP-006` | Authorized knowledge/backup và manual fallback | Authority, capacity, cross-training, test evidence |

`spof_status` cho mọi dependency là `To be validated`. Nhiều providers hoặc nhiều người không tự loại trừ common-mode failure.

## R04 — Current controls theo mức bằng chứng

| Layer | Available observations | Kết luận được phép |
|---|---|---|
| `As-Documented` | Không có SOP hoặc document được cung cấp | Không thể mô tả documented controls; không suy controls không tồn tại |
| `As-Designed` | Current design `Not provided` | Không thể đánh giá design adequacy hiện tại |
| `As-Performed` | Operating evidence `Not provided` | Không thể đánh giá operation hoặc operating effectiveness |
| `Target-State` | `OBS-TGT-001`–`014` | Chỉ là design proposal; chưa triển khai hoặc phê duyệt |

- `current control observation IDs`: `[]`
- `performed observation IDs`: `[]`
- `assessment_status`: `Not assessed`
- `evidence_status`: `Not checked`
- sample size/population/testing result: `Not provided`
- formal operating-effectiveness conclusion: không được đưa ra.

## R05 — Gaps và design opportunities

Không có đủ current baseline để xác nhận `Missing Control`, `Weak Design`, `Operating Deviation` hay `Compliance Gap`.

- `gap_ids`: `[]`
- `CMP-001.coverage_assessment`: `Not assessed`
- `CMP-001.current observation IDs`: `[]`
- `CMP-001.target observation IDs`: `OBS-TGT-001`–`014`
- mandatory baseline links: `[]`

Các thiếu hụt về source/evidence là limitations, không phải bằng chứng control absence hoặc failure.

### Design opportunity register

| ID | Design opportunity | Linked controls |
|---|---|---|
| `OPP-001` | Thiết lập global control core và entity-specific overlay, với supplier/entity scope rõ ràng | `CTL-001`, `004`, `006`, `011`, `014` |
| `OPP-002` | Tách request authentication khỏi beneficiary/account validation và dùng nguồn độc lập | `CTL-002`, `003` |
| `OPP-003` | Liên kết bank-change case trực tiếp với affected-payment gate và release integrity | `CTL-007`–`009` |
| `OPP-004` | Thiết kế process-role SoD, effective-access rules và privileged monitoring cùng lúc | `CTL-005`, `008`, `012` |
| `OPP-005` | Chuẩn hóa exception, override, audit trail, monitoring và closure | `CTL-010`, `011`, `014` |
| `OPP-006` | Thiết kế resilience, authorized fallback và common-mode dependency challenge | `CTL-013` |

Thông tin còn thiếu cần xác minh:

- danh sách entity/site/country, payment corridor và nơi bank account được duy trì;
- official objective, scope và authority model;
- jurisdiction, contracts, adopted policies/standards và mandatory requirements;
- supplier master architecture, entity-sharing và unique supplier logic;
- workflow, ERP/master-data, IAM, payment platform, interfaces và logs;
- trusted-contact source và các validation methods được phép;
- transaction volume, variation, seasonality, pending-payment behavior;
- risk appetite, risk-rating methodology và key-control criteria;
- exception, emergency, bulk-change và manual/offline scenarios;
- thresholds, escalation criteria, service levels và metric definitions;
- data classification, privacy/security basis và retention requirements;
- current activities, controls, access assignments, incidents và evidence nếu có.

## R06 — Ba phương án và working recommendation

### So sánh options

| Tiêu chí | Option A — Minimum-control proposal, compliance unverified | Option B — Balanced control and efficiency | Option C — Automation-first; leading-practice claim unverified |
|---|---|---|---|
| Core design | Controlled manual intake, independent verification, maker-checker, affected-payment revalidation, release approval và case evidence | Standard multi-entity workflow, common data/control core, local overlays, integrated change-to-payment gate, selective automation và monitoring | Authenticated supplier portal, integrated validation service, rules engine, automated gates, continuous monitoring |
| Benefit | Ít technology change hơn; có thể tạo minimum control discipline tương đối nhanh | Cân bằng fraud/error prevention, traceability, scalability và practical implementation | Consistency và scale cao hơn khi data/process đã trưởng thành |
| Main trade-off | Manual burden, inconsistent execution, slower cycle, people dependency, weaker cross-entity visibility | Cần process/data standardization, integration, access design và change governance | Cost/complexity cao; phụ thuộc data quality, interfaces, third parties và cyber/privacy controls |
| Relative cost | Thấp hơn; không lượng hóa | Trung bình; không lượng hóa | Cao hơn; không lượng hóa |
| Complexity | Thấp–trung bình | Trung bình | Cao |
| Technology dependency | Thấp hơn nhưng vẫn cần controlled records/access | Workflow, master data, IAM, payment interface và reporting | Portal/API, rules, event monitoring và resilient integrations |
| People impact | Manual workload và judgment cao | Role/duty redesign, training và exception management có kiểm soát | Change impact lớn; cần skills quản trị automation/data/vendor |
| Relative implementation time | Ngắn hơn, không phải deadline | Trung gian, không phải deadline | Dài hơn, không phải deadline |
| Residual exposure | Tương đối cao hơn do manual variation; không chấm điểm | Thấp hơn Option A nếu design và integrations được xác nhận; không chấm điểm | Có thể thấp hơn cho standardized happy path nhưng tạo technology/common-mode risks mới |
| Critical dependencies | Trusted contacts, independent duties, evidence repository, local baseline | Approved common model, local overlays, data quality, IAM, workflow/payment integration, fallback | Stable rules, mature data, strong change/access controls, provider resilience và validated business case |

### Working recommendation: `REC-001`

Chọn **Option B — Balanced control and efficiency** làm working recommendation, với confidence `Low` do thiếu operating context.

Rationale:

- quy trình cắt ngang supplier master và payment release nên manual controls rời rạc của Option A dễ tạo inconsistent cross-entity coverage;
- Option B cho phép một canonical case và control set truy nguyên từ request đến release;
- có thể giữ independent human challenge tại authentication, exception và release trong khi tự động hóa routing, linkage, audit trail và monitoring;
- tránh phụ thuộc sớm vào data/integration maturity mà Option C cần;
- tạo nền để chuyển từng component sang automation sau khi process, data và exception rules ổn định.

Điều kiện trước khi phê duyệt hoặc triển khai:

1. Xác nhận boundary, entity scope và official objective.
2. Xác minh jurisdiction và mandatory/advisory baseline theo từng entity; cập nhật local overlays.
3. Phê duyệt duty model, decision rights, SoD và effective-access design.
4. Chốt validation methods, exception criteria, thresholds, escalation, service levels và retention basis.
5. Xác nhận system/data architecture, interface integrity, audit-log capability và fallback.
6. Walkthrough happy path, negative cases, cross-entity cases, emergency/bulk/manual paths và recovery scenarios.
7. Thực hiện design testing và user/access/configuration validation trước production.
8. Có human approval có thẩm quyền trước khi phát hành SOP, RCM, access hoặc workflow production.

Phased design sequence, không phải roadmap có deadline:

- `Foundation`: chốt scope, baseline, data model, duty/authority model và minimum control objectives.
- `Controlled workflow`: triển khai common case, validation, approval, payment gate, audit trail và exception lifecycle.
- `Selective automation`: tự động hóa stable rules/integrations sau data-quality và control validation.
- `Monitoring`: bổ sung KPI/KRI/KCI và evidence-based tuning.

Candidate metrics, chưa có threshold, frequency hoặc metric owner:

- KPI: complete-request-to-activation cycle time; affected-payment hold-resolution time; first-time-valid request rate.
- KRI: repeated bank changes; accounts shared across suppliers; override/emergency usage; rejected/returned payment; payment linked to recent change theo window `To be validated`.
- KCI: tỷ lệ case có independent authentication; tỷ lệ có beneficiary validation; tỷ lệ affected payment qua release gate; SoD/access exceptions; audit-trail completeness; exception closure.

## R07 — Design/no-change hypothesis

### `NCS-001`

- `scenario_basis`: `Design hypothesis`
- linked risks: `RSK-001`–`010`
- linked design opportunities: `OPP-001`–`006`
- existing protection: `Not provided`
- existing logical control IDs: `[]`
- existing control observation IDs: `[]`
- evidence status: `Not checked`
- horizon: `null`
- probability/loss/risk score: `Not assessed`

Causal scenario:

> Nếu doanh nghiệp đưa quy trình multi-entity vào vận hành mà không thiết lập một minimum authenticated, independently approved và traceable change-to-payment design, một yêu cầu giả mạo, dữ liệu sai, cross-entity propagation, incompatible access hoặc uncontrolled exception có thể được sử dụng trong payment release; hậu quả có thể gồm payment sai beneficiary, khó thu hồi, supplier dispute, delayed payment, inaccurate records, investigation difficulty, data exposure và governance failure.

Đây không phải xác nhận current deficiency hoặc incident. Current protections có thể tồn tại nhưng chưa được cung cấp.

Uncertainty và validation cần thiết:

- inventory current activities/controls theo từng entity;
- user-role/effective-access và configuration evidence;
- bank-change và affected-payment population;
- exception, override, rejected/returned-payment và incident history;
- trusted-contact/data lineage;
- system/interface/audit-log coverage;
- jurisdiction, contract và adopted internal baseline;
- dependency capacity, fallback và recovery testing.

## RCM skeleton truy nguyên

Grain dưới đây là **một row cho mỗi Risk–Control association**. Logical `control_id` tách khỏi `control_observation_id`. Mọi observation là `Target-State`; current observations, requirement IDs, baseline links, evidence IDs và gap IDs đều rỗng. Tất cả rows liên kết `REC-001`, source `SRC-001` và `SRC-002`, review status `Not reviewed`.

| RCM ID | Step ID | Risk ID | Control-objective ID | Control / observation | Design-opportunity link |
|---|---|---|---|---|---|
| `RCM-001` | `STEP-001` | `RSK-001` | `COBJ-001` | `CTL-001` / `OBS-TGT-001` | `OPP-001` |
| `RCM-002` | `STEP-002` | `RSK-001` | `COBJ-001` | `CTL-002` / `OBS-TGT-002` | `OPP-002` |
| `RCM-003` | `STEP-003` | `RSK-001` | `COBJ-002` | `CTL-003` / `OBS-TGT-003` | `OPP-002` |
| `RCM-004` | `STEP-003` | `RSK-002` | `COBJ-002` | `CTL-003` / `OBS-TGT-003` | `OPP-002` |
| `RCM-005` | `STEP-004` | `RSK-002` | `COBJ-002`, `003` | `CTL-004` / `OBS-TGT-004` | `OPP-001` |
| `RCM-006` | `STEP-006` | `RSK-002` | `COBJ-003` | `CTL-006` / `OBS-TGT-006` | `OPP-001` |
| `RCM-007` | `STEP-004` | `RSK-003` | `COBJ-003` | `CTL-004` / `OBS-TGT-004` | `OPP-001` |
| `RCM-008` | `STEP-005`, `006` | `RSK-003` | `COBJ-003`, `004` | `CTL-005` / `OBS-TGT-005` | `OPP-004` |
| `RCM-009` | `STEP-006` | `RSK-003` | `COBJ-003` | `CTL-006` / `OBS-TGT-006` | `OPP-001` |
| `RCM-010` | `STEP-005`, `006` | `RSK-004` | `COBJ-004` | `CTL-005` / `OBS-TGT-005` | `OPP-004` |
| `RCM-011` | `STEP-008` | `RSK-004` | `COBJ-004` | `CTL-008` / `OBS-TGT-008` | `OPP-004` |
| `RCM-012` | `STEP-005`–`008` | `RSK-004` | `COBJ-004` | `CTL-012` / `OBS-TGT-012` | `OPP-004` |
| `RCM-013` | `STEP-004`, `007` | `RSK-005` | `COBJ-005` | `CTL-007` / `OBS-TGT-007` | `OPP-003` |
| `RCM-014` | `STEP-008` | `RSK-005` | `COBJ-006` | `CTL-008` / `OBS-TGT-008` | `OPP-003` |
| `RCM-015` | `STEP-008` | `RSK-006` | `COBJ-006` | `CTL-008` / `OBS-TGT-008` | `OPP-003` |
| `RCM-016` | `STEP-007`, `008` | `RSK-006` | `COBJ-006` | `CTL-009` / `OBS-TGT-009` | `OPP-003` |
| `RCM-017` | `STEP-001`–`009` | `RSK-007` | `COBJ-007` | `CTL-010` / `OBS-TGT-010` | `OPP-005` |
| `RCM-018` | `STEP-009` | `RSK-007` | `COBJ-008` | `CTL-011` / `OBS-TGT-011` | `OPP-005` |
| `RCM-019` | `STEP-001` | `RSK-008` | `COBJ-008` | `CTL-001` / `OBS-TGT-001` | `OPP-001` |
| `RCM-020` | `STEP-006` | `RSK-008` | `COBJ-008` | `CTL-006` / `OBS-TGT-006` | `OPP-001` |
| `RCM-021` | `STEP-009` | `RSK-008` | `COBJ-008` | `CTL-011` / `OBS-TGT-011` | `OPP-005` |
| `RCM-022` | `STEP-001`–`009` | `RSK-009` | `COBJ-009` | `CTL-013` / `OBS-TGT-013` | `OPP-006` |
| `RCM-023` | `STEP-001`–`009` | `RSK-009` | `COBJ-007` | `CTL-010` / `OBS-TGT-010` | `OPP-005` |
| `RCM-024` | `STEP-001`–`009` | `RSK-010` | `COBJ-010` | `CTL-012` / `OBS-TGT-012` | `OPP-004` |
| `RCM-025` | `STEP-001`–`009` | `RSK-010` | `COBJ-010` | `CTL-014` / `OBS-TGT-014` | `OPP-005` |

RCM-wide nulls và limitations:

- `requirement_ids: []`
- `baseline_link_ids: []`
- `documented_observation_ids: []`
- `designed_current_observation_ids: []`
- `performed_observation_ids: []`
- `evidence_ids: []`
- `gap_ids: []`
- `assessed_period: Not applicable — draft Target-State`
- `risk rating / residual risk: Not assessed`
- `control owner / action owner / deadline: To be validated`
- `mandatory_or_advisory: Not assessed`
- `review_status: Not reviewed`

## QA và approval gates

QA status của draft:

- objective, trigger và boundaries đã được nêu dưới nhãn đề xuất;
- các step không được trình bày như current state;
- risks dùng Cause → Event → Impact → Objective;
- controls liên kết risk và control objective;
- logical controls tách khỏi Target-State observations;
- quan hệ nhiều-nhiều được giữ trong RCM;
- potential SoD không bị nâng thành actual conflict;
- unique/shared dependency không bị kết luận là SPOF;
- không tạo current controls, fake gaps, compliance claims hoặc operating-effectiveness conclusion;
- không bịa role chính thức, threshold, score, owner, sample size, deadline hoặc loss;
- R07 được giữ dưới nhãn `Design hypothesis`.

Human approval có thẩm quyền là bắt buộc trước khi:

- chốt process boundary và official objectives;
- ban hành SOP/RCM;
- gán duties, authority hoặc access;
- áp dụng local mandatory baseline;
- quyết định thresholds, exception rules, metrics và retention;
- cấu hình hoặc thay đổi production workflow;
- chấp nhận residual exposure;
- chuyển control từ manual sang automated;
- sử dụng kết quả test để kết luận operating effectiveness.

---

## (2) Tự kê khai file đã đọc và giới hạn môi trường

Tôi đã đọc đầy đủ `skills/thien-skill-risk-control-process/SKILL.md`; các reference được SKILL định tuyến cho case này gồm `architecture-layers-taxonomy.md`, `risk-control-key-control.md`, `gaps-rationalization-rcm.md`, `sod-spof-dependencies.md`, `target-state-and-improvement.md`, `data-model-qa-execution.md`; trong `end-to-end-process-profiles.md` chỉ đọc mục lục/legend và đúng nhóm **C. Procurement và Supplier**. Tôi cũng đọc các template cần trực tiếp cho deliverable: `process-intake.yaml`, `process-architecture-step-register.yaml`, `control-register.yaml`, `control-baseline-comparison.yaml`, `rcm.yaml`, `target-state-options.yaml` và `qa-checklist.yaml`.

Tôi chỉ dùng thao tác đọc cục bộ (`sed`, `wc`, `rg` để định vị mục); không đọc git diff/history, `docs/HANDOFF.md`, lịch sử test, prior outputs/reviews hay nguồn web; không sửa hoặc tạo file/artifact. Do không có nguồn doanh nghiệp, operating evidence, system access hoặc nguồn chính thức theo jurisdiction, response chỉ có thể là Target-State proposal có điều kiện, không xác minh compliance, configuration hay operating effectiveness.
