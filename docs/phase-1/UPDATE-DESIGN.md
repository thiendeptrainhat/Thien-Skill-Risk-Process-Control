# Thiết kế cập nhật — Phase 1

## 1. Trạng thái và căn cứ

- Ngày thiết kế: 27/08/2026, Asia/Ho_Chi_Minh.
- Baseline repository: commit **d65fad595e0265dbe665477b6a5747faa5811139**, skill 1.0.0.
- Phạm vi ủy quyền hiện tại: thiết kế Phase 1, tra cứu công khai chỉ đọc, tạo tài liệu thiết kế và ma trận nghiệm thu.
- Chưa được thực hiện: sửa runtime skill/template, tăng version, build ZIP, cài skill, cấu hình connector, commit/push hoặc phát hành.
- Trạng thái thiết kế: **PROPOSED — READY FOR USER REVIEW**. Không phải phê duyệt nghiệp vụ, chứng nhận hay readiness của phiên bản skill mới.

Căn cứ nội bộ: [skill hiện tại](../../skills/thien-skill-risk-process-control/SKILL.md), [common data model](../../skills/thien-skill-risk-process-control/templates/common-data-model.yaml), [handoff hiện tại](../../skills/thien-skill-risk-process-control/references/governance-security-handoffs.md), [release manifest](../../RELEASE-MANIFEST.yaml) và [behavioral report](../../tests/behavioral-report.md).

## 2. Quyết định đã xác nhận và phạm vi loại trừ

| Quyết định từ người dùng | Hệ quả thiết kế |
|---|---|
| Một skill lõi dùng trên Claude/ChatGPT/Codex | Nội dung trung lập với host, kiểm tra capability thực tế; không tạo runtime riêng |
| Áp dụng khi đọc hoặc tư vấn một/nhóm quy trình | Bao gồm tài liệu hiện trạng và thiết kế mới, không chỉ kiểm tra SOP |
| Không giới hạn theo nhóm E2E cố định | Giữ 94 seed profiles, thêm cách xử lý quy trình chưa có tên hoặc nhiều E2E liên quan |
| Có Document-Evidence chuyên sâu | Handoff tùy nhu cầu, không nhân bản OCR hoặc bắt cài skill phụ để phân tích chat |
| Theo ngôn ngữ người dùng, không tự giả định | Không đổi ngôn ngữ mặc định, không bịa actual state/owner/score/source |
| Chỉ triển khai Phase 1 ở lượt này | Toàn bộ thay đổi vận hành trong Mục 10 chỉ là kế hoạch cho Phase 2–3 |

Không đưa vào đợt nâng cấp: OCR engine, kho full-text standards, công cụ training/model mới, API/MCP server mới, tự mua tài liệu, tự đăng ký tài khoản, thay hệ thống sản xuất hoặc thay license/branding.

Luật áp dụng cho license của skill không tự xác định jurisdiction của quy trình được phân tích. Jurisdiction, industry, risk appetite và các cam kết áp dụng standards của từng tổ chức phải đến từ engagement.

## 3. Mục tiêu và điều kiện hoàn thành nghiệp vụ

| ID | Câu hỏi skill phải trả lời | Bằng chứng đầu ra |
|---|---|---|
| R01 | Quy trình phục vụ mục tiêu gì, nên thiết kế theo E2E nào? | Objective, trigger, outcome, boundary; mapping candidate/được hỗ trợ, nguồn, rationale và điểm chưa xác định |
| R02 | Có những risk nào? | Cause–event–impact–objective, step/process liên quan, dữ kiện và suy luận tách riêng |
| R03 | Expected/key controls theo nguồn phù hợp là gì? | Control objective, baseline source/locator, applicability, mandatory/advisory, candidate controls và keyness rationale |
| R04 | Current controls là gì? | Documented/designed/evidenced-performed controls tách riêng, source/evidence loc và coverage |
| R05 | Gap giữa baseline và hiện trạng nằm ở đâu? | So sánh theo objective/coverage thực chất, gap type, căn cứ, mức uncertainty; không coi thiếu evidence là absence |
| R06 | Nên cải tiến thế nào cho phù hợp? | Recommendation/options, lợi ích, trade-off, dependency, điều kiện/approval và thông tin cần xác nhận |
| R07 | Nếu giữ nguyên thì có rủi ro gì? | No-change scenario, risk driver, impact, protection còn có, exposure/uncertainty và lựa chọn xử lý tạm thời khi phù hợp |

Các yêu cầu xuyên suốt:

