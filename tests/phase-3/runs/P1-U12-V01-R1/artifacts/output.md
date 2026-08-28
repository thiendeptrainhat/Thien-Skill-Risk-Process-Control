# Đánh giá kiểm soát ngăn thanh toán trùng

Chưa có căn cứ xác định gap chỉ vì kiểm soát hiện tại khác hình thức tham khảo. Chặn tự động kết hợp review ngoại lệ là một cách thực hiện thay thế phù hợp về mục tiêu và thời điểm đối với giao dịch trùng đúng khóa. Tuy nhiên, chưa đủ bằng chứng để xác nhận bao phủ mọi trường hợp “cùng nghĩa vụ” hoặc hiệu quả vận hành toàn kỳ.

Mục tiêu là ngăn thanh toán nhiều lần cho cùng nghĩa vụ; phạm vi đánh giá là kiểm tra trước phát lệnh, chặn và xử lý ngoại lệ. Đây là dữ liệu tổng hợp với nguồn, bằng chứng hư cấu; quyền dùng AI, lưu và tái phân phối được nêu tại dòng 1 của [nguồn đầu vào](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U12-V01/input.md:1>). Không có xác minh nguồn bên ngoài.

## Căn cứ và giới hạn

| Nguồn | Vai trò/lớp phân tích | Nội dung có thể sử dụng |
|---|---|---|
| REF-12 §4 | Baseline advisory, không phải một lớp current state | Khuyến nghị người rà soát đối chiếu hóa đơn trùng trước thanh toán; mục tiêu là không trả cùng nghĩa vụ nhiều lần, không bắt buộc công nghệ. Không phải căn cứ xác định compliance gap chỉ do khác hình thức. |
| CONFIG-12 v5 §2 | As-Designed | Chặn theo `supplier_id + invoice_number + amount` trước phát lệnh; tài khoản vận hành không đổi được cấu hình; ngoại lệ chuyển hàng chờ để người khác xem xét. |
| SOP-12 §5 | As-Documented | Yêu cầu người kiểm soát review hàng chờ hằng ngày và giữ log giải quyết; chưa chứng minh yêu cầu này đã được thực hiện hằng ngày. |
| LOG-12 | As-Performed, giới hạn các sự kiện được mô tả | Một giao dịch trùng ngày 03/07/2026 bị chặn; một ngoại lệ đã chuyển review và chưa phát lệnh. Không chứng minh review đã hoàn tất hoặc kiểm soát vận hành hiệu quả cả kỳ. |

Version duy nhất được nêu là CONFIG-12 v5; ngày hiệu lực/phê duyệt và chủ sở hữu các tài liệu là `Not provided`. Việc REF-12 được tổ chức tiếp nhận thành nghĩa vụ nội bộ chưa được cung cấp; đánh giá này dùng đúng tính advisory đã nêu, không đưa ra kết luận tuân thủ.

## Có gap nào được chứng minh?

| Khía cạnh | Đánh giá theo mục tiêu và cả bộ kiểm soát |
|---|---|
| Coverage và precision | Khóa trùng xác định rõ, hỗ trợ ngăn giao dịch có cùng ba trường. “Trùng khóa” chưa đồng nghĩa “cùng nghĩa vụ” trong mọi biến thể. Việc đổi số hóa đơn chưa được kiểm thử: đây là giới hạn bằng chứng và giả thuyết về khoảng trống coverage, chưa phải kết luận hệ thống đã bỏ lọt. [CONFIG-12 §2; dòng cuối nguồn đầu vào] |
| Timing | Chặn trước phát lệnh phù hợp với mục tiêu phòng ngừa. LOG-12 hỗ trợ điều này trong trường hợp được mô tả. Không có căn cứ buộc bổ sung một bước thủ công giống REF-12 chỉ để khớp hình thức. [REF-12 §4; CONFIG-12 §2; LOG-12] |
| Independence và dependency | Hạn chế quyền đổi cấu hình của tài khoản vận hành cùng người review khác là bảo vệ có cơ sở ở lớp thiết kế. Chưa có kiểm thử thay đổi cấu hình; quyền đặc quyền, khả năng bypass và tính độc lập thực tế toàn kỳ chưa được xác minh. Cũng chưa có bằng chứng về completeness/accuracy của dữ liệu ba trường và phạm vi các luồng phát lệnh. [CONFIG-12 §2; dòng cuối nguồn đầu vào] |
| Ngoại lệ và evidence | Hàng chờ và review hằng ngày bổ sung cho chặn tự động, không tự là kiểm soát trùng lặp cần bỏ. Đã có bằng chứng một ngoại lệ chưa phát lệnh, nhưng chưa có kết quả xử lý/đóng ngoại lệ hay coverage toàn kỳ. Không đồng nhất “chưa cung cấp log giải quyết” với “không giữ log”. [SOP-12 §5; LOG-12] |

