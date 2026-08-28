# Phân tích SOP-17A — bản dự thảo

SOP đã mô tả chuỗi từ nhận yêu cầu sửa chữa đến bàn giao và thu tiền, với các điểm kiểm soát về báo giá, kiểm tra thiết bị và xác nhận của khách. Điểm cần làm rõ trước tiên là cách duyệt chi phí ngoài báo giá: §3 xác nhận chưa có tài liệu về nội dung này. Đây là **khoảng trống tài liệu**, chưa phải bằng chứng rằng thực tế không có kiểm soát hoặc đã xảy ra sai phạm.

## 1. Phạm vi E2E

Mục tiêu suy ra từ §§1–2, cần chủ quy trình xác nhận: sửa đúng yêu cầu đã thống nhất, bàn giao kết quả được chấp nhận và thu đúng khoản tiền thỏa thuận. Khách hàng là bên nhận kết quả; trách nhiệm chủ quy trình chưa được cung cấp.

Luồng **As-Documented** theo §1:

Nhận yêu cầu → Kiểm tra thiết bị → Báo giá để khách chấp thuận → Sửa → Kiểm tra kết quả → Bàn giao và thu tiền.

Điểm đầu là nhận yêu cầu; điểm cuối trong đoạn trích là bàn giao và thu tiền. Chưa rõ thứ tự hoặc điều kiện phụ thuộc giữa bàn giao và thanh toán. Nguồn chỉ thể hiện luồng thuận; chưa mô tả nhánh khách từ chối báo giá, không sửa được, kiểm tra không đạt hoặc chưa thanh toán. Không tự bổ sung các nhánh này thành quy trình đang vận hành. Tên E2E mang tính mô tả, chưa gán cấp L0–L5 hay mã thư viện chuẩn.

## 2. Kiểm soát được mô tả

Các mã dưới đây chỉ dùng truy nguyên trong bản phân tích. Mục tiêu kiểm soát là diễn giải của người phân tích; hành động trong cột thứ hai lấy từ SOP, không phải xác nhận đã thực hiện.

| Kiểm soát / nguồn | Nội dung As-Documented | Mục tiêu kiểm soát suy ra | Thuộc tính cần làm rõ |
|---|---|---|---|
| CTL-01 — Kiểm tra đầu vào, §§1–2 | Kiểm tra thiết bị; kỹ thuật viên ghi lỗi. | Xác định đúng tình trạng và vấn đề cần xử lý trước khi báo giá/sửa. | Ai kiểm tra; cách nhận diện thiết bị; tiêu chí chẩn đoán; nơi lưu ghi nhận. Không mặc định người ghi cũng là người kiểm tra. |
| CTL-02 — Chấp thuận báo giá, §1 | Báo giá để khách chấp thuận, trước bước sửa theo trình tự nêu trong SOP. | Phạm vi và chi phí sửa được thống nhất trước khi triển khai. | Người lập/duyệt báo giá nội bộ; bằng chứng và thời điểm khách chấp thuận; phiên bản báo giá; xử lý khi không đồng ý. |
| CTL-03 — Kiểm tra sau sửa, §§1–2 | Kiểm tra kết quả; kỹ thuật viên ghi kết quả kiểm tra. | Kết quả sửa được đánh giá trước bàn giao, có dấu vết truy nguyên. | Tiêu chí đạt/không đạt; ai kiểm tra; mức độc lập cần thiết; xử lý và kiểm tra lại khi không đạt. |
| CTL-04 — Xác nhận bàn giao, §2 | Khách xác nhận khi bàn giao. | Có xác nhận về việc bàn giao cho khách. | Khách xác nhận nội dung gì, theo hình thức nào, gắn với thiết bị/hồ sơ nào; cách lưu và xử lý tranh chấp. |

CTL-01 và CTL-03 nằm ở hai thời điểm khác nhau, nên không có căn cứ coi là trùng lặp. Việc ghi lỗi/kết quả hỗ trợ truy nguyên nhưng tự nó chưa chứng minh đã kiểm tra đúng tiêu chí. “Sửa” và “thu tiền” là hoạt động nghiệp vụ; chưa đủ mô tả để coi chúng là kiểm soát độc lập. Chưa có căn cứ chỉ định control nào là key control hoặc đánh giá hiệu quả vận hành.

## 3. Rủi ro và các điểm cần làm rõ

Những tình huống dưới đây là suy luận có điều kiện từ tài liệu, không phải sự cố đã quan sát; chưa chấm điểm rủi ro.

