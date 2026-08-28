# Phân tích quy trình–rủi ro–kiểm soát

Bản dự thảo để review, chưa phải RCM/SOP được phê duyệt, kết luận kiểm toán hoặc kết luận operating effectiveness (OE). Phạm vi: `PROC-19A`, `PROC-19B`; bằng chứng thực hiện được cung cấp chỉ liên quan B-19/TX-19 ngày 10/07/2026. Dữ liệu truy nguyên: [data.json](/private/tmp/thien-rpc-phase3.xGeed0/P1-U19-V01-R1/data.json).

## 1. Tóm tắt điều hành

Mục tiêu là chỉ dùng tài khoản nhà cung cấp đã xác nhận (`OBJ-19A`) và trả đúng nghĩa vụ được duyệt (`OBJ-19B`). Hai quy trình cần được nhìn xuyên suốt từ thay đổi tài khoản/master data đến sử dụng beneficiary để thanh toán và đối chiếu, không tách việc xác nhận ở hai phòng/bước thành hai lớp bảo vệ độc lập.

- `CTL-SHARED-19` là **một logical control dùng chung**, được gọi ở hai quy trình. SOP-19B xác nhận cùng cấu hình và cơ chế, nên có căn cứ giữ chung ID; không phải chỉ do tên giống nhau.
- Baseline nội bộ `REQ-19 §2` yêu cầu xác nhận thay đổi tài khoản qua kênh độc lập trước lần thanh toán đầu tiên và hồ sơ có locator. Gọi dịch vụ hoặc lưu status chưa tự chứng minh đáp ứng cả hai yêu cầu.
- Checklist B-19 ghi `VERIFIED`, ô nguồn cuộc gọi trống; trace cùng ngày ghi `PENDING_REVIEW` trước phát lệnh; TX-19 đã phát. Trạng thái xác nhận cuối cùng là `Unresolved`. Không chọn checklist hay trace làm nguồn thắng khi chủ nguồn chưa giải thích.
- Có căn cứ ghi nhận thiếu trường/thiếu bằng chứng truy nguyên trong hồ sơ cung cấp và mâu thuẫn status. Chưa đủ để kết luận xác nhận độc lập không diễn ra, toàn bộ hồ sơ không có locator, TX-19 là lần thanh toán đầu tiên, đã trả sai tài khoản, có gian lận hoặc control thất bại trên toàn population.
- Hai control khác được SOP mô tả là đối chiếu PO/nhận hàng/hóa đơn và tách người lập–phát lệnh. Chúng hỗ trợ `OBJ-19B`, nhưng không tự thay thế xác nhận beneficiary qua kênh độc lập.
- `CTL-SHARED-19` là **key-control candidate** cần review theo từng quy trình; chưa có designation được phê duyệt. Không chấm inherent/residual risk, severity hoặc priority vì thiếu phương pháp.
- Thứ tự xử lý đề xuất: hòa giải B-19/TX-19 → làm rõ rule/status/locator và trách nhiệm → kiểm chứng control thanh toán khác → lựa chọn phương án cải tiến trên dữ liệu và ngân sách thực tế. Đây là thứ tự theo dependency, không phải risk rating.

Skill risk-process-control được dùng để giữ một ID control dùng chung, tách observations theo lớp/phạm vi/kỳ và bảo toàn mâu thuẫn khi tạo RCM/action view.

## 2. Nguồn, phạm vi và giới hạn

Nguồn trực tiếp đã đọc: [hồ sơ tổng hợp](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U19-V01/input.md:1>), dòng 1–10. Các locator dưới đây chỉ vị trí trong bản tổng hợp, không phải bằng chứng đã mở bản gốc các tài liệu được nhắc tới.

