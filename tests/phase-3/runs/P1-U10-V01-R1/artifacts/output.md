# Kiểm soát thanh toán theo SOP-PAY-10

Mục tiêu là trả đúng đối tượng, đúng số tiền và đúng nghĩa vụ đã được duyệt (§1). Hồ sơ cho phép trích xuất **4 cơ chế/yêu cầu kiểm soát ở lớp As-Documented**; chưa chứng minh chúng đang được thực hiện hoặc vận hành hữu hiệu.

Nguồn duy nhất `SRC-01`: [nội dung SOP được cung cấp](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U10-V01/input.md>), SOP-PAY-10 v1, phê duyệt ngày 01/06/2026 theo phần đầu tài liệu. Ngày hiệu lực, tình trạng còn áp dụng, chủ sở hữu tài liệu, đơn vị và kỳ đánh giá: `Not provided`. Nguồn ghi: “DỮ LIỆU TỔNG HỢP; được phép phân tích trong AI.”

Phạm vi đọc: §1–§4, từ kiểm tra trước lập lệnh đến phê duyệt trước phát lệnh, cùng yêu cầu xử lý chênh lệch/ngoại lệ; chưa có căn cứ dựng toàn bộ quy trình thanh toán đến kết quả ngân hàng. Confidence: `Medium` cho trích xuất tài liệu, do chỉ có một nguồn; trạng thái vận hành: `Unresolved`. Bản phân tích là dự thảo, `review_status: Not reviewed`.

## 1. Kiểm soát được tài liệu quy định

Các ghi nhận dưới đây đều là `As-Documented`, `Documented`, phạm vi thanh toán theo SOP; kỳ vận hành được đánh giá: `Not provided`. ID chỉ dùng để truy nguyên trong bản phân tích này.

| Control / observation | Nội dung có căn cứ | Mục tiêu kiểm soát và nhận xét thiết kế sơ bộ | Nguồn |
|---|---|---|---|
| `CTL-PAY-01` / `OBS-PAY-01-D` — Đối chiếu trước lập lệnh | Người lập lệnh kiểm tra hóa đơn với đơn hàng và biên bản nhận trước khi lập lệnh. | Hỗ trợ bảo đảm lệnh có căn cứ nghĩa vụ phù hợp. Thời điểm được xác định rõ; chưa nêu các trường phải đối chiếu, tiêu chí chấp nhận chênh lệch hoặc dấu vết kiểm tra cần lưu. | SRC-01 §2 |
| `CTL-PAY-02` / `OBS-PAY-02-D` — Hai người phê duyệt tuần tự | Hai người có thẩm quyền, khác người lập lệnh, phải phê duyệt lần lượt trước khi phát lệnh; dấu vết duyệt được lưu cùng hồ sơ. | Hỗ trợ bảo đảm lệnh được cho phép trước khi phát và tách người lập khỏi người duyệt. Có tiêu chí về số người, trình tự, thời điểm và yêu cầu lưu dấu vết; chưa có căn cứ xác định thẩm quyền cụ thể, nội dung mỗi người phải kiểm tra hoặc cơ chế chống bỏ qua bước duyệt. | SRC-01 §3 |
| `CTL-PAY-03` / `OBS-PAY-03-D` — Giữ lại chênh lệch | Chênh lệch phải được giữ lại để xử lý. Người thực hiện: `Not provided`; trigger: có chênh lệch. | Hướng tới việc chênh lệch được xử lý có kiểm soát. Chưa rõ đối tượng được giữ lại là hồ sơ hay lệnh, cơ chế giữ, người xử lý, điều kiện giải phóng và bằng chứng kết thúc xử lý. | SRC-01 §4, vế về chênh lệch |
| `CTL-PAY-04` / `OBS-PAY-04-D` — Xác nhận riêng ngoại lệ | Ngoại lệ cần xác nhận riêng. Người xác nhận, thời điểm và hình thức xác nhận: `Not provided`. | Hướng tới ngoại lệ được xem xét riêng. Mô tả chưa đủ để xác định thẩm quyền, tiêu chí hoặc khả năng kiểm thử; không tự diễn giải “xác nhận” thành một cấp phê duyệt đã được quy định. | SRC-01 §4, vế về ngoại lệ |

Các mục tiêu và nhận xét ở cột thứ ba là diễn giải phân tích từ §1–§4, không phải bằng chứng vận hành. Accountability của control owner, hệ thống, mức tự động hóa, thời hạn lưu hồ sơ và tuyến escalation chưa được cung cấp. Chưa đủ cơ sở phân loại control nào là **key control**; trạng thái này là `To be validated`.

