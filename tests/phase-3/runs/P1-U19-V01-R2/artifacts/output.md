# Phân tích E2E, rủi ro và kiểm soát — bản dự thảo

## Tóm tắt điều hành

Điểm cần xử lý là **chưa có cơ sở thống nhất, truy nguyên được để kết luận beneficiary B-19 đã được xác nhận đúng yêu cầu trước thanh toán**. Đây chưa phải kết luận tài khoản sai, gian lận hoặc control thất bại trên toàn quy trình.

- `CTL-SHARED-19` là **một control logic**, được dùng tại hai điểm của `PROC-19A` và `PROC-19B`. SOP-19B xác nhận cùng cấu hình/cơ chế; không được đếm thành hai lớp bảo vệ độc lập.
- `REQ-19 §2` yêu cầu kênh xác nhận độc lập, hoàn tất trước lần thanh toán đầu tiên và hồ sơ có locator. Gọi dịch vụ hoặc lưu chữ `VERIFIED` chưa tự chứng minh đủ ba điều kiện.
- Checklist B-19 ghi `VERIFIED` nhưng trường nguồn cuộc gọi trống; trace trung tâm ghi `PENDING_REVIEW` trước phát lệnh. Chủ nguồn chưa giải thích. Giữ cả hai observation và trạng thái tổng hợp `Unresolved`, không tự chọn nguồn thắng.
- `TX-19` đã phát ngày 10/07/2026; chưa đủ để kết luận vi phạm REQ-19: cần xác minh liên kết với đúng tài khoản/phiên bản B-19, đây có phải first payment sau thay đổi, timestamps, bằng chứng xác nhận khác và hiệu lực quy định tại ngày đó.
- Ưu tiên theo dependency: hòa giải hồ sơ và locator; làm rõ điều kiện chấp nhận kết quả chung; sau đó chọn phương án quản lý thủ công/tích hợp phù hợp. Không tự bỏ một điểm gọi hoặc tự động hóa trước khi chốt rule.

[analysis-data.json](/private/tmp/thien-rpc-phase3.xGeed0/P1-U19-V01-R2/analysis-data.json) chứa các object, source locator, baseline links, scoped observations, comparisons, RCM relationships, no-change scenarios và actions để tạo các view từ cùng dữ liệu.

Phạm vi kết luận: phân tích hồ sơ tổng hợp, documentation/theoretical coverage và quan sát của một trường hợp. Không có phương pháp chấm risk, population đáng tin cậy hoặc kiểm thử vận hành đã thực hiện; do đó không chấm inherent/residual risk, severity, sample size hoặc formal operating effectiveness. Mọi thiết kế/RCM/action là draft, chưa được phê duyệt.

## 1. Mục tiêu, boundary và E2E phù hợp

| Quy trình, mục tiêu | Boundary đã cung cấp | E2E candidate và giới hạn |
|---|---|---|
| `PROC-19A`; `OBJ-19A`: chỉ sử dụng tài khoản đã xác nhận | Nhận yêu cầu đổi tài khoản → phê duyệt/lưu master data | `E2E-19-SUP`: đoạn quản trị thay đổi thông tin trong Supplier-Onboarding-to-Offboarding. Chỉ là partial mapping, không có bằng chứng toàn vòng đời nhà cung cấp. |
| `PROC-19B`; `OBJ-19B`: trả đúng nghĩa vụ được duyệt; sử dụng đầu vào liên quan OBJ-19A | Nhận hóa đơn → duyệt/trả tiền → đối chiếu sổ | `E2E-19-PAY`: Invoice-to-Payment, nối tới đối chiếu sổ. Phù hợp hơn việc chia riêng theo phòng ban. |
| Hai quy trình có giao diện chung | Kết quả xác nhận beneficiary/master data hỗ trợ quyết định thanh toán | `E2E-19-P2P`: Procure-to-Pay là chuỗi lớn hơn để liên kết. Không tự bổ sung sourcing, mua hàng hay nhận hàng thực tế chỉ vì có PO/chứng từ nhận hàng. |

