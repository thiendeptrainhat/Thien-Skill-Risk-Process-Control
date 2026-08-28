# Phase 1 — Thiết kế cập nhật Thien-Skill-Risk-Process-Control

Ngày lập: 27/08/2026 · Baseline: 1.0.0 · Trạng thái: bản thiết kế chờ người dùng duyệt.

## Kết quả cần đọc

| Tài liệu | Nội dung |
|---|---|
| [UPDATE-DESIGN.md](UPDATE-DESIGN.md) | Phạm vi, mục tiêu R01–R07, workflow, cấu trúc dữ liệu, handoff và bản đồ thay đổi Phase 2 |
| [REFERENCE-LIBRARY-CATALOG.md](REFERENCE-LIBRARY-CATALOG.md) | Danh mục nguồn ứng viên, bằng chứng tra cứu, giới hạn truy cập và quyền sử dụng |
| [ACCEPTANCE-MATRIX.yaml](ACCEPTANCE-MATRIX.yaml) | Đặc tả kiểm thử, fixture, hành vi cần quan sát và điều kiện không đạt cho Phase 3 |
| [REVIEW-AND-DECISIONS.md](REVIEW-AND-DECISIONS.md) | Kiểm tra Phase 1, giới hạn, các quyết định còn mở và điều kiện chuyển phase |

## Phạm vi đã được ủy quyền

Người dùng đồng ý triển khai **Phase 1** của kế hoạch một đợt nâng cấp qua ba phase:

1. Thiết kế và tiêu chí nghiệm thu — phạm vi bộ tài liệu này.
2. Cập nhật nội dung vận hành của skill — chưa được thực hiện.
3. Kiểm thử hành vi, cập nhật tài liệu phát hành và đóng ZIP — chưa được thực hiện.

Đây không phải bản skill mới và không phải báo cáo đã đạt behavioral tests. Các tài liệu nằm ngoài thư mục skill để không tự trở thành hướng dẫn vận hành hay tài nguyên đóng gói.

## Nguyên tắc của phương án nâng cấp

- Một skill lõi; tên hiển thị **Thien-Skill-Risk-Process-Control**, ID **thien-skill-risk-process-control**.
- Phân tích theo phạm vi E2E mở; 94 profiles hiện có là ví dụ tham chiếu, không phải danh mục đóng.
- Tận dụng công cụ được phép của host; không bắt buộc MCP/API riêng.
- Document-Evidence là năng lực phối hợp tùy nhu cầu; không sao chép OCR chuyên sâu vào skill này.
- Giữ bốn analysis layers, yêu cầu bằng chứng và nguyên tắc không tự suy đoán.
- Giữ logo, license hiện tại và ngôn ngữ trả lời theo người dùng.
- Giữ định hướng ba gói Claude, ChatGPT và Universal từ cùng nguồn. Không cài đặt trong phạm vi hiện tại.

## Kết quả thiết kế

Skill sau nâng cấp được thiết kế để trả lời bảy câu hỏi: E2E phù hợp; risk; expected/key controls có căn cứ; current controls theo mức bằng chứng; gap; cải tiến; và rủi ro nếu giữ nguyên. Mỗi kết luận phải có nguồn hoặc được nhận diện là đề xuất/chưa đủ cơ sở.

Ma trận có **25 nhóm kiểm thử, 32 biến thể dự kiến** bao phủ bảy mục tiêu nghiệp vụ và sáu yêu cầu xuyên suốt. Toàn bộ vẫn ở trạng thái **not_run**; Phase 1 chỉ xác minh thiết kế, cấu trúc và coverage, chưa xác minh hành vi skill sau nâng cấp.

Danh mục ban đầu có **11 nguồn bên ngoài ứng viên**, không phải 11 kết nối đã cài:

- 9 nguồn có trang giới thiệu/catalog chính thức đọc được; chưa đồng nghĩa đã đọc toàn bộ tài nguyên hoặc được phép sử dụng toàn văn trong AI.
- 2 nguồn chuyên ngành không mở được trong phiên tra cứu và được giữ ở trạng thái hạn chế truy cập.
- Các điều kiện AI-use của ISO được ghi riêng; không tự đưa toàn văn ISO vào baseline.
- Danh mục có thể mở rộng khi engagement phát sinh; không giới hạn ngành theo danh sách ban đầu.

## Cách duyệt

Đọc UPDATE-DESIGN trước, sau đó kiểm tra nguồn và acceptance matrix. Các chi tiết là đề xuất triển khai, không giả định người dùng đã phê duyệt mọi lựa chọn nguồn hoặc schema.

Không cần mua tài liệu, cấp thêm quyền hay lựa chọn một ngành cố định để hoàn thành Phase 1. Chỉ cần giải quyết quyền truy cập khi một công việc cụ thể thật sự phụ thuộc nguồn đó.

Trước Phase 2 cần người dùng chấp thuận bộ thiết kế và chốt nhãn phiên bản phát hành. Đề xuất phiên bản bổ sung là **1.1.0** nếu thay đổi vẫn tương thích; chưa thay version trong repository.
