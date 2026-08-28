# Đánh giá key controls và phương án thay thế

C-21A là **ứng viên key control**, chưa phải designation đã được phê duyệt. C-21B không phải key control đối với rủi ro đổi tài khoản giả. C-21C là phương án tương lai có thể xem xét, nhưng chưa đủ căn cứ coi tương đương hoặc thay C-21A.

Phạm vi: từ nhận yêu cầu đổi tài khoản → cập nhật master data → phát lệnh thanh toán, tập trung vào lần thanh toán đầu sau thay đổi. Nguồn là [trích đoạn được cung cấp](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U21-V01/input.md>). Nguồn cảnh báo đây là dữ liệu tổng hợp, không phải tiêu chuẩn thật; quyền đọc, dùng AI và lưu/tái phân phối được nêu trong phạm vi bộ test.

## Căn cứ đánh giá

REF-21 §3 chỉ đưa ra outcome advisory: chỉ thanh toán vào tài khoản thuộc nhà cung cấp đã được xác thực; không bắt buộc một công nghệ. Vì vậy, callback hay dịch vụ kiểm tra quyền sở hữu là cách triển khai cần đánh giá theo outcome, không phải cơ chế bắt buộc do REF-21 quy định. Chưa có căn cứ adoption hoặc nghĩa vụ bắt buộc để kết luận compliance. Version, ngày hiệu lực và phạm vi tổ chức/kỳ áp dụng của các trích đoạn chưa được cung cấp; chưa xác nhận trạng thái hiện hành ngoài nội dung đã đọc.

BRIEF-21 §1 xác định rủi ro trọng yếu: yêu cầu thay tài khoản giả → dữ liệu tài khoản của kẻ gian được đưa vào luồng thanh toán → tiền có thể chuyển sai người nhận, gây thất thoát và làm sai mục tiêu thanh toán đúng nhà cung cấp. Đây là rủi ro được nguồn nêu, không phải bằng chứng gian lận đã xảy ra. Không chấm điểm inherent/residual risk vì chưa có thang và methodology được phê duyệt.

## Phân loại từng hoạt động

Các phân loại dưới đây là đề xuất phân tích, chờ tổ chức review và phê duyệt.

| ID, lớp và nguồn | Phân loại đề xuất | Căn cứ, vai trò và giới hạn |
|---|---|---|
| C-21A — `As-Documented`; SOP-21 §4 | Key-control candidate; preventive, manual | Người độc lập gọi số đã xác lập từ trước, xác nhận tài khoản và lưu ghi nhận trước lần thanh toán đầu sau thay đổi. Cơ chế này trực tiếp challenge yêu cầu giả trước khi tiền được chuyển. Trong bộ thông tin đã đọc, đây là cơ chế chính hướng tới rủi ro trọng yếu; chưa thấy phương án hiện hành tương đương được chứng minh. Nếu bỏ hoặc thực hiện sai, yêu cầu giả có thể dẫn đến thanh toán cho kẻ gian. |
| C-21B — `As-Documented`; SOP-21 §5 | Không key; hoạt động hỗ trợ trình bày báo cáo | Rà cách viết tên giúp báo cáo dễ đọc, nhưng không chứng minh quyền sở hữu tài khoản, tính xác thực của yêu cầu hay người nhận tiền. Đối với rủi ro đổi tài khoản giả, đây là `Non-Control Activity`, chưa đủ căn cứ gọi là supporting risk control cho C-21A. Chỉ xem xét supporting control cho một mục tiêu chất lượng dữ liệu riêng nếu có criteria, risk linkage và reliance được xác nhận. Không thể dùng B để bù hoặc thay A. |
| C-21C — `Target-State`, dự kiến; DESIGN-21 §2 | Candidate alternative; chưa phải current, key hoặc compensating control đã được chấp thuận | Kết hợp kiểm tra quyền sở hữu tài khoản với xác nhận ngoài luồng có thể hướng tới cùng outcome. Tuy nhiên, chưa kiểm thử coverage và chưa có quyết định thay A. Không cộng C vào protection hiện tại; không coi C tốt hơn chỉ vì sử dụng dịch vụ/công nghệ. |

Keyness của A dựa trên chuỗi REF-21 §3 → outcome xác thực người nhận → rủi ro trọng yếu BRIEF-21 §1 → cơ chế xác nhận độc lập SOP-21 §4, không dựa đơn thuần vào việc control có trong SOP. Cần xác nhận thêm mức reliance thực tế của quyết định phát lệnh thanh toán, các control khác ngoài trích đoạn và người có quyền phê duyệt designation.

