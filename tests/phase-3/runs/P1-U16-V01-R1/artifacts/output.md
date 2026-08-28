# Phân tích quy trình nhận hàng trả

Đã phối hợp thực tế với Thien-Skill-Document-Evidence và đọc toàn bộ một trang scan. Có thể xác định luồng **nhận yêu cầu → kiểm đếm → duyệt → hoàn tiền**, nhưng **người duyệt hoàn tiền bị che, chưa thể xác định**. Không suy đoán người duyệt, thẩm quyền hay nội dung bên dưới vùng che.

Đây là bản nháp **As-Documented của bản được cung cấp**, không phải quy trình đã được tổ chức xác nhận đang hiệu lực. Các đề xuất dưới đây thuộc **Target-State — cần phê duyệt**. Không có hồ sơ giao dịch hoặc kiểm thử vận hành: `assessment_status: Not assessed`, `evidence_status: Insufficient evidence` đối với As-Performed.

## 1. Nguồn và cách đọc

Nguồn `SRC-RET-01`: :codex-file-citation{path="/Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U16-V01/input.pdf" purpose="source"}, trang 1. Nhãn đầu trang là “SYNTHETIC SCAN - SOP-SYN-16”; ngay dưới ghi “Dữ liệu tổng hợp; được phép dùng AI.” Đây là mô tả của nguồn, không phải bằng chứng giao dịch thực tế hay xác nhận hiệu lực SOP.

- Bản nguồn được giữ nguyên; bản render và dữ liệu dẫn xuất lưu riêng. SHA-256 nguồn khớp giữa hai lượt kiểm tra; hash không xác thực tài liệu.
- Native text không có nội dung; đã render bằng Poppler cục bộ và đọc ảnh bằng khả năng xem ảnh của phiên (`PLATFORM_NATIVE`). Không chạy OCR tiếng Việt, không dùng dịch vụ OCR bên ngoài, không cài mới hay upload tài liệu qua connector.
- Ánh xạ giữ nguyên: `document_id=doc-9182b8b70c2027a5c8167536-0001`; `evidence_id=EV-P1-U16-V01-R1-001`; `extraction_run_id=P1-U16-V01-R1-DE`.
- Version, ngày hiệu lực, chủ sở hữu/phê duyệt SOP, đơn vị và kỳ áp dụng: `Not provided`; độ đầy đủ so với SOP gốc chưa xác minh. Phân loại bảo mật chưa được cung cấp; gói xử lý được giữ như tài liệu mật.
- Confidence phân tích As-Documented từ phần đọc rõ: **Medium**, vì chỉ có một nguồn scan chưa được người có thẩm quyền xác nhận; confidence trích xuất được giữ riêng trong gói Document–Evidence. Ô bị che: **Unresolved**, không có candidate value. Việc hai agent cùng đọc một ảnh không tạo hai nguồn độc lập.

## 2. Luồng quy trình — As-Documented

Mục tiêu `OBJ-RET-01`: “đối chiếu hàng và hoàn tiền đúng” — trang 1, dòng “Mục tiêu”. Phạm vi đọc được của `PROC-RET-01` bắt đầu ở nhận yêu cầu và kết thúc tại bước hoàn tiền. Chưa đủ căn cứ xác định toàn bộ vòng đời trả hàng hay cấp L0–L5; không tự thêm vận chuyển, hạch toán hoặc hệ thống xử lý. Các mã RET bên dưới là mã phân tích của bản nháp, không phải mã chính thức trong SOP.

| Bước | Hoạt động và bàn giao đọc được | Vai trò/hồ sơ theo nguồn | Locator |
|---|---|---|---|
| STEP-RET-01 | Nhận yêu cầu, tiếp đến kiểm đếm | Người nhận và hồ sơ đầu vào chi tiết: Not provided | Trang 1, chuỗi bước; DE-F05 |
| STEP-RET-02 | Kiểm đếm, tiếp đến duyệt | Nhân viên kho; Phiếu nhận | Trang 1, bảng, dòng dữ liệu 1; DE-F06–DE-F08 |
| STEP-RET-03 | Duyệt hoàn tiền, trước bước hoàn tiền | Người thực hiện: **OBSCURED / HUMAN_REVIEW_REQUIRED**; hồ sơ: Ghi nhận duyệt | Trang 1, bảng, dòng dữ liệu 2; DE-F09–DE-F11 |
| STEP-RET-04 | Hoàn tiền | Người thực hiện, hệ thống, căn cứ số tiền và chứng từ hoàn: Not provided | Trang 1, chuỗi bước; DE-F05 |

