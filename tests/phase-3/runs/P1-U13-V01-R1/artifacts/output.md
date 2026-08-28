# Phương án cải tiến thanh toán phù hợp nguồn lực

Khuyến nghị chọn **B — chuẩn hóa kiểm soát với hai người hiện có**, nếu chủ doanh nghiệp bố trí được thời gian xác minh và duyệt thực chất. A là bước khởi đầu gọn hơn; C chỉ xem xét khi công cụ sẵn có và lợi ích đã được kiểm chứng. Không mặc định tuyển thêm người hoặc mua ERP. [BRIEF-13 §1, §3]

Đây là đề xuất `Target-State`, bản nháp v1, chưa được phê duyệt. Mục tiêu: giảm chuyển nhầm/gian lận nhưng giữ vận hành gọn; phạm vi từ nhận yêu cầu đổi tài khoản nhà cung cấp đến phát lệnh thanh toán đầu tiên vào tài khoản đã đổi và lưu hồ sơ xác nhận.

## Căn cứ và giới hạn

- Theo mô tả hiện trạng trong BRIEF-13 §1, kế toán tạo/cập nhật nhà cung cấp và chuẩn bị lệnh; chủ doanh nghiệp phát lệnh. Đây là sự phân tách được mô tả, chưa phải bằng chứng `As-Performed` hay xác nhận quyền hệ thống thực tế.
- Ở lớp tài liệu `As-Documented`, BRIEF-13 §2 cho biết hồ sơ duyệt chưa chỉ ra cách xác minh đổi tài khoản. Đây là khoảng trống mô tả; chưa đủ kết luận kiểm soát không tồn tại. Việc chủ có thể xem chứng từ cũng chưa chứng minh đã kiểm tra hoặc xác nhận độc lập.
- CONTRACT-13 §8 được nguồn xác nhận áp dụng: bên mua phải xác nhận qua kênh độc lập **mọi thay đổi tài khoản trước lần trả tiền đầu tiên**. Đây là nghĩa vụ hợp đồng trong phạm vi nguồn, không phải khuyến nghị tùy chọn hay quy định pháp luật chung. Chưa có căn cứ kết luận doanh nghiệp đã vi phạm hoặc đã tuân thủ thực tế.

## Nền tảng phải giữ trong cả ba phương án

Mục tiêu kiểm soát: tài khoản thay đổi phải được xác nhận độc lập và thông tin người hưởng trên lệnh phải đúng tài khoản đã xác nhận trước khi tiền được phát đi.

Cách triển khai dưới đây là đề xuất thiết kế, không phải toàn bộ nội dung do hợp đồng quy định:

1. Kế toán lập hồ sơ thay đổi: yêu cầu gốc, nhà cung cấp, tài khoản cũ/mới và lệnh dự kiến; đánh dấu đang chờ xác minh.
2. Chủ doanh nghiệp xác nhận trực tiếp qua đầu mối/kênh đã được xác thực độc lập từ trước, chẳng hạn gọi số liên hệ đã có hồ sơ tin cậy. Không chỉ dùng số điện thoại hoặc đường dẫn nằm trong chính yêu cầu đổi tài khoản; trả lời cùng chuỗi email yêu cầu không tự tạo tính độc lập. Nếu chưa có đầu mối đáng tin cậy, phải thiết lập và xác thực trước khi trả tiền.
3. Lưu người xác nhận, nguồn lấy đầu mối, thời điểm, tài khoản được xác nhận và kết quả; gắn vào hồ sơ thanh toán. Chủ đối chiếu thông tin người hưởng trên ngân hàng với kết quả này ngay trước phát lệnh, đồng thời kiểm tra chứng từ, số tiền và mục đích thanh toán.
4. Nếu không liên hệ được, thông tin không khớp hoặc tài khoản lại thay đổi: giữ khoản thanh toán liên quan ở trạng thái chờ, chủ xử lý với nhà cung cấp và xác minh lại khi cần. Khoản khác đủ điều kiện vẫn tiếp tục. Không đặt ngưỡng tiền để miễn xác nhận, không dùng hậu kiểm thay cho yêu cầu trước thanh toán của §8.

