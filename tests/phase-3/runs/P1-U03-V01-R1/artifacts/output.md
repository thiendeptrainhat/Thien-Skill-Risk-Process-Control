# E2E, giao điểm và kiểm soát dùng chung

Nhóm này nên được đọc như **một E2E thu hồi liên kết với ba luồng có boundary riêng**, không phải một chuỗi chỉ thuộc một phòng ban. **CTL-REC-07 là một logical control với ba điểm sử dụng**, không phải ba kiểm soát khác nhau.

Đây là bản phân tích dự thảo, `review_status: Not reviewed`. Tên E2E và mã mới dưới đây là định danh nội bộ để tái sử dụng; giữ nguyên mã nguồn và `CTL-REC-07`. Không gán mã thư viện ngoài hay cấp L0–L5 chưa được xác nhận. Dữ liệu nguồn ghi: “DỮ LIỆU TỔNG HỢP; được phép phân tích trong AI.”

## 1. Objective và boundary E2E

`OBJ-REC-01`: xử lý lô cần thu hồi, giải quyết khách hàng và theo dõi hành động nhà cung cấp. Nguồn: SRC-RECALL-03 §1.

Các dòng sau thuộc `As-Documented`: tái cấu trúc mô tả được cung cấp, chưa xác nhận toàn bộ vận hành.

| ID ổn định | E2E nội bộ | Trigger → điểm kết thúc | Vai trò trong nhóm |
|---|---|---|---|
| E2E-REC-01 | Xác nhận thu hồi → giải quyết hồ sơ thu hồi | Quality xác nhận lô cần thu hồi → lô được xử lý, khách hàng được giải quyết, hành động nhà cung cấp được theo dõi | E2E chính của hồ sơ; xuyên qua thông báo, khóa xuất, trả hàng, hoàn tiền và phản hồi nhà cung cấp. §1 |
| E2E-RET-01 | Yêu cầu trả → tiếp nhận/xác định cách xử lý hàng | Yêu cầu trả → nhận/xác định cách xử lý hàng | Boundary riêng, giao với thu hồi qua hàng trả; không tự bao gồm hoàn tiền. §2 |
| E2E-REF-01 | Yêu cầu hoàn tiền được chấp thuận → đối chiếu tiền/công nợ | Yêu cầu được chấp thuận → tiền và sổ công nợ được đối chiếu | Giao với thu hồi qua giải quyết khách hàng; không kết thúc chỉ vì đã duyệt hoặc đã chi tiền. §2 |
| E2E-SUP-01 | Yêu cầu nguyên nhân → chấp thuận phản hồi/hành động | Yêu cầu nhà cung cấp phản hồi nguyên nhân → phản hồi và hành động được chấp thuận | Giao với thu hồi qua nguyên nhân và hành động; “được chấp thuận” không chứng minh hành động đã hoàn tất hoặc có hiệu quả. §1–§2 |

Quality chỉ được nguồn xác định là bên xác nhận lô cần thu hồi; chưa đủ căn cứ gán Quality làm owner của toàn bộ E2E hay control. Owner, version và hiệu lực tài liệu: `Not provided`. Confidence của trích xuất boundary: `Medium — Documented`, dựa trên một nguồn tổng hợp, chưa được corroborate.

## 2. Các điểm giao nhau

Dùng quan hệ nhiều–nhiều thay vì ép ba luồng phụ thành các nhánh cha–con độc quyền.

