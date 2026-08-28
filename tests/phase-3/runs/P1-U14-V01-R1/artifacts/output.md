# Rủi ro nếu không khắc phục và hướng xử lý

Tại **09:00 ngày 02/07/2026**, tài khoản E-14 được ghi nhận còn **ENABLED**, trong khi ngày làm việc cuối cùng là 01/07/2026 và POL-14 §2 yêu cầu vô hiệu hóa trước khi kết thúc ngày đó. Đây là sai lệch trạng thái cần xử lý trong trường hợp đã quan sát; **chưa có bằng chứng truy cập trái phép hoặc thiệt hại**. Đề nghị kiểm tra trạng thái hiện tại và chuyển xử lý cho người có thẩm quyền, không chờ kỳ đối chiếu cuối tuần.

Mục tiêu kiểm soát là chấm dứt quyền truy cập đúng thời điểm nghỉ việc và có bằng chứng xác nhận hoàn tất. Phạm vi xem xét: từ thông báo nghỉ việc đến vô hiệu hóa và xác nhận kết quả; bằng chứng thực tế hiện chỉ bao phủ E-14 tại thời điểm nêu trên.

## 1. Căn cứ và giới hạn

| Lớp phân tích | Nguồn | Điều có thể kết luận |
|---|---|---|
| As-Documented | POL-14 §2 | Yêu cầu nội bộ áp dụng: vô hiệu hóa trước khi kết thúc ngày làm việc cuối cùng. Đây không phải căn cứ để kết luận vi phạm pháp luật. |
| As-Documented | SOP-14 §4 | Quản lý gửi danh sách; nhóm tài khoản xử lý email và đối chiếu cuối tuần. Đoạn cung cấp chưa làm rõ thời hạn xử lý từng tài khoản, xác nhận hoàn tất và escalation. Không suy rằng SOP cho phép đợi đến cuối tuần mới vô hiệu hóa. |
| As-Performed, theo dữ liệu tổng hợp được cung cấp | HR-14; LOG-14, 09:00 ngày 02/07/2026 | Email đã đến nhóm tài khoản; E-14 còn ENABLED tại một thời điểm sau ngày nghỉ. Chưa biết thời điểm nhận email, lịch sử vô hiệu hóa/tái kích hoạt hoặc hoạt động đăng nhập. |
| Chưa xác nhận | Hồ sơ đối chiếu và cấu hình hệ thống | Không có biên bản đối chiếu trong hồ sơ không chứng minh đối chiếu chưa thực hiện. As-Designed và các lớp chặn truy cập khác chưa được cung cấp. |

Mức tin cậy: **Medium**, giới hạn ở nội dung tổng hợp đã đọc; chưa kiểm tra email/log gốc. Không suy tài khoản ENABLED liên tục từ lúc nghỉ đến lúc kiểm tra, không suy sai lệch của toàn bộ nhân viên nghỉ việc hoặc kết luận hiệu quả vận hành toàn kỳ. Nguyên nhân gốc: **Unresolved**.

## 2. Nếu giữ nguyên, rủi ro gì có thể xảy ra?

Các nội dung sau là **kịch bản rủi ro suy luận**, không phải sự cố đã được chứng minh:

- **Truy cập không còn được phép:** nếu tài khoản tiếp tục ENABLED và thông tin xác thực còn sử dụng được, người nghỉ việc hoặc người khác nắm thông tin đó có thể truy cập trong phạm vi quyền còn lại → xem/sao chép dữ liệu, sửa/xóa thông tin hoặc mạo danh thực hiện thao tác → ảnh hưởng bảo mật, tính toàn vẹn dữ liệu và hoạt động kinh doanh. Mức ảnh hưởng phụ thuộc quyền thực tế và các lớp bảo vệ khác; hiện chưa biết.
- **Tái diễn chậm thu hồi quyền:** nếu nguyên nhân khiến trường hợp E-14 chưa đạt trạng thái yêu cầu không được xử lý, các hồ sơ nghỉ việc khác có thể tiếp tục vượt mốc POL-14 → kéo dài cơ hội truy cập ngoài thẩm quyền và phát sinh công việc xử lý ngoại lệ. Chưa có population hoặc dữ liệu để xác định mức phổ biến.
- **Khó xác minh và xử lý hậu quả:** nếu không thu thập, bảo toàn dấu vết thay đổi và sử dụng tài khoản, việc xác định ai đã thao tác, thời điểm và phạm vi ảnh hưởng có thể bị hạn chế → chậm điều tra nội bộ và khôi phục nếu thực sự có sự cố. Việc chưa được cung cấp log không chứng minh hệ thống không lưu log.

**Bảo vệ hiện biết:** có yêu cầu POL-14, thông báo đã đến nhóm xử lý và cơ chế đối chiếu cuối tuần được SOP mô tả. Tuy nhiên, thông báo không chứng minh vô hiệu hóa đã hoàn tất; đối chiếu cuối tuần chưa có bằng chứng thực hiện và tự nó không bảo đảm phòng ngừa truy cập trước thời điểm đối chiếu. Không tính biện pháp đề xuất bên dưới là bảo vệ đang có.

Phơi nhiễm còn lại là khả năng sử dụng quyền sau khi nghỉ việc nếu đường truy cập vẫn khả dụng. Xác suất, tổn thất, phương pháp rating, risk appetite và time horizon đều **Not provided**; không gán mức cao/thấp, điểm inherent/residual hay ước tính tiền. Thiếu dữ liệu không có nghĩa rủi ro thấp.

