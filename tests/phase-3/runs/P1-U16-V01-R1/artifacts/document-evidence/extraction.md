# Trích đọc bản scan - bàn giao document/evidence

DRAFT — REQUIRES HUMAN APPROVAL. Trạng thái: READY_FOR_HUMAN_REVIEW; phần vai trò duyệt hoàn tiền bị chặn ở cấp trường, không phải đã trích đủ mọi giá trị trọng yếu.

## Phạm vi và nhận diện

- Handoff: HANDOFF-P1-U16-V01-R1-DE; extraction_run_id: P1-U16-V01-R1-DE.
- document_id: doc-9182b8b70c2027a5c8167536-0001; evidence_id: EV-P1-U16-V01-R1-001.
- Nguồn được người dùng chỉ định: `input.pdf` trong thư mục fixture hiện tại; 60.623 bytes; một trang PDF vật lý được cung cấp.
- SHA-256 byte nguồn: `9182b8b70c2027a5c81675365c6afd7383e2fbb9fa1cd7498aaf9b02f264714a`.
- Nguồn là USER_PROVIDED_COPY; nguồn gốc vật lý, người tạo/người scan, chủ thể nghiệp vụ, thời kỳ áp dụng và phiên bản nghiệp vụ: UNKNOWN. Không gọi đây là bản gốc/có chứng thực.
- Mục tiêu: cung cấp lời văn, bảng, thứ tự nhìn thấy và phần chưa đọc được để phân tích quy trình; không kết luận kiểm soát đã vận hành, hiệu lực, tính xác thực, pháp lý hoặc fraud.
- Cơ sở đọc: yêu cầu của người dùng đối với đúng PDF này, chỉ xử lý cục bộ; người nhận là tác vụ chính trong cùng phiên. Phân loại chưa được chủ nguồn xác nhận, xử lý như CONFIDENTIAL; không phát hành ra ngoài.
- Profile: `profile.generic-document` 1.0.0; common field semantics 1.0.0; phần process/table là bảng mở rộng cho mục đích trích đọc. Đây là bảng Markdown có provenance, không phải JSON extraction-package đã được chạy schema validator. Skill không khai báo version trong SKILL.md: UNKNOWN.

## Phương pháp và coverage

Native text được thử trước bằng pypdf 6.10.0: trang 1 có `raw_native_text=""`, 0 ký tự; không đồng nghĩa trang trống. PDF chứa một image object 1200×1600, 8 bit/component. Bản sao `working.pdf` có hash khớp nguồn.

Lưu ý raw inventory: thao tác inventory thực sự đọc `input.pdf`, trước khi tạo `working.pdf`; lệnh không truyền `--copy-role`, nên script ghi mặc định `WORKING_COPY`. Đó là nhãn mặc định của công cụ, không phải sự kiện tạo bản sao hay xác nhận provenance. Gói này gọi `input.pdf` là USER_PROVIDED_COPY và `working.pdf` là bản sao byte-identical được tạo sau đó. Raw `checksum.computed_at=UNKNOWN` được giữ nguyên; khoảng thời gian lệnh inventory thực tế nằm trong `tool-trace.json`, không điền lại thời điểm hash chính xác không quan sát được.

Poppler/pdftoppm 26.05.0 render toàn trang 1 ở 180 dpi, không xoay/cắt/chỉnh tương phản. Ảnh derivative: `page-1-180dpi.png`, 1530×1980 pixel, SHA-256 `9db8473ada668e58e6ff1908bb99a09bb291b04b43e1017d6e515bdbeeca6ec3`.

Đọc bằng capability xem ảnh gốc của nền tảng qua `view_image`: execution_mode=PLATFORM_NATIVE; adapter/model version=UNKNOWN, không tuyên bố đây là engine OCR chạy local. Mọi chuyển đổi tệp chạy local; không gọi dịch vụ OCR/cloud bên ngoài, không upload/mở URL. Ảnh được tool hiển thị ở 1376×1780 pixel; không tạo bounding box suy đoán từ kích thước hiển thị.

Tesseract 5.5.2 có sẵn nhưng chỉ có `eng/osd/snum`, không có `vie`; chỉ kiểm tra version/language, KHÔNG chạy OCR, không cài model. Không có OCR output hay OCR numeric confidence.

