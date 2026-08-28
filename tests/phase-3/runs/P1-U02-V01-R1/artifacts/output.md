# Định hình quy trình cho mượn hiện vật

Nên định hình một E2E riêng: **“Yêu cầu mượn hiện vật → hoàn trả, đối chiếu tình trạng và khép trách nhiệm”**. Đây là tên đề xuất cho bảo tàng, không phải tên hoặc mã chuẩn của một thư viện. Không cần chờ chọn thư viện mới xác định được ranh giới theo mục tiêu.

Mục tiêu nguồn nêu là **hoàn trả đúng hiện vật, với hồ sơ tình trạng và trách nhiệm được đối chiếu**; vì vậy kết thúc ở “giao hiện vật” hay “kết thúc trưng bày” đều chưa đủ. [SRC-MUSEUM-02 §2]

## 1. Ranh giới và cấu trúc E2E

- **Bắt đầu:** nhận yêu cầu mượn; đầu vào là yêu cầu và thông tin hiện vật/điều kiện mượn cần làm rõ. Việc nhận yêu cầu có trong nguồn; bộ trường thông tin cụ thể chưa được cung cấp. [§1]
- **Kết thúc đề xuất:** nhận lại đúng hiện vật, hoàn tất đối chiếu tình trạng và trách nhiệm; nếu có tổn hại/chênh lệch, phải có kết quả xử lý được người có thẩm quyền chấp thuận trước khi khép hồ sơ.
- **Xuyên chức năng:** bao phủ các bàn giao giữa bảo tàng, bộ phận bảo quản, đơn vị vận chuyển và đơn vị mượn; không chia thành các quy trình rời chỉ theo bên tham gia. [§1–2]
- **Giới hạn:** chỉ định hình vòng cho mượn–hoàn trả, không mở rộng sang toàn bộ vòng đời sưu tập, mua sắm hoặc thanh lý. Giữ mức E2E; phân cấp vào kiến trúc L0–L5 của bảo tàng còn `To be validated`.

Bảng dưới tách rõ mô tả nguồn và thiết kế đề xuất; không phải bản đồ hoạt động thực tế đã kiểm chứng.

| Chặng | As-Documented — nguồn đang mô tả | Target-State — kết quả cần chốt, bản nháp |
|---|---|---|
| Xét yêu cầu | Nhận yêu cầu, xem điều kiện bảo quản. [§1] | Có quyết định cho mượn, yêu cầu bổ sung hoặc từ chối dựa trên tiêu chí và thẩm quyền được phê duyệt. |
| Chuẩn bị giao | Thỏa thuận trách nhiệm, ghi tình trạng trước giao; hồ sơ mô tả ảnh trước/sau. [§1, §3] | Nhận diện rõ từng hiện vật; có hồ sơ tình trạng gốc, điều kiện chấp nhận và trách nhiệm bàn giao thống nhất trước khi giao. |
| Vận chuyển và trưng bày | Vận chuyển, trưng bày; các bên có bàn giao riêng. [§1–2] | Theo được bên đang giữ hiện vật, thời điểm chuyển giao, tình trạng khi giao/nhận và ngoại lệ phát sinh. |
| Thu hồi và đối chiếu | Hoàn trả, đối chiếu tình trạng sau nhận. [§1–2] | Đối chiếu đúng hiện vật và tình trạng với hồ sơ gốc; ghi kết quả phù hợp hoặc chênh lệch theo tiêu chí được duyệt. |
| Khép hồ sơ/ngoại lệ | Chưa được cung cấp cơ chế xử lý tổn hại. [§3] | Trường hợp phù hợp được khép hồ sơ; trường hợp có tổn hại giữ trạng thái mở, bảo toàn chứng cứ, xác định trách nhiệm và theo dõi đến quyết định xử lý. |

Đề xuất chỉ định một Process Owner chịu trách nhiệm xuyên suốt; người/vai trò cụ thể và thẩm quyền hiện là `Not provided`, không tự mặc định bộ phận bảo quản là owner.

## 2. Các rủi ro chính

Các kịch bản dưới đây là **suy luận rủi ro (`Inferred`) từ mô tả nguồn**, không phải sự cố hoặc sai phạm đã xảy ra. Mỗi hướng kiểm soát là **Target-State, draft**, cần xác nhận thiết kế và người chịu trách nhiệm.

