# Danh mục nguồn tham khảo — Phase 1

Ngày tra cứu: **27/08/2026**. Đây là danh mục ứng viên và nhật ký mức kiểm chứng, không phải kho standards, thư viện controls hoàn chỉnh hay danh sách connector đã cài.

## 1. Cách đọc và giới hạn

- **overview_verified:** đọc được trang giới thiệu/catalog chính thức; chỉ xác nhận nội dung quan sát tại đó.
- **content_verified:** phải đọc đúng tài nguyên/điều khoản cần cho một claim. Phase 1 không gán trạng thái này cho toàn bộ framework.
- **access_limited:** không đọc được trang/tài nguyên trong môi trường tra cứu; không dùng search snippet làm baseline.
- **rights_to_check:** quyền dùng nội dung cụ thể chưa được xác lập; không đồng nghĩa cấm mọi hình thức tham khảo công khai.
- **restricted_pending_permission:** đã thấy điều kiện hạn chế liên quan; không đưa nội dung hạn chế vào AI baseline khi chưa có cơ sở quyền phù hợp.

Mức access, content verification, quyền sử dụng trong AI và quyền tái phân phối phải ghi riêng. Một metadata/date, trang công khai hoặc quyền mua/đọc tài liệu không tự chứng minh các quyền còn lại.

Đề xuất Phase 2 chỉ đưa vào skill tên nguồn, đường dẫn chính thức, công dụng, điều kiện lựa chọn và giới hạn. **Không đóng gói full-text, workbook, bảng taxonomy/control catalog hoặc credential của bên thứ ba.**

Các ghi chú “nên dùng” bên dưới là quyết định thiết kế được đề xuất, không phải tuyên bố nguồn áp dụng bắt buộc cho tổ chức của người dùng.

## 2. Nguồn để định hướng cấu trúc quy trình

### LIB-P01 — APQC Process Classification Framework

