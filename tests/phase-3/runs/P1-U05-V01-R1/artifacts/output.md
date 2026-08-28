# Quy trình đề xuất cho dịch vụ bảo dưỡng thiết bị tận nơi

Đề xuất quản lý mỗi yêu cầu bằng một hồ sơ xuyên suốt, với ba điểm chốt: **được phép thực hiện và đã thống nhất chi phí → đạt kiểm tra chất lượng và được khách nghiệm thu → đối chiếu thanh toán, đóng hồ sơ**. Bắt đầu bằng mô hình thử nghiệm có kiểm soát; chưa cần quyết định tự động hóa toàn bộ.

Đây là **Target-State, bản thảo v0.1 để thảo luận**, chưa phải SOP được phê duyệt. Tất cả bước, vai trò, kiểm soát và hồ sơ bên dưới là đề xuất; không phải hiện trạng đã xác minh.

## 1. Căn cứ và phạm vi

- Nguồn: BRIEF-05 §1–§3, đọc toàn bộ nội dung được cung cấp. Giữ nguyên lưu ý nguồn: “DỮ LIỆU TỔNG HỢP; được phép phân tích trong AI.” Phiên bản, ngày, chủ sở hữu và người phê duyệt brief: `Not provided`.
- Theo §1, dịch vụ chưa hoạt động; mục tiêu là thiết bị hoạt động trở lại, khách chấp nhận kết quả cùng hồ sơ chi phí. Theo §2, phạm vi mong muốn kéo dài đến thanh toán. Theo §3, chưa có SOP, hệ thống, người phụ trách, ngân sách hoặc cam kết thời gian được duyệt.
- Không có baseline vận hành để kết luận control hiện hữu, lỗi vận hành hay khoảng trống hiện trạng. Thiết kế được duyệt: `Not provided`; không gắn đề xuất này là As-Designed hoặc As-Performed.
- Confidence: `Medium` đối với ý định được mô tả trong một nguồn; `Low` đối với tính khả thi thực tế, cần xác nhận loại thiết bị, năng lực, nhu cầu và chi phí. `review_status: Not reviewed`.

Tên quy trình đề xuất riêng cho dịch vụ: **Yêu cầu bảo dưỡng → Khôi phục, nghiệm thu và thanh toán**; không gán tên hoặc mã của thư viện bên ngoài.

Mục tiêu dùng để thiết kế:

- **OBJ-01:** Khôi phục chức năng thiết bị và có kết quả được khách chấp nhận [§1]. An toàn khi thực hiện là điều kiện thiết kế đề xuất, cần chuyên môn xác nhận.
- **OBJ-02:** Khách chấp nhận hồ sơ chi phí và nghĩa vụ thanh toán được xử lý, có dấu vết đối chiếu [§1–§2].

Điểm bắt đầu là khách gửi yêu cầu. Kết thúc bình thường khi đã nghiệm thu, khách chấp nhận chi phí và tiền được xác nhận theo thỏa thuận. Hồ sơ không sửa được, khách hủy hoặc còn tranh chấp phải có trạng thái riêng; không tính là hoàn thành thành công. Mua vật tư, nhà thầu ngoài và bảo hành sau bàn giao là các giao diện cần chốt, chưa được mặc định là quy trình hiện có. Chưa thiết kế thao tác kỹ thuật, cấu hình hệ thống hoặc đưa ra kết luận pháp lý.

## 2. Luồng công việc và điểm kiểm soát

Bảng này đồng thời là step register và phân công theo vai trò đề xuất. Một “điều phối” giữ đầu mối hồ sơ từ đầu đến cuối; người giữ vai trò thực tế và quyền quyết định đều cần được chỉ định. Đầu vào ban đầu gồm thông tin liên hệ tối thiểu, thiết bị, triệu chứng, địa điểm và nhu cầu; các trường cụ thể cần chốt theo phạm vi dịch vụ. Các bước dựa trên chuỗi mong muốn ở §2; thứ tự chi tiết, nhánh và hồ sơ là thiết kế đề xuất.