Đã xem toàn bộ 1/1 trang được cung cấp: banner, thông báo AI, tiêu đề, mục tiêu, chuỗi bước, toàn bảng 3 cột/2 hàng dữ liệu và 2 dòng cuối. Không thấy số trang in hoặc chỉ dẫn tổng số trang; completeness của toàn SOP bên ngoài tệp này: UNKNOWN. Không thấy chữ viết tay, chữ ký, dấu, QR/barcode trên trang đã xem; không xác thực sự vắng mặt ở nguồn ngoài phạm vi.

## Quy ước trường/provenance

Mọi dòng DE-Fxx dưới đây thừa hưởng document_id/evidence_id/run_id/profile/version ở trên; `source_page=1`, `bounding_box=null`; region là mô tả vị trí/bảng nhìn thấy, không phải tọa độ đo. Với trường có chữ, `source_snippet=raw_value`; `display_value=raw_value`. Không sửa chính tả, dấu, ký tự hay nội dung.

Các trường đọc trực tiếp: `method=VISION_ADAPTER`, adapter=`platform-native image viewing via view_image`, version=UNKNOWN; `normalization=PRESERVE_RAW@1.0.0`, locale=NOT_APPLICABLE. Các dimension OCR/layout/extraction/normalization/validation/overall đều không có numeric confidence; band=UNKNOWN, score=null, source=UNKNOWN. `unit=null`, `currency=null` (không có số tiền/currency để suy luận). `status_flags=[UNVERIFIED]`; reviewer/decision/reviewed_at/reviewed_value=null. Validation đối với tính đúng nghiệp vụ/human verification: NOT_TESTED; review status=PENDING. Không gọi agent visual review là human approval.

Trong bảng, “null” là giá trị rỗng có semantics ở cột trạng thái, không phải chữ in trong nguồn; các ngoặc vuông là chú thích của người trích, không phải raw text.

| field_id / field_name (group; type) | Region | raw_value | normalized_value | field_status |
|---|---|---|---|---|
| DE-F00 / scan_banner (document; TEXT) | Banner trên cùng | SYNTHETIC SCAN - SOP-SYN-16 | SYNTHETIC SCAN - SOP-SYN-16 | PRESENT |
| DE-F01 / document_title (document; TEXT) | Tiêu đề đậm dưới thông báo AI | Quy trình nhận hàng trả | Quy trình nhận hàng trả | PRESENT |
| DE-F02 / document_number (reference; IDENTIFIER) | Mã trong banner DE-F00 | SOP-SYN-16 | SOP-SYN-16 | PRESENT |
| DE-F03 / source_use_notice (security; TEXT) | Dòng ngay dưới banner | Dữ liệu tổng hợp; được phép dùng AI. | Dữ liệu tổng hợp; được phép dùng AI. | PRESENT |
| DE-F04 / process_objective (process; TEXT) | Dòng “Mục tiêu” | Mục tiêu: đối chiếu hàng và hoàn tiền đúng. | Mục tiêu: đối chiếu hàng và hoàn tiền đúng. | PRESENT |
| DE-F05 / process_sequence (process; TEXT) | Chuỗi bước phía trên bảng | Nhận yêu cầu -> kiểm đếm -> duyệt -> hoàn tiền. | Nhận yêu cầu -> kiểm đếm -> duyệt -> hoàn tiền. | PRESENT |
| DE-F06 / counting_step (table; TEXT) | DE-T01 hàng dữ liệu 1, cột Bước | Kiểm đếm | Kiểm đếm | PRESENT |
| DE-F07 / counting_role (table; TEXT) | DE-T01 hàng dữ liệu 1, cột Người thực hiện | Nhân viên kho | Nhân viên kho | PRESENT |
| DE-F08 / counting_record (table; TEXT) | DE-T01 hàng dữ liệu 1, cột Hồ sơ | Phiếu nhận | Phiếu nhận | PRESENT |
| DE-F09 / refund_approval_step (table; TEXT) | DE-T01 hàng dữ liệu 2, cột Bước | Duyệt hoàn tiền | Duyệt hoàn tiền | PRESENT |
| DE-F10 / refund_approval_role (table; TEXT) | DE-T01 hàng dữ liệu 2, cột Người thực hiện; vùng xám sọc | null | null | OBSCURED |
| DE-F11 / refund_approval_record (table; TEXT) | DE-T01 hàng dữ liệu 2, cột Hồ sơ | Ghi nhận duyệt | Ghi nhận duyệt | PRESENT |
| DE-F12 / discrepancy_exception (process; TEXT) | Dòng đầu dưới bảng | Ngoại lệ: giữ hàng để làm rõ chênh lệch. | Ngoại lệ: giữ hàng để làm rõ chênh lệch. | PRESENT |
| DE-F13 / record_linking (records; TEXT) | Dòng cuối | Lưu hồ sơ theo mã yêu cầu trả hàng. | Lưu hồ sơ theo mã yêu cầu trả hàng. | PRESENT |
| DE-F14 / document_date (date; DATE) | Đã xem toàn trang | null | null | NOT_PRESENT |
| DE-F15 / business_version (document; IDENTIFIER) | Đã xem toàn trang; “16” trong mã không được tự coi là version | null | null | NOT_PRESENT |
| DE-F16 / business_entity (party; TEXT) | Đã xem toàn trang | null | null | NOT_PRESENT |
| DE-F17 / request_receipt_role (process; TEXT) | DE-F05 có bước nhận yêu cầu; không nêu người thực hiện trên trang | null | null | NOT_PRESENT |
| DE-F18 / refund_execution_role (process; TEXT) | DE-F05 có bước hoàn tiền; không nêu người thực hiện trên trang | null | null | NOT_PRESENT |
| DE-F19 / approval_threshold (process; TEXT) | Đã xem toàn trang; không có ngưỡng/giá trị duyệt | null | null | NOT_PRESENT |
| DE-F20 / retention_duration (records; TEXT) | DE-F13 nêu cách liên kết; không nêu thời hạn lưu | null | null | NOT_PRESENT |