Đây là mappings do analyst đề xuất (`MAP-19-01…04`), không phải taxonomy/reference ID chính thức của publisher. L0–L5, parent process, entity/site, process owner, SLA và volume: `Not provided/To be validated`. Không ép dựng đủ sáu cấp từ hai boundary.

Luồng hiện trạng chỉ xác định được các ràng buộc sau:

| Step ID | Nội dung As-Documented | Người thực hiện/timing có nguồn |
|---|---|---|
| `STEP-19A-01…03` | Nhận yêu cầu; gọi dịch vụ và lưu status; phê duyệt/lưu master data | Người cập nhật master data gọi dịch vụ. Thứ tự chi tiết giữa cuộc gọi, cập nhật và phê duyệt chưa đủ mô tả. |
| `STEP-19B-01…04` | Nhận hóa đơn; đối chiếu PO/nhận hàng/hóa đơn; lập lệnh; duyệt | Match trước lập lệnh. Người match, người duyệt, precision và approval authority chưa nêu. |
| `STEP-19B-05…06` | Gọi dịch vụ trước phát lệnh; phát lệnh/thanh toán | Người phát khác người lập theo SOP. Không suy vị trí cuộc gọi so với lập lệnh ngoài điều kiện “trước phát”. |
| `STEP-19B-07` | Đối chiếu sổ | Chỉ có end boundary; chưa đủ owner, criteria, evidence để xác định một reconciliation control riêng. |

Các exception, rejection/rework, escalation, evidence-retention và handoff acceptance chưa được cung cấp. Không biến sơ đồ happy path suy đoán thành As-Performed. Chưa có nguồn riêng để xác nhận lớp As-Designed.

## 2. Nguồn, bằng chứng và độ tin cậy

Đọc trực tiếp [hồ sơ tổng hợp](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U19-V01/input.md>); không đọc chứng từ gốc, chạy OCR, truy cập hệ thống hay tra cứu bên ngoài. Nguồn cho phép đọc, dùng AI và lưu/tái phân phối trong phạm vi đã nêu tại dòng 1.

| Source ID / locator trong hồ sơ | Nội dung có thể sử dụng | Giới hạn |
|---|---|---|
| `SRC-19-SCOPE`, dòng 1–3, 10 | Quyền sử dụng; OBJ-19A/B; PROC-19A/B; dữ kiện thiếu | Entity/site, methodology, ngân sách, action owner/date và keyness approval chưa có. |
| `REQ-19 §2`, dòng 4 | Quy định nội bộ được phê duyệt cho cả hai quy trình | Nội dung và phạm vi được cung cấp; version/ngày hiệu lực/authority record gốc chưa có. Không phải nghĩa vụ pháp luật đã kiểm chứng. |
| `SOP-19A §3`, dòng 5 | Cuộc gọi dịch vụ/lưu status khi cập nhật master data | Chỉ chứng minh As-Documented. |
| `SOP-19B §4`, dòng 6 | Dùng chung control; timing trước phát; match; phân tách lập/phát | Chưa có cấu hình được kiểm tra hoặc bằng chứng thực hiện các control này. |
| `EVD-19A`, dòng 7 | Checklist B-19 ký 10/07/2026, raw status VERIFIED; trường nguồn cuộc gọi trống | Không có timestamp xác nhận, locator khác hoặc xác định checklist thuộc điểm dùng nào. |
| `EVD-19B`, dòng 8 | Trace cùng ngày, raw status PENDING_REVIEW trước phát lệnh | State semantics, timestamps chi tiết, correlation và nguyên nhân khác biệt chưa được chủ nguồn giải thích. |
| `EVD-19C`, dòng 9 | TX-19 đã phát 10/07/2026 | Một trường hợp, không phải full population; không chứng minh settlement, matching, phê duyệt hay control pass. |

Confidence `Medium` cho diễn giải nội dung nguồn được cung cấp; `Unresolved` cho trạng thái xác nhận thực sự của B-19. Đây không phải thang probability hoặc risk rating.

## 3. Risks, expected controls và current controls