Ngoại lệ được ghi riêng: **“giữ hàng để làm rõ chênh lệch”** — trang 1, dưới bảng, DE-F12. Nguồn không nêu người giải quyết, điều kiện đóng, nhánh từ chối, thời hạn hay điểm quay lại luồng. **Giữ hàng không tự chứng minh đã chặn hoàn tiền.**

Yêu cầu hồ sơ xuyên suốt: **“Lưu hồ sơ theo mã yêu cầu trả hàng”** — trang 1, dòng cuối, DE-F13. Nơi lưu, thời hạn lưu và người chịu trách nhiệm chưa được mô tả.

## 3. Rủi ro và kiểm soát

Các rủi ro dưới đây là **kịch bản suy luận**, chưa phải sự kiện hoặc sai phạm đã xảy ra; confidence **Low** đối với việc chúng có tồn tại trong thực tế, cần walkthrough và hồ sơ xác nhận. Tất cả hướng về OBJ-RET-01. Không chấm điểm inherent/residual risk khi chưa có phương pháp được phê duyệt.

| Liên kết rủi ro → mục tiêu kiểm soát | Kiểm soát được mô tả — As-Documented | Đánh giá thiết kế/bằng chứng trong phạm vi nguồn |
|---|---|---|
| **RSK-RET-01:** Nếu kiểm đếm thiếu hoặc không có căn cứ đối chiếu, số lượng hàng trả có thể sai, kéo theo hoàn tiền sai. **COBJ-RET-01:** Số lượng hàng trả được ghi nhận chính xác, có căn cứ đối chiếu. | **CTL-RET-01:** Nhân viên kho kiểm đếm; hồ sơ được nêu là Phiếu nhận. Nguồn: DE-F06–DE-F08, bảng dòng 1. | Có actor, action, vị trí trước duyệt và loại hồ sơ. Chưa nêu đối chiếu với tài liệu nào, trường phải kiểm tra hoặc cách ghi chênh lệch. Phiếu nhận là hồ sơ SOP yêu cầu, **chưa được cung cấp dưới dạng bằng chứng đã thực hiện**. |
| **RSK-RET-02:** Nếu thẩm quyền/tiêu chí chưa được xác minh hoặc bước duyệt bị bỏ qua, hoàn tiền không phù hợp có thể phát sinh, gây thất thoát và sai kết quả hoàn tiền. **COBJ-RET-02:** Chỉ hoàn tiền trên căn cứ và phê duyệt phù hợp. | **CTL-RET-02:** Duyệt trước hoàn tiền; có “Ghi nhận duyệt”. Nguồn: DE-F05, DE-F09–DE-F11. | Trình tự có thể hỗ trợ phòng ngừa, nhưng ô người duyệt bị che. Tiêu chí, hạn mức, bằng chứng thẩm quyền, cơ chế từ chối và khả năng vượt bước chưa rõ. **Không thể chốt RACI, key-control status hoặc kết luận xung đột SoD.** |
| **RSK-RET-03:** Nếu chênh lệch không được giải quyết trước quyết định liên quan, có thể hoàn tiền sai hoặc giữ hàng kéo dài. **COBJ-RET-03:** Chênh lệch được xử lý và có quyết định rõ trước khi tiếp tục. | **CTL-RET-03:** Giữ hàng để làm rõ chênh lệch. Nguồn: DE-F12, dòng ngoại lệ. | Đây là bảo vệ được mô tả đối với hàng đang có chênh lệch; chưa đủ để xác nhận kiểm soát đối với dòng tiền. Actor, hồ sơ xử lý, điều kiện giải phóng và escalation: Not provided. |
| **RSK-RET-04:** Nếu hồ sơ không liên kết theo yêu cầu trả hàng, có thể không truy được căn cứ kiểm đếm–duyệt–hoàn tiền, gây khó đối soát và sửa sai. **COBJ-RET-04:** Mỗi yêu cầu truy nguyên được hồ sơ liên quan. | **CTL-RET-04:** Lưu hồ sơ theo mã yêu cầu trả hàng. Nguồn: DE-F13, dòng cuối. | Có nguyên tắc liên kết hồ sơ; chưa xác định bộ hồ sơ bắt buộc, kho lưu, quyền truy cập, retention và cách chứng minh đã lưu đầy đủ. Đây không phải bằng chứng rằng hồ sơ thực tế đã đầy đủ. |

Chưa có căn cứ phân loại kiểm soát nào là **Key Control đã được phê duyệt**. Các điểm chưa rõ ở bảng trên là **giới hạn nguồn và documentation questions**, không chứng minh kiểm soát không tồn tại, vận hành thất bại hay là audit finding. Bước nhận yêu cầu/hoàn tiền tự thân cũng chưa đủ mô tả để coi là một kiểm soát riêng.

