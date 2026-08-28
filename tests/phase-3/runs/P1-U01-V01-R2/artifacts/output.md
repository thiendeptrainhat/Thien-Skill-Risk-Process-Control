# Phân tích SOP mua hàng và thanh toán

E2E phù hợp là **Procure-to-Pay (P2P)**: từ nhu cầu mua đến nhận hàng, xử lý hóa đơn, thanh toán và ghi sổ/đóng chênh lệch. SOP đã mô tả phê duyệt nhu cầu, kiểm đếm hàng, đối chiếu ba chứng từ và tách người lập với người phát hành lệnh. Tuy nhiên, chưa đủ thông tin để xác nhận mức thẩm quyền, chống thanh toán trùng, xác minh người thụ hưởng và hoàn tất ghi sổ.

Đây là bản phân tích dự thảo ở lớp **As-Documented**. Kiểm soát “hiện tại” dưới đây nghĩa là *được SOP quy định*, không phải đã được xác nhận vận hành. Phần “nên có” là **Target-State — đề xuất của người phân tích, chờ phê duyệt**, không phải yêu cầu pháp luật/tiêu chuẩn đã được xác minh.

## 1. Căn cứ và phạm vi

| Nội dung | Căn cứ/giới hạn |
|---|---|
| Nguồn duy nhất | SRC-SOP-01, “Quy trình mua hàng và thanh toán”, v2; ghi nhận phê duyệt ngày 01/01/2026; phạm vi mua hàng nội địa. Các dẫn chiếu § bên dưới đều thuộc nguồn này. |
| Tình trạng tài liệu | Ngày hiệu lực, người phê duyệt, chủ sở hữu tài liệu/quy trình và tình trạng bị thay thế: **Not provided**. Ngày phê duyệt không tự chứng minh hiệu lực hiện tại. |
| Cảnh báo nguồn | “DỮ LIỆU TỔNG HỢP DÙNG CHO KIỂM THỬ. Không mô tả doanh nghiệp thật. Được phép phân tích trong AI.” |
| Hồ sơ thiếu | Ma trận duyệt được §4 viện dẫn nhưng không có trong hồ sơ; không có giao dịch, log, walkthrough hoặc bằng chứng vận hành. Hệ thống, khối lượng và kỳ vận hành: **Not provided**. |
| Confidence | **Medium — Documented** đối với nội dung trích từ một SOP; **Low — Inferred** đối với kịch bản rủi ro chưa kiểm chứng. Thiết kế thực tế ngoài SOP và As-Performed: **Unresolved**. |
| Trạng thái đánh giá | Chỉ đánh giá độ rõ, phạm vi bao phủ và khả năng kiểm tra của mô tả. Chưa chấm điểm rủi ro/thiết kế do không có phương pháp được duyệt; hiệu lực vận hành: **Not assessed**. Review status: **Not reviewed**. |

## 2. E2E và chuỗi công việc

Mục tiêu theo §1 là nhận đúng hàng đã được duyệt và trả đúng nhà cung cấp, đúng số tiền, một lần. Trigger là bộ phận sử dụng gửi nhu cầu; điểm kết thúc theo §2 là hàng đã nhận, hóa đơn và khoản thanh toán được ghi sổ, chênh lệch được xử lý. Bộ phận sử dụng là bên nhận kết quả hàng hóa; nhà cung cấp là bên nhận thanh toán — suy luận trực tiếp từ §1–2, cần xác nhận khi lập kiến trúc chính thức.

P2P phù hợp vì bao phủ cả cam kết mua, nhận hàng và chi trả; chỉ gọi là Invoice-to-Payment sẽ bỏ phần nhu cầu/PO/nhận hàng. Phần ghi sổ có giao diện với Transaction-to-Record, nhưng SOP không đủ căn cứ để mở rộng sang toàn bộ Record-to-Report. Lựa chọn nhà cung cấp, hợp đồng và quản trị dữ liệu nhà cung cấp là các giao diện cần xác nhận, chưa phải các bước hiện trạng được mô tả. Đây là phân loại phân tích, không phải mã/tên quy trình đã được tổ chức phê duyệt; không gán mã thư viện bên ngoài hoặc ép tạo đầy đủ L0–L5.

