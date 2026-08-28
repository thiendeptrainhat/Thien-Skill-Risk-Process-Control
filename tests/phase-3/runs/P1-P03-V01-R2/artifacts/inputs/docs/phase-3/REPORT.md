# Phase 3 — kiểm thử và đóng gói 1.1.0

Ngày thực hiện: **28/08/2026** (Asia/Ho_Chi_Minh).

**29/29 biến thể model trên snapshot cuối đã chạy và được review đạt; ba ZIP 1.1.0 đã được tạo, kiểm tra checksum và parity.** Phạm vi model là `Codex desktop delegated local runtime`, không phải chứng nhận cài đặt hoặc behavior của mọi nền tảng. Gate tổng hợp, bao gồm kiểm tra chính báo cáo release này (P03), nằm tại `current_release_gate` trong [kết quả máy](../../tests/phase-3/acceptance-results.json); không suy từ exit code của runner hoặc tự gán pass từ nội dung báo cáo.

## Phạm vi và cách đọc bằng chứng

Phase 3 kiểm tra bản nâng cấp Phase 2 theo [ma trận đã duyệt](../phase-1/ACCEPTANCE-MATRIX.yaml): 25 nhóm, gồm 29 biến thể model và ba kiểm tra packaging/release. R01–R07 là E2E, risk, expected/key controls, current controls, gap, improvement và no-change exposure; X01–X06 là portability, quyền nguồn, an toàn, handoff, traceability và giới hạn kết luận.

Mỗi biến thể model được gọi bằng `collaboration.spawn_agent`, `fork_turns=none`, với prompt đã lưu, input tổng hợp riêng và đúng snapshot. Executor không nhận rubric/đáp án. Reviewer gốc đọc câu trả lời và trace sau khi chạy, chấm từng invariant với locator; không sửa raw output để đạt. Reviewer không phải người sinh câu trả lời nhưng có tham gia soạn skill/fixtures, **không phải bên bảo đảm độc lập thứ ba**.

Snapshot cuối: [round-2 manifest](../../tests/phase-3/snapshots/round-2/manifest.json), 49 file; content SHA-256:

```text
c438e1c23ea70b5ea14e5092841580cb3938a14e49499f870db0eb6aaf9adc2a
```

Model context: `0303a497434fb718`; surface: `Codex desktop delegated local runtime`. Exact model ID không được giao diện trả về, giữ `null / not_available`, không tự đoán. Invocation là nạp snapshot được chỉ định, **không phải kiểm thử automatic discovery hoặc implicit activation**.

[Xem cấu trúc hồ sơ và cách chạy lại validator](../../tests/phase-3/README.md), [evidence index](../../tests/phase-3/evidence-index.json), [reviews](../../tests/phase-3/reviews/).

## Kết quả theo loại

| Loại | Bằng chứng / trạng thái |
|---|---|
| Model behavior | 29/29 biến thể hiện hành đạt review: 23 core-business-logic, 1 backward-compatibility và 5 biến thể cho live lookup / file parity / live handoff |
| Chat / Word / native PDF | Ba forward runs và group comparison đạt trên một SOP tổng hợp có bảng; khác locator theo định dạng, không OCR thêm |
| Live external lookup | U06 đã mở nguồn NIST chính thức; chỉ các phần thực đọc được dùng, không coi catalog quá lớn/không mở được là đã xác minh |
| Live Document-Evidence | U16-V01 có dispatch và specialist trace thực; native text = 0, local parse/render + platform-native vision; không chạy OCR, không suy inference chạy on-device; ô bị che giữ pending human review |
| Tooling | 61/61 kiểm tra công cụ đạt; không phải 61 behavioral cases |
| Canonical structure | 9 nhóm kiểm tra đạt, không lỗi/cảnh báo |
| YAML | 21 file YAML và frontmatter đọc được; description 174 ký tự |
| Legacy registry | 104/104 kiểm tra registry đạt; runner cũ vẫn ghi 0 model executions, 28 selected = not_run |
| ZIP content | P01/P02 đạt: 48/49/49 files theo metadata allowlist, đúng roots, checksum, không symlink/path traversal; hai lượt build byte-identical |
| Release-report review | P03 là kiểm tra riêng của báo cáo này; kết quả cuối được lưu ở evidence index và acceptance-results, không tự chứng nhận trong văn bản được review |

Bằng chứng static: [tooling](../../tests/phase-3/static/tooling-tests.txt), [canonical structure](../../tests/phase-3/static/canonical-structure.json), [YAML](../../tests/phase-3/static/canonical-yaml.json), [registry](../../tests/phase-3/static/legacy-registry.json), [command trace](../../tests/phase-3/static/preflight-command-trace.json).

[Fixture integrity](../../tests/phase-3/static/fixture-integrity.json) kiểm tra đủ 64 file input/QA và toàn bộ inventory giữ nguyên hash. Bộ 29 biến thể là hữu hạn, một lần chạy được review cho mỗi biến thể hiện hành; không phải phép đo xác suất thành công hoặc kiểm thử lặp trên nhiều model. Các review static P01/P02 là self-check của tác giả công cụ, tách khỏi builder nhưng không phải bên thứ ba.

## Ba gói bàn giao

| Gói | Số file | Root trong archive |
|---|---:|---|
| [Claude](../../dist/1.1.0/Thien-Skill-Risk-Process-Control-v1.1.0-Claude.zip) | 48 | `thien-skill-risk-process-control/` |
| [ChatGPT](../../dist/1.1.0/Thien-Skill-Risk-Process-Control-v1.1.0-ChatGPT.zip) | 49 | `thien-skill-risk-process-control/` |
| [Universal](../../dist/1.1.0/Thien-Skill-Risk-Process-Control-v1.1.0-Universal.zip) | 49 | `.agents/skills/thien-skill-risk-process-control/` |