DE-F10: `display_value="PENDING_HUMAN_CONFIRMATION"`, `source_snippet=null`, flags=`[UNVERIFIED,HUMAN_REVIEW_REQUIRED]`, validation=HUMAN_REVIEW_REQUIRED, review_required=true; không coi là blank, không gán tên/chức danh. Không xác định được nguyên nhân vùng che hay đây có phải redaction chủ ý; không thử khôi phục.

DE-F14…DE-F20: `display_value="NOT_PRESENT_ON_SUPPLIED_PAGE"`; chỉ là “không thấy được nêu trên trang cung cấp”, không kết luận việc/kiểm soát/chính sách thực tế không tồn tại. Critical document/date/version và vai trò/ngưỡng cần owner xác nhận nếu được dùng để thiết kế/trách nhiệm.

Ngôn ngữ cho profile: DE-F21 / language (document; TEXT), raw_value=null (không có trường ngôn ngữ in sẵn), normalized_value=`["vi","en"]`, display_value="Tiếng Việt; banner tiếng Anh", field_status=INFERRED; basis=DE-F00+DE-F01…DE-F13; method=RULE_DERIVED, rule=LANGUAGE_FROM_VISIBLE_CONTENT@1.0.0, locale=NOT_APPLICABLE; không phải thông số OCR. Confidence UNKNOWN; human review PENDING.

## Bảng và thứ tự quan sát

DE-T01: một bảng vật lý trên trang 1; headers nguyên văn `Bước | Người thực hiện | Hồ sơ`; 3 cột, 1 header row, 2 data rows. Không có continuation, tổng cộng hay dòng trùng lặp quan sát được.

| Hàng nguồn | Bước | Người thực hiện | Hồ sơ | Field refs |
|---|---|---|---|---|
| 1 | Kiểm đếm | Nhân viên kho | Phiếu nhận | DE-F06/DE-F07/DE-F08 |
| 2 | Duyệt hoàn tiền | [OBSCURED - không đọc được] | Ghi nhận duyệt | DE-F09/DE-F10/DE-F11 |

Chuỗi DE-F05 chỉ thể hiện thứ tự lời văn. Không có decision diamond/nhánh vẽ; không chèn nhánh từ chối, SLA, hạn mức hay trình tự xử lý ngoại lệ. DE-F12 nêu “giữ hàng”, không nêu “giữ tiền”; không đồng nhất hai nội dung.

