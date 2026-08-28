# Phase 2 — Cập nhật nội dung vận hành

Ngày: 28/08/2026. Trạng thái: **Phase 2 hoàn tất — nguồn 1.1.0 chưa phát hành**.

## Phạm vi và phiên bản

Người dùng đã yêu cầu triển khai Phase 2 theo [thiết kế Phase 1](../phase-1/UPDATE-DESIGN.md). Nội dung nguồn hướng tới **1.1.0 — unreleased**, kế thừa bản 1.0.0 tại commit `d65fad595e0265dbe665477b6a5747faa5811139`.

Phase 2 cập nhật skill, references, templates, metadata định tuyến và ví dụ. Không phải bản phát hành hoặc nghiệm thu hành vi. ZIP, manifest, checksum, README/INSTALL phát hành và hồ sơ kiểm thử 1.0.0 được giữ nguyên cho đến Phase 3.

## Nội dung đã hiện thực

| Mục tiêu | Nội dung vận hành |
|---|---|
| R01 — Hiểu E2E | Nhận chat/PDF/Word, xác định objective/trigger/outcome/boundary; mapping ngoài 94 seeds, nhiều E2E hoặc chưa đủ cơ sở |
| R02 — Risk | Giữ cause–event–impact–objective, tách dữ kiện khỏi suy luận và sự kiện đã xảy ra |
| R03 — Expected/key controls | Tra cứu nguồn theo scope và quyền; tách source-derived expectation khỏi analyst proposal, giải thích keyness |
| R04 — Current controls | Giữ logical control ID và observation riêng theo lớp, phạm vi, kỳ, nguồn và bằng chứng |
| R05 — Gaps | So sánh theo control objective/coverage, kể cả alternatives; không coi thiếu mô tả/evidence là không có control |
| R06 — Cải tiến | Gắn recommendation với gap hoặc design opportunity; nêu trade-off, dependency và approval |
| R07 — Nếu giữ nguyên | No-change scenario có risk driver, existing protection, exposure, uncertainty; không bịa loss/probability/score |

Tài nguyên chính:

- [Skill entrypoint](../../skills/thien-skill-risk-process-control/SKILL.md).
- [External process/control library discovery](../../skills/thien-skill-risk-process-control/references/external-process-control-libraries.md).
- [Common data model và migration rules](../../skills/thien-skill-risk-process-control/references/data-model-qa-execution.md).
- [Control baseline comparison](../../skills/thien-skill-risk-process-control/templates/control-baseline-comparison.yaml).
- [Document-Evidence handoff](../../skills/thien-skill-risk-process-control/references/governance-security-handoffs.md#61-document-evidence-handoff-tùy-chọn).

## Các ranh giới được giữ

- Một core skill, theo ngôn ngữ người dùng; không thêm OCR engine, API/MCP server hay dependency bắt buộc.
- Danh mục 11 nguồn là pointers và snapshot nghiên cứu 27/08/2026, không phải kết nối đã cài hoặc baseline đã xác minh cho mọi engagement. Không tra cứu lại nguồn hoặc tải full text ở Phase 2.
- Document-Evidence là phối hợp tùy chọn. Native input đủ thì dùng trực tiếp; packet synthetic/được cung cấp không chứng minh specialist đã chạy.
- Giữ license/logo/assets và bản skill đã cài. Chưa commit, push, cài đặt hoặc phát hành.

## Dữ liệu và khả năng đọc output cũ

Giữ fields 1.0.0, IDs, null, locators và `design_assessment`. Fields mới là bổ sung; không đổi tên ngầm hoặc tự suy current state từ dữ liệu thiếu. Schema có thay đổi dùng 1.1.0, schema không đổi giữ version cũ.

| Identifier | Vai trò |
|---|---|
| CTL | Logical control, có thể liên kết nhiều processes/risks |
| OBS | Ghi nhận hoặc đánh giá control theo layer/scope/kỳ |
| MAP | Mapping process với reference item |
| CBL | Liên kết baseline với source/objective/candidate control |
| CMP | So sánh baseline và các observations |
| NCS | No-change scenario |
| OPP | Design opportunity, không cần tạo gap hiện trạng giả |

Kiểm tra giữ fields ở cấp cấu trúc không thay kiểm thử migration/hành vi bằng model. Phần đó vẫn thuộc Phase 3.

## Kiểm tra và giới hạn

Kết quả trên snapshot nguồn cuối được lưu tại [STRUCTURAL-CHECKS.json](STRUCTURAL-CHECKS.json):

- Canonical package validator: 9 nhóm kiểm tra đạt, không có lỗi hoặc cảnh báo; bao gồm cấu trúc, metadata, links, assets và các bản license.
- Ruby/Psych: parse thành công 21 file YAML và frontmatter; không có duplicate mapping keys. Metadata giữ trạng thái unreleased, runtime verification false và không có dependency bắt buộc mới.
- Đối chiếu cấu trúc 18 template YAML cũ với baseline: không mất hoặc thay giá trị legacy; chỉ 8 template được nâng schema lên 1.1.0. Nội dung 94 seed profiles không đổi.
- Rà soát 20 file Markdown: 211 local links, gồm 120 anchor links, không thiếu đích. `git diff --check` đạt.
- Rà soát độc lập đã khép 4 điểm: workflow anchor, điều kiện dùng nguồn trong handoff, tách test design khỏi executed results, và null state `Unresolved`.

Script `quick_validate.py` của `skill-creator` không chạy được do thiếu PyYAML; không cài dependency. Các kiểm tra thay thế ở trên đã chạy, nhưng không ghi script này là đạt.

Behavioral tests, migration bằng model, live lookup/document ingestion và xác minh từng nền tảng vẫn **not_run**; không suy từ YAML/package hợp lệ thành skill đã vận hành đúng. Dữ liệu mới là phần mở rộng: chưa cam kết consumer strict schema 1.0.0 chấp nhận schema 1.1.0.

Chỉ thay 22 file nguồn runtime đã có, thêm 2 tài nguyên runtime và hồ sơ Phase 2. Không sửa scripts/tests/dist hoặc tài liệu, license, metadata phát hành 1.0.0; các file Phase 1 và `.DS_Store` có sẵn được giữ nguyên.

Theo `skill-creator`, nội dung dùng progressive disclosure: entrypoint chỉ định tuyến tới phần cần đọc; không nạp toàn bộ thư viện hoặc nhân bản OCR.

## Chuyển sang Phase 3

Phase 3 cần được người dùng cho phép riêng: tạo fixtures, chạy và review bộ kiểm thử đã thiết kế, xác minh capability thực tế, cập nhật runner/builder và tài liệu phát hành, đồng bộ version declarations rồi đóng ba ZIP từ cùng snapshot. Không tự cài lên Claude/ChatGPT/Codex hoặc commit/push vì hoàn tất Phase 2.

Các khai báo license/application và release manifest hiện vẫn mô tả bản 1.0.0; việc đồng bộ phạm vi phiên bản mới là bước chuẩn bị phát hành, không sửa hồi tố lịch sử hoặc điều khoản license.