| Bước | As-Documented: công việc, vai trò và bàn giao | Nguồn/điểm còn mở |
|---|---|---|
| STEP-01 | Người yêu cầu lập đề nghị; người quản lý duyệt nhu cầu trước khi người mua gửi PO. | §3.1; chưa mô tả nhánh từ chối, sửa đề nghị hoặc sửa PO. |
| STEP-02 | Kho kiểm đếm, ghi phiếu nhận; báo chênh lệch cho người mua. | §3.2; chưa rõ tiêu chí chấp nhận hàng và cách đóng chênh lệch. |
| STEP-03 | Kế toán đối chiếu PO, phiếu nhận, hóa đơn; chênh lệch được giữ lại để xử lý. | §3.3; đối tượng bị giữ, người xử lý, quyền giải phóng và điều kiện chuyển sang thanh toán chưa rõ. |
| STEP-04 | Người lập lệnh gửi danh sách thanh toán; người có thẩm quyền **khác** phát hành lệnh. | §3.4; chưa rõ người phát hành phải kiểm tra những thuộc tính nào và cách xác nhận kết quả chuyển tiền. |
| STEP-05 | Hóa đơn, khoản thanh toán được ghi sổ và chênh lệch được xử lý. | §2 chỉ xác định kết quả cuối; chưa mô tả người thực hiện, trình tự, đối soát và bằng chứng đóng. Không suy thành một bước kiểm soát đã đầy đủ. |

§4 yêu cầu lưu hồ sơ xuyên suốt; không đủ căn cứ xác định nơi lưu, người quản lý hoặc thời hạn lưu.

## 3. Kiểm soát hiện tại theo SOP

Các CTL dưới đây là ID phân tích nội bộ, giữ nguyên khi tham chiếu lại. Mỗi dòng chỉ có observation ở lớp As-Documented, phạm vi mua hàng nội địa của v2; kỳ vận hành chưa được cung cấp. Hồ sơ SOP yêu cầu lưu **không phải** bằng chứng thực hiện đã nhận được.

| Control ID | Mục tiêu kiểm soát | Mô tả có nguồn | Giới hạn mô tả/bằng chứng |
|---|---|---|---|
| CTL-01 | Chỉ gửi cam kết mua dựa trên nhu cầu được phép. | Người quản lý duyệt nhu cầu trước khi người mua gửi PO — §3.1. | §4 yêu cầu lưu đề nghị, PO và dấu vết duyệt; thiếu ma trận thẩm quyền, tiêu chí duyệt và kiểm tra PO khớp nội dung được duyệt. |
| CTL-02 | Số lượng hàng nhận được ghi nhận và sai lệch được nhận biết. | Kho kiểm đếm, lập phiếu nhận, báo chênh lệch cho người mua — §3.2. | Có yêu cầu lưu phiếu nhận (§4); chưa rõ đối chiếu mã hàng/quy cách, nghiệm thu chất lượng, xử lý nhận thiếu/thừa và bằng chứng giải quyết. |
| CTL-03 | Nghĩa vụ thanh toán được kiểm tra với đơn đặt hàng và hàng nhận. | Kế toán đối chiếu PO–phiếu nhận–hóa đơn, giữ chênh lệch để xử lý — §3.3. | Chưa rõ trường dữ liệu, độ chính xác/ngưỡng chấp nhận, dấu vết đối chiếu và điều kiện giải phóng. Không tự diễn giải “giữ lại” thành cơ chế khóa thanh toán trên hệ thống. |
| CTL-04 | Người lập không tự phát hành lệnh thanh toán. | Người có thẩm quyền khác người lập phát hành lệnh — §3.4. | Có nguyên tắc phân tách vai trò; thiếu ma trận duyệt, tiêu chí review danh sách, dữ liệu người dùng/quyền truy cập và bằng chứng phát hành thực tế. |
| CTL-05 | Hồ sơ giao dịch và phê duyệt có thể truy nguyên. | Lưu đề nghị, PO, phiếu nhận, hóa đơn và dấu vết duyệt — §4. | Chưa rõ người lưu, liên kết giữa các chứng từ, nơi lưu, quyền truy cập, thời hạn lưu; danh sách/lệnh thanh toán, kết quả chuyển tiền và kết quả xử lý ngoại lệ chưa được nêu rõ trong yêu cầu lưu. |