| Chặng và căn cứ | Nguyên nhân → sự kiện → tác động đến mục tiêu | Mục tiêu kiểm soát/định hướng đề xuất |
|---|---|---|
| Xét điều kiện; vận chuyển, trưng bày. [§1] | Nếu đánh giá điều kiện không bao phủ đầy đủ hành trình và nơi trưng bày, hiện vật có thể chịu điều kiện không phù hợp hoặc bị tổn hại, làm sai lệch tình trạng khi hoàn trả. | Xác định điều kiện bảo quản/di chuyển phù hợp với từng hiện vật và cách xử lý khi điều kiện không còn đáp ứng; tiêu chí chuyên môn chưa được cung cấp. |
| Các bàn giao riêng. [§2] | Nếu nhận diện hiện vật và trách nhiệm giữ hiện vật không nối được giữa các bàn giao, có thể giao/nhận nhầm hoặc thất lạc mà không xác định được điểm phát sinh, ảnh hưởng việc thu hồi đúng hiện vật. | Dùng nhận diện nhất quán và hồ sơ giao–nhận liên kết xuyên các bên; xác nhận hiện vật, tình trạng, bên giao/nhận và thời điểm tại mỗi bàn giao. |
| Ghi nhận trước/sau, đối chiếu khi nhận. [§1, §3] | Nếu ảnh không đủ để so sánh hoặc không có tiêu chí đối chiếu rõ, chênh lệch có thể bị bỏ sót hay đánh giá không nhất quán, khiến hồ sơ tình trạng không hỗ trợ được kết luận nhận lại. | Gắn ảnh với đúng hiện vật và thời điểm; bổ sung mô tả tình trạng, tiêu chí đánh giá và kết quả đối chiếu, không dùng việc “có ảnh” thay kết luận kiểm tra. |
| Thỏa thuận trách nhiệm và xử lý tổn hại. [§1–3] | Nếu trách nhiệm tại từng chặng và cách xử lý tổn hại không rõ, khi phát sinh chênh lệch các bên có thể tranh chấp hoặc để vụ việc kéo dài, khiến trách nhiệm không được khép. | Làm rõ điểm chuyển trách nhiệm, cách thông báo, bằng chứng cần giữ, đầu mối quyết định và điều kiện đóng ngoại lệ trong thỏa thuận/quy trình được duyệt. |
| Hoàn trả. [§1–2] | Nếu mốc hoàn trả và đầu mối theo dõi không rõ, hiện vật có thể chậm hoặc không được thu hồi, khiến vòng cho mượn và hồ sơ trách nhiệm còn mở. | Quản lý mốc hoàn trả đã thỏa thuận và đường xử lý khi không đáp ứng; mốc, thời hạn và cơ chế hiện hành chưa được cung cấp. |

Nguồn đã mô tả một số lớp bảo vệ: xem điều kiện bảo quản, thỏa thuận trách nhiệm và ghi nhận/đối chiếu tình trạng. Chưa có bằng chứng để kết luận chúng vận hành hiệu quả. **§3 chỉ chứng minh giới hạn hồ sơ được cung cấp**, không chứng minh ngoài thực tế không có tiêu chí hoặc cơ chế xử lý.

Nếu thực tế cũng chỉ dừng ở ảnh trước/sau và chưa có cơ chế bổ sung, tổn hại có thể khó đánh giá hoặc quy trách nhiệm dù đã chụp ảnh. Đây là kịch bản cần xác minh, chưa phải kết luận về rủi ro tồn dư.

## 3. Chưa chọn thư viện: tiếp tục thế nào?

Trước mắt giữ mô hình riêng theo mục tiêu trên. Khi chọn nguồn tham chiếu, ưu tiên nguồn chuyên ngành quản lý sưu tập/cho mượn hiện vật, đối chiếu **mục tiêu, trigger, outcome và bàn giao**, không chỉ tên quy trình. Taxonomy hỗ trợ phân loại, không tự quyết định thứ tự công việc hoặc kiểm soát bắt buộc.

Trong phạm vi này chưa tra cứu nguồn ngoài: thư viện, phiên bản, item ID và mapping đều chưa được xác minh; không gán mã tham chiếu hay tuyên bố phù hợp tiêu chuẩn.

Ba việc cần xác nhận để hoàn thiện bản nháp:

1. Tiêu chí chấp nhận tình trạng, hồ sơ đối chiếu và thẩm quyền quyết định khi có khác biệt.
2. Cách chuyển trách nhiệm giữa các bên, mốc hoàn trả và luồng xử lý tổn hại thực tế.
3. Process Owner và một bộ hồ sơ cho mượn–hoàn trả xuyên suốt để kiểm tra các bàn giao; đây là xác minh hiện trạng, không thay đánh giá hiệu quả vận hành toàn kỳ.

*Phạm vi bằng chứng:* SRC-MUSEUM-02 §1–3 là dữ liệu tổng hợp, được phép phân tích trong AI. Phiên bản, chủ sở hữu, hiệu lực/phê duyệt nguồn, hệ thống và bằng chứng vận hành: `Not provided`. “As-Documented” ở đây chỉ là nội dung mô tả đã nhận, không khẳng định đó là SOP đã ban hành. Confidence đối với hiện trạng: `Low` do chỉ có mô tả chưa kiểm chứng; As-Designed/As-Performed chưa xác nhận. Chưa có phương pháp được duyệt nên không chấm điểm rủi ro. Tất cả đề xuất cần review/phê duyệt bởi người có thẩm quyền; chưa phải quy trình chính thức.

