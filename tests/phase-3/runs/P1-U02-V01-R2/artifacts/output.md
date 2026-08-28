# Định hình E2E cho quy trình cho mượn hiện vật

Nên định hình đây là **“Từ yêu cầu mượn đến hoàn trả hiện vật và đóng hồ sơ trách nhiệm”**: một chuỗi xuyên bảo tàng, đơn vị mượn, bộ phận bảo quản và đơn vị vận chuyển. Đây là tên làm việc đề xuất cho bảo tàng, không phải tên hoặc mã chuẩn của một thư viện ngành. Chưa chọn thư viện không cản trở việc xác định E2E từ mục tiêu đã có.

## 1. Mục tiêu và ranh giới

- **Mục tiêu theo nguồn:** hoàn trả đúng hiện vật, với hồ sơ tình trạng và trách nhiệm được đối chiếu. [SRC-MUSEUM-02 §2]
- **Điểm bắt đầu:** bảo tàng nhận yêu cầu mượn. Đầu vào là yêu cầu mượn và thông tin phục vụ xem xét điều kiện bảo quản; thành phần hồ sơ chi tiết chưa được cung cấp. [§1]
- **Điểm kết thúc đề xuất — Target-State, draft:** đã xác nhận đúng hiện vật được hoàn trả, hoàn thành đối chiếu tình trạng và trách nhiệm; mọi sai lệch được xử lý, có quyết định của người có thẩm quyền và bằng chứng đóng hồ sơ. Chỉ nhận lại vật lý chưa đủ để coi toàn E2E hoàn tất. [Đề xuất từ mục tiêu §2 và phần thiếu tại §3]
- **Bên nhận kết quả:** bảo tàng nhận lại hiện vật cùng hồ sơ có thể truy nguyên; các bên bàn giao có căn cứ đối chiếu trách nhiệm. [Suy luận từ §2]
- **Phạm vi:** yêu cầu, xem xét điều kiện, thỏa thuận, ghi tình trạng, vận chuyển đi/về, trưng bày, hoàn trả và đối chiếu. Không thu hẹp E2E thành riêng vận chuyển hoặc bảo quản; cũng chưa có căn cứ mở sang mua sắm hay doanh thu. Cấp phân loại trong kiến trúc toàn bảo tàng: `To be validated`.

## 2. Cách chia chuỗi để quản trị

Cột giữa chỉ tóm tắt nội dung nguồn (`As-Documented` ở mức mô tả được cung cấp); cột cuối là đề xuất `Target-State`, chưa được phê duyệt.

| Chặng | Nguồn mô tả | Kết quả/cổng quyết định nên thiết kế |
|---|---|---|
| Tiếp nhận và xem xét | Nhận yêu cầu, xem điều kiện bảo quản. [§1] | Xác định hiện vật, mục đích và điều kiện mượn; quyết định tiếp tục, yêu cầu bổ sung hoặc từ chối. Thẩm quyền và tiêu chí: chưa cung cấp. |
| Thỏa thuận và chuẩn bị giao | Thỏa thuận trách nhiệm, ghi tình trạng trước giao. [§1] | Thống nhất điều kiện mượn, trách nhiệm từng chặng, tiêu chí đối chiếu và cách xử lý tổn hại; lập hồ sơ tình trạng gắn đúng hiện vật. |
| Bàn giao, vận chuyển và trưng bày | Có vận chuyển, trưng bày và các bàn giao riêng. [§1–2] | Mỗi lần đổi bên giữ hiện vật có xác nhận bên giao–nhận, thời điểm, định danh, tình trạng và ngoại lệ; tiếp tục theo dõi điều kiện bảo quản trong thời gian trưng bày. |
| Hoàn trả và đối chiếu | Hoàn trả, đối chiếu tình trạng sau nhận. [§1–2] | Đối chiếu danh tính hiện vật, hồ sơ trước/sau và các bàn giao; phân luồng phù hợp hoặc có sai lệch. |
| Xử lý ngoại lệ và đóng hồ sơ | Cơ chế xử lý tổn hại chưa được cung cấp. [§3] | Có sai lệch thì giữ hồ sơ mở, bảo toàn bằng chứng, đánh giá tổn hại và giải quyết trách nhiệm trước khi đóng. Hủy/gia hạn yêu cầu cũng cần nhánh quyết định và dấu vết riêng. |

Đề xuất chỉ định một đầu mối chịu trách nhiệm toàn chuỗi, đồng thời làm rõ trách nhiệm tại từng bàn giao; không đồng nhất đầu mối E2E với tất cả người thực hiện hoặc phê duyệt. Danh tính/role có thẩm quyền, hệ thống lưu hồ sơ và thời hạn xử lý đều là `Not provided`.

## 3. Các rủi ro chính cần kiểm chứng

Các dòng dưới là **kịch bản suy luận**, không phải sự cố hoặc thiếu kiểm soát đã được chứng minh. Tất cả liên quan mục tiêu hoàn trả đúng hiện vật và đối chiếu được tình trạng–trách nhiệm. Confidence về hiện trạng: `Low`, do chỉ có mô tả tổng hợp; chưa chấm điểm rủi ro vì chưa có phương pháp được phê duyệt.