Các risk dưới đây là kịch bản Cause → Event → Impact, không phải kết luận sự cố đã xảy ra.

| Risk ID → mục tiêu | Kịch bản | Control objective / liên kết control |
|---|---|---|
| `RSK-19-01` → OBJ-19A/B | Nếu status không có bằng chứng độc lập đúng tài khoản hoặc còn mâu thuẫn → có thể dùng tài khoản chưa xác nhận → thanh toán sai bên nhận/khó thu hồi hoặc không đạt mục tiêu trả đúng nghĩa vụ. | `COBJ-19-01`: xác nhận độc lập trước first payment; `COBJ-19-03`: hồ sơ truy nguyên được. `CTL-SHARED-19`. Căn cứ REQ-19, SOP-19A/B, EVD-19A/B/C. |
| `RSK-19-02` → OBJ-19B | Nếu match/authorization/segregation không đủ chính xác hoặc bị bỏ qua → có thể phát lệnh không đúng nghĩa vụ duyệt → chi sai, tranh chấp/chênh lệch sổ. | `COBJ-19-02`: nghĩa vụ đúng và phân tách lập/phát. `CTL-19-MATCH`, `CTL-19-SOD`. Đây là hypothesis từ OBJ-19B/SOP-19B; chưa có evidence deviation. |
| `RSK-19-03` → OBJ-19A/B | Thiếu đường dẫn nguồn hoặc status chưa hòa giải → quyết định có thể dựa trên kết quả không truy nguyên được → quyết định sai, chậm xử lý và không chứng minh được REQ-19. | `COBJ-19-03`; `CTL-SHARED-19`. REQ-19 và EVD-19A/B. |
| `RSK-19-04` → OBJ-19A/B | Cùng dịch vụ/cấu hình gặp lỗi dữ liệu hoặc gián đoạn → hai điểm cùng sai/chậm → xác nhận và chi trả bị ảnh hưởng. | `COBJ-19-04`: khả năng sử dụng kết quả tin cậy/ứng phó gián đoạn, là proposal. `DEP-19-01`. SOP-19A/B chứng minh shared dependency, không chứng minh outage/SPOF. |

### Baseline được nguồn hỗ trợ

- `CBL-19-01`: REQ-19 §2 → COBJ-19-01/03 → RSK-19-01/03 → CTL-SHARED-19. Ba điều kiện là independent channel, timing trước first payment và locator. Không suy requirement bắt buộc một phần mềm, hard-stop hay một kênh liên hệ cụ thể.
- `CBL-19-02`: SOP-19B §4 → COBJ-19-02 → RSK-19-02 → CTL-19-MATCH/CTL-19-SOD. Giữ đúng nội dung match trước lập và phát khác lập; không tự đặt tolerance.
- `CBL-19-03/04`: liên kết status với account version/time, xử lý conflict và resilience là **analyst implementation proposals**, không phải điều khoản chuẩn ngoài đã xác minh.

### Một logical control, nhiều observation

| Control / observation | Layer và scope | Current description và assessment |
|---|---|---|
| `CTL-SHARED-19` / `OBS-19-D01` | As-Documented; PROC-19A; kỳ hiệu lực chưa cung cấp | Người cập nhật master data gọi dịch vụ và lưu status. Có hướng tới xác nhận beneficiary; đoạn SOP chưa đủ mô tả independent channel, locator, criteria, exception và accountability. |
| Cùng `CTL-SHARED-19` / `OBS-19-D02` | As-Documented; PROC-19B; kỳ hiệu lực chưa cung cấp | Cùng dịch vụ/cấu hình/cơ chế, gọi trước phát lệnh. Timing có ích nhưng gọi chưa đồng nghĩa xác nhận hoàn tất hay có cơ chế chặn phát. |
| Cùng `CTL-SHARED-19` / `OBS-19-P01` | As-Performed observation của checklist B-19 ngày 10/07/2026; vị trí process chưa nêu | Giữ nguyên VERIFIED và trường nguồn cuộc gọi trống. Chỉ xác nhận nội dung record theo mô tả, không xác nhận hành động independent verification đã hoàn thành. |
| Cùng `CTL-SHARED-19` / `OBS-19-P02` | As-Performed observation của trace B-19 trước phát lệnh ngày 10/07/2026 | Giữ nguyên PENDING_REVIEW. Không ghi đè checklist/SOP hoặc tự suy failure; cần reconciliation. |
| `CTL-19-MATCH` / `OBS-19-D03` | As-Documented; PROC-19B | Đối chiếu PO/nhận hàng/hóa đơn trước lập lệnh. Có theoretical coverage nghĩa vụ; owner, tolerance, evidence, exception và thực hiện TX-19 chưa cung cấp. |
| `CTL-19-SOD` / `OBS-19-D04` | As-Documented; PROC-19B | Người phát khác người lập. Có process-role segregation rule; chưa chứng minh system enforcement hay actual users. |

