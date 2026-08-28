DỮ LIỆU TỔNG HỢP; nguồn và bằng chứng đều hư cấu, được phép dùng AI và lưu/tái phân phối trong bộ test.
REF-12 §4: Hướng dẫn advisory của tổ chức Hư Cấu khuyến nghị người rà soát đối chiếu hóa đơn trùng trước thanh toán. Mục tiêu: ngăn trả cùng nghĩa vụ nhiều lần. Không quy định công nghệ bắt buộc.
CONFIG-12 v5 §2: Hệ thống hiện được cấu hình chặn trùng theo supplier_id + invoice_number + amount trước phát lệnh. Tài khoản vận hành không được đổi cấu hình. Ngoại lệ đưa vào hàng chờ và một người khác xem xét.
LOG-12: Một giao dịch trùng ngày 03/07/2026 bị chặn; một ngoại lệ được chuyển review, chưa phát lệnh.
SOP-12 §5: Người kiểm soát xem hàng chờ ngoại lệ hằng ngày và giữ log giải quyết.
Chưa có kiểm thử các biến thể đổi số hóa đơn, kiểm thử thay đổi cấu hình hoặc coverage toàn kỳ.