| Bước | Người thực hiện đề xuất | Công việc, đầu ra và chuyển bước | Nhánh ngoại lệ / kiểm soát |
|---|---|---|---|
| STEP-01 — Tiếp nhận | Điều phối | Tạo mã hồ sơ, kiểm tra thông tin, xác nhận nhu cầu và chuyển đánh giá kỹ thuật. | Thiếu thông tin: yêu cầu bổ sung, giữ trạng thái chờ; hủy hoặc đóng theo quy tắc sẽ được duyệt, không tự coi im lặng là đồng ý. CTL-01, CTL-07. |
| STEP-02 — Đánh giá nhu cầu | Phụ trách kỹ thuật | Đối chiếu yêu cầu với loại thiết bị được phục vụ, năng lực, điều kiện tiếp cận và khả năng đáp ứng; xác định cần khảo sát tại chỗ hay có thể báo phạm vi sơ bộ. | Ngoài năng lực hoặc chưa đánh giá được nguy cơ: không nhận cam kết khôi phục; chuyển người có chuyên môn xem xét hoặc từ chối có lý do. CTL-01, CTL-03. |
| STEP-03 — Thỏa thuận sơ bộ và đặt lịch | Điều phối | Gửi phạm vi dự kiến, phí khảo sát/di chuyển nếu có, nguyên tắc báo giá và hủy lịch; xác nhận khách đồng ý rồi kiểm tra người, dụng cụ, vật tư trước khi chốt lịch. | Không đồng ý: sửa đề nghị hoặc đóng yêu cầu. Thiếu nguồn lực/khách đổi lịch: cập nhật lịch được hai bên xác nhận; không hứa SLA chưa được duyệt. CTL-01, CTL-02. |
| STEP-04 — Khảo sát và cho phép làm | Kỹ thuật viên; phụ trách kỹ thuật xử lý ngoại lệ | Kiểm tra thực trạng tại nơi làm, xác nhận điều kiện an toàn, phạm vi cuối cùng, tiêu chí kết quả và báo giá. Có chấp thuận của khách trước phần công việc phát sinh nghĩa vụ chi phí. | Không an toàn: dừng và báo phụ trách kỹ thuật. Không sửa được hoặc khách không chấp thuận: kết thúc ngoại lệ; phí nào được thu phải dựa trên thỏa thuận trước đó. CTL-02, CTL-03. |
| STEP-05 — Thực hiện | Kỹ thuật viên | Làm trong phạm vi đã duyệt; ghi công việc, vật tư, thay đổi và kết quả vào hồ sơ; chuyển kiểm tra chất lượng. | Phát sinh ngoài phạm vi: dừng phần phát sinh, quay STEP-04 để đánh giá và xin chấp thuận; không làm trước rồi hợp thức hóa giá. CTL-02, CTL-03, CTL-07. |
| STEP-06 — Kiểm tra chất lượng | Người kiểm tra chất lượng được chỉ định | Đối chiếu kết quả với tiêu chí kỹ thuật đã duyệt cho loại thiết bị; lưu phép kiểm tra và kết quả trước khi chuyển nghiệm thu. | Không đạt: ghi lỗi, quay STEP-04 để quyết định làm lại hoặc dừng. Chỉ làm lại khi an toàn, khả thi và được phép; nếu không, đóng ngoại lệ có phương án xử lý. Không đặt số lần làm lại tùy ý. CTL-03, CTL-04. |
| STEP-07 — Nghiệm thu | Điều phối, với xác nhận của khách | Trình bày kết quả, hướng dẫn bàn giao và bảng chi phí so với báo giá; lấy xác nhận riêng của khách về kết quả và chi phí. | Khách không chấp nhận: ghi rõ phần tranh chấp; kỹ thuật về STEP-04, chi phí về CTL-02/CTL-06 để xử lý. Chưa có xác nhận thì giữ chờ/tranh chấp, không ghi nghiệm thu thành công. CTL-05. |
| STEP-08 — Thanh toán và đóng hồ sơ | Phụ trách thanh toán; điều phối đóng hồ sơ | Đối chiếu hồ sơ được chấp nhận với khoản phải thu và bằng chứng tiền thực nhận; lưu chứng từ phù hợp rồi đóng hồ sơ đủ điều kiện. | Chưa trả: trạng thái chờ thanh toán. Sai lệch/hoàn tiền: chuyển người có thẩm quyền quyết định, lưu lý do và đối chiếu lại; chỉ đóng ngoại lệ khi có quyết định hợp lệ. CTL-06, CTL-07. |

Mọi hồ sơ chờ cần có đầu mối, lý do, hành động tiếp và ngày xem lại được giao. Quy tắc hết thời gian chờ, dừng làm lại, xử lý nợ và escalation: `To be validated`; không để vòng lặp mở vô hạn.

## 3. Rủi ro và kiểm soát đề xuất

Đây là kịch bản rủi ro suy luận từ dịch vụ dự kiến, **không phải sự cố đã xảy ra**. Căn cứ là OBJ-01/02 và BRIEF-05 §1–§3; chi tiết kiểm soát là analyst proposal, chưa được đối chiếu với một chuẩn bắt buộc. Chưa chấm inherent/residual risk vì chưa có phương pháp được duyệt.