Confidence của phân loại A/B: `Medium`, có căn cứ trực tiếp trong trích đoạn nhưng chưa đối chứng triển khai. Tính tương đương của C: `Unresolved`. Không có operating evidence; `As-Performed: Not assessed`, `evidence_status: Insufficient evidence` cho cả ba. Không suy từ đó rằng control thất bại.

## Điều kiện để C-21C thay thế C-21A

Đây là điều kiện kiểm chứng/thiết kế đề xuất, không phải yêu cầu công nghệ của REF-21 và không phải kết quả test đã thực hiện:

1. **Coverage và precision:** chứng minh dịch vụ xác nhận đúng quan hệ nhà cung cấp–chủ tài khoản, không chỉ kiểm tra cách viết tên. Xác định population thuộc phạm vi, các trường hợp không được dịch vụ hỗ trợ và tiêu chí xử lý kết quả không rõ; so sánh với coverage của A trên cùng phạm vi.
2. **Timing và liên kết dữ liệu:** hoàn tất xác minh trước phát lệnh thanh toán đầu sau thay đổi; chứng minh tài khoản thực sự dùng thanh toán là tài khoản đã được xác minh, kể cả khi dữ liệu được thay đổi tiếp sau kiểm tra.
3. **Independence và common-mode failure:** xác nhận ngoài luồng phải dùng nguồn liên hệ đáng tin cậy, độc lập với yêu cầu đổi tài khoản đang kiểm tra. Hai phép kiểm tra cùng phụ thuộc một đầu vào giả không tự tạo hai lớp bảo vệ độc lập.
4. **Exception và khả năng duy trì:** thiết kế tuyến xử lý khi sai khớp, không xác minh được, dịch vụ gián đoạn hoặc ngoài coverage. Đề xuất chưa phát lệnh khi chưa xác minh được tài khoản; xử lý exception/fallback theo quy tắc được phê duyệt và bảo toàn control objective, không tự động bỏ qua control. Cần đánh giá dữ liệu, tích hợp, thay đổi cấu hình, khả năng override, capacity và phụ thuộc dịch vụ.
5. **Evidence và testability:** quy định người chịu trách nhiệm, người thực hiện độc lập, tiêu chí chấp nhận, dấu thời gian, tài khoản kiểm tra, kết quả, exception và quyết định cho phép thanh toán; xác định lưu giữ và truy xuất bằng chứng. Kiểm thử theo objective, population và methodology được phê duyệt; chưa ấn định cỡ mẫu hoặc ngưỡng.
6. **Approval và chuyển đổi:** chỉ thay A sau khi kết quả kiểm chứng coverage tương đương hoặc tốt hơn trong phạm vi chấp thuận được review, residual exposure được xem xét và đúng người có thẩm quyền phê duyệt. Cần quyết định keyness của control set mới, cập nhật SOP và có kế hoạch chuyển đổi/rollback. Người phê duyệt và căn cứ thẩm quyền: `Not provided`.

## Phương án và đề xuất

- **Giữ A, làm rõ thiết kế:** duy trì cơ chế theo SOP trong khi làm rõ sự độc lập, quản trị số liên hệ, liên kết xác nhận với lệnh thanh toán và xử lý exception. Những điểm này chưa mô tả trong trích đoạn; chưa chứng minh là thiếu trong thực tế. Phương án vẫn phụ thuộc người thực hiện và dữ liệu liên hệ.
- **Thử C như lớp bổ sung:** có thể tăng kiểm tra trực tiếp quyền sở hữu và tạo dữ liệu so sánh, nhưng thêm công việc, chi phí và phụ thuộc dịch vụ. Trong giai đoạn chưa được chấp thuận thay thế, không dừng A; không mặc định hai cơ chế tạo giá trị tăng thêm nếu trùng coverage hoặc cùng điểm yếu.
- **Thay A bằng C có điều kiện:** chỉ cân nhắc sau các gate trên. Lợi ích giảm thao tác lặp hoặc tăng coverage phải được chứng minh; chưa có dữ liệu về chi phí, volume, nguồn lực và thời gian triển khai để chọn phương án công nghệ.

Khuyến nghị hiện tại: giữ A làm ứng viên key control để review, không dựa vào B cho rủi ro gian lận tài khoản và tiếp tục đánh giá C có điều kiện. Nếu giữ nguyên, protection được mô tả vẫn là A; exposure nếu xác nhận bị bỏ qua, sai hoặc dùng nguồn liên hệ không đáng tin chỉ là kịch bản cần xác minh, không phải observed operating deviation. Mọi thay đổi và designation đều ở trạng thái dự thảo, chưa có business approval. Cách phân lớp, tách key candidate khỏi approval và giữ điều kiện tương đương của phương án thay thế được áp dụng theo skill `thien-skill-risk-process-control`.