Claude chỉ loại `agents/openai.yaml`; nội dung nghiệp vụ, license và logo cùng canonical. Khác hash toàn ZIP là đúng thiết kế, không phải lệch nội dung. [SHA256SUMS](../../dist/1.1.0/SHA256SUMS), [packaging report](../../dist/1.1.0/packaging-report.json) và [build trace](../../tests/phase-3/static/build-command-trace.json) giữ kết quả thực. `publication: created` của builder nghĩa là tạo thư mục local, không phải phát hành GitHub. ZIP 1.0.0 không bị ghi đè.

Các mẫu kiểm tra không chứng minh mọi end-to-end process/ngành đều được bao phủ đầy đủ. Phạm vi mở của skill là phương pháp discovery và tham chiếu nguồn theo quyền, không phải một catalog đầy đủ đã kết nối sẵn.

## Những phân biệt đã kiểm tra

- Tên/acronym chưa rõ cần hỏi; quy trình ngoài seed không bị ép vào danh mục; một bộ tài liệu có thể nối nhiều E2E.
- SOP khác log được giữ ở observations riêng cùng logical control; sai lệch một giao dịch không thành kết luận OE cả kỳ.
- Controls được so theo objective, coverage, precision, timing, independence và dependency; manual/automated khác hình thức chưa đủ tạo gap.
- Baseline mandatory/advisory, phiên bản, kỳ áp dụng và quyền đọc/AI use/redistribution tách riêng.
- Phương án cải tiến có điều kiện, trade-off và approval; không tự đặt ngân sách, nhân sự, risk score, loss hoặc xác suất.
- U19 giữ một shared control, các observations và 13 RCM rows; [1.112 kiểm tra liên kết/field/null bổ sung](../../tests/phase-3/reviews/support/P1-U19-V01-R2-link-recheck.json) không thay cho review nội dung.
- U22 giữ nguyên dữ liệu 1.0.0 và thêm thông tin chưa biết riêng; [kiểm tra preservation](../../tests/phase-3/reviews/support/P1-U22-V01-R1-preservation-recheck.json) không bảo đảm mọi strict-schema consumer cũ chấp nhận fields mới.

## Bề mặt nền tảng

| Bề mặt | Trạng thái đúng phạm vi |
|---|---|
| Codex delegated local runtime | Có forward runs; không suy thành chứng nhận toàn nền tảng hoặc cài ZIP/discovery thành công |
| Claude Desktop | not_run |
| Claude Web | not_run |
| ChatGPT Desktop | not_run |
| ChatGPT Web | not_run |
| Cài đặt ZIP / tài khoản / connectors | not_run — không thực hiện |

Các profile không có web, bị giới hạn quyền hoặc không có specialist là **điều kiện mô phỏng**, không phải bằng chứng host đó thiếu capability. Dòng Codex chung trong ma trận là nhãn kế hoạch; context thực được ghi bằng surface cụ thể ở trên.

[README](../../README.md), [INSTALL](../../INSTALL.md) và [Platform guidance](PLATFORM-GUIDANCE.md) phân biệt upload Claude, local `.agents/skills`, `.claude/skills` và giới hạn ChatGPT Web. Nguồn chính thức được kiểm tra ngày 28/08/2026; không thay cho cài thử. ChatGPT Web cần đường phân phối plugin riêng theo tài liệu đã đọc; ba ZIP hiện tại không phải plugin và không được gọi là native web importer đã xác minh.

## Lịch sử, giới hạn và thay đổi Phase 3

- Giữ baseline commit `d65fad595e0265dbe665477b6a5747faa5811139`, bộ 104/28 cũ và ZIP 1.0.0. Không cộng chúng vào behavioral passes của 1.1.0.
- Round 1 có bốn raw runs U01/U02/U04/U19, giữ `executed_unreviewed`. Chỉ thay câu evidence-description đã lỗi thời trong registry để tạo round 2; cả bốn được chạy lại trong context mới, không chuyển pass giữa snapshots.
- U01 round 1, U06 và U12 có preparatory filename-only listing vượt thư mục fixture trước khi đọc harness; trace ghi không đọc nội dung fixture khác/rubric/history. Giữ đây là hạn chế protocol, không xóa khỏi lịch sử.
- Traces là ghi chép do executor tạo, không phải full host transcript. Lỗi quote/date/tool command và output bị cắt được giữ kèm cách khôi phục; validator không tự chứng minh danh tính executor, hidden context hoặc độ đúng của reviewer.
- `skill-creator` được dùng để giữ một entrypoint gọn và tài nguyên có định tuyến. Description rút xuống 174 ký tự; version/license-application declarations đồng bộ 1.1.0. Không đổi điều khoản license hoặc logo. Official quick-validator thiếu PyYAML trong môi trường; không cài thêm, dùng kiểm tra canonical và Ruby safe YAML đã ghi kết quả.
- Thêm capture/assemble/evidence validator và builder theo version; test fixtures/raw outputs ở ngoài runtime ZIP. Chưa thêm OCR engine hoặc dependency bắt buộc vào Document-Evidence.
- Pattern scan giới hạn [không thấy tên file khớp các mẫu secret đã liệt kê](../../tests/phase-3/static/bounded-pattern-scan.json); không phải bảo đảm không có mọi loại dữ liệu nhạy cảm hoặc malware.
- Không cài skill, không thay quyền/tài khoản, không commit/push GitHub và không phát hành ra ngoài. Kết quả test không cấp quyền phê duyệt nghiệp vụ, sử dụng license hay publication.

[Work log](WORKLOG.md) ghi các mốc kỹ thuật; báo cáo này không thay raw evidence hoặc phê duyệt của người dùng.
