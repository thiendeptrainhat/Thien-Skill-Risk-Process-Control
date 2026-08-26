<p align="center">
  <img src="skills/thien-skill-risk-process-control/assets/logo-1100.png" alt="Logo TDTN" width="220">
</p>

# Thien-Skill-Risk-Process-Control

Skill chuyên sâu về **quy trình, rủi ro và kiểm soát**, giúp chuyển tài liệu, phỏng vấn, bằng chứng và dữ liệu vận hành thành một chuỗi phân tích có thể truy nguyên:

`Business Objective → End-to-End Process → Process → Risk → Control Objective → Control → Evidence → Metric/Test Attribute → Gap → Recommendation → Action`

Skill hỗ trợ Claude, ChatGPT Desktop và Codex theo từng gói phân phối. Nội dung nghiệp vụ của các gói là như nhau; chỉ cấu trúc cài đặt và metadata nền tảng khác nhau.

> [!IMPORTANT]
> GitHub chỉ lưu trữ mã nguồn và các gói ZIP. Việc clone hoặc tải repository **không tự kích hoạt skill**. Skill chỉ hoạt động sau khi được upload, import hoặc giải nén vào đúng thư mục mà Claude, ChatGPT Desktop hoặc Codex nhận diện.

## Thông tin phát hành

| Thuộc tính | Giá trị |
|---|---|
| Tên hiển thị | `Thien-Skill-Risk-Process-Control` |
| Skill ID | `thien-skill-risk-process-control` |
| Phiên bản | `1.0.0` |
| Repository | Private |
| Ngôn ngữ trả lời | Theo ngôn ngữ người dùng |
| License | Tran Ngoc Thien's Skills Commercial Source-Available License 2.0 |
| Trạng thái package | 3/3 archive integrity pass |
| Kiểm thử deterministic | 104/104 case pass |

## Chọn đúng gói cài đặt

| Gói | Bề mặt phù hợp | Cách dùng chính |
|---|---|---|
| [Claude ZIP](dist/Thien-Skill-Risk-Process-Control-v1.0.0-Claude.zip) | Claude có mục `Customize > Skills`; Claude Code | Upload nguyên ZIP hoặc giải nén vào `.claude/skills/` |
| [ChatGPT ZIP](dist/Thien-Skill-Risk-Process-Control-v1.0.0-ChatGPT.zip) | ChatGPT Desktop có hỗ trợ standalone skills; Codex user scope | Import qua giao diện Skills nếu có, hoặc giải nén vào `~/.agents/skills/` |
| [Universal `.agents` ZIP](dist/Thien-Skill-Risk-Process-Control-v1.0.0-Universal.zip) | Codex Desktop, Codex CLI, Codex IDE và repository-scoped skills | Giải nén tại project root để tạo `.agents/skills/<skill-id>/` |

### Phạm vi hỗ trợ cần lưu ý

- **ChatGPT Desktop:** OpenAI hỗ trợ standalone skills. Mở mục **Skills** trong sidebar để xem các skill có sẵn. Tùy tài khoản/workspace, thao tác import hoặc upload có thể khác nhau.
- **Codex:** đọc skill từ `.agents/skills/` ở cấp project hoặc user và tự nhận thay đổi; nếu skill chưa xuất hiện, khởi động lại Codex.
- **ChatGPT Web:** standalone skill không phải hình thức phân phối đầy đủ cho ChatGPT Web. Muốn dùng trong Chat/Work trên web, skill cần được đóng gói và phát hành dưới dạng **plugin**. Release `1.0.0` hiện tại chưa phải plugin.
- **Claude:** có thể upload custom skill ZIP từ giao diện Skills; Claude Code dùng `.claude/skills/`.

## Cài đặt nhanh từ GitHub

### 1. Tải repository hoặc một file ZIP

Vì repository là private, người tải phải có quyền truy cập GitHub phù hợp.

Clone bằng GitHub CLI:

