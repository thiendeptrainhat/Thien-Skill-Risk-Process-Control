<p align="center">
  <img src="skills/thien-skill-risk-control-process/assets/logo-1100.png" alt="Logo TDTN" width="220">
</p>

# Thien-Skill-Risk-Control-Process

Skill phân tích và tư vấn một hoặc nhiều quy trình từ chat, PDF, Word, SOP và bằng chứng liên quan: xác định E2E phù hợp, risks, expected/current controls, gaps, cải tiến và rủi ro nếu giữ nguyên.

Một skill lõi, không giới hạn ở một nhóm E2E cố định. Ba gói Claude, ChatGPT và Universal dùng chung nội dung nghiệp vụ; khác wrapper thư mục và metadata nền tảng.

## Vai trò của skill

Skill là trợ lý phân tích quy trình, rủi ro và thiết kế kiểm soát: giúp đọc hiểu một quy trình đang có, tư vấn quy trình mới hoặc xem xét một nhóm quy trình liên kết từ đầu đến cuối.

Giá trị chính là nối **mục tiêu kinh doanh → quy trình E2E → risks → expected/current controls → gaps → cải tiến và rủi ro nếu giữ nguyên**, kèm nguồn và giới hạn bằng chứng. Skill hỗ trợ người sở hữu quy trình, quản lý rủi ro, kiểm soát nội bộ và kiểm toán ra quyết định; không tự phê duyệt SOP, thay người có thẩm quyền hoặc phát hành ý kiến bảo đảm.

Với tài liệu khó đọc, Risk-Control-Process phụ trách diễn giải nghiệp vụ; Document-Evidence có thể hỗ trợ trích xuất và truy nguyên khi khả dụng, được phép và thực sự cần. Không phải cài một bộ OCR mới để dùng skill cho mọi câu hỏi.

## Skill giúp trả lời bảy câu hỏi gì?

| Mục tiêu | Kết quả hỗ trợ quyết định |
|---|---|
| R01 — Nên thiết kế theo E2E nào? | Objective, trigger, outcome, boundary; một hoặc nhiều mapping candidates, nguồn và rationale. Có thể trả “chưa đủ cơ sở để ánh xạ”, không ép tên process vào danh mục |
| R02 — Có risks nào? | Cause → Event → Impact → Objective, gắn với process/step; phân biệt dữ kiện, suy luận và kịch bản có thể xảy ra |
| R03 — Expected/key controls là gì? | Control objective, baseline source/locator, applicability, mandatory/advisory và candidate controls; keyness có rationale, không đồng nghĩa tổ chức đã phê duyệt |
| R04 — Current controls thực sự biết được là gì? | Giữ riêng documented, designed và evidenced-performed observations cùng nguồn, kỳ, scope và giới hạn đọc tài liệu |
| R05 — Gap nằm ở đâu? | So theo objective, coverage, timing, precision, independence, evidence và dependency; xét alternative/compensating controls, không chỉ so tên |
| R06 — Nên cải tiến thế nào? | Options, lợi ích, trade-offs, dependency, tính khả thi, thông tin cần xác nhận và approval; greenfield có thể đề xuất mà không tạo fake gap |
| R07 — Không cải tiến thì sao? | No-change scenario, cause/event/impact, existing protection, exposure còn lại, uncertainty và validation needed; không bịa probability, loss hoặc time horizon |

Đây là phạm vi thiết kế của skill, không phải cam kết mọi câu hỏi đều có đủ dữ liệu hoặc nguồn để kết luận. Câu hỏi hẹp chỉ cần các phần liên quan; engagement đầy đủ cần trả lời và nêu giới hạn cho cả bảy mục tiêu.

## Lợi ích và tính năng khi kích hoạt

### 1. Phạm vi E2E mở, không bị khóa vào 94 profiles

94 profiles là điểm bắt đầu để discovery, không phải danh sách đầy đủ. Skill xem business outcome và ranh giới thực tế trước khi chọn tên; một SOP có thể chỉ là subprocess của E2E lớn hơn, hoặc giao nhiều E2E.

Khi cần tham khảo ngoài seeds, skill hướng dẫn tra cứu nguồn phù hợp bằng capability thực sự được phép: taxonomy, process reference model, vendor blueprint, control framework hoặc notation. APQC taxonomy không tự là thứ tự workflow; vendor blueprint không tự là yêu cầu kiểm soát bắt buộc.

