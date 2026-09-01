# Cài đặt Thien-Skill-Risk-Control-Process 1.2.0

Hướng dẫn cho ba ZIP `1.2.0` tại `dist/1.2.0/`. Đối chiếu ZIP và checksum/version trong [RELEASE-MANIFEST.yaml](RELEASE-MANIFEST.yaml) trước khi dùng. Đây là minor release bổ sung hành vi R07, guard cho compliance label và hardening tooling/repository hygiene. [Báo cáo Phase 3](docs/phase-3/REPORT.md) vẫn chỉ phản ánh tên cũ `1.1.0`; qualification riêng của `1.2.0` nằm tại [tests/release-1.2.0](tests/release-1.2.0/README.md).

## 1. Chuẩn bị và hiểu cấu trúc ZIP

Repository hiện [public](https://github.com/thiendeptrainhat/Thien-Skill-Risk-Control-Process); việc công khai không thay điều khoản license. Chọn **file ZIP trong `dist/1.2.0/`**, không upload nguyên ZIP repository từ GitHub. Các release cũ trong `dist/` được giữ riêng làm lịch sử.

| File | Đường dẫn đến entrypoint bên trong archive |
|---|---|
| `Thien-Skill-Risk-Control-Process-v1.2.0-Claude.zip` | `thien-skill-risk-control-process/SKILL.md` |
| `Thien-Skill-Risk-Control-Process-v1.2.0-ChatGPT.zip` | `thien-skill-risk-control-process/SKILL.md` |
| `Thien-Skill-Risk-Control-Process-v1.2.0-Universal.zip` | `.agents/skills/thien-skill-risk-control-process/SKILL.md` |

Claude không có `agents/` metadata OpenAI; ChatGPT và Universal có. Nội dung process/risk/control, license và assets cùng lấy từ một canonical skill.

Trước khi cài:

1. Đọc [LICENSE](LICENSE), [LICENSE-APPLICATION.md](LICENSE-APPLICATION.md), [NOTICE](NOTICE) và [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
2. So SHA-256 với checksum đúng phiên bản. Ví dụ trên macOS:

```bash
shasum -a 256 "/path/to/Thien-Skill-Risk-Control-Process-v1.2.0-Claude.zip"
```

3. Xem danh sách file nếu cài local:

```bash
unzip -l "/path/to/Thien-Skill-Risk-Control-Process-v1.2.0-Universal.zip"
```

4. Chọn một scope cài. Nếu đã có thư mục cùng skill ID, dừng bước giải nén và làm theo [mục cập nhật](#8-cập-nhật-và-gỡ-lỗi); không ghi đè hoặc trộn bản cũ.

Các lệnh bên dưới là hướng dẫn để người dùng tự thực hiện, không phải bằng chứng đã cài. Thay `/path/to/...` bằng đường dẫn thật và giữ dấu ngoặc kép nếu có khoảng trắng.

## 2. Claude Web và Claude Desktop

Anthropic hướng dẫn upload ZIP trong **Customize > Skills**; code execution và quyền tạo skill phải được cho phép. Nếu mục này bị ẩn hoặc bị quản trị chặn, cần xử lý quyền với chủ tài khoản/workspace, không tìm cách vượt chặn. [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

Thực hiện trên bề mặt Claude có Custom Skills:

1. Tải gói **Claude**, giữ nguyên ZIP.
2. Mở **Customize > Skills → + → Create skill → Upload a skill**.
3. Chọn ZIP Claude, chờ host xử lý và bật skill trong danh sách.
4. Dùng prompt phù hợp ở [mục xác nhận](#7-xác-nhận-đúng-mức), với dữ liệu không nhạy cảm.

Đây là upload custom skill, không phải đính kèm ZIP vào một cuộc chat. Claude Desktop cũng có khu vực Customize; việc ứng dụng cụ thể có cho upload và bật skill vẫn cần kiểm tra trong tài khoản. [Claude directory guide](https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory).

Gói có một thư mục skill ở cấp đầu archive. Khi tự tùy chỉnh, giữ `SKILL.md` và tài nguyên trong cùng thư mục; đối chiếu giới hạn metadata của giao diện trước upload. [Create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills).

## 3. Codex local

OpenAI mô tả local discovery ở `.agents/skills` trong repository và `~/.agents/skills` cho user. Chọn một trong hai cách dưới đây. [Build skills — local locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

### Project scope — Universal ZIP

Giải nén **tại project root**, không phải bên trong `.agents/skills`:

```bash
unzip "/path/to/Thien-Skill-Risk-Control-Process-v1.2.0-Universal.zip" -d "/path/to/project"
```

Entry point phải là:

```text
/path/to/project/.agents/skills/thien-skill-risk-control-process/SKILL.md
```

### User scope — ChatGPT ZIP

Gói ChatGPT không có wrapper `.agents`, nên dùng đích là thư mục skills:

```bash
mkdir -p ~/.agents/skills
unzip "/path/to/Thien-Skill-Risk-Control-Process-v1.2.0-ChatGPT.zip" -d ~/.agents/skills
```

Entry point phải là:

```text
~/.agents/skills/thien-skill-risk-control-process/SKILL.md
```

Mở phiên Codex local sử dụng scope đó; kiểm tra bằng `/skills` hoặc `$thien-skill-risk-control-process`. Nếu thay đổi chưa xuất hiện, khởi động lại Codex. [Build skills](https://learn.chatgpt.com/docs/build-skills).

Không tự chuyển hướng dẫn local này thành hướng dẫn cho Codex cloud, remote host hoặc ChatGPT Web; mỗi môi trường cần tài nguyên và quyền riêng.

## 4. ChatGPT Desktop

OpenAI xác nhận standalone skills và mục **Skills** trên ứng dụng desktop. Tuy nhiên nguồn đã đọc chưa xác lập một thao tác native import ZIP chung cho mọi tài khoản, cũng chưa đủ để khẳng định mọi chế độ Chat/Work đọc đường dẫn Codex local. [Build skills](https://learn.chatgpt.com/docs/build-skills).

Phương án đã thống nhất cho repository này vẫn là **Universal ZIP → `.agents/skills/`**:

1. Xác định đang dùng Codex local trong ứng dụng hay một bề mặt ChatGPT khác. Tài liệu ứng dụng phân biệt các lựa chọn này. [ChatGPT desktop app](https://learn.chatgpt.com/docs/app).
2. Với Codex local, làm theo [mục 3](#3-codex-local). Với host khác có cơ chế đọc local skills đã được xác nhận, đặt nguyên skill vào thư mục discovery của host đó; không mặc định đường dẫn chỉ từ tên ứng dụng.
3. Với Universal, giải nén vào **thư mục cha của `.agents`**. Nếu đã có `.agents`, không tạo thêm `.agents` lồng bên trong. Cho user scope, kết quả cuối là `~/.agents/skills/thien-skill-risk-control-process/SKILL.md`.
4. Mở Skills và xác nhận skill thực sự được nhận. Chọn bằng `@` khi bề mặt hỗ trợ; [cách gọi của ChatGPT](https://learn.chatgpt.com/docs/skills-and-plugins).

Nếu chỉ thấy file trên đĩa nhưng không có skill trong host, trạng thái mới là **đã giải nén**, chưa phải **đã cài/kích hoạt**. Không đổi đuôi ZIP, đoán nút import hoặc upload vào chat để thay cho native installation. Gói ChatGPT có thể cung cấp cùng thư mục skill khi host yêu cầu folder; định dạng import cụ thể phải theo hướng dẫn của chính host.

## 5. ChatGPT Web

Tài liệu web mô tả workflows bằng files, skills và plugins, nhưng không cung cấp quy trình import standalone ZIP của repository này. [ChatGPT on the web](https://learn.chatgpt.com/docs/web).

Đường phân phối skills trên web được OpenAI nêu là qua plugin. Ba ZIP của repository **không phải plugin package**; không có claim đã được đưa vào plugin directory hoặc đã cài trên ChatGPT Web. [Build skills — distribution](https://learn.chatgpt.com/docs/build-skills#distribute-skills-with-plugins).

Vì vậy:

- không dùng upload ZIP vào chat, Project Files hoặc Knowledge như bằng chứng native skill đã cài;
- giải nén `.agents` trên máy không tự cài sang ChatGPT Web;
- có thể dùng tài liệu được phép làm context khi host đọc được, nhưng phải gọi đúng là sử dụng nội dung tham khảo, không phải native activation;
- muốn phân phối native trên web theo đường plugin cần một hạng mục đóng gói/kiểm thử riêng được phê duyệt; không tự thêm plugin hoặc connector trong bản này.

## 6. Claude Code

Claude Code dùng `.claude/skills`, khác `.agents/skills` của Codex. Chọn project scope:

```bash
mkdir -p "/path/to/project/.claude/skills"
unzip "/path/to/Thien-Skill-Risk-Control-Process-v1.2.0-Claude.zip" -d "/path/to/project/.claude/skills"
```

Hoặc user scope:

```bash
mkdir -p ~/.claude/skills
unzip "/path/to/Thien-Skill-Risk-Control-Process-v1.2.0-Claude.zip" -d ~/.claude/skills
```

Kết quả là `<scope>/.claude/skills/thien-skill-risk-control-process/SKILL.md`. Gọi `/thien-skill-risk-control-process`. Nếu thư mục skills chưa tồn tại khi phiên bắt đầu, khởi động lại để host nhận vị trí mới. [Claude Code — skills](https://code.claude.com/docs/en/skills).

Cài thư mục Claude Code trên máy không phải thao tác upload custom skill của Claude Web/Desktop.

## 7. Xác nhận đúng mức

| Mức kiểm tra | Cần thấy gì | Không được suy ra |
|---|---|---|
| Artifact | ZIP đúng version/hash; đủ entrypoint, references, templates, assets và license | Host đã nhận skill |
| Discovery | Skill xuất hiện trong danh sách đúng scope/tài khoản | Model đã nạp skill cho task cụ thể |
| Activation | Host trace hoặc bằng chứng nạp đúng skill khi khả dụng | Câu trả lời nghiệp vụ đã đúng |
| Behavior | Output/source trace đáp ứng tiêu chí của case đã chạy | Mọi ngành, dữ liệu hoặc platform đều đạt |

Prompt thử:

```text
Dùng Thien-Skill-Risk-Control-Process. Đây là mô tả giả lập: nhân viên gửi
yêu cầu mua hàng, quản lý duyệt trên email, kế toán thanh toán theo hóa đơn.
Chỉ có mô tả này, chưa có log/evidence vận hành hoặc baseline được xác minh.
Phân tích E2E candidates, risk/control questions và phần cần xác nhận.
Không coi thiếu thông tin là control không tồn tại; không tự tạo risk score.
```

Kết quả cần giữ được giới hạn đầu vào, tách documented/performed, không bịa baseline và không tự mở rộng quyền. Một prompt smoke test chưa phải nghiệm thu đầy đủ.

## 8. Cập nhật và gỡ lỗi

Khi cập nhật từ `1.1.1` lên `1.2.0`, skill ID vẫn là `thien-skill-risk-control-process`. Sao lưu tùy chỉnh, dùng cơ chế quản lý skill của host để thay bản cũ bằng một cây `1.2.0` hoàn chỉnh; không trộn file giữa hai phiên bản. Về lịch sử, bản `1.1.1` đã đổi ID cũ `thien-skill-risk-process-control` thành ID hiện tại; nếu nâng trực tiếp từ `1.1.0` hoặc cũ hơn, không giữ cả hai ID cùng kích hoạt và không tự xóa bản cũ chưa đối chiếu.

Khi cập nhật:

1. Tải ZIP mới và checksum cùng version.
2. Giữ bản sao tùy chỉnh cũ **ngoài** các thư mục skill mà host scan; đổi tên thư mục nhưng giữ cùng frontmatter name vẫn có thể tạo bản trùng.
3. Đối chiếu thay đổi; thay bản cũ bằng một thư mục mới hoàn chỉnh hoặc cơ chế cập nhật của UI. Không trộn file hai phiên bản.
4. Kiểm tra lại discovery, activation và một case phù hợp; giữ record/version cũ khi cần đối chiếu.

| Vấn đề | Kiểm tra trước |
|---|---|
| Không thấy `.agents` sau giải nén | File manager có đang ẩn thư mục bắt đầu bằng dấu chấm không; xác nhận đường dẫn entrypoint |
| Skill không xuất hiện | Đúng host, scope, tên thư mục, `SKILL.md`, quyền và trạng thái enable; không suy từ tên ZIP |
| Đường dẫn lồng `.agents/skills/.agents/skills` | Universal đã bị giải nén sai cấp; đặt lại nguyên cây đúng vị trí, không sửa IDs để chữa lỗi |
| Claude từ chối ZIP | Đúng gói Claude, một skill folder cấp đầu, metadata theo giới hạn UI và quyền upload; không dùng giới hạn API thay giới hạn giao diện |
| Model không dùng skill | Chọn/gọi rõ skill và xem trace khi có; kiểm tra đúng phiên bản được nạp |
| Scan hoặc bảng không đọc được | Giữ partial coverage; dùng capability/specialist được phép hoặc yêu cầu bản rõ, không giả đã OCR |
| Nguồn standards bị chặn | Giữ limitation/proposal có nhãn; không mua, đăng nhập hoặc dùng mirror để vượt quyền |

## 9. Phạm vi xác minh và quyền sử dụng

Nguồn hướng dẫn được mở ngày **28/08/2026**; xem [Platform guidance](docs/phase-3/PLATFORM-GUIDANCE.md). Không cài thử, upload hoặc đăng nhập live platforms để viết hướng dẫn này. Kết quả Phase 3 phải được xem riêng trong báo cáo và manifest của đúng phiên bản.

Có ZIP, quyền GitHub hoặc cài thành công không tự cấp quyền sử dụng/sửa đổi/phân phối. Giữ license, notice và attribution đi kèm; ưu tiên bản tiếng Việt và cơ chế pháp luật/tòa án Việt Nam theo nội dung license.
