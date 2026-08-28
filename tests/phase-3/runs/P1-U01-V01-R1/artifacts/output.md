# Phân tích SOP mua hàng và thanh toán

E2E phù hợp là **Procure-to-Pay (P2P) — từ nhu cầu mua đến nhận hàng, thanh toán và hoàn tất ghi sổ/xử lý chênh lệch**. SOP đã mô tả những kiểm soát có liên hệ trực tiếp với mục tiêu: duyệt nhu cầu trước khi gửi PO, kiểm đếm khi nhận hàng, đối chiếu ba chứng từ, giữ chênh lệch để xử lý và tách người lập–phát hành lệnh thanh toán. Tuy nhiên, chỉ với SOP này, chưa thể xác nhận các kiểm soát đã vận hành hoặc bảo đảm trả đúng nhà cung cấp, đúng tiền, một lần.

## 1. Căn cứ và giới hạn

Nguồn dữ liệu là dữ liệu tổng hợp, không mô tả doanh nghiệp thật và được phép phân tích trong AI. Phân tích chỉ sử dụng nội dung đã cung cấp, không tra cứu bên ngoài.

| Nguồn | Thông tin được cung cấp | Phần chưa xác nhận |
|---|---|---|
| SRC-SOP-01, toàn bộ §1–§4 | SOP mua hàng và thanh toán, v2; ghi phê duyệt ngày 01/01/2026; phạm vi mua hàng nội địa | Chủ sở hữu tài liệu, người phê duyệt, ngày hiệu lực và tình trạng còn hiệu lực: `Not provided`/`To be validated`. Ngày phê duyệt không được tự coi là ngày hiệu lực. |
| Ma trận duyệt được dẫn tại SRC-SOP-01 §4 | SOP nêu mức thẩm quyền nằm tại tài liệu riêng | Tài liệu, phiên bản, người có thẩm quyền và các ngưỡng: `Not provided`; chưa kiểm tra nội dung. |

Phân biệt các lớp phân tích:

- `As-Documented`: nội dung SOP thực sự quy định. Các ghi nhận bên dưới có trạng thái `Documented`, confidence `Medium` vì chỉ có một nguồn tài liệu, chưa được đối chứng.
- `As-Designed`: chưa có nguồn bổ sung xác nhận thiết kế hiện trạng ngoài SOP; không tự nâng các mô tả hoặc đề xuất thành thiết kế đã được tổ chức xác nhận.
- `As-Performed`: `Not provided`. Đánh giá vận hành: `Not assessed`; bằng chứng phục vụ đánh giá vận hành: `Insufficient evidence`.
- `Target-State`: các kiểm soát nên có là đề xuất của người phân tích, chưa phê duyệt. Chúng không phải yêu cầu pháp luật/chuẩn bên ngoài đã xác minh và không được tính vào bảo vệ hiện tại.

Toàn bộ báo cáo là bản dự thảo, `review_status: Not reviewed`. Không giả định ERP, mức tự động hóa, chủ sở hữu kiểm soát, ngưỡng duyệt, dung sai, thời hạn xử lý hay bằng chứng thực hiện. Không chấm điểm rủi ro do chưa có phương pháp được phê duyệt.

## 2. E2E và ranh giới

Mục tiêu và ranh giới lấy trực tiếp từ SRC-SOP-01:

- **OBJ-01:** nhận đúng hàng đã được duyệt (§1).
- **OBJ-02:** trả đúng nhà cung cấp, đúng số tiền và một lần (§1).
- **OBJ-03:** hàng đã nhận, hóa đơn và khoản thanh toán được ghi sổ, chênh lệch được xử lý (§2).

Trigger là bộ phận sử dụng gửi nhu cầu; end state là đáp ứng đầy đủ OBJ-03, không chỉ dừng ở phát hành lệnh. Đối tượng hưởng kết quả gồm bộ phận sử dụng và nhà cung cấp, suy từ §1–§2; Process Owner và kiến trúc phân cấp chính thức: `Not provided`.

Luồng `As-Documented`: lập đề nghị → quản lý duyệt nhu cầu → người mua gửi PO (§3.1) → kho kiểm đếm, lập phiếu nhận và báo chênh lệch (§3.2) → kế toán đối chiếu PO–phiếu nhận–hóa đơn, giữ chênh lệch để xử lý (§3.3) → lập danh sách thanh toán → người có thẩm quyền khác phát hành lệnh (§3.4). Lưu hồ sơ là yêu cầu xuyên suốt theo §4. Ghi sổ và xử lý dứt điểm chênh lệch là **điều kiện kết thúc đã nêu**, nhưng các bước, người chịu trách nhiệm và bằng chứng đóng việc chưa được mô tả đủ.