Catalog đi kèm là các đầu mối/metadata có ngày quan sát, không phải kho full-text đã nạp hay connector đã kết nối. Không có web hoặc thiếu quyền đọc nguồn thì vẫn có thể đưa design proposal có nhãn; không gọi proposal đó là standard-derived hay compliant. Xem [external library guide](skills/thien-skill-risk-control-process/references/external-process-control-libraries.md).

### 2. Phân biệt tài liệu, thiết kế và thực tế vận hành

| Lớp | Ý nghĩa |
|---|---|
| `As-Documented` | Tài liệu thực sự mô tả gì |
| `As-Designed` | Thiết kế hiện trạng được nguồn phù hợp xác nhận |
| `As-Performed` | Việc thực hiện được evidence hỗ trợ trong đúng case/kỳ/phạm vi |
| `Target-State` | Phương án tương lai được đề xuất |

Ví dụ: SOP yêu cầu hai cấp duyệt nhưng log một giao dịch chỉ có một cấp. Skill giữ hai observations riêng, liên kết cùng logical control khi có căn cứ; không sửa mô tả SOP theo log và không suy kết luận cho cả kỳ từ một giao dịch.

### 3. Baseline controls có căn cứ, gap không máy móc

Skill tách requirement hoặc principle của nguồn khỏi cách triển khai do analyst đề xuất. Một control trong thư viện không tự là key control; cần xét significant risk, obligation, dependency và khả năng thay thế trong bối cảnh cụ thể.

“Không thấy control trong SOP đã đọc” không đồng nghĩa control không tồn tại. Documentation gap, design gap, evidence limitation, operating deviation và compliance gap được phân biệt. Compliance gap cần mandatory baseline đã xác minh; khác tên hoặc manual/automated chưa đủ để kết luận deficiency.

### 4. Cải tiến có lựa chọn và no-change exposure

Khi có trade-off đáng kể, skill so sánh phương án kiểm soát tối thiểu, cân bằng và nâng cao theo lợi ích, rủi ro, chi phí, công nghệ, con người và dependency. Nhãn **Minimum compliant** chỉ dùng khi mandatory baseline đã được xác minh và đối chiếu; nếu chưa đủ thì dùng **Minimum-control proposal — compliance unverified**.

Với material gap, phần “nếu giữ nguyên” làm rõ nguy cơ và protection còn có. Nếu mới là hypothesis hoặc thiết kế mới, skill giữ đúng nhãn đó, không biến tương lai thành sự cố đã xảy ra.

### 5. Một chuỗi dữ liệu truy nguyên

`Objective → Process → Risk → Control objective → Baseline / Control observations → Comparison → Gap hoặc Design opportunity → Recommendation / Action`

Logical control ID được tái sử dụng qua nhiều process/risks; mỗi observation có layer, scope, kỳ và nguồn riêng. Comparison, RCM và action views tham chiếu cùng IDs, giúp đối chiếu kết luận và giữ conflict.

Contract `1.1.0` bổ sung fields/objects khi đọc output `1.0.0`, giữ IDs, facts, null, locators và `design_assessment`; không tự nâng record cũ thành performed hoặc verified. Đây không phải bảo đảm mọi consumer strict-schema `1.0.0` đọc được fields mới.

### 6. Đọc đầu vào linh hoạt, không nhân bản OCR

Chat và PDF/Word đọc được có thể phân tích bằng capability của host. Scan, bảng/sơ đồ khó hoặc provenance chưa đủ có thể cần **Thien-Skill-Document-Evidence**, nhưng đây là handoff tùy chọn, không phải dependency bắt buộc cho mọi task.

Risk-Control-Process sở hữu diễn giải process/risk/control; Document-Evidence sở hữu extraction/integrity/provenance. Handoff giữ locators, coverage, warnings, review status và điều kiện quyền sử dụng liên quan. Extraction verified không chứng minh control đã vận hành hiệu quả. Skill không bổ sung OCR engine, tự cài specialist hay giả rằng specialist đã chạy.

### 7. Các năng lực hỗ trợ khác