```bash
gh repo clone thiendeptrainhat/Thien-Skill-Risk-Process-Control
cd Thien-Skill-Risk-Process-Control
```

Hoặc mở thư mục [`dist/`](dist/) trên GitHub và tải đúng ZIP trong bảng lựa chọn ở trên.

### 2. Kiểm tra tính toàn vẹn

Trước khi cài, kiểm tra SHA-256 của ba gói:

```bash
cd dist
shasum -a 256 -c SHA256SUMS
```

Kết quả mong đợi là `OK` cho cả ba ZIP. Hash chuẩn cũng được ghi tại [RELEASE-MANIFEST.yaml](RELEASE-MANIFEST.yaml).

## Hướng dẫn theo từng nền tảng

### A. Claude trên web hoặc ứng dụng có Custom Skills

1. Tải [Claude ZIP](dist/Thien-Skill-Risk-Process-Control-v1.0.0-Claude.zip).
2. Không giải nén file.
3. Mở **Customize > Skills**.
4. Chọn **+ > Create skill > Upload a skill**.
5. Upload file Claude ZIP.
6. Bật skill trong danh sách Skills.
7. Kiểm tra bằng một prompt phù hợp, ví dụ:

```text
Hãy dùng Thien-Skill-Risk-Process-Control để phân tích SOP đính kèm,
tách As-Documented và As-Performed, sau đó lập risk-control gap register.
```

Custom skill upload lên Claude mặc định gắn với tài khoản cá nhân. Việc chia sẻ trong tổ chức phụ thuộc gói Team/Enterprise và cấu hình quản trị.

### B. Claude Code — cài cho một project

Từ thư mục gốc của project cần sử dụng skill:

```bash
mkdir -p .claude/skills
unzip /path/to/Thien-Skill-Risk-Process-Control-v1.0.0-Claude.zip -d .claude/skills
```

Cấu trúc sau cài đặt:

```text
.claude/
└── skills/
    └── thien-skill-risk-process-control/
        ├── SKILL.md
        ├── references/
        ├── templates/
        ├── examples/
        ├── assets/
        └── scripts/
```

Gọi trực tiếp bằng:

```text
/thien-skill-risk-process-control
```

Claude Code cũng có thể tự kích hoạt skill khi yêu cầu phù hợp với phần `description` trong `SKILL.md`.

### C. Claude Code — cài cho người dùng

Để skill dùng được trong mọi project của tài khoản trên máy:

```bash
mkdir -p ~/.claude/skills
unzip /path/to/Thien-Skill-Risk-Process-Control-v1.0.0-Claude.zip -d ~/.claude/skills
```

Nếu thư mục `.claude/skills/` chưa tồn tại khi phiên Claude Code bắt đầu, hãy khởi động lại Claude Code sau khi cài.

### D. Codex Desktop, Codex CLI hoặc Codex IDE — project scope

Tải [Universal ZIP](dist/Thien-Skill-Risk-Process-Control-v1.0.0-Universal.zip), kiểm tra nội dung trước khi giải nén:

```bash
unzip -l Thien-Skill-Risk-Process-Control-v1.0.0-Universal.zip
```

Sau đó giải nén tại project root:

```bash
unzip Thien-Skill-Risk-Process-Control-v1.0.0-Universal.zip -d /path/to/project
```

Kết quả phải có:

```text
/path/to/project/.agents/skills/thien-skill-risk-process-control/SKILL.md
```

Không giải nén chồng lên một phiên bản cũ chưa sao lưu hoặc chưa đối chiếu thay đổi.

### E. Codex — user scope

Tải [ChatGPT ZIP](dist/Thien-Skill-Risk-Process-Control-v1.0.0-ChatGPT.zip), sau đó:

```bash
mkdir -p ~/.agents/skills
unzip Thien-Skill-Risk-Process-Control-v1.0.0-ChatGPT.zip -d ~/.agents/skills
```