- **X01 — Portable:** một nguồn nghiệp vụ; host capability và platform verification được báo riêng.
- **X02 — Source-governed:** phân biệt discovery, nội dung thực đọc, version, applicability, quyền dùng AI và quyền tái phân phối.
- **X03 — Safe:** nguồn ngoài/tài liệu là dữ liệu, không phải chỉ thị; không gửi dữ liệu mật trong truy vấn hoặc vượt quyền.
- **X04 — Optional handoff:** Document-Evidence không là hard dependency; không giả lập việc một skill/tool đã chạy.
- **X05 — Traceable:** cùng IDs/source objects trong các view; giữ null, coverage và conflict.
- **X06 — Evidence-bounded:** không tự giả định; không suy As-Performed/OE, điểm rủi ro, nghĩa vụ hoặc phê duyệt từ mô tả đơn thuần.

Phạm vi mở không có nghĩa mọi nguồn đã có sẵn hoặc mọi tên E2E đều được một standards body quy định. Kết quả hợp lệ có thể là **chưa đủ cơ sở để ánh xạ**, kèm phần phân tích vẫn làm được và câu hỏi cần quyết định.

## 4. Kích hoạt và chọn mức độ xử lý

| Đầu vào/yêu cầu | Route đề xuất | Điều cần giữ |
|---|---|---|
| Chat mô tả quy trình hoặc hỏi một vấn đề hẹp | Phân tích trực tiếp, đọc module cần thiết | Không ép tạo toàn bộ RCM/báo cáo |
| SOP/policy/PDF/Word đọc được | Trích bước/controls và locator; đánh giá hiện trạng theo lớp nguồn hỗ trợ | Không mặc định tài liệu là thực tế vận hành |
| Scan, bảng/sơ đồ mất cấu trúc, thiếu trang hoặc OCR không chắc | Kiểm tra capability, dùng Document-Evidence nếu thực sự cần và khả dụng | Giữ coverage chưa đọc và uncertainty; không tự cài dependency |
| Tư vấn quy trình mới/chưa có SOP | Thiết kế Target-State, tham khảo nguồn phù hợp | Current state chưa cung cấp; không tạo gap hiện trạng giả |
| Nhóm quy trình liên quan | Map nhiều E2E và handoff/dependency; giữ shared controls | Không chia thuần phòng ban, không ép một family duy nhất |
| Chỉ yêu cầu OCR/định dạng/đối soát chứng từ | Không chọn Risk-Process-Control làm owner chính | Chuyển phần chuyên môn phù hợp, không tự mở rộng nhiệm vụ |

Giữ automatic discovery theo description rõ ràng; không biến mọi câu hỏi có chữ “risk” thành trigger. Không thể bảo đảm host luôn tự kích hoạt; hướng dẫn sử dụng có ví dụ gọi tên skill.

## 5. Workflow đề xuất, kế thừa workflow hiện tại

Đây là phân nhóm thiết kế để triển khai vào workflow hiện tại trong Phase 2, không phải thay thế bằng một chuỗi bắt buộc mới cho mọi câu hỏi.

### 5.1 Intake và trạng thái capability

Thu thập dữ kiện đã có, chỉ hỏi phần thiếu làm thay đổi quyết định: mục tiêu, intended use, trigger/outcome, phạm vi, nguồn, kỳ phân tích, industry/jurisdiction khi cần, hiện trạng hay thiết kế mới.

Ghi capability quan sát được: đọc file, layout/vision/OCR, tra cứu web, nguồn người dùng cung cấp, connector đã cấu hình và specialist khả dụng. Không suy capability từ tên “Claude”, “ChatGPT”, “Codex” hoặc registry trống.

Phân biệt trạng thái **available**, **unavailable**, **not_checked**, **permission_required**. Chỉ dùng capability được phép cho nhiệm vụ. Không kiểm tra hay đăng nhập tất cả nguồn theo danh mục mỗi lần kích hoạt.

### 5.2 Hiểu E2E theo phạm vi mở

