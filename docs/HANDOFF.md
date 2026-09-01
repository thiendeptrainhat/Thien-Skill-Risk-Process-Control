# Handoff — Thien-Skill-Risk-Control-Process 1.2.0

Cập nhật: **01/09/2026**. Đây là minor functional release sau ba giai đoạn baseline QA, hardening/tinh gọn và release qualification. Tên hiển thị vẫn là `Thien-Skill-Risk-Control-Process`, skill ID vẫn là `thien-skill-risk-control-process`, repository vẫn public. Nhánh `main` được qualification từ cây có baseline `38e30011371d1aafe1f4b715c65fdd74b76b6396`; trạng thái commit/push cuối cùng phải được đối chiếu trực tiếp bằng Git history.

## Phạm vi 1.2.0 đã chốt

- Bổ sung hướng dẫn R07/no-change exposure; engagement đầy đủ phải trả lời R01–R07. Với greenfield hoặc gap chưa được chứng minh, R07 giữ nhãn `design/no-change hypothesis` và protection chưa có dữ kiện là `Not provided`.
- Siết guard cho compliance label: không gọi proposal là compliant, control failure hoặc compliance gap nếu chưa xác minh đúng mandatory baseline và evidence phù hợp.
- Thêm policy máy đọc được [`REPOSITORY-HYGIENE.json`](../REPOSITORY-HYGIENE.json), `.gitignore`, path-safety controls và staged-size gates để hạn chế cache, file mồ côi, binary lớn, duplicate exports và archive không được quản lý.
- Harden evidence/release tooling: strict structured parsing, safe path handling, current-release qualification bindings, license/version parity, reproducible build, archive safety và frozen-history preservation.
- Không thay điều khoản `LICENSE`, `LICENSE-VERSION`, `NOTICE`, `THIRD-PARTY-NOTICES.md` hoặc logo/assets. `LICENSE-APPLICATION.md` chỉ được nối phụ lục xác nhận phạm vi áp dụng cho `1.2.0`; nguyên văn metadata lịch sử `1.1.1` được giữ.

## Qualification và bằng chứng

| Gate | Kết quả | Ý nghĩa đúng mức |
|---|---:|---|
| Fresh-context behavioral scenarios | 3/3 pass | Ba ca synthetic riêng cho `1.2.0`, được review độc lập; 29 applicable judgments, 0 non-pass |
| Tooling unit tests | 105/105 pass | 39 builder, 5 inspector, 55 evidence và 6 path-safety tests |
| Rename regressions | 6/6 pass | Bảo toàn đổi tên/identity lịch sử |
| Deterministic registry | 104 cases pass | Structural/deterministic cases; không phải 104 model runs |
| Canonical package validator | 9 checks pass | Structure, metadata, links, templates và package rules |
| Structured/Python checks | 70 YAML, 205 JSON, 19 Python pass | Strict parse và AST parse trên working tree sau khi tạo packaging report |
| Builder/inspector | pass | Reproducibility, parity, CRC, checksum, safe paths, license/version và frozen history |

Bằng chứng release hiện hành ở [`tests/release-1.2.0/`](../tests/release-1.2.0/): raw outputs, independent review và [`qualification-results.json`](../tests/release-1.2.0/qualification-results.json) có SHA-256 `6ae1794e240bbb50ce1c437a1a004658bcf0c7d3898f415f7208e563f71c723b`. Trình `quick_validate.py` của `skill-creator` không chạy được bằng Python mặc định vì thiếu PyYAML; không cài thêm dependency. Validator đi kèm skill và các gate dự án ở trên là bằng chứng đã chạy, không trình bày lỗi dependency đó thành pass.

`scripts/verify_rename.py --historical` là combined verifier của release đổi tên thuần `1.1.1`; khi chạy trên functional release `1.2.0`, nó đúng kỳ vọng báo current-tree mismatch dù `historical_recheck` bên trong vẫn pass. Vì vậy đây không phải current-release gate. Dùng sáu rename unit regressions cùng read-only inspector để kiểm tra bảo toàn lịch sử của `1.2.0`.