Kiểm tra:

```text
~/.agents/skills/thien-skill-risk-process-control/SKILL.md
```

Trong Codex, dùng `/skills` để kiểm tra danh sách hoặc nhập:

```text
$thien-skill-risk-process-control
```

### F. ChatGPT Desktop

1. Tải [ChatGPT ZIP](dist/Thien-Skill-Risk-Process-Control-v1.0.0-ChatGPT.zip).
2. Mở **Skills** trong sidebar của ChatGPT Desktop.
3. Nếu tài khoản/workspace hiển thị chức năng import hoặc upload standalone skill, chọn file ChatGPT ZIP.
4. Nếu không có chức năng đó nhưng đang làm việc trong Codex, dùng cách cài `.agents/skills/` ở mục D hoặc E.
5. Sau khi skill xuất hiện, chọn bằng `@` hoặc mô tả trực tiếp yêu cầu để ChatGPT tự kích hoạt.

### G. ChatGPT Web

Release này **không thể chỉ được tải từ GitHub rồi tự xuất hiện trong ChatGPT Web**. Theo mô hình phân phối hiện tại của OpenAI:

- standalone skills phù hợp với ChatGPT Desktop, Codex CLI và IDE extension;
- ChatGPT Web sử dụng skill được phân phối thông qua plugin;
- repository này chưa chứa package plugin và chưa được submit/publish vào plugin directory.

Nếu cần hỗ trợ ChatGPT Web, bước tiếp theo là tạo plugin adapter từ canonical skill, kiểm thử trên Chat/Work và thực hiện quy trình publish riêng.

## Xác nhận skill đã hoạt động

Skill có thể được kích hoạt theo hai cách:

1. **Explicit invocation:** chọn hoặc gọi trực tiếp skill.
2. **Implicit invocation:** nền tảng nhận thấy yêu cầu phù hợp với mô tả của skill và tự nạp hướng dẫn.

Prompt kiểm tra tối thiểu:

```text
Hãy dùng Thien-Skill-Risk-Process-Control.
Cho biết bạn cần những đầu vào nào để lập current-state process map,
risk register và control register mà không tự suy đoán dữ liệu còn thiếu.
```

Dấu hiệu hoạt động đúng:

- hỏi hoặc ghi rõ các dữ liệu trọng yếu còn thiếu;
- tách `As-Documented`, `As-Designed`, `As-Performed` và `Target-State`;
- không tự đặt risk score, threshold, sample size hoặc system configuration;
- giữ liên kết objective → process → risk → control → evidence → action;
- nêu confidence, source, assumptions, unresolved items và approval gate.

## Lợi ích khi sử dụng

### 1. Một chuỗi truy nguyên thống nhất

Thay vì tạo riêng process map, risk register, control register và action plan không liên kết, skill duy trì quan hệ bằng ID ổn định. Điều này giúp:

- truy ngược một recommendation về objective, risk và evidence;
- phát hiện orphan control, orphan risk hoặc action không có owner;
- tạo nhiều RCM view từ cùng nguồn dữ liệu;
- giảm mâu thuẫn giữa workflow, RACI, RCM và audit handoff.

### 2. Phân biệt tài liệu với vận hành thực tế

Bốn lớp phân tích giúp tránh kết luận sai rằng quy trình đang vận hành đúng chỉ vì SOP mô tả như vậy:

- `As-Documented`: tài liệu đang quy định gì;
- `As-Designed`: thiết kế logic tổng thể là gì;
- `As-Performed`: bằng chứng cho thấy thực tế diễn ra thế nào;
- `Target-State`: thiết kế tương lai được đề xuất.

### 3. Risk-based nhưng không máy móc

Skill bắt đầu từ business objective và end-to-end outcome, sau đó mới xác định risk và control. Nó không mặc định mọi control đều là key control, mọi role overlap đều là actual SoD conflict hoặc mọi unique owner đều là SPOF.