| Nhóm | Khả năng trong phạm vi được giao |
|---|---|
| Document analysis | Phân tích policy/SOP, approval matrix, exceptions và mâu thuẫn giữa tài liệu |
| Architecture và workflow | L0–L5, SIPOC, step register, RACI, handoff, decision routes, Mermaid/BPMN conceptual |
| RCM | Risk-centric, control-centric, requirement-centric, audit-test và baseline–current–gap views |
| SoD | Tách process-role, system-access và actual-user; không kết luận actual conflict từ role design đơn thuần |
| SPOF/dependency | Backup, capacity, substitute, lead time, common-mode failure và evidence; unique owner chưa tự là SPOF |
| Metrics | Phân biệt KPI/KRI/KCI, giữ methodology và basis cho target/threshold |
| Audit support | Walkthrough, evidence request, test attributes và draft handoff; không phát hành audit opinion |
| Assessment/training | Assessment theo methodology được duyệt; workshop, simulation và case có nhãn synthetic khi phù hợp |

Các mode: `document-analysis`, `current-state-discovery`, `risk-control-analysis`, `target-state-design`, `rcm`, `sod`, `spof-dependency`, `audit-support`, `advisory`, `assessment`, `training`.

References được nạp theo nhu cầu. Khung 14 bước dành cho engagement đầy đủ; không ép một câu hỏi nhỏ phải tạo toàn bộ templates.

## Cách sử dụng skill

### 1. Gọi skill và giao đúng phạm vi

