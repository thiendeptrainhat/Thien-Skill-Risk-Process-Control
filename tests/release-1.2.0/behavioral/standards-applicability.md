---
case_id: R120-BEH-003
release_candidate: 1.2.0
execution_mode: independent_fresh_context
executor_relation: independent
status: executed_unreviewed
---

## (1) Nguyên văn response nghiệp vụ

### Kết luận điều hành

Với thông tin hiện có, chưa thể kết luận quy trình ERP “compliant” hoặc “non-compliant” với NIST/COBIT, và cũng chưa thể xác nhận operating issue hay control failure.

Điều có thể kết luận là mô tả qua chat hiện quá thiếu để:

- xác định đầy đủ control design;
- kiểm tra control;
- đối chiếu với một compliance baseline;
- đánh giá cách control thực tế vận hành.

Các nhận định dưới đây vì vậy là đánh giá giới hạn về tính đầy đủ/testability của mô tả, candidate risk scenarios và đề xuất Target-State; không phải compliance opinion, audit finding hay operating-effectiveness conclusion.

### Phạm vi và căn cứ

- Business objective tạm xác định: chỉ cấp đúng quyền ERP cần thiết cho đúng người có thẩm quyền, kịp thời, có thể truy nguyên và quản lý xuyên suốt vòng đời quyền truy cập. Objective này cần Process Owner xác nhận.
- Boundary hiện được mô tả: trưởng bộ phận gửi email → IT tạo account.
- Nguồn: management representation qua chat.
- `As-Designed`: chỉ là current-state hypothesis cần xác minh.
- `As-Performed`: `Not assessed`.
- Confidence: trung bình đối với việc tái hiện đúng nội dung chat; thấp đối với thiết kế đầy đủ và cách quy trình thực tế vận hành.
- Không chấm risk severity, residual risk, key-control status hoặc remediation priority vì chưa có methodology/risk appetite được phê duyệt.

### Current-state hypothesis

| Bước được mô tả | Điều biết được | Điều chưa biết |
|---|---|---|
| Trưởng bộ phận gửi email | Có sự tham gia của trưởng bộ phận và một yêu cầu qua email | Trigger, nội dung bắt buộc, xác thực người gửi, thẩm quyền phê duyệt, role được yêu cầu, business justification, phạm vi dữ liệu, ngày hiệu lực/hết hạn, exception |
| IT tạo account | IT thực hiện provisioning | IT dựa trên tiêu chí nào, quyền nào được cấp, có kiểm tra approval/least privilege/SoD không, cấu hình ERP có chặn sai lệch không, ai xác nhận kết quả, evidence/log nào được lưu |
| Kết thúc | Có thể suy luận account được tạo | Account đã kích hoạt hay chưa, người dùng/owner có xác nhận không, quyền có khớp yêu cầu không, monitoring/review/revocation có thuộc quy trình không |

Email của trưởng bộ phận có thể là một tín hiệu authorization, nhưng chỉ trở thành control có thể đánh giá nếu xác minh được authority, nội dung/criteria, timing, authentication, evidence retention và exception handling. Việc IT tạo account tự nó là activity vận hành, chưa phải control nếu không có bước xác minh hoặc reconciliation rõ ràng.

### Candidate risks và control coverage