| Source/locator | Điều nguồn hỗ trợ | Trạng thái và giới hạn |
|---|---|---|
| `OBJ-19A/B`, dòng 2 | Hai business objectives | Theo hồ sơ; không thêm objective tổ chức khác |
| `PROC-19A/B`, dòng 3 | Start/end boundary của hai quy trình | Entity, site, process owner, hệ thống cụ thể, SLA, volume: `Not provided` |
| `REQ-19 §2`, dòng 4 | Yêu cầu nội bộ đã được phê duyệt cho cả hai quy trình: kênh độc lập, trước first payment, có locator | Internal mandate theo hồ sơ, không phải luật/standard bên ngoài; version, ngày hiệu lực, authority cụ thể và hiệu lực tại 10/07/2026 chưa cung cấp |
| `SOP-19A §3`, dòng 5 | Dịch vụ shared; người cập nhật master gọi và lưu status | Chưa có full SOP, version/effective status hoặc specification hệ thống |
| `SOP-19B §4`, dòng 6 | Cùng shared control; gọi trước phát; khác người lập/phát; matching trước lập | Không chứng minh các hoạt động đã thực hiện trên TX-19 |
| `EVD-19A`, dòng 7 | Checklist ký 10/07/2026 cho B-19 ghi `VERIFIED`; ô nguồn cuộc gọi trống | Chưa có locator xác nhận khác hoặc khóa gắn checklist với invocation cụ thể |
| `EVD-19B`, dòng 8 | Trace B-19 ghi `PENDING_REVIEW` trước phát lệnh | Giữ nguyên cảnh báo: chủ nguồn chưa giải thích khác biệt |
| `EVD-19C`, dòng 9 | TX-19 đã phát 10/07/2026 | Giữ nguyên cảnh báo: một trường hợp, không phải full population; phát lệnh khác với settlement/đối chiếu hoàn tất |

Nguồn nêu rõ dữ liệu tổng hợp được phép đọc, dùng AI và lưu/tái phân phối trong phạm vi đã nêu. Không mở rộng quyền này sang nguồn hoặc người nhận khác. Không dùng nguồn ngoài, không chạy OCR, không gọi specialist và không thay đổi dữ liệu hay cấu hình production.

Lớp phân tích:

- `As-Documented`: nội dung REQ/SOP/boundary được cung cấp.
- `As-Designed`: `Not provided`; chưa có evidence xác nhận cấu hình hoặc rule thực tế. Không nâng mô tả SOP thành thiết kế đã kiểm chứng.
- `As-Performed`: các ghi nhận giới hạn ở B-19/TX-19 theo EVD, không suy ra cả kỳ/population.
- `Target-State`: mọi phương án, metric, test procedure và action dưới đây đều là đề xuất chưa phê duyệt.

Confidence của nội dung mô tả nguồn: `Medium`, vì chỉ có bản tổng hợp. Confidence về final verification của B-19: `Unresolved`. `Not provided` là thiếu dữ kiện; không có nghĩa bằng 0, không có control hoặc rủi ro thấp.

## 3. E2E phù hợp và process map có căn cứ

| Mapping ID | Process và E2E phù hợp | Boundary/fit | Không suy rộng |
|---|---|---|---|
| `MAP-19A` | `PROC-19A`: phân đoạn quản trị master data tài khoản trong Supplier-Onboarding-to-Offboarding | Nhận yêu cầu đổi tài khoản → phê duyệt/lưu master data; `partial_match` với vòng đời nhà cung cấp | Không khẳng định đã bao phủ onboarding, due diligence hoặc offboarding |
| `MAP-19B` | `PROC-19B`: Invoice-to-Payment, mở rộng đến đối chiếu sổ | Nhận hóa đơn → duyệt → trả tiền → đối chiếu sổ; `candidate_match` | Chi tiết approval/payment/reconciliation chưa có |
| `MAP-19C` | Giao diện Procure-to-Pay giữa master data nhà cung cấp và thanh toán | Cùng `CTL-SHARED-19` phục vụ cả hai objective và hai process | Chưa map toàn Procure-to-Pay; không có các bước mua hàng upstream ngoài matching được nêu |