CTL-03 và CTL-04 là **ứng viên key control**: trực tiếp hỗ trợ xác minh khoản phải trả và ngăn người lập tự phát hành lệnh, liên quan mục tiêu thanh toán đúng tại §1. Chưa phân loại chính thức vì chưa biết mức trọng yếu, kiểm soát thay thế, mức độ dựa vào kiểm soát và phê duyệt của tổ chức. CTL-05 hỗ trợ truy nguyên, không tự bảo đảm khoản thanh toán đúng hoặc duy nhất.

## 4. Rủi ro, kiểm soát nên có và khoảng trống cần làm rõ

Các kịch bản rủi ro là **Inferred từ mục tiêu và mô tả SOP**, không phải sự cố đã quan sát. Các GAP là **khoảng trống mô tả trong hồ sơ đã đọc**, không khẳng định kiểm soát vắng mặt trong thực tế. Căn cứ cho mức kết quả cần đạt là §1–2; cách triển khai đề xuất là phán đoán thiết kế, chưa được benchmark với nguồn ngoài.

| Rủi ro: nguyên nhân → sự kiện → tác động/mục tiêu | Bảo vệ đã mô tả | Khoảng trống và kiểm soát đề xuất Target-State |
|---|---|---|
| **RSK-01 / STEP-01:** nếu duyệt nhu cầu không ràng buộc nội dung và thẩm quyền của PO, PO sai hoặc vượt phạm vi được duyệt có thể được gửi → cam kết mua không phù hợp, ảnh hưởng nhận đúng hàng đã duyệt. | CTL-01; hồ sơ CTL-05. | **GAP-01 — Unclear Control**, §3.1, §4: cần ma trận duyệt và quy tắc sửa PO. Đề xuất làm rõ CTL-01: trước khi gửi PO, kiểm tra nội dung/giá trị với đề nghị và thẩm quyền áp dụng; giữ dấu vết liên kết, trả lại sai lệch hoặc chuyển phê duyệt phù hợp. Không tự đặt hạn mức hay thêm cấp duyệt. |
| **RSK-02 / STEP-02:** nếu kiểm nhận chỉ đếm mà không kiểm tra thuộc tính hàng được duyệt, hàng sai loại/quy cách có thể được chấp nhận → không đáp ứng nhu cầu và phát sinh chi phí xử lý. | CTL-02; CTL-03 hỗ trợ đối chiếu chứng từ sau đó. | **GAP-02 — Insufficient Precision trong mô tả**, §3.2–3.3: “kiểm đếm” chưa làm rõ kiểm tra gì ngoài số lượng. Đề xuất bổ sung CTL-02 theo loại hàng: đối chiếu hàng thực nhận với PO và tiêu chí nghiệm thu được duyệt; ghi kết quả, xử lý từ chối/nhận một phần/chênh lệch và lưu bằng chứng chấp nhận. Người có thẩm quyền nghiệm thu: **To be validated**. |
| **RSK-03 / STEP-03–04:** nếu tiêu chí đối chiếu và giải phóng chênh lệch không rõ, khoản không khớp có thể được đưa vào thanh toán → trả sai số tiền hoặc trả cho hàng chưa đủ điều kiện; ngoại lệ cũng có thể tồn đọng. | CTL-03 phát hiện/giữ chênh lệch; CTL-04 tách phát hành. | **GAP-03 — Unclear Control/Missing Exception Handling chi tiết**, §3.3–3.4: chưa rõ đối chiếu số lượng, đơn giá, tổng tiền, nhận/thanh toán từng phần và ai đóng ngoại lệ. Đề xuất làm rõ CTL-03: quy định trường đối chiếu, tiêu chí chấp nhận, dấu vết kết quả; khoản chưa đạt không đưa vào danh sách trả cho đến khi có xử lý và phê duyệt hợp lệ. Lập hồ sơ ngoại lệ có người xử lý, điều kiện đóng và tuyến escalation; hạn xử lý/ngưỡng phải được xác nhận. |
| **RSK-04 / STEP-03–04:** nếu hóa đơn hoặc lệnh được nhập/gửi lại mà không kiểm tra lịch sử và trạng thái, cùng nghĩa vụ có thể được trả nhiều lần → thất thoát tiền, trái mục tiêu “một lần”. | CTL-03 kiểm tra chứng từ và CTL-04 tách phát hành, nhưng chưa mô tả kiểm tra trùng. | **GAP-04 — nội dung chống trùng chưa được mô tả**, §1, §3.3–3.4. Đề xuất **CTL-06**: trước khi đưa vào danh sách và trước khi phát hành, kiểm tra nhận diện hóa đơn/nhà cung cấp cùng lịch sử, số tiền đã trả và trạng thái lệnh; giữ trường hợp nghi trùng để xác minh, lưu kết quả review. Chỉ gửi lại lệnh khi trạng thái lệnh cũ đã được xác nhận; quy tắc nhận diện và xử lý cảnh báo giả cần phê duyệt. |
| **RSK-05 / STEP-04:** nếu dữ liệu người thụ hưởng/tài khoản sai hoặc bị sửa mà không xác minh độc lập, tiền có thể chuyển sai bên dù bộ chứng từ khớp → mất tiền và vẫn còn nghĩa vụ với nhà cung cấp đúng. | CTL-04 là phân tách phát hành; CTL-03 kiểm tra bộ chứng từ. Chưa có căn cứ hai kiểm soát này xác minh tài khoản nhận tiền. | **GAP-05 — nội dung xác minh người thụ hưởng chưa được mô tả**, §1, §3.4. Đề xuất **CTL-07**: xác minh độc lập thông tin nhà cung cấp/tài khoản mới hoặc thay đổi qua nguồn/kênh tin cậy, kiểm tra người thụ hưởng trên lệnh với dữ liệu đã được xác nhận trước phát hành; giữ sai lệch và lưu bằng chứng xác minh/phê duyệt. Phải xác định quyền sửa, kiểm tra và phát hành, cùng cơ chế xử lý ngoại lệ. |
| **RSK-06 / STEP-05:** nếu không có đối soát trạng thái chuyển tiền với hóa đơn và ghi sổ, giao dịch có thể bị bỏ sót/ghi sai hoặc coi lệnh thất bại là đã trả → sai số dư và không đạt điều kiện kết thúc. | §2 nêu kết quả cuối; CTL-05 hỗ trợ hồ sơ. Kết quả cuối này tự nó chưa phải kiểm soát đối soát. | **GAP-06 — bước/kiểm soát hoàn tất chưa được mô tả**, §2–4. Đề xuất **CTL-08**: đối soát danh sách đã duyệt, kết quả thanh toán từ nguồn độc lập thích hợp, hóa đơn và bút toán; điều tra khoản không khớp/đang chờ/thất bại, lưu kết quả review và bằng chứng đóng. Người lập/review, thời điểm thực hiện và nguồn dữ liệu: **To be validated**. |
| **RSK-07 / xuyên suốt:** nếu hồ sơ không được liên kết, bảo quản và truy xuất nhất quán, chứng từ/dấu vết có thể thất lạc hoặc bị sửa → không chứng minh được giao dịch được duyệt, đã nhận/đã trả và khó xử lý chênh lệch. | CTL-05 yêu cầu lưu các chứng từ; CTL-02–04 tạo nội dung có thể cần truy nguyên. | **GAP-07 — Missing Retention/Unclear Control trong mô tả**, §4. Đề xuất làm rõ CTL-05: liên kết hồ sơ theo giao dịch; xác định người lưu, nơi lưu, quyền truy cập, quản lý thay đổi và thời hạn lưu có căn cứ; bổ sung kết quả kiểm tra, lệnh/kết quả thanh toán, hồ sơ xử lý chênh lệch khi phù hợp. Không tự đặt số năm lưu. |

