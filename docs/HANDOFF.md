# Handoff — Thien-Skill-Risk-Control-Process 1.1.1

Cập nhật: **28/08/2026**. Bản này chỉ đổi tên skill từ `Thien-Skill-Risk-Process-Control` sang `Thien-Skill-Risk-Control-Process`; không thay nội dung nghiệp vụ.

## Phạm vi đã thống nhất

- Tên hiển thị mới: `Thien-Skill-Risk-Control-Process`.
- Skill ID và thư mục mới: `thien-skill-risk-control-process`.
- Phiên bản package: `1.1.1`; schema nghiệp vụ vẫn giữ version đã có, không tăng đồng loạt.
- Giữ nguyên điều khoản `LICENSE`, `LICENSE-VERSION`, third-party notices và toàn bộ logo/assets. Trong `NOTICE` chỉ đổi tên sản phẩm; `LICENSE-APPLICATION.md` chỉ đồng bộ tên, ID và phiên bản được áp dụng, không sửa điều khoản cấp phép.
- Repository hiện là [thiendeptrainhat/Thien-Skill-Risk-Control-Process](https://github.com/thiendeptrainhat/Thien-Skill-Risk-Control-Process), **public**. Người dùng xác nhận đã tự chuyển sang public và yêu cầu đổi URL, commit/push. Không đổi chủ sở hữu, thư mục workspace, bản đã cài hoặc quyền/tài khoản khác.
- Commit/push được người dùng yêu cầu riêng trong bước publication tiếp nối; đối chiếu Git history và remote để xác nhận commit thực tế. Không cài đặt, tạo GitHub Release/tag, thêm OCR hay connector.

## Tài nguyên hiện hành

| Tài nguyên | Mục đích |
|---|---|
| [README](../README.md) | Vai trò, lợi ích và cách dùng ở trước; cài đặt ở dưới |
| [INSTALL](../INSTALL.md) | Đường dẫn và cách gọi ID mới; lưu ý thay/tắt ID cũ |
| [Canonical SKILL.md](../skills/thien-skill-risk-control-process/SKILL.md) | Một lõi skill, 49 files |
| [Release manifest](../RELEASE-MANIFEST.yaml) | Version 1.1.1, tên ZIP, roots và SHA-256 |
| [Ba ZIP 1.1.1](../dist/1.1.1/) | Claude / ChatGPT / Universal, cùng nội dung nghiệp vụ |
| [SHA256SUMS](../dist/1.1.1/SHA256SUMS) / [packaging report](../dist/1.1.1/packaging-report.json) | Kiểm tra archive và parity |
| [Kiểm tra đổi tên](../tests/rename-1.1.1/) | Kết quả thực, tooling output và giới hạn |

## Kiểm tra và ranh giới kết luận

Ba ZIP mới được tạo từ cùng nguồn và qua validator, kiểm tra roots/parity/CRC/checksum. Bộ 61 tooling tests và sáu regression tests riêng cho phép kiểm tra đổi tên đã chạy đạt. `scripts/verify_rename.py` đối chiếu từng file với baseline Git: chỉ cho phép các thay thế định danh đã liệt kê và version package; mọi thay đổi nghiệp vụ, schema, điều khoản license, logo hoặc lịch sử đều phải bị báo lỗi. Kết quả trước publication giữ tại `tests/rename-1.1.1/results.json`; kiểm tra sau cập nhật URL/trạng thái hiện hành tại `tests/rename-1.1.1/publication-results.json`.

Trình `quick_validate.py` của skill-creator không chạy được với Python mặc định vì thiếu PyYAML; không cài thêm dependency. Dùng validator đi kèm và kiểm tra YAML của môi trường sẵn có; không trình bày lỗi môi trường đó thành một pass của quick-validator.

Không chạy lại model behavioral tests hoặc native discovery/activation cho ID mới. Kết quả Phase 3 — 29 model variants / 95 judgments, sáu capability-simulation profiles và các ca chat/Word/PDF, NIST, Document-Evidence — chỉ thuộc snapshot **tên cũ 1.1.0**. Static equivalence không phải một lần thực thi model mới hoặc bảo đảm mọi nền tảng.

## Giữ nguyên và đọc lại lịch sử

URL cũ và nhãn PRIVATE trong `LICENSE-APPLICATION.md`, ZIP và bằng chứng đã tạo được giữ như metadata lịch sử trước khi người dùng chuyển public/đổi tên repository. Không sửa điều khoản license hoặc ghi đè ZIP 1.1.1. README, INSTALL, manifest và remote phản ánh URL/trạng thái mới. Việc công khai không tự chuyển license thành open-source hoặc cấp quyền sử dụng ngoài các điều khoản đã có.

Baseline trước đổi tên là commit [db9b0f4](https://github.com/thiendeptrainhat/Thien-Skill-Risk-Control-Process/tree/db9b0f42c1a2ce0938abc888a03699d401b9fd41). Bản 1.0.0/1.1.0 trong `dist`, toàn bộ hồ sơ Phase 1–3, raw outputs, reviews, snapshots và các kết quả cũ được giữ nguyên byte. Không đổi input path/hash hay gán pass mới cho receipt cũ.

Do các tài liệu/receipts lịch sử tham chiếu tên và nguồn cũ, hãy đọc tại cây Git baseline để các liên kết tương đối đúng phiên bản. [Báo cáo Phase 3 tại baseline](https://github.com/thiendeptrainhat/Thien-Skill-Risk-Control-Process/blob/db9b0f42c1a2ce0938abc888a03699d401b9fd41/docs/phase-3/REPORT.md) và [handoff trước đổi tên](https://github.com/thiendeptrainhat/Thien-Skill-Risk-Control-Process/blob/db9b0f42c1a2ce0938abc888a03699d401b9fd41/docs/HANDOFF.md) giữ bối cảnh đầy đủ.

`scripts/verify_rename.py --historical` dựng cây baseline đó trong thư mục tạm và chạy lại validator cũ. Gate `evidence_complete` nếu đạt chỉ là gate **1.1.0**; không áp dụng cho tên/ZIP mới. Không chạy mặc định `--phase3` hay assemble lại evidence index cũ trên cây đã đổi tên.

## Lệnh kiểm tra

```sh
python3 -B scripts/run_tests.py --json
python3 -B -m unittest discover -s tests/phase-3/tooling -v
python3 -B -m unittest discover -s tests/rename-1.1.1 -v
python3 -B scripts/verify_rename.py --historical
python3 -B scripts/build_release.py --write --json
```

Lệnh build chỉ xác nhận `unchanged` nếu ZIP đã có khớp tuyệt đối; không ghi đè bản phát hành khác. Xem [INSTALL](../INSTALL.md#8-cập-nhật-và-gỡ-lỗi) để chuyển từ ID cũ sang ID mới mà không kích hoạt trùng. Policy/SOP/RCM/target-state vẫn là draft, Document-Evidence vẫn tùy chọn và các giới hạn nghiệp vụ không thay đổi.
