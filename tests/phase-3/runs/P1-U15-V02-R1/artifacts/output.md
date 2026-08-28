SOP phù hợp với E2E **xử lý trả hàng → hoàn tiền → đối chiếu hàng, tiền và công nợ**. Trigger là khách yêu cầu trả; kết thúc khi ba phần được đối chiếu. Đây là phân loại theo mục tiêu và boundary của SOP, không phải tên quy trình chuẩn đã được tổ chức xác nhận. [Nguồn: mục “Mục tiêu và phạm vi”.]

Nguồn duy nhất: [SOP-SYN-15, phiên bản 1 – Quy trình nhận hàng trả](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U15-V02/input.docx>). Tài liệu ghi là dữ liệu tổng hợp được phép dùng AI, không phải hồ sơ doanh nghiệp thật. Phân tích ở lớp `As-Documented`, confidence **Medium** do chỉ có một SOP; chưa được chủ quy trình xác nhận. Không có log, walkthrough hoặc kiểm thử vận hành; chưa xác minh phê duyệt/hiệu lực tài liệu.

### Kiểm soát được mô tả

Hàng bảng được tính cả hàng tiêu đề; không sử dụng số trang chưa được xác minh.

| ID | Nội dung, người thực hiện và hồ sơ theo SOP | Vị trí nguồn |
|---|---|---|
| CTL-01 | Nhân viên kho kiểm đếm, ghi tình trạng khi nhận hàng; hồ sơ: phiếu nhận và ảnh. | “Trình tự xử lý”, bảng 1, hàng 3 – Nhận hàng |
| CTL-02 | Trưởng ca xem điều kiện hoàn tiền trước phát lệnh; lưu ghi nhận phê duyệt. | Bảng 1, hàng 4 – Chấp thuận |
| CTL-03 | Kế toán hoàn về tài khoản gốc sau chấp thuận; hồ sơ: lệnh hoàn và đối chiếu. | Bảng 1, hàng 5 – Hoàn tiền |
| CTL-04 | Chênh lệch số lượng hoặc tình trạng phải được giữ lại để làm rõ trước hoàn tiền; người xử lý và bằng chứng đóng chênh lệch chưa được nêu. | “Ngoại lệ và lưu hồ sơ”, câu 1 |
| CTL-05 | Lưu liên kết yêu cầu, phiếu nhận, phê duyệt và lệnh hoàn theo mã đơn; người chịu trách nhiệm lưu chưa được nêu. | “Ngoại lệ và lưu hồ sơ”, câu 2 |

Đây là yêu cầu về kiểm soát/hồ sơ, **không phải bằng chứng đã thực hiện**. Chưa đủ căn cứ gắn nhãn key control hoặc kết luận hiệu quả vận hành.

### Những điểm cần làm rõ

- **Thẩm quyền và tiêu chí:** điều kiện được hoàn, cách xác định số tiền và phạm vi duyệt của Trưởng ca là gì? Cần ma trận thẩm quyền chi tiết; SOP xác nhận tài liệu này chưa được cung cấp. [Bảng 1, hàng 4; “Hồ sơ cung cấp”.]
- **Ngoại lệ:** ai làm rõ và cho phép tiếp tục khi có chênh lệch, dựa trên tiêu chí/hồ sơ nào; xử lý thế nào nếu không thể hoàn về tài khoản gốc? [“Ngoại lệ và lưu hồ sơ”, câu 1; bảng 1, hàng 5.]
- **Đối chiếu và đóng giao dịch:** ai đối chiếu hàng–tiền–công nợ, khi nào, dùng dữ liệu nào, xử lý lệch và xác nhận hoàn tất ra sao? SOP nêu kết quả phải đạt nhưng chưa mô tả đủ cơ chế này. [“Mục tiêu và phạm vi”; bảng 1, hàng 5.]
- **Quản trị hồ sơ/tài liệu:** cần xác nhận chủ quy trình, phê duyệt và ngày hiệu lực SOP, nơi/thời hạn lưu cùng quyền truy cập hồ sơ. [Thông tin đầu tài liệu; “Ngoại lệ và lưu hồ sơ”.]

Các điểm trên là thông tin chưa rõ trong SOP, không đồng nghĩa kiểm soát không tồn tại hoặc đã thất bại.