### 4. Cân bằng kiểm soát và hiệu quả

Khi có trade-off đáng kể, skill có thể so sánh các lựa chọn từ minimum-compliant đến balanced và leading/automation-first theo:

- lợi ích và residual exposure;
- chi phí và độ phức tạp;
- phụ thuộc công nghệ, dữ liệu và con người;
- thời gian triển khai;
- nhu cầu governance và approval.

### 5. Giảm hallucination và overclaim

Skill buộc phân biệt fact, evidence-backed conclusion, inference, assumption, proposal và unresolved item. Khi chưa đủ bằng chứng, nó dùng các trạng thái như `Not provided`, `To be validated` hoặc `Unresolved` thay vì tự điền dữ liệu có vẻ hợp lý.

### 6. Sẵn sàng cho nhiều deliverable

Nguồn dữ liệu có cấu trúc có thể được chuyển tiếp sang Word, Excel, PowerPoint hoặc dashboard mà vẫn giữ source reference, analysis layer, confidence và review status.

## Tính năng chính

| Nhóm tính năng | Khả năng |
|---|---|
| Document analysis | Phân tích policy, standard, SOP, procedure, work instruction, approval matrix, form và mâu thuẫn tài liệu |
| Current-state discovery | Xác định trigger, boundary, actor, decision, exception, handoff, system, data và evidence |
| Process architecture | Xây dựng value chain, E2E process và hierarchy L0–L5 theo evidence có sẵn |
| Risk and control | Viết risk theo Cause → Event → Impact → Objective; xác định control objective, control design và testability |
| Key controls | Đánh giá key-control rationale, alternatives, dependency và consequence of failure |
| RCM | Quản lý liên kết many-to-many risk–control–evidence–test attribute và tạo nhiều view |
| SoD | Phân tích process-role, system-access và actual-user; tách potential, actual và exercised conflict |
| SPOF/dependency | Phân tích people, system, supplier, site, data, approval, knowledge, backup, capacity và common-mode failure |
| Target-state design | Thiết kế workflow, roles, controls, systems, metrics, governance và implementation roadmap |
| Metrics | Phân biệt KPI, KRI và KCI; không tự đặt target hoặc threshold |
| Workflow/diagram | Tạo step register, swimlane, Mermaid và BPMN conceptual; không tuyên bố đã render nếu chưa kiểm tra |
| Audit support | Hỗ trợ walkthrough, evidence request, draft audit-program skeleton và test attributes; không phát hành audit opinion |
| Assessment | Đánh giá process maturity, documentation quality, control design và compliance mapping theo methodology được duyệt |
| Training | Tạo workshop, case study, simulation, RCM/SoD exercise và scoring rubric |
| Standards mapping | Phân biệt nghĩa vụ bắt buộc, hợp đồng, adopted standard, framework và advisory best practice |

## 11 chế độ vận hành

1. `document-analysis`
2. `current-state-discovery`
3. `risk-control-analysis`
4. `target-state-design`
5. `rcm`
6. `sod`
7. `spof-dependency`
8. `audit-support`
9. `advisory`
10. `assessment`
11. `training`

## Nguồn lực đi kèm

- Workflow chuẩn 14 bước từ intake đến remediation handoff.
- Profile discovery cho 94 end-to-end process families.
- 14 reference module theo progressive disclosure.
- 18 YAML template dùng chung common data model.
- Example catalog cho P2P, O2C, R2R, access lifecycle, CAPA và các process family khác.
- Package validator dùng Python standard library, không yêu cầu network.
- Bộ 104 deterministic acceptance cases và 28 behavioral scenarios được chọn theo rủi ro.

## Ví dụ yêu cầu

```text
Phân tích policy và SOP đính kèm, lập conflict log và chỉ ra các nội dung lỗi thời.
```

```text
Lập current-state P2P từ tài liệu và walkthrough notes; tách rõ As-Documented và As-Performed.
```