P2P phù hợp vì nối nhu cầu–mua–nhận–hóa đơn–thanh toán qua nhiều vai trò. Chỉ gọi là Invoice-to-Payment sẽ bỏ phần nhu cầu và nhận hàng. Quản lý/lựa chọn nhà cung cấp và đối soát–báo cáo kế toán có thể là các giao diện liên quan, nhưng chưa được mô tả để coi là quy trình hiện hành đã xác nhận. Không mở rộng SOP thành toàn bộ Source-to-Pay hoặc tự gán mã tham chiếu chính thức.

Nhánh từ chối nhu cầu, hủy/sửa PO, giao thiếu, giải phóng khoản giữ và thanh toán thất bại: `To be validated`; không tự thêm chúng vào luồng hiện trạng.

## 3. Kiểm soát hiện tại theo tài liệu

Mỗi dòng dưới đây là một logical control với observation `As-Documented` riêng; phạm vi mua hàng nội địa, nguồn v2, kỳ vận hành chưa được cung cấp. Các chứng từ được SOP yêu cầu lưu **không phải** bằng chứng giao dịch đã nhận được.

| Control / observation | Nội dung được SOP mô tả và mục tiêu hỗ trợ | Bằng chứng theo yêu cầu SOP | Giới hạn thiết kế cần làm rõ |
|---|---|---|---|
| CTL-01 / OBS-D01 | Người quản lý duyệt nhu cầu trước khi người mua gửi PO; hỗ trợ OBJ-01, ngăn cam kết mua khi nhu cầu chưa duyệt (§3.1). | Đề nghị, PO và dấu vết duyệt (§4). | Chưa có ma trận thẩm quyền; chưa rõ tiêu chí duyệt, PO có phải khớp bản nhu cầu đã duyệt và thay đổi nào cần duyệt lại. SOP không nói phải duyệt trước khi **tạo** PO. |
| CTL-02 / OBS-D02 | Kho kiểm đếm, ghi phiếu nhận và báo chênh lệch cho người mua; hỗ trợ OBJ-01 và dữ liệu đầu vào cho OBJ-02 (§3.2). | Phiếu nhận (§4); việc lưu báo cáo chênh lệch riêng chưa được nêu. | Chưa rõ đối chiếu với PO nào, kiểm tra mã hàng/quy cách/chất lượng, hàng giao từng phần và quyền chấp nhận sai lệch. |
| CTL-03 / OBS-D03 | Kế toán đối chiếu PO, phiếu nhận và hóa đơn; chênh lệch được giữ lại để xử lý; hỗ trợ OBJ-02–03 (§3.3). | Ba chứng từ phải lưu (§4); SOP chưa nêu rõ bằng chứng kết quả đối chiếu và đóng chênh lệch. | Chưa rõ trường đối chiếu, dung sai, thời điểm trước thanh toán, đối tượng bị giữ, quyền giải phóng và escalation. |
| CTL-04 / OBS-D04 | Người lập lệnh gửi danh sách; một người có thẩm quyền khác phát hành lệnh; hỗ trợ OBJ-02 bằng phân tách lập–phát hành (§3.4). | Dấu vết duyệt theo yêu cầu chung (§4); danh sách/lệnh và xác nhận thanh toán chưa được liệt kê rõ là hồ sơ phải lưu. | Chưa rõ nội dung phải kiểm tra khi phát hành, liên kết danh sách với lệnh thực gửi, thẩm quyền cụ thể và cơ chế ngăn cùng người thực hiện cả hai vai trò. |
| CTL-05 / OBS-D05 | Yêu cầu lưu đề nghị, PO, phiếu nhận, hóa đơn và dấu vết duyệt; hỗ trợ truy nguyên OBJ-01–03 (§4). | Các loại hồ sơ vừa nêu; chưa có hồ sơ thực tế trong đầu vào. | Người lưu, nơi lưu, thời hạn lưu, quyền sửa/xóa, cách liên kết và truy xuất: `Not provided`. Đây là kiểm soát hỗ trợ, không tự bảo đảm giao dịch chính xác. |