1. Trích business outcome, beneficiary/customer, trigger, end condition, inputs/outputs, activities, systems và handoffs được nguồn hỗ trợ.
2. Phân biệt quy trình đang thấy với E2E lớn hơn: tài liệu có thể chỉ mô tả một subprocess.
3. Dùng seed profiles để định hướng, nhưng tìm ngoài danh mục khi không phù hợp hoặc khi cần benchmark chuyên ngành.
4. Xem xét nguồn taxonomy, reference model hoặc vendor blueprint theo [catalog](REFERENCE-LIBRARY-CATALOG.md); không coi taxonomy là trình tự workflow.
5. Cho phép một process map sang nhiều reference items/E2E; giữ primary/supporting/overlap rationale khi có cơ sở.
6. Phân biệt **reference classification** với **recommended organization-specific E2E design**. Tên đề xuất không được giả làm tên/ID chuẩn của nguồn.
7. Giữ mapping là candidate nếu evidence chưa đủ; hỏi điểm phân định hoặc trả no reliable match. Không tự chọn một family chỉ vì trùng acronym.

Đánh giá mức phù hợp bằng rationale và evidence. Không tạo điểm phần trăm similarity/confidence nếu chưa có một phương pháp được xác định và chấp nhận.

### 5.3 Tra cứu process library và control baseline

- Tra cứu chỉ đọc bằng công cụ host sẵn có, nguồn được người dùng cung cấp hoặc connector đã được cấu hình và cho phép.
- Chọn nguồn theo scope; không cố đọc đủ tất cả framework. Registry là nơi bắt đầu, không là whitelist đóng.
- Trước truyền tài liệu ra ngoài, kiểm tra permission và data classification. Truy vấn web dùng mô tả nghiệp vụ tối thiểu đã loại thông tin nhạy cảm, không chép SOP hoặc tên cá nhân/bí mật vào query.
- Tách metadata, content access, AI-use permission và redistribution permission. Public/free access không tự chứng minh nội dung đã được kiểm chứng, quyền sử dụng trong AI hoặc quyền tái phân phối.
- Đọc nội dung/điều khoản thực sự hỗ trợ claim trước khi gắn baseline verified. Search snippet, trang giới thiệu hoặc tên framework không đủ chứng minh một control cụ thể.
- Với nguồn bị hạn chế, dừng truy cập phần đó; dùng nguồn hợp lệ khác hoặc yêu cầu nội dung/quyền phù hợp. Không tìm mirror để vượt chặn.
- Nếu không có source được xác minh, vẫn có thể đưa risk/control design proposal có nhãn, nhưng không gọi là standard-derived, compliant hay fully benchmarked.
- Nếu nguồn xung đột, lưu từng version/scope và điểm khác nhau; không tự giải quyết conflict về authority trọng yếu.

Phạm vi quốc gia, điều kiện chứng nhận, hợp đồng và adoption quyết định nghĩa vụ. Không biến best practice thành bắt buộc hoặc một nguồn nước ngoài thành luật cho mọi tổ chức.

### 5.4 Risk và control baseline

Kế thừa Cause–Event–Impact–Objective. Tách source facts, analyst inference và proposal; không tạo sự kiện thất thoát/gian lận đã xảy ra khi chỉ có risk scenario.

Từ nguồn phù hợp, xác định control objective trước; sau đó đề xuất control pattern với owner/action/timing/data/criteria/evidence/exception như dữ liệu đã biết hoặc nội dung cần phê duyệt. Source chỉ quy định outcome thì không gán một cách triển khai duy nhất là bắt buộc.

Keyness cần rationale theo significant risk, obligation, dependency và khả năng thay thế trong bối cảnh cụ thể. Một control được liệt kê trong thư viện chưa tự là key control. Phải phân biệt key-control candidate, supporting control và alternative/compensating control; gắn source → objective → risk → control → keyness rationale. Đánh giá của analyst không tự là quyết định keyness đã được tổ chức phê duyệt.

### 5.5 Current state và so sánh

Giữ nguyên bốn analysis layers của baseline. Không thêm lớp “actual” mơ hồ.

- As-Documented: tài liệu hiện hành ghi gì.
- As-Designed: thiết kế được xác nhận, kể cả có tài liệu bổ sung.
- As-Performed: việc thực hiện có evidence phù hợp cho đúng case/kỳ/phạm vi.
- Target-State: đề xuất tương lai chưa phê duyệt.

So sánh theo control objective, coverage, timing, precision, independence, evidence và dependency. Xem xét alternative/compensating controls và điều kiện chấp nhận; khác tên hoặc manual/automated không tự tạo deficiency.

Phân biệt documentation gap, design gap, evidence limitation, operating deviation và compliance gap có baseline mandatory đã xác minh. Một control chưa xuất hiện trong SOP có thể là **not described in reviewed scope**, không tự là **does not exist**.

Một transaction log chỉ hỗ trợ kết luận trong phạm vi quan sát; không tự chứng minh operating effectiveness của cả kỳ/population. Formal assurance vẫn thuộc owner có thẩm quyền như baseline hiện tại.

