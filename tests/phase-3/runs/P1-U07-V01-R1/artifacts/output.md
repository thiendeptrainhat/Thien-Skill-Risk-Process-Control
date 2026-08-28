# Gợi ý E2E và kiểm soát cho hoạt động cho thuê thiết bị

E2E phù hợp là **“Từ yêu cầu thuê đến thu hồi thiết bị và tất toán thuê”**. Đây là tên và ranh giới đề xuất riêng cho mô tả này, không phải tên/mã chính thức của một thư viện chuẩn. Mục tiêu là hoàn tất dịch vụ thuê đồng thời đối chiếu được thiết bị và công nợ, đúng với CHAT-07 §1.

Phạm vi trả lời: `Target-State — draft v0.1`, chờ người có thẩm quyền phê duyệt; owner/approver cụ thể: `To be validated`.

Về “best practice”: chưa có tài liệu chuẩn được cung cấp và lượt này không được tra cứu ngoài. Vì vậy, các kiểm soát dưới đây là **đề xuất thiết kế của analyst**, có lý do theo rủi ro và mục tiêu; chưa được benchmark với nguồn chính thức, không phải yêu cầu bắt buộc hay kết luận tuân thủ.

## 1. Ranh giới E2E đề xuất

- **Bắt đầu:** trung tâm nhận yêu cầu thuê.
- **Kết thúc:** thiết bị đã được thu hồi và xác định tình trạng; tiền thuê, cọc, khoản phát sinh và khoản hoàn trả đã được đối chiếu, xử lý có căn cứ trước khi đóng giao dịch. Ca còn tranh chấp, thiếu thiết bị hoặc chưa khớp tiền phải được giữ trạng thái chưa hoàn tất và theo dõi xử lý.
- **Người nhận kết quả dự kiến:** khách thuê và trung tâm; chủ quy trình xuyên suốt chưa được cung cấp.

Luồng đích đề xuất:

`Nhận yêu cầu → Xác nhận khả dụng và điều kiện thuê → Giao thiết bị, ghi nhận giao/cọc → Theo dõi hạn trả → Nhận lại và kiểm tra tình trạng → Xác định khoản phải thu/khấu trừ/hoàn trả → Đối chiếu và đóng thuê`

Các bước xác nhận điều kiện, theo dõi hạn trả và kiểm tra trước đóng thuê là phần đề xuất, không phải hoạt động hiện hành đã được chứng minh.

Có thể dùng các family sau làm giả thuyết tham chiếu, chưa phải mapping chuẩn đã xác minh:

- **Order-to-Cash:** giao diện nhận đơn, thực hiện dịch vụ và thu tiền; riêng family này chưa thể hiện đầy đủ vòng thu hồi thiết bị cho thuê.
- **Return-to-Refund:** phần nhận lại, kiểm tra và hoàn tiền; cần điều chỉnh vì trả thiết bị thuê không đồng nghĩa trả lại hàng đã mua.
- **Maintenance-to-Reliability / Acquire-to-Retire:** giao diện xử lý thiết bị không đạt và quản lý vòng đời tài sản. Mua sắm, bảo trì chi tiết và thanh lý nằm ngoài mô tả hiện có, không được tự thêm như hiện trạng.

## 2. Các kiểm soát nên có

Toàn bộ bảng là `Target-State — draft`; căn cứ nghiệp vụ là CHAT-07 §1–§2, còn cách triển khai là đề xuất. Các rủi ro là tình huống có thể xảy ra, không phải sự cố đã quan sát. Người thực hiện, reviewer, thẩm quyền duyệt, nơi lưu và thời hạn lưu bằng chứng đều cần được trung tâm xác định; chưa suy ra từ việc “nhân viên ghi sổ giao nhận”.