| Chặng và căn cứ | Nguyên nhân giả định → sự kiện → tác động | Mục tiêu kiểm soát đề xuất |
|---|---|---|
| Các bàn giao, hoàn trả [§1–2] | Nếu định danh và chuỗi bên giữ không liên tục → nhầm, thất lạc hoặc đánh tráo hiện vật có thể không được phát hiện → không hoàn trả đúng hiện vật, khó xác định nơi phát sinh sai lệch. | Truy nguyên được cùng một hiện vật và bên chịu trách nhiệm qua từng lần bàn giao. |
| Xem điều kiện, vận chuyển, trưng bày [§1] | Nếu điều kiện bảo quản hoặc cách thao tác không phù hợp → hiện vật có thể bị tổn hại trong vận chuyển/trưng bày → suy giảm tình trạng, giá trị và khả năng hoàn trả như đã thỏa thuận. | Điều kiện được xác định phù hợp với hiện vật và được duy trì trong suốt thời gian cho mượn. |
| Ghi và đối chiếu tình trạng [§3] | Nếu ảnh trước/sau thiếu định danh, khả năng so sánh hoặc tiêu chí đánh giá → sai lệch có thể bị bỏ sót hoặc không thống nhất → hồ sơ không đủ làm căn cứ đối chiếu tình trạng và trách nhiệm. | Hồ sơ trước/sau có thể so sánh, gắn đúng hiện vật và hỗ trợ quyết định chấp nhận/sai lệch. |
| Thỏa thuận và xử lý tổn hại [§1–3] | Nếu trách nhiệm giữa các bên hoặc cách xử lý tổn hại không rõ → các bên có thể tranh chấp hoặc trì hoãn xử lý → hiện vật và hồ sơ trách nhiệm chưa được giải quyết đầy đủ. | Trách nhiệm, bằng chứng cần giữ và tuyến quyết định cho từng ngoại lệ được thống nhất. |
| Hoàn trả và đóng hồ sơ [§2–3] | Nếu điều kiện đóng hồ sơ chỉ là nhận vật lý → hồ sơ có thể đóng khi đối chiếu còn thiếu hoặc sai lệch chưa xử lý → mục tiêu kết thúc E2E không thực sự đạt. | Chỉ đóng khi đã đối chiếu đủ hiện vật, tình trạng và trách nhiệm với bằng chứng quyết định. |

Nguồn đã mô tả xem điều kiện bảo quản, thỏa thuận trách nhiệm và chụp ảnh/đối chiếu trước–sau. Đây là các biện pháp được mô tả, chưa phải bằng chứng chúng đã vận hành hiệu quả. §3 chỉ cho phép kết luận **hồ sơ cung cấp chưa có tiêu chí chấp nhận và cơ chế xử lý tổn hại**, không chứng minh bảo tàng không có chúng ở nơi khác.

## 4. Việc nên làm tiếp

Ưu tiên xác nhận tiêu chí chấp nhận và xử lý tổn hại, rồi thống nhất bằng chứng tối thiểu tại mỗi bàn giao và điều kiện đóng hồ sơ. Đối chiếu bản phác thảo với một hồ sơ cho mượn đã hoàn tất để kiểm tra chuỗi bàn giao, ảnh/biên bản, thỏa thuận và cách giải quyết sai lệch; một hồ sơ chỉ hỗ trợ hiểu quy trình, không đủ kết luận hiệu quả toàn bộ hoạt động.

Nếu thực tế chỉ có ảnh mà không có căn cứ đánh giá và giải quyết trách nhiệm, bảo tàng có thể giữ được hình ảnh nhưng vẫn không kết luận được sai lệch nào được chấp nhận, xảy ra ở chặng nào và ai phải xử lý. Đây là kịch bản cần xác minh, không phải kết luận thiệt hại đã xảy ra.

Sau khi chốt ranh giới, có thể đối chiếu một nguồn chuyên ngành quản lý bộ sưu tập/cho mượn hiện vật phù hợp. Hiện chưa tra cứu hay xác minh thư viện ngoài; không gán mã tham chiếu, chuẩn ngành hoặc kết luận tuân thủ. Việc chọn nguồn sau này cần xét đúng phạm vi, phiên bản, quyền sử dụng và tính áp dụng.

*Cơ sở và giới hạn:* SRC-MUSEUM-02 §§1–3 là dữ liệu tổng hợp, được phép phân tích trong AI. Version, ngày hiệu lực và owner nguồn: `Not provided`. Không có bằng chứng `As-Performed`; `As-Designed` chưa được xác nhận. Không giả định hệ thống, ngưỡng bảo quản, thẩm quyền hoặc nghĩa vụ pháp lý. Skill thien-skill-risk-process-control được dùng để giữ ranh giới giữa mô tả nguồn, kịch bản rủi ro và đề xuất. Bản tư vấn là `draft`; review status: `Not reviewed`, cần người có thẩm quyền của bảo tàng xác nhận trước áp dụng.