### 5.6 Cải tiến và no-change exposure

Gắn recommendation với gap hoặc design opportunity và control objective. Tách mandatory remediation khỏi discretionary enhancement. Với lựa chọn có trade-off, trình phương án và điều kiện khả thi thay vì luôn chọn automation.

Mỗi material gap có phần nếu giữ nguyên: causal scenario, event/impact có thể xảy ra, existing protection, exposure chưa được xử lý, uncertainty và validation needed. Nếu chưa có gap được chứng minh, trình scenario như hypothesis, không nâng thành actual deficiency.

Không tự tạo risk score, loss, probability, time horizon, owner, due date hoặc ngân sách. Có thể nêu ưu tiên bằng rationale/critical dependencies; rating định lượng chỉ theo methodology được cung cấp/phê duyệt.

### 5.7 Báo cáo và stop conditions

Cho câu hỏi hẹp: câu trả lời tương xứng, có source/limitation. Cho engagement đầy đủ: trả bảy câu trả lời R01–R07 bằng một bộ dữ liệu truy nguyên.

Dừng phần bị ảnh hưởng khi thiếu authority, source bị khóa, dữ liệu trọng yếu không đọc được hoặc lựa chọn bắt buộc chưa rõ. Tiếp tục phần độc lập an toàn; không giả định toàn engagement đã hoàn thành.

## 6. Đề xuất cấu trúc dữ liệu và đầu ra

Đây là **contract thiết kế**, chưa phải schema runtime đã sửa. Kế thừa base_fields, IDs và many-to-many relationships của common data model; bổ sung field/relationship có mục đích rõ, không dựng database riêng.

| Nhóm record/view | Trường thiết kế cần có | Quy tắc |
|---|---|---|
| Process reference mapping | process_id, reference_library_id, reference_item_id, reference_version, source_id/locator, relationship_scope, fit_status, mapping_rationale, unresolved_questions | External ID chỉ ghi khi đã đọc nguồn; null nếu chưa có. Một process có nhiều mappings; giữ internal process ID khác external ID |
| Source-use record | source_id, reference_kind, issuing_body, official_location, observed_version/status, date_checked, content_checked_scope, access_status, ai_use_status, redistribution_status, applicability, limitations | Tái sử dụng source register; không coi một cờ verified là xác minh mọi mặt |
| Baseline-to-control link | source_id/locator, baseline_basis, mandatory_or_advisory, applicability_rationale, control_objective_ids, candidate_control_ids, interpretation_rationale | Baseline có thể là requirement, principle, practice hoặc analyst proposal; proposal không giả có external citation |
| Logical control identity | control_id, control_objective/risk links, process/step relationships | Một control dùng chung nhiều E2E giữ cùng logical ID khi có căn cứ; tên giống nhau chưa đủ để gộp identity |
| Control observation/assessment | control_observation_id, control_id, analysis_layer, control_description, assessed_scope, assessed_period, source/evidence_ids và locators, key_control_status/rationale, design_assessment, assessment_status, limitations | Mỗi ghi nhận có ID riêng; giữ các lớp/kỳ/nguồn mâu thuẫn, không ghi đè mô tả hoặc evidence vào một record duy nhất |
| Comparison view | objective/risk links, baseline links, logical_control_ids, documented/designed/performed_observation_ids, target_observation_ids khi có, evidence_ids, coverage_assessment, gap_ids, limitations | Tham chiếu đúng observation cùng scope/kỳ, không chỉ logical ID. “Evidence insufficient” không là fail; không ép control matching một-một |
| Recommendation/action | gap/design-opportunity link, recommendation/action IDs, option rationale, dependencies, owner/due-date status, approval requirements | Không tạo fake gap để gắn recommendation cho greenfield |
| No-change scenario | risk/gap links khi có, scenario_basis, cause/event/impact, existing_protection, unmitigated_exposure, horizon, uncertainty, validation_needed | horizon có thể null; không dùng future risk như actual incident |

Source-use metadata không phải một trạng thái vận hành của tổ chức. Vai trò “expected/current” trong comparison không thay thế analysis_layer. Nếu tạo candidate control cho target design, gắn Target-State/proposed; nếu chỉ mô tả requirement, giữ nó ở source/requirement record.

