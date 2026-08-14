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

Áp dụng module này khi người dùng yêu cầu best practice, global standard, industry standard, regulatory control, compliance mapping, certification mapping hoặc source của một control.

Thực hiện các nguyên tắc sau:

- Xác minh source hiện hành tại thời điểm thực hiện công việc; không hard-code version như thể luôn hiện hành.
- Ưu tiên nguồn chính thức và văn bản gốc.
- Tách tính có thẩm quyền của source khỏi applicability cho organization/process cụ thể.
- Phân biệt legal/regulatory obligation, contractual obligation, adopted standard, framework recommendation, industry practice và organization preference.
- Không dùng cụm “global standard control” nếu chưa nêu source, clause, status và applicability.
- Không dùng blog, bài viết hoặc AI summary làm căn cứ duy nhất cho control trọng yếu.
- Không biến best practice hoặc framework recommendation thành legal requirement.
- Không sao chép dài standard, framework, publication hoặc tài liệu có bản quyền.
- Ghi source, version/status, clause/reference, verification date, limitations và confidence cho mỗi proposed control.
- Khi không thể xác minh nguồn hiện hành hoặc nội dung trả phí, ghi giới hạn và yêu cầu human verification.

## 2. Phân loại control source

Phân loại mỗi source vào một nhóm chính và ghi nhóm phụ khi cần:

1. `Mandatory law or regulation`: law, regulation, binding rule hoặc quyết định có hiệu lực trong jurisdiction và scope áp dụng.
2. `Regulatory guidance`: guidance, circular, supervisory expectation, FAQ hoặc interpretive material của regulator; xác định riêng mức ràng buộc.
3. `Contractual requirement`: obligation từ contract, covenant, customer term, supplier term hoặc service agreement có hiệu lực.
4. `Adopted or certified standard requirement`: requirement của standard mà organization đã adopt, cam kết hoặc dùng cho certification scope.
5. `Recognized framework-aligned control`: control hoặc principle được mapping với recognized framework nhưng không tự bắt buộc.
6. `Industry common practice`: practice được sử dụng phổ biến trong industry phù hợp.
7. `Leading practice`: practice nâng cao có thể vượt common practice và cần đánh giá feasibility.
8. `Organization-specific control`: control do policy, risk appetite, governance hoặc design decision nội bộ tạo ra.
9. `Compensating control`: control thay thế hoặc giảm exposure khi primary requirement/control không thể đáp ứng theo cách ban đầu.

Không dùng `Compensating control` để che giấu non-compliance. Xác minh requirement có cho phép alternative hoặc compensating approach không và ai có authority phê duyệt.

## 3. Lập source record

Tạo một source register record với tối thiểu các field sau:

| Field | Cách ghi |
|---|---|
| `source_id` | Gán ID ổn định và duy nhất. |
| `source_type` | Chọn taxonomy tại Mục 2. |
| `source_name` | Ghi tên dùng trong mapping. |
| `official_title` | Ghi title chính thức theo nguồn gốc. |
| `issuing_body` | Ghi cơ quan, standards body, contracting party hoặc policy owner. |
| `version` | Ghi edition/version được xác minh hoặc `To be validated`; không hard-code. |
| `publication_date` | Ghi ngày publication nếu có nguồn. |
| `effective_date` | Ghi ngày có hiệu lực; phân biệt với publication date. |
| `source_status` | Ghi current, amended, superseded, withdrawn, draft, transitional hoặc chưa xác minh theo source chính thức. |
| `clause_or_reference` | Ghi article, clause, control, section hoặc pinpoint reference. |
| `jurisdiction` | Ghi lãnh thổ/phạm vi pháp lý; dùng `Not applicable` cho source không theo jurisdiction khi phù hợp. |
| `mandatory_or_advisory` | Ghi legal/regulatory, contractual, adopted/internal hoặc advisory status; tránh nhãn nhị phân thiếu context. |
| `adopted_by_organization` | Ghi evidence adoption, certification hoặc internal approval. |
| `adoption_status` | Ghi adopted, partially adopted, planned, not adopted hoặc `To be validated`. |
| `applicability` | Ghi kết luận và rationale theo Mục 5. |
| `date_verified` | Ghi ngày kiểm tra source và status. |
| `official_location` | Ghi official URL, gazette, standards catalog, contract repository hoặc controlled policy location. |
| `language` | Ghi official language và status của translation. |
| `copyright_or_license` | Ghi restriction về access, quotation, reproduction và redistribution. |
| `limitations` | Ghi scope exclusion, transition, unavailable text hoặc interpretive uncertainty. |
| `verification_evidence` | Liên kết screenshot, metadata, publication notice hoặc controlled record được phép lưu. |
| `owner_or_reviewer` | Ghi role chịu trách nhiệm xác minh applicability khi cần. |
| `confidence` | Dùng confidence scale được định nghĩa cho engagement. |

