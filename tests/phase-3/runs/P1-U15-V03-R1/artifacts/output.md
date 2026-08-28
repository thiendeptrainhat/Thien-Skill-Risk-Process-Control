E2E phù hợp: **Từ yêu cầu trả hàng đến hoàn tiền và đối chiếu hàng–tiền–công nợ** (Return-to-Refund, nhãn mô tả phân tích, cần chủ quy trình xác nhận). Mục tiêu là hoàn tiền đúng giao dịch được chấp thuận; bắt đầu khi khách yêu cầu trả, kết thúc khi đối chiếu xong, xuyên qua dịch vụ, kho, trưởng ca và kế toán. Nguồn: tr. 1, “Mục tiêu và phạm vi” và bảng “Trình tự xử lý”.

Phân tích ở lớp **As-Documented**, dựa trên SOP-SYN-15, phiên bản 1: :codex-file-citation{path="/Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U15-V03/input.pdf" purpose="source"}. Đây là dữ liệu tổng hợp được phép dùng trong AI và lưu trong bộ kiểm thử, không phải hồ sơ doanh nghiệp thật. Ngày hiệu lực và phê duyệt SOP chưa được nêu.

### Kiểm soát được mô tả

| Nội dung theo SOP | Người thực hiện và hồ sơ được yêu cầu | Vị trí nguồn, đều tại tr. 1 |
|---|---|---|
| Kiểm đếm và ghi tình trạng hàng nhận lại. | Nhân viên kho; phiếu nhận, ảnh. | Bảng “Trình tự xử lý”, dòng “Nhận hàng”. |
| Xem điều kiện hoàn tiền trước phát lệnh. | Trưởng ca; ghi nhận phê duyệt. | Cùng bảng, dòng “Chấp thuận”. |
| Chỉ hoàn về tài khoản gốc sau chấp thuận. | Kế toán; lệnh hoàn và đối chiếu. | Cùng bảng, dòng “Hoàn tiền”. |
| Giữ chênh lệch số lượng/tình trạng để làm rõ trước hoàn tiền. | Người xử lý và hồ sơ đóng ngoại lệ: chưa nêu. | “Ngoại lệ và lưu hồ sơ”, câu 1. |
| Liên kết yêu cầu, phiếu nhận, phê duyệt và lệnh hoàn theo mã đơn, hỗ trợ truy nguyên. | Người lưu, nơi lưu và thời hạn lưu: chưa nêu. | “Ngoại lệ và lưu hồ sơ”, câu 2. |

Bước tiếp nhận ghi mã đơn và lý do trả tạo đầu vào truy nguyên; chưa mô tả việc kiểm tra tính hợp lệ của yêu cầu (bảng “Trình tự xử lý”, dòng “Tiếp nhận”).

### Điểm cần làm rõ

- Điều kiện hoàn tiền cụ thể và giới hạn thẩm quyền Trưởng ca là gì? Ma trận thẩm quyền chi tiết chưa được cung cấp (“Chấp thuận”; “Hồ sơ cung cấp”).
- Ai làm rõ chênh lệch, ai cho phép tiếp tục và lưu bằng chứng xử lý thế nào? (“Ngoại lệ và lưu hồ sơ”).
- Ai thực hiện/soát xét đối chiếu hàng–tiền–công nợ, khi nào và theo tiêu chí nào để đóng giao dịch? (“Mục tiêu và phạm vi”; dòng “Hoàn tiền”).
- Cách xác minh tài khoản gốc; trách nhiệm, nơi và thời hạn lưu hồ sơ; tình trạng phê duyệt/hiệu lực SOP cần được xác nhận (dòng “Hoàn tiền”; “Ngoại lệ và lưu hồ sơ”; phần đầu tài liệu).

Độ tin cậy phân tích: trung bình, dựa trên một SOP. Không có log, walkthrough hay kiểm thử vận hành (“Hồ sơ cung cấp”), nên chưa kết luận hiệu quả vận hành hoặc công nhận kiểm soát nào là key control. Những điểm chưa nêu là giới hạn mô tả/bằng chứng, không chứng minh kiểm soát không tồn tại.