Ví dụ identity: SOP mô tả một control hai cấp duyệt và log ghi một case chỉ một cấp có thể liên kết cùng logical control, nhưng phải có hai observation riêng với layer, locator và scope tương ứng. Không thay description trong SOP bằng log, cũng không dùng SOP để làm đầy phần evidence còn thiếu. Keyness và kết quả đánh giá giữ phạm vi/rationale/review status của observation; chưa biết kỳ hoặc layer thì giữ null/unresolved, không tự cấp giá trị.

Trạng thái đề xuất:

- fit_status: supported_match, candidate_match, partial_match, no_reliable_match, unresolved.
- coverage_assessment: alignment_supported, potential_gap, documented_gap, evidence_insufficient, conflicting_evidence, not_applicable.
- ai_use_status: not_assessed, conditions_to_check, permission_evidenced, restricted_pending_permission.
- assessment_status kế thừa ý nghĩa trong hướng dẫn hiện tại; null semantics kế thừa common data model, không tự chuyển “unknown” thành zero/false. Field design_assessment đang có trong control-register phải được bảo toàn, không đổi tên ngầm thành assessment_status.

Các tên field/enum và observation ID này là đề xuất Phase 1, chưa phải schema được triển khai. Phase 2 phải xác định mapping/prefix và cách đọc output 1.0.0: giữ IDs, facts, null, design_assessment và locators cũ; thiếu field mới thì ghi chưa cung cấp, không suy baseline verified, layer hay performed state. Không tự đổi schema_version của mọi file. Nếu không thể giữ compatibility bằng thay đổi additive, dừng phần thay schema/version và trình lại quyết định cho người dùng. P1-U22 kiểm tra điều kiện này trước claim tương thích.

### Output tối thiểu cho một engagement đầy đủ

1. Executive answer cho R01–R07, scope, analysis layers và limitations.
2. E2E map/step register và mapping rationale; không buộc vẽ hình khi bảng đủ rõ.
3. Risk/control register cùng bảng baseline–current–gap.
4. Recommendation/no-change exposure/action view.
5. Source register, evidence/coverage và danh sách cần người dùng xác nhận.

Các view dùng chung IDs; không sao chép nhiều bộ facts độc lập. Có thể trả Markdown; chỉ tạo Word/Excel hoặc artifact khác khi người dùng yêu cầu và capability phù hợp.

## 7. Handoff với Document-Evidence

Skill này sở hữu diễn giải process–risk–control; Document-Evidence sở hữu integrity/extraction/provenance. Handoff ở đây là chuyển phần việc cho capability thực sự khả dụng, có thể trong cùng assistant/session; không giả định cơ chế skill-gọi-skill hoặc liên nền tảng tự động.

### Yêu cầu gửi

| Thông tin | Mục đích |
|---|---|
| task/handoff ID; objective; document_sources | Một tác vụ bounded, xác định đúng nguồn được phép đọc |
| authorized_scope; data_classification; local/cloud constraints | Không mở rộng quyền hoặc gửi tài liệu sang dịch vụ ngoài |
| required_content | Steps, decisions, roles, controls, bảng/sơ đồ và locator cần cho phân tích |
| expected output và unresolved areas | Chỉ yêu cầu dữ liệu cần thiết, không ép chạy reconciliation/investigation route |

### Kết quả cần nhận và kiểm tra

- task/handoff ID và document/extraction-run identifiers nếu runtime có.
- Nội dung trích xuất và locator: file, page/section/paragraph/table/region theo format; không bịa số trang Word hoặc chat.
- scope_and_coverage, trang/phần chưa đọc, extraction method và warning.
- raw/normalized values khi normalization cần thiết, field/table status và confidence có căn cứ; không tạo numeric OCR confidence.
- source/evidence references, contradictions, human-review queue, limitations và review/approval status.

Ánh xạ document_id vào source register, giữ evidence_id của upstream nếu có; không cấp tên khác làm mất đường truy nguyên. HUMAN_REVIEW_REQUIRED/UNVERIFIED không được biến thành verified fact khi nhập sang RCM.

Nếu Document-Evidence không khả dụng nhưng host đọc được: tiếp tục bằng capability được phép và giữ giới hạn. Nếu không đọc được phần quyết định: yêu cầu bản rõ/working transcription hoặc human review; không giả đã OCR.

Không sửa Document-Evidence hoặc tạo phụ thuộc hard vào phiên bản cài ở máy này trong Phase 2. Nếu phát hiện contract không tương thích thật sự, ghi separate change request để người dùng quyết định.

## 8. Cách nghiệm thu thiết kế và runtime

Chi tiết tại [ACCEPTANCE-MATRIX.yaml](ACCEPTANCE-MATRIX.yaml).

