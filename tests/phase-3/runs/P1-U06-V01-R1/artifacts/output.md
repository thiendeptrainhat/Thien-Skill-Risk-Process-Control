# Thiết kế E2E quản lý quyền truy cập — bản tham khảo, chưa phê duyệt

Nên bổ sung hai kết quả đầu ra cho SOP: **quyền đã được xử lý đúng yêu cầu hợp lệ** và **việc xử lý đã được xác nhận, đối soát**. Việc gửi yêu cầu hoặc thông báo chưa tự chứng minh hai kết quả này.

Phân tích dưới đây dùng mục tiêu tại SOP-ACCESS-06 §3: quyền phù hợp nhu cầu được phê duyệt trong suốt quá trình gia nhập, đổi việc và rời tổ chức. NIST được dùng làm nguồn tham khảo thiết kế, không phải căn cứ tự động kết luận tổ chức phải tuân thủ NIST.

## 1. Điều nguồn nội bộ thực sự cho biết

Nguồn SRC-01 là [nội dung SOP được cung cấp](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U06-V01/input.md>), §§1–3. Đây là dữ liệu tổng hợp, không mật, được phép phân tích trong AI. Version, ngày hiệu lực, người sở hữu/phê duyệt SOP, phạm vi hệ thống và kỳ đánh giá: **Not provided**.

| Nhánh | As-Documented — chỉ theo phần đã đọc | Giới hạn cần giữ |
|---|---|---|
| Gia nhập, §1 | Quản lý yêu cầu; vận hành tài khoản cấp quyền theo nhóm chức năng được yêu cầu. | Chưa mô tả tiêu chí quyền phù hợp hoặc một bước phê duyệt riêng. Không đồng nhất người gửi yêu cầu với người có thẩm quyền phê duyệt. |
| Đổi việc, §2 | Quản lý gửi email điều chỉnh. | Chưa mô tả cách xác định quyền cũ cần bỏ, người thực hiện, kiểm tra kết quả hoặc thời hạn. |
| Thôi việc, §2 | Nhân sự thông báo để thu hồi tài khoản. | Chưa mô tả xác nhận hoàn tất hoặc đối chiếu danh sách tài khoản với nhân sự. |

Các thiếu sót trên là **documentation gaps trong phạm vi cung cấp**, chưa chứng minh control không tồn tại. As-Designed chưa được xác nhận độc lập; As-Performed chưa có operating logs. Không đánh giá hiệu quả vận hành, chấm điểm rủi ro hoặc kết luận vi phạm.

## 2. Nguồn công khai đã kiểm tra và phạm vi sử dụng

Ngày kiểm tra thực tế: **28/08/2026, UTC+07:00**. Chỉ dùng nguồn chính thức làm căn cứ; không đăng nhập, trả phí hay cài đặt.

| Nguồn | Tài nguyên và nội dung thực đọc | Dùng cho việc gì; giới hạn |
|---|---|---|
| SRC-02 — NIST, Joint Task Force, *Security and Privacy Controls for Information Systems and Organizations* | [SP 800-53 Rev. 5, PDF chính thức](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf), tháng 9/2020, cập nhật 10/12/2020. Đã đọc AC-2 và phần liên quan, AC-5, AC-6/AC-6(7), PS-4, PS-5. | Control catalog; hỗ trợ các nguyên tắc/cơ chế ghi cụ thể ở mục 3. Không phải taxonomy E2E hay sơ đồ quy trình của tổ chức. Content verified chỉ cho các mục đã đọc. |
| SRC-03 — NIST, *The NIST Cybersecurity Framework (CSF) 2.0* | [NIST CSWP 29](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf), 26/02/2024; đọc mô tả phạm vi, PR.AA-01/05, PR.PS-04 và ID.RA-07. | Framework outcomes: định hướng mục tiêu, không ấn định một cách triển khai duy nhất. Các mã này không phải mã quy trình. Content verified trong phạm vi nêu trên. |
| SRC-04 — NIST, điều kiện sử dụng | [Copyright, Fair Use, and Licensing Statements](https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications), các mục về dữ liệu/tác phẩm ngoài SRD và ấn phẩm kỹ thuật của NIST; trang cập nhật 24/06/2025. | Căn cứ quyền sử dụng, không phải nguồn control. Điều kiện nêu quyền tạo tác phẩm phái sinh/tái bản và yêu cầu ghi nhận nguồn; cần giữ riêng ngoại lệ tài liệu bên thứ ba. |