Hai ID `CTL-19-MATCH/SOD` do analyst cấp để truy nguyên hành động có trong SOP; không phải controls mới vừa triển khai. TX-19 nằm ở `OBS-19-TX`, là **process observation**, không được dùng làm bằng chứng CTL-SHARED-19 đã pass.

Key-control rationale: CTL-SHARED-19 là **key-control candidate** riêng trong phạm vi mỗi SOP vì trực tiếp hỗ trợ REQ-19 và quyết định của cả hai quy trình dựa vào kết quả của nó. Chưa có methodology/significant-risk assessment, inventory alternatives hoặc approval designation; không được ghi “approved key control” cho mọi layer/kỳ. Matching và maker–releaser separation hỗ trợ OBJ-19B, nhưng chưa chứng minh thay thế tương đương independent beneficiary confirmation. Keyness của chúng đối với OBJ-19B còn cần đánh giá, không mặc định mọi control đều key.

## 4. Comparison, gaps, SoD và dependency

| Comparison / issue ID | Kết luận đúng phạm vi | Validation cần thiết |
|---|---|---|
| `CMP-19-01` → `GAP-19-03` | Documentation gap trong đoạn đã đọc: gọi/lưu status chưa đủ mô tả independent channel, locator, precision, pending/conflict route và trách nhiệm. Potential design gap, chưa phải bằng chứng các cơ chế không tồn tại. | Thiết kế/SOP đầy đủ, data contract, trạng thái và exception rules được phê duyệt, configuration evidence, owner/authority. |
| `CMP-19-02` → `GAP-19-01` | Observation: hai status khác nhau chưa hòa giải. Có thể khác thời điểm, phiên bản hoặc semantics; chưa được phép chọn một trạng thái làm sự thật chung. | Raw events, event/correlation IDs, timestamps/timezone, account version, định nghĩa status, giải thích và review của nguồn có thẩm quyền. |
| `CMP-19-02` → `GAP-19-02` | Trường nguồn cuộc gọi của checklist trống là dữ kiện; chưa đủ chứng minh locator tồn tại. Không suy rằng không có locator ở record khác hoặc chưa hề xác nhận. | Confirmation record/locator gốc truy xuất được; bằng chứng kênh độc lập và timing; liên kết B-19/account/TX-19/first payment. |
| `CMP-19-03` → `OPP-19-02` | Match/SoD được SOP mô tả nhưng thiếu performed evidence. Đây là evidence limitation, không tạo fake Missing Control/finding. | Criteria, approval matrix, match evidence, role/access/transaction logs và reconciliation record. |

Không có confirmed finding hoặc formal compliance/OE conclusion. Root cause và severity chưa được xác định.

SoD (`SOD-19-01`): biết rule phân tách ở process-role level; system-access và actual-user levels chưa có dữ liệu. Người cập nhật master data gọi dịch vụ không tự chứng minh tự xác nhận hoặc actual conflict. Không có cơ sở khẳng định cùng người lập/phát TX-19 hay conflict đã được exercised.

Dependency (`DEP-19-01`): hai consumers dùng chung service/configuration là có căn cứ. Backup, capacity, substitution lead time, recovery time, outage tolerance và manual workaround đều chưa cung cấp; `spof_status: To be validated`. Đây là common-mode dependency cần khảo sát, không phải confirmed SPOF.

