# Phần bổ sung cho mô hình 1.1.0 — bản dự thảo

Đã lập phần bổ sung **tách riêng khỏi record 1.0.0**. Cách này giữ nguyên logical control `CTL-L001`, hai liên kết với `RSK-L001` và `RSK-L002`, toàn bộ giá trị, `null`, locator và `schema_version: "1.0.0"` của hai khối gốc.

Cảnh báo nguồn được giữ nguyên:

> SYNTHETIC TEST DATA; authorized for AI processing. These are retained legacy records, not new source evidence.

## Tệp bàn giao

- [Bản JSON gốc 1.0.0](/private/tmp/thien-rpc-phase3.xGeed0/P1-U22-V01-R1/legacy-1.0.0.json): bản sao phần JSON đầu vào, không thêm hoặc sửa field. Cảnh báo nguồn nằm ở trên và trong sidecar.
- [Phần bổ sung 1.1.0](/private/tmp/thien-rpc-phase3.xGeed0/P1-U22-V01-R1/supplement-1.1.0.json): đọc cùng bản gốc; đây là envelope sidecar đề xuất, chưa phải schema tích hợp được consumer cụ thể chấp nhận.

Mục tiêu là bảo toàn dữ liệu và bổ sung quan hệ/metadata; không tái đánh giá kiểm soát. `analysis_layer: null`, confidence `Unresolved`, review status `Not reviewed`; không có giả định nghiệp vụ mới.

## Ánh xạ bổ sung

| Thành phần | Cách xử lý |
|---|---|
| Logical control | Chỉ một `CTL-L001`; không nhân bản theo hai risks. |
| Control objective | Thêm `control_objective_ids: ["COBJ-L001"]`, giữ nguyên singular `control_objective_id` trong bản gốc. |
| RCM | Hai relationship mới `RCM-ADD-001` và `RCM-ADD-002` tham chiếu hai dòng gốc và cùng `CTL-L001`. Đây là ID quan hệ mới, không thay ID nghiệp vụ. |
| Observations | `control_observations: []`, `control_observation_ids: []`, `legacy_projection_observation_id: null`; các relationship cũng giữ observation/layer/scope/period là `null`. |
| Assessment mới | `assessment_status: "Not assessed"`, `evidence_status: "Not checked"` chỉ áp dụng việc tái đánh giá chưa thực hiện, không ghi đè kết luận legacy. |
| Source-use | Tách nội dung JSON đã đọc khỏi `Legacy.xlsx` và `SOP-5` chưa đọc. Quyền AI được nêu cho đầu vào tổng hợp; không suy quyền hoặc xác minh cho nguồn được trích dẫn. |

`design_assessment` trong control và cả hai dòng RCM vẫn giữ nguyên:

> Adequate design per 2025 review; operating effectiveness not assessed.

Không thay chuỗi này bằng `Not assessed`, không biến nó thành đánh giá thiết kế hiện tại hoặc kết luận operating effectiveness. Các trường `evidence: null`, `control_owner: null`, `analysis_layer: null` và cả hai `residual_risk: null` được bảo toàn.

## Những phần chưa thể xác nhận

- **Layer, scope và kỳ:** record không cho biết. Trích dẫn SOP không đủ để gán `As-Documented`; cụm “2025 review” không đủ để tự điền kỳ observation. Không gán `As-Designed` hoặc `As-Performed`.
- **Nguồn và assessment:** chưa có nội dung `Legacy.xlsx:Controls!D7`, `SOP-5 section 4.2` hoặc hồ sơ review 2025 để kiểm tra version, hiệu lực, phạm vi và căn cứ đánh giá. Metadata xác nhận đã đọc JSON không xác nhận các nguồn đó.
- **Owner và thực hiện:** “Preparer” trong mô tả không xác định control owner; chưa có bằng chứng thực hiện, người chịu trách nhiệm hoặc operating effectiveness.
- **Định nghĩa các object liên quan:** chưa có record định nghĩa `RSK-L001`, `RSK-L002`, `COBJ-L001`. Chỉ xác nhận được ID và quan hệ được ghi trong đầu vào, chưa kiểm tra đầy đủ nội dung risk/control objective. Không tạo object giả để lấp thiếu.
- **Residual risk và coverage:** không có phương pháp rating được phê duyệt hay bằng chứng để đánh giá. Giữ `null`; thiếu dữ liệu không có nghĩa control failed hoặc rủi ro bằng 0.
- **Tích hợp:** chưa có consumer/schema validator cụ thể để kiểm thử. Với consumer 1.0.0 strict-schema, chỉ đưa bản gốc vào consumer và giữ sidecar riêng; không cam kết consumer cũ sẽ nhận field mới.

Khi có nguồn và xác nhận layer/phạm vi/kỳ, có thể tạo observation riêng nối về `CTL-L001`; chỉ điền projection ID nếu projection thực sự lấy từ observation đó. Nếu việc tích hợp buộc thay đổi hoặc làm mất nghĩa record gốc, cần quyết định schema trước khi tiếp tục.

Phần bổ sung tuân theo quy tắc legacy-compatible của skill: dữ liệu gốc bất biến, extension có thể thiếu, không suy performance từ record lưu trữ. Đây là bản dự thảo chờ người quản trị dữ liệu xem xét; không phải kết luận assurance.
