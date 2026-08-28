# Baseline và khoảng trống SOP — Site A, quý IV/2025

Không nên mặc định dùng bản mới nhất. Theo dữ liệu được cung cấp, baseline cho Site A trong quý IV/2025 là **Quy định nội bộ v1 — SRC-RULE-09A §2**: mọi thay đổi tài khoản người nhận phải được xác nhận độc lập trước lần thanh toán đầu tiên sau thay đổi.

Mục tiêu kiểm soát là bảo vệ tính đúng đắn của thanh toán khi tài khoản người nhận thay đổi. Phạm vi đánh giá giới hạn từ thay đổi tài khoản đến lần thanh toán đầu tiên; lớp phân tích là `As-Documented`, không phải kết luận về thực tế vận hành.

## 1. Baseline nào áp dụng?

| Nguồn | Hiệu lực, phạm vi và tính ràng buộc | Kết luận cho Site A, quý IV/2025 |
|---|---|---|
| SRC-RULE-09A §2 — v1 | Hiệu lực 01/01/2025; được áp dụng tại Site A trong năm 2025. Yêu cầu nội bộ bắt buộc theo dữ liệu cung cấp. | `Applicable`. Dùng yêu cầu xác nhận độc lập đối với mọi thay đổi tài khoản, trước thanh toán đầu tiên, làm tiêu chí đối chiếu. |
| SRC-RULE-09B §2 — v2 | Ban hành 01/03/2026; ngày hiệu lực riêng chưa được cung cấp. Chỉ có phạm vi pilot Site B, với cơ chế tự động đã cấu hình tại Site B. | `Not applicable` cho phạm vi/kỳ đang xét: khác thời điểm, khác site. Không có căn cứ hồi tố, mở rộng sang Site A hoặc coi v1 đã bị thay thế tại Site A trong năm 2025. |
| SRC-PRACTICE-09C §1 | Hướng dẫn ngành **hư cấu**, có tính advisory; Site A chưa adopt. Phiên bản/ngày hiệu lực chưa được cung cấp. | Không phải baseline bắt buộc. Kiểm tra liên tục chỉ là lựa chọn cải tiến có thể cân nhắc, không phải tiêu chí để kết luận SOP vi phạm. |
| SRC-SOP-09D §3 | SOP Site A trong hồ sơ viện dẫn “v2 một người duyệt”; thiếu ngày phê duyệt và quyết định mở rộng pilot. Phiên bản/ngày hiệu lực của SOP chưa được cung cấp. | Đây là tài liệu được đánh giá, không đủ thẩm quyền để tự thay đổi baseline. Việc chính bản SOP này đã có hiệu lực trong quý IV/2025 là `Unresolved`. |

V1 và v2 không nhất thiết mâu thuẫn với nhau: chúng có phạm vi và thời điểm khác nhau. Vấn đề là SOP Site A đang viện dẫn một cơ chế chưa có căn cứ áp dụng cho kỳ được đánh giá. “Mới hơn” và “ban hành” không đồng nghĩa với “đã có hiệu lực và được áp dụng tại đây”.

## 2. Khoảng trống và giới hạn kết luận

| Ghi nhận | Căn cứ và kết luận được phép | Xác minh/xử lý cần thiết |
|---|---|---|
| G-01 — Viện dẫn và mô tả coverage chưa phù hợp baseline | SRC-SOP-09D §3 viện dẫn v2 trong khi SRC-RULE-09A §2 áp dụng. Trích đoạn SOP chưa thể hiện cách đáp ứng đủ ba yếu tố: mọi thay đổi, xác nhận độc lập, trước thanh toán đầu tiên. Đây là khoảng trống tài liệu/đối chiếu yêu cầu nội bộ trong phạm vi đã đọc; chưa phải bằng chứng control không tồn tại. | Đối chiếu SOP đầy đủ và các control liên quan với v1. Dự thảo chỉnh viện dẫn và mô tả rõ cách đáp ứng từng yếu tố; trình người có thẩm quyền phê duyệt. |
| G-02 — Thiếu căn cứ về version, phê duyệt và phạm vi áp dụng | SRC-SOP-09D §3 không có ngày phê duyệt hay quyết định mở rộng pilot. Chưa xác nhận được bản SOP có hiệu lực trong quý IV/2025 hoặc quyền sử dụng cơ chế v2 tại Site A. | Thu bản SOP kiểm soát đúng kỳ, lịch sử phiên bản, hồ sơ phê duyệt/hiệu lực và quyết định ngoại lệ hoặc mở rộng nếu có. Không suy hồ sơ không được cung cấp là quyết định chắc chắn không tồn tại. |
| E-01 — Giới hạn bằng chứng vận hành | Nguồn nêu rõ không có operating evidence. `As-Designed` tại Site A và `As-Performed` trong quý IV/2025 chưa được chứng minh. | Nếu cần đánh giá tiếp, thu hồ sơ thay đổi tài khoản, dấu vết xác nhận độc lập, thời điểm thanh toán đầu tiên, cấu hình áp dụng tại Site A và ngoại lệ tương ứng. Đây là yêu cầu bằng chứng, không phải kiểm thử đã thực hiện. |

Không thể kết luận “một người duyệt” tự nó đồng nghĩa thiếu độc lập: cần xem toàn bộ cơ chế xác nhận và control thay thế. Tuy nhiên, cấu hình tự động tại **Site B** không chứng minh Site A có cơ chế tương đương; cũng không tự tạo quyền thay thế yêu cầu v1. Không kết luận operating failure, effectiveness hay actual SoD conflict từ SOP này.

## 3. Hướng xử lý

Đối với hồ sơ quý IV/2025, giữ v1 làm baseline và xử lý G-01/G-02 theo tài liệu đúng kỳ. Không hồi tố một bản SOP sửa hiện nay để chứng minh cách vận hành năm 2025. Nếu muốn dùng v2 cho Site A trong tương lai, cần xác nhận phạm vi phê duyệt, hiệu lực/chuyển tiếp, quan hệ thay thế và điều kiện cấu hình trước khi quyết định; không tự kéo dài v1 sang các kỳ chưa được cung cấp dữ liệu. Người phê duyệt/owner cụ thể chưa được cung cấp.

Nếu giữ nguyên viện dẫn thiếu căn cứ, người sử dụng có thể bỏ qua xác nhận độc lập, dẫn tới thanh toán vào tài khoản sai hoặc bị thay đổi trái phép. Đây là **kịch bản rủi ro**, không phải sự cố đã xảy ra. Bảo vệ hiện biết chỉ là yêu cầu v1 trên tài liệu; mức độ thực thi và control bổ sung tại Site A chưa rõ. Không có cơ sở chấm điểm rủi ro hoặc định lượng thiệt hại.

Mức tin cậy cao cho lựa chọn baseline trong phạm vi các trích đoạn đã cho; chưa đủ căn cứ về hiệu lực bản SOP và vận hành thực tế. Đây là đánh giá dự thảo, chưa phải kết luận tuân thủ hay assurance chính thức. Dữ liệu nguồn là dữ liệu tổng hợp, được phép đọc, dùng AI và lưu trong hồ sơ được chỉ định; không có xác minh độc lập nguồn gốc bên ngoài và không suy rộng quyền tái phân phối.