- **Loại nguồn:** taxonomy phân cấp, đa ngành; không phải một E2E workflow có sẵn hoặc control standard.
- **Nguồn đã đọc:** [PCF FAQ](https://www.apqc.org/process-frameworks/pcf-faqs), [Cross-Industry Excel 8.0](https://www.apqc.org/resource-library/resource-listing/apqc-process-classification-framework-pcf-cross-industry-excel-12).
- **Quan sát:** trang tài nguyên ghi 8.0, 27/02/2026 và Public Content. FAQ phân biệt classification với thứ tự thực hiện, cho phép mapping nhiều reference items.
- **Kiểm chứng:** overview_verified; workbook/PDF và giấy phép bên trong chưa đọc.
- **Quyền:** rights_to_check cho nội dung chi tiết/AI-use; chưa xác lập quyền tái phân phối.
- **Nên dùng:** điểm khởi đầu cho taxonomy, tên và cross-reference; giữ thứ tự workflow của organization là thiết kế riêng.
- **Không dùng:** ép mọi hoạt động vào PCF, suy số thứ tự PCF thành sequence, lấy PCF làm control baseline.

### LIB-P02 — Microsoft Dynamics 365 Business Process Catalog

- **Loại nguồn:** vendor blueprint/E2E scenarios gắn với Dynamics 365.
- **Nguồn đã đọc:** [Microsoft Learn — About the catalog](https://learn.microsoft.com/en-us/dynamics365/guidance/business-processes/about). [Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=108187) là endpoint tài nguyên, nhưng lần xác minh lại trả lỗi công cụ.
- **Quan sát:** trang giới thiệu có cấu trúc business process catalog và liên hệ với scenario/triển khai sản phẩm. Chưa đọc workbook.
- **Kiểm chứng:** overview_verified; không pin edition workbook vì nội dung tải xuống chưa được kiểm chứng.
- **Quyền:** rights_to_check theo từng tài nguyên; không suy license của một GitHub repo sang workbook Download Center.
- **Nên dùng:** gợi ý E2E/interfaces, đặc biệt khi context có Dynamics hoặc cần đối chiếu thiết kế ERP.
- **Không dùng:** mặc định cấu hình sản phẩm là chuẩn trung lập, control bắt buộc hay sự thật về hệ thống của tổ chức.

### LIB-P03 — ASCM SCOR Digital Standard

- **Loại nguồn ứng viên:** reference model chuyên supply chain; phân loại này là định hướng nghiên cứu, chưa nghiệm thu nội dung trong phiên.
- **Trang đã thử:** [SCOR DS](https://www.ascm.org/corporate-solutions/standards-tools/scor-ds/), [Open Access Guidance](https://www.ascm.org/corporate-solutions/standards-tools/scor-ds/open-access-guidance/).
- **Quan sát:** công cụ trả HTTP 403; không đọc được nội dung hai trang. Không vượt chặn hoặc đăng nhập.
- **Kiểm chứng:** access_limited; version, nội dung chi tiết và license chưa xác minh. Từ “open access” trong tên link không là bằng chứng quyền sử dụng.
- **Nên dùng:** chỉ giữ trong candidate index để xác minh bằng nguồn/truy cập hợp lệ khi cần.
- **Không dùng:** gán edition, tái phân phối catalog hoặc khẳng định benchmark dựa trên nguồn chưa đọc.

### LIB-P04 — TM Forum Business Process Framework / eTOM

- **Loại nguồn ứng viên:** taxonomy/reference framework chuyên doanh nghiệp dịch vụ/viễn thông; chưa nghiệm thu nội dung trong phiên.
- **Trang đã thử:** [eTOM](https://www.tmforum.org/open-digital-architecture/process-framework-etom/), [GB921 resource endpoint](https://www.tmforum.org/resources/suite/gb921-business-process-framework-etom-suite-v25-5/).
- **Quan sát:** không mở được trang; resource trả HTTP 403. Không xác nhận edition chỉ từ URL hoặc kết quả tìm kiếm.
- **Kiểm chứng:** access_limited; full text, version và membership/license conditions chưa xác minh.
- **Nên dùng:** candidate chuyên ngành; yêu cầu xác minh tài nguyên cụ thể trước mapping.
- **Không dùng:** ép mọi ngành theo viễn thông; coi taxonomy là workflow thực tế hoặc nguồn compliance controls đã xác minh.

## 3. Nguồn cho risk, control objective và baseline

### LIB-C01 — COSO Internal Control — Integrated Framework

- **Loại nguồn:** internal-control framework.
- **Nguồn đã đọc:** [COSO Internal Control](https://www.coso.org/internal-control).
- **Quan sát:** trang giới thiệu nhận diện framework được cập nhật năm 2013 và có các tài liệu bổ sung riêng. Đây không phải bằng chứng đã đọc đầy đủ framework hoặc mọi guidance.
- **Kiểm chứng:** overview_verified; không xác nhận một control/điều khoản chi tiết.
- **Quyền:** rights_to_check cho từng publication; không đóng gói lại nội dung framework.
- **Nên dùng:** định hướng control objectives và cấu trúc đánh giá khi nội dung cần dùng đã được tiếp cận hợp lệ.
- **Không dùng:** coi COSO là danh sách key controls chi tiết cho mọi process, hoặc đồng nghĩa pháp luật.

### LIB-C02 — ISO 9001

- **Loại nguồn:** catalog của tiêu chuẩn hệ thống quản lý chất lượng.
- **Nguồn đã quan sát:** [ISO 9001 catalog](https://www.iso.org/standard/62085.html).
- **Metadata quan sát:** ISO 9001:2015, edition 5, amendment 1:2024; trang nói đang chuẩn bị bản thay thế. Không hard-code bản này là hiện hành mãi hoặc coi draft tương lai đã có hiệu lực.
- **Kiểm chứng:** overview_verified; không đọc full text hoặc dùng clause làm baseline trong Phase 1.
- **Quyền:** restricted_pending_permission cho nội dung hạn chế sử dụng trong AI; xem Mục 5. Không cho rằng mua PDF tự giải quyết điều kiện AI-use.
- **Nên dùng:** directory pointer/metadata để nhận diện nguồn cần kiểm tra quyền và applicability.
- **Không dùng:** tự ingest tiêu chuẩn hoặc gắn đáp ứng ISO khi chưa có nội dung được phép dùng và căn cứ áp dụng.

### LIB-C03 — ISO 31000

- **Loại nguồn:** catalog của hướng dẫn quản lý rủi ro.
- **Nguồn đã quan sát:** [ISO 31000 catalog](https://www.iso.org/standard/65694.html).
- **Metadata quan sát:** ISO 31000:2018, edition 2; version của từng tài nguyên vẫn phải kiểm tra lúc dùng.
- **Kiểm chứng:** overview_verified; không đọc full text, không tạo baseline theo điều khoản trong Phase 1.
- **Quyền:** restricted_pending_permission như ghi chú ISO tại Mục 5.
- **Nên dùng:** nhận diện tài liệu methodology cần kiểm tra quyền/applicability trước khi dùng nội dung.
- **Không dùng:** suy một risk-scoring scale cụ thể hoặc một bộ control bắt buộc chỉ từ tên ISO 31000.

### LIB-C04 — ISACA COBIT

- **Loại nguồn:** framework về governance/management của enterprise information and technology.
- **Nguồn đã đọc:** [ISACA COBIT](https://www.isaca.org/resources/cobit).
- **Quan sát:** trang giới thiệu liệt kê bộ COBIT 2019 và publication Governance and Management Objectives; không đọc toàn bộ sách.
- **Kiểm chứng:** overview_verified; không xác nhận các chi tiết practice/control trong tài nguyên bán riêng.
- **Quyền:** rights_to_check theo publication; không mua, đăng nhập hoặc tải sách trong Phase 1.
- **Nên dùng:** benchmark governance/IT process khi có nhu cầu và nội dung hợp lệ.
- **Không dùng:** mặc định áp dụng đầy đủ cho mọi process hoặc biến objectives thành cấu hình/control đã triển khai.

### LIB-C05 — NIST Cybersecurity Framework

- **Loại nguồn:** cybersecurity outcomes/framework và current/target organizational profiles.
- **Nguồn đã đọc:** [CSF resource center](https://www.nist.gov/cyberframework), [CSF 2.0 Profiles](https://www.nist.gov/cyberframework/profiles).
- **Quan sát:** trang cung cấp CSF 2.0 và tài nguyên lập current/target profiles để phân tích khoảng cách.
- **Kiểm chứng:** overview_verified; từng outcome và informative reference phải được đọc/xác minh khi dùng.
- **Quyền:** tài nguyên công khai; kiểm tra điều kiện cho nội dung/third-party mappings cụ thể, không mặc định mọi file có cùng quyền.
- **Nên dùng:** cyber-related outcomes và profile comparison, không thay toàn bộ process architecture.
- **Không dùng:** coi mọi outcome là một key control cụ thể hoặc áp dụng toàn CSF cho mọi SOP.

### LIB-C06 — NIST SP 800-53 / Cybersecurity and Privacy Reference Tool

- **Loại nguồn:** security/privacy control catalog và dữ liệu tham chiếu.
- **Nguồn đã đọc:** [SP 800-53 Rev. 5 publication](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), [CPRT catalog](https://csrc.nist.gov/projects/cprt/catalog).
- **Quan sát:** publication có planning note về release 5.2.0; CPRT liệt kê dataset 5.2.0. Revision của publication và release của dataset là metadata khác nhau.
- **Kiểm chứng:** overview_verified; chưa tải hoặc đối chiếu từng control/dataset.
- **Quyền:** công khai để tra cứu; kiểm tra điều kiện của file/mapping được chọn, đặc biệt nội dung bên thứ ba.
- **Nên dùng:** tìm candidate controls cho security/privacy có scope phù hợp và rationale.
- **Không dùng:** áp dụng toàn catalog mặc định; suy equivalence từ crosswalk một mình hoặc bỏ qua parameters/context.

## 4. Nguồn notation — không phải E2E/control library

### LIB-N01 — OMG Business Process Model and Notation

- **Loại nguồn:** chuẩn notation/modeling.
- **Nguồn đã đọc:** [BPMN 2.0.2 specification landing page](https://www.omg.org/spec/BPMN/2.0.2).
- **Quan sát:** trang nhận diện 2.0.2, normative PDF và machine-readable artifacts. Không đọc toàn specification trong Phase 1.
- **Kiểm chứng:** overview_verified.
- **Quyền:** rights_to_check theo tài nguyên; không bundle specification.
- **Nên dùng:** semantics/notation khi phải vẽ hoặc trao đổi process model; kiểm tra phần cụ thể trước khẳng định conformance.
- **Không dùng:** coi sơ đồ BPMN đúng cú pháp là quy trình đúng, controls tốt hay vận hành hiệu quả.

## 5. Quan sát quan trọng về quyền và phiên bản

### ISO: quyền AI-use cần được kiểm tra riêng

Footer của [trang ISO đã mở](https://www.iso.org/standard/62085.html) nêu hạn chế dùng nội dung cho AI, ngoài ngoại lệ Open data theo điều kiện riêng. Vì vậy thiết kế không tự ingest full text ISO. Chỉ mở đường xử lý nội dung khi có quyền phù hợp được xác minh hoặc tài nguyên Open data cụ thể có điều kiện cho phép; không suy quyền từ việc người dùng có bản PDF.

Đây là ghi nhận điều kiện công bố để thiết kế access gate, không phải kết luận pháp lý về một hợp đồng/license cụ thể. Không sao chép điều khoản dài vào skill và không coi một câu “đồng ý” của người dùng là thay thế giấy phép của bên có quyền.

### Metadata thay đổi không đồng nghĩa nguồn nào cũng phải được đọc lại toàn bộ

Khi engagement cần baseline, xác minh edition, amendment, status và đúng nội dung liên quan. Ghi ngày/nguồn kiểm tra; không tự gán ngày hết hạn cố định hoặc “latest” dựa trên tên file.

Ví dụ thiết kế rút ra từ việc tra cứu: framework publication, dataset release và workbook download có thể mang metadata khác nhau. Phải ghi đúng object/version đã đọc, không dùng một version chung cho cả hệ nguồn.

## 6. Cách chọn nguồn khi skill được kích hoạt

1. Xác định câu hỏi: classification/E2E, controls, regulatory obligations hay notation.
2. Xem nguồn tổ chức đã cung cấp/adopt và quyền xử lý trong engagement; không mặc định thư viện ngoài có precedence cao hơn policy/luật áp dụng.
3. Chọn một số nguồn có scope phù hợp trong catalog; tìm nguồn chính thức ngoài catalog nếu cần.
4. Kiểm tra access/AI-use và quyền gửi dữ liệu trước retrieval. Dùng truy vấn chung đã loại thông tin nhạy cảm.
5. Mở đúng trang/nội dung hợp lệ và lưu locator/version/check date; metadata không thay clause verification.
6. Gắn classification với E2E organization-specific bằng rationale. Tách source requirement, interpretation và proposed control.
7. Nếu không truy cập được, ghi limitation; không vượt chặn, bịa nguồn hoặc tuyên bố fully benchmarked.

Nguồn nội bộ, luật/quy định chuyên ngành và thư viện ngành khác là **source slots mở**, không bị loại vì không nằm trong 11 nguồn. Chỉ thêm record khi đã biết publisher, phạm vi và authority từ engagement. Không giả định jurisdiction Việt Nam chỉ vì license của skill theo pháp luật Việt Nam.

## 7. Chuyển sang Phase 2

Catalog này đủ để thiết kế một source-discovery guide, chưa đủ để tạo sẵn toàn bộ key-control baseline. Phiên bản skill tương lai phải kiểm tra nội dung đúng cho từng case và nêu giới hạn.

Hai nguồn access_limited vẫn tùy chọn, không làm hỏng phần phân tích khác. Nếu người dùng cần kết nối tự động với một thư viện hạn chế, đó là quyết định tích hợp riêng sau khi chốt quyền, cách truy cập và phạm vi.