Rationalization: giữ một logical ID; **chưa bỏ một trong hai điểm gọi**. Điểm upstream có thể ngăn sai sớm, điểm trước phát có thể kiểm tra tính còn áp dụng tại thời điểm sử dụng; incremental coverage này cần xác minh bằng thiết kế/record. Cũng không coi chúng là control độc lập bù trừ nhau. Chưa có burden/cycle-time data để kết luận duplicated, redundant hoặc over-control.

## 5. Cải tiến và lựa chọn Target-State

`OBS-19-T01` là đề xuất củng cố cùng CTL-SHARED-19: lưu kết quả xác nhận độc lập có locator, beneficiary/account version, event/time và provenance; hai điểm dùng tham chiếu kết quả nhất quán. Nếu pending, conflict hoặc chưa có bằng chứng phù hợp, không dùng status như một kết quả đã xác nhận; chuyển xử lý có thẩm quyền trước quyết định thanh toán liên quan. Đây là **rule đề xuất**, chưa phải current hard-stop.

| Option | Lợi ích có điều kiện | Trade-off / dependency |
|---|---|---|
| A — Minimum-control proposal; compliance chưa được kết luận | Review thủ công được kiểm soát đối với confirmation/locator/timing; có thể ít thay đổi hệ thống hơn. | Cần người có thẩm quyền/độc lập, capacity, bằng chứng review; còn human-error risk. |
| B — Balanced control and efficiency | Một record có version/locator và data contract dùng chung; giảm nhập lặp, tách exception review; giữ timing cần thiết ở mỗi điểm. | Phải chốt source-of-truth, status semantics, ownership và khả năng tích hợp; common-mode risk vẫn còn. |
| C — Automation-first proposal | Gate tự động kiểm tra criteria trước sử dụng/phát lệnh nếu rule/data đã đáng tin. | Sai rule có thể ảnh hưởng đồng loạt; cần UAT, access/change governance, failure route, rollback và approval production. Không mặc định tốt hơn manual. |

B là candidate để thẩm định sau khi hòa giải evidence; A có thể được xem xét làm biện pháp tạm thời nếu được phê duyệt và khả thi. Chưa chọn phương án triển khai vì thiếu ngân sách, capacity, technology feasibility, implementation time và risk appetite. Không đưa savings, thời hạn hoặc chi phí ước tính không có căn cứ.

### Action view — draft, chưa giao việc chính thức

| Action → recommendation | Gap/opportunity; no-change link | Việc cần làm và evidence đóng | Dependency |
|---|---|---|---|
| `ACT-19-01 → REC-19-01` | GAP-19-01/02; NCS-19-01 | Hòa giải B-19/TX-19; lấy locator, timestamp, account version, correlation và first-payment status. Đóng khi người có authority xác nhận reconciliation có nguồn; nếu chưa đủ thì giữ Unresolved, không sửa raw record để “khớp”. | Độc lập với thiết kế tương lai. |
| `ACT-19-02 → REC-19-02` | GAP-19-03; NCS-19-01 | Chốt control contract OBS-19-T01, owner/criteria/exception, cập nhật thiết kế/SOP theo approval. Closure cần specification được phê duyệt, test records, transition/rollback. | ACT-19-01 cho semantics và thiết kế dựa trên conflict. |
| `ACT-19-03 → REC-19-03` | OPP-19-01; NCS-19-02 | Khảo sát DEP-19-01 và thử phương án fallback/common-mode trong môi trường được phép; có capacity/tolerance/authority evidence. | Có thể khảo sát song song; không tự đặt recovery target. |
| `ACT-19-04 → REC-19-04` | OPP-19-02; NCS-19-03 | Lấy match, approval, user/access và reconciliation evidence; hoàn thiện test design. Nếu cần assurance, owner độc lập chốt scope/methodology và kết luận. | Không chờ automation; không tự chốt sample. |

