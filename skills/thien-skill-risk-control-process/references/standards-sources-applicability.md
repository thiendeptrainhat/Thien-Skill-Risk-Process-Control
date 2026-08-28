# Standard, source, applicability và control provenance

## Mục lục

1. [Mục đích và nguyên tắc](#1-mục-đích-và-nguyên-tắc)
2. [Phân loại control source](#2-phân-loại-control-source)
3. [Lập source record](#3-lập-source-record)
4. [Xác minh nguồn hiện hành](#4-xác-minh-nguồn-hiện-hành)
5. [Đánh giá applicability](#5-đánh-giá-applicability)
6. [Phân biệt mandatory và advisory](#6-phân-biệt-mandatory-và-advisory)
7. [Dùng standard và framework](#7-dùng-standard-và-framework)
8. [Đề xuất best-practice control pattern](#8-đề-xuất-best-practice-control-pattern)
9. [Quản lý copyright và quyền sử dụng](#9-quản-lý-copyright-và-quyền-sử-dụng)
10. [Mapping source tới control và requirement](#10-mapping-source-tới-control-và-requirement)
11. [Xử lý nguồn không đủ hoặc mâu thuẫn](#11-xử-lý-nguồn-không-đủ-hoặc-mâu-thuẫn)
12. [Kiểm tra chất lượng](#12-kiểm-tra-chất-lượng)

## 1. Mục đích và nguyên tắc

Áp dụng module này khi người dùng yêu cầu best practice, global standard, industry standard, regulatory control, compliance mapping, certification mapping hoặc source của một control. Khi cần tìm thư viện E2E/process hoặc chọn nguồn bên ngoài, đọc [external-process-control-libraries.md](external-process-control-libraries.md); đó là danh mục điểm tham chiếu và discovery guide, không phải connector hoặc nội dung baseline đã có sẵn.

Thực hiện các nguyên tắc sau:

- Xác minh source và nội dung liên quan tại thời điểm dùng cho claim; không hard-code version như thể luôn hiện hành hoặc mở mọi nguồn khi skill kích hoạt.
- Ưu tiên nguồn chính thức và văn bản gốc.
- Tách tính có thẩm quyền của source khỏi applicability cho organization/process cụ thể.
- Phân biệt legal/regulatory obligation, contractual obligation, adopted standard, framework recommendation, industry practice và organization preference.
- Không dùng cụm “global standard control” nếu chưa nêu source, clause, status và applicability.
- Không dùng blog, bài viết hoặc AI summary làm căn cứ duy nhất cho control trọng yếu.
- Không biến best practice hoặc framework recommendation thành legal requirement.
- Không sao chép dài standard, framework, publication hoặc tài liệu có bản quyền.
- Ghi source, version/status, clause/reference, verification date, limitations và confidence có căn cứ cho mỗi control được trình bày là source-derived. Proposal chưa có external source phải được nhận diện là analyst proposal, không bịa citation.
- Tách quyền truy cập, phạm vi nội dung đã đọc, quyền dùng nội dung trong AI và quyền tái phân phối. Một cờ `verified` không chứng minh cả bốn mặt.
- Khi không thể xác minh nguồn hoặc nội dung cần thiết, ghi giới hạn của claim và yêu cầu xác minh phù hợp; vẫn làm phần phân tích độc lập an toàn.

## 2. Phân loại control source

Ghi riêng `reference_kind` theo công dụng: process taxonomy, process reference model, vendor blueprint, control framework/catalog, management standard, risk guidance, law/regulation, contract/internal policy hoặc modeling notation. Phân loại này không xác định source có bắt buộc hay không; không đưa một taxonomy hoặc chuẩn notation thành control requirement.

Với source được dùng cho control baseline, phân loại `source_type` vào một nhóm chính và ghi nhóm phụ khi cần:

1. `Mandatory law or regulation`: law, regulation, binding rule hoặc quyết định có hiệu lực trong jurisdiction và scope áp dụng.
2. `Regulatory guidance`: guidance, circular, supervisory expectation, FAQ hoặc interpretive material của regulator; xác định riêng mức ràng buộc.
3. `Contractual requirement`: obligation từ contract, covenant, customer term, supplier term hoặc service agreement có hiệu lực.
4. `Adopted or certified standard requirement`: requirement của standard mà organization đã adopt, cam kết hoặc dùng cho certification scope.
5. `Recognized framework-aligned control`: control hoặc principle được mapping với recognized framework nhưng không tự bắt buộc.
6. `Industry common practice`: practice được sử dụng phổ biến trong industry phù hợp.
7. `Leading practice`: practice nâng cao có thể vượt common practice và cần đánh giá feasibility.
8. `Organization-specific control`: control do policy, risk appetite, governance hoặc design decision nội bộ tạo ra.
9. `Compensating control`: control thay thế hoặc giảm exposure khi primary requirement/control không thể đáp ứng theo cách ban đầu.

`Compensating control` mô tả vai trò thiết kế, không phải issuing authority hoặc một giấy phép miễn trừ. Nếu gặp nhãn legacy này, vẫn ghi nguồn requirement thực tế và basis cho alternative. Không dùng nó để che giấu non-compliance; xác minh requirement có cho phép approach đó không và ai có authority phê duyệt.

## 3. Lập source record

Tái sử dụng một source register; không lập bộ facts riêng trong từng RCM/template. Giữ `source_id`, `version`, `date_verified`, `source_reference` và locators đã có; thêm metadata khi có căn cứ, không đổi tên hoặc suy giá trị cho output cũ. Record cần đủ các field liên quan tới claim sau:

| Field | Cách ghi |
|---|---|
| `source_id` | Gán ID ổn định và duy nhất. |
| `source_type` | Chọn taxonomy tại Mục 2. |
| `reference_kind` | Ghi công dụng của nguồn; tách khỏi authority/mandatory status. |
| `source_name` | Ghi tên dùng trong mapping. |
| `official_title` | Ghi title chính thức theo nguồn gốc. |
| `issuing_body` | Ghi cơ quan, standards body, contracting party hoặc policy owner. |
| `version` | Giữ field cũ cho edition/version đúng tài nguyên; để null/chưa xác minh nếu chưa có, không tự điền “latest”. Phân biệt publication revision với dataset release. |
| `publication_date` | Ghi ngày publication nếu có nguồn. |
| `effective_date` | Ghi ngày có hiệu lực; phân biệt với publication date. |
| `source_status` | Ghi current, amended, superseded, withdrawn, draft, transitional hoặc chưa xác minh theo source chính thức. |
| `clause_or_reference` | Ghi article, clause, control, section hoặc pinpoint reference. |
| `jurisdiction` | Ghi lãnh thổ/phạm vi pháp lý; dùng `Not applicable` cho source không theo jurisdiction khi phù hợp. |
| `mandatory_or_advisory` | Ghi legal/regulatory, contractual, adopted/internal hoặc advisory status; tránh nhãn nhị phân thiếu context. |
| `adopted_by_organization` | Ghi evidence adoption, certification hoặc internal approval. |
| `adoption_status` | Ghi adopted, partially adopted, planned, not adopted hoặc `To be validated`. |
| `applicability` | Ghi kết luận và rationale theo Mục 5. |
| `date_verified` | Ghi ngày thực xác minh thành công và scope tương ứng; không gán ngày thử truy cập thất bại thành ngày verified. |
| `date_checked` | Ngày thực sự thực hiện lượt kiểm tra, kể cả chỉ đọc metadata hoặc truy cập thất bại; không tự đồng nghĩa `date_verified`. |
| `content_verification_status` | `not_checked`, `overview_verified` hoặc `content_verified`, kèm scope chính xác; không gán cho toàn framework chỉ vì đọc một trang. |
| `content_checked_scope` | Ghi đúng tài nguyên, section/clause/item/metadata đã đọc và phần chưa đọc. |
| `access_status` | Ghi access quan sát ở đúng tài nguyên: `not_checked`, `available`, `access_limited` hoặc `permission_required`; không suy toàn website có cùng access. |
| `ai_use_status` | `not_assessed`, `conditions_to_check`, `permission_evidenced` hoặc `restricted_pending_permission`; quyền dùng nội dung trong AI xét riêng quyền đọc. |
| `redistribution_status` | Ghi quyền/phạm vi tái phân phối đã kiểm tra hoặc chưa xác minh; không suy quyền từ public access hoặc AI-use. |
| `official_location` | Ghi official URL, gazette, standards catalog, contract repository hoặc controlled policy location. |
| `language` | Ghi official language và status của translation. |
| `copyright_or_license` | Ghi basis, điều kiện và locator về access, AI-use, quotation, reproduction và redistribution theo nội dung cụ thể. |
| `limitations` | Ghi scope exclusion, transition, unavailable text hoặc interpretive uncertainty. |
| `verification_evidence` | Liên kết screenshot, metadata, publication notice hoặc controlled record được phép lưu. |
| `owner_or_reviewer` | Ghi role chịu trách nhiệm xác minh applicability khi cần. |
| `confidence` | Dùng confidence scale được định nghĩa cho engagement. |

Không dùng `version` của source làm version của skill, control hoặc policy. Không coi source record là bằng chứng organization đã adopt standard nếu thiếu adoption evidence. Các field mới thiếu trong record cũ giữ null/not_checked theo common data model; không tự nâng thành verified hoặc permitted.

Một lượt kiểm tra có thể xác nhận metadata edition nhưng chưa đọc clause. Ghi rõ mức đó và giữ lịch sử kiểm tra nếu access/status thay đổi; không ghi đè lần đọc trước thành một lần xác minh mới chưa diễn ra. Metadata trong skill hoặc registry là observation có ngày, không phải runtime verification của engagement. Quyền sử dụng và content verification không phải analysis layer hay bằng chứng control đang vận hành.

## 4. Xác minh nguồn hiện hành

Chỉ tra cứu khi câu hỏi cần nguồn đó, bằng công cụ host được phép, nguồn người dùng cung cấp hợp lệ hoặc connector đã cấu hình và được cho phép. Trước retrieval, kiểm tra capability, privacy và điều kiện sử dụng đã biết theo [discovery guide](external-process-control-libraries.md). Không mua, đăng nhập, cài connector hoặc truyền tài liệu ra ngoài chỉ vì đã chọn một source trong danh mục.

Thực hiện protocol sau tại thời điểm dùng source:

1. Mở official publisher, regulator, gazette, standards body, framework owner, contract repository hoặc controlled company source.
2. Xác minh official title, issuing body, publication date, effective date và identifier.
3. Xác minh current edition/version, amendment, addendum, corrigendum, interpretation, supersession, withdrawal và transition.
4. Xác minh jurisdiction, effective period, covered subject, activity, entity, product, process và exceptions.
5. Xác minh translation có phải official/authorized không; ưu tiên authoritative text khi có conflict.
6. Đọc đúng nội dung hỗ trợ claim và lưu locator, `content_checked_scope`, access/AI-use/redistribution status; trang giới thiệu không chứng minh một clause hay control cụ thể.
7. Ghi `date_checked`, `date_verified` trong phạm vi thực xác minh, official location và evidence được phép lưu. Chỉ dùng secondary source để tìm official source hoặc bổ sung context có nhãn.
8. Nếu không truy cập được authoritative text, giữ riêng metadata đã kiểm chứng và nội dung chưa kiểm chứng; không đưa kết luận dứt khoát phụ thuộc phần chưa đọc. Không bịa current status từ snippet.

Không dựa vào title, search snippet, blog, training slide hoặc bản sao không rõ provenance để nói standard “mới nhất” hoặc requirement “bắt buộc”.

Đối với law/regulation, kiểm tra amendment, repeal, transition và authority theo ngày sự kiện. Đối với contract, kiểm tra parties, effective date, term, amendment, order of precedence và surviving obligations. Đối với internal policy, kiểm tra version, approval, effective date, scope và superseded documents.

## 5. Đánh giá applicability

Không suy ra applicability chỉ từ tên source hoặc ngành. Lập applicability analysis theo các dimension phù hợp:

- `Subject`: organization, legal entity, regulated entity, business unit, supplier hoặc customer nào?
- `Jurisdiction`: source áp dụng ở lãnh thổ nào và có extraterritorial effect không?
- `Activity`: process, service, product, transaction hoặc data processing nào nằm trong scope?
- `Industry`: sector, license, certification hoặc supervisory regime nào liên quan?
- `Size or criteria`: source có criteria, exemption hoặc trigger nào? Chỉ dùng criteria đã xác minh; không hard-code.
- `Time`: effective date, transition, grandfathering, contract term hoặc policy period nào?
- `Adoption`: organization đã adopt, certify, contractually commit hoặc approve source ở mức nào?
- `Organizational scope`: entity, site, system, product, process hoặc geography nào nằm trong scope adoption/certification?
- `Exclusion`: exception, carve-out, alternative approach hoặc non-applicable clause nào?
- `Dependency`: source có viện dẫn source khác hoặc phụ thuộc local implementation không?

Ghi kết luận bằng một trong các trạng thái có rationale:

- `Applicable`;
- `Conditionally applicable`;
- `Not applicable`;
- `To be validated`.

Không coi `Not applicable` là miễn mọi related obligation. Ghi source hoặc criterion hỗ trợ kết luận. Luật áp dụng cho license của skill không tự xác định jurisdiction của quy trình. Chuyển legal interpretation trọng yếu cho qualified legal/compliance reviewer.

## 6. Phân biệt mandatory và advisory

Phân loại bằng logic sau:

### Law hoặc regulation

Chỉ ghi `Mandatory legal/regulatory` khi:

- source có hiệu lực tại ngày liên quan;
- subject, jurisdiction, activity và scope đều áp dụng;
- điều khoản tạo nghĩa vụ, cấm đoán hoặc điều kiện ràng buộc;
- không có exemption hoặc transition loại trừ case.

Không gọi regulatory guidance là law. Xác định guidance có binding effect do incorporation, supervisory mandate hoặc mechanism khác không.

### Contract

Ghi `Mandatory contractual` trong phạm vi parties, scope và term của contract. Không trình bày contractual requirement như nghĩa vụ pháp luật áp dụng cho mọi organization.

### Adopted hoặc certified standard

Không coi standard tự động là mandatory chỉ vì được quốc tế công nhận. Xác định standard trở thành binding trong context nào:

- law/regulation incorporation;
- contract incorporation;
- certification commitment;
- tender/customer condition;
- board, policy hoặc governance adoption.

Ghi rõ `mandatory due to [basis]`, scope adoption và evidence. Nếu chưa adopt, phân loại requirement của standard là advisory candidate cho organization, trừ khi có basis khác.

### Framework và practice

Ghi framework recommendation, industry common practice và leading practice là `Advisory` trừ khi source khác đã incorporate chúng. Không gọi framework alignment là certification compliance.

### Internal policy

Ghi `Mandatory internally` nếu policy có authority, approval, effective status và scope phù hợp. Không đồng nhất internal mandate với legal obligation.

## 7. Dùng standard và framework

Dùng [danh mục tham chiếu mở](external-process-control-libraries.md) làm điểm bắt đầu, không như danh sách bắt buộc hoặc giới hạn nguồn. Luật/quy định, hợp đồng, policy nội bộ và thư viện ngành ngoài danh mục vẫn được xem xét nếu có scope, authority và quyền phù hợp.

| Loại tham chiếu | Cách dùng | Không suy ra |
|---|---|---|
| Process taxonomy/reference model | Phân loại, tên/ID, boundary hoặc process relationships khi nguồn hỗ trợ | Taxonomy tự là workflow, danh mục exhaustive hay control requirement |
| Vendor blueprint | Gợi ý scenario, interface và triển khai trong context sản phẩm | Cấu hình vendor là control bắt buộc hoặc actual system của organization |
| Control framework/catalog, management standard, risk guidance | Xác định principle/requirement/objective hoặc candidate control trong scope đã đọc | Mọi item là key control, hoặc một pattern duy nhất là bắt buộc |
| Law/regulation, contract/internal policy | Xác định obligation dựa trên authority, effective period và adoption | Mọi guidance đều là luật; một nguồn bên ngoài luôn thắng hierarchy nội bộ |
| Modeling notation | Biểu diễn và kiểm tra semantics của model | Sơ đồ đúng cú pháp chứng minh process/controls đúng hoặc vận hành hiệu quả |

Phân loại nguồn trước khi dùng, rồi xác minh đúng nội dung và applicability. Không dùng một version/verification status chung cho cả hệ nguồn có publication, dataset, workbook và addendum khác nhau.

Khi mapping source:

1. Xác minh quyền dùng nội dung rồi trích/paraphrase requirement/principle ở mức cần thiết.
2. Phân biệt direct requirement với interpretation hoặc design recommendation.
3. Gắn pinpoint reference và status.
4. Giải thích applicability và limitation.
5. Chuyển requirement thành control objective trước khi đề xuất control cụ thể.
6. Cho phép nhiều control patterns đáp ứng cùng objective; không sao chép control máy móc.

## 8. Đề xuất best-practice control pattern

Dùng các pattern sau như candidate design khi context phù hợp:

- Maker–checker;
- Four-eyes review;
- Independent approval;
- Three-way match;
- Automated validation;
- Duplicate detection;
- System-enforced threshold;
- Master-data governance;
- Independent reconciliation;
- Exception reporting;
- Aging monitoring;
- Mandatory field validation;
- Sequence control;
- Restricted access;
- Privileged-access review;
- Change approval;
- Audit log;
- Physical count;
- Confirmation;
- Quality release;
- Contract compliance check;
- Vendor due diligence;
- Customer credit control;
- Data-quality validation;
- Backup and recovery testing;
- Root-cause analysis và CAPA;
- Continuous control monitoring.

Điều chỉnh từng pattern theo:

- objective và risk;
- transaction volume và process velocity;
- organization size và operating model;
- system/data capability;
- role independence và capacity;
- legal, contractual, certification hoặc internal requirement;
- cost, customer impact, exception volume và practicality;
- evidence, resilience và testability.

Đây là candidate patterns, không là bằng chứng chúng được một standard cụ thể yêu cầu hoặc đã phổ biến trong mọi ngành. Không áp dụng cho mọi organization một cách máy móc. Không tự đặt approval threshold, review frequency, retention period hoặc configuration value. Phân biệt key-control candidate, supporting control và alternative/compensating control; chỉ đề xuất keyness sau khi link objective/risk, dependency và khả năng thay thế. Nhãn analyst không tự là phê duyệt của organization.

## 9. Quản lý copyright và quyền sử dụng

Tôn trọng copyright, license và access terms của standard, framework, contract, publication và database. Metadata công khai, quyền subscription, quyền đọc PDF hoặc repo private không tự cấp quyền ingest vào AI, tạo derivative hay tái phân phối. Kiểm tra loại quyền đối với đúng tài nguyên và mục đích sử dụng; chưa rõ thì giữ điều kiện cần kiểm tra thay vì bịa permission.

Thực hiện:

- Chỉ tóm tắt requirement hoặc principle bằng lời riêng sau khi có quyền dùng nội dung phù hợp; paraphrase không tự khắc phục một hạn chế AI-use.
- Chỉ trích phần ngắn cần thiết và dùng pinpoint citation khi quyền trích dẫn cho phép.
- Không sao chép dài standard, annex, control catalog, table, figure, questionnaire hoặc proprietary methodology.
- Không tái tạo substantial portion bằng cách chia thành nhiều đoạn trích nhỏ.
- Không đóng gói full-text, workbook, bảng taxonomy/control catalog, credential hoặc tài nguyên bên thứ ba vào skill này. Nhu cầu tái sử dụng ngoài pointer/metadata cần được xác định quyền và ủy quyền riêng, không tự mở rộng phạm vi.
- Không suy ra quyền redistribution từ quyền truy cập, subscription, bản người dùng cung cấp hoặc repository visibility.
- Ghi `copyright_or_license`, `access_status`, `ai_use_status`, `redistribution_status`, phạm vi được phép và evidence/locator tương ứng trong source record.
- Dùng official link và metadata được phép khi không có quyền xử lý nội dung chi tiết; không coi mọi metadata đều là Open data.
- Tách user-provided document khỏi authoritative-source verification; coi tài liệu đó là evidence được cung cấp, không là quyền tái cấp phép.
- Che thông tin mật của contract, policy hoặc standard license trong output ngoài scope.

Nếu cần exact wording để ra quyết định trọng yếu nhưng không có lawful access, yêu cầu người dùng hoặc qualified reviewer cung cấp/xác minh đúng clause cùng quyền xử lý phù hợp; không bịa hoặc dựa vào memory.

### Gate cho nội dung hạn chế AI-use

Với nội dung ISO chịu hạn chế đã ghi nhận trong [danh mục nguồn](external-process-control-libraries.md), giữ `ai_use_status: restricted_pending_permission` cho phần bị hạn chế cho đến khi có cơ sở quyền phù hợp được xác minh. Không tự ingest full text, xử lý bản PDF do người dùng gửi hoặc tái diễn đạt clause từ nguồn bị hạn chế chỉ vì có quyền mua/đọc. Ngoại lệ Open data phải xét đúng tài nguyên và điều kiện của nó; không mở rộng ra toàn website/framework.

Không coi một câu đồng ý của người dùng là giấy phép của bên có quyền. Khi điều kiện quyền chưa giải quyết, chỉ giữ pointer/metadata được phép, nêu giới hạn và làm phần phân tích độc lập; không đưa claim standard-derived từ nội dung chưa được phép xử lý. Đây là access gate, không thay thế kết luận pháp lý của reviewer có thẩm quyền.

## 10. Mapping source tới control và requirement

Tạo `ControlSource` hoặc mapping record với tối thiểu:

- `control_id`;
- `requirement_id` hoặc `source_id`;
- `source_type`;
- `source_name` hoặc `official_title`;
- `issuing_body`;
- `version`;
- `clause_or_reference`;
- `jurisdiction`;
- `mandatory_or_advisory`;
- `adopted_by_organization` hoặc `adoption_status`;
- `applicability` và rationale;
- `date_verified`;
- `limitations`;
- `source_reference`;
- `assumptions`;
- `confidence`;
- `review_status`.

Bổ sung `baseline_basis` (requirement, principle, practice hoặc analyst proposal), `control_objective_ids`, `candidate_control_ids` và `interpretation_rationale` khi cần cho baseline-to-control view. Field nguồn lặp trong view phải được dẫn xuất từ cùng source register, không cập nhật thành nhiều bản độc lập. Một nguồn có thể liên kết nhiều objectives/controls và một objective có thể có nhiều nguồn.

Với analyst proposal không có external baseline, không tạo source/requirement/clause giả: để external link chưa có, ghi rationale, facts được cung cấp và limitation. Với source thật, giữ source requirement → interpretation → control objective → candidate control là các bước riêng. Nguồn và keyness rationale không thay bằng chứng control hiện tại đã vận hành; current observations phải giữ layer, kỳ và evidence của chúng.

Phân biệt:

- source yêu cầu outcome/control objective;
- source mô tả một control cụ thể;
- source chỉ cung cấp framework principle;
- control do organization tự thiết kế để đáp ứng requirement;
- compensating control được chấp thuận thay cho primary approach.

Không ghi control “required by standard” nếu source chỉ nêu principle hoặc outcome. Không ghi “compliant” chỉ vì một control được mapping; đánh giá design, implementation, scope và evidence theo methodology phù hợp.

## 11. Xử lý nguồn không đủ hoặc mâu thuẫn

Khi source thiếu hoặc mâu thuẫn:

1. Ghi từng source, version, date, authority và exact point of conflict.
2. Ưu tiên authoritative current source cho mệnh đề về requirement.
3. Kiểm tra order of precedence trong law, contract hoặc internal document hierarchy.
4. Phân biệt conflict thật với khác scope, date, entity hoặc terminology.
5. Không tự chọn threshold, role hoặc control khi authority chưa rõ.
6. Ghi `To be validated`, confidence và owner của validation.
7. Escalate legal, regulatory, contractual hoặc certification interpretation trọng yếu cho qualified reviewer.

Nếu source đã superseded, chỉ dùng cho historical period phù hợp và ghi rõ status. Nếu source đang draft, không trình bày như requirement hiện hành.

| Tình huống | Cách tiếp tục | Claim phải giữ lại |
|---|---|---|
| Không có capability tra cứu hoặc chưa có nguồn hợp lệ | Dùng nội dung người dùng được phép cung cấp, hoặc đưa analyst proposal có rationale | Không gọi proposal là standard-derived, compliant hoặc fully benchmarked |
| Đọc được catalog/metadata nhưng chưa có clause/item | Giữ `overview_verified` và scope đã đọc; yêu cầu nội dung/quyền phù hợp nếu cần | Không suy một key control hoặc external process ID từ title |
| HTTP 403, cần tài khoản/quyền mới, hạn chế AI-use | Dừng phần bị ảnh hưởng, ghi access/rights và ngày; dùng nguồn hợp lệ độc lập nếu phù hợp | Không vượt chặn, tìm mirror, dùng credentials ngoài workflow hay giả connector đã chạy |
| Baseline mandatory trọng yếu chưa thể xác minh | Nêu claim bị chặn, yêu cầu reviewer/nguồn có thẩm quyền; tiếp tục phần độc lập | Không hạ mandatory thành advisory để tuyên bố đã hoàn tất compliance |

Lỗi truy cập được ghi cho lần kiểm tra và tài nguyên cụ thể, không là kết luận nguồn bị chặn vĩnh viễn. Chỉ kiểm tra lại khi nhiệm vụ cần và có đường truy cập được phép; một status cũ không cho phép vượt restriction hiện tại.

## 12. Kiểm tra chất lượng

Trước khi giao output, kiểm tra:

- Mỗi proposed standard/framework control có source type, title, issuing body, version/status, pinpoint reference và date verified.
- Mỗi source có applicability rationale theo subject, jurisdiction, activity, time và adoption.
- Đã phân biệt legal/regulatory, contractual, adopted/internal và advisory status.
- Không trình bày best practice, framework recommendation hoặc industry practice như law.
- Không trình bày standard là mandatory nếu chưa có basis và scope adoption.
- Không hard-code standard version, threshold, rating, review frequency, retention period hoặc sample size.
- Đã kiểm tra amendment, supersession, withdrawal và transition từ official source khi có thể.
- Không dùng blog hoặc secondary summary làm căn cứ duy nhất cho key control.
- Scope `content_verified` có đúng clause/item đã đọc; metadata/overview không bị nâng thành baseline chi tiết.
- `date_checked`/`date_verified` không được tự cấp từ ngày chạy, ngày build hoặc snapshot trong skill nếu chưa thực hiện kiểm tra tương ứng.
- Access, AI-use và redistribution được ghi riêng; source bị hạn chế được xử lý đúng gate, không suy quyền từ public/free/private.
- Không sao chép dài, bundle tài nguyên bên thứ ba hoặc tái phân phối nội dung ngoài quyền được xác minh.
- Taxonomy/notation/vendor blueprint được dùng đúng vai trò; external IDs chỉ đến từ nội dung đã đọc và không giả làm workflow/current state.
- Chỉ mô tả tool/source retrieval thực sự đã dùng; không nói connector đã cài, đang hoạt động hoặc đã đọc toàn thư viện.
- Source ID, requirement ID và control ID tie out với source register, RCM và control library.
- Mọi limitation, unavailable text, unverified status, assumption và confidence được nêu rõ.
- Output của skill dừng ở draft compliance/certification mapping, issue/gap analysis và handoff. Mọi formal compliance conclusion, legal interpretation hoặc certification decision phải do Legal, Compliance, certification body hoặc authority có thẩm quyền phát hành.