Tên E2E là phân loại đề xuất của analyst dựa vào trigger/outcome, không phải ID thư viện chính thức. `reference_library_id/reference_item_id = null`; L0–L5 và taxonomy chính thức của tổ chức: `To be validated`.

| Step ID | Nội dung As-Documented | Performer/control | Căn cứ và khoảng trống |
|---|---|---|---|
| `STEP-19A-01` | Nhận yêu cầu đổi tài khoản | Performer chưa cung cấp | PROC-19A, dòng 3 |
| `STEP-19A-02` | Gọi dịch vụ, lưu status | Người cập nhật master; `CTL-SHARED-19` | SOP-19A §3; chưa biết chính xác trước/sau approval hoặc lưu master |
| `STEP-19A-03` | Phê duyệt/lưu master data | Authority, criteria và evidence chưa cung cấp | PROC-19A, dòng 3 |
| `STEP-19B-01` | Nhận hóa đơn và xử lý phê duyệt trong boundary | Chưa cung cấp | PROC-19B; không tự tạo số cấp duyệt |
| `STEP-19B-02` | Đối chiếu PO/nhận hàng/hóa đơn trước lập lệnh | `CTL-19-MATCH`; performer chưa cung cấp | SOP-19B §4 |
| `STEP-19B-03` | Lập lệnh | Người lập; phía maker của `CTL-19-SOD` | SOP-19B §4 |
| `STEP-19B-04` | Gọi shared control trước phát lệnh | `CTL-SHARED-19`; caller chưa cung cấp | SOP-19B §4; chưa rõ quan hệ thứ tự với bước lập lệnh hoặc rule chặn |
| `STEP-19B-05` | Phát lệnh bởi người khác người lập | Người phát; `CTL-19-SOD` | SOP-19B §4; EVD-19C chỉ hỗ trợ sự kiện TX-19 đã phát |
| `STEP-19B-06` | Trả tiền và đối chiếu sổ | Chưa cung cấp | Chỉ là end boundary; chưa đủ đặc tả để tạo control đối chiếu hiện hành riêng |

Map trên là step register với các quan hệ thứ tự được nguồn hỗ trợ, chưa phải workflow đầy đủ đã xác nhận. Handoff cần xác minh là cách beneficiary/phiên bản tài khoản/status từ master data được gắn vào lệnh thanh toán. Chưa biết system of record, khóa liên kết, đường từ chối, rework, override, SLA hoặc escalation; không tự bổ sung như current state.

Mốc bắt buộc trong REQ-19 là **trước lần thanh toán đầu tiên**, không tự đổi thành trước lưu master data hoặc yêu cầu gọi xác nhận độc lập lại cho mọi hóa đơn.

## 4. Risk, expected controls và current controls

### 4.1 Risk register

Các risk statements dưới đây là suy luận về khả năng xảy ra sự kiện, không phải khẳng định sự cố/gian lận đã xảy ra. Rating và risk owner đều chưa cung cấp.

| Risk ID | Cause → Event → Impact → Objective | Căn cứ/điểm kiểm soát |
|---|---|---|
| `RSK-19-01` | Nếu xác nhận chưa đủ căn cứ hoặc status mâu thuẫn được dùng để phát lệnh → có thể dùng/trả tới tài khoản chưa được xác nhận đúng → thất thoát hoặc không trả đúng nghĩa vụ → OBJ-19A/B | REQ-19; SOP-19A/B; EVD-19A/B/C. STEP-19A-02, STEP-19B-04/05 |
| `RSK-19-02` | Nếu matching/phê duyệt/tách lập–phát không thực hiện đúng → lệnh có thể không phù hợp nghĩa vụ hoặc kết quả ghi nhận/đối chiếu sai → chi sai/thừa, sổ không khớp nghĩa vụ → OBJ-19B | OBJ/PROC-19B, SOP-19B. Đây là scenario có điều kiện, chưa có deviation của matching/SoD |
| `RSK-19-03` | Ô nguồn cuộc gọi trống và status chưa hòa giải → không truy nguyên được quyết định xác nhận đúng đối tượng/thời điểm → reliance thiếu căn cứ, không chứng minh yêu cầu hồ sơ → OBJ-19A/B | REQ-19; EVD-19A/B. Khác RSK-19-01 ở event mất khả năng truy nguyên, không cộng gộp điểm rủi ro |
| `RSK-19-04` | Hai điểm gọi cùng dịch vụ/cấu hình → một lỗi status/gián đoạn có thể tác động cả hai process → cùng dựa vào kết quả sai hoặc trì hoãn/đi vòng xử lý → OBJ-19A/B | SOP-19A/B; common-mode hypothesis, chưa có incident hoặc SPOF được xác nhận |

