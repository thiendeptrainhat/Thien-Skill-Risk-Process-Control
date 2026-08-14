# Source-skill map

## Quy tắc tái sử dụng

Map này mô tả cách các capability từ inventory được chuyển thành thiết kế của skill. `Reuse`
không có nghĩa là sao chép câu chữ hoặc code. Mỗi pattern chỉ được giữ khi phù hợp với bốn lớp
phân tích, evidence rules, human approval gates và yêu cầu chạy đa nền tảng.

Các module đích dùng mã sau:

| Mã | Module |
|---|---|
| `M01` | `architecture-layers-taxonomy.md` |
| `M02` | `document-analysis-and-discovery.md` |
| `M03` | `risk-control-key-control.md` |
| `M04` | `gaps-rationalization-rcm.md` |
| `M05` | `sod-spof-dependencies.md` |
| `M06` | `target-state-and-improvement.md` |
| `M07` | `workflow-metrics-mining-audit.md` |
| `M08` | `standards-sources-applicability.md` |
| `M09` | `governance-security-handoffs.md` |
| `M10` | `data-model-qa-execution.md` |

## Capability map

| Source ID | Capability được tham khảo | Pattern được giữ | Điều chỉnh bắt buộc | Thành phần loại bỏ | Xung đột và cách xử lý | Module đích |
|---|---|---|---|---|---|---|
| `SRC-OPS-PROCESS-DOC` | SOP, RACI, flow, exception, metric | Purpose/scope/roles/steps/exceptions/metrics là các view của cùng process record | Thêm objective, trigger/end boundary, system/data/evidence, approvals, handoffs, layer và confidence; role phải là role, không mặc định tên cá nhân | Lời hứa tạo “complete SOP” từ chỉ tên process; publish/update connector behavior | Nguồn cho phép bắt đầu từ mô tả rất ít; skill này không được bịa steps. Thiếu dữ liệu được ghi `Unresolved` hoặc hỏi khi material | `M01`, `M02`, `M07`, `M10` |
| `SRC-OPS-PROCESS-OPT` | Current-state, waste, future-state, impact | Map trước khi cải tiến; xem waiting, rework, handoff, over-processing và manual work | Thêm risk appetite, control coverage, compliance, evidence, capacity, residual exposure và nhiều design option | “Automate where possible” như mặc định; “checkpoint not gate” như nguyên tắc phổ quát; ước lượng impact không có dữ liệu | Tốc độ có thể xung đột kiểm soát. Chỉ simplify/automate sau risk-control review; không bỏ gate khi residual risk vượt appetite | `M05`, `M06`, `M07` |
| `SRC-OPS-COMPLIANCE-TRACK` | Requirement-control-owner-evidence-gap | Trace requirement đến control/evidence/remediation và audit calendar | Phân loại mandatory/advisory, applicability, source currency và bốn lớp; chỉ ghi effectiveness khi có evidence thích hợp | Bảng framework tóm lược như căn cứ; hard-coded framework statements; “track control effectiveness” không kèm testing basis | Generic compliance checklist dễ biến best practice thành nghĩa vụ. `M08` nắm source status; `M07` nắm testing basis | `M04`, `M07`, `M08` |
| `SRC-FIN-AUDIT-SUPPORT` | Design/OE split, evidence sufficiency, workpaper fields, manual/automated/IT-dependent control | Tách design adequacy khỏi operating effectiveness; control/test cần objective, population, procedure, evidence, exception và reviewer | Mở rộng ngoài ICFR; dùng assertion/test attribute theo context; sample là proposed consideration, không phải quyết định cuối | Materiality heuristics, sample-size table, SOX deficiency conclusion và “one test” shortcut cho automated controls | Nguồn đưa hướng dẫn số cụ thể trong khi brief cấm bịa sample/rating. Skill chỉ đề xuất sau khi có population, methodology và approval | `M03`, `M07`, `M09` |
| `SRC-FIN-SOX-TESTING` | Control matrix, sample-selection rationale, workpaper, remediation | Structured audit handoff và testable control attributes | Đổi “effective/deficiency” thành draft assessment phù hợp scope; buộc reliability test cho IPE và evidence source | Sample ranges mặc định; automatic key-control list; checkbox kết luận audit; CEAVOP áp cho mọi domain | Audit support không được tự phát hành assurance. Human gate tại `M09`; testing logic tại `M07` | `M03`, `M07`, `M09` |
| `SRC-REG-POLICY-DIFF` | Requirement extraction, source tag, scope limitation, policy match, no-match handling | Requirement-level mapping; disclosed scope limitation; source status travels downstream; no silent supplementation | Mở rộng ngoài U.S. regulatory/legal; phân biệt document conflict, control gap, compliance gap và potential finding; ưu tiên official source | Matter-specific paths/writes, U.S.-specific docket rules, automatic handoff/write, lengthy default disclaimer | Nguồn yêu cầu dừng với mọi partial input; brief cho phép tiếp tục khi thiếu không chặn. Chỉ dừng nếu thiếu làm đổi material scope/conclusion | `M02`, `M04`, `M08`, `M09` |
| `SRC-PRIVACY-REG-GAP` | Applicability-first scoping, discrete obligations, current-state diff, remediation | Jurisdiction/threshold/sector/adoption check trước mapping; gap từng requirement; uncertainty visible | Mở rộng khỏi privacy; current state phải tách As-Documented/Designed/Performed; owner/deadline không tự điền | Privacy categories, U.S./EU examples, automatic dated-file write, accepted-gap table không có approval gate | “Accepted gap” chỉ hợp lệ sau authorized risk acceptance; `M09` bắt human approval | `M04`, `M08`, `M09` |
| `SRC-PRIVACY-COLD-START` | Progressive intake, short batches, no silent gaps, source documents, resume markers, connector check | Không hỏi lại; yêu cầu doc/link trước khi bắt gõ lại; explicit missing register; chỉ đánh dấu connector available sau test thật | Intake theo materiality: câu hỏi blocking trước, non-blocking dùng placeholder/confidence; không ghi global profile | Ghi đè/migrate config, ambient plugin setup, legal practice-specific questions và default positions | Nguồn có “sensible defaults”; brief cấm giả định ngầm. Mọi default phải ghi rõ, có basis và không dùng cho threshold/obligation | `M02`, `M09`, `M10` |
| `SRC-SEARCH-SOURCE-MGMT` | Source availability, priority, fallback, rate-limit behavior | Ghi source scope/status; tiếp tục bằng nguồn còn lại và disclose limitation; tránh retry ngay khi rate-limited | Xếp hạng theo authority và query type: policy fact ưu tiên approved document; current practice ưu tiên evidence/log; law ưu tiên official issuer | General default “chat first”; hướng dẫn kết nối platform-specific; tự động dò connector không tồn tại | Recency không đồng nghĩa authority. One-source-of-truth và provenance thắng default priority của enterprise search | `M02`, `M08`, `M10` |
| `SRC-BUILDER-SKILLS-QA` | Dependency mapping, trust surface, freshness, schema, conflicts, injection heuristics | QA gồm upstream/downstream/auto-trigger/breakage; kiểm path/link/schema/freshness/conflict/security; clean scan không phải security guarantee | Chuyển legal-specific verdict thành package QA và output QA; test structural, behavioral, manual và not-run tách riêng | Cơ chế installer/allowlist, raw exact-quote security report, legal-only 13-parameter verdict, external config paths | Nguồn vừa nói REFUSE không override vừa nói verdict advisory. Skill này theo policy cấp cao và human approval; không tái tạo installer behavior | `M09`, `M10` |
| `SRC-DATA-VALIDATE` | Population, null, duplicate, join, reasonableness, cross-check, reproducibility | Event-log/population QA; data grain; completeness; duplicates; date/timezone; cross-validation; caveat/confidence | Chuyển generic analysis QA thành conformance/SoD/control-data reliability checks; không suy control failure chỉ từ anomaly | Numeric red-flag thresholds như rule tuyệt đối; assumptions về warehouse/SQL availability | “Anomaly” là validation lead, không phải operating failure. Cần process context/evidence trước classification | `M05`, `M07`, `M10` |
| `SRC-DATA-CREATE-VIZ` | Purpose/audience-led visualization, accuracy, misleading-axis checks | Chọn diagram/view theo relationship; clarity, labels, scale, limitations và visual QA | Ưu tiên Mermaid/swimlane/BPMN conceptual cho process; render chỉ khi tool có thật; luôn giữ step register canonical | Python/matplotlib dependency, tự ghi PNG vào current directory, chart taxonomy không liên quan | Nguồn mặc định render bằng code; portability yêu cầu syntax/table fallback và cấm tuyên bố render khi chưa kiểm | `M07`, `M09` |
| `SRC-HEALTH-FRAUD-DETECT` | Deterministic evidence floor, staged detect-review-synthesize, indicator framing | Mọi số liệu/allegation phải trace được; model có thể diễn giải nhưng không tự thêm fact; suspected pattern không phải confirmed finding | Áp dụng cho risk/control analytics, process mining và SoD; lưu source reference, confidence, reviewer status; preserve evidence handoff | Toàn bộ healthcare detector, shell/network workflow, data-root writes, external datasets và dollar ranking | Fraud investigation nằm ngoài phạm vi. Skill chỉ flag red flag/control bypass và handoff, không kết luận intent/fraud | `M03`, `M07`, `M09`, `M10` |
| `SRC-LEGAL-DEEP-RESEARCH` | Tool precondition, jurisdiction limit, terminal failure, source-bound report | Kiểm tool/connector availability; dừng rõ khi nguồn chuyên môn bắt buộc không có; giữ jurisdiction boundary | Dùng official-source policy đa jurisdiction; output được tổng hợp với source labels và copyright limits | Westlaw-specific polling, verbatim report relay, U.S.-only scope, provider-specific connector/terms | Verbatim relay xung đột portability, synthesis và licensing. Không thu nạp implementation; chỉ giữ boundary/failure lesson | `M08`, `M09`, `M10` |
| `SRC-CORP-INTEGRATION-MGMT` | Tracker IDs, owner/status/dependency/deadline basis | Stable ID, dependency, blocker, status, source/basis và last-updated fields trong action/implementation views | Tổng quát hóa khỏi M&A; mọi owner/date phải `Not provided` nếu thiếu; canonical schema thay cho file state riêng | Deal-specific workplan, automatic writes, tier logic, contract/legal conclusions và file export mechanics | Structured tracker hữu ích nhưng domain/legal scope không phù hợp. Chỉ giữ schema pattern; routing pháp lý vẫn là handoff | `M05`, `M06`, `M09`, `M10` |