```text
Tạo risk register, control objective register và RCM cho quy trình Order-to-Cash.
```

```text
Phân tích SoD ở ba lớp process role, system access và actual user; không kết luận actual conflict nếu thiếu dữ liệu user assignment.
```

```text
Đánh giá dependency và SPOF của quy trình payroll, bao gồm backup, capacity, lead time và common-mode failure.
```

```text
Đề xuất target-state options cho quy trình vendor onboarding, so sánh benefit, risk, cost, complexity và dependency.
```

## Guardrails và giới hạn

Skill không:

- tự phát hành legal opinion, compliance certification hoặc audit opinion;
- tự kết luận operating effectiveness khi thiếu methodology, population, testing và evidence;
- sửa trực tiếp source document, ERP, access hoặc production workflow;
- tự đặt risk rating, materiality, threshold, sample size hoặc control frequency;
- coi best practice là nghĩa vụ pháp lý khi chưa xác minh applicability;
- thay thế phê duyệt của process owner, risk owner, Internal Audit, Legal, Compliance, IT Security hoặc authority phù hợp.

Mọi policy, SOP, RCM và target-state design do skill tạo phải được xem là **draft** cho đến khi người có thẩm quyền phê duyệt.

## Kiểm thử và mức độ tin cậy

| Kiểm thử | Trạng thái |
|---|---|
| Package structure, metadata, links, assets và license parity | Pass |
| Deterministic case registry | 104/104 pass |
| Archive integrity | 3/3 pass |
| Behavioral execution summaries trên Codex | 28 case đã được chạy nhưng evidence không đầy đủ; không tính là verified pass |
| Claude live-surface behavioral testing | Chưa chạy |
| ChatGPT upload-surface behavioral testing | Chưa chạy |

Xem [acceptance report](tests/acceptance-report.md), [behavioral report](tests/behavioral-report.md) và [release manifest](RELEASE-MANIFEST.yaml) để biết phạm vi xác minh chính xác.

## Cập nhật phiên bản đã cài

1. Đồng bộ repository bằng `git pull --ff-only` hoặc tải ZIP mới.
2. Kiểm tra `RELEASE-MANIFEST.yaml`, version và SHA-256.
3. Sao lưu phiên bản đang cài nếu có tùy chỉnh local.
4. Cài lại đúng package theo nền tảng.
5. Chạy prompt xác nhận kích hoạt.

GitHub không tự đồng bộ bản đã upload lên Claude hoặc ChatGPT. Mỗi phiên bản mới phải được import/upload lại theo cơ chế của nền tảng.

## License và quyền sử dụng

Đọc đầy đủ:

- [LICENSE](LICENSE)
- [LICENSE-APPLICATION.md](LICENSE-APPLICATION.md)
- [NOTICE](NOTICE)
- [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)

Việc có quyền truy cập repository, tải ZIP hoặc cài đặt thành công **không tự động cấp quyền sử dụng, sửa đổi hoặc phân phối**. Bản tiếng Việt của license được ưu tiên khi có khác biệt hoặc mâu thuẫn; pháp luật Việt Nam và tòa án có thẩm quyền tại Việt Nam được áp dụng theo nội dung license.

## Tài liệu nền tảng chính thức

- [OpenAI — Build skills](https://developers.openai.com/codex/skills)
- [Claude — Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
- [Claude Code — Extend Claude with skills](https://code.claude.com/docs/en/skills)

## Tài liệu trong repository

- [Hướng dẫn cài đặt ngắn](INSTALL.md)
- [Canonical SKILL.md](skills/thien-skill-risk-process-control/SKILL.md)
- [Requirement coverage matrix](skills/thien-skill-risk-process-control/references/requirement-coverage-matrix.md)
- [Common data model và QA](skills/thien-skill-risk-process-control/references/data-model-qa-execution.md)
- [Source provenance](skills/thien-skill-risk-process-control/references/source-skill-inventory.md)