### 4.2 Expected baseline và control objectives

| Baseline ID | Control objective | Expected outcome và nguồn | Current/candidate control |
|---|---|---|---|
| `CBL-19-01` | `COBJ-19-01` | Xác nhận thay đổi tài khoản bằng kênh độc lập trước first payment — REQ-19 §2 | `CTL-SHARED-19` là cơ chế được mô tả; đủ coverage thực tế chưa xác minh |
| `CBL-19-02` | `COBJ-19-02` | Hồ sơ có locator — REQ-19 §2 | Cùng `CTL-SHARED-19`; chi tiết liên kết phiên bản/status và kiểm tra khả năng truy xuất là đề xuất triển khai |
| `CBL-19-03` | `COBJ-19-03` | Matching PO/nhận hàng/hóa đơn trước lập — SOP-19B §4 | `CTL-19-MATCH` |
| `CBL-19-04` | `COBJ-19-03` | Người phát khác người lập — SOP-19B §4 | `CTL-19-SOD` |
| `CBL-19-05` | `COBJ-19-02/04` | Status đáng tin cậy và xử lý an toàn dependency chung | Analyst proposal, không baseline pháp lý/standard; `CTL-19-MON` chỉ Target-State |

REQ-19 là căn cứ nội bộ được cung cấp. SOP-19B là baseline thiết kế được tài liệu mô tả; approval/effective status của SOP chưa cung cấp. Không gọi phương án mới “standard-derived”, “compliant” hoặc chứng nhận tuân thủ. Yêu cầu xác nhận/locator khác với cách triển khai form bắt buộc, khóa phiên bản, rule chặn hay workflow; các cách triển khai này cần phê duyệt.

### 4.3 Control observations — không ghi đè nguồn

| Observation ID | Logical control/layer/scope/kỳ | Nội dung được giữ nguyên | Đánh giá giới hạn |
|---|---|---|---|
| `OBS-19-DA` | CTL-SHARED-19; As-Documented; PROC-19A; kỳ hiệu lực chưa cung cấp | Người cập nhật master gọi dịch vụ và lưu status | Hướng tới mục tiêu xác nhận; thiếu mô tả kênh, locator, criteria và exception trong đoạn đọc |
| `OBS-19-DB` | CTL-SHARED-19; As-Documented; PROC-19B; kỳ hiệu lực chưa cung cấp | Cùng cấu hình/cơ chế, gọi trước phát lệnh | Timing của điểm gọi có căn cứ; chưa biết service completion hoặc release gate |
| `OBS-19-PA` | CTL-SHARED-19; As-Performed; checklist B-19; 10/07/2026 | `VERIFIED`; nguồn cuộc gọi trống | Chưa xác định checklist thuộc invocation A hay B; không tự gán qua tên EVD |
| `OBS-19-PB` | CTL-SHARED-19; As-Performed; trace B-19 trước phát lệnh; 10/07/2026 | `PENDING_REVIEW`; khác biệt chưa giải thích | Final state `Unresolved`; không coi trace tự động đáng tin hơn checklist |
| `OBS-19-DM` | CTL-19-MATCH; As-Documented; PROC-19B; kỳ chưa cung cấp | Đối chiếu ba nguồn trước lập | Có theoretical coverage về nghĩa vụ; owner, dung sai, xử lý mismatch, evidence chưa có |
| `OBS-19-DS` | CTL-19-SOD; As-Documented; PROC-19B; kỳ chưa cung cấp | Người phát khác người lập | Có thiết kế process-role; actual users/access và vận hành chưa đánh giá |
| `OBS-19-TS` | CTL-SHARED-19; Target-State; hai process; chưa hiệu lực | Củng cố locator, independent confirmation và eligibility/exception handling | Proposal, không tính vào current protection |
| `OBS-19-TM` | CTL-19-MON; Target-State; hai process; chưa hiệu lực | Đối soát/monitor status và xử lý bất nhất | Control mới đề xuất; không phải control hiện có hoặc backup đã chứng minh |