## Các quyết định thiết kế xuyên nguồn

### 1. Evidence thắng fluency

Các nguồn process/optimization có xu hướng tạo output hoàn chỉnh từ input thưa. Thiết kế đích chỉ
cho phép completion khi field có source; nếu không dùng `Not provided`, `To be validated`,
`Inferred` hoặc `Unresolved`. As-Performed cần evidence, walkthrough, log, data, observation hoặc
reperformance phù hợp.

### 2. Design support không phải assurance

Các nguồn SOX cung cấp workpaper tốt nhưng cũng chứa sample-size heuristics và conclusion labels.
Skill giữ test attributes và evidence logic, nhưng không quyết định sample cuối cùng, operating
effectiveness, deficiency severity, audit opinion hoặc legal compliance. Skill chỉ chuẩn bị draft assessment,
test results, issue mapping và handoff; formal conclusion thuộc assurance, Legal hoặc Compliance owner có thẩm quyền.

### 3. Applicability trước control recommendation

Các pattern policy/reg-gap được giữ theo trình tự:

`source status → applicability → discrete requirement → current-state layer → risk → control → gap`.

Framework recommendation, industry practice và leading practice không được đổi nhãn thành
mandatory requirement. Nguồn không xác minh được được ghi `To be validated`.

### 4. Một canonical model, nhiều view