Thiết kế trên giấy có logic phòng ngừa/phát hiện, nhưng độ chính xác, bao phủ, ngoại lệ và khả năng kiểm thử còn phụ thuộc thông tin chưa có. Không đủ căn cứ phân loại manual/automated hoặc đánh giá hiệu lực thực tế.

CTL-03 và CTL-04 là **ứng viên key control**, chưa phải designation được duyệt: một cơ chế xác minh nghĩa vụ/số tiền, một cơ chế kiểm soát việc phát hành thanh toán. Nếu chúng thất bại, OBJ-02 có thể bị ảnh hưởng trực tiếp. Cần xác nhận mức trọng yếu, sự phụ thuộc vào hai cơ chế này và các kiểm soát thay thế/bù trừ trước khi quyết định keyness.

## 4. Rủi ro, kiểm soát nên có và khoảng trống

Các RSK dưới đây là **suy luận rủi ro có điều kiện**, không phải sự cố đã xảy ra. Confidence về điều kiện đang tồn tại: `Low`; cần xác minh. Các GAP chỉ là khoảng trống tài liệu/giới hạn hồ sơ hoặc candidate design gap, không phải khẳng định control không tồn tại, operating deviation hay audit finding. Nguồn kỳ vọng là mục tiêu §1–§2; cách triển khai ở cột cuối là `Target-State`, dự thảo cần validation và phê duyệt.