Đặc biệt, §3 chỉ **yêu cầu lưu dấu vết duyệt**; hồ sơ đầu vào không chứa dấu vết duyệt thực tế. Các chứng từ được §2 nhắc đến cũng chưa được cung cấp.

## 2. Có thể và chưa thể đánh giá gì?

Có thể đánh giá sơ bộ tính đầy đủ, nhất quán của mô tả, mức phù hợp thiết kế với mục tiêu, độ bao phủ rủi ro về lý thuyết và khả năng kiểm thử. Cụ thể:

- §2–§3 đặt kiểm tra và phê duyệt trước lập/phát lệnh, phù hợp về logic với việc phòng ngừa thanh toán sai hoặc chưa được cho phép. Đây không phải kết luận thiết kế đã đầy đủ.
- §3 có nhiều thuộc tính kiểm thử rõ hơn §4: hai người, khác người lập, duyệt lần lượt, trước phát lệnh và lưu dấu vết. Cần làm rõ thẩm quyền, tiêu chí duyệt và dữ liệu thời điểm trước khi kiểm thử.
- §2 chưa làm rõ cách xác minh “đúng đối tượng, số tiền”; §4 còn thiếu trách nhiệm, điều kiện xử lý và bằng chứng. Đây là hạn chế mô tả trong hồ sơ đã đọc, không chứng minh doanh nghiệp thiếu hoặc không thực hiện các kiểm soát đó.

Chưa thể xác nhận thiết kế đã triển khai trong thực tế (`As-Designed`), việc thực hiện (`As-Performed`), tỷ lệ sai lệch, hiệu quả vận hành, mức rủi ro còn lại hay xung đột phân nhiệm ở người dùng thực tế. Không có căn cứ kết luận kiểm soát “đạt”, “thất bại” hoặc tuân thủ một chuẩn bên ngoài.

Đối với đánh giá vận hành: `assessment_status: Not assessed`; `evidence_status: Insufficient evidence`. Các trạng thái này không xóa các nhận xét thiết kế có căn cứ nêu trên và không có nghĩa control failed.

## 3. Bằng chứng cần bổ sung

1. **Xác nhận thiết kế và hiệu lực:** bản SOP còn hiệu lực, chủ sở hữu, ngày hiệu lực; ma trận thẩm quyền, phân công người lập/người duyệt và quyền truy cập liên quan; tiêu chí đối chiếu/duyệt, quy tắc xử lý chênh lệch và ngoại lệ. Nếu dùng hệ thống, cần cấu hình workflow và quyền override phù hợp kỳ đánh giá, không chỉ lời xác nhận của quản lý.
2. **Cho CTL-PAY-01:** bộ hóa đơn–đơn hàng–biên bản nhận gắn với lệnh thanh toán, dấu vết nội dung/kết quả đối chiếu, người kiểm tra và thời điểm. Walkthrough một hồ sơ thực tế giúp hiểu cách thực hiện; không đại diện cho cả kỳ.
3. **Cho CTL-PAY-02:** hồ sơ và dấu vết hai lượt duyệt, danh tính/thẩm quyền từng người tại thời điểm duyệt, người lập, thời gian từng lượt và thời điểm phát lệnh. Đối chiếu để kiểm tra tính khác người, tuần tự và trước phát lệnh; kiểm tra dấu vết có được lưu cùng hồ sơ theo §3 không.
4. **Cho CTL-PAY-03–04:** hồ sơ chênh lệch/ngoại lệ, dấu vết giữ và xử lý, quyết định giải phóng nếu áp dụng, xác nhận riêng, người có thẩm quyền và bằng chứng kết thúc xử lý. Cần truy vết được đến giao dịch; không chỉ lấy các giao dịch đi theo luồng bình thường.
5. **Nếu muốn đánh giá hiệu quả vận hành:** chốt mục tiêu, phạm vi, kỳ và phương pháp được phê duyệt; có population đầy đủ, kiểm tra độ tin cậy dữ liệu, phương án lấy mẫu hoặc toàn bộ population, thủ tục thực sự đã thực hiện và kết quả/bằng chứng tương ứng. Chưa có cơ sở tự ấn định cỡ mẫu. Các nội dung trên hiện là yêu cầu bằng chứng/kiểm thử tiềm năng, chưa phải kiểm thử đã chạy.

Khi đủ điều kiện, có thể chuẩn bị bản đánh giá vận hành dự thảo và hồ sơ kết quả để bàn giao; kết luận operating effectiveness chính thức thuộc assurance owner độc lập có thẩm quyền. Trước mắt, đầu ra phù hợp là danh mục kiểm soát **theo tài liệu**, nhận xét thiết kế có giới hạn và danh sách bằng chứng cần xác minh như trên.