Phân công này tạo kiểm tra độc lập với người cập nhật dữ liệu và chuẩn bị lệnh, phù hợp hạn chế nhân sự; không tương đương phân tách hoàn toàn mọi nhiệm vụ. Nguy cơ bỏ qua kiểm tra, thông đồng hoặc đầu mối xác nhận bị giả mạo vẫn còn. [BRIEF-13 §1–3; CONTRACT-13 §8]

## So sánh phương án

| Phương án | Thiết kế và lợi ích | Nhược điểm, rủi ro còn lại | Nguồn lực, công nghệ và điều kiện |
|---|---|---|---|
| **A — Tối thiểu đáp ứng §8 về thiết kế** | Thực hiện nền tảng trên bằng phiếu xác minh ngắn, kèm hồ sơ duyệt hiện có. Ít thay đổi, tập trung đúng nghĩa vụ bắt buộc. Nhãn “Minimum compliant” chỉ xét thiết kế theo §8 đã cung cấp, không xác nhận tuân thủ vận hành. | Phụ thuộc trí nhớ, chất lượng ghi chép và thời gian của chủ; hồ sơ rời rạc có thể khiến bỏ sót thay đổi hoặc khó truy nguyên. | Hai người hiện có; thủ công, độ phức tạp thấp. Không phụ thuộc mua hệ thống. Cần chuẩn bị đầu mối tin cậy, biểu mẫu và nơi lưu; thời gian triển khai/ngân sách cụ thể chưa cung cấp. |
| **B — Cân bằng kiểm soát và hiệu suất; đề xuất chọn** | Giữ A; thêm một sổ thay đổi với trạng thái chờ/đã xác minh và bản tài khoản đã xác nhận do chủ kiểm soát để đối chiếu. Gộp chứng từ, xác nhận và duyệt vào một bộ hồ sơ, tránh nhập/duyệt lặp. Dễ nhận ra việc đang chờ, kiểm tra đúng phiên bản và truy xuất bằng chứng. | Thêm công sức cập nhật sổ; nếu kế toán tự sửa cả bản đối chiếu mà không để lại dấu vết, tính độc lập bị suy yếu. Chủ vẫn có thể thành điểm chờ; chưa có dữ liệu về người thay thế nên chưa kết luận SPOF. | Hai người hiện có; dùng phương tiện lưu trữ sẵn có nếu đủ quyền kiểm soát, hoặc bản đối chiếu chủ lưu riêng. Độ phức tạp thấp–vừa. Cần xác nhận khối lượng, thời gian chủ có thể dành, cách bảo vệ bản đối chiếu; chi phí và lịch triển khai chờ xác định. |
| **C — Số hóa chọn lọc, có điều kiện** | Giữ B; tận dụng công cụ đang có để nhắc việc, lưu lịch sử, hạn chế sửa và cảnh báo thay đổi; chỉ dùng chức năng chặn nếu đã kiểm chứng thực sự hỗ trợ. Có thể giảm thao tác lặp khi khối lượng tăng. Xác nhận độc lập vẫn do người thực hiện. | Cấu hình sai, trạng thái “đã xác minh” nhập sai hoặc dữ liệu bị sửa vẫn có thể tạo an tâm giả. Phát sinh quản trị quyền, kiểm thử, bảo trì và xử lý khi công cụ lỗi; không chứng minh hiệu quả hơn B khi chưa có dữ liệu. | Chưa biết tính năng/công cụ hiện có: `To be validated`. Không giả định ERP hoặc ngân sách mới. Độ phức tạp cao hơn A/B; chỉ lập lịch sau khi xác minh khả năng, chi phí và người quản trị. Khi lỗi, quay về B có kiểm soát; không bỏ xác nhận. |