- Phase 1: kiểm tra coverage R01–R07/X01–X06, logic hợp đồng dữ liệu, source status, links và ranh giới ủy quyền.
- Phase 2: kiểm tra runtime instructions/templates thực sự phù hợp với thiết kế đã duyệt.
- Phase 3: chạy behavioral cases với raw artifacts và rubric tách khỏi model; giữ platform/capability và hashes.
- Không dùng một nhãn PASS cho cả cấu trúc ZIP, nội dung nghiệp vụ, quyền sử dụng nguồn và runtime behavior.
- Tài liệu test tổng hợp phải được gắn nhãn synthetic; không giả standard chính thức hoặc evidence của doanh nghiệp.
- Nguồn giả lập dùng cho test logic khác với test tra cứu thật. Cả hai loại phải được phân biệt trong report.
- Ma trận xác định rõ case/variant bắt buộc cho từng claim. Đạt phải có đủ bằng chứng, đạt mọi mandatory invariant và không xuất hiện forbidden behavior; đã review, chưa chạy hoặc chỉ đạt một biến thể không thay kết quả của cả nhóm.

## 9. Điều kiện chuyển phase và quyết định còn mở

| Quyết định | Trạng thái | Khi cần |
|---|---|---|
| Chấp thuận thiết kế và danh mục nguồn như candidate index | Chờ người dùng duyệt | Trước Phase 2 |
| Nhãn release tiếp theo | Đề xuất 1.1.0 nếu additive; chưa chốt | Trước sửa version/release metadata |
| Thư viện nội bộ/trả phí và quyền dùng AI cụ thể | Chưa cung cấp; không giả định đã có | Chỉ khi engagement hoặc test cụ thể phụ thuộc nguồn |
| Truy cập/cài đặt để kiểm thử Claude/ChatGPT surfaces | Chưa được cấp thêm quyền | Trước test yêu cầu hành động mới; nếu chưa có thì not_run |
| Commit/push và phát hành GitHub | Không nằm trong ủy quyền Phase 1 | Chỉ thực hiện khi người dùng yêu cầu |

Hai nguồn bị chặn truy cập không chặn hoàn thành thiết kế: chúng là optional candidates, không có baseline claim dựa trên nội dung chưa đọc.

## 10. Bản đồ thay đổi dự kiến cho Phase 2–3

Đường dẫn dưới đây tương đối với root repository; không file nào trong danh sách đã được sửa ở Phase 1.

| Nhóm | Artifact đích dự kiến | Delta |
|---|---|---|
| Entry/routing | skills/thien-skill-risk-process-control/SKILL.md; agents/openai.yaml nếu metadata cần chỉnh | Scope mở, đúng trigger, selective references; giữ invocation policy |
| E2E | references/architecture-layers-taxonomy.md; target-state-and-improvement.md; end-to-end-process-profiles.md | Open-world mapping; seed không exhaustive; loại trùng catalog ở nơi không cần |
| Source | references/standards-sources-applicability.md; một reference mới về external-library discovery nếu hợp lý | Loại nguồn, access/AI-use gates, lookup/fallback; không connector code |
| Risk/gap | references/risk-control-key-control.md; gaps-rationalization-rcm.md | Baseline/current/evidence, equivalent controls, no-change exposure |
| Input/handoff | references/document-analysis-and-discovery.md; governance-security-handoffs.md; integration/master-orchestrator-registry-entry.yaml nếu mô tả capability đổi | Optional Document-Evidence contract và truthful runtime status |
| Model/views | references/data-model-qa-execution.md; templates/common-data-model.yaml; process-architecture-step-register.yaml; control-register.yaml; rcm.yaml; action-plan.yaml | Additive fields/links; comparison view có thể thêm một template khi cần, không nhân đôi facts |
| Coverage/examples | references/requirement-coverage-matrix.md; examples/catalog.md; tests/ | Kế thừa regression, thêm suite thực tế và evidence records |
| Build/report | scripts/run_tests.py; scripts/build_release.py; README.md; INSTALL.md; RELEASE-MANIFEST.yaml | Bỏ lệ thuộc số case/version hard-code khi cần; báo cáo static/behavioral riêng; đồng bộ version |
| Distribution | dist/ và checksum của release mới | Ba ZIP từ cùng snapshot; nội dung canonical đồng nhất sau normalize wrapper/metadata |

License, assets/logo và Document-Evidence không thuộc phạm vi chỉnh sửa. Các sửa đổi chỉ được thực hiện sau khi phase tương ứng được ủy quyền.