| Risk và control objective | Bảo vệ hiện tại, điểm còn chưa rõ | Đề xuất / thông tin cần xác minh |
|---|---|---|
| **RSK-01 → OBJ-01.** Nếu PO không được ràng buộc với nhu cầu và thẩm quyền đã duyệt, PO sai/vượt phạm vi có thể được gửi, tạo cam kết mua không phù hợp và nhận hàng ngoài nhu cầu. **COBJ-01:** cam kết mua phải phù hợp nhu cầu và quyền duyệt hợp lệ. | CTL-01 tạo cổng duyệt trước gửi PO. **GAP-01:** thiếu ma trận được dẫn; tiêu chí khớp và duyệt lại chưa mô tả (§3.1, §4). | Làm rõ CTL-01: trước gửi PO, đối chiếu với đúng bản nhu cầu đã duyệt; kiểm tra quyền duyệt theo ma trận có hiệu lực; giữ liên kết và dấu thời gian. Quy tắc duyệt lại khi sửa PO phải được người có thẩm quyền quyết định, không tự đặt ngưỡng. Yêu cầu ma trận và hồ sơ sửa/duyệt PO để xác minh. |
| **RSK-02 → OBJ-01–02.** Nếu kiểm đếm không bao phủ nhận diện/quy cách hàng, hàng sai có thể được chấp nhận và phiếu nhận sai làm cơ sở thanh toán, gây thiếu hàng phù hợp hoặc trả tiền không đúng. **COBJ-02:** phiếu nhận phản ánh đúng hàng thực nhận, phù hợp đơn đã duyệt. | CTL-02 kiểm đếm và báo chênh lệch; CTL-03 đối chiếu chứng từ về sau. **GAP-02:** tiêu chí nghiệm thu, xử lý hàng không phù hợp và bằng chứng xử lý chưa rõ (§3.2–§3.3). | Làm rõ CTL-02: kho so sánh số lượng/nhận diện hàng với PO; bổ sung kiểm tra quy cách/chất lượng theo loại hàng nếu cần, với vai trò được giao có thẩm quyền. Ghi kết quả, hàng nhận từng phần và quyết định chấp nhận/trả/giữ. Không mặc định mọi loại hàng cần cùng thủ tục. |
| **RSK-03 → OBJ-02–03.** Nếu đối chiếu không đủ chi tiết hoặc khoản chênh lệch được giải phóng thiếu căn cứ, hóa đơn sai có thể được thanh toán hoặc chênh lệch tồn đọng, gây trả sai tiền và không hoàn tất xử lý. **COBJ-03:** chỉ thanh toán nghĩa vụ đã xác minh; mọi chênh lệch có quyết định xử lý truy nguyên được. | CTL-03 có đối chiếu ba chứng từ và giữ chênh lệch; CTL-04 tạo thêm cổng phát hành. **GAP-03:** độ chính xác, phạm vi giữ, quyền giải phóng và closure chưa rõ (§3.3–§3.4). | Làm rõ CTL-03: kế toán lưu kết quả đối chiếu các trường cần thiết như nhà cung cấp, hàng, số lượng, đơn giá và tổng tiền; xác định rõ điều kiện được đưa vào thanh toán. Lập dấu vết chênh lệch–quyết định–kiểm tra lại–đóng. Dung sai, người phê duyệt ngoại lệ, thời hạn/escalation: `To be validated`. |
| **RSK-04 → OBJ-02.** Nếu dữ liệu người thụ hưởng/tài khoản sai hoặc bị thay đổi mà không được xác minh, một khoản thanh toán đúng hóa đơn vẫn có thể chuyển sai nơi, gây mất tiền và chưa trả được nhà cung cấp đúng. **COBJ-04:** người thụ hưởng và thông tin trả tiền phải hợp lệ, được xác minh. | CTL-03 hỗ trợ đối chiếu chứng từ; CTL-04 tách lập–phát hành. Hai cơ chế này chưa được mô tả là xác minh tài khoản. **GAP-04:** cơ chế xác minh dữ liệu người thụ hưởng không được mô tả trong phạm vi SOP đã đọc (§1, §3.3–§3.4). | **CTL-06, mới ở Target-State:** xác minh độc lập thông tin người thụ hưởng khi thiết lập/thay đổi, dùng nguồn liên hệ đã xác thực; lưu dữ liệu trước/sau và kết quả xác minh. Trước phát hành, CTL-04 đối chiếu lệnh với thông tin đã được xác minh. Chủ sở hữu và performer của CTL-06: `To be validated`. Hỏi về quy trình dữ liệu nhà cung cấp và kiểm soát bù trừ hiện có trước khi coi là thiếu control. |
| **RSK-05 → OBJ-02.** Nếu hóa đơn/danh sách/lệnh được gửi lại mà không kiểm tra trạng thái và lịch sử thanh toán, cùng nghĩa vụ có thể được trả nhiều lần, gây chi vượt. **COBJ-05:** mỗi nghĩa vụ hợp lệ chỉ được thanh toán một lần. | CTL-03–04 là các điểm có thể hỗ trợ, nhưng đối chiếu ba chứng từ và hai người tham gia không tự chứng minh chống trùng. **GAP-05:** kiểm tra trùng và xử lý lệnh gửi lại chưa mô tả (§1, §3.3–§3.4). | **CTL-07, mới ở Target-State:** kiểm tra dấu hiệu trùng dựa trên định danh nhà cung cấp/hóa đơn, số tiền và lịch sử/trạng thái thanh toán trước khi xử lý thanh toán, kể cả lệnh gửi lại; chỉ giải phóng cảnh báo có lý do và phê duyệt thích hợp. Lưu kết quả kiểm tra và disposition. Owner/performer: `To be validated`; có thể dùng manual hoặc hệ thống tùy khối lượng và dữ liệu, không tự chọn ERP. |
| **RSK-06 → OBJ-02.** Nếu lệnh phát hành khác danh sách được kiểm tra hoặc quyền phát hành bị sử dụng sai, thanh toán không được phép có thể ra ngoài, gây thất thoát. **COBJ-06:** lệnh thực gửi phải đúng nội dung hợp lệ và được người khác có thẩm quyền phát hành. | CTL-04 đã quy định người khác phát hành. **GAP-06:** tiêu chí review và bảo toàn nội dung danh sách–lệnh chưa rõ; chưa có thông tin quyền thực tế (§3.4, §4). | Làm rõ CTL-04: người phát hành kiểm tra người thụ hưởng, số tiền, trạng thái được thanh toán và khớp danh sách với lệnh thực gửi; lưu người lập/người phát hành, thời điểm và nội dung đã kiểm tra. Đối chiếu phân công/quyền truy cập thực tế với ma trận; không kết luận có xung đột SoD thực tế chỉ từ SOP. |
| **RSK-07 → OBJ-03.** Nếu phát hành lệnh bị coi là đã thanh toán mà không đối soát kết quả, giao dịch thất bại, ghi thiếu/trùng hoặc chênh lệch chưa xử lý có thể bị bỏ sót, làm sai số dư và đóng quy trình sớm. **COBJ-07:** trạng thái thanh toán, hóa đơn, ghi sổ và chênh lệch phải nhất quán trước khi hoàn tất. | §2 nêu end state; CTL-03 hỗ trợ xử lý chênh lệch, CTL-05 hỗ trợ truy nguyên. Chưa mô tả một control xác nhận kết quả thanh toán/đối soát. **GAP-07:** bước ghi sổ, đối soát và closure thiếu chi tiết (§2–§4). | **CTL-08, mới ở Target-State:** đối chiếu lệnh và kết quả thanh toán với nghĩa vụ/hóa đơn và sổ; xử lý lệnh thất bại/hoàn trả, giao dịch chưa ghi và chênh lệch trước đóng hồ sơ. Lưu kết quả đối soát và bằng chứng đóng từng ngoại lệ; owner, performer, nhịp đối soát và escalation: `To be validated`. |
| **RSK-08 → OBJ-01–03.** Nếu hồ sơ thiếu liên kết hoặc bị mất/sửa không truy vết, có thể không tái dựng được căn cứ nhận hàng/duyệt/trả tiền, làm khó phát hiện lỗi và xử lý tranh chấp. **COBJ-08:** hồ sơ giao dịch và quyết định phải đầy đủ, toàn vẹn và truy xuất được. | CTL-05 đã yêu cầu lưu bộ chứng từ và dấu vết duyệt. **GAP-08:** trách nhiệm, nơi lưu, quyền truy cập, thời hạn và dấu vết xử lý ngoại lệ chưa rõ (§4). | Làm rõ CTL-05: định danh liên kết toàn bộ hồ sơ, bao gồm kết quả kiểm tra và ngoại lệ, danh sách/lệnh và kết quả thanh toán; phân định người lưu, quyền sửa/xóa và yêu cầu truy xuất. Thời hạn lưu cần căn cứ áp dụng được xác nhận, không tự đặt số năm. |