**Phân biệt revision với release dữ liệu:** [trang công bố SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) thông báo minor release **5.2.0 ngày 27/08/2025**. Nội dung control dùng dưới đây là bản PDF Rev. 5 ghi rõ cập nhật 10/12/2020, không giả nhận PDF này là dataset 5.2.0. Trang CPRT không trả nội dung control cho bộ đọc hiện tại; lượt mở catalog OSCAL bị giới hạn dung lượng. Vì vậy, chưa xác minh nội dung đầy đủ release 5.2.0 và không tuyên bố mapping này đã được đối chiếu toàn bộ release đó. [Trang CSF chính thức](https://www.nist.gov/cyberframework) hiện giới thiệu CSF 2.0.

Về quyền, tách bốn việc: access **available** cho hai PDF đã đọc; AI-use **permission_evidenced trong phạm vi diễn giải này**, dựa trên quyền dùng/tạo phái sinh đã nêu, không suy rằng có một giấy phép AI riêng; redistribution giới hạn ở bản phân tích có dẫn nguồn, không đóng gói toàn văn/catalog; quyền đối với tài liệu bên thứ ba không được mở rộng từ quyền của NIST. “Republished courtesy of the National Institute of Standards and Technology.” Đây là bản diễn giải tiếng Việt và thiết kế của analyst ngày 28/08/2026, không phải bản dịch chính thức hay tài liệu được NIST bảo chứng.

Applicability: hai nguồn phù hợp về chủ đề quản lý quyền truy cập nhân sự; sử dụng ở mức **advisory / recognized framework-aligned candidate**. Entity, jurisdiction, nghĩa vụ hợp đồng và adoption nội bộ chưa có; applicability bắt buộc là **To be validated**. Ngày xuất bản không phải ngày bắt đầu nghĩa vụ của tổ chức.

## 3. Thiết kế E2E và nguồn hỗ trợ từng đề xuất

**Target-State, draft:** “Quản lý vòng đời quyền truy cập nhân sự” là tên đề xuất riêng, không phải tên hoặc ID E2E do NIST cấp. Phạm vi chính là định danh/quyền; đầu nối nhân sự cung cấp sự kiện gia nhập, đổi việc, thôi việc. Chưa gán cấp L0–L5 vì chưa có kiến trúc doanh nghiệp.

Vòng đời bắt đầu từ nhu cầu truy cập hợp lệ của người gia nhập; trong thời gian làm việc có nhánh thay đổi và rà soát; kết thúc khi quyền không còn hợp lệ đã được thu hồi và xác nhận trên phạm vi hệ thống được phê duyệt. Mỗi yêu cầu có điểm đóng riêng: xử lý đủ, kiểm tra kết quả và lưu dấu vết; yêu cầu bị từ chối có lý do. Ngoại lệ chưa xử lý không được ghi là hoàn tất.

Bảng sau phân biệt **nội dung nguồn hỗ trợ** với **cách triển khai do analyst đề xuất**. REC-* chỉ là mã đề xuất của bản phân tích.

| Đề xuất và control objective | Nguồn thực sự hỗ trợ | Cách triển khai đề xuất — chưa phải quy định hiện hành |
|---|---|---|
| **REC-01 — Liên kết toàn vòng đời.** Mọi sự kiện có liên quan được chuyển thành xử lý quyền có thể truy nguyên. | SRC-02, **AC-2(h,l)**: nối quản lý tài khoản với biến động nhân sự. [AC-2, trang in 19–20](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf#page=46). | Dùng một hồ sơ/mã yêu cầu xuyên quản lý–nhân sự–vận hành; ghi sự kiện, ngày hiệu lực, người liên quan, hệ thống/phạm vi và trạng thái xử lý. “Một hồ sơ chung” là lựa chọn thiết kế, không phải mẫu NIST bắt buộc. |
| **REC-02 — Cấp đúng quyền hợp lệ.** Quyền mới không vượt nhu cầu đã được người có thẩm quyền chấp thuận. | SRC-02, **AC-2(c–f,i), AC-6**; SRC-03, **PR.AA-05**: phê duyệt, quyền tối thiểu và quản trị quyền. [AC-6, trang in 36](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf#page=63); [PR.AA-05, trang in 20](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=25). | Trước khi cấp, đối chiếu yêu cầu với danh mục nhóm/quyền được tổ chức phê duyệt; lưu ai duyệt, phạm vi và lý do. Yêu cầu thiếu căn cứ được trả lại hoặc từ chối, không mặc nhiên cấp theo tên nhóm được yêu cầu. |
| **REC-03 — Thay đổi không tích lũy quyền thừa.** Quyền sau chuyển việc phản ánh nhiệm vụ mới. | SRC-02, **PS-5(a,c)**: rà lại nhu cầu, điều chỉnh quyền khi chuyển vị trí. [PS-5, trang in 225–226](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf#page=252). | Trên cùng yêu cầu đổi việc, ghi quyền giữ/bỏ/thêm và ngày thực hiện; kiểm tra cả quyền cũ, không chỉ thêm nhóm mới. Trường hợp cần bàn giao có thời hạn phải được quyết định riêng, không tự coi là ngoại lệ hợp lệ. |
| **REC-04 — Rời tổ chức không còn truy cập trái phép.** Thu hồi đầy đủ, đúng thời điểm nhưng vẫn bảo toàn thông tin của tổ chức. | SRC-02, **PS-4(a,b,e)**: ngắt truy cập, thu hồi thông tin xác thực, giữ khả năng tiếp cận dữ liệu tổ chức. [PS-4, trang in 224–225](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf#page=251). | Lập danh sách hệ thống/tài khoản thuộc từng người và theo dõi kết quả từng nơi. Không dùng bước duyệt cấp mới để trì hoãn một thu hồi đã đủ căn cứ. Cơ chế khóa/xóa, xử lý phiên truy cập và bàn giao dữ liệu phải được chủ hệ thống xác nhận trước khi thiết kế chi tiết. |
| **REC-05 — Chỉ đóng khi có kết quả kiểm chứng.** Kết quả thực thi khớp yêu cầu hợp lệ, có dấu vết truy nguyên. | SRC-03, **PR.PS-04** hỗ trợ việc tạo và cung cấp log; **không quy định** mẫu phiếu hay bước xác nhận đóng yêu cầu. [PR.PS-04, trang in 20](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=25). | Đề xuất đối chiếu kết quả quyền/tài khoản với yêu cầu sau xử lý; lưu trạng thái trước–sau, thời điểm, người thực hiện và kết quả kiểm tra. Chỉ gửi email “đã xử lý” không đủ cho tiêu chí đóng đề xuất này. Lỗi hoặc xử lý một phần phải giữ mở và chuyển xử lý tiếp. |
| **REC-06 — Phát hiện quyền/tài khoản không còn phù hợp.** Danh sách quyền đang tồn tại có căn cứ nhân sự và nhu cầu hợp lệ. | SRC-02, **AC-2(j), AC-6(7)** hỗ trợ rà soát tài khoản/quyền. [AC-6(7), trang in 38](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf#page=65). | Đối chiếu danh sách tài khoản nhân sự trong scope với danh sách nhân sự và yêu cầu đã duyệt; kiểm tra tính đầy đủ của cả hai nguồn, điều tra chênh lệch và xác nhận xử lý. Đối chiếu với HR là cách triển khai đề xuất, không phải công thức bắt buộc của nguồn. Tài khoản dịch vụ/chung/không thuộc nhân sự phải phân loại riêng, không tự kết luận trái phép chỉ vì không khớp HR. |
| **REC-07 — Ngoại lệ có quyết định và theo dõi.** Yêu cầu chưa rõ, lỗi hoặc ngoại lệ không âm thầm trở thành quyền thường xuyên. | SRC-03, **ID.RA-07** hỗ trợ quản lý, ghi nhận và theo dõi thay đổi/ngoại lệ. [ID.RA-07, trang in 19](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf#page=24). | Ghi lý do, phạm vi, người có thẩm quyền quyết định, biện pháp tạm thời và điều kiện kết thúc; chuyển cấp khi quá thời hạn được duyệt. Quyền khẩn cấp, xử lý khi hệ thống lỗi và đường dự phòng là thiết kế cần thống nhất, không được suy từ email hiện có. |

Nguồn hỗ trợ boundary và objectives; **toàn bộ trình tự E2E, biểu mẫu, tiêu chí đóng và cách đối chiếu là bản tổng hợp thiết kế**, không phải quy trình được chép nguyên từ một framework.

Phân công gợi ý để xác nhận: nhân sự cung cấp trạng thái nhân sự; quản lý xác nhận nhu cầu; vận hành thực thi thay đổi. E2E owner, approver, người kiểm tra kết quả, authority xử lý ngoại lệ và escalation: **To be validated**. Không tự đặt SLA, tần suất rà soát hay thời hạn lưu bằng chứng. Chưa xác định control nào là key control.

## 4. Điều cần xác nhận trước khi áp dụng

Nếu thực tế cũng thiếu kiểm tra quyền cũ và xác nhận hoàn tất, yêu cầu có thể bị bỏ sót hoặc xử lý một phần, để lại quyền thừa/tài khoản còn hoạt động; từ đó có thể phát sinh truy cập, sửa đổi hoặc lộ thông tin ngoài nhu cầu được phê duyệt. Đây là **risk scenario suy luận**, không phải sự cố đã xảy ra. Bảo vệ được SOP mô tả hiện nay là yêu cầu từ quản lý và thông báo nhân sự; chưa có bằng chứng về mức bảo vệ thực tế hoặc control bù trừ.

Bước tiếp theo là xác nhận bản SOP có hiệu lực, ma trận thẩm quyền, phạm vi tài khoản/hệ thống, danh mục quyền, dữ liệu nhân sự, cơ chế xử lý hiện tại và bằng chứng của các nhánh gia nhập–đổi việc–thôi việc. Kiểm tra có cơ chế xác nhận/đối soát tương đương nào đang tồn tại trước khi bổ sung control trùng lặp.

Có thể thiết kế hồ sơ theo dõi có kiểm soát trước; quyết định tích hợp/tự động hóa cần dựa vào khối lượng, chất lượng dữ liệu, khả năng hệ thống và chi phí chưa được cung cấp. Đề xuất này không yêu cầu mua hay cấu hình sản phẩm cụ thể.

**Trạng thái:** draft, Not reviewed; confidence **Medium** cho khả năng áp dụng vào SOP ngắn này, vì nguồn control đã đọc nhưng thiết kế thực tế và authority chưa được xác nhận. Hiệu quả vận hành: **Not assessed — Insufficient evidence**. Việc ban hành SOP, thay đổi quyền hạn hoặc chấp nhận ngoại lệ cần người có thẩm quyền phê duyệt. Skill đã định hướng việc tách lớp và tách nguồn–objective–cách triển khai; không thay thế quyết định quản trị.