| Rủi ro | Chuỗi nguyên nhân → sự kiện → tác động và mục tiêu | Bước liên quan |
|---|---|---|
| RSK-01 | Thông tin hoặc đánh giá nguồn lực không đủ → nhận việc/đặt lịch vượt khả năng → chậm hoặc không khôi phục được thiết bị, ảnh hưởng OBJ-01. | STEP-01–03 |
| RSK-02 | Phạm vi, thay đổi và giá không được thống nhất → thực hiện/thu phí ngoài sự đồng ý → tranh chấp hồ sơ chi phí, ảnh hưởng OBJ-02. | STEP-03–05, 07–08 |
| RSK-03 | Điều kiện nơi làm hoặc phương pháp chưa được xác nhận phù hợp → thao tác gây tai nạn/hư hại → tổn hại người, tài sản và khả năng khôi phục an toàn, ảnh hưởng OBJ-01. | STEP-02, 04–06 |
| RSK-04 | Tiêu chí kiểm tra hoặc nghiệm thu không rõ → đánh dấu hoàn tất khi chức năng chưa đạt/khách chưa chấp nhận → làm lại, khiếu nại, ảnh hưởng OBJ-01/02. | STEP-06–07 |
| RSK-05 | Khoản phải thu, điều chỉnh và tiền thực nhận không được đối chiếu → thu sai, bỏ sót hoặc ghi nhận thanh toán chưa xảy ra → thất thu/tranh chấp, ảnh hưởng OBJ-02. | STEP-08 |
| RSK-06 | Hồ sơ phân tán hoặc quyền truy cập không phù hợp → mất, sửa sai hoặc lộ dữ liệu dịch vụ → không truy nguyên được việc/chi phí và ảnh hưởng khách hàng, tác động OBJ-01/02. | STEP-01–08 |

| Kiểm soát / mục tiêu kiểm soát | Ai, khi nào và thực hiện thế nào — đều là đề xuất | Hồ sơ cần lưu và xử lý ngoại lệ |
|---|---|---|
| CTL-01 — Chỉ nhận và đặt lịch cho yêu cầu đủ thông tin, trong năng lực (RSK-01) | Điều phối kiểm tra từng yêu cầu; phụ trách kỹ thuật xác nhận khả năng phục vụ theo danh mục thiết bị, năng lực và nguồn lực đã được duyệt, trước khi cam kết lịch. | Phiếu yêu cầu, kết quả sàng lọc, phân công/lịch được xác nhận. Thiếu điều kiện: giữ chờ hoặc chuyển phụ trách kỹ thuật quyết định từ chối/đề xuất lịch khác. |
| CTL-02 — Công việc và chi phí có chấp thuận phù hợp (RSK-02) | Điều phối quản lý phiên bản báo giá; người có quyền giá nội bộ duyệt theo ma trận sẽ được chốt; khách chấp thuận phạm vi và giá trước thực hiện, kể cả thay đổi. Dùng báo giá gốc và yêu cầu thay đổi để so sánh. | Báo giá, chấp thuận có thời điểm, bảng thay đổi; không chỉ dựa vào lời kể sau khi làm. Chưa đủ duyệt: dừng phần liên quan; chuyển người có quyền quyết định, không tự vượt hạn mức. |
| CTL-03 — Chỉ thực hiện trong điều kiện an toàn được chấp nhận (RSK-03) | Kỹ thuật viên kiểm tra trước thao tác và khi điều kiện thay đổi, theo tiêu chí do người có chuyên môn phù hợp xác lập; phụ trách kỹ thuật review trường hợp không rõ. | Phiếu đánh giá điều kiện, quyết định cho phép/dừng. Có nguy cơ chưa giải quyết: dừng, ghi nhận và báo người có thẩm quyền kỹ thuật; không dùng quyền duyệt giá để bỏ qua an toàn. Đây không phải hướng dẫn kỹ thuật. |
| CTL-04 — Kết quả đáp ứng tiêu chí kỹ thuật (RSK-04) | Người kiểm tra chất lượng kiểm tra từng công việc trước bàn giao, so với tiêu chí được duyệt theo thiết bị; mức độ độc lập và năng lực người kiểm tra cần chốt trước thử nghiệm. | Checklist có kết quả thực tế, người kiểm tra, thời điểm và lỗi còn mở. Không đạt: không chuyển nghiệm thu; chuyển phụ trách kỹ thuật phê duyệt hướng xử lý/làm lại. |
| CTL-05 — Khách chấp nhận kết quả và hồ sơ chi phí (RSK-02, RSK-04) | Điều phối đối chiếu kết quả QC, báo giá/thay đổi với bảng chi phí và lấy xác nhận khách tại STEP-07. Sự đồng ý về chi phí không thay cho đạt kỹ thuật, và ngược lại. | Biên bản/xác nhận nghiệm thu, bảng chi phí, ý kiến chưa thống nhất. Thiếu hoặc bị từ chối: giữ trạng thái chờ/tranh chấp; chuyển kỹ thuật hoặc người có quyền thương mại theo nội dung. |
| CTL-06 — Thu, điều chỉnh và đóng tài chính đúng hồ sơ (RSK-05, RSK-02) | Phụ trách thanh toán đối chiếu mỗi khoản thu/điều chỉnh với báo giá được duyệt, nghiệm thu hoặc thỏa thuận phí ngoại lệ và bằng chứng giao dịch thực nhận. Người khác có thẩm quyền duyệt hoàn tiền/miễn giảm theo phân quyền được chốt. | Bảng đối chiếu, chứng từ thu, quyết định điều chỉnh. Sai lệch: không ghi đã thanh toán hoặc tự xóa nợ; chuyển người có quyền xử lý và lưu kết quả đối chiếu lại. |
| CTL-07 — Hồ sơ đầy đủ, truy nguyên được và truy cập đúng quyền (RSK-06) | Điều phối kiểm tra hồ sơ theo mã yêu cầu tại mỗi chuyển bước; người quản trị hồ sơ được chỉ định kiểm soát quyền và thay đổi. Chỉ thu dữ liệu cần thiết; người nhận bàn giao xác nhận tiếp nhận. | Lịch sử trạng thái, phiên bản và quyền truy cập. Thiếu/mâu thuẫn: trả về người lập để xử lý, không sửa mất bản gốc; mất truy cập: dùng phương án tạm được duyệt và đối chiếu sau khôi phục. |

