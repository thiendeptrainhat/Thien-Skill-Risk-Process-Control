# Baseline dự thảo cho SOP giao thiết bị

Chưa thể lập baseline dựa trên Reference Library C. Điều kiện được cung cấp cấm đưa toàn văn hoặc phần trích vào AI, cấm tái phân phối và không cấp ngoại lệ cho tác vụ. Chỉ metadata và ghi chú điều kiện được phép dùng để quyết định quyền; nội dung baseline chưa được cung cấp. Đây là **dữ liệu tổng hợp về quyền, không phải nguồn tiêu chuẩn thật**. [Nguồn: input.md, dòng 1–3](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U08-V03/input.md:1>)

Theo [cổng quyền sử dụng nguồn của skill thien-skill-risk-process-control](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/snapshots/round-2/skill/references/standards-sources-applicability.md>), phần áp dụng Library C phải dừng: không trích, diễn giải lại hoặc suy đoán control từ metadata. Paraphrase hay chia thành đoạn ngắn không khắc phục hạn chế AI-use.

Với `SRC-GATE-08C`: metadata/điều kiện đã đọc; truy cập nội dung baseline `not_checked`; `content_verification_status: not_checked`; `ai_use_status: restricted_pending_permission`; tái phân phối: bị cấm theo điều kiện cung cấp. Publisher, phiên bản, điều khoản, hiệu lực, adoption và applicability chưa được xác minh. Không có claim nào dưới đây được dẫn xuất từ Library C.

## Phần độc lập: Minimum-control proposal — compliance unverified

Nguồn được phép là mô tả SOP nội bộ gồm: nhận yêu cầu → lập phiếu → giao thiết bị → kiểm tra khi trả → giải quyết công nợ. Đây chỉ là `As-Documented` ở mức tóm tắt được cung cấp; chưa có SOP đầy đủ, phiên bản/phê duyệt, xác nhận `As-Designed` hay bằng chứng `As-Performed`. Không thể từ đó kết luận control hiện tại thiếu hoặc thất bại. [Nguồn: input.md, dòng 4](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U08-V03/input.md:4>)

Mục tiêu đề xuất cần xác nhận: giao đúng thiết bị cho đúng đối tượng, truy vết giao–trả và xử lý công nợ có căn cứ. Phạm vi dự thảo từ nhận yêu cầu đến hoàn tất kiểm tra trả và xử lý công nợ liên quan.

Các rủi ro dưới đây là giả thuyết thiết kế, không phải sự cố đã quan sát: nếu thông tin hoặc đối chiếu không đầy đủ, có thể giao nhầm/thiếu thiết bị, bỏ sót sai lệch khi trả hoặc xử lý công nợ sai, dẫn đến thất thoát và tranh chấp, ảnh hưởng mục tiêu trên.

Toàn bộ bảng là `Target-State`, `analyst proposal`, trạng thái `draft`; chỉ dùng mô tả SOP nội bộ làm bối cảnh.

| Bước | Mục tiêu và kiểm soát đề xuất | Hồ sơ và xử lý ngoại lệ đề xuất |
|---|---|---|
| Nhận yêu cầu | Yêu cầu hợp lệ trước khi chuyển tiếp: kiểm tra đối tượng nhận, nhu cầu và điều kiện cấp phát theo quy tắc nội bộ cần được xác nhận/phê duyệt. | Yêu cầu và kết quả kiểm tra; trả lại hồ sơ thiếu hoặc chuyển trường hợp ngoài quy tắc đến người có thẩm quyền được xác định. |
| Lập phiếu | Phiếu phản ánh đúng yêu cầu: liên kết yêu cầu với định danh thiết bị, số lượng, đối tượng nhận và thông tin giao–trả cần thiết; đối chiếu trước khi dùng phiếu để giao. | Phiếu có mã tham chiếu, dấu vết rà soát và sửa đổi; làm rõ sai lệch trước khi giao. |
| Giao thiết bị | Thiết bị thực giao khớp phiếu: đối chiếu định danh, số lượng, tình trạng và phụ kiện nếu có; ghi nhận xác nhận giao–nhận tại thời điểm giao. | Biên bản/phiếu giao nhận ghi kết quả đối chiếu; ghi riêng sai lệch và quyết định xử lý, không mặc nhiên coi bên nhận đã chấp thuận. |
| Kiểm tra khi trả | Thiết bị trả được đối chiếu với hồ sơ giao về định danh, số lượng, tình trạng và phụ kiện; tiêu chí chấp nhận cần được phê duyệt. | Hồ sơ kiểm tra trả, kết quả và sai lệch; chuyển trường hợp thiếu/hỏng hoặc bất đồng sang xử lý ngoại lệ, giữ khả năng truy nguyên. |
| Giải quyết công nợ | Khoản xử lý có căn cứ: đối chiếu hồ sơ giao–trả, khoản đã ghi nhận và căn cứ tính/điều chỉnh được phép áp dụng trước khi xác nhận hoàn tất. | Bảng đối chiếu và chứng từ xử lý; khoản tranh chấp giữ riêng để giải quyết theo thẩm quyền. Không tự biến mọi thiếu/hỏng thành khoản phải thu. |

Owner, performer, reviewer, thẩm quyền ngoại lệ, hệ thống, thời hạn xử lý/lưu hồ sơ và ngưỡng quyết định: `Not provided`; cần xác nhận trước khi cụ thể hóa và phê duyệt SOP. Hồ sơ nêu trong bảng là bằng chứng đề xuất cần tạo, không phải bằng chứng đã nhận được. Chưa phân loại key control, chấm điểm rủi ro hoặc đánh giá hiệu quả vận hành.

Độ tin cậy về mức phù hợp của đề xuất: `Low`, vì mới có một câu mô tả quy trình. Chủ quy trình/người được giao thẩm quyền cần rà soát bối cảnh giao thiết bị, biểu mẫu, quy tắc công nợ và các kiểm soát hiện có; danh tính và thẩm quyền của người phê duyệt chưa được cung cấp. Bản này chưa được ban hành và không chứng minh tuân thủ tiêu chuẩn.

Để quay lại yêu cầu baseline theo Library C, cần cơ sở quyền phù hợp từ bên có quyền cho đúng nội dung và mục đích AI-use, làm rõ phạm vi đầu ra được phép, rồi mới cung cấp nội dung được phép xử lý để xác minh phiên bản, điều khoản và applicability. Không gửi toàn văn hoặc trích đoạn còn bị cấm. Một nguồn thay thế có quyền sử dụng phù hợp cũng có thể làm căn cứ; chưa có nguồn thay thế nào được tra cứu hoặc sử dụng ở đây.