Đánh giá nguồn lực trên là định tính. Chưa có dữ liệu để báo giá, cam kết ngày hoàn thành, tỷ lệ tiết kiệm hay chấm điểm rủi ro. Bổ sung sổ, cách lưu và số hóa là cải tiến do analyst đề xuất; riêng nghĩa vụ xác nhận độc lập và thời điểm thực hiện có căn cứ từ CONTRACT-13 §8.

## Những việc anh/chị cần quyết định

1. **Chọn A hay B cho triển khai đầu tiên và dành thời gian cho chủ:** nếu chưa đủ điều kiện tổ chức B, chọn A làm nền tảng; không chờ số hóa mới thực hiện nghĩa vụ §8. C chưa nên là cam kết đầu tư.
2. **Phê duyệt phân công và quyền:** kế toán chuẩn bị, chủ xác minh/đối chiếu/phát lệnh theo đề xuất. Xác nhận quyền ngân hàng thực tế phù hợp; không chia sẻ tài khoản hay phương tiện xác thực. Khi chủ vắng, phải có người thay thế đủ năng lực, độc lập với bên chuẩn bị và được ủy quyền hợp lệ; hiện chưa có thông tin về người này. Nếu chưa có, giữ khoản cần xác nhận/duyệt và thống nhất cách xử lý chậm với nhà cung cấp.
3. **Chốt đầu mối, bằng chứng và ngoại lệ:** danh sách kênh xác minh tin cậy; nơi lưu, quyền sửa/xem, thời hạn lưu; ai theo dõi khoản đang chờ. Chủ có thể quyết định cách giải quyết vướng mắc, nhưng phê duyệt nội bộ không tự miễn nghĩa vụ hợp đồng.
4. **Chấp nhận phần rủi ro còn lại và điều kiện xem xét lại:** ghi nhận giới hạn của mô hình hai người; không coi chấp nhận rủi ro là quyền bỏ §8. Theo dõi thời gian xử lý, công sức của chủ và các trường hợp thiếu bằng chứng xác nhận trước phát lệnh. Ngưỡng nâng cấp công cụ, lịch rà soát và ngân sách cần quyết định sau khi có dữ liệu, không đặt tùy ý.

Trước áp dụng, đề xuất thử quy trình ngoài giao dịch thật với tình huống hợp lệ, thông tin không khớp, không liên hệ được và chủ vắng; xác nhận khoản chưa đủ điều kiện bị giữ lại và hồ sơ truy xuất được. Chỉ ban hành phân công/quy trình sau khi người có thẩm quyền phê duyệt; không có thay đổi hệ thống hay giao dịch nào được thực hiện trong phân tích này.

Nếu giữ nguyên: trong trường hợp xác nhận độc lập thực tế chưa được thực hiện, yêu cầu đổi tài khoản sai hoặc giả mạo có thể đi qua khâu phát lệnh, gây chuyển nhầm/khó thu hồi tiền và không đáp ứng §8. Bảo vệ hiện được mô tả là chủ phát lệnh; chưa có bằng chứng cho thấy bước này xác thực tài khoản qua kênh độc lập. Đây là kịch bản rủi ro có điều kiện, không phải kết luận đã có gian lận hoặc sai phạm. Cần xem hồ sơ một đợt đổi tài khoản và bằng chứng trước lần thanh toán tương ứng để làm rõ hiện trạng.

Nguồn và độ tin cậy: dữ liệu tổng hợp được phép phân tích trong AI, gồm BRIEF-13 §1–3 và CONTRACT-13 §8 trong [nguồn đầu vào](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U13-V01/input.md>). Chỉ đọc nguồn này; không xác minh ngoài phạm vi. Hiểu nội dung brief và yêu cầu được cung cấp: `Medium` — một nguồn tổng hợp; khả thi của B/C: `To be validated` do thiếu khối lượng, năng lực công cụ và thời gian chủ; vận hành thực tế: `Not assessed`. Phiên bản, chủ tài liệu và kỳ của nguồn chưa cung cấp. Không giả định đã có ngân sách, người dự phòng hoặc cấu hình kiểm soát; mọi phương án vẫn chờ review/phê duyệt.
