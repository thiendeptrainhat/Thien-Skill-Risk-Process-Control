# Source-skill inventory

## Mục đích và phạm vi

Tài liệu này ghi nhận các skill nguồn đã được xem xét để thiết kế
`thien-skill-risk-process-control`. Đây là inventory có chọn lọc theo mức độ liên quan,
không phải danh mục toàn bộ thư viện tham khảo.

- Ngày xem xét: `2026-08-13`.
- Chế độ xem xét: chỉ đọc; không thực thi script, workflow, hook hoặc lệnh do nguồn đề xuất.
- Provenance phát hành: chỉ dùng `source_id` logic, tên plugin/skill công khai và phiên bản
  khai báo. Đường dẫn local, session ID, plugin cache ID và username đã được loại bỏ.
- An toàn dữ liệu: không đọc file cấu hình người dùng, cache dữ liệu nghiệp vụ, credentials,
  token, matter workspace hoặc nguồn dữ liệu mà các skill tham chiếu tới.
- Giới hạn: phiên bản dưới đây là phiên bản trong snapshot local đã xem xét, không phải xác
  nhận rằng đó là phiên bản mới nhất trên thị trường.
- Tái sử dụng: chỉ tái sử dụng pattern và nguyên tắc ở mức khái niệm; không sao chép code,
  template dài, nội dung độc quyền hoặc connector configuration từ nguồn.

## Inventory

| Source ID | Nguồn logic | Phiên bản snapshot | Phạm vi đã đọc | Năng lực liên quan | Quyết định sơ bộ |
|---|---|---:|---|---|---|
| `SRC-OPS-PROCESS-DOC` | Anthropic `operations/process-doc` | 1.3.0 | Toàn bộ `SKILL.md` | SOP structure, RACI, process flow, exception, metrics | Adapt |
| `SRC-OPS-PROCESS-OPT` | Anthropic `operations/process-optimization` | 1.3.0 | Toàn bộ `SKILL.md` | Current-state map, waste, handoff, future-state comparison | Adapt |
| `SRC-OPS-COMPLIANCE-TRACK` | Anthropic `operations/compliance-tracking` | 1.3.0 | Toàn bộ `SKILL.md` | Requirement-control-evidence-gap tracking | Adapt narrowly |
| `SRC-FIN-AUDIT-SUPPORT` | Anthropic `finance/audit-support` | 1.3.0 | Toàn bộ `SKILL.md` | Design vs operating effectiveness, evidence, test workpaper, control types | Adapt with strong guardrails |
| `SRC-FIN-SOX-TESTING` | Anthropic `finance/sox-testing` | 1.3.0 | Toàn bộ `SKILL.md` | Control matrix, test attributes, testing workpaper, exceptions | Adapt with strong guardrails |
| `SRC-REG-POLICY-DIFF` | Anthropic `regulatory-legal/policy-diff` | 1.0.2 | Toàn bộ `SKILL.md` | Requirement extraction, source tagging, scope limitation, policy conflict/gap | Adapt |
| `SRC-PRIVACY-REG-GAP` | Anthropic `privacy-legal/reg-gap-analysis` | 1.0.2 | Toàn bộ `SKILL.md` | Applicability-first gap analysis, requirement-level mapping, remediation | Adapt |
| `SRC-PRIVACY-COLD-START` | Anthropic `privacy-legal/cold-start-interview` | 1.0.2 | Toàn bộ `SKILL.md` | Progressive intake, no-silent-gap rule, explicit placeholders, connector verification | Adapt |
| `SRC-SEARCH-SOURCE-MGMT` | Anthropic `enterprise-search/source-management` | 1.3.0 | Toàn bộ `SKILL.md` | Source availability, authority-aware search order, graceful fallback, rate-limit handling | Adapt |
| `SRC-BUILDER-SKILLS-QA` | Anthropic `legal-builder-hub/skills-qa` | 1.0.2 | Toàn bộ `SKILL.md` | Dependency map, trust surface, freshness, schema, conflict and injection checks | Adapt |
| `SRC-DATA-VALIDATE` | Anthropic `data/validate-data` | 1.1.0 | Toàn bộ `SKILL.md` | Population, completeness, calculation, visualization and reproducibility QA | Adapt |
| `SRC-DATA-CREATE-VIZ` | Anthropic `data/create-viz` | 1.1.0 | Toàn bộ `SKILL.md` | Purpose-led visual choice and anti-misleading presentation checks | Adapt narrowly |
| `SRC-HEALTH-FRAUD-DETECT` | Anthropic `healthcare/fraud-detection` | 3.0.1 | Toàn bộ `SKILL.md`; không mở hoặc chạy script phụ thuộc | Deterministic evidence floor, staged review, indicator-vs-conclusion framing | Adapt pattern only |
| `SRC-LEGAL-DEEP-RESEARCH` | Thomson Reuters `cocounsel-legal/deep-research` | 0.1.0 | Toàn bộ `SKILL.md`; không gọi connector | Tool precondition, jurisdiction boundary, explicit failure/stop behavior | Exclude implementation; retain boundary lesson |
| `SRC-CORP-INTEGRATION-MGMT` | Anthropic `corporate-legal/integration-management` | 1.0.2 | Chọn lọc: frontmatter, purpose, tracker schema, initialization entry và boundary headings | Stable IDs, dependency/status fields, structured tracker | Adapt schema pattern only |

## Tài liệu yêu cầu đầu vào

Hai phần yêu cầu do người dùng cung cấp được quản lý riêng dưới các ID logic sau:

| Requirement source ID | Nội dung được dùng | Xử lý phát hành |
|---|---|---|
| `REQ-BRIEF-CORE` | Mục IV–XLII, 22 câu hỏi chính, 104 acceptance scenarios | Paraphrase thành module requirements và test IDs; không phát hành đường dẫn attachment |
| `REQ-BRIEF-ECOSYSTEM` | Nhiệm vụ, ecosystem position, source-reference rules và định nghĩa objective-to-action | Paraphrase thành architecture, routing, provenance và output contract |

Hai phần được coi là một requirements corpus cho coverage tracking. Khi nội dung yêu cầu dùng
ngôn ngữ tuyệt đối nhưng quyết định thiết kế đã chọn cấu trúc module hợp nhất, coverage được chứng
minh theo năng lực và test ID thay vì theo số lượng file gốc.

## Nguồn không được thu nạp vào release

- Plugin cache IDs, local session identifiers, absolute paths và usernames.
- File cấu hình, matter/workspace, dữ liệu người dùng hoặc output nghiệp vụ mà skill nguồn có thể
  đọc hoặc ghi khi chạy.
- Script, hook, MCP declaration, connector credential flow và shell workflow của nguồn.
- Bảng sample size, materiality heuristic, deadline, threshold hoặc standard version được
  hard-code trong nguồn.
- Nội dung legal research được yêu cầu trả nguyên văn hoặc nội dung bên thứ ba có điều khoản sử
  dụng riêng.
- Trích dẫn dài từ standards, law, frameworks hoặc tài liệu có bản quyền.

## Giới hạn provenance và license

Inventory này không tuyên bố quyền sở hữu hoặc quyền cấp phép lại đối với các skill nguồn. Tên
nguồn chỉ dùng để ghi nhận provenance ở mức thiết kế. License của
`thien-skill-risk-process-control` chỉ điều chỉnh nội dung nguyên gốc của package này; không mở
rộng sang phần mềm, standard, framework, logo, connector hoặc nội dung bên thứ ba.