`OBS-19-TX` là observation của step phát lệnh từ EVD-19C, **không** phải thêm một observation “shared control đã thành công”.

Đối với phần vận hành chưa đủ evidence: `assessment_status = Not assessed`, `evidence_status = Insufficient evidence`. Những trạng thái này không xóa `design_assessment` riêng của mỗi observation trong dữ liệu.

### 4.4 Key-control rationale, alternatives, SoD và dependency

`CTL-SHARED-19` là key candidate ở cả hai scope As-Documented, nhưng rationale và approval được giữ riêng:

- Trong PROC-19A: cơ chế xác nhận chính được mô tả cho dữ liệu tài khoản sẽ dùng ở thanh toán; liên kết REQ-19 → COBJ-19-01/02 → RSK-19-01/03.
- Trong PROC-19B: được gọi ngay trước phát lệnh, nên có reliance trực tiếp vào kết quả beneficiary. Rationale này không chứng minh điều kiện “đã xác nhận” thực sự được enforced.
- Không có alternative tương đương được chứng minh. Matching kiểm tra căn cứ nghĩa vụ; SoD tách người lập/phát; cả hai chưa chứng minh kênh liên hệ beneficiary độc lập. Hai điểm gọi cùng dịch vụ cũng không tự là hai controls độc lập.
- Designation, phương pháp đánh giá significant risk, reviewer và approver: `Not provided`. Không áp một approval giả cho mọi process/kỳ/layer. CTL-19-MATCH/SOD không mặc nhiên được đánh dấu key; vai trò của chúng với risk thanh toán cần đánh giá tiếp.

Không đủ căn cứ bỏ một điểm gọi shared vì “trùng”: điểm gọi trước phát có thể kiểm tra tình trạng mới hơn, nhưng incremental coverage, cache/refresh và phiên bản chưa rõ. Chỉ rationalize sau coverage review và approval.

SoD: nguồn cho thấy yêu cầu process-role separation; system-access và actual-user đều chưa cung cấp. Người cập nhật master đồng thời gọi dịch vụ không tự chứng minh họ tự xác nhận hoặc có actual conflict.

`DEP-19-01`: dependency dịch vụ chung có căn cứ. Backup, capacity, substitution lead time, recovery capability, tolerance, knowledge và workaround chưa cung cấp; `SPOF = To be validated`, không phải SPOF đã xác nhận.

## 5. So sánh baseline–current, gaps và rủi ro nếu giữ nguyên

