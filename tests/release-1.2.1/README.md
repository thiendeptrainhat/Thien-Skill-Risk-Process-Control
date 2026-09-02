# Release qualification 1.2.1

Đây là qualification dành riêng cho patch metadata `1.2.1` ngày 02/09/2026.

## Phạm vi

- Đổi Display Name thành `Thiện's Skill — Risk-Control-Process Intelligence`.
- Giữ nguyên skill ID `thien-skill-risk-control-process`, repository và package basename `Thien-Skill-Risk-Control-Process`.
- Bỏ giới hạn tổng `dist` 32 MiB theo xác nhận của owner; vẫn giữ 3 MiB/file và 8 MiB/release directory.
- Xác minh deterministic metadata, source binding, validator/tooling, archive parity và checksum.

## Phân tách bằng chứng

Không có behavioral model run mới cho `1.2.1`. Trường `behavioral_evaluations` trong `qualification-results.json` là mảng rỗng và manifest ghi số scenario mới bằng `0`.

Bằng chứng nghiệp vụ gần nhất vẫn thuộc release `1.2.0` tại `tests/release-1.2.0/qualification-results.json`. Report `1.2.1` chỉ tham chiếu report đó bằng path và SHA-256 với quan hệ `inherited_not_reexecuted_or_relabelled`; không sao chép raw output, không đổi version của receipt và không tính ba scenario cũ thành lần chạy mới.

## Giới hạn

- Claude/ChatGPT live behavior: `not_run`.
- Native installation/discovery: `not_run`.
- Cross-platform behavioral equivalence: `not_run`.
- `skill-creator` quick validator không chạy bằng Python mặc định do thiếu PyYAML; không cài dependency mới. Validator đi kèm skill và các gate dự án được ghi riêng.

`qualification-results.json` là receipt máy đọc được cho release này. ZIP và packaging report nằm tại `dist/1.2.1/` sau khi builder hoàn tất.