## 4. Điểm cần người xác nhận và đề xuất

Giữ nguyên hàng đợi của Document–Evidence:

| Review ID | Vấn đề và nguồn | Xác nhận cần có trước khi dùng chính thức |
|---|---|---|
| **DE-HR-01 → DE-F10** | Critical field: ô Người thực hiện, dòng Duyệt hoàn tiền, trang 1 bị che; giá trị chưa xác định | Bản rõ hơn hoặc bản chép có xác nhận của chủ tài liệu; đối chiếu văn bản thẩm quyền đúng phiên bản/kỳ. Không mặc định là quản lý, kế toán trưởng hoặc người kiểm đếm. |
| **DE-HR-02 → DE-F14–DE-F20** | Chưa rõ độ đầy đủ, version, ngày, đơn vị; trang không nêu vai trò nhận yêu cầu/hoàn tiền, ngưỡng duyệt và thời hạn lưu | Xác nhận bản đủ/đúng phiên bản, owner và phạm vi sử dụng; bổ sung nguồn cho các vai trò/ngưỡng/thời hạn trước triển khai. Nhãn SOP-SYN-16 và metadata không thay thế thông tin hiệu lực. |
| **DE-HR-03** | Toàn bộ transcription chỉ mới được agent đọc, chưa human validation | Người có thẩm quyền đối chiếu trang nguồn và xác nhận nội dung trước phát hành hoặc sử dụng để cấu hình/phê duyệt quy trình. |

Đề xuất **Target-State — draft**, dựa trên mục tiêu/rủi ro của tài liệu, **không phải yêu cầu từ một tiêu chuẩn ngoài đã xác minh**:

1. **Làm rõ CTL-RET-01/02:** bổ sung căn cứ đối chiếu hàng, cách xác định số tiền, người có thẩm quyền, tiêu chí duyệt/từ chối và bằng chứng cần lưu. Chỉ điền hạn mức sau khi nhận được quy định đã phê duyệt.
2. **Hoàn chỉnh CTL-RET-03:** quy định rõ người xử lý chênh lệch, điều kiện chuyển bước, việc có chặn hoàn tiền hay không, căn cứ giải phóng hàng và escalation. Đây là bổ sung đề xuất, không phải nhánh hiện trạng đã được xác nhận.
3. **Hoàn chỉnh CTL-RET-04:** xác định bộ hồ sơ liên kết theo mã yêu cầu, gồm căn cứ nhận/kiểm đếm, ghi nhận duyệt, xử lý ngoại lệ và chứng từ hoàn tiền phù hợp; owner, nơi lưu và retention cần được phê duyệt.
4. **Kiểm chứng thực tế trước kết luận vận hành:** walkthrough một yêu cầu có mã định danh và các hồ sơ tương ứng; xem thêm đường xử lý chênh lệch khi có. Đây là đề nghị thu thập bằng chứng, không phải kiểm thử đã chạy hay cỡ mẫu để kết luận operating effectiveness.

Nếu giữ nguyên các phần mô tả chưa rõ, những bảo vệ đã ghi — kiểm đếm, duyệt, giữ hàng và liên kết hồ sơ — vẫn chưa đủ căn cứ để đánh giá độ bao phủ, thẩm quyền và cách xử lý ngoại lệ. Kịch bản RSK-RET-01–04 vì vậy cần được kiểm chứng; chưa có dữ liệu xác suất, tổn thất hoặc mức rủi ro còn lại.

Người chịu trách nhiệm hành động/phê duyệt cụ thể và hạn hoàn thành: **To be validated**, không tự giao cho nhân viên kho hoặc người duyệt chưa đọc được.

## Hồ sơ bàn giao

Bản trích xuất và human-review queue: [extraction.md](/private/tmp/thien-rpc-phase3.xGeed0/P1-U16-V01-R1/document-evidence/extraction.md). Dấu vết chuyên gia: [tool-trace.json](/private/tmp/thien-rpc-phase3.xGeed0/P1-U16-V01-R1/document-evidence/tool-trace.json). [Bàn giao thực tế](/private/tmp/thien-rpc-phase3.xGeed0/P1-U16-V01-R1/specialist-dispatch.json) giữ task/handoff IDs và phạm vi được phép.

Cảnh báo kỹ thuật được bảo toàn: dò byte ban đầu gắn cờ JavaScript, trong khi pdfinfo báo không có JavaScript và pypdf không tìm thấy active-content key khi kiểm tra cấu trúc tĩnh. Không thực thi nội dung chủ động; khác biệt này nằm trong trace, không phải kết luận xác thực hoặc kiểm định malware.

**Trạng thái: bản nháp để người có thẩm quyền review; phần vai trò duyệt vẫn Unresolved.**