Tất cả action owner, accountable executive, due date, budget và priority rating: **Not provided**; trường có cấu trúc giữ null kèm lý do. Vai trò phê duyệt phải được tổ chức chỉ định, không mặc định người cập nhật master data hoặc người phát lệnh là Control Owner. Không có action đã triển khai hoặc đã đóng.

## 6. Rủi ro nếu giữ nguyên

| Scenario ID | Cause → event → impact và bảo vệ hiện có | Exposure chưa xử lý / uncertainty |
|---|---|---|
| `NCS-19-01` — GAP-19-01/02/03 | Giữ status không hòa giải/không truy nguyên và criteria chưa rõ → có thể sử dụng tài khoản khi xác nhận chưa được chứng minh → thanh toán sai hoặc không chứng minh REQ-19. Có dịch vụ, match và segregation được SOP mô tả. | Chưa xác nhận operating protection; match/SoD không thay thế independent confirmation. Chưa biết locator khác, timeline, account/first-payment linkage và alternatives. Không khẳng định TX-19 đã gây thiệt hại. |
| `NCS-19-02` — OPP-19-01 | Nếu dịch vụ/cấu hình chung gặp lỗi hoặc outage → hai consumers cùng sai/chậm → ảnh hưởng xác nhận và trả nghĩa vụ. Hai điểm gọi vẫn dùng cùng cơ chế. | Kịch bản giả thuyết, chưa chứng minh outage hoặc thiếu backup. Cần capacity, substitutes, lead time, recovery tolerance và test evidence. |
| `NCS-19-03` — OPP-19-02 | Nếu match/SoD không đủ chính xác hoặc không vận hành → có thể phát lệnh không đúng nghĩa vụ → chi sai/chênh lệch. Hai controls được mô tả trong SOP. | Kịch bản giả thuyết; thiếu evidence không chứng minh fail. Cần kiểm tra criteria, authority, effective users, execution và đối chiếu sổ. |

Không tự đặt horizon, probability, loss hoặc risk score; các trường này là null/Not assessed.

## 7. Evidence/test attributes và dữ liệu bàn giao

Các thủ tục `TST-19-01…06` trong JSON là **potential tests, chưa thực hiện**: xác minh kênh độc lập; timing trước first payment; locator/status transitions; exception/configuration design; matching theo criteria được duyệt; maker/releaser identity và effective access. Trước kiểm thử vận hành cần objective, approved methodology, population, completeness/accuracy/lineage checks và approach sampling/full-population được phê duyệt. Không dùng một case để tính deviation rate hoặc phát hành OE.

Metrics Target-State, chưa tính và chưa có target/threshold được duyệt:

- `MET-19-01` — KCI: first payments sau đổi tài khoản có xác nhận độc lập đúng timing và locator truy xuất được / tổng first payments liên quan trong kỳ.
- `MET-19-02` — KRI: distinct confirmation IDs có conflict chưa xử lý / tổng distinct confirmation IDs được dùng; phải đối chiếu đúng version/time.
- `MET-19-03` — KPI: thời gian từ nhận yêu cầu đổi tài khoản tới phê duyệt/lưu master data; tách pending/rejected và báo aging để tránh che backlog.

Grain dữ liệu: **3 control logic; 7 control observations** gồm 4 As-Documented, 2 As-Performed record observations và 1 Target-State; **13 RCM association rows**. Một process observation TX-19 được lưu riêng. Control count phải là `COUNT DISTINCT control_id`, không đếm observations/lần gọi/RCM rows.

Bản JSON giữ 4 risks, 3 gap records có classification/giới hạn, 3 comparisons, 3 no-change scenarios và 4 actions. RCM lấy description/assessment từ đúng observation ID; action view lấy recommendation/gap/opportunity/dependency từ cùng object set, không lập facts riêng.

Theo nguyên tắc của skill, các lớp nguồn, keyness candidate, evidence limitations và approval gates được giữ riêng. Mọi thay đổi authority, SoD, production workflow, automation, bỏ/giảm control hoặc chấp nhận residual risk cần phê duyệt có thẩm quyền. Báo cáo này không phát hành SOP/RCM chính thức và không giải quyết thay chủ nguồn các mâu thuẫn còn mở.