CTL-06–08 là **kiểm soát mới được đề xuất**, chưa tính vào bảo vệ hiện tại; chủ sở hữu/người thực hiện/người duyệt cụ thể chưa được cung cấp. Với CTL-01–05, các bổ sung là đề xuất tăng độ rõ hoặc tăng coverage của cùng kiểm soát, không phải kiểm soát đã vận hành. Chưa quyết định manual hay automated vì chưa có thông tin hệ thống và khối lượng. Trước khi bổ sung, cần kiểm tra các tài liệu/kiểm soát thay thế để tránh trùng lặp.

**Nếu giữ nguyên:** nếu thực tế cũng thiếu các cơ chế tương ứng và không có kiểm soát khác bù đắp, các kịch bản RSK-01–07 vẫn có thể ảnh hưởng mục tiêu. CTL-01–05 tạo các hàng rào trên giấy nhưng chưa đủ căn cứ xác định mức bảo vệ thực tế, xác suất, thiệt hại hay residual risk. Đặc biệt, đối chiếu ba chứng từ và tách người phát hành không tự chứng minh đã ngăn thanh toán trùng hoặc chuyển sai tài khoản. Đây là kịch bản có điều kiện, không phải xác nhận thất thoát hay control failure.

## 5. Thông tin cần làm rõ để kết luận tiếp