Sau khi host đã nhận diện skill, chọn hoặc gọi **Thien-Skill-Risk-Control-Process** bằng cơ chế của nền tảng. Nếu chưa cài, xem [phần cài đặt bên dưới](#cài-đặt). Không dùng lời tự nhận “đã kích hoạt” của model làm bằng chứng duy nhất về phiên bản được nạp.

Cho biết bạn muốn đọc/đánh giá quy trình hiện có, thiết kế quy trình mới, phân tích một nhóm E2E hay chỉ xử lý một vấn đề hẹp. Không cần yêu cầu toàn bộ bộ hồ sơ khi chỉ muốn xem một gap.

### 2. Cung cấp đầu vào và mục đích

Gửi nội dung qua chat hoặc đính kèm PDF/Word/SOP mà bạn được phép xử lý trong AI. Nếu có, bổ sung mục tiêu kinh doanh, trigger/outcome, đơn vị/phạm vi, thời kỳ, hệ thống, approval matrix, baseline được áp dụng và bằng chứng vận hành.

Thông tin chưa có có thể ghi “chưa cung cấp”. Skill cần chỉ ra phần nào chưa đủ căn cứ và hỏi dữ kiện làm thay đổi trọng yếu kết luận; không tự đặt owner, ngưỡng, deadline hoặc mức chấp nhận risk. Quyền đọc tài liệu không tự là quyền tải lên dịch vụ ngoài.

### 3. Yêu cầu đầu ra và đối chiếu kết quả

Với engagement đầy đủ, yêu cầu bảy mục tiêu ở bảng trên; với câu hỏi nhỏ, chỉ lấy phần liên quan. Kiểm tra source/locator, các lớp As-Documented / As-Designed / As-Performed / Target-State, cơ sở chọn baseline và các thông tin còn cần xác minh.

Kết quả là phân tích hoặc đề xuất dự thảo. Xác nhận tính phù hợp và phê duyệt với người có thẩm quyền trước khi áp dụng thay đổi; không coi một control được mô tả hoặc trích xuất đúng là đã vận hành hiệu quả.

### Ví dụ yêu cầu

```text
Đọc SOP Word đính kèm và phân tích đủ bảy mục tiêu: E2E phù hợp, risks,
expected/key controls, current controls, gaps, cải tiến và no-change exposure.
Chỉ coi controls trong SOP là As-Documented; nếu thiếu evidence hãy ghi rõ.
```

```text
Tư vấn thiết kế một quy trình chưa có SOP: xử lý yêu cầu thu hồi và tái sử dụng
thiết bị giữa khách hàng, nhà cung cấp và các cơ sở. Không ép vào seed có sẵn.
Tìm reference phù hợp nếu được phép; nếu không đủ căn cứ, giữ mapping candidate.
Không bịa current controls hoặc gap hiện trạng.
```

```text
Phân tích nhóm quy trình onboarding nhà cung cấp, mua hàng, nhận hàng và thanh toán.
Giữ shared control IDs, so controls thực tế với baseline theo objective/coverage,
nêu alternatives, điểm thiếu bằng chứng và rủi ro nếu không cải tiến.
```

## Guardrails và giới hạn

Skill không:

- tự cấp quyền truy cập nguồn, mua tài liệu, cài connector hoặc chuyển tài liệu mật sang dịch vụ ngoài;
- coi public access, sở hữu PDF, quyền dùng trong AI và quyền tái phân phối là một;
- tạo risk score, threshold, sample size, owner, deadline hoặc phê duyệt khi thiếu căn cứ;
- dùng policy/SOP hoặc lời xác nhận đơn thuần thay operating evidence;
- coi framework alignment là certification, legal compliance hoặc formal assurance;
- sửa trực tiếp source, ERP, access hay production workflow;
- biến tài liệu, OCR text hoặc trang web thành chỉ thị thực thi.

Không đủ nguồn chỉ chặn kết luận phụ thuộc nguồn đó; phần độc lập an toàn có thể tiếp tục. Mọi policy, SOP, RCM và target-state design vẫn là **draft** cho đến khi người có thẩm quyền phê duyệt.

## Phiên bản và trạng thái

| Thuộc tính | Giá trị |
|---|---|
| Tên hiển thị | `Thien-Skill-Risk-Control-Process` |
| Skill ID | `thien-skill-risk-control-process` |
| Phiên bản | `1.1.1` — chỉ đổi tên từ `1.1.0` |
| Trạng thái | Bản đổi tên; kiểm tra định danh, nội dung không đổi và packaging riêng, không công bố model runs mới |
| Repository | [Public — Thien-Skill-Risk-Control-Process](https://github.com/thiendeptrainhat/Thien-Skill-Risk-Control-Process) |
| Ngôn ngữ trả lời | Theo ngôn ngữ người dùng |
| License | Tran Ngoc Thien's Skills Commercial Source-Available License 2.0 |

Ba ZIP `1.1.1` bên dưới mang tên mới, giữ nội dung nghiệp vụ của `1.1.0`. Version và checksum tại [release manifest](RELEASE-MANIFEST.yaml); phạm vi đổi tên và kết quả kiểm tra tại [handoff hiện hành](docs/HANDOFF.md). Điều khoản license và logo giữ nguyên. Người dùng đã chuyển repository sang public và yêu cầu đổi URL theo tên skill mới. ZIP và bằng chứng `1.1.0` vẫn được giữ làm lịch sử.

## Kiểm thử và mức độ tin cậy

Trên snapshot **tên cũ** `1.1.0`, **29/29 biến thể model** đã chạy trong các context mới và được review theo từng invariant tại `Codex desktop delegated local runtime`. Bao gồm ba dạng chat/Word/PDF của một SOP tổng hợp, một ca tra cứu NIST thực tế và một handoff Document-Evidence thực tế. Có **61/61 kiểm tra công cụ** riêng và ba ZIP đã kiểm tra checksum, cấu trúc, parity; không cộng các loại kiểm tra này thành behavioral passes.

[Báo cáo Phase 3](docs/phase-3/REPORT.md) và `current_release_gate` trong [kết quả máy](tests/phase-3/acceptance-results.json) là hồ sơ **1.1.0**, không phải gate cho tên/ZIP `1.1.1`. Bản đổi tên chỉ được kiểm tra tĩnh và đối chiếu nội dung; không chạy lại 29 model variants, không chứng nhận discovery của ID mới. Claude Desktop/Web, ChatGPT Desktop/Web và cài đặt/discovery thực tế vẫn **not_run**. Kết quả trên dữ liệu tổng hợp không bảo đảm mọi quy trình, tài liệu hoặc mô hình đều đạt.

Tách riêng structural checks, deterministic invariants, model behavioral runs và live-platform acceptance. ZIP hợp lệ, schema đọc được hoặc docs có hướng dẫn cài không chứng minh behavior đã đạt trên Claude/ChatGPT/Codex.

Đọc hồ sơ lịch sử tại [cây Git trước đổi tên](https://github.com/thiendeptrainhat/Thien-Skill-Risk-Control-Process/tree/db9b0f42c1a2ce0938abc888a03699d401b9fd41) để các đường dẫn tương đối đúng phiên bản, gồm [Phase 3 test records](tests/phase-3/README.md) và [platform evidence](docs/phase-3/PLATFORM-GUIDANCE.md). [Acceptance report 1.0.0](tests/acceptance-report.md) và [behavioral report 1.0.0](tests/behavioral-report.md) chỉ là lịch sử: 104 registry cases và 28 provisional cases không được cộng thành behavioral passes của 1.1.0 hay 1.1.1. Luôn đối chiếu version, ngày, scope và giới hạn của từng kết quả.

## Cài đặt

> [!IMPORTANT]
> GitHub lưu mã nguồn và ZIP, không kích hoạt skill trong tài khoản AI. Tải ZIP, đặt file đúng chỗ, được nền tảng nhận diện và kiểm thử tác vụ là những bước khác nhau. Tên gói “ChatGPT” hoặc “Universal” không bảo đảm mọi bề mặt nhận ZIP trực tiếp.

### Chọn đúng ZIP

| Gói | Bên trong ZIP | Dùng như thế nào |
|---|---|---|
| [Claude ZIP](dist/1.1.1/Thien-Skill-Risk-Control-Process-v1.1.1-Claude.zip) | `thien-skill-risk-control-process/` | Upload custom skill trong Claude; hoặc giải nén cho Claude Code |
| [ChatGPT ZIP](dist/1.1.1/Thien-Skill-Risk-Control-Process-v1.1.1-ChatGPT.zip) | Thư mục skill, có `agents/openai.yaml` | Gói thư mục không có wrapper `.agents`; dùng cho local discovery phù hợp, không mặc định là ZIP importer của ChatGPT |
| [Universal ZIP](dist/1.1.1/Thien-Skill-Risk-Control-Process-v1.1.1-Universal.zip) | `.agents/skills/thien-skill-risk-control-process/` | Gói giải nén `.agents` đã chọn cho môi trường local; xem điều kiện riêng của ChatGPT Desktop |

Không cần cài cả ba gói vào cùng một môi trường. Chúng không phải ba skill khác nhau, plugin, OCR engine hay bộ connector.

### Tải và kiểm tra

1. Trong repository public, mở [`dist/1.1.1/`](dist/1.1.1/) và tải đúng ZIP cùng checksum của phiên bản đó. ZIP từ **Code > Download ZIP** là toàn repository, không phải gói upload Claude.
2. Đọc [license và quyền sử dụng](#license-và-quyền-sử-dụng), xem nội dung ZIP trước khi cài.
3. Nếu có đủ ba gói trong cùng thư mục với `SHA256SUMS`, chạy kiểm tra sau trên macOS:

```bash
cd /path/to/downloaded-packages
shasum -a 256 -c SHA256SUMS
```

Nếu chỉ tải một gói, tính SHA-256 của file đó rồi so với đúng dòng trong checksum/manifest. Hash trùng chỉ xác nhận file khớp bản phát hành, không chứng minh chất lượng phân tích hay quyền dùng nội dung bên trong.

### Đi theo bề mặt đang dùng

| Bề mặt | Hướng dẫn |
|---|---|
| Claude Web / Claude Desktop có Custom Skills | Upload nguyên Claude ZIP qua mục Skills, bật skill; [các bước](INSTALL.md#2-claude-web-và-claude-desktop) |
| Codex local: desktop, CLI, IDE | Universal ZIP → project root; hoặc ChatGPT ZIP → thư mục personal skills; [các bước](INSTALL.md#3-codex-local) |
| ChatGPT Desktop | Giữ phương án Universal `.agents`; xác nhận host thực sự nhận skill, không suy khả năng import từ tên ZIP; [điều kiện](INSTALL.md#4-chatgpt-desktop) |
| ChatGPT Web | Chưa có quy trình native import ba ZIP này được xác minh; không xem upload file vào chat là cài skill; [giới hạn](INSTALL.md#5-chatgpt-web) |
| Claude Code | Dùng Claude ZIP, không dùng wrapper `.agents`; [các bước](INSTALL.md#6-claude-code) |

Hướng dẫn được đối chiếu ngày **28/08/2026** với [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills) và [Claude — Use skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude), không phải kết quả cài thử trên tài khoản. Bằng chứng từng nền tảng và giới hạn được ghi tại [Platform guidance](docs/phase-3/PLATFORM-GUIDANCE.md).

### Xác nhận sau khi cài

Kiểm tra skill xuất hiện trong danh sách của host và có bằng chứng nạp đúng file/phiên bản nếu host cung cấp. Trong ChatGPT, chọn skill bằng `@`; Codex dùng `$` hoặc `/skills`. Không coi lời tự nhận “đã dùng skill” của model là bằng chứng duy nhất. [OpenAI — Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins).

Prompt thử, dùng dữ liệu không nhạy cảm:

```text
Hãy dùng Thien-Skill-Risk-Control-Process để phân tích quy trình dưới đây.
Xác định objective, trigger, outcome, E2E candidate và điểm chưa đủ cơ sở.
Tách control được mô tả khỏi control có evidence vận hành.
Chỉ hỏi thông tin còn thiếu làm thay đổi trọng yếu kết luận; không tự đặt score.
```

Xem [INSTALL.md](INSTALL.md) để tránh giải nén lồng thư mục, xử lý bản cũ và kiểm tra từng bề mặt. Smoke check này không thay thế behavioral testing đầy đủ.

## Cập nhật phiên bản đã cài

Bản `1.1.1` đổi ID từ `thien-skill-risk-process-control` sang `thien-skill-risk-control-process`. Sau khi sao lưu tùy chỉnh, dùng cơ chế của host để thay/tắt bản cũ rồi cài đúng một bản mới; không giữ cả hai ID cùng kích hoạt. Chưa có thao tác cài đặt hoặc tự đổi bản đã cài trong lần đổi tên này.

Tải đúng ZIP/version mới, kiểm tra checksum, giữ bản sao tùy chỉnh cũ ngoài thư mục discovery rồi cập nhật đúng một vị trí cài. Không trộn file cũ/mới hoặc cài đồng thời nhiều bản cùng skill ID. Xem [quy trình cập nhật](INSTALL.md#8-cập-nhật-và-gỡ-lỗi).

GitHub không tự cập nhật các bản đã upload hoặc giải nén; phải dùng cơ chế cập nhật của host và kiểm tra lại bản thực sự được nạp.

## License và quyền sử dụng

Repository hiện public; trạng thái hiển thị này không thay điều khoản license. URL cũ và nhãn PRIVATE trong `LICENSE-APPLICATION.md`/ZIP là metadata tại thời điểm tạo gói trước thay đổi repository; giữ nguyên các bản đó để bảo toàn checksum. URL và trạng thái hiện hành nằm trong [release manifest](RELEASE-MANIFEST.yaml).

Đọc đầy đủ:

- [LICENSE](LICENSE)
- [LICENSE-APPLICATION.md](LICENSE-APPLICATION.md)
- [NOTICE](NOTICE)
- [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)

Việc có quyền truy cập repository, tải ZIP hoặc cài đặt thành công **không tự động cấp quyền sử dụng, sửa đổi hoặc phân phối**. Bản tiếng Việt của license được ưu tiên khi có khác biệt hoặc mâu thuẫn; pháp luật Việt Nam và tòa án có thẩm quyền tại Việt Nam được áp dụng theo nội dung license.

## Tài liệu trong repository

- [Handoff dự án và trạng thái bàn giao](docs/HANDOFF.md)
- [Báo cáo nghiệm thu Phase 3 — lịch sử 1.1.0](docs/phase-3/REPORT.md)
- [Hướng dẫn cài đặt](INSTALL.md)
- [Bằng chứng hướng dẫn nền tảng — 28/08/2026](docs/phase-3/PLATFORM-GUIDANCE.md)
- [Canonical SKILL.md](skills/thien-skill-risk-control-process/SKILL.md)
- [External process/control libraries](skills/thien-skill-risk-control-process/references/external-process-control-libraries.md)
- [Common data model và QA](skills/thien-skill-risk-control-process/references/data-model-qa-execution.md)
- [Requirement coverage matrix](skills/thien-skill-risk-control-process/references/requirement-coverage-matrix.md)
- [Source provenance](skills/thien-skill-risk-control-process/references/source-skill-inventory.md)
