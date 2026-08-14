# Cài đặt Thien-Skill-Risk-Process-Control 1.0.0

Ba file ZIP được sinh khi chạy release build từ cùng một nguồn chuẩn. Chúng có cùng nội dung nghiệp vụ, version và license; chỉ khác cấu trúc đóng gói hoặc metadata theo bề mặt đích.

## Gói Claude

File: `Thien-Skill-Risk-Process-Control-v1.0.0-Claude.zip`

- Dùng chức năng upload custom skill trên bề mặt Claude có hỗ trợ ZIP.
- ZIP có một thư mục skill ở cấp cao nhất; trong đó `SKILL.md` là entry point.
- Gói không chứa metadata riêng của OpenAI.
- Việc Claude Desktop hoặc Claude Web hiển thị chức năng upload phụ thuộc tài khoản, workspace và tính năng đang được Anthropic cung cấp.

## Gói ChatGPT

File: `Thien-Skill-Risk-Process-Control-v1.0.0-ChatGPT.zip`

- Dùng chức năng upload/import personal skill trên bề mặt ChatGPT có hỗ trợ.
- ZIP có một thư mục skill ở cấp cao nhất, `SKILL.md`, và `agents/openai.yaml` cho metadata giao diện OpenAI.
- ChatGPT Desktop và ChatGPT Web có thể yêu cầu import riêng theo từng tài khoản hoặc workspace; package này chỉ chuẩn bị artifact, không tự cài đặt hoặc publish.

## Gói Universal `.agents`

File: `Thien-Skill-Risk-Process-Control-v1.0.0-Universal.zip`

- Giải nén tại thư mục gốc phù hợp để nhận đường dẫn:
  `.agents/skills/thien-skill-risk-process-control/SKILL.md`.
- Dùng cho Codex và các môi trường đọc skill từ `.agents/skills/`, gồm ChatGPT Desktop khi bề mặt đó hỗ trợ thư mục skill cục bộ.
- Nếu giải nén vào vị trí khác, sao chép nguyên thư mục `thien-skill-risk-process-control` vào `.agents/skills/`; không tách riêng `SKILL.md` khỏi các thư mục `references`, `templates`, `examples`, `assets` và `scripts`.

## Kiểm tra sau khi giải nén

1. Xác nhận chỉ có một thư mục mang mã `thien-skill-risk-process-control` tại vị trí cài đặt.
2. Xác nhận `SKILL.md`, `LICENSE`, `LICENSE-APPLICATION.md`, `NOTICE` và `THIRD-PARTY-NOTICES.md` tồn tại.
3. Trước khi giải nén, kiểm tra hash của chính file ZIP bằng `dist/SHA256SUMS`; file checksum này không liệt kê hash của từng file bên trong archive.
4. Khởi động lại hoặc yêu cầu bề mặt đích nạp lại skill nếu cần.
5. Gọi skill bằng tên `thien-skill-risk-process-control` hoặc chọn skill trong giao diện được hỗ trợ.

## Giới hạn và quyền sử dụng

Repository nguồn là private tại `https://github.com/thiendeptrainhat/Thien-Skill-Risk-Process-Control`. Có ZIP hoặc cài đặt thành công không tự cấp quyền sử dụng. Đọc `LICENSE`, `LICENSE-APPLICATION.md` và `NOTICE` trước khi sử dụng hoặc phân phối.