1. **Ma trận duyệt áp dụng:** phiên bản/hiệu lực, phạm vi, hạn mức, quyền ủy quyền và quy tắc thay đổi PO/lệnh. Đây là tài liệu được SOP viện dẫn, không phải một kiểm soát mới do người phân tích tự áp đặt — liên quan GAP-01, GAP-03, GAP-05.
2. **Hướng dẫn chi tiết hoặc kiểm soát bù đắp đang có:** tiêu chí nhận hàng và đối chiếu, đối tượng bị giữ, điều kiện giải phóng, chống trùng, xác minh dữ liệu nhà cung cấp, đối soát/ghi sổ và quản lý hồ sơ — GAP-02–07. Nếu đã có, bổ sung dẫn chiếu thay vì mặc định phải tạo thêm control.
3. **Hồ sơ giao dịch đã khử định danh và walkthrough:** lần theo đề nghị → duyệt → PO → nhận → đối chiếu → danh sách/lệnh → kết quả thanh toán → ghi sổ/đóng chênh lệch; bao gồm các tình huống ngoại lệ phù hợp. Đây là yêu cầu xác minh tiếp, chưa phải thủ tục đã thực hiện hoặc kết quả kiểm thử.
4. **Phân công thực tế và quyền hệ thống, nếu có:** ai lập, sửa dữ liệu người thụ hưởng, kiểm tra và phát hành; có thể là cùng người hoặc dùng chung tài khoản không? SOP quy định khác người ở §3.4 nhưng chưa có dữ liệu để xác nhận SoD ở cấp người dùng/quyền truy cập. Không kết luận có hay không có xung đột thực tế chỉ từ tên vai trò.
5. **Chủ sở hữu, hiệu lực tài liệu và cơ chế phê duyệt thay đổi:** xác nhận ai chịu trách nhiệm giải quyết các điểm mở, phê duyệt thiết kế và nhận rủi ro. Người phụ trách hành động và thời hạn hoàn thành: **To be validated**, không tự ấn định.

Skill được dùng để giữ riêng yêu cầu trên giấy, giả thuyết rủi ro và đề xuất tương lai; vì vậy chưa phát hành kết luận hiệu lực vận hành, tuân thủ hay audit finding. Mọi thay đổi SOP, thẩm quyền hoặc phân công phải được người có thẩm quyền phê duyệt trước khi áp dụng.
