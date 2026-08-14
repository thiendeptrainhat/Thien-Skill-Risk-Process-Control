# Nhận diện rủi ro, thiết kế control và xác định key control

## Mục lục

1. [Mục đích và nguyên tắc](#1-mục-đích-và-nguyên-tắc)
2. [Nhận diện rủi ro theo process step](#2-nhận-diện-rủi-ro-theo-process-step)
3. [Chuẩn hóa risk statement](#3-chuẩn-hóa-risk-statement)
4. [Lập risk record](#4-lập-risk-record)
5. [Xác định control objective](#5-xác-định-control-objective)
6. [Soạn control description](#6-soạn-control-description)
7. [Lập control record](#7-lập-control-record)
8. [Phân loại control](#8-phân-loại-control)
9. [Đánh giá chất lượng thiết kế](#9-đánh-giá-chất-lượng-thiết-kế)
10. [Xác định testability và giới hạn kết luận](#10-xác-định-testability-và-giới-hạn-kết-luận)
11. [Xác định key control](#11-xác-định-key-control)
12. [Phân biệt control với non-control activity](#12-phân-biệt-control-với-non-control-activity)
13. [Kiểm tra truy nguyên và chất lượng](#13-kiểm-tra-truy-nguyên-và-chất-lượng)

## 1. Mục đích và nguyên tắc

Áp dụng module này khi cần nhận diện rủi ro trong quy trình, xác định control objective, mô tả control, đánh giá design quality hoặc phân loại key control.

Thực hiện các nguyên tắc sau:

- Bắt đầu từ business objective, process objective và required outcome.
- Phân tích theo end-to-end process và từng process step; không giới hạn theo silo phòng ban.
- Tách `As-Documented`, `As-Designed`, `As-Performed` và `Target-State` trong mọi nhận định.
- Liên kết từng risk với objective bị ảnh hưởng và từng control với risk được xử lý.
- Chỉ ghi dữ kiện có source hoặc evidence; ghi assumption và confidence cho nội dung chưa xác minh.
- Không bịa role, system, configuration, population, threshold, frequency, rating hoặc evidence.
- Không tự chấm inherent risk, residual risk hoặc design rating khi chưa có methodology được chấp thuận.
- Không kết luận operating effectiveness từ policy, SOP hoặc control description.
- Không coi automated control luôn tốt hơn manual control; đánh giá theo context, dependency và practicality.
- Giữ một source of truth cho risk ID, control ID, owner, threshold, version và control description.

## 2. Nhận diện rủi ro theo process step

### Quy tắc input tối thiểu

Khi input chỉ nêu “risk X bị bỏ sót” mà chưa cung cấp process/objective/step/source, chỉ được: (1) phân loại `candidate missing-risk observation`; (2) nêu các fraud/error/safety/legal lenses cần challenge; (3) đưa risk-statement và control-objective **template có placeholder/null**; (4) lập validation request. Không tự cấp `risk_id`, `objective_id`, `control_id`, owner, trigger, system, evidence, cause cụ thể hoặc objective của organization. Nếu nêu control pattern, gắn `candidate Target-State hypothesis`, giải thích điều kiện áp dụng và để ID/owner/frequency/threshold/evidence `To be validated`. “Fraud risk bị bỏ sót” không tự chứng minh fraud, control gap, current-control absence hoặc operating failure.

Thực hiện lần lượt:

1. Xác định objective, trigger, input, output, stakeholder và end state của quy trình.
2. Tách quy trình thành các step, handoff, decision point, exception path và dependency.
3. Challenge từng step bằng các câu hỏi sau:
   - Step có thể không được thực hiện, bị bỏ qua hoặc bị override không?
   - Step có thể được thực hiện sai, trễ, hai lần hoặc ngoài sequence không?
   - Người không có thẩm quyền có thể thực hiện hoặc phê duyệt step không?
   - Input, master data hoặc transaction data có thể thiếu, sai, trùng hoặc không kịp thời không?
   - System, interface, equipment hoặc utility có thể không sẵn sàng không?
   - Fraud, error, conflict of interest hoặc management override có thể phát sinh không?
   - Legal, regulatory, contractual hoặc internal requirement có thể bị vi phạm không?
   - Customer, financial reporting, safety, quality, environment, privacy hoặc cybersecurity có thể bị ảnh hưởng không?
   - Dependency, bottleneck, single point of failure hoặc capacity constraint có tồn tại không?
   - Exception, manual workaround hoặc change có thể không được kiểm soát không?
4. Xem xét tối thiểu các risk driver phù hợp:
   - People, skill, capacity và governance;
   - Process, quality, fraud và error;
   - System, data, model, AI, cybersecurity và privacy;
   - Third party, contract, supplier và supply chain;
   - Regulation, financial, market và external event;
   - Safety, environment, site, equipment, utility, project và change.
5. Loại bỏ cách diễn đạt trùng lặp; giữ riêng các risk khác nhau về cause, event, impact hoặc objective.
6. Gắn source, evidence, assumption và confidence cho từng risk.

Không viết risk chỉ là tên chủ đề như “rủi ro quy trình”, “rủi ro hệ thống” hoặc “rủi ro tuân thủ”. Không viết control failure thay cho risk event nếu chưa phân tích cause và impact.

## 3. Chuẩn hóa risk statement

Viết risk statement theo cấu trúc:

> Due to **[cause hoặc risk driver]**, **[uncertain event hoặc failure]** may occur, resulting in **[business impact]** and affecting **[objective]**.

Hoặc biểu diễn ngắn:

> Cause → Risk Event → Impact → Objective

Kiểm tra từng thành phần:

- Mô tả `cause` là điều kiện hoặc driver làm tăng khả năng xảy ra event.
- Mô tả `event` là sự kiện không chắc chắn hoặc failure có thể xảy ra.
- Mô tả `impact` là hậu quả kinh doanh, khách hàng, tài chính, tuân thủ, an toàn, chất lượng hoặc vận hành.
- Liên kết `objective` với business objective hoặc process objective cụ thể.
- Tách cause khỏi impact; không đảo ngược hai thành phần.
- Tránh khẳng định kết luận pháp lý nếu chưa có legal analysis có thẩm quyền.
- Ghi nhiều impact hoặc objective bằng quan hệ có cấu trúc khi cần; không nhồi nhiều risk độc lập vào một statement.

Ví dụ đạt chuẩn:

> Do dữ liệu tài khoản ngân hàng của vendor được nhập thủ công và không có xác minh độc lập, thông tin thanh toán không hợp lệ có thể được kích hoạt, dẫn đến thanh toán sai hoặc gian lận và ảnh hưởng mục tiêu thanh toán chính xác, hợp lệ.

## 4. Lập risk record

Tạo một record cho từng risk với tối thiểu các field:

| Field | Cách ghi |
|---|---|
| `risk_id` | Gán ID ổn định và duy nhất. |
| `process_id` | Liên kết process chứa risk. |
| `step_id` | Liên kết process step phát sinh hoặc chịu risk. |
| `objective_id` | Liên kết objective bị ảnh hưởng. |
| `risk_statement` | Dùng cấu trúc Cause–Event–Impact–Objective. |
| `cause` | Ghi cause hoặc risk driver. |
| `event` | Ghi uncertain event hoặc failure. |
| `impact` | Ghi hậu quả có thể xảy ra. |
| `risk_category` | Dùng taxonomy của engagement; không tự tạo category gây trùng. |
| `affected_stakeholders` | Liệt kê stakeholder bị ảnh hưởng. |
| `source` | Ghi nguồn tạo dữ kiện hoặc yêu cầu. |
| `evidence` | Liên kết evidence hiện có; không đồng nhất source với evidence vận hành. |
| `inherent_risk` | Dùng methodology được phê duyệt; để trạng thái chưa đánh giá nếu thiếu. |
| `existing_controls` | Liên kết một hoặc nhiều `control_id`; không chép lại control tùy tiện. |
| `control_coverage` | Mô tả coverage theo cause, event hoặc impact và nêu khoảng trống. |
| `residual_exposure` | Chỉ đánh giá theo methodology và evidence phù hợp. |
| `assumptions` | Ghi rõ nội dung tạm giả định. |
| `confidence` | Dùng thang confidence đã được định nghĩa cho engagement. |
| `owner` | Ghi risk owner đã xác minh hoặc `To be validated`. |

Không tự điền rating khi thiếu criteria, appetite, scale hoặc người có thẩm quyền. Không dùng việc thiếu dữ liệu để suy ra risk thấp.

## 5. Xác định control objective

Mô tả control objective như trạng thái cần đạt để xử lý risk, không như một hoạt động kiểm tra.

Thực hiện:

1. Bắt đầu từ objective và risk event.
2. Xác định điều kiện phải đúng trước, trong hoặc sau process step.
3. Viết outcome có thể đánh giá được nhưng không gắn sẵn một control duy nhất.
4. Giữ control objective đủ rộng để cho phép nhiều control cùng hỗ trợ nhưng đủ cụ thể để xác định coverage.
5. Gán `control_objective_id` ổn định và liên kết với `risk_id` phù hợp.

Ví dụ:

> Only authorized and valid vendors are created or modified.

Tránh viết:

> Manager reviews the vendor form.

Câu thứ hai là activity hoặc control description chưa đầy đủ, không phải control objective.

## 6. Soạn control description

Soạn control description theo cấu trúc:

> **[Control owner hoặc performer]** performs **[specific control action]** at **[frequency hoặc trigger]** using **[system, report hoặc source data]** to prevent or detect **[risk]**, retains **[evidence]**, and escalates exceptions to **[role]** within **[defined timeframe]**.

Làm rõ tối thiểu:

- Ai chịu accountability và ai trực tiếp thực hiện?
- Thực hiện action nào và trên population nào?
- Thực hiện khi nào: theo frequency hay trigger nào?
- Dùng system, report, data source hoặc criteria nào?
- Áp dụng threshold và precision nào, nếu có căn cứ?
- Ngăn ngừa, phát hiện hoặc sửa chữa risk nào?
- Tạo và giữ evidence nào?
- Xử lý exception, escalation và follow-up ra sao?

Ví dụ đạt chuẩn:

> Vendor Master Data Team xác minh quyền sở hữu tài khoản ngân hàng, thông tin thuế và approval bắt buộc trước khi kích hoạt vendor mới trong ERP; lưu approved onboarding package và system audit log; chuyển exception đến Procurement Manager theo thời hạn đã được phê duyệt.

Không tự thêm frequency, threshold, timeframe, system hoặc role nếu source không cung cấp. Dùng `Not provided` hoặc `To be validated` và nêu tác động tới testability.

## 7. Lập control record

Tạo một record cho từng control với tối thiểu các field:

| Field | Cách ghi |
|---|---|
| `control_id` | Gán ID ổn định và duy nhất. |
| `control_name` | Đặt tên ngắn, phân biệt được. |
| `control_objective` | Liên kết hoặc mô tả trạng thái cần đạt. |
| `risk_ids` | Liên kết tất cả risk được control xử lý. |
| `process_id` | Liên kết process. |
| `step_id` | Liên kết process step. |
| `control_description` | Dùng cấu trúc action–timing–data–evidence–exception. |
| `control_owner` | Ghi role accountable đã xác minh. |
| `performer` | Ghi role thực hiện. |
| `reviewer` | Ghi role review, nếu áp dụng. |
| `approver` | Ghi role approval, nếu áp dụng. |
| `control_type` | Phân loại theo mục đích. |
| `control_nature` | Phân loại theo cách vận hành. |
| `frequency` | Ghi frequency có nguồn hoặc trạng thái chưa có. |
| `trigger` | Ghi event kích hoạt control. |
| `system` | Ghi system hoặc application dependency. |
| `data_source` | Ghi report, data object hoặc source system. |
| `population` | Xác định population thuộc phạm vi control. |
| `threshold` | Ghi threshold có căn cứ; không hard-code. |
| `precision` | Mô tả mức precision hoặc criteria review. |
| `evidence` | Ghi artifact chứng minh việc thực hiện. |
| `retention` | Ghi retention requirement có căn cứ. |
| `exception_handling` | Mô tả cách ghi nhận và xử lý exception. |
| `escalation` | Mô tả role, condition và route escalation. |
| `automation_level` | Mô tả mức automation theo taxonomy được chọn. |
| `it_dependency` | Liên kết dependency về system, configuration, interface hoặc report. |
| `key_control_status` | Ghi classification và approval status. |
| `control_source` | Liên kết requirement, policy, framework hoặc design source. |
| `design_assessment` | Ghi assessment theo methodology đã phê duyệt. |
| `limitations` | Ghi limitation, assumption, override hoặc scope exclusion. |

Liên kết source và applicability theo [standards-sources-applicability.md](standards-sources-applicability.md) khi control bắt nguồn từ law, regulation, contract, standard, framework hoặc practice.

## 8. Phân loại control

Phân loại độc lập theo các chiều sau; không dùng một chiều thay cho chiều khác.

### Theo mục đích

- `Preventive`: ngăn event trước khi xảy ra.
- `Detective`: phát hiện event hoặc deviation đã xảy ra.
- `Corrective`: khắc phục condition hoặc impact.
- `Directive`: định hướng hành vi hoặc yêu cầu thực hiện.
- `Monitoring`: theo dõi hiệu quả, xu hướng hoặc exception của controls/process.

### Theo cách vận hành

- `Manual`;
- `Automated`;
- `IT-dependent manual`;
- `Hybrid`.

### Theo tần suất hoặc trigger

- `Per transaction`;
- `Daily`;
- `Weekly`;
- `Monthly`;
- `Quarterly`;
- `Annual`;
- `Event-driven`;
- `Continuous`.

Chỉ chọn giá trị phản ánh thiết kế có nguồn. Không mặc định frequency tối ưu hoặc thay đổi frequency khi chưa đánh giá risk, volume, precision và burden.

### Theo phạm vi

- `Entity-level`;
- `Process-level`;
- `Transaction-level`;
- `Application-level`;
- `Infrastructure-level`.

Ghi nhiều classification khi cần và tránh gộp các chiều vào một nhãn không rõ nghĩa.

## 9. Đánh giá chất lượng thiết kế

Đánh giá từng control theo các dimension sau:

1. `Objective alignment`: xác định control có hướng tới trạng thái cần đạt không.
2. `Risk coverage`: xác định control xử lý cause, event hay impact và coverage còn thiếu.
3. `Timing`: đánh giá control diễn ra đủ sớm để ngăn hoặc phát hiện risk không.
4. `Frequency`: đánh giá frequency có phù hợp với tốc độ phát sinh risk và volume không.
5. `Precision`: đánh giá criteria, threshold, granularity và investigation scope.
6. `Population completeness`: đánh giá toàn bộ population có được đưa vào control không.
7. `Data reliability`: đánh giá completeness, accuracy, source, transformation và access của data/report.
8. `Owner competence`: đánh giá authority, capability và accountability của owner/performer.
9. `Independence`: đánh giá self-review, self-approval và conflict of duties.
10. `Evidence`: đánh giá evidence có chứng minh được action, thời điểm, reviewer và result không.
11. `Exception management`: đánh giá identification, logging, disposition và closure.
12. `Escalation`: đánh giá criteria, route, authority và timeliness.
13. `Resilience`: đánh giá backup, continuity và recovery khi người/system không sẵn sàng.
14. `Override susceptibility`: đánh giá khả năng bypass hoặc management override.
15. `Dependency`: đánh giá system, data, interface, third party và upstream control.
16. `Sustainability`: đánh giá khả năng duy trì qua volume, turnover và change.
17. `Cost and practicality`: cân bằng risk reduction với burden, capacity và customer impact.

Ghi observation và rationale theo từng dimension. Chỉ tổng hợp thành design assessment khi engagement đã xác định scale, criteria và approval authority. Không tự hard-code rating hoặc threshold.

## 10. Xác định testability và giới hạn kết luận

Xác định một control là có thể test về thiết kế khi control record làm rõ:

- owner/performer;
- action và criteria;
- population;
- frequency hoặc trigger;
- system và data source;
- evidence;
- exception handling và escalation.

Từ policy, SOP, procedure hoặc control description, chỉ kết luận về:

- design adequacy;
- document completeness;
- theoretical risk coverage;
- testability.

Chỉ chuẩn bị draft operating-effectiveness assessment và test-results handoff khi có testing objective, approved methodology, population, sample hoặc full-population approach, system data, data-reliability work, executed walkthrough/observation/inspection/reperformance và evidence phù hợp. Không tự quyết định sample size khi chưa có objective, population, frequency, assurance level, methodology và professional judgment phù hợp. Skill không tự phát hành formal operating-effectiveness conclusion; assurance owner độc lập có thẩm quyền giữ quyết định đó.

Nếu evidence thiếu, ghi `assessment_status: Not assessed` và `evidence_status: Insufficient evidence`; không dùng chúng như null semantics và không chuyển thành kết luận control failed.

## 11. Xác định key control

Không coi mọi control là key control. Thực hiện quy trình sau:

1. Xác định significant risk hoặc requirement trọng yếu bằng methodology đã được phê duyệt.
2. Xác định control nào tạo coverage chính cho risk hoặc requirement đó.
3. Xác định control thay thế, compensating control và supporting control có thực sự tương đương không.
4. Đánh giá hậu quả nếu control không tồn tại hoặc thất bại.
5. Đánh giá mức reliance của management, governance body, financial reporting, compliance, safety, quality hoặc environment.
6. Đánh giá dependency của các control hoặc decision khác vào control này.
7. Ghi source, evidence, assumption, confidence và người phê duyệt classification.

Cân nhắc key classification khi có một hoặc nhiều căn cứ sau:

- Control xử lý significant risk.
- Control là cơ chế chính để ngăn hoặc phát hiện material failure.
- Control liên kết trực tiếp với legal, regulatory hoặc contractual obligation trọng yếu đã được xác minh.
- Control xử lý financial reporting risk trọng yếu.
- Control xử lý safety, quality hoặc environmental risk trọng yếu.
- Không có control thay thế tương đương trong thời gian yêu cầu.
- Việc control thất bại có thể khiến residual risk vượt risk appetite đã được phê duyệt.
- Nhiều control hoặc decision quan trọng phụ thuộc vào control.
- Management hoặc governance body dựa vào output của control.
- Requirement hoặc governance decision yêu cầu test/certification định kỳ.

Ghi key-control rationale với tối thiểu:

- `control_id`;
- linked `risk_id` và `requirement_id`, nếu có;
- rationale theo criteria được áp dụng;
- role của control trong control set;
- alternative hoặc compensating controls;
- consequence of failure;
- dependency và reliance;
- source và evidence;
- assumption và confidence;
- proposed classification;
- reviewer, approver và review status.

Phân biệt:

- `Key Control`;
- `Supporting Control`;
- `Compensating Control`;
- `Monitoring Control`;
- `Redundant Control`;
- `Non-Control Activity`.

Không hạ key status chỉ vì có nhiều controls cùng tên hoặc cùng risk. Kiểm tra strength, timing, precision, independence và actual coverage của control thay thế trước khi kết luận.

## 12. Phân biệt control với non-control activity

Không tự coi các câu sau là control:

- “Nhân viên phải cẩn thận.”
- “Tuân thủ chính sách.”
- “Quản lý theo dõi.”
- “Hệ thống có báo cáo.”
- “Được phê duyệt.”

Yêu cầu mô tả rõ:

- ai thực hiện;
- làm gì;
- khi nào;
- trên population nào;
- dựa trên system, data hoặc criteria nào;
- tạo evidence nào;
- xử lý exception ra sao.

Phân loại activity là `Non-Control Activity` nếu activity chỉ tạo output vận hành mà không thay đổi khả năng hoặc tác động của risk, không xác minh criteria, không ngăn/detect/correct risk và không tạo monitoring hữu ích.

## 13. Kiểm tra truy nguyên và chất lượng

Trước khi giao output, kiểm tra:

- Mỗi risk có cause, event, impact và objective.
- Mỗi risk liên kết process và step phù hợp.
- Mỗi control liên kết ít nhất một risk và một control objective.
- Mỗi control có owner, action, timing/trigger, data, evidence và exception handling hoặc nêu rõ thiếu gì.
- Mỗi proposed key control có rationale, significant-risk linkage và approval status.
- Không over-classify toàn bộ controls là key.
- Không dùng best practice như mandatory requirement khi chưa xác minh source và applicability.
- Không kết luận operating effectiveness chỉ từ documentation.
- Không bịa rating, threshold, population, sample size, role, system hoặc source.
- Không mất quan hệ nhiều-nhiều giữa risk và control khi chuyển sang RCM.
- Giữ risk ID, control objective ID và control ID nhất quán trong process map, control library, RCM và test program.
