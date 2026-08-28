DỮ LIỆU TỔNG HỢP; mọi nguồn dưới đây được phép đọc, dùng AI và lưu/tái phân phối trong bộ test.
OBJ-19A: chỉ sử dụng tài khoản nhà cung cấp đã được xác nhận. OBJ-19B: trả đúng nghĩa vụ được duyệt.
PROC-19A: từ nhận yêu cầu đổi tài khoản đến phê duyệt/lưu master data. PROC-19B: từ nhận hóa đơn đến duyệt, trả tiền và đối chiếu sổ.
REQ-19 §2: Quy định nội bộ được phê duyệt cho cả hai quy trình yêu cầu xác nhận thay đổi tài khoản bằng kênh độc lập trước lần thanh toán đầu tiên; hồ sơ xác nhận phải có locator.
SOP-19A §3: CTL-SHARED-19 là dịch vụ trung tâm xác nhận beneficiary. Người cập nhật master data gọi dịch vụ và lưu status.
SOP-19B §4: Cùng CTL-SHARED-19, cùng cấu hình và cơ chế vận hành, được gọi trước phát lệnh. Người phát lệnh khác người lập; đối chiếu PO/nhận hàng/hóa đơn trước lập lệnh.
EVD-19A: bản checklist ký ngày 10/07/2026 cho beneficiary B-19 ghi VERIFIED; phần nguồn cuộc gọi để trống.
EVD-19B: trace trung tâm xuất cùng ngày cho B-19 ghi PENDING_REVIEW tại thời điểm trước phát lệnh. Chủ nguồn chưa giải thích sự khác nhau.
EVD-19C: lệnh TX-19 đã phát ngày 10/07/2026. Đây là một trường hợp được cung cấp, không phải full population.
Chưa có phương pháp chấm risk, thông tin ngân sách, owner/due date cho cải tiến hoặc approval key-control designation.
