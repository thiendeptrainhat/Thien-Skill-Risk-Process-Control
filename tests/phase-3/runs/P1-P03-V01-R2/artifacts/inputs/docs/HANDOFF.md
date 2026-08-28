# Handoff — Thien-Skill-Risk-Process-Control 1.1.0

Cập nhật: **28/08/2026**. Đây là hồ sơ bàn giao dự án sau Phase 3, không phải contract giao việc nghiệp vụ cho Document-Evidence.

## Trạng thái bàn giao

Ba phase nâng cấp đã hoàn tất trong phạm vi được người dùng chấp thuận: thiết kế; cập nhật nội dung vận hành; kiểm thử và tạo ba ZIP 1.1.0. Gate tổng hợp tại thời điểm khép Phase 3 là `evidence_complete`; xem [kết quả hiện hành](../tests/phase-3/acceptance-results.json) để xác nhận `current_release_gate` sau các cập nhật tài liệu.

| Hạng mục | Trạng thái và căn cứ |
|---|---|
| Lõi skill | Một canonical skill 1.1.0, 49 files; [SKILL.md](../skills/thien-skill-risk-process-control/SKILL.md) |
| Phạm vi nghiệp vụ | E2E mở; risk; expected/key controls; current controls; gaps; improvement; no-change exposure |
| Model testing | 29/29 biến thể hiện hành đạt review, 95 per-run invariant judgments, trong `Codex desktop delegated local runtime` |
| Công cụ kiểm tra | 61/61 tests của tooling; không phải 61 lần kiểm thử nghiệp vụ |
| File / nguồn ngoài / specialist | Có ba biến thể chat/Word/PDF, một live lookup NIST và một handoff Document-Evidence thực; xem [báo cáo Phase 3](phase-3/REPORT.md) |
| Phân phối | Ba ZIP dùng cùng nội dung nghiệp vụ, checksum và parity đã kiểm tra; chưa cài vào host |
| Claude/ChatGPT native, ZIP discovery/activation | `not_run`; không suy từ kết quả delegated Codex |
| License và thương hiệu | Giữ điều khoản license, notices và logo; khai báo phạm vi phiên bản là 1.1.0 |

Các hồ sơ [Phase 1](phase-1/README.md) và [Phase 2](phase-2/README.md) ghi trạng thái tại thời điểm của từng phase, không phải trạng thái hiện tại. Bộ 104 registry / 28 provisional summaries cũ, ZIP 1.0.0 và bốn runs round-1 `executed_unreviewed` được giữ nguyên, không cộng vào 29 passes của bản mới.

## Nội dung cần tiếp nhận

| Tài nguyên | Mục đích |
|---|---|
| [README](../README.md) | Vai trò, lợi ích, hướng dẫn sử dụng ở trước; cài đặt ở dưới |
| [INSTALL](../INSTALL.md) | Thao tác và giới hạn cài theo từng host |
| [Release manifest](../RELEASE-MANIFEST.yaml) | Version, ba tên ZIP, archive roots và checksum |
| [Thư mục ZIP 1.1.0](../dist/1.1.0/) | Claude, ChatGPT, Universal; không dùng ZIP toàn repository để upload Claude |
| [SHA256SUMS](../dist/1.1.0/SHA256SUMS) / [packaging report](../dist/1.1.0/packaging-report.json) | Kiểm tra bytes và khác biệt wrapper/metadata được phép |
| [Bằng chứng Phase 3](../tests/phase-3/README.md) | Fixtures, snapshots, raw outputs, traces, reviews và cách chạy validator |
| [Platform guidance](phase-3/PLATFORM-GUIDANCE.md) | Nguồn chính thức đã đọc và giới hạn suy luận về cài đặt |

Canonical content SHA-256: `c438e1c23ea70b5ea14e5092841580cb3938a14e49499f870db0eb6aaf9adc2a`. Snapshot dùng cho 29 runs: [round-2 manifest](../tests/phase-3/snapshots/round-2/manifest.json); context ID `0303a497434fb718`. Exact model ID không được giao diện cung cấp, giữ `null / not_available`.

## Cập nhật tài liệu và giữ bằng chứng