CTL-03 và CTL-04 là **ứng viên key control**, vì dự kiến là các điểm chặn chính đối với thao tác không an toàn và bàn giao kết quả không đạt; sự nghiệm thu của khách không tự thay thế được hai kiểm tra này. Chưa có bằng chứng về kiểm soát thay thế, mức rủi ro hoặc phê duyệt keyness; phụ trách kỹ thuật và người có thẩm quyền quản trị rủi ro cần review. Các kiểm soát còn lại vẫn cần thiết nhưng không mặc định đều là key.

Tên người, control owner chịu trách nhiệm cuối cùng, người thay thế, ngưỡng duyệt, thời gian escalation, công cụ và thời hạn lưu hồ sơ: `To be validated`. Phân công ở trên là gợi ý vai trò thực hiện, không tự gán một người làm mọi owner. Chưa kết luận hiệu lực vận hành. Khi thử nghiệm, cần kiểm tra thực sự có thể truy từ hồ sơ đến người thực hiện, thời điểm, tiêu chí, kết quả và việc xử lý ngoại lệ.

## 4. Phương án triển khai

| Phương án | Lợi ích và đánh đổi dự kiến | Điều kiện phụ thuộc |
|---|---|---|
| A — Minimum-control proposal; tuân thủ chưa xác minh | Biểu mẫu chuẩn, sổ hồ sơ dùng chung có kiểm soát quyền và xác nhận thủ công. Ít tích hợp ban đầu nhưng phụ thuộc kỷ luật cập nhật, đối chiếu và năng lực điều phối. | Chốt người, biểu mẫu, quyền, nơi lưu và phương án dự phòng; xác nhận số lượng hồ sơ có thể quản lý. |
| B — Cân bằng kiểm soát và hiệu suất | Công cụ quản lý yêu cầu/lịch, trạng thái bắt buộc và lưu phê duyệt. Có thể giảm nhập lại, nhưng cần cấu hình, đào tạo và quản lý thay đổi. | Quy tắc đã rõ, dữ liệu thống nhất, ngân sách và người quản trị công cụ. |
| C — Tự động hóa cao | Tích hợp đặt lịch, vật tư, báo giá và thanh toán. Có thể hỗ trợ quy mô lớn hơn; phát sinh rủi ro phân quyền, tích hợp và xử lý ngoại lệ. | Có dữ liệu nhu cầu, quy trình ổn định, business case và kiểm thử đầy đủ trước áp dụng. |

