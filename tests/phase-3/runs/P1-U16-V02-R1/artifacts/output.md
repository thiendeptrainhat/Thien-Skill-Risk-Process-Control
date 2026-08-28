# Phân tích sơ bộ quy trình nhận hàng trả

Packet cho phép nhận diện mục tiêu đối chiếu số lượng và hoạt động trưởng ca xem xét. **Chưa đủ căn cứ xác định người có quyền duyệt hoàn tiền hoặc kết luận kiểm soát vận hành hiệu quả.** Ô “G... đốc” phải được con người xác nhận trước khi dùng để kết luận thẩm quyền.

## 1. Phạm vi và nguồn

Đây là phân tích phần nội dung được cung cấp, không phải đánh giá toàn bộ tài liệu gốc. Theo skill risk-process-control, tôi tách mô tả trong packet (`As-Documented`, chưa xác minh) khỏi đề xuất (`Target-State`, draft), và giữ phần thẩm quyền chưa đọc rõ là `Unresolved`.

| Thuộc tính | Nội dung giữ từ nguồn |
|---|---|
| Định danh | `packet_id: SYN-PACKET-16`; `extraction_run_id: SYN-EXTRACT-16`; `source_id: SRC-SCAN-16`; `document_id: DOC-16` |
| Bản chất, phương pháp | Packet hư cấu, consumer-only; `method: synthetic_manual_transcription`. Không phải kết quả Document-Evidence/OCR thật; không gọi specialist hoặc chạy OCR trong phân tích này. |
| Điều kiện sử dụng | `source_access_and_ai_use_conditions: được phép đọc, dùng AI và lưu trong bộ test; không có dữ liệu thật` |
| Coverage | Trang 1 đầy đủ **phần mục tiêu**; trang 2 bảng phê duyệt chỉ đọc được một phần. Không suy rằng toàn bộ trang 1 hoặc tài liệu đã được đọc đầy đủ. |
| Cảnh báo | “chữ mờ ở người duyệt; chưa xác minh phân quyền” |
| Review nguồn | `review_status: UNVERIFIED` |
| Metadata còn thiếu | Phiên bản, ngày hiệu lực, chủ sở hữu tài liệu, phạm vi đơn vị và kỳ áp dụng: `Not provided`. |

Chỉ đọc packet văn bản; không kiểm tra ảnh scan gốc. Độ tin cậy đối với mô tả tài liệu gốc: **Low**, vì transcription chưa được xác minh. `As-Designed` được xác nhận và `As-Performed`: `Not provided`. Bản phân tích: draft, chưa được người có thẩm quyền review/phê duyệt.

## 2. Mục tiêu và phần quy trình có thể dựng

Mục tiêu được chép tại `SRC-SCAN-16 / DOC-16, trang 1, mục 1`: “Quy trình nhận hàng trả nhằm đối chiếu số lượng và quyết định hoàn tiền.” Trạng thái trường: `TRANSCRIBED`.

Ranh giới phân tích tạm thời là phần nhận hàng trả phục vụ quyết định hoàn tiền; trigger chi tiết, đầu vào đối chiếu và toàn bộ đường đi đến quyết định chưa được mô tả. Thực chi hoàn tiền và đối soát sau chi chưa có dữ liệu, không tự thêm thành bước hiện hành. Chưa đủ căn cứ gán cấp L0–L5 hoặc xác nhận đây là E2E hoàn chỉnh.

| Nội dung trong packet | Diễn giải có giới hạn | Layer, locator và trạng thái |
|---|---|---|
| “Nhân viên nhận ghi số lượng” | Có mô tả hoạt động ghi số lượng. Chưa biết cách kiểm đếm, nguồn đối chiếu, biểu mẫu hay hệ thống. Ghi dữ liệu tự thân chưa đủ chứng minh một control. | `As-Documented`; trang 2, bảng 1, hàng 1; `TRANSCRIBED`; Low |
| “trưởng ca xem xét” | Có mô tả hoạt động review; chưa rõ đối tượng, tiêu chí, thời điểm, dấu vết và cách xử lý chênh lệch. Không đồng nhất “xem xét” với “phê duyệt hoàn tiền”. | `As-Documented`; cùng hàng 1; `TRANSCRIBED`; Low |
| Ô Người duyệt: `raw: 'G... đốc'` | `normalized: null`; chức danh, phạm vi quyền và quan hệ với trưởng ca: `Unresolved`. Không suy đoán từ phần chữ còn đọc được. | Trang 2, bảng 1, hàng 2, ô Người duyệt; `evidence_id: UP-EVD-16-02`; `HUMAN_REVIEW_REQUIRED` |

Nguồn của cả ba dòng là `SRC-SCAN-16 / DOC-16`, tiếp nhận qua `SYN-PACKET-16 / SYN-EXTRACT-16`. ID `UP-EVD-16-02` là định danh upstream của trường cần review, **không phải bằng chứng một lần phê duyệt đã xảy ra**. Trình tự đầy đủ, handoff, nhánh từ chối/ngoại lệ, owner và hệ thống chưa xác định.

## 3. Rủi ro và kiểm soát

Các rủi ro dưới đây là **suy luận có điều kiện**, chưa phải sự cố hoặc thiếu sót vận hành được chứng minh. Mục tiêu kiểm soát và cách hoàn thiện là đề xuất analyst (`Target-State`, draft), không phải yêu cầu pháp lý/tiêu chuẩn đã được xác minh.