## 3. Biện pháp tạm thời — Target-State, dự thảo cần phê duyệt

1. **Xử lý trường hợp E-14:** đề nghị nhóm tài khoản xác minh đúng định danh và trạng thái hiện tại. Nếu còn ENABLED, người có quyền thực hiện vô hiệu hóa theo quy trình được phép; lưu trạng thái trước/sau, thời điểm và người thực hiện. Yêu cầu người được giao kiểm tra kết quả. Nếu hệ thống có phiên truy cập/token hoặc tài khoản liên quan, đội kỹ thuật xác định phạm vi và xử lý theo thẩm quyền; không mặc định một thao tác đã thu hồi mọi đường truy cập.
2. **Nếu chưa thể vô hiệu hóa:** ghi nhận nguyên nhân, chuyển ngay ngoại lệ cho cấp có thẩm quyền và đề xuất chặn truy cập bằng biện pháp thay thế khả dụng đã được duyệt. Phải nêu phạm vi được chặn, phần còn hở, người theo dõi và thời điểm hết hiệu lực/đánh giá lại do người có thẩm quyền quyết định. Giám sát tăng cường chỉ hỗ trợ phát hiện, không thay thế vô hiệu hóa và không hợp thức hóa việc quá mốc POL-14.
3. **Bảo toàn và kiểm tra bằng chứng:** đề nghị bên được phép thu thập lịch sử trạng thái tài khoản, log xác thực và hoạt động liên quan đến mốc nghỉ việc đến lúc thu hồi được xác nhận; ghi rõ khoảng thiếu và độ phủ log. Không xóa tài khoản hoặc dữ liệu làm mất dấu vết. Nếu thấy dấu hiệu bất thường, chuyển xử lý sự cố theo quy trình hiện hành; chưa cáo buộc E-14 có hành vi sai phạm.
4. **Theo dõi tạm từng hồ sơ đến hạn:** đề xuất danh sách kiểm soát gắn ngày nghỉ, tài khoản, người tiếp nhận, hạn theo POL-14 và bằng chứng hoàn tất; xác nhận kết quả trước mốc bắt buộc, chuyển ngoại lệ khi có nguy cơ trễ. Phân công người thực hiện, người thay thế và nhịp theo dõi phải được duyệt; không chỉ dựa vào kỳ đối chiếu cuối tuần.

Các biện pháp này chưa được thực thi. Người chịu trách nhiệm cuối cùng, người phê duyệt ngoại lệ và ngày hoàn tất khắc phục cụ thể: **Not provided**; cần phân công theo thẩm quyền của tổ chức.

## 4. Hướng khắc phục và điều kiện đóng

- **Xác minh nguyên nhân trước khi quy trách nhiệm:** đối chiếu thời điểm gửi/nhận email, phân công xử lý, hồ sơ công việc, lịch sử thay đổi trạng thái và ngoại lệ được duyệt nếu có. Các khả năng bỏ sót email, chậm phân công, lỗi thao tác hoặc tái kích hoạt chỉ là giả thuyết.
- **Chuẩn hóa SOP theo kết quả POL-14:** làm rõ chuỗi thông báo → tiếp nhận → xác định tài khoản và hạn → vô hiệu hóa → xác nhận kết quả → lưu bằng chứng. Bổ sung đường xử lý thông báo muộn, lỗi kỹ thuật và người xử lý vắng mặt. Đối chiếu cuối tuần có thể là lớp kiểm tra bổ sung, không thay cho hoàn tất từng hồ sơ đúng hạn.
- **Chọn cách triển khai phù hợp:** theo dõi thủ công có kiểm soát là phương án cần ít tích hợp hơn nhưng phụ thuộc năng lực và kỷ luật theo dõi. Workflow tích hợp có thể hỗ trợ nhắc hạn và xác nhận nhưng chỉ nên cân nhắc khi định danh, dữ liệu nghỉ việc, logic ngoại lệ và trách nhiệm đã rõ; cần kiểm thử, quản trị thay đổi và đường xử lý lỗi. Chưa đủ dữ liệu để chọn tự động hóa, ước tính chi phí hoặc thời gian triển khai.
- **Đóng có bằng chứng:** trường hợp E-14 cần xác nhận trạng thái và phạm vi thu hồi thực tế, hồ sơ xử lý, kết quả rà soát dấu vết cùng những khoảng chưa xác minh. Khắc phục quy trình cần SOP được phê duyệt và bằng chứng các hồ sơ trong phạm vi kiểm tra được thống nhất đã hoàn tất đúng mốc, ngoại lệ được xử lý. Không đóng chỉ vì đã gửi email hoặc phát hành SOP.

Ưu tiên trên dựa vào việc trạng thái sau ngày nghỉ không đạt kết quả kiểm soát mong muốn, không phải một mức rating tự đặt. Mọi thay đổi quyền truy cập, SOP, cơ chế thay thế hoặc chấp nhận phơi nhiễm còn lại cần đúng thẩm quyền. Đây là bản tư vấn dự thảo theo dữ liệu giả lập được phép phân tích trong AI, chưa được phê duyệt; không phải kết luận assurance hoặc xác nhận tuân thủ pháp lý.