Các risk rows cũng mô tả **kịch bản nếu giữ nguyên những điểm chưa rõ mà thực tế chưa có kiểm soát phù hợp**. Ví dụ, CTL-03–04 có thể vẫn cho phép trả trùng hoặc sai tài khoản nếu chúng không bao phủ hai thuộc tính này. Đây chỉ là giả thuyết phơi nhiễm, không phải kết luận còn bao nhiêu residual risk. Phải tìm các kiểm soát thay thế/bù trừ ngoài SOP và kiểm tra phạm vi, thời điểm, tính độc lập, dữ liệu, bằng chứng của chúng trước khi xác nhận gap hoặc thêm control mới.

## 5. Hồ sơ nên làm rõ tiếp theo

Theo thứ tự phụ thuộc của phân tích, không phải xếp hạng mức rủi ro:

1. Bổ sung ma trận duyệt được SOP dẫn chiếu; xác nhận phiên bản/hiệu lực SOP và các vai trò accountable. Việc này quyết định cách đọc CTL-01, CTL-04 và quyền xử lý ngoại lệ.
2. Làm rõ tiêu chí nhận hàng, đối chiếu, đối tượng bị giữ, quyền giải phóng và bằng chứng closure; cung cấp mẫu biểu/quy trình liên quan cho GAP-02–03.
3. Xác nhận cơ chế kiểm tra người thụ hưởng, chống trùng, bảo toàn danh sách–lệnh và xử lý thanh toán thất bại; cung cấp tài liệu thiết kế, phân quyền và ví dụ hồ sơ đã khử định danh cho GAP-04–07.
4. Cung cấp một walkthrough truy nguyên được từ nhu cầu đến kết quả thanh toán, ghi sổ và xử lý chênh lệch, cùng hồ sơ lưu theo §4. Walkthrough giúp xác nhận trường hợp cụ thể; không tự đại diện cho toàn kỳ. Nếu cần đánh giá vận hành rộng hơn, phải xác định objective, population, độ tin cậy dữ liệu và phương pháp kiểm thử được phê duyệt trước; chưa đặt cỡ mẫu.

Ưu tiên trước mắt là hoàn chỉnh và xác minh thiết kế kiểm soát đã có, sau đó mới quyết định cần bổ sung hay tự động hóa gì. Các đề xuất, phân công, thẩm quyền, ngưỡng và thay đổi quy trình phải được người có thẩm quyền phê duyệt; báo cáo này không phát hành SOP/RCM chính thức và không đưa ra kết luận assurance hoặc tuân thủ pháp luật.