| Comparison / gap | Nhận định và layer | Confidence / điều cần xác minh |
|---|---|---|
| `CMP-19-02 / GAP-19-01` | Evidence limitation tại hồ sơ B-19: ô nguồn cuộc gọi trống, chưa có locator khác được cung cấp; so với REQ-19 yêu cầu locator | Medium cho trường trống; chưa chứng minh toàn hồ sơ không có locator. Cần bản gốc và nguồn truy xuất được |
| `CMP-19-01/02 / GAP-19-02` | Observation mâu thuẫn evidence: VERIFIED/PENDING_REVIEW, cùng với sự kiện lệnh đã phát | `Unresolved`. Cần chronology, semantics, beneficiary/account version, invocation, first-payment và release/settlement |
| `CMP-19-01/02 / GAP-19-03` | Documentation gap trong các đoạn SOP đã đọc: chưa mô tả đủ độc lập, locator, release criteria, PENDING/override, owner, retention, escalation | Medium về phạm vi tài liệu. Design gap chỉ là potential cho đến khi kiểm tra full specification và alternative controls |
| `CMP-19-03 / GAP-19-04` | Evidence limitation cho matching, approval, actual maker/releaser và payment/reconciliation | Không phải observed deviation. Cần hồ sơ giao dịch/quyền; EVD-19C không lấp phần thiếu |
| `CMP-19-04 / OPP-19-01` | Design opportunity để làm rõ common-mode dependency/monitoring/backup | Không tạo Missing Control giả hoặc kết luận SPOF từ dữ liệu thiếu |

Root cause của các issue chưa được xác nhận. Không tự gọi chúng là confirmed audit findings; không đưa compliance conclusion lịch sử khi chưa xác minh đầy đủ authority/effective scope và evidence liên quan.

| No-change ID | Cause → event → impact và existing protection | Exposure/uncertainty còn lại |
|---|---|---|
| `NCS-19-01` → GAP-19-01/02/03 | Nếu tiếp tục dùng status chưa hòa giải, hồ sơ chưa truy nguyên → có thể cho dùng/phát lệnh với xác nhận thiếu căn cứ → trả sai beneficiary hoặc không chứng minh yêu cầu nội bộ. Shared, matching, SoD là protection được tài liệu mô tả | Shared có performed evidence mâu thuẫn; matching/SoD không chứng minh thay thế độc lập. Chưa biết final state, actual loss hoặc first-payment flag. Liên kết RSK-19-01/03, OBJ-19A/B |
| `NCS-19-02` → GAP-19-04 | Nếu matching/authority/SoD thực tế không đủ → có thể phát hoặc ghi nhận sai nghĩa vụ → chi sai/thừa/sổ sai. Matching và separation được SOP nêu | Đây là hypothesis từ evidence limitation, không phải kết luận controls đang yếu. Liên kết RSK-19-02, OBJ-19B |
| `NCS-19-03` → OPP-19-01 | Nếu dịch vụ chung có lỗi/gián đoạn → hai process cùng bị ảnh hưởng → kết quả xác nhận không đáng tin hoặc trì hoãn | Mitigation/backup chưa cung cấp, không đồng nghĩa không tồn tại. Chưa xác định SPOF. Liên kết RSK-19-04, OBJ-19A/B |

Không tự đặt xác suất, số tiền tổn thất, risk score hay horizon; `horizon = null`. Target-State chưa triển khai không được tính là protection hiện tại.

## 6. Cải tiến và action view

### Phương án Target-State để quyết định

| Option | Thiết kế đề xuất | Lợi ích, trade-off và dependency |
|---|---|---|
| A — Minimum-control proposal, compliance unverified | Review thủ công có kiểm soát để đối chiếu xác nhận độc lập/locator trước first payment; giữ chờ khi thiếu/bất nhất; lưu disposition và authority | Ít thay đổi hệ thống hơn nhưng tăng workload và phụ thuộc người. Chỉ có thể đáp ứng nội dung REQ đã cung cấp khi rule/evidence/authority được xác nhận; chưa là kết luận compliant |
| B — Cân bằng control và hiệu quả | Một hồ sơ xác nhận trung tâm có khóa beneficiary/phiên bản/case, evidence locator và history; hai điểm gọi dùng cùng định nghĩa, kiểm tra điều kiện sử dụng và route exception rõ | Giảm nhập lại/diễn giải status; cần chốt ownership, data lineage, semantics, độ mới và access. Chưa có business case/ngân sách để quyết định triển khai |
| C — Automation-first có điều kiện | Tự động eligibility check và cảnh báo bất nhất, kiểm soát change/access, thử negative cases và fallback được phê duyệt | Có thể giảm kiểm tra lặp khi volume phù hợp; rủi ro tự động lan truyền dữ liệu/rule sai và common-mode dependency. Chỉ xem xét sau khi dữ liệu/rules ổn định và pilot được xác minh |

