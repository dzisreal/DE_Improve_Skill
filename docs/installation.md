# Cài đặt global trên Linux và macOS

## Phạm vi và yêu cầu

- Git để clone repository; Python 3.9+ để chạy installer và test.
- Codex đã được cài và cấu hình để sử dụng skills. Xem hướng dẫn chính thức tại
  <https://developers.openai.com/codex/> nếu máy chưa có Codex.
- Gói này không cần Node.js, pip package, Docker hay cloud credential.
- `~/.agents/skills/` là phạm vi user-global của máy chạy lệnh. Nó không tự đồng
  bộ giữa Mac, Linux, container, tài khoản khác hoặc cloud workspace mới.
- Không chạy installer bằng `sudo`: cần cài vào home của người dùng Codex.

## Linux

Kiểm tra công cụ:

```sh
git --version
python3 --version
```

Nếu thiếu, ví dụ trên Ubuntu/Debian:

```sh
sudo apt-get update
sudo apt-get install -y git python3 unzip
```

Các bản phân phối khác dùng package manager tương ứng. Sau đó:

```sh
git clone https://github.com/dzisreal/DE_Improve_Skill.git
cd DE_Improve_Skill
# Chỉ cần trước khi PR đầu được merge; sau đó dùng main hoặc commit đã chọn.
git switch feat/global-de-skills-bootstrap
python3 scripts/validate_bundle.py
python3 codex-global-skills/install.py --check
python3 codex-global-skills/install.py
```

## macOS, bao gồm Apple Silicon

Kiểm tra `git --version` và `python3 --version`. Nếu thiếu Git, cài Command Line
Tools bằng `xcode-select --install`. Nếu máy đã có Homebrew, có thể cài Python bằng
`brew install python`. Nếu không dùng Homebrew, dùng installer từ
<https://www.python.org/downloads/macos/>. Chọn Python 3.9 trở lên.

```sh
git clone https://github.com/dzisreal/DE_Improve_Skill.git
cd DE_Improve_Skill
git switch feat/global-de-skills-bootstrap
python3 scripts/validate_bundle.py
python3 codex-global-skills/install.py --check
python3 codex-global-skills/install.py
```

Sau merge, thay nhánh PR bằng `main` hoặc commit đã chọn. Bộ cài chỉ copy tài liệu
và script Python, không có binary phụ thuộc Intel/ARM; chưa cần cài Spark hoặc JVM.

## Cài từ ZIP, dùng trên máy khác hoặc offline

Từ một checkout có Python, tạo ZIP:

```sh
python3 scripts/package_skills.py
```

Chuyển cả `dist/codex-global-skills.zip` và file `.sha256` đi kèm sang máy đích.
Hoặc tải artifact của job CI tương ứng trong tab Actions; giải nén artifact của
GitHub trước để lấy ZIP nội bộ và file checksum.

Linux:

```sh
sha256sum -c codex-global-skills.zip.sha256
unzip codex-global-skills.zip
cd codex-global-skills
python3 install.py --check
python3 install.py
```

macOS:

```sh
shasum -a 256 -c codex-global-skills.zip.sha256
unzip codex-global-skills.zip
cd codex-global-skills
python3 install.py --check
python3 install.py
```

Không cần kết nối upstream khi cài. Checksum kiểm tra nội dung theo bundle đã lấy;
nó không chứng minh nguồn tải là đáng tin nếu cả ZIP và checksum đều bị thay thế.

## Xác minh

```sh
python3 codex-global-skills/install.py --check
```

Với ZIP, chạy `python3 install.py --check` trong thư mục vừa giải nén. Lệnh này
không ghi file; chỉ kiểm tra bundle, xung đột và báo số skill chưa cài. Sau cài
thành công phải thấy `0 skills not installed`. Không diễn giải exit code 0 của
`--check` trước cài là đã cài xong.

Mở chat Codex mới và gọi một tên skill, ví dụ `$data-architect`. Với CLI hỗ trợ
app-server, có thể kiểm tra machine-readable từ repo:

```sh
python3 scripts/verify_codex_discovery.py
```

Script chỉ hỏi danh sách skills, không gọi model. Nó có thể tạo state/cache của
Codex trong home người dùng; máy phải cho phép Codex ghi state. CLI quá cũ hoặc
khác phiên bản protocol có thể không hỗ trợ. Khi đó kiểm tra trong chat mới.

## Đường dẫn tùy chọn

```sh
python3 codex-global-skills/install.py --destination /absolute/path/to/skills
```

Một đường dẫn tùy ý **không tự trở thành đường dẫn Codex khám phá**. Dùng tùy chọn
này cho staging/test hoặc thư mục đã được Codex cấu hình hỗ trợ. Mặc định vẫn là
`~/.agents/skills/`. Installer từ chối đích có symlink; nếu đó là cấu hình chủ ý,
truyền đường dẫn thật đã resolve và kiểm tra lại Codex discovery.

## Cập nhật và rollback

Cài lại cùng nội dung là idempotent. Installer không tự ghi đè phiên bản khác hay
chỉnh sửa cá nhân. Để cập nhật:

1. Ghi lại commit đang dùng; commit hoặc sao lưu các chỉnh sửa cá nhân nếu có.
2. Lấy phiên bản repo mới và chạy validator.
3. Di chuyển **chỉ các thư mục skill thuộc bundle** sang thư mục backup ngoài
   `~/.agents/skills/` để Codex không phát hiện trùng tên. Đừng đổi tên thư mục backup
   ngay trong cây skills vì bộ khám phá có thể vẫn quét nó.
4. Chạy installer rồi kiểm tra discovery và mở chat mới.
5. Nếu cần rollback, di chuyển bản mới ra ngoài cây skills, phục hồi thư mục backup
   đúng tên và mở chat mới. Không xóa bản có chỉnh sửa chưa được sao lưu.

Danh sách đúng năm thư mục cần quản lý nằm trong `manifest.json` và bảng ở README.
Để gỡ bỏ, di chuyển năm thư mục đó ra ngoài `~/.agents/skills/`; các built-in và
skills khác không bị ảnh hưởng. Không xóa toàn bộ thư mục `~/.agents`.

## Lỗi thường gặp

| Thông báo | Xử lý |
|---|---|
| `Existing skill differs` | So sánh/sao lưu bản đang có, rồi làm theo quy trình cập nhật; không ép ghi đè |
| `Bundle checksum mismatch` | Lấy lại checkout/ZIP đúng phiên bản; nếu đang phát triển, review thay đổi và cập nhật manifest có chủ đích |
| `Permission denied` | Xác nhận đang chạy bằng tài khoản đúng và home có thể ghi; trong cloud xin quyền đúng phạm vi |
| `Destination must not contain symlinks` | Kiểm tra symlink, truyền đường dẫn thật nếu đó là lựa chọn có chủ đích |
| Cài xong nhưng không thấy skill | Mở chat mới, kiểm tra user/home/host và khả năng khám phá `~/.agents/skills/` của bản Codex đang dùng |
| Skill đòi MCP nhưng chưa kết nối | Báo thiếu bằng chứng hoặc cung cấp log mẫu; các JSON đi kèm chỉ là template, chưa kết nối dịch vụ |