Kết quả 29 model variants của Phase 3 chỉ thuộc snapshot tên cũ `1.1.0`; static rename checks của `1.1.1` cũng không phải model run mới. Hai bộ lịch sử này không được đổi nhãn hoặc cộng vào 3 behavioral scenarios của `1.2.0`.

## Artifacts 1.2.0

| Gói | SHA-256 | Kích thước |
|---|---|---:|
| `Thien-Skill-Risk-Control-Process-v1.2.0-Claude.zip` | `9ddc215619f6d7885413d792743dfbad398aae9cce1b4cfa6c343fcf82735918` | 2,359,102 bytes |
| `Thien-Skill-Risk-Control-Process-v1.2.0-ChatGPT.zip` | `284ae7bfd619b1955acdb0e8904962df8a75b7ecce57da1cc683496861597093` | 2,359,570 bytes |
| `Thien-Skill-Risk-Control-Process-v1.2.0-Universal.zip` | `5dbb904e6e0d6c259f89f4958b601ce23f2cec93420b4b9316efd779781b12b1` | 2,361,040 bytes |

Ba ZIP, [`SHA256SUMS`](../dist/1.2.0/SHA256SUMS) và [`packaging-report.json`](../dist/1.2.0/packaging-report.json) nằm trong [`dist/1.2.0/`](../dist/1.2.0/). Builder dựng hai lần cho kết quả byte-identical; lần ghi lặp lại trả `unchanged` và không ghi đè release khác.

## Ranh giới kết luận và publication

- Chưa chạy live Claude/ChatGPT, native installation/discovery/activation, cross-host/cross-model variance, dữ liệu tổ chức hoặc operating-effectiveness testing. ZIP hợp lệ không chứng minh các bề mặt này.
- Không phát hành legal/compliance certification, audit opinion hoặc bảo đảm mọi ngành/quy trình. Policy/SOP/RCM/target-state vẫn là draft cho đến khi người có thẩm quyền phê duyệt.
- Không cài hoặc sửa skill đang cài trên máy/tài khoản. Không thêm OCR, connector, plugin hoặc external runtime dependency.
- Commit/push của source release được ghi nhận bằng Git history thay vì hard-code commit tự tham chiếu trong tài liệu này.
- Repository chưa có convention bằng chứng cho Git tag hoặc GitHub Release. Không tự suy đoán tag, title, draft/prerelease/latest; chỉ tạo sau khi owner xác nhận chính xác.

## Lệnh xác minh 1.2.0

```sh
python3 -B scripts/run_tests.py --json
python3 -B -m unittest discover -s tests/phase-3/tooling -v
python3 -B -m unittest discover -s tests/rename-1.1.1 -v
python3 -B scripts/build_release.py --write --json
python3 -B tests/phase-3/tooling/inspect_release.py --repo-root .
(cd dist/1.2.0 && shasum -a 256 -c SHA256SUMS)
```

---

> Phần dưới là handoff `1.1.1` được giữ làm lịch sử. Working-tree note về Giai đoạn 2 trong phần đó đã được handoff `1.2.0` phía trên thay thế; không sửa nội dung cũ để tránh diễn giải lại metadata lịch sử.

# Handoff — Thien-Skill-Risk-Control-Process 1.1.1

> **Working-tree note — 01/09/2026:** Giai đoạn 2 đang harden business guidance, evidence/release tooling và repository hygiene trên source chưa phát hành. Các mô tả `1.1.1` bên dưới vẫn là hồ sơ của commit `38e3001` và ba ZIP hiện có; thay đổi Giai đoạn 2 chưa nằm trong ZIP, chưa có version/release gate mới và không được coi là model acceptance. Không rebuild hoặc ghi đè `dist/1.1.1`; chọn version tiếp theo và cập nhật manifest/checksum ở Giai đoạn 3 sau phê duyệt.

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