Chi phí, ngân sách, implementation time, staffing/capacity và residual-risk rating của cả ba option: `Not provided/Not assessed`; không có ước tính định lượng. Ưu tiên ACT-19-01 và làm rõ rule trước; B là phương án để thẩm định, không phải lựa chọn đã phê duyệt.

Không bỏ điểm gọi, đổi authority/SoD/access, triển khai production, miễn yêu cầu xác nhận hoặc chấp nhận residual risk chỉ từ đề xuất này. Approval ngoại lệ không mặc nhiên cho phép bỏ REQ-19.

| Action → recommendation | Liên kết | Việc cần làm / tiêu chí bàn giao | Dependency / approval |
|---|---|---|---|
| `ACT-19-01 → REC-19-01` | GAP-19-01/02; CMP-19-01/02; NCS-19-01 | Thu original checklist/trace, locator, kênh độc lập, version/case/invocation, timezone/history, first-payment marker và lệnh/settlement; hòa giải bằng chứng theo thời điểm | Không có action tiên quyết. Chủ nguồn và authority phù hợp phải phân định; không ghi đè raw status hoặc tạo evidence hồi tố như thể đã có trước lệnh |
| `ACT-19-02 → REC-19-02` | GAP-19-01/02/03; CMP-19-01/02; NCS-19-01 | Chốt specification của shared control: evidence/locator, eligibility, PENDING/mismatch/exception, owner và retention; sửa SOP/form nếu cần sau approval. Acceptance: requirement–rule–evidence map và walkthrough/UAT đủ các nhánh | Phụ thuộc ACT-19-01. Phê duyệt target state, role/authority, key designation và system change trước áp dụng |
| `ACT-19-03 → REC-19-03` | GAP-19-04; CMP-19-03; NCS-19-02 | Thu hồ sơ matching/phê duyệt, user/access lịch sử, lập–phát, bank/ledger/reconciliation; phân biệt design với case evidence | Có thể làm song song. Mọi OE testing cần assurance owner duyệt objective, methodology, population và sampling |
| `ACT-19-04 → REC-19-04` | OPP-19-01; DEP-19-01; CMP-19-04; NCS-19-03 | Xác minh dependency/substitute/capacity/tolerance; đánh giá option, chỉ pilot monitoring/automation khi data/rules phù hợp | Design/pilot phụ thuộc ACT-19-01/02. Authority phải phê duyệt resources, option và residual-risk acceptance |

Với mọi action: owner/accountable executive, due date và ngân sách = `Not provided`; `target_date = null`; status = `Draft`; closure evidence trống. Các nhóm tham gia gợi ý trong data.json không phải người được giao việc hoặc authority đã được xác nhận.

## 7. Dữ liệu RCM, kiểm chứng và các quyết định còn mở

[data.json](/private/tmp/thien-rpc-phase3.xGeed0/P1-U19-V01-R1/data.json) giữ các object và quan hệ để tạo view: objective, process, step, source, requirement, risk, control objective, logical control, observation, baseline, comparison, gap, dependency, recommendation, action và no-change scenario.

Grain RCM là **risk–control–observation–scope**, không phải “mỗi dòng là một control”. Dữ liệu có 4 risks, 3 current logical controls, 1 target-only monitoring proposal, 8 control observations và 18 association rows. `CTL-SHARED-19` chỉ đếm một lần; hai documented points, hai evidence records và nhiều objective/risk links không nhân số control hoặc rating.