Đề xuất lấy **A làm điểm xuất phát để kiểm chứng mô hình**, với cùng các điểm chốt chất lượng, an toàn và chi phí nêu trên; chuyển B khi dữ liệu cho thấy nhu cầu. C chưa có căn cứ để ưu tiên ở giai đoạn ý tưởng. Đây là so sánh định tính, confidence `Low`; chi phí, thời gian triển khai, số người và mức giảm rủi ro của cả ba phương án chưa được ước tính. Không gọi phương án nào là “đã tuân thủ”.

## 5. Những quyết định anh/chị cần chốt

1. **Phục vụ việc gì, ở đâu?** Loại thiết bị, khách hàng, địa bàn, việc nhận/không nhận; phân biệt bảo dưỡng với sửa chữa khôi phục. Chốt trường hợp phải chuyển chuyên gia hoặc từ chối.
2. **Bán kết quả hay công việc?** Phí khảo sát, di chuyển, nhân công, vật tư; điều kiện thu phí khi không khôi phục được; hủy lịch, phát sinh và phạm vi cam kết/bảo hành. Không mặc định “không sửa được vẫn thu đủ” hoặc “luôn miễn phí”.
3. **Thế nào là an toàn và hoàn thành?** Người đủ thẩm quyền xác lập tiêu chí kỹ thuật theo thiết bị, kiểm tra chất lượng, nghiệm thu; điều kiện dừng/làm lại và xử lý khách không chấp nhận. Chưa đủ quyết định này thì chưa nhận việc thực tế thuộc phạm vi tương ứng.
4. **Ai chịu trách nhiệm và ai có quyền duyệt?** Chỉ định chủ quy trình, người thực hiện, control/risk owner, người thay thế; quyền duyệt giá, thay đổi, ngoại lệ, hoàn tiền và đóng hồ sơ. Kiêm nhiệm có thể được xem xét, nhưng người tự lập điều chỉnh không nên tự duyệt; độc lập QC cần thiết kế theo rủi ro. Chưa có dữ liệu để kết luận SoD thực tế.
5. **Nguồn lực và cam kết phục vụ?** Nhu cầu dự kiến, năng lực kỹ thuật, dụng cụ, vật tư/nhà thầu, lịch làm việc, ngân sách và trần thử nghiệm. SLA cần xác định mốc bắt đầu/dừng, thời gian chờ khách/vật tư và người xử lý trễ; chưa đặt con số tùy ý.
6. **Dùng hồ sơ và công cụ nào?** Chọn nguồn dữ liệu chính, quyền xem/sửa, lưu trữ, người quản trị, sao lưu/khôi phục và cách xử lý khi người/công cụ không sẵn sàng. Thời hạn lưu và mức độ dự phòng cần căn cứ thực tế, chưa thể kết luận SPOF.
7. **Điều kiện thương mại và nghĩa vụ áp dụng?** Chốt địa bàn/pháp nhân, điều khoản khách hàng, chứng từ, bảo vệ dữ liệu và nghĩa vụ chuyên ngành theo loại thiết bị. Chuyển người có chuyên môn xác minh trước mở dịch vụ; bản này không thực hiện tra cứu pháp luật hoặc xác nhận tuân thủ.
8. **Khi nào được thử nghiệm và mở rộng?** Chọn người phê duyệt, phạm vi/khối lượng thử nghiệm, tiêu chí đạt và điều kiện dừng. Chạy thử các nhánh: yêu cầu bình thường, không an toàn, phát sinh giá, QC không đạt, khách từ chối, thiếu tiền và mất truy cập hồ sơ. Ghi kết quả rồi quyết định sửa thiết kế, tiếp tục hoặc dừng; chưa ấn định số ca, ngân sách hay ngày khai trương.

Sau khi chốt, nên đo thời gian từ tiếp nhận đến nghiệm thu/thanh toán (KPI), hồ sơ khiếu nại hoặc phải làm lại (KRI), và mức đầy đủ của bằng chứng phê duyệt/QC (KCI). Đây mới là hướng đo; công thức, mẫu số, nguồn, người quản lý, nhịp review và ngưỡng phản ứng cần được duyệt từ dữ liệu thử nghiệm, chưa có target mặc định.

Nếu chưa triển khai, chưa phát sinh rủi ro vận hành của dịch vụ này. Nếu mở dịch vụ khi các quyết định trên còn bỏ ngỏ, những kịch bản RSK-01–06 có thể xuất hiện mà trách nhiệm và điểm chặn chưa rõ; đây là dự báo có điều kiện, không phải phát hiện hiện trạng. Chỉ ban hành SOP, áp dụng quyền hạn hoặc đưa quy trình vào vận hành sau khi người có thẩm quyền phê duyệt thiết kế và các điều kiện liên quan.