Phân loại phù hợp hiện tại là **evidence limitation** đối với biến thể, thay đổi cấu hình và coverage toàn kỳ. Potential design gap về nhận diện cùng nghĩa vụ còn `To be validated`, sau khi kiểm tra rule và các kiểm soát bổ sung. Chưa chứng minh missing control, operating deviation hoặc compliance gap. Cũng chưa đủ để tuyên bố hoàn toàn tương đương với mục tiêu tham khảo.

## Cải tiến đề xuất — Target-State, draft

1. Giữ bộ kiểm soát chặn trùng và review ngoại lệ trong khi xác minh coverage. Không bổ sung review thủ công đại trà chỉ vì REF-12 mô tả người rà soát; không bỏ review ngoại lệ vì đã có tự động hóa.
2. Lập kiểm thử dự kiến trong môi trường kiểm thử được phép: trùng đúng khóa; đổi số/cách ghi số hóa đơn nhưng vẫn cùng nghĩa vụ; giao dịch hợp lệ không trùng; chuyển review và giải phóng/từ chối ngoại lệ. Kèm kiểm thử hạn chế quyền vận hành và bằng chứng phê duyệt, log, kiểm thử hồi quy khi đổi cấu hình. Đối soát population hóa đơn, hàng chờ và lệnh thanh toán trong kỳ đánh giá cần thống nhất. Đây là đề xuất chưa thực hiện; cần xác nhận dữ liệu đáng tin cậy và methodology trước khi quyết định cách chọn mẫu hoặc kiểm tra toàn bộ.
3. Hoàn thiện khả năng truy nguyên xử lý ngoại lệ: đối chiếu yêu cầu review hằng ngày với log có giao dịch, người review, thời điểm, quyết định, căn cứ và liên kết lệnh thanh toán. Xác nhận tiêu chí giải phóng, thẩm quyền và escalation; nếu đã có tài liệu khác thì dẫn chiếu, không mặc định chúng đang thiếu. Người phụ trách cụ thể và thời hạn hành động: `To be validated`.
4. Chỉ mở rộng thiết kế nếu xác nhận coverage chưa đủ. Có thể cân nhắc chuẩn hóa số hóa đơn/định danh nghĩa vụ và mở rộng rule, hoặc review thủ công có mục tiêu cho biến thể khó nhận diện. Rule rộng có thể tăng chặn nhầm; review thủ công cần năng lực xử lý và bằng chứng đầy đủ. Chọn theo kết quả kiểm thử, chất lượng dữ liệu và khối lượng thực tế, không mặc định tự động hóa luôn tốt hơn. Đây là analyst proposal, không phải yêu cầu công nghệ từ REF-12.

Nếu giữ nguyên mà không xác minh: giả thuyết là cùng nghĩa vụ đổi số hóa đơn có thể không khớp khóa, không vào hàng chờ, rồi được phát lệnh lần nữa, gây trả thừa và ảnh hưởng mục tiêu thanh toán đúng. Chặn đúng khóa và review các ngoại lệ được nhận diện là bảo vệ hiện có theo nguồn; chúng chưa chứng minh bao phủ tình huống này. Chưa xác nhận sự cố, tổn thất hoặc xác suất; cần kiểm thử và kiểm tra kiểm soát bổ sung để phân định.

Confidence: `Medium` cho nhận định thiết kế trong phạm vi trích đoạn; `Unresolved` cho coverage biến thể và toàn kỳ. Đánh giá operating effectiveness toàn kỳ: `Not assessed`, evidence: `Insufficient evidence`; không tự chấm risk score. Bản tư vấn là dự thảo theo cách tiếp cận objective-based của skill; thay đổi SOP/cấu hình hoặc chấp nhận residual risk cần người có thẩm quyền phê duyệt. Không phát hành kết luận assurance chính thức.