| Risk-centric view | Controls và lớp | Comparison / action |
|---|---|---|
| RSK-19-01 | CTL-SHARED-19: documented ở A/B, evidence mâu thuẫn, target enhancement tách riêng | CMP-19-01; ACT-19-01/02 |
| RSK-19-02 | CTL-19-MATCH và CTL-19-SOD: As-Documented, chưa có performed evidence | CMP-19-03; ACT-19-03 |
| RSK-19-03 | CTL-SHARED-19: documented/evidence/target tách lớp; CTL-19-MON: Target-State only | CMP-19-02; ACT-19-01/02 |
| RSK-19-04 | Current shared dependency có căn cứ, mitigation chưa cung cấp; CTL-19-MON chỉ hỗ trợ monitoring ở Target-State, không thay thế recovery | CMP-19-04; ACT-19-04 |

Khi tạo control-centric view, join bằng `control_id`, giữ từng `control_observation_id`; không chọn một status “mới nhất” để xóa conflict. Khi tạo action view, join action → recommendation → gap/opportunity → comparison → no-change; giữ nguyên owner/date/null. Bản RCM chính thức vẫn cần approval.

Các test attributes chỉ là thiết kế dự kiến, chưa thực thi:

- `TST-19-01`: occurrence, độc lập, đúng beneficiary/version, locator và confirmation trước first-payment event.
- `TST-19-02`: completeness/reliability của history, status semantics, timestamps/timezone, khóa liên kết và exception/override.
- `TST-19-03`: matching, approval, distinct actual users/effective access đúng kỳ và kết quả payment/reconciliation.

Không chốt sample size. Nếu mở rộng đánh giá, trước hết cần population/kỳ, data-reliability work, phương pháp được duyệt và thủ tục đã thực hiện; kết luận OE chính thức thuộc assurance owner có thẩm quyền.

Metric proposals, chưa có dữ liệu để tính:

| Metric | Định nghĩa đề xuất | Giới hạn/response |
|---|---|---|
| `MET-19-01 — KCI` | First-payment cases sau đổi tài khoản có xác nhận độc lập đúng phiên bản và locator trước mốc yêu cầu / tổng first-payment cases sau đổi trong kỳ | Cần đối soát population và evidence; investigate hồ sơ thiếu, không suy tỷ lệ toàn bộ từ B-19 |
| `MET-19-02 — KRI` | Đếm lệnh trong scope có status bất nhất hoặc PENDING tại mốc kiểm tra được định nghĩa | Là tín hiệu cần triage, không tự là vi phạm/control failure |
| `MET-19-03 — KPI` | Thời điểm đủ điều kiện theo rule được duyệt trừ thời điểm nhận yêu cầu đổi tài khoản | Đo queue/rework/capacity; không bỏ control để giảm cycle time |

Metric owner, cadence, target, threshold và escalation: `To be validated/Not provided`. Công thức chỉ dùng sau khi khóa semantics, completeness và timezone; không đặt số 0 khi denominator hoặc dữ liệu chưa có.

Cần quyết định/bổ sung trước khi kết luận riêng B-19 hoặc phê duyệt triển khai:

1. Chủ nguồn giải thích thế nào về VERIFIED/PENDING_REVIEW; có locator, independent-channel evidence và timeline đúng version/case không?
2. TX-19 có phải lần thanh toán đầu tiên sau đổi tài khoản, đã settlement và đối chiếu chưa; policy/version nào có hiệu lực ngày đó?
3. Ai có authority phê duyệt design, key designation, exception và risk acceptance; phương pháp risk, nguồn lực và due date nào được duyệt?
4. Actual users/access, population và dependency/backup evidence là gì?

Các câu hỏi này giới hạn những kết luận phụ thuộc dữ kiện còn thiếu; không làm mất phần phân tích và các đề xuất dự thảo có căn cứ ở trên.