1. **Chi phí phát sinh — §3, liên quan CTL-02.** Nếu phát sinh được thực hiện trước khi thống nhất giá mới, khách có thể từ chối thanh toán, ảnh hưởng thu tiền và quan hệ khách hàng. CTL-02 bao phủ báo giá ban đầu; CTL-04 diễn ra lúc bàn giao nên không tự thay thế chấp thuận trước đối với phát sinh. Cần xác nhận: hiện đang xử lý phát sinh thế nào, ai được duyệt nội bộ, khách chấp thuận ra sao, có kiểm soát thay thế hoặc quy định ở tài liệu khác không?
2. **Chất lượng sửa chữa — §§1–2, CTL-01/03.** Nếu tiêu chí kiểm tra không rõ hoặc không phù hợp, lỗi có thể bị bỏ sót và thiết bị được bàn giao khi chưa đạt, gây tái sửa/khiếu nại. Hai bước kiểm tra là lớp bảo vệ được mô tả, nhưng chưa đủ thông tin về độ chính xác của thiết kế. Cần tiêu chí chẩn đoán, nghiệm thu và tuyến xử lý không đạt; không suy ra kiểm tra yếu chỉ vì đoạn trích ngắn.
3. **Bàn giao và thu tiền — §§1–2, CTL-04.** Nếu hồ sơ bàn giao, giá được chấp thuận và khoản thu không được đối chiếu phù hợp, có thể thu thiếu/sai hoặc khó giải quyết tranh chấp. SOP chưa mô tả phép đối chiếu này; xác nhận bàn giao không tự chứng minh đã thu tiền. Cần làm rõ số tiền phải thu, bằng chứng thu, người chịu trách nhiệm và điều kiện đóng hồ sơ/chưa thanh toán.
4. **Trách nhiệm và ngoại lệ — §§1–3.** Ai chịu trách nhiệm xuyên suốt và ở từng lần chuyển việc? Ai quyết định khi khách từ chối, sửa không được hoặc kết quả không đạt? Hệ thống/sổ theo dõi, biểu mẫu, nơi lưu hồ sơ và thời hạn xử lý chưa được cung cấp. Đây là yêu cầu xác minh, không phải kết luận thiếu người phụ trách hoặc thiếu hệ thống.

Nếu giữ nguyên cách mô tả hiện nay, rủi ro riêng của tài liệu là người thực hiện có thể hiểu khác nhau về quyền duyệt phát sinh và bằng chứng cần lưu. Mức phơi nhiễm thực tế còn phụ thuộc cơ chế đang áp dụng; chưa biết tần suất, tổn thất hay kiểm soát bù trừ.

## 4. Hướng bổ sung — Target-State, chưa phê duyệt

Trước hết, xác minh cơ chế duyệt phát sinh hiện có. Nếu đã có cơ chế được phê duyệt, cập nhật hoặc dẫn chiếu vào SOP; nếu chưa có, đề xuất một điểm quyết định trước phần việc phát sinh: ghi lý do, phạm vi và giá điều chỉnh; xác định phê duyệt nội bộ cần thiết và chấp thuận của khách; lưu dấu vết; quy định cách xử lý khi chưa được chấp thuận. Không tự đặt hạn mức, chức danh hay thời hạn.

Tiếp theo, làm rõ tiêu chí kiểm tra, xác nhận bàn giao, đối chiếu khoản thu và các nhánh ngoại lệ. Có thể đối chiếu hồ sơ sửa chữa đã khử định danh với báo giá/chấp thuận, ghi nhận kiểm tra, phát sinh, bàn giao và thanh toán để xác minh As-Performed; hiện chưa thực hiện walkthrough hoặc kiểm thử. Các thay đổi cần người có thẩm quyền của đơn vị review/phê duyệt trước khi áp dụng; người phê duyệt cụ thể: `Not provided`.

## Căn cứ và giới hạn

Nguồn duy nhất là nội dung SOP-17A §§1–3 được cung cấp; đã đọc trực tiếp toàn bộ native text. Giữ nguyên điều kiện nguồn: “DỮ LIỆU TỔNG HỢP; được phép phân tích trong AI.” Document-Evidence không khả dụng; không gọi/cài specialist và không sử dụng OCR. Không cần năng lực đó để đọc phần nội dung này.

Phiên bản, hiệu lực, chủ tài liệu, tình trạng phê duyệt và kỳ áp dụng: `Not provided`. Confidence đối với nội dung được ghi là `Medium` — một nguồn văn bản, chưa đối chứng; mục tiêu và kịch bản suy luận có confidence `Low`, cần xác minh như trên. Chỉ phân tích **As-Documented** và tách riêng đề xuất **Target-State**; **As-Designed** chưa được xác nhận độc lập, **As-Performed** chưa có bằng chứng. Không tra cứu bên ngoài, không kết luận tuân thủ hay hiệu quả vận hành. Trạng thái review: `Not reviewed`.