| Relationship ID | from_id → to_id | Quan hệ và ranh giới cần giữ |
|---|---|---|
| MAP-REC-RET | E2E-REC-01 → E2E-RET-01 | `overlaps_via_return_handling`: xử lý lô thu hồi giao với yêu cầu trả và kết quả tiếp nhận/cách xử lý. Nguồn §1–§2. |
| MAP-REC-REF | E2E-REC-01 → E2E-REF-01 | `overlaps_via_customer_refund`: giải quyết khách hàng giao với luồng hoàn tiền; đối chiếu tiền/công nợ vẫn có boundary riêng. Nguồn §1–§2. |
| MAP-REC-SUP | E2E-REC-01 → E2E-SUP-01 | `overlaps_via_supplier_response_and_actions`: phản hồi/hành động được chấp thuận khác với hành động được theo dõi. Không đồng nhất điều kiện đóng hai E2E. Nguồn §1–§2. |
| MAP-RET-REF-CAND | E2E-RET-01 → E2E-REF-01 | `candidate_handoff`, **suy luận cần xác nhận**: nguồn chưa nói nhận hàng là điều kiện bắt buộc trước chấp thuận hoàn tiền, cũng chưa nêu chứng từ bàn giao. |

Ba quan hệ đầu có `analysis_layer: As-Documented`, confidence `Medium`; quan hệ candidate có layer `null`, confidence `Low — Inferred`. Tất cả `Not reviewed`.

Thông báo khách hàng (`STEP-REC-NOTIFY`) và khóa xuất kho (`STEP-REC-HOLD`) thuộc phạm vi thu hồi theo §1. Chưa đủ boundary để dựng một E2E giao hàng lớn hơn từ riêng hoạt động xuất kho. Mô tả hiện có cũng chưa đủ để khẳng định toàn bộ các nhánh chạy tuần tự hay điều kiện đóng mọi hồ sơ giống nhau.

## 3. Một control, ba điểm gọi

`CTL-REC-07`: dịch vụ trung tâm kiểm tra mã lô/recall status. Căn cứ dùng chung là **cùng dịch vụ, cùng cấu hình và cùng cơ chế quản lý thay đổi** tại SRC-RECALL-03 §3; không chỉ vì trùng tên.

| Điểm sử dụng | Relationship ID | Vai trò và mapping E2E |
|---|---|---|
| STEP-SHP-CHECK — tại xuất kho | MAP-CTL-SHP | Hỗ trợ kiểm soát việc xuất lô thu hồi trong E2E-REC-01. Chưa chứng minh dịch vụ chính là toàn bộ cơ chế khóa xuất kho. |
| STEP-RET-CHECK — tại tiếp nhận trả | MAP-CTL-RET | Cùng một điểm kiểm tra thuộc E2E-RET-01 và hỗ trợ E2E-REC-01. |
| STEP-REF-GATE — trước duyệt hoàn tiền | MAP-CTL-REF | Cổng đầu vào `is_upstream_gate_for` E2E-REF-01, vì E2E này bắt đầu **sau chấp thuận**; đồng thời hỗ trợ E2E-REC-01. |

Cả ba quan hệ là `CTL-REC-07 → is_invoked_at → STEP-…`, `As-Documented`, nguồn §3, confidence `Medium`, `Not reviewed`. Không có căn cứ nói dịch vụ này cũng được gọi trong điều tra nhà cung cấp.

`COBJ-REC-01` — control objective suy ra, cần xác nhận: quyết định xuất kho, nhận trả và chấp thuận hoàn tiền phải nhất quán với đúng mã lô/trạng thái thu hồi.

`RSK-REC-01` — kịch bản suy luận: dữ liệu trạng thái sai/không kịp thời hoặc kết quả không được áp dụng → quyết định không phù hợp trạng thái lô → lô tiếp tục lưu thông hoặc khách hàng được xử lý sai → ảnh hưởng OBJ-REC-01. Đây không phải ghi nhận sự cố, không có chấm điểm hay ước lượng tổn thất.

Phạm vi control được mô tả chỉ là kiểm tra mã lô/trạng thái. Chưa đủ căn cứ để coi nó bao phủ tính đầy đủ thông báo, số tiền hoàn, đối chiếu công nợ hay chất lượng phản hồi nhà cung cấp. Owner, nguồn dữ liệu gốc, rule cụ thể, override/escalation và retention: `Not provided`; key-control status: `To be validated`; design assessment: `Not assessed`.