Không dùng `version` của source làm version của skill, control hoặc policy. Không coi source record là bằng chứng organization đã adopt standard nếu thiếu adoption evidence.

## 4. Xác minh nguồn hiện hành

Thực hiện protocol sau tại thời điểm dùng source:

1. Mở official publisher, regulator, gazette, standards body, framework owner, contract repository hoặc controlled company source.
2. Xác minh official title, issuing body, publication date, effective date và identifier.
3. Xác minh current edition/version, amendment, addendum, corrigendum, interpretation, supersession, withdrawal và transition.
4. Xác minh jurisdiction, effective period, covered subject, activity, entity, product, process và exceptions.
5. Xác minh translation có phải official/authorized không; ưu tiên authoritative text khi có conflict.
6. Ghi `date_verified`, official location và evidence of status.
7. Đối chiếu secondary source chỉ để bổ sung context hoặc tìm official source.
8. Nếu không truy cập được authoritative text, ghi `Current status not verified` và không đưa kết luận dứt khoát phụ thuộc source.

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

Không coi `Not applicable` là miễn mọi related obligation. Ghi source hoặc criterion hỗ trợ kết luận. Chuyển legal interpretation trọng yếu cho qualified legal/compliance reviewer.

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

Xem xét các source family sau khi phù hợp; xác minh edition/version và applicability mỗi lần sử dụng:

- COSO Internal Control và COSO ERM;
- ISO 31000;
- ISO 9001;
- ISO 14001;
- ISO 45001;
- ISO 22301;
- ISO/IEC 27001 và ISO/IEC 27002;
- ISO 37301;
- COBIT;
- NIST frameworks;
- IIA Global Internal Audit Standards;
- OECD guidance;
- APQC Process Classification Framework;
- BPMN;
- industry-specific regulations;
- applicable accounting standards;
- applicable legal requirements;
- internal company standards.

Không trình bày danh sách này như source bắt buộc hoặc hiện hành mặc định. Chỉ chọn source liên quan tới objective, risk, industry, jurisdiction, adoption và use case.

Khi mapping source:

1. Trích requirement/principle ở mức cần thiết.
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

Không áp dụng pattern cho mọi organization một cách máy móc. Không tự đặt approval threshold, review frequency, retention period hoặc configuration value. Không kết luận pattern là key control trước khi thực hiện key-control rationale.

## 9. Quản lý copyright và quyền sử dụng

Tôn trọng copyright, license và access terms của standard, framework, contract, publication và database.

Thực hiện:

- Tóm tắt requirement hoặc principle bằng lời riêng.
- Chỉ trích phần ngắn cần thiết và dùng pinpoint citation khi quyền trích dẫn cho phép.
- Không sao chép dài standard, annex, control catalog, table, figure, questionnaire hoặc proprietary methodology.
- Không tái tạo substantial portion bằng cách chia thành nhiều đoạn trích nhỏ.
- Không đưa full-text standard trả phí vào skill, template, report hoặc shared repository nếu chưa có quyền.
- Không suy ra quyền redistribution từ quyền truy cập, subscription, bản người dùng cung cấp hoặc repository visibility.
- Ghi `copyright_or_license`, access limitation và permitted use trong source record.
- Dùng official link/catalog metadata khi không được phép lưu nội dung.
- Tách user-provided document khỏi authoritative-source verification; coi tài liệu đó là evidence được cung cấp, không là quyền tái cấp phép.
- Che thông tin mật của contract, policy hoặc standard license trong output ngoài scope.

Nếu cần exact wording để ra quyết định trọng yếu nhưng không có lawful access, yêu cầu người dùng hoặc qualified reviewer cung cấp/xác minh đúng clause; không bịa hoặc dựa vào memory.

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
- Không sao chép dài hoặc tái phân phối nội dung có bản quyền.
- Source ID, requirement ID và control ID tie out với source register, RCM và control library.
- Mọi limitation, unavailable text, unverified status, assumption và confidence được nêu rõ.
- Output của skill dừng ở draft compliance/certification mapping, issue/gap analysis và handoff. Mọi formal compliance conclusion, legal interpretation hoặc certification decision phải do Legal, Compliance, certification body hoặc authority có thẩm quyền phát hành.