| Candidate risk scenario | Control objective cần đạt | Current coverage có thể xác nhận | Phân loại an toàn |
|---|---|---|---|
| Do authority và tiêu chí phê duyệt chưa rõ, quyền có thể được cấp cho người hoặc mục đích không hợp lệ, dẫn đến truy cập trái phép, sai lệch dữ liệu, gian lận hoặc gián đoạn | Chỉ yêu cầu hợp lệ, do đúng authority phê duyệt, mới được provisioning | Chỉ biết trưởng bộ phận gửi email; chưa xác minh email có phải approval hợp lệ | `Unclear/Untestable control description`; candidate design gap |
| Do yêu cầu email tự do và role catalog không được cung cấp, IT có thể hiểu sai hoặc cấp quyền vượt nhu cầu | Quyền được xác định theo approved role/entitlement và least privilege | Không có thông tin về role catalog, request fields hoặc entitlement criteria | Potential weak-design/precision gap; không phải bằng chứng quyền quá mức đã được cấp |
| Do chưa có role/permission map, SoD rule, user assignment hoặc effective-access data, người dùng có thể nhận incompatible permissions | Quyền xung đột được ngăn chặn hoặc có exception/mitigation được phê duyệt | Không đánh giá được ở process-role, system-access hoặc actual-user level | Potential SoD concern; không phải actual SoD conflict |
| Do provisioning thủ công không có reconciliation được mô tả, quyền thực cấp có thể khác quyền được duyệt | Quyền provisioning phải khớp yêu cầu và approval | Chưa có evidence về verification hoặc reconciliation | Candidate design gap; không phải operating deviation |
| Do request, approval và system event chưa được liên kết bằng audit trail, tổ chức có thể không chứng minh được ai đã yêu cầu, duyệt và cấp quyền | Mỗi lần cấp quyền phải traceable và có evidence phù hợp | Log/ticket/evidence không được cung cấp | Evidence limitation và candidate auditability gap; không được kết luận log không tồn tại |
| Do lifecycle, expiry và revocation không nằm trong mô tả, quyền có thể tiếp tục sau khi nhu cầu thay đổi | Quyền phải được thay đổi hoặc thu hồi khi không còn hợp lệ | Không có thông tin về mover, termination, time-bound hoặc periodic review | E2E dependency cần xác minh; chưa phải confirmed missing control |

Không có căn cứ để nói rủi ro hoặc sự cố trên đã thực sự xảy ra.

### Điều gì có thể và không thể gọi là gap/issue

Có thể gọi:

- Mô tả control hiện được cung cấp là không đầy đủ và chưa testable.
- Các thuộc tính như authority, criteria, entitlement, evidence, exception và escalation là `Not provided`.
- Có evidence limitation cho phần `As-Performed`.
- Có candidate/potential design gaps nếu các control bổ sung thực sự không tồn tại.
- Có potential SoD concern cần phân tích tiếp.

Chưa thể gọi:

- `Compliance gap` với NIST hoặc COBIT: chưa có exact source/version, clause/objective, adoption basis, applicable scope, effective period hoặc evidence đối chiếu.
- `Missing Control` trên toàn tổ chức: chỉ có thể nói control đó “không được mô tả trong phạm vi chat đã cung cấp”.
- `Operating deviation`: chưa có approved design/criteria và case evidence cho thấy thực tế khác thiết kế.
- `Control failure` hoặc ineffective operation: chưa có population, testing methodology, configuration, log, sample và executed test.
- `Actual SoD conflict`: chưa có role-to-permission map, user assignment, effective access và scope/kỳ.
- Unauthorized access, fraud, policy breach hoặc non-compliance đã xảy ra.
- Confirmed audit finding, formal compliance opinion hoặc certification conclusion.

Cụm “phải compliant với NIST và COBIT” hiện chỉ là một management direction cần được chuyển thành assessable criteria. Nó không tự xác định edition, scope, clause, mandatory/advisory status hay bằng chứng adoption. Jurisdiction không tự quyết định NIST/COBIT có áp dụng, nhưng cần để xác định luật/quy định liên quan và các nghĩa vụ ràng buộc khác.

### Target-State đề xuất

Đây là analyst proposal dựa trên risk/control logic, chưa phải nội dung được xác minh là do NIST hoặc COBIT yêu cầu:

1. Dùng request/ticket được xác thực, có tối thiểu user, business need, requested role/scope, effective/expiry information và liên kết case ID.
2. Phê duyệt theo approval matrix được ban hành; xác định rõ requester, approving authority và application/role owner khi cần.
3. Đối chiếu với approved role catalog, least-privilege criteria và SoD rules trước khi provisioning.
4. IT chỉ provisioning từ request đã hoàn tất approval; không tự lựa chọn quyền ngoài criteria được duyệt.
5. Thực hiện verification/reconciliation độc lập hoặc system-enforced giữa quyền được duyệt và quyền thực cấp.
6. Liên kết request, approval, provisioning event, exception và completion confirmation thành audit trail có thể truy xuất.
7. Thiết kế riêng emergency/privileged access với approval path, giới hạn thời gian, logging và independent post-review.
8. Mở rộng sang lifecycle dependency: mover, temporary access expiry, termination/revocation và access recertification; frequency/threshold phải được phê duyệt, không tự đặt.
9. Theo dõi các metric candidate như tỷ lệ cấp quyền có approval hợp lệ trước provisioning, tỷ lệ quyền thực cấp khớp quyền duyệt, open exceptions/aging và provisioning cycle time; target chưa được xác định.

Ba mức triển khai:

- Option A — `Minimum-control proposal — compliance unverified`: chuẩn hóa ticket, approval matrix, role catalog, manual SoD/least-privilege check, provisioning evidence và reconciliation. Thay đổi thấp hơn nhưng còn manual burden.
- Option B — Balanced control and efficiency: controlled workflow, approval routing, role/SoD validation, linked provisioning evidence, exception monitoring và lifecycle integration. Đây là lựa chọn tạm ưu tiên nếu volume và system capability phù hợp.
- Option C — Automation-first: IAM/ERP integration, automated provisioning/deprovisioning, preventive rules và continuous monitoring. Chỉ phù hợp sau khi role model, data, exception logic, configuration governance và change control đủ trưởng thành.

Mọi thay đổi authority, SoD, access role hoặc ERP/IAM configuration cần phê duyệt có thẩm quyền trước khi áp dụng.

### Kịch bản nếu giữ nguyên

Nếu giả định không có control nào khác ngoài hai bước được mô tả, việc tiếp tục provisioning từ email tự do có thể dẫn tới quyền không hợp lệ, vượt nhu cầu, không tương thích hoặc không thể truy nguyên; hậu quả có thể gồm sai lệch dữ liệu, gian lận, gián đoạn hoạt động và khó chứng minh fulfillment của nghĩa vụ.

Đây là `design/no-change hypothesis`, không phải bằng chứng về current deficiency hoặc incident. Nếu tổ chức có approval, RBAC, configuration, logging hoặc monitoring chưa được cung cấp, exposure thực tế có thể khác đáng kể.

### Thông tin cần thu thập để hoàn tất đánh giá

1. Exact NIST/COBIT publication, edition/version, clauses/objectives cần áp dụng và official authoritative text được phép sử dụng.
2. Evidence về adoption: policy/board decision, contract, certification scope hoặc authority nội bộ.
3. Entity, jurisdiction, ERP environment, user population, business units, privilege types và kỳ đánh giá.
4. Access policy/SOP, approval matrix/delegation, role catalog, SoD rules, emergency-access và lifecycle rules.
5. ERP/IAM workflow, role/permission mapping, preventive configuration, audit-log configuration và change history.
6. Population đầy đủ của access requests và accounts được tạo trong kỳ; ticket/email/approval/log tương ứng.
7. Data-reliability work và approved testing methodology. Sau đó mới thiết kế sample hoặc full-population testing; chưa đủ căn cứ để tự đặt sample size.

Kết quả hiện tại có review status `Draft/To be validated`; không được sử dụng như formal compliance conclusion hoặc operating-effectiveness assessment.

## (2) Self-disclosure

Đã đọc đầy đủ:

- `skills/thien-skill-risk-control-process/SKILL.md`
- `references/document-analysis-and-discovery.md`
- `references/risk-control-key-control.md`
- `references/gaps-rationalization-rcm.md`
- `references/sod-spof-dependencies.md`
- `references/target-state-and-improvement.md`
- `references/standards-sources-applicability.md`
- `references/data-model-qa-execution.md`
- `templates/qa-checklist.yaml`

Không dùng nguồn ngoài, không duyệt web, không đọc nội dung NIST/COBIT, prior output, review, diff, release note hay test history. Vì vậy mọi control pattern nêu trên là analyst proposal, không phải standard-derived mapping. Không tạo hoặc sửa artifact/file.