## 4. Giữ riêng mô tả và bằng chứng theo case

| Observation ID | Layer / phạm vi | Ghi nhận được hỗ trợ | Giới hạn |
|---|---|---|---|
| OBS-REC-07-DOC | As-Documented; ba điểm gọi; kỳ hiệu lực chưa được cung cấp | Mô tả một dịch vụ dùng chung theo SRC-RECALL-03 §3 | Không chứng minh mọi giao dịch đều gọi control. Chưa có cấu hình để lập observation As-Designed được xác nhận riêng. |
| OBS-REC-07-A | As-Performed; 15/07/2026; case A tại xuất kho | CTL-REC-07 trả `BLOCK`. SRC-LOG-03, case A | Không tự chứng minh caller đã chặn xuất kho hoặc không bị override. |
| OBS-REC-07-B | As-Performed; 15/07/2026; case B ở khâu hoàn tiền | CTL-REC-07 trả `REVIEW`. SRC-LOG-03, case B | Trace mô tả chưa nêu thời điểm so với phê duyệt; không chứng minh review hoàn tất, đã duyệt hoặc đã chi tiền. |

Hai kết quả khác nhau không tự là mâu thuẫn hay lý do tách control: đó là hai case/ngữ cảnh khác nhau; cần rule và input nếu muốn đánh giá kết quả đúng/sai. Confidence là `Medium` trong giới hạn trích trace được cung cấp; chưa kiểm tra raw log hay reperformance.

Giữ nguyên cảnh báo: **“Hồ sơ không bao phủ các giao dịch khác.”** Không tạo observation vận hành cho tiếp nhận trả hàng từ mô tả §3. Không suy tỷ lệ thực hiện, tỷ lệ lỗi hoặc operating effectiveness cho toàn bộ control/E2E. Phần đánh giá vận hành toàn bộ: `Not assessed / Insufficient evidence`.

## 5. Dùng lại ở nhiều view

Dữ liệu có cấu trúc nằm tại [model.json](/private/tmp/thien-rpc-phase3.xGeed0/P1-U03-V01-R1/model.json). Mỗi relationship có `from_id`, `relationship_type`, `to_id`, source, layer, confidence và review status.

- **E2E view:** lọc các quan hệ hỗ trợ/giao nhau theo `E2E-…`; một điểm kiểm tra có thể xuất hiện ở nhiều E2E.
- **Control view:** lấy một record `CTL-REC-07`, nối tới ba `STEP-…` và các observation riêng; đếm distinct control ID, không đếm số dòng join.
- **Evidence view:** lọc `OBS-…` theo layer, ngày và case. Không gộp DOC/A/B thành một assessment chung.
- **Risk/control view:** tái dùng `RSK-REC-01` và `COBJ-REC-01` với nhãn suy luận; không biến chúng thành risk rating hay control objective đã phê duyệt.

Theo nguyên tắc tách logical identity và observation của skill, thay đổi tên/view không làm đổi ID hoặc ghi đè nguồn. Khi bổ sung bằng chứng, thêm observation đúng kỳ/phạm vi.

Cần xác nhận tiếp: điều kiện bàn giao trả hàng → hoàn tiền; owner và quy tắc áp dụng BLOCK/REVIEW; cấu hình/nguồn status và bằng chứng caller thực thi ở cả ba điểm. Dùng chung cấu hình tạo khả năng lỗi ảnh hưởng đồng thời nhiều điểm, nhưng chưa đủ thông tin về dự phòng và workaround để kết luận SPOF. Không có đủ dữ kiện xác định thêm control dùng chung; điều này không có nghĩa chúng không tồn tại.

Nguồn phân tích: [input.md](</Users/thiendeptrainhat/Documents/Thien's Skills Library/Thien-Risk-Process-Control/tests/phase-3/fixtures/P1-U03-V01/input.md>), các locator SRC-RECALL-03 §1–§3 và SRC-LOG-03 nêu tại từng nhận định. Không dùng nguồn ngoài.