## Cảnh báo nguồn và preflight

DE-F03 được giữ nguyên như tuyên bố trong nguồn: “Dữ liệu tổng hợp; được phép dùng AI.” Đây là source statement, không phải chứng cứ độc lập về nguồn gốc/đồng ý hay quyền mở rộng phạm vi. Không thấy cảnh báo cấm AI trên trang đã xem.

Inventory `thien-document-inventory` 1.0.0 dùng byte-pattern heuristic gắn `ACTIVE_CONTENT_JAVASCRIPT` (tìm pattern /JS hoặc /JavaScript). Poppler/pdfinfo 26.05.0 báo JavaScript=no; pypdf 6.10.0 duyệt cấu trúc tĩnh 8 indirect objects, không thấy key/action trong tập /JS, /JavaScript, /AA, /OpenAction, /Launch, /EmbeddedFiles, /URI, /XFA, /AcroForm, /Sig, /RichMedia, /Encrypt. Discrepancy được giữ; không coi byte-pattern là một action được xác nhận, cũng không gọi PDF an toàn malware/có xác thực. Không thực thi action, macro, code hoặc liên kết.

PDF không mã hóa theo hai parser; extension/signature/MIME khớp PDF; page count 1. Metadata có title “Synthetic degraded scan SOP-SYN-16”, Author/Creator “anonymous”, Producer ReportLab và ngày năm 2000; đây là metadata không xác thực, KHÔNG dùng làm ngày ban hành/hiệu lực hay định danh chủ thể. Chi tiết raw ở `native-inspection.json`.

## Human-review queue và hạn chế bàn giao

| review_item_id | Field/object | Vấn đề và hành động cần người có thẩm quyền | Trạng thái |
|---|---|---|---|
| DE-HR-01 | DE-F10 / DE-T01 row 2 col 2 | Vai trò duyệt hoàn tiền bị che. Cần bản rõ/được phép đọc hoặc xác nhận chức danh từ owner có thẩm quyền, ghi nguồn xác nhận; không điền phỏng đoán. Tác động: chưa chốt trách nhiệm duyệt/SoD. | PENDING; critical; phần trường BLOCKED |
| DE-HR-02 | DE-F14…DE-F20 và completeness | Xác nhận đây là bản đủ/đúng phiên bản/phạm vi sử dụng; cung cấp nguồn date/version/entities và các vai trò/ngưỡng/thời hạn còn thiếu nếu cần cho triển khai. Không giả định từ metadata. | PENDING |
| DE-HR-03 | DE-F00…DE-F21 / DE-T01 | Chủ nguồn/reviewer đối chiếu transcription với trang và phê duyệt mục đích dùng; agent visual reading không thay human verification. Không có reviewer/approval nào đã được ghi. | PENDING |

JSON chi tiết của queue ở `human-review.json`. Không có kết luận process-risk/control-effectiveness trong gói này. Không có giao dịch thực tế hay bằng chứng vận hành được cung cấp; các tên hồ sơ trong SOP không chứng minh hồ sơ đã được lập/duyệt.

## QA thực hiện trong phạm vi

- Hash nguồn trước/sau đọc và hash working copy khớp cùng digest; chỉ chứng minh byte equality ở các lần kiểm tra đã ghi.
- Native extraction và toàn trang render được giữ; coverage đọc 1/1 trang native image page, field coverage còn DE-F10 bị che.
- 2 hàng×3cột đều có source field refs; ô che không bị bỏ qua hoặc đổi thành tên đoán.
- Raw/normalized và absent/obscured/inferred phân biệt; không thêm threshold/date/version từ suy luận.
- Chưa có human validation, bản rõ cho DE-F10 hoặc kiểm chứng completeness nguồn ngoài tệp.
- Không thực hiện schema-validator JSON extraction-package, reconciliation hoặc authenticity/security certification; không có kết luận thay thế cho các kiểm tra đó.

Các artifact chỉ nằm trong thư mục output được chỉ định; không thay đổi nguồn. `tool-trace.json` ghi các thao tác thật và giới hạn, không phải exported host transcript đầy đủ.