SOP, process map, RACI, RCM, SoD, dependency, metric, audit handoff và action plan là view của cùng
object graph. Stable IDs và relationship validation được ưu tiên hơn nhiều tracker độc lập.

### 5. Tool-optional và portable

Connector, Python, Westlaw, workflow engine và renderer trong nguồn không trở thành dependency bắt
buộc. Nếu tool không có, skill dùng structured table, Mermaid source hoặc handoff; luôn disclose
phần chưa được render, tested hoặc verified.

### 6. Read-only và human gate

Không kế thừa các pattern ghi config, matter folder, ERP, production workflow hoặc source document.
Mọi policy/SOP/RCM/target design là draft. Việc phát hành, đổi quyền, bỏ key control, chấp nhận gap,
kết luận OE hoặc gửi ra ngoài cần người có thẩm quyền phê duyệt.

## Pattern bị loại bỏ có chủ đích

- Hard-coded sample size, materiality, risk score, control threshold, standard version hoặc deadline.
- “Automate by default”, “checkpoint instead of gate” hoặc “all listed controls are key”.
- Lấy policy/management statement làm bằng chứng duy nhất cho As-Performed hay OE.
- Automatic write/publish/update/config migration hoặc handoff có side effect.
- Legal/fraud/audit conclusion do model tự phát hành.
- Plugin-specific absolute path, connector name, source credential và environment setup.
- Output “verbatim” từ dịch vụ bên thứ ba hoặc nội dung standards có bản quyền.
- Tuyên bố scan sạch đồng nghĩa an toàn hoặc test specification đồng nghĩa test đã chạy.

## Traceability sang requirements

Ánh xạ từng mục IV–XLII và toàn bộ test ID A01–M09 nằm tại
[`requirement-coverage-matrix.md`](requirement-coverage-matrix.md). Inventory và map này chỉ chứng
minh provenance/pattern decision; chúng không thay thế behavioral test execution hoặc acceptance
report.
