# Platform guidance — Phase 3

## 1. Phạm vi và ngày kiểm tra

- Ngày mở nguồn chính thức: **28/08/2026**, múi giờ Asia/Ho_Chi_Minh.
- Phạm vi: hướng dẫn cài đặt cho một canonical skill và ba ZIP mục tiêu `1.1.0`; không phải chứng nhận tương thích mọi nền tảng.
- Không cài skill, upload ZIP, đăng nhập ứng dụng, cấu hình connector hoặc chạy live-platform acceptance trong tiểu tác vụ tài liệu này.
- Tài liệu dùng kết quả đọc nguồn, không dùng search snippets hoặc API capability để suy ra quyền/tính năng của giao diện ChatGPT/Claude.
- Trạng thái build, behavioral và release acceptance phải lấy từ [manifest](../../RELEASE-MANIFEST.yaml) và các [báo cáo kiểm thử](../../tests/), đúng version/run.

## 2. Nguồn đã mở và giới hạn kết luận

| ID | Nguồn chính thức | Nội dung hỗ trợ trực tiếp | Giới hạn |
|---|---|---|---|
| OA-01 | [Build skills](https://learn.chatgpt.com/docs/build-skills) | Standalone skills trên desktop/CLI/IDE; Codex local dùng `.agents/skills`; web distribution qua plugin | Không xác nhận tài khoản, nút import ZIP chung hoặc mọi chế độ ChatGPT đọc cùng local path |
| OA-02 | [Skills & Plugins](https://learn.chatgpt.com/docs/skills-and-plugins) | Phân biệt skill/plugin và cách gọi `@` trong ChatGPT, `$` trong Codex | Enable/install được mô tả ở mức workflow, không có quy trình import ba ZIP của repository này |
| OA-03 | [ChatGPT desktop app](https://learn.chatgpt.com/docs/app) | Phân biệt chọn ChatGPT với Codex, cùng các chế độ Chat/Work trong ứng dụng | Không chứng minh discovery của một skill local trên mọi mode hoặc account |
| OA-04 | [ChatGPT on the web](https://learn.chatgpt.com/docs/web) | Files, skills và plugins hỗ trợ workflows trên web | Không có chỉ dẫn native standalone ZIP importer cho gói này trong nội dung đã đọc |
| AN-01 | [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) | Custom ZIP upload trong Skills, yêu cầu code execution và quyền theo workspace | Có hướng dẫn không có nghĩa UI của user đã bật tính năng hoặc upload đã thành công |
| AN-02 | [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) | ZIP gồm một skill folder cấp đầu; trang UI nêu description tối đa 200 ký tự | Không thay bằng constraint khác lấy từ API; vẫn cần kiểm tra gói và upload thực tế riêng |
| AN-03 | [Claude directory guide](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory) | Customize có trên Claude và Claude Desktop | Directory/install skill từ catalog không đồng nghĩa repository private này đã có trong catalog |
| AN-04 | [Claude Code skills](https://code.claude.com/docs/en/skills) | Personal/project `.claude/skills`, gọi bằng slash; local discovery khác account-enabled skills | Không dùng đường dẫn CLI để suy rằng Claude Web/Desktop đã cài custom ZIP |

URL cũ [developers.openai.com/codex/skills/](https://developers.openai.com/codex/skills/) chuyển hướng tới OA-01 khi mở ngày kiểm tra; hướng dẫn mới trỏ thẳng đến trang đích. Không dùng ngày crawl hoặc version của Codex CLI làm ngày xác minh hành vi của skill.

Đây là tóm tắt phạm vi nội dung đã đọc, không bundle bản sao tài liệu nền tảng. Các bước cụ thể nằm trong [INSTALL.md](../../INSTALL.md).

## 3. Quan sát cục bộ

Lệnh chỉ để đọc phiên bản:

```text
~/.local/bin/codex --version
codex-cli 0.146.0
```

Lệnh trả exit code 0 và cảnh báo không tạo được PATH aliases do quyền hệ thống. Không sửa quyền, PATH hoặc cài/nâng cấp gì để xử lý cảnh báo. Quan sát này chỉ xác nhận executable trả phiên bản, không xác nhận đã nạp skill, có session đăng nhập hoặc đã chạy behavioral test.

## 4. Ma trận quyết định cài đặt

| Bề mặt | Artifact/cách dùng trong phạm vi hiện tại | Bằng chứng còn cần tại tài khoản đích |
|---|---|---|
| Claude Web | Claude ZIP, native Custom Skills upload theo AN-01/AN-02 | Quyền upload/enable, host chấp nhận gói và nạp đúng version |
| Claude Desktop | Cùng Claude ZIP khi UI có Custom Skills; không thay bằng local Claude Code folder | Xác nhận UI/mode và scope tài khoản thực tế |
| Codex local trong desktop, CLI hoặc IDE | Universal wrapper cho project; ChatGPT ZIP không wrapper cho personal directory | Host discovery/activation và behavior của bản được nạp |
| ChatGPT Desktop ngoài Codex local | Giữ Universal làm package giải nén đã chọn; chỉ coi là native install khi host xác nhận discovery | Cơ chế local/import cụ thể, vị trí được host đọc và mode; chưa suy từ OA-01 phần Codex |
| ChatGPT Web | Ba standalone ZIP không có quy trình native import đã xác minh | Nếu đi theo plugin distribution: hạng mục packaging, quyền phân phối và acceptance riêng |
| Claude Code | Claude ZIP vào `.claude/skills` đúng scope | Discovery/activation của CLI thực tế |

Một artifact được giải nén đúng chưa chứng minh discovery; discovery chưa chứng minh activation cho task; activation chưa chứng minh chất lượng output. Bản ghi này không điền thay trạng thái runtime trong release report.

## 5. Quyết định đóng gói và ranh giới

Giữ đúng ba tên:

- `Thien-Skill-Risk-Process-Control-v1.1.0-Claude.zip`
- `Thien-Skill-Risk-Process-Control-v1.1.0-ChatGPT.zip`
- `Thien-Skill-Risk-Process-Control-v1.1.0-Universal.zip`

Claude/ChatGPT có `thien-skill-risk-process-control/` tại root ZIP; Universal có `.agents/skills/thien-skill-risk-process-control/`. Đây là quyết định đóng gói của repository, không là tuyên bố nhà cung cấp công nhận tên gói. Wrapper Universal được giữ theo phương án đã thống nhất, không tự đổi thành `.agent`, plugin hoặc installer.

Các giới hạn cần giữ trong README/INSTALL:

- Không gọi đính kèm ZIP vào chat/Project Files/Knowledge là native installation.
- Không suy khả năng ChatGPT Web/Desktop từ Codex local hoặc Skills API.
- Không tự khẳng định nút upload/import tồn tại; nếu chưa có bằng chứng, ghi điều kiện và dừng ở trạng thái đặt file.
- Không dùng một lần tạo file hoặc một prompt smoke test để công bố mọi platform đã đạt.
- Không thêm plugin/connector nhằm lấp khoảng trống phân phối web khi chưa được phê duyệt.
- Không đồng nhất quyền GitHub, license của skill và quyền xử lý các tài liệu được đưa vào engagement.

## 6. Kiểm tra trước khi bàn giao release

1. Đối chiếu version và tên ba ZIP với manifest/checksum; không link bản `1.0.0` như bản `1.1.0`.
2. Kiểm tra wrapper, entrypoint và metadata của từng artifact; giới hạn description UI Claude ở AN-02 cần được đối chiếu với canonical description.
3. Giữ một nội dung nghiệp vụ, nguyên license/notice/attribution; không tạo nhánh chuyên môn riêng theo host.
4. Báo đúng những gì đã chạy ở từng môi trường. Trạng thái thiếu run evidence không được tự đổi thành pass.
5. Nếu user cần native ChatGPT Web hoặc một import flow chưa được tài liệu xác lập, ghi nhu cầu riêng để quyết định; không tự triển khai hoặc giả định hỗ trợ.

Việc chuẩn bị ba ZIP và tài liệu không cần thay quyết định một skill lõi. Khoảng trống native web/import chỉ giới hạn claim triển khai; không ngăn bàn giao package với giới hạn rõ ràng.