| Rủi ro theo cause → event → impact → objective | Bảo vệ được mô tả và giới hạn | Mục tiêu kiểm soát / hướng hoàn thiện đề xuất |
|---|---|---|
| Nếu số lượng ghi nhận sai và review không phát hiện, quyết định hoàn tiền có thể dùng dữ liệu sai, dẫn tới hoàn không đúng hoặc tranh chấp, ảnh hưởng mục tiêu đối chiếu số lượng và quyết định hoàn tiền. Căn cứ suy luận: trang 1 mục 1 và trang 2 bảng 1 hàng 1. | Hoạt động ghi số lượng và trưởng ca xem xét có trong packet. Review chỉ là **control candidate**: chưa đủ thuộc tính để xác nhận coverage, thiết kế đầy đủ hoặc testability. Không có bằng chứng đã thực hiện. | Số lượng dùng cho quyết định phải có căn cứ đối chiếu và chênh lệch được giải quyết. Đề xuất làm rõ review đối chiếu số lượng ghi nhận với hàng/chứng từ phù hợp trước quyết định; lưu người review, thời điểm, kết quả và cách xử lý chênh lệch. Người chịu trách nhiệm, dữ liệu chuẩn, tiêu chí, nơi lưu và tuyến escalation: `To be validated`. |
| Nếu quy tắc phân quyền thực tế không rõ hoặc bị áp dụng sai, quyết định hoàn tiền có thể do người không đúng thẩm quyền thực hiện hoặc bị trì hoãn, ảnh hưởng tính hợp lệ và tiến độ quyết định. Căn cứ đặt câu hỏi: trang 2 bảng 1 hàng 2, `UP-EVD-16-02`. | Ô mờ là **hạn chế nguồn**, không chứng minh doanh nghiệp thiếu phân quyền. Chưa thể xác nhận cơ chế duyệt, cấp duyệt, hạn mức hoặc control thay thế; trưởng ca xem xét không tự bù cho thẩm quyền chưa biết. | Quyết định được thực hiện đúng quyền và điều kiện đã phê duyệt. Trước hết xác minh nguyên văn ô Người duyệt và căn cứ phân quyền có hiệu lực; sau đó mới đề xuất cách kiểm tra và lưu dấu vết quyết định theo căn cứ đó. Không tự gán chức danh hay hạn mức. |

Confidence cho hai kịch bản: Low (`Inferred`); validation là làm rõ thiết kế review và thẩm quyền bằng nguồn có thể đọc được. Không đủ dữ liệu phân loại key control, actual SoD conflict hoặc SPOF. Không chấm inherent/residual risk, không đặt sample size; đánh giá vận hành là `Not assessed`, bằng chứng vận hành là `Insufficient evidence`.

## 4. Giới hạn, cải tiến và điểm cần xác nhận

Phần đọc được chưa mô tả tiêu chí review, evidence, timing hoặc ngoại lệ. Đây là hạn chế mô tả **trong phạm vi packet đã đọc**, không phải kết luận toàn bộ SOP thiếu các nội dung đó. Bảng phê duyệt đọc dở khiến đánh giá thẩm quyền phải dừng ở `Unresolved`; chưa có cơ sở gọi là control failure, compliance gap hoặc audit finding.

Các bước tiếp theo được đề xuất, chưa thực hiện:

1. **Human review ô Người duyệt:** giữ nguyên queue của nguồn — “xác nhận ô Người duyệt trang 2 trước khi kết luận thẩm quyền”. Cần bản rõ hoặc xác nhận nguyên văn có locator, kèm phiên bản/ngày hiệu lực và căn cứ phân quyền liên quan. Không đổi `normalized: null` hay nâng trạng thái upstream trước khi có xác nhận có căn cứ.
2. **Làm rõ nội dung review:** bổ sung phần tài liệu mô tả người chịu trách nhiệm, đối tượng/tiêu chí đối chiếu, thời điểm, kết quả cần lưu, xử lý chênh lệch và escalation. Chỉ đề xuất cập nhật SOP sau khi biết thiết kế và control thay thế hiện có; không tự thêm một cấp phê duyệt.
3. **Nếu cần đánh giá thực tế sau này:** xác định scope/kỳ, thu evidence giao dịch và walkthrough theo phương pháp được duyệt. Bước này chưa chạy và không phải điều kiện để sử dụng phần phân tích tài liệu có giới hạn ở trên.

Owner và thời hạn cho các việc trên: `Not provided`; người dùng cần chỉ định người quản lý tài liệu/phân quyền có thẩm quyền. Mọi thay đổi trách nhiệm, phân quyền hoặc SOP phải được phê duyệt trước khi áp dụng.

Nếu quy trình không thay đổi, chưa thể kết luận mức rủi ro còn lại: biện pháp bảo vệ duy nhất được mô tả trong phần đọc được là ghi số lượng và xem xét, chưa được kiểm chứng vận hành. Hai kịch bản trên chỉ có thể dùng làm câu hỏi xác minh. Riêng việc dùng ô mờ làm căn cứ ban hành quyền duyệt có thể dẫn tới gán sai thẩm quyền; vì vậy **không sử dụng packet này như approval matrix đã được xác nhận**.
