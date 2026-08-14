# Control gap, control rationalization và Risk and Control Matrix

## Mục lục

1. [Mục đích và nguyên tắc](#1-mục-đích-và-nguyên-tắc)
2. [Phân loại control gap](#2-phân-loại-control-gap)
3. [Lập gap record](#3-lập-gap-record)
4. [Phân biệt gap, observation và finding](#4-phân-biệt-gap-observation-và-finding)
5. [Thực hiện control rationalization](#5-thực-hiện-control-rationalization)
6. [Chọn rationalization disposition](#6-chọn-rationalization-disposition)
7. [Thiết kế RCM nhiều-nhiều](#7-thiết-kế-rcm-nhiều-nhiều)
8. [Lập RCM record](#8-lập-rcm-record)
9. [Áp dụng null semantics](#9-áp-dụng-null-semantics)
10. [Tạo các RCM view](#10-tạo-các-rcm-view)
11. [Quản lý rating, testing và sampling](#11-quản-lý-rating-testing-và-sampling)
12. [Kiểm tra chất lượng và tie-out](#12-kiểm-tra-chất-lượng-và-tie-out)

## 1. Mục đích và nguyên tắc

Áp dụng module này khi cần phân tích control gap, loại bỏ over-control hoặc duplicated control, rationalize control set, tạo RCM hoặc chuyển đổi giữa các RCM view.

Thực hiện các nguyên tắc sau:

- Bắt đầu từ objective, risk, requirement và existing control coverage.
- Tách `As-Documented`, `As-Designed`, `As-Performed` và `Target-State`.
- Không gọi một nội dung là operating deviation nếu chưa có evidence về cách thực hiện thực tế.
- Không tự động biến mọi gap thành audit finding.
- Không loại bỏ control chỉ để rút ngắn cycle time hoặc giảm cost.
- Không thêm control chỉ vì “càng nhiều càng tốt”.
- Bảo toàn quan hệ nhiều-nhiều giữa risk, control, requirement, process step, evidence và action.
- Không bịa severity, rating, threshold, sample size, owner hoặc remediation deadline.
- Giữ một source of truth cho ID và canonical description; tạo view từ dữ liệu gốc thay vì tạo các bảng độc lập.

## 2. Phân loại control gap

Chọn một hoặc nhiều `gap_type` từ taxonomy sau; ghi primary type và related types nếu một gap có nhiều đặc điểm:

| Gap type | Câu hỏi phân tích |
|---|---|
| `Missing Control` | Có risk hoặc requirement chưa được control nào xử lý không? |
| `Weak Design` | Control có tồn tại nhưng không đủ để đạt control objective không? |
| `Unclear Control` | Mô tả có thiếu actor, action, timing, data, evidence hoặc exception không? |
| `Untestable Control` | Người kiểm tra có thể xác định population, criteria và evidence không? |
| `No Evidence` | Thiết kế có quy định evidence phù hợp không? Evidence thực tế có được cung cấp không? |
| `Inadequate Frequency` | Frequency có phù hợp với tốc độ phát sinh risk, volume và detection window không? |
| `Insufficient Precision` | Criteria, threshold hoặc review depth có đủ precision không? |
| `Incomplete Population` | Control có bỏ sót transaction, location, system, entity hoặc exception không? |
| `Unreliable Data` | Data/report có thiếu completeness, accuracy, provenance hoặc access control không? |
| `Missing Owner` | Có role accountable được xác định và chấp thuận không? |
| `Conflicting Owner` | Nhiều nguồn có gán owner khác nhau hoặc accountability chồng lấn không? |
| `Inadequate Segregation` | Duties có tạo self-review, self-approval hoặc conflict không? |
| `Override Risk` | Control có thể bị bypass mà không có approval, logging hoặc post-review không? |
| `Missing Exception Handling` | Có cách ghi nhận, xử lý và đóng exception không? |
| `Missing Escalation` | Có trigger, route, authority và timeframe escalation không? |
| `Missing Monitoring` | Không ai theo dõi performance, exception, aging hoặc control failure phải không? |
| `Missing Retention` | Evidence có retention requirement hoặc khả năng truy xuất không? |
| `Unsupported IT Dependency` | Manual control có dựa vào system/report/configuration chưa được kiểm soát không? |
| `Uncontrolled Manual Workaround` | Workaround có approval, access, reconciliation và expiry không? |
| `Duplicated Control` | Hai control có lặp action, population, timing và risk coverage không? |
| `Redundant Control` | Control có không tạo incremental coverage hoặc reliance hữu ích không? |
| `Over-Control` | Control burden có vượt giá trị risk reduction nhưng vẫn cần phân tích residual risk không? |
| `Control Bottleneck` | Control có tạo queue, delay hoặc capacity constraint trọng yếu không? |
| `Control Not Aligned to Risk` | Control có không xử lý cause, event hoặc impact của linked risk không? |
| `Control Not Aligned to Requirement` | Control có không đáp ứng obligation hoặc adopted requirement được mapping không? |
| `Operating Deviation` | Evidence có cho thấy thực tế khác thiết kế/documentation không? |

Không dùng `No Evidence` để kết luận control không vận hành nếu engagement chỉ đánh giá design và chưa thu thập evidence thực tế. Ghi rõ layer được đánh giá.

## 3. Lập gap record

Tạo một record cho từng gap với tối thiểu các field:

| Field | Cách ghi |
|---|---|
| `gap_id` | Gán ID ổn định và duy nhất. |
| `process_id` | Liên kết process chịu ảnh hưởng. |
| `risk_id` | Liên kết risk; cho phép nhiều link trong association table. |
| `control_id` | Liên kết control nếu gap thuộc một control; dùng null semantics khi không áp dụng. |
| `gap_type` | Chọn taxonomy phù hợp; không dùng nhãn chung nếu có type cụ thể. |
| `description` | Mô tả condition, expected state và difference. |
| `cause` | Ghi root cause đã xác minh hoặc giả thuyết cần validation. |
| `impact` | Ghi impact lên objective, risk, requirement, cost, capacity hoặc customer. |
| `source` | Ghi nguồn của expected state và observed state. |
| `evidence` | Liên kết artifact hỗ trợ condition; phân biệt missing evidence với evidence of absence. |
| `severity` | Dùng methodology được phê duyệt; không tự hard-code scale. |
| `recommendation` | Ghi outcome cần đạt, không áp đặt một giải pháp khi còn alternatives. |
| `alternative_options` | So sánh retain, strengthen, automate, consolidate, replace, monitor, remove hoặc compensate. |
| `owner` | Ghi action owner hoặc `To be validated`; không mặc định control owner. |
| `priority` | Dùng criteria và governance của engagement. |
| `dependency` | Liên kết prerequisite, system, data, person, project hoặc external dependency. |

Bổ sung khi cần:

- `layer`: As-Documented, As-Designed, As-Performed hoặc Target-State;
- `requirement_id`;
- `control_objective_id`;
- `assumptions`;
- `confidence`;
- `review_status`;
- `management_response`;
- `target_date`;
- `validation_needed`.

Không gộp nhiều gap có owner, cause, recommendation hoặc dependency khác nhau vào một record chỉ để giảm số dòng.

## 4. Phân biệt gap, observation và finding

Phân loại output theo maturity của evidence và mandate:

- `Observation`: ghi nhận condition hoặc inconsistency cần xem xét, chưa kết luận deficiency.
- `Design Opportunity`: nêu cơ hội cải thiện target state mà không khẳng định control hiện tại không đạt.
- `Control Gap`: nêu chênh lệch design hoặc coverage so với risk/control objective.
- `Compliance Gap`: nêu chênh lệch với requirement bắt buộc đã xác minh về applicability.
- `Potential Finding`: nêu issue có thể trở thành finding sau validation theo audit methodology.
- `Confirmed Finding`: chỉ dùng khi scope, criteria, condition, cause, effect, evidence và authority xác nhận đều đáp ứng methodology có thẩm quyền.

Không tự nâng cấp classification vì gap có impact lớn. Không gọi framework recommendation là compliance gap nếu framework chỉ advisory hoặc chưa được organization adopt.

## 5. Thực hiện control rationalization

Lập control universe trước khi rationalize. Nhóm controls theo risk, control objective, requirement, population, process step, timing và evidence.

Challenge từng control set:

1. Xác định controls trùng action, population, criteria, timing hoặc evidence.
2. Xác định controls cùng xử lý một risk nhưng không tăng coverage, precision, independence hoặc resilience.
3. Xác định approvals hoặc reviews không tạo thêm challenge hay decision right.
4. Xác định reports được tạo nhưng không có người review, action hoặc escalation.
5. Xác định controls tạo bottleneck, queue, rework hoặc excessive handoff.
6. Xác định controls không còn phù hợp với process, system, requirement hoặc risk.
7. Xác định manual controls có thể automate sau khi process và criteria đã ổn định.
8. Xác định controls tốn nhiều resource nhưng vẫn không đủ strength.
9. Xác định upstream preventive control có thể thay thế downstream duplicate detective controls không.
10. Xác định common dependency có thể làm nhiều controls thất bại cùng lúc không.

Đánh giá incremental coverage trước khi gọi control là duplicated hoặc redundant. Hai controls cùng risk vẫn có thể bổ sung nhau nếu khác timing, population, independence, data source, objective hoặc failure mode.

Lập rationalization record với tối thiểu:

- `rationalization_id`;
- `control_ids` trong control set;
- linked `risk_ids`, `control_objective_ids` và `requirement_ids`;
- current purpose và coverage;
- overlap và incremental coverage;
- design strength và limitations;
- dependency và common-mode failure;
- evidence và actual use of output;
- operational burden, capacity và customer impact;
- proposed disposition;
- alternative options;
- expected benefit;
- risk of change;
- residual exposure consideration;
- prerequisite và implementation dependency;
- owner, reviewer, approver và review status;
- source, assumption và confidence.

## 6. Chọn rationalization disposition

Chọn một hoặc nhiều disposition sau và ghi rationale:

- `Retain`: giữ nguyên khi control tạo coverage cần thiết và design phù hợp.
- `Strengthen`: cải thiện owner, action, frequency, precision, data, evidence, exception hoặc resilience.
- `Automate`: chuyển phần phù hợp sang system control sau khi chuẩn hóa process, data và criteria.
- `Consolidate`: hợp nhất controls khi vẫn bảo toàn coverage, independence, timing và evidence.
- `Replace`: thay control yếu hoặc lỗi thời bằng control khác mạnh hơn và khả thi hơn.
- `Convert to monitoring`: chuyển activity sang monitoring khi không cần transaction-level prevention/detection.
- `Remove`: loại bỏ chỉ sau khi đánh giá requirement, reliance, alternative coverage và residual risk.
- `Add compensating control`: thêm mitigation khi control chính không khả thi hoặc chưa sẵn sàng.

Không remove hoặc consolidate control trước khi:

- xác minh control không bắt buộc theo law, regulation, contract, certification hoặc internal adoption;
- đánh giá effect lên significant risk và key-control set;
- kiểm tra upstream/downstream dependency;
- xác định residual risk theo methodology;
- có owner và governance approval phù hợp;
- lập transition, rollback và validation plan khi thay đổi trọng yếu.

Không đề xuất automation cho process chưa chuẩn hóa, data không đáng tin cậy hoặc exception logic chưa rõ.

## 7. Thiết kế RCM nhiều-nhiều

Bảo toàn các quan hệ sau:

- Một risk liên kết nhiều controls.
- Một control liên kết nhiều risks.
- Một control objective liên kết nhiều risks và controls.
- Một requirement liên kết nhiều controls; một control có thể hỗ trợ nhiều requirements.
- Một control có nhiều evidence items, test attributes, gaps và actions.

Ưu tiên mô hình chuẩn hóa:

- Lưu canonical `Risk`, `ControlObjective`, `Control`, `Requirement`, `Evidence`, `Gap` và `Action` thành object riêng.
- Lưu association `Risk–Control`, `Requirement–Control` và `Control–Evidence` bằng link table hoặc mảng ID có kiểm soát.
- Chỉ flatten thành RCM view khi xuất báo cáo.
- Không nhân risk rating hoặc control count chỉ vì quan hệ nhiều-nhiều tạo nhiều dòng.
- Dùng stable ID làm key; không dùng tên dễ thay đổi làm key duy nhất.

Nếu dùng một bảng phẳng, tạo một `rcm_id` riêng cho từng association row và giữ canonical IDs. Ghi rõ grain của bảng để tránh double count.

## 8. Lập RCM record

Hỗ trợ tối thiểu các field sau; không bắt buộc mọi field có giá trị khi dữ liệu chưa đủ:

### Process và objective

- `rcm_id`
- `process_id`
- `process_name`
- `subprocess_id`
- `step_id`
- `objective_id`
- `business_objective`
- `process_objective`

### Risk

- `risk_id`
- `risk_statement`
- `risk_cause`
- `risk_event`
- `risk_impact`
- `risk_category`
- `inherent_likelihood`
- `inherent_impact`
- `inherent_rating`

### Control objective và control

- `control_objective_id`
- `control_objective`
- `control_id`
- `control_name`
- `control_description`
- `control_owner`
- `control_performer`
- `control_reviewer`
- `control_approver`
- `control_type`
- `control_nature`
- `frequency`
- `trigger`
- `system`
- `data_source`
- `population`
- `threshold`
- `precision`
- `evidence`
- `retention`
- `exception_handling`
- `escalation`
- `key_control`
- `compensating_control`

### Source, assessment và testing

- `control_source`
- `mandatory_or_advisory`
- `design_assessment`
- `design_gap`
- `residual_risk`
- `kri`
- `kci`
- `test_attribute`
- `test_procedure`
- `sampling_consideration`
- `source_reference`
- `assumptions`
- `confidence`
- `review_status`

Giữ `risk_statement` và `control_description` đồng nhất với canonical records. Nếu output cần snapshot theo thời điểm, ghi source version và snapshot date thay vì sửa dữ liệu lịch sử.

## 9. Áp dụng null semantics

Không thay giá trị thiếu bằng nội dung suy đoán. Dùng nhất quán:

- `Null`: chưa có giá trị trong data model và chưa xác định nguyên nhân.
- `Not provided`: source hoặc người dùng chưa cung cấp giá trị cần thiết.
- `Not applicable`: field không áp dụng cho record; ghi rationale khi có thể gây hiểu nhầm.
- `To be validated`: có candidate value hoặc claim nhưng chưa đủ evidence/approval để xác nhận.

Không dùng chuỗi rỗng, dấu gạch ngang, `0`, `No` hoặc `N/A` lẫn lộn để biểu diễn các trạng thái trên. Không coi `Null` là không có risk, không có control hoặc assessment thấp.

Khi chuyển đổi file hoặc view:

1. Bảo toàn null state gốc.
2. Không tự điền owner, threshold, rating, sample size hoặc source.
3. Ghi transformation rule và validation issue.
4. Tách `Not applicable` khỏi `Not provided` trong filtering và metrics.

## 10. Tạo các RCM view

Tạo view từ cùng canonical data:

- `Risk-centric view`: nhóm theo risk; hiển thị toàn bộ controls, gaps và residual exposure liên quan.
- `Control-centric view`: nhóm theo control; hiển thị toàn bộ risks, requirements, dependencies, evidence và tests.
- `Process-step view`: sắp theo end-to-end process, subprocess và step.
- `Requirement-centric view`: nhóm theo legal, regulatory, contractual, adopted hoặc internal requirement.
- `Audit-test view`: nhóm key controls/testable controls với attributes, evidence và procedures.
- `Management-action view`: nhóm gaps, recommendations, actions, owner, dependency và review status.

Kiểm tra view conservation:

- Không làm mất risk–control association khi pivot.
- Không làm mất một control vì control xử lý nhiều risk.
- Không double count risk hoặc control trong summary metric.
- Không biến advisory source thành mandatory khi tạo requirement-centric view.
- Không biến `Null` thành factual value.
- Giữ source reference, assumption và confidence qua mọi view.

## 11. Quản lý rating, testing và sampling

Không hard-code inherent likelihood, inherent impact, inherent rating, residual risk, gap severity hoặc priority.

Trước khi dùng rating, yêu cầu:

- methodology và scale được phê duyệt;
- criteria cho likelihood và impact;
- aggregation rule và treatment của outlier;
- risk appetite hoặc tolerance liên quan;
- source, assessor, assessment date và approval status.

Không tự suy ra residual risk chỉ từ số lượng controls. Đánh giá design, coverage, dependency và operating evidence theo mandate.

Chỉ đề xuất `test_attribute`, `test_procedure` và draft test-results handoff dựa trên control design và evidence đã thực thi. Không tự phát hành formal operating-effectiveness conclusion. Không quyết định sample size cuối cùng khi chưa có testing objective, population size, frequency, expected deviation, assurance level, methodology và professional judgment có thẩm quyền.

Ghi `sampling_consideration` dưới dạng yếu tố cần xem xét hoặc `To be validated`; không bịa một con số.

## 12. Kiểm tra chất lượng và tie-out

Trước khi giao output, kiểm tra:

- Mỗi gap liên kết process, risk, control hoặc requirement phù hợp.
- Mỗi gap có source và evidence hoặc ghi rõ thiếu evidence.
- `Operating Deviation` chỉ dựa trên as-performed evidence.
- Không tự động đổi gap thành confirmed finding.
- Mỗi rationalization decision có coverage analysis, alternatives và residual-risk consideration.
- Không remove key hoặc mandatory control khi chưa có review và approval.
- Mỗi risk–control association được bảo toàn trong mọi view.
- Risk ID, control objective ID, control ID và requirement ID tồn tại và không trùng ngoài chủ đích.
- Không có orphan control, orphan gap hoặc orphan action.
- Không double count risk/rating do flatten many-to-many.
- Không bịa rating, threshold, sample size, owner hoặc deadline.
- Null semantics được dùng nhất quán.
- Source, applicability và mandatory/advisory status tie out với source register.
- RCM tie out với process map, control library, workflow, RACI, audit program và action register.
