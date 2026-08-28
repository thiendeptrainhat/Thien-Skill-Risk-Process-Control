DỮ LIỆU TỔNG HỢP — CONSUMER-ONLY. Packet hư cấu, không phải kết quả một lượt Document-Evidence/OCR thật. Được phép xử lý trong AI.
packet_id: SYN-PACKET-16
extraction_run_id: SYN-EXTRACT-16
source_id: SRC-SCAN-16
document_id: DOC-16
method: synthetic_manual_transcription
source_access_and_ai_use_conditions: được phép đọc, dùng AI và lưu trong bộ test; không có dữ liệu thật
coverage: trang 1 đầy đủ phần mục tiêu; trang 2 bảng phê duyệt chỉ đọc được một phần
readable_content:
  - locator: trang 1, mục 1
    raw: Quy trình nhận hàng trả nhằm đối chiếu số lượng và quyết định hoàn tiền.
    status: TRANSCRIBED
  - locator: trang 2, bảng 1, hàng 1
    raw: Nhân viên nhận ghi số lượng, trưởng ca xem xét.
    status: TRANSCRIBED
  - locator: trang 2, bảng 1, hàng 2, ô Người duyệt
    raw: 'G... đốc'
    normalized: null
    status: HUMAN_REVIEW_REQUIRED
    evidence_id: UP-EVD-16-02
warnings: chữ mờ ở người duyệt; chưa xác minh phân quyền
review_status: UNVERIFIED
human_review_queue: xác nhận ô Người duyệt trang 2 trước khi kết luận thẩm quyền.
