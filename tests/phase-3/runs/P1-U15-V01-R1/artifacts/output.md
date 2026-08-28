E2E phù hợp là **từ yêu cầu trả hàng đến hoàn tiền và đối chiếu hàng–tiền–công nợ**, nhằm hoàn tiền đúng giao dịch được chấp thuận. Đây là tên mô tả theo ranh giới SOP, không phải mã phân loại chuẩn. Nguồn: [SOP-SYN-15, phiên bản 1](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U15-V01/input.md:9>), mục “Mục tiêu và phạm vi”, dòng 9.

Các nội dung dưới đây thuộc `As-Documented`. Nguồn là dữ liệu tổng hợp được phép dùng AI; chưa có log, walkthrough hay kiểm thử, nên không xác nhận việc thực hiện hoặc hiệu quả vận hành (dòng 5, 29). Độ tin cậy: `Medium` cho diễn giải từ một SOP; tình trạng phê duyệt/hiệu lực chưa được cung cấp.

### Kiểm soát trích xuất

Vị trí dẫn dưới đây đều thuộc SOP trên. “Hồ sơ” là hồ sơ SOP yêu cầu, không phải bằng chứng thực tế đã nhận.

| Nội dung kiểm soát | Người thực hiện / hồ sơ | Vị trí nguồn |
|---|---|---|
| Kiểm đếm và ghi tình trạng khi nhận hàng, hỗ trợ phát hiện sai lệch hàng trả. | Nhân viên kho; phiếu nhận, ảnh. | “Trình tự xử lý” → “Nhận hàng”, dòng 17. |
| Xem điều kiện hoàn tiền trước phát lệnh, nhằm chỉ hoàn giao dịch được chấp thuận. | Trưởng ca; ghi nhận phê duyệt. | “Chấp thuận”, dòng 19. |
| Hoàn về tài khoản gốc sau chấp thuận, hạn chế hoàn sai nơi nhận hoặc trước phê duyệt. | Kế toán; lệnh hoàn và đối chiếu. | “Hoàn tiền”, dòng 21. |
| Giữ chênh lệch số lượng/tình trạng để làm rõ trước hoàn tiền. | Người xử lý và hồ sơ giải quyết chưa nêu. | “Ngoại lệ và lưu hồ sơ”, dòng 25. |
| Lưu liên kết yêu cầu, phiếu nhận, phê duyệt và lệnh hoàn theo mã đơn để truy nguyên giao dịch. | Người quản lý hồ sơ chưa nêu. | “Ngoại lệ và lưu hồ sơ”, dòng 25. |

Bước tiếp nhận chỉ nêu ghi mã đơn và lý do trả; chưa mô tả việc kiểm tra tính hợp lệ nên không tự coi đây là kiểm soát xác minh độc lập (dòng 15).

### Những điểm cần làm rõ

- Điều kiện được hoàn, cách xác định số tiền và giới hạn thẩm quyền của trưởng ca là gì? Cần ma trận thẩm quyền và quy tắc được phê duyệt; nguồn xác nhận ma trận chưa được cung cấp (dòng 19, 29).
- Ai xử lý chênh lệch, ai cho phép tiếp tục hoàn tiền; tiêu chí, thời hạn và hồ sơ đóng ngoại lệ là gì (dòng 25)?
- Ai đối chiếu hàng–tiền–công nợ, dùng dữ liệu nào, khi nào và thế nào là hoàn tất? SOP nêu kết quả cuối và tên hồ sơ nhưng chưa mô tả cách đối chiếu (dòng 9, 21).
- Hồ sơ lưu ở đâu, ai quản lý, quyền truy cập và thời hạn lưu là gì? Cần xác nhận thêm chủ sở hữu, phê duyệt và hiệu lực SOP (dòng 3, 25).

Đây là các điểm chưa rõ trong tài liệu, không phải kết luận kiểm soát không tồn tại hoặc đã thất bại. Bản diễn giải cần chủ quy trình xác nhận.