| Điểm kiểm soát và mục tiêu | Rủi ro giả thuyết nếu điều kiện không được kiểm soát | Cách thực hiện đề xuất, bằng chứng và ngoại lệ |
|---|---|---|
| Xác nhận khả dụng: chỉ cam kết thiết bị đúng yêu cầu và thực sự sẵn dùng | Thông tin lịch/tình trạng không cập nhật có thể dẫn đến nhận trùng lịch hoặc giao thiếu, ảnh hưởng hoàn tất thuê | Trước xác nhận thuê, đối chiếu yêu cầu với thiết bị, lịch cam kết và tình trạng sử dụng. Lưu kết quả kiểm tra và xác nhận thuê; khi không đáp ứng, ghi rõ phương án thay thế được khách chấp nhận hoặc lý do từ chối. Công cụ quản lý lịch hiện tại: `Not provided`. |
| Thống nhất điều kiện thuê: tiền thuê/cọc và cách xử lý phát sinh có căn cứ rõ ràng | Điều kiện không rõ có thể dẫn đến tính phí, khấu trừ hoặc hoàn cọc sai, gây tranh chấp và sai công nợ | Trước giao, ghi nhận điều kiện về thiết bị, thời gian thuê, giá, cọc, trả muộn, hư hỏng/mất và cách giải quyết bất đồng; lưu xác nhận của các bên. Điều kiện khác mẫu hoặc chưa rõ phải được xử lý theo thẩm quyền trước khi áp dụng. Không tự đặt mức cọc, tỷ lệ khấu trừ hoặc xác nhận quyền giữ cọc. |
| Bàn giao: đúng thiết bị, đủ phụ kiện và có tình trạng ban đầu đối chiếu được | Nhận dạng hoặc ghi nhận ban đầu không đủ có thể làm giao nhầm, mất phụ kiện hoặc không phân định được hư hỏng, ảnh hưởng thu hồi tài sản | Khi giao, đối chiếu mã nhận dạng, số lượng, phụ kiện và tình trạng theo tiêu chí phù hợp loại thiết bị. Lưu biên bản/xác nhận giao nhận; ảnh chỉ là bằng chứng bổ trợ khi phù hợp. Chênh lệch phải được làm rõ trước khi hoàn tất phần giao bị ảnh hưởng. |
| Thu hồi và kiểm tra: nhận đúng thiết bị và xác định được trạng thái sau thuê | Kiểm tra không có tiêu chí hoặc không so với lúc giao có thể bỏ sót thiếu/hỏng, gây thất thoát hoặc đưa thiết bị chưa đạt vào lượt thuê sau | Khi nhận lại, đối chiếu mã, phụ kiện, số lượng và tình trạng với hồ sơ giao; lưu kết quả và chênh lệch. Tiêu chí kiểm tra cần người có chuyên môn xác lập và người có thẩm quyền duyệt. Tách thiết bị chưa kiểm tra/chưa đạt khỏi danh sách sẵn cho thuê; ghi riêng bất đồng để xử lý, không mặc định quy lỗi cho khách. |
| Hoàn cọc: đúng căn cứ, đúng người, đúng số tiền và không trùng | Tính toán thiếu căn cứ hoặc không kiểm tra lịch sử hoàn có thể dẫn đến khấu trừ sai, hoàn sai/trùng, làm sai tất toán | Trước hoàn, đối chiếu tiền cọc đã nhận, điều kiện thuê, thời gian thực tế, kết quả trả và khoản phát sinh có căn cứ; kiểm tra người nhận và giao dịch hoàn trước đó. Đề xuất người rà soát độc lập với người lập tính toán, tùy khả năng bố trí và phê duyệt thiết kế. Lưu bảng tính, căn cứ, phê duyệt và chứng từ hoàn; khoản chưa rõ được ghi ngoại lệ, xử lý theo điều kiện áp dụng đã xác nhận. |
| Đối chiếu và theo dõi ca mở: thiết bị và tiền không bị bỏ sót khi đóng thuê | Các ghi nhận giao–trả–thu–hoàn không liên kết có thể làm bỏ sót tài sản chưa trả hoặc công nợ chưa xử lý, cản trở đối chiếu đầy đủ | Trước đóng giao dịch, đối chiếu sổ giao nhận với trạng thái thiết bị, cọc, hoàn cọc và khoản phải thu theo mã giao dịch/thiết bị. Lưu kết quả đối chiếu và danh sách chênh lệch; ca quá hạn, chưa thu hồi hoặc chưa khớp tiền cần người theo dõi và tuyến xử lý được chỉ định. Tần suất rà soát toàn bộ ca mở: `To be validated`, không tự ấn định. |

## 3. Giới hạn và bước xác nhận

CHAT-07 §1 chỉ mô tả kiểm tra hàng sẵn, giao–nhận, kiểm tra tình trạng, hoàn cọc và ghi sổ. §2 nói rõ chưa cung cấp tiêu chí kiểm tra, quy định khấu trừ hoặc bằng chứng thực hiện. Do đó, chưa kết luận các kiểm soát hiện tại thiếu, thất bại hay hiệu quả; chưa có cơ sở xác nhận `As-Performed`, chấm rủi ro hoặc chỉ định “key control”. Confidence về hiện trạng: **Low**, do chỉ có mô tả chat chưa kiểm chứng; tính phù hợp chi tiết của đề xuất: `To be validated`.

Để hoàn thiện, cần xác nhận loại thiết bị và tiêu chí kiểm tra; điều kiện thuê/cọc/khấu trừ được áp dụng; vai trò và thẩm quyền; cách quản lý lịch, sổ và tiền; cùng hồ sơ một vòng thuê từ giao đến hoàn cọc. Chỉ sau đó mới hoàn thiện mô tả kiểm soát và phê duyệt áp dụng. Nếu cần benchmark có trích dẫn, cần nguồn chuẩn được phép xử lý hoặc một lượt tra cứu được cho phép riêng.

Nguồn duy nhất về nghiệp vụ: **CHAT-07 §1–§2**, trong `input.md`; chủ nguồn, phiên bản và ngày hiệu lực: `Not provided`. Giữ nguyên cảnh báo nguồn: “DỮ LIỆU TỔNG HỢP; được phép phân tích trong AI.” Không thực hiện external lookup trong lượt này.
