# Segregation of Duties, Single Point of Failure và dependency

## Mục lục

1. [Mục đích và nguyên tắc](#1-mục-đích-và-nguyên-tắc)
2. [Phân tích SoD ở ba cấp](#2-phân-tích-sod-ở-ba-cấp)
3. [Xác định potential và actual conflict](#3-xác-định-potential-và-actual-conflict)
4. [Áp dụng conflict pattern](#4-áp-dụng-conflict-pattern)
5. [Lập SoD conflict record](#5-lập-sod-conflict-record)
6. [Thiết kế mitigating control](#6-thiết-kế-mitigating-control)
7. [Kiểm soát emergency access](#7-kiểm-soát-emergency-access)
8. [Lập bản đồ dependency](#8-lập-bản-đồ-dependency)
9. [Lập dependency record](#9-lập-dependency-record)
10. [Đánh giá SPOF](#10-đánh-giá-spof)
11. [Xử lý unique owner và common-mode failure](#11-xử-lý-unique-owner-và-common-mode-failure)
12. [Kiểm tra chất lượng](#12-kiểm-tra-chất-lượng)

## 1. Mục đích và nguyên tắc

Áp dụng module này khi cần phân tích Segregation of Duties (`SoD`), conflict về quyền hạn, emergency access, dependency hoặc Single Point of Failure (`SPOF`).

Thực hiện các nguyên tắc sau:

- Phân biệt process design, system entitlement và effective access của actual user.
- Không mặc định role conflict là actual conflict khi chưa có user assignment hoặc effective-access evidence.
- Không mặc định mọi conflict phải loại bỏ; đánh giá business justification và mitigation khi full segregation không khả thi.
- Không coi mọi unique owner hoặc unique performer là SPOF.
- Không coi số lượng provider lớn hơn một là đủ để loại trừ SPOF; kiểm tra common-mode failure và competing demand.
- Không bịa user, role, access, authority, backup, capacity, recovery time, outage tolerance hoặc review frequency.
- Không hard-code severity, threshold hoặc tolerance; dùng methodology và appetite đã được phê duyệt.
- Gắn source, evidence, assumption, confidence và review status cho mỗi kết luận.

## 2. Phân tích SoD ở ba cấp

Phân tích riêng từng cấp và chỉ hợp nhất sau khi tie-out dữ liệu.

### 2.1. Process-role SoD

Phân tích duties được gán cho role trong process map, SOP, RACI hoặc approval matrix.

Thực hiện:

1. Liệt kê activity tạo lập, thay đổi, phê duyệt, ghi nhận, giữ tài sản, thanh toán, review và monitoring.
2. Xác định activity pair có thể cho phép một role khởi tạo và che giấu hoặc tự phê duyệt cùng giao dịch.
3. Gắn process, step, role và decision right.
4. Đánh dấu design conflict là `Potential` nếu chưa có dữ liệu actual user.
5. Ghi document conflict khi policy, SOP, RACI hoặc approval matrix phân công khác nhau.

Không dùng process-role analysis để khẳng định actual user có effective access.

### 2.2. System-access SoD

Phân tích role, permission, transaction code, privilege hoặc entitlement trong system/application.

Thực hiện:

1. Lập role-to-permission và permission-to-activity map.
2. Xác định role đơn lẻ hoặc role combination tạo conflicting capabilities.
3. Kiểm tra inherited role, nested group, privileged access, interface account và service account.
4. Kiểm tra environment, entity, business unit, data scope và effective date.
5. Xác định preventive rule, workflow restriction hoặc configuration có thực sự chặn execution không.
6. Đánh dấu role-level capability là `Potential` khi chưa gán cho actual user hoặc chưa chứng minh user có thể thực hiện cả hai activity.

Không đồng nhất role name với effective permission. Không coi system role design là bằng chứng giao dịch đã xảy ra.

### 2.3. Actual-user SoD

Phân tích effective access của từng user khi có dữ liệu đủ tin cậy.

Thực hiện:

1. Kết hợp user assignment, direct permission, inherited role, privileged access và temporary access.
2. Xác minh effective date, expiry, entity, environment và data scope.
3. Xác minh cùng một user có capability thực hiện cả activity A và B không.
4. Tách access capability khỏi transaction evidence.
5. Kiểm tra transaction log nếu mandate yêu cầu xác định conflict đã được exercised.
6. Xác định mitigating control và kết quả review liên quan.

Chỉ dùng `Actual conflict` khi evidence chứng minh cùng một actual user có effective conflicting capabilities trong cùng scope và thời kỳ liên quan. Ghi riêng `Conflict exercised` nếu log chứng minh user đã thực hiện cả hai activity; không gộp hai khái niệm.

## 3. Xác định potential và actual conflict

Áp dụng decision logic sau:

1. Nếu activity pair không incompatible trong context, ghi `No conflict` và rationale.
2. Nếu process role hoặc system role có conflicting duties/capabilities nhưng chưa có user assignment, ghi `Potential`.
3. Nếu có user assignment nhưng thiếu effective permission, scope hoặc timing, ghi `To be validated` và không nâng thành actual.
4. Nếu cùng user có effective conflicting capabilities trong cùng scope/thời kỳ, ghi `Actual`.
5. Nếu transaction evidence cho thấy user đã thực hiện cả hai sides, ghi thêm exercised status và evidence.
6. Nếu preventive configuration chặn một activity dù role name có vẻ conflict, kiểm tra configuration evidence trước khi kết luận.
7. Nếu access đã hết hạn hoặc revoke, phân biệt current status với historical exposure.

Không dùng `Potential` như đồng nghĩa với low risk. Không dùng `Actual` như đồng nghĩa với fraud hoặc control failure. Đánh giá risk, business justification và mitigation riêng.

## 4. Áp dụng conflict pattern

Dùng các pattern sau như candidate rules; điều chỉnh theo process, system, authority và business model. Không coi danh sách là đầy đủ hoặc bắt buộc cho mọi organization.

### Procurement và Accounts Payable

- Request purchase và approve purchase.
- Create vendor và approve vendor.
- Create vendor và process invoice.
- Purchase và receive.
- Receive và approve invoice.
- Process invoice và release payment.

### Sales và Order-to-Cash

- Create customer và approve credit.
- Create order và approve discount.
- Ship goods và record revenue.
- Issue credit note và approve credit note.
- Perform billing và record cash receipt.

### Finance và Treasury

- Prepare journal và post journal.
- Post journal và approve journal.
- Perform bank reconciliation và execute payment.
- Create bank account và approve bank account.
- Record asset và maintain physical custody.

### Inventory

- Maintain custody và record inventory.
- Count inventory và approve adjustment.
- Issue stock và approve adjustment.

### HR và Payroll

- Create employee và process payroll.
- Change salary và approve salary change.
- Prepare payroll và release payroll payment.

### IT

- Request access và approve access.
- Develop change và deploy change.
- Administer system và review administrator logs.
- Create user và certify access.

Thêm pattern theo industry hoặc organization chỉ khi có source và applicability. Không hard-code materiality hoặc severity cho pattern.

## 5. Lập SoD conflict record

Tạo một record cho mỗi incompatible activity pair và scope với tối thiểu các field:

| Field | Cách ghi |
|---|---|
| `sod_conflict_id` | Gán ID ổn định và duy nhất. |
| `activity_a` | Ghi activity thứ nhất và liên kết process step/permission. |
| `activity_b` | Ghi activity thứ hai và liên kết process step/permission. |
| `risk` | Mô tả risk event và impact do combination tạo ra. |
| `roles_involved` | Liệt kê process role và system role liên quan. |
| `users_involved` | Liệt kê user chỉ khi có dữ liệu được phép sử dụng; nếu chưa có, dùng null semantics. |
| `system` | Ghi system, environment, entity và relevant scope. |
| `severity` | Dùng methodology được phê duyệt; không tự đặt rating. |
| `actual_or_potential` | Ghi `Potential`, `Actual` hoặc `To be validated` theo evidence. |
| `business_justification` | Ghi lý do cần giữ combination và approval source. |
| `mitigating_control` | Liên kết control ID; không dùng mô tả chung chung. |
| `mitigation_owner` | Ghi owner độc lập và có authority phù hợp. |
| `monitoring` | Mô tả population, data, criteria, evidence và exception follow-up. |
| `approval` | Ghi approver và approval evidence cho exception/risk acceptance. |
| `review_frequency` | Ghi frequency có căn cứ hoặc `To be validated`; không hard-code. |

Bổ sung khi cần:

- `sod_level`: process-role, system-access hoặc actual-user;
- `scope` và `effective_period`;
- `conflict_exercised`;
- `transaction_evidence`;
- `source` và `source_reference`;
- `assumptions`, `confidence` và `review_status`;
- `expiry` và `recertification_status`.

Không đưa unnecessary personal data vào report. Dùng user ID hoặc role-based pseudonymization khi danh tính không cần thiết cho decision.

## 6. Thiết kế mitigating control

Cho phép mitigating control khi full segregation không khả thi vì quy mô, staffing, system limitation, emergency hoặc business continuity, nhưng không mặc định mitigation luôn đủ.

Đánh giá mitigation theo:

- `Independence`: người thực hiện mitigation có độc lập với conflicted duties không?
- `Coverage`: mitigation có bao phủ toàn bộ relevant population, period, entity và system không?
- `Timing`: mitigation có preventive hoặc sufficiently timely detective effect không?
- `Precision`: criteria có phát hiện unauthorized, unusual hoặc self-approved transaction không?
- `Data reliability`: report/log có đầy đủ, chính xác và chống sửa đổi không?
- `Evidence`: có lưu review, exception, investigation và closure không?
- `Authority`: reviewer có quyền challenge, reject, revoke hoặc escalate không?
- `Sustainability`: mitigation có duy trì khi volume tăng, staff vắng hoặc system thay đổi không?
- `Common-mode dependency`: mitigation có phụ thuộc cùng user, data hoặc system đang tạo conflict không?

Mô tả mitigating control bằng owner, action, frequency/trigger, system/data, population, evidence, exception handling và escalation. Không dùng “manager review” hoặc “management oversight” nếu thiếu các thuộc tính này.

Nếu chấp nhận conflict, ghi business justification, residual exposure, approval, expiry và periodic recertification theo governance được phê duyệt.

## 7. Kiểm soát emergency access

Yêu cầu emergency hoặc break-glass access có tối thiểu:

1. `Approval`: yêu cầu pre-approval phù hợp hoặc documented emergency approval path.
2. `Time limit`: giới hạn thời gian và tự động hết hạn khi system hỗ trợ; không tự đặt duration.
3. `Logging`: ghi đầy đủ user, privilege, reason, timestamp, activity và affected object.
4. `Post-review`: yêu cầu review độc lập, timely, documented và có exception follow-up.

Bổ sung theo context:

- unique named account thay cho shared credential;
- least privilege và scoped access;
- ticket/case linkage;
- alerting và privileged-session monitoring;
- credential rotation hoặc revocation;
- periodic test của break-glass process;
- review owner, escalation và evidence retention.

Đánh dấu gap khi thiếu một trong bốn thuộc tính bắt buộc. Không kết luận emergency access được kiểm soát chỉ vì có log nếu không có approval và post-review.

## 8. Lập bản đồ dependency

### Quy tắc input tối thiểu

Khi input chỉ mô tả một dependency pattern (ví dụ hai site dùng cùng utility) mà chưa có record nguồn, chỉ phân loại candidate `shared/common-mode dependency`; không tự cấp dependency/risk ID, giả định tên site/provider, recovery target, capacity, topology, test result hoặc xác nhận SPOF. Dùng prefix canonical khi người dùng yêu cầu tạo draft IDs; nếu không, giữ ID `Not provided`. Mọi risk statement, treatment và recovery design ở trạng thái hypothesis cho đến khi có source/evidence và owner phê duyệt.

Phân tích dependency đối với tối thiểu các loại phù hợp:

- Person;
- Skill;
- Approval authority;
- System;
- Application;
- Interface;
- Data;
- Master data;
- Equipment;
- Site;
- Warehouse;
- Supplier;
- Material;
- Utility;
- Contract;
- License;
- Bank;
- Transport route;
- Knowledge;
- Password hoặc credential;
- Shared service.

Thực hiện:

1. Xác định provider và consumer của dependency.
2. Liên kết dependency với process, step, control và business objective.
3. Xác định minimum requirement về availability, capacity, quality, authority hoặc data.
4. Xác định direct, upstream, downstream, outsourced, shared và fourth-party dependencies.
5. Xác định substitute, lead time, capacity và precondition để substitute hoạt động.
6. Xác định manual workaround, documentation, cross-training, backup và recovery arrangement.
7. Xác định common-mode failure, geographic concentration và competing demand.
8. Gắn source, evidence, assumption và confidence.

Không dừng ở first-tier supplier hoặc primary system. Theo dõi dependency chain đến điểm failure có thể làm gián đoạn outcome trong scope.

## 9. Lập dependency record

Tạo một record cho mỗi dependency với tối thiểu các field:

| Field | Cách ghi |
|---|---|
| `dependency_id` | Gán ID ổn định và duy nhất. |
| `dependency_type` | Chọn type phù hợp. |
| `provider` | Ghi person, role, system, supplier, site hoặc service cung cấp. |
| `consumer` | Ghi process, step, control, system hoặc stakeholder phụ thuộc. |
| `process_id` | Liên kết process. |
| `step_id` | Liên kết process step. |
| `minimum_requirement` | Mô tả mức tối thiểu đã được phê duyệt; không tự đặt threshold. |
| `capacity` | Ghi capacity có evidence hoặc `To be validated`. |
| `substitute_available` | Ghi substitute thực sự có thể dùng, không chỉ tên candidate. |
| `substitution_lead_time` | Ghi lead time có evidence; không hard-code. |
| `recovery_time` | Ghi capability/target đã được phê duyệt và phân biệt với actual evidence. |
| `maximum_outage_tolerance` | Ghi tolerance có nguồn; không tự suy ra. |
| `documentation_available` | Ghi tài liệu hiện hành, đủ dùng và có thể truy cập. |
| `cross_training` | Ghi người được đào tạo, scope, currency và evidence. |
| `backup` | Ghi backup person/system/site/supplier và readiness. |
| `manual_workaround` | Mô tả workaround, capacity, control và test status. |
| `spof_status` | Ghi kết luận theo methodology hoặc `To be validated`. |
| `risk` | Liên kết `risk_id` hoặc mô tả risk event/impact. |
| `owner` | Ghi dependency owner được xác minh. |
| `evidence` | Liên kết BIA, contract, log, test, inventory, interview hoặc record khác. |

Bổ sung `source`, `assumptions`, `confidence`, `review_status`, `common_mode_group` và `competing_demand` khi cần.

## 10. Đánh giá SPOF

Đánh giá một dependency là SPOF dựa trên combination của:

- `Criticality`: failure ảnh hưởng objective hoặc minimum service ra sao?
- `Backup availability`: backup có tồn tại, sẵn sàng, được ủy quyền và truy cập được không?
- `Substitution lead time`: substitute có hoạt động trước tolerance được phê duyệt không?
- `Capacity`: backup/substitute có đủ capacity và quality không?
- `Documentation`: knowledge, procedure, configuration và contact có đầy đủ và hiện hành không?
- `Cross-training`: backup personnel có được đào tạo và thực hành không?
- `Recovery time`: recovery capability có phù hợp target/tolerance được phê duyệt không?
- `Common-mode failure`: primary và backup có cùng site, utility, credential, network, supplier hoặc component không?
- `Geographic concentration`: các alternatives có cùng vùng rủi ro không?
- `Shared dependency`: nhiều processes hoặc customers có phụ thuộc cùng resource không?
- `Competing demand`: backup có bị nhiều consumers cùng cần trong disruption không?

Chỉ kết luận SPOF khi evidence và methodology cho thấy failure của dependency có thể làm gián đoạn outcome trọng yếu và không có mitigation/substitute đủ hiệu quả trong tolerance áp dụng.

Không hard-code rating, outage tolerance, recovery target hoặc capacity threshold. Nếu thiếu dữ liệu, ghi `To be validated` và nêu evidence cần thu thập hoặc test cần thực hiện.

## 11. Xử lý unique owner và common-mode failure

Không tự động coi mọi unique owner là SPOF.

Đối với unique owner hoặc unique performer, kiểm tra:

- Có competent và authorized backup không?
- Backup có quyền system, delegation và approval authority cần thiết không?
- Procedure, decision criteria, contact và knowledge có được tài liệu hóa không?
- Cross-training có hiện hành và có evidence không?
- Handover hoặc absence scenario đã được walkthrough/test chưa?
- Backup có đủ capacity trong thời gian cần thiết không?
- Primary và backup có cùng điểm failure như credential, device, location hoặc approver không?

Nếu các điều kiện trên đủ và có evidence, ghi unique ownership nhưng không gắn SPOF tự động. Nếu owner duy nhất chỉ là accountability trong khi execution có resilient backup, phân biệt accountability với operational dependency.

Ngược lại, không loại trừ SPOF chỉ vì có nhiều người, nhiều systems hoặc nhiều suppliers. Kiểm tra:

- tất cả dùng cùng database, interface, utility, site hoặc credential;
- suppliers dùng cùng fourth party, material source hoặc route;
- alternate approver thiếu authority;
- backup capacity không đủ;
- manual workaround chưa được test;
- resources bị competing demand trong cùng disruption.

Nhóm dependencies có common-mode failure bằng `common_mode_group` và đánh giá ở cấp group, không chỉ từng record riêng lẻ.

## 12. Kiểm tra chất lượng

Trước khi giao output, kiểm tra:

- Đã phân tích riêng process-role, system-access và actual-user SoD.
- Đã phân biệt `Potential`, `Actual` và `Conflict exercised`.
- Không suy ra actual conflict từ role name hoặc role matrix đơn lẻ.
- Mỗi accepted conflict có business justification, mitigation, owner, approval và review.
- Mitigating control có independence, population, precision, evidence và exception handling.
- Emergency access có approval, time limit, logging và post-review.
- Mỗi SPOF conclusion liên kết dependency record và evidence.
- Mỗi dependency có provider, consumer, minimum requirement, substitute, lead time, capacity, owner và evidence hoặc trạng thái thiếu rõ ràng.
- Không coi unique owner là SPOF tự động.
- Đã kiểm tra common-mode failure, geographic concentration, shared dependency và competing demand.
- Không bỏ sót upstream, downstream hoặc fourth-party dependency.
- Không bịa user, access, authority, backup, capacity, recovery target, tolerance, rating hoặc frequency.
- Đã giảm thiểu personal data trong SoD output.
