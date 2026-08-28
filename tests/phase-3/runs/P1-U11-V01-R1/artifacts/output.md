# Đối chiếu SOP với giao dịch TX-11

TX-11 đã phát lệnh lúc 09:02 dù bước duyệt thứ hai được ghi `SKIPPED` lúc 09:01. Đây là sai lệch vận hành có bằng chứng so với SOP được cung cấp, trong đúng giao dịch này; không chỉ là thiếu dấu vết phê duyệt. Chưa đủ cơ sở kết luận `CTL-PAY-11` không hiệu quả cho các giao dịch khác hoặc toàn kỳ. [LOG-11 §1, rows 2–3; SOP-PAY-11 §3]

## Kiểm soát và ghi nhận theo lớp

Mục tiêu kiểm soát rút ra từ SOP: chỉ phát lệnh sau khi có duyệt của người quản lý, tiếp đó là duyệt của người phát hành độc lập. Phạm vi đối chiếu là khâu duyệt → phát lệnh của TX-11 ngày 02/07/2026, không phải toàn bộ chu trình thanh toán. Đầu vào là **dữ liệu tổng hợp, được phép phân tích trong AI**.

Giữ nguyên một logical `control_id: CTL-PAY-11`. Các `OBS-` dưới đây là ID ghi nhận phân tích mới, không phải hai kiểm soát khác nhau và không ghi đè nội dung SOP.

| control_observation_id | control_id | analysis_layer | Phạm vi/kỳ | Nội dung và căn cứ |
|---|---|---|---|---|
| OBS-PAY-11-AD | CTL-PAY-11 | As-Documented | SOP-PAY-11 §3; kỳ hiệu lực: Not provided | Người quản lý duyệt, sau đó người phát hành độc lập duyệt trước phát lệnh. Đây là quy định trên tài liệu, không chứng minh đã vận hành. |
| OBS-PAY-11-AP | CTL-PAY-11 | As-Performed | Duy nhất TX-11, 02/07/2026, 09:00–09:02 | 09:00 `manager_approval=APPROVED` [LOG-11 row 1]; 09:01 `second_approval=SKIPPED` [row 2]; 09:02 `payment_release=EXECUTED` [row 3]. LOG-11 §1 xác nhận export đầy đủ cho các bước duyệt/phát lệnh của riêng TX-11. |

Không tạo ghi nhận `As-Designed`: chưa có bằng chứng xác nhận cấu hình hoặc thiết kế hiện hành ngoài nội dung SOP. Không có thiết kế `Target-State` trong phạm vi yêu cầu này.

## Sai lệch cần theo dõi

`DEV-PAY-11-01` — `Operating Deviation`, liên kết `CTL-PAY-11`, đối chiếu `OBS-PAY-11-AD` với `OBS-PAY-11-AP`:

- Duyệt quản lý có trước phát lệnh, phù hợp về trình tự của bước này; log không chứng minh chất lượng hoặc thẩm quyền người duyệt.
- Duyệt thứ hai đã bị bỏ qua nhưng lệnh vẫn được phát. Xác định được một giao dịch có sai lệch; không tính tỷ lệ sai lệch toàn kỳ từ hồ sơ này.
- Nguyên nhân: `Not provided`. Tính được phép của ngoại lệ: `Unresolved`; hồ sơ không có quyết định chấp thuận ngoại lệ. Không tự suy rằng đây là ngoại lệ hợp lệ, hành vi gian lận hoặc lỗi cấu hình hệ thống.
- Tính độc lập giữa người quản lý và người phát hành: `Unresolved`, vì không có định danh người thực hiện/phân quyền. Chưa kết luận actual SoD conflict.

Rủi ro suy luận từ sai lệch: nếu tình trạng phát lệnh khi bỏ duyệt thứ hai tiếp diễn, giao dịch sai hoặc không hợp lệ có thể không được chặn trước khi phát lệnh, ảnh hưởng mục tiêu thanh toán được kiểm soát. Duyệt quản lý là lớp bảo vệ quan sát được ở TX-11, nhưng chưa có căn cứ coi nó thay thế tương đương cho duyệt độc lập. Chưa biết kiểm soát bù trừ hoặc thiệt hại thực tế; không lượng hóa rủi ro. [Căn cứ: SOP-PAY-11 §3; LOG-11 rows 1–3]

## Giới hạn và xác minh tiếp

Confidence: `Medium` cho các ghi nhận và đối chiếu trên, dựa trên bản tổng hợp được cung cấp; không kiểm tra trực tiếp hệ thống nguồn. Xác nhận completeness của LOG-11 được giữ đúng phạm vi TX-11, không nâng thành xác nhận độ tin cậy dữ liệu toàn kỳ. Phiên bản, chủ tài liệu và ngày hiệu lực SOP: `Not provided`; cần xác nhận bản áp dụng tại ngày giao dịch trước khi kết luận vi phạm yêu cầu hiện hành chính thức.

`design_assessment: Not assessed`; đánh giá operating effectiveness: `assessment_status: Not assessed`. Bằng chứng đủ cho ghi nhận sai lệch TX-11 nhưng không đủ cho kết luận OE rộng hơn. Chưa có phương pháp OE được phê duyệt, population toàn kỳ, phương án chọn mẫu/full-population và công việc kiểm tra độ tin cậy dữ liệu tương ứng. Không phát hành formal OE conclusion hoặc confirmed audit finding.

Đề nghị bổ sung lý do bỏ duyệt, quy tắc và quyết định ngoại lệ áp dụng cho TX-11, định danh/thẩm quyền người thực hiện, cùng bằng chứng kiểm soát bù trừ nếu có. Việc mở rộng kiểm tra và kết luận assurance cần người phụ trách assurance độc lập có thẩm quyền xác định phạm vi, phương pháp và phê duyệt. Người chịu trách nhiệm xử lý cụ thể và thời hạn: `To be validated`.

Trạng thái: bản phân tích dự thảo, `review_status: Not reviewed`.