Yêu cầu tiếp nối của người dùng: cập nhật handoff, đưa vai trò/lợi ích/cách dùng lên đầu README, đưa cài đặt xuống dưới, sau đó commit và push. Cập nhật này không thay runtime instructions, templates nghiệp vụ, license hoặc ba ZIP; không phát sinh một bộ model tests mới.

README mà P03-R1 đã đọc được lưu **byte-identical** cùng result/index/run-record cũ tại [documentation snapshot](../tests/phase-3/documentation-snapshots/pre-handoff-update-2026-08-28/manifest.json). Chỉ đổi nơi lưu con trỏ input của receipt cũ; raw output, trace và review cũ không bị viết lại.

README mới và handoff cần lượt P03 tài liệu riêng trước khi bàn giao. Kết quả chính thức nằm ở evidence index và acceptance-results sau khi gắn review; không tự gán pass từ việc file đã tồn tại. Retest tài liệu không được cộng thành model behavioral passes.

## GitHub và ranh giới quyền

Repository đích: [thiendeptrainhat/Thien-Skill-Risk-Process-Control](https://github.com/thiendeptrainhat/Thien-Skill-Risk-Process-Control), private; nhánh `main`, remote `origin`. Người dùng đã yêu cầu riêng việc commit/push cho lần bàn giao này, sau khi Phase 3 khép mà chưa thực hiện Git publication.

Trạng thái commit/push thực tế phải đối chiếu Git history và remote; gate kiểm thử không phải quyền publication hoặc bằng chứng đã push. Không hard-code SHA của chính commit chứa tài liệu này. GitHub commit/push không đồng nghĩa đã tạo GitHub Release/tag hoặc cài skill vào Claude/ChatGPT/Codex.

Giữ repository private khi lưu raw evidence có metadata đường dẫn local. Không đưa `.DS_Store`, credentials hoặc file ngoài phạm vi vào commit. Việc cài đặt, đổi quyền/tài khoản, tạo connector/plugin hoặc live-platform acceptance chưa được thực hiện trong lần bàn giao này.

## Kiểm tra khi tiếp tục công việc

Từ repository root:

```sh
python3 -B scripts/assemble_phase3_evidence.py --write
python3 -B scripts/run_tests.py --phase3 --json
python3 -B -m unittest discover -s tests/phase-3/tooling -v
python3 -B tests/phase-3/tooling/inspect_release.py --repo-root .
```

Đọc `current_release_gate` và claims theo đúng context/snapshot; exit code 0 chỉ xác nhận integrity. Không dùng `--write-results` với Phase 3 và không ghi đè lịch sử 104/28. Không sửa fixture/snapshot/raw output để làm test đạt; nếu đổi lõi skill, cần snapshot và phạm vi retest phù hợp trước khi đóng ZIP mới.

## Giới hạn cần giữ và việc chỉ làm khi được yêu cầu

- Phạm vi E2E mở là phương pháp discovery, không phải bảo đảm một catalog đầy đủ cho mọi ngành. Tra cứu nguồn theo quyền và applicability của từng engagement; catalog pointers không phải các connector đã cài.
- Document-Evidence là tùy chọn. Handoff đã thử dùng local parse/render và platform-native vision trên một scan tổng hợp; không chạy OCR engine và ô bị che vẫn pending human review.
- Sáu profile kiểm thử có điều kiện capability mô phỏng. Cả bộ dùng dữ liệu tổng hợp hữu hạn; không suy thành tỷ lệ chính xác trên mọi tài liệu/model hoặc bảo đảm độc lập thứ ba.
- Giữ `release_candidate` và `runtime_verification.verified: false` của metadata: gate nghiệp vụ/packaging không chứng minh native discovery hay phê duyệt nghiệp vụ.
- Nếu cần cài thử trên Claude Desktop/Web, ChatGPT Desktop/Web hoặc triển khai web qua plugin, phải thống nhất phạm vi, tài khoản/quyền và tiêu chí riêng. Không tự tạo thêm “Phase 4”, plugin hay dependency OCR.
- Policy/SOP/RCM/target-state do skill hỗ trợ vẫn là draft cho đến khi người có thẩm quyền phê duyệt.
